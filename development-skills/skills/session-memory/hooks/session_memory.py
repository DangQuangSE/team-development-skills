#!/usr/bin/env python3
"""Load useful context from the current or another AI coding session.

Claude hook behavior:
  - SessionStart/startup: inject a bounded summary of the nearest previous
    session for the same project.
  - UserPromptSubmit: recognize explicit requests such as
    ``/session read "API migration"`` and inject that session's summary.

Codex uses the same behavior through ``--provider codex`` and reads
``~/.codex/session_index.jsonl`` plus Codex rollout JSONL files. Compatible
providers can use the plain-text output mode with ``--provider generic``.

The hook never injects a raw transcript.
Only titles, user prompts, and short assistant text are included so a long old
session cannot consume the new session's context window.

CLI behavior:
  python session_memory.py --provider codex list
  python session_memory.py --provider codex read <session-name>
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

sys.path.insert(0, str(Path(__file__).parent / "lib"))
from ck_config_utils import find_project_root, get_claude_dir, get_home_dir, get_sessions_dir
from hook_logger import HookLogger, strip_ansi


MAX_INPUT = 1024 * 1024
MAX_CONTEXT_CHARS = 9000
MAX_EXPLICIT_CONTEXT_CHARS = 14000
MAX_MESSAGE_CHARS = 700
MAX_RECORDS = 120
MAX_GLOBAL_RECORDS = 240
_log = HookLogger("session-memory")


@dataclass
class SessionRecord:
    """Small index entry and selected conversation excerpts for one session."""

    path: Path
    session_id: str
    title: str = ""
    first_user: str = ""
    recent_users: list[str] = field(default_factory=list)
    recent_assistant: list[str] = field(default_factory=list)
    first_timestamp: str = ""
    workdir: str = ""
    mtime: float = 0.0

    @property
    def name(self) -> str:
        if self.title:
            return self.title
        if self.first_user:
            compact = re.sub(r"\s+", " ", self.first_user).strip()
            return compact[:72] + ("..." if len(compact) > 72 else "")
        return f"session-{self.session_id[:8]}"


def _event_value(event: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = event.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _input_event() -> dict[str, Any]:
    try:
        raw = sys.stdin.read(MAX_INPUT)
        value = json.loads(raw) if raw.strip() else {}
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def _claude_projects_dir() -> Path:
    override = os.environ.get("CLAUDE_PROJECTS_DIR")
    if override:
        return Path(override).expanduser()
    return get_claude_dir() / "projects"


def _encoded_project_name(cwd: str) -> str:
    """Match Claude's project directory encoding on Windows and Unix."""
    normalized = cwd.replace("/", "\\")
    drive_match = re.match(r"^([A-Za-z]):(.*)$", normalized)
    if drive_match:
        return (drive_match.group(1).lower() + "-" + drive_match.group(2).replace("\\", "-")).rstrip("-")
    return normalized.replace("\\", "-").replace("/", "-").strip("-")


def _transcript_dir(event: dict[str, Any]) -> Path | None:
    transcript = _event_value(event, "transcript_path") or os.environ.get("CLAUDE_TRANSCRIPT_PATH", "")
    if transcript:
        path = Path(transcript).expanduser()
        if path.parent.exists():
            return path.parent

    cwd = _event_value(event, "cwd", "project_dir") or os.environ.get("CLAUDE_PROJECT_DIR", "") or os.getcwd()
    projects_dir = _claude_projects_dir()
    encoded = _encoded_project_name(cwd)
    candidates = []
    try:
        candidates = [p for p in projects_dir.iterdir() if p.is_dir() and p.name.casefold() == encoded.casefold()]
    except OSError:
        return None
    if candidates:
        return candidates[0]
    direct = projects_dir / encoded
    return direct if direct.is_dir() else None


def _content_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        return str(content.get("text") or "")
    if not isinstance(content, list):
        return ""
    parts = []
    for block in content:
        if isinstance(block, str):
            parts.append(block)
        elif isinstance(block, dict) and block.get("type") in {"text", "input_text", "output_text"}:
            text = block.get("text")
            if isinstance(text, str):
                parts.append(text)
    return " ".join(parts)


def _clean_message(text: str) -> str:
    text = strip_ansi(text).replace("\x00", " ")
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return ""
    # Claude emits internal command/task messages as user entries too.
    if text.startswith("<") and any(
        token in text[:120].lower()
        for token in ("<local-", "<system", "<task-", "<command-", "<ide_")
    ):
        return ""
    return text[:MAX_MESSAGE_CHARS]


def _metadata_title(entry: dict[str, Any]) -> str:
    entry_type = str(entry.get("type") or "").lower()
    if entry_type not in {"ai-title", "custom-title", "session-title", "session_name"}:
        return ""
    for key in ("aiTitle", "customTitle", "sessionName", "session_name", "title", "name"):
        value = entry.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def read_session(path: Path) -> SessionRecord | None:
    """Extract a bounded summary from a Claude JSONL transcript."""
    try:
        stat = path.stat()
    except OSError:
        return None

    record = SessionRecord(path=path, session_id=path.stem, mtime=stat.st_mtime)
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                except (TypeError, ValueError):
                    continue
                if not isinstance(entry, dict):
                    continue

                if not record.session_id or record.session_id == path.stem:
                    candidate_id = entry.get("sessionId")
                    if isinstance(candidate_id, str) and candidate_id.strip():
                        record.session_id = candidate_id.strip()
                if not record.first_timestamp and isinstance(entry.get("timestamp"), str):
                    record.first_timestamp = entry["timestamp"]
                if not record.workdir and isinstance(entry.get("cwd"), str):
                    record.workdir = entry["cwd"]
                title = _metadata_title(entry)
                if title:
                    record.title = title

                entry_type = entry.get("type")
                if entry_type == "user":
                    # Tool results are represented as user entries in Claude's
                    # log but are not part of the user's conversation intent.
                    if "toolUseResult" in entry or "tool_use_id" in entry:
                        continue
                    message = entry.get("message")
                    content = message.get("content") if isinstance(message, dict) else entry.get("content")
                    text = _clean_message(_content_text(content))
                    if text:
                        record.recent_users.append(text)
                        record.recent_users = record.recent_users[-4:]
                        record.first_user = record.first_user or text
                elif entry_type == "assistant":
                    message = entry.get("message")
                    content = message.get("content") if isinstance(message, dict) else entry.get("content")
                    text = _clean_message(_content_text(content))
                    if text:
                        record.recent_assistant.append(text)
                        record.recent_assistant = record.recent_assistant[-3:]
    except (OSError, UnicodeError):
        return None
    return record


def _codex_sessions_dir() -> Path:
    override = os.environ.get("CODEX_SESSIONS_DIR")
    if override:
        return Path(override).expanduser()
    return get_home_dir() / ".codex" / "sessions"


def _codex_session_index() -> Path:
    override = os.environ.get("CODEX_SESSION_INDEX")
    if override:
        return Path(override).expanduser()
    return get_home_dir() / ".codex" / "session_index.jsonl"


def _load_codex_index() -> list[dict[str, str]]:
    """Return the latest title/update row for each Codex thread."""
    latest: dict[str, dict[str, str]] = {}
    try:
        with _codex_session_index().open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                try:
                    entry = json.loads(line)
                except (TypeError, ValueError):
                    continue
                if not isinstance(entry, dict):
                    continue
                session_id = entry.get("id") or entry.get("session_id")
                if not isinstance(session_id, str) or not session_id.strip():
                    continue
                latest[session_id] = {
                    "session_id": session_id,
                    "title": str(entry.get("thread_name") or entry.get("title") or "").strip(),
                    "updated_at": str(entry.get("updated_at") or "").strip(),
                }
    except OSError:
        return []
    return sorted(latest.values(), key=lambda item: item.get("updated_at", ""), reverse=True)


def _codex_transcript_path(session_id: str, event: dict[str, Any]) -> Path | None:
    transcript = _event_value(event, "transcript_path") or os.environ.get("CODEX_TRANSCRIPT_PATH", "")
    if transcript:
        candidate = Path(transcript).expanduser()
        if candidate.is_file():
            return candidate
    sessions_dir = _codex_sessions_dir()
    try:
        matches = [path for path in sessions_dir.rglob("*.jsonl") if path.name.endswith(f"{session_id}.jsonl")]
    except OSError:
        return None
    if not matches:
        return None
    return max(matches, key=lambda path: path.stat().st_mtime)


def read_codex_session(
    path: Path,
    session_id: str = "",
    title: str = "",
    updated_at: str = "",
) -> SessionRecord | None:
    """Extract the same bounded summary from a Codex rollout JSONL file."""
    try:
        stat = path.stat()
    except OSError:
        return None
    record = SessionRecord(
        path=path,
        session_id=session_id or path.stem.rsplit("-", 1)[-1],
        title=title,
        first_timestamp=updated_at,
        mtime=stat.st_mtime,
    )
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                except (TypeError, ValueError):
                    continue
                if not isinstance(entry, dict):
                    continue
                entry_type = entry.get("type")
                payload = entry.get("payload")
                if entry_type == "session_meta" and isinstance(payload, dict):
                    record.session_id = str(payload.get("id") or payload.get("session_id") or record.session_id)
                    record.workdir = str(payload.get("cwd") or record.workdir)
                elif entry_type == "turn_context" and isinstance(payload, dict):
                    record.workdir = str(payload.get("cwd") or record.workdir)
                elif entry_type == "response_item" and isinstance(payload, dict):
                    if payload.get("type") != "message" or payload.get("role") not in {"user", "assistant"}:
                        continue
                    text = _clean_message(_content_text(payload.get("content")))
                    if not text:
                        continue
                    if payload.get("role") == "user":
                        record.recent_users.append(text)
                        record.recent_users = record.recent_users[-4:]
                        record.first_user = record.first_user or text
                    else:
                        record.recent_assistant.append(text)
                        record.recent_assistant = record.recent_assistant[-3:]
    except (OSError, UnicodeError):
        return None
    return record


def list_codex_sessions(event: dict[str, Any], same_project: bool = True) -> list[SessionRecord]:
    current_id = (
        _event_value(event, "session_id", "sessionId", "thread_id", "threadId")
        or os.environ.get("CODEX_SESSION_ID")
        or os.environ.get("CODEX_THREAD_ID", "")
    )
    current_transcript = _event_value(event, "transcript_path") or os.environ.get("CODEX_TRANSCRIPT_PATH", "")
    cwd = _event_value(event, "cwd", "project_dir") or os.environ.get("CODEX_PROJECT_DIR", "")
    records: list[SessionRecord] = []
    index = _load_codex_index()
    known_paths: set[Path] = set()
    for item in index:
        session_id = item["session_id"]
        path = _codex_transcript_path(session_id, event)
        if not path:
            continue
        resolved = path.resolve()
        if resolved in known_paths:
            continue
        known_paths.add(resolved)
        if current_id and session_id == current_id:
            continue
        if current_transcript and resolved == Path(current_transcript).expanduser().resolve():
            continue
        record = read_codex_session(path, session_id, item.get("title", ""), item.get("updated_at", ""))
        if record and (not same_project or not cwd or not record.workdir or _same_path(record.workdir, cwd)):
            records.append(record)
    return records


def _same_path(left: str, right: str) -> bool:
    try:
        return os.path.normcase(os.path.abspath(left)) == os.path.normcase(os.path.abspath(right))
    except (OSError, TypeError):
        return left.casefold() == right.casefold()


def list_sessions(event: dict[str, Any], provider: str = "claude") -> list[SessionRecord]:
    if provider == "codex":
        return list_codex_sessions(event)
    directory = _transcript_dir(event)
    if not directory:
        return []
    current_id = _event_value(event, "session_id") or os.environ.get("CLAUDE_SESSION_ID", "")
    current_transcript = _event_value(event, "transcript_path") or os.environ.get("CLAUDE_TRANSCRIPT_PATH", "")
    records = []
    try:
        paths = sorted(directory.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    except OSError:
        return []
    for path in paths[:MAX_RECORDS]:
        if current_id and path.stem == current_id:
            continue
        if current_transcript and Path(current_transcript).resolve() == path.resolve():
            continue
        record = read_session(path)
        if record:
            records.append(record)
    return records


def _all_project_sessions(event: dict[str, Any]) -> list[SessionRecord]:
    """Read other project transcript folders only for an explicit lookup."""
    projects_dir = _claude_projects_dir()
    current_dir = _transcript_dir(event)
    current_id = _event_value(event, "session_id") or os.environ.get("CLAUDE_SESSION_ID", "")
    current_transcript = _event_value(event, "transcript_path") or os.environ.get("CLAUDE_TRANSCRIPT_PATH", "")
    records: list[SessionRecord] = []
    try:
        directories = [path for path in projects_dir.iterdir() if path.is_dir()]
    except OSError:
        return records
    for directory in directories:
        if current_dir and directory.resolve() == current_dir.resolve():
            continue
        try:
            paths = sorted(directory.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
        except OSError:
            continue
        for path in paths[:MAX_RECORDS]:
            if current_id and path.stem == current_id:
                continue
            if current_transcript and Path(current_transcript).resolve() == path.resolve():
                continue
            record = read_session(path)
            if record:
                records.append(record)
                if len(records) >= MAX_GLOBAL_RECORDS:
                    return records
    return records


def nearest_session(event: dict[str, Any], provider: str = "claude") -> SessionRecord | None:
    sessions = list_sessions(event, provider)
    return sessions[0] if sessions else None


def _alias_files(event: dict[str, Any]) -> list[Path]:
    files = []
    explicit = os.environ.get("CLAUDE_SESSION_ALIASES_FILE")
    if explicit:
        files.append(Path(explicit).expanduser())
    files.append(get_claude_dir() / "session-aliases.json")
    project_root = find_project_root(_event_value(event, "cwd") or None)
    if project_root:
        files.extend([
            project_root / ".claude" / "session-aliases.json",
            project_root / ".claude" / "session-data" / "session-aliases.json",
        ])
    try:
        files.append(get_sessions_dir(_event_value(event, "cwd") or None) / "session-aliases.json")
    except Exception:
        pass
    unique = []
    seen = set()
    for path in files:
        key = str(path).casefold()
        if key not in seen:
            unique.append(path)
            seen.add(key)
    return unique


def load_aliases(event: dict[str, Any]) -> dict[str, dict[str, str]]:
    aliases: dict[str, dict[str, str]] = {}
    for path in _alias_files(event):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        raw = data.get("aliases", data) if isinstance(data, dict) else {}
        if not isinstance(raw, dict):
            continue
        for name, info in raw.items():
            if isinstance(info, str):
                info = {"session_id": info}
            if not isinstance(info, dict):
                continue
            normalized = _normalize(str(name))
            if normalized:
                aliases[normalized] = {
                    key: str(value)
                    for key, value in info.items()
                    if isinstance(value, (str, int))
                }
    return aliases


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().casefold())


def _alias_session(alias: dict[str, str], records: Iterable[SessionRecord]) -> SessionRecord | None:
    direct_path = alias.get("transcript_path") or alias.get("transcriptPath") or alias.get("path")
    if direct_path:
        record = read_session(Path(direct_path).expanduser())
        if record:
            return record
    session_id = alias.get("session_id") or alias.get("sessionId") or alias.get("id")
    if session_id:
        for record in records:
            if record.session_id == session_id or record.path.stem == session_id:
                return record
    return None


def named_session(name: str, event: dict[str, Any], provider: str = "claude") -> SessionRecord | None:
    name_key = _normalize(name)
    records = list_codex_sessions(event, same_project=False) if provider == "codex" else list_sessions(event)
    aliases = load_aliases(event)
    alias = aliases.get(name_key)
    if alias:
        record = _alias_session(alias, records)
        if record:
            return record
    all_records = records if provider == "codex" else records + _all_project_sessions(event)
    for record in all_records:
        if _normalize(record.name) == name_key or _normalize(record.title) == name_key:
            return record
    for record in all_records:
        if record.session_id == name or record.path.stem == name:
            return record
    if len(name) >= 8:
        for record in all_records:
            if record.session_id.startswith(name) or record.path.stem.startswith(name):
                return record
    return None


def _trim_context(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n... (session context truncated)"


def format_session(record: SessionRecord, explicit: bool = False) -> str:
    heading = "Referenced session" if explicit else "Nearest previous session"
    lines = [
        f"## {heading} (auto-loaded)",
        f"Name: {record.name}",
        f"Session ID: {record.session_id}",
    ]
    if record.first_timestamp:
        lines.append(f"Started: {record.first_timestamp}")
    if record.recent_users:
        lines.append("\n### User messages")
        lines.extend(f"- {message}" for message in record.recent_users)
    if record.recent_assistant:
        lines.append("\n### Recent assistant notes")
        lines.extend(f"- {message}" for message in record.recent_assistant)
    if not record.recent_users and not record.recent_assistant:
        lines.append("\nThe transcript has no readable text excerpts.")
    limit = MAX_EXPLICIT_CONTEXT_CHARS if explicit else MAX_CONTEXT_CHARS
    return _trim_context("\n".join(lines), limit)


def _quoted_or_rest(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] in "\"'`" and value[-1] == value[0]:
        return value[1:-1].strip()
    return value.rstrip(" .,!?:;")


def parse_prompt(prompt: str) -> tuple[str, str] | None:
    """Return (operation, name), or None for ordinary prompts."""
    text = prompt.strip()
    if re.fullmatch(r"/session\s+list/?", text, re.IGNORECASE) or re.fullmatch(
        r"(?:list|show)\s+sessions?", text, re.IGNORECASE
    ):
        return "list", ""
    patterns = [
        r"/session(?:-read)?\s+(?:read\s+)?(?P<name>.+)$",
        r"(?:read|load|open|show)\s+(?:the\s+)?session(?:\s+named)?\s+(?P<name>.+)$",
        r"(?:đọc|mở|xem)\s+(?:session|phiên)(?:\s+tên)?\s+(?P<name>.+)$",
    ]
    for pattern in patterns:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            name = _quoted_or_rest(match.group("name"))
            return ("read", name) if name else None
    return None


def list_context(event: dict[str, Any], provider: str = "claude") -> str:
    records = list_codex_sessions(event, same_project=False) if provider == "codex" else list_sessions(event)
    if not records:
        return "## Sessions\nNo previous sessions were found for this project."
    lines = ["## Available previous sessions", ""]
    for record in records[:20]:
        lines.append(f"- {record.name} ({record.session_id})")
    return "\n".join(lines)


def emit_context(context: str, event_name: str, provider: str = "claude") -> None:
    if not context:
        return
    if provider in {"codex", "agents", "cursor", "generic"}:
        print(context)
    elif event_name == "SessionStart":
        payload = {"hookSpecificOutput": {"hookEventName": event_name, "additionalContext": context}}
        print(json.dumps(payload, ensure_ascii=False))
    else:
        payload = {"additionalContext": context}
        print(json.dumps(payload, ensure_ascii=False))


def run_hook(event: dict[str, Any], provider: str = "claude") -> None:
    event_name = _event_value(event, "hook_event_name", "hookEventName", "event") or "SessionStart"
    if event_name == "SessionStart":
        source = _event_value(event, "source") or "startup"
        if source != "startup" or os.environ.get("BENCHMARK_MODE") == "1":
            return
        if os.environ.get("CLAUDE_PARENT_SESSION_ID"):
            return
        record = nearest_session(event, provider)
        if record:
            _log.info(f"Loaded nearest session: {record.name}")
            emit_context(format_session(record), event_name, provider)
        return

    if event_name != "UserPromptSubmit":
        return
    prompt = _event_value(event, "prompt", "user_prompt")
    parsed = parse_prompt(prompt)
    if not parsed:
        return
    operation, name = parsed
    if operation == "list":
        emit_context(list_context(event, provider), event_name, provider)
        return
    record = named_session(name, event, provider)
    if not record:
        emit_context(
            f"## Session lookup\nNo previous session named `{name}` was found.\n\n"
            "Use `/session list` to see the available names.",
            event_name,
            provider,
        )
        return
    _log.info(f"Loaded requested session: {record.name}")
    emit_context(format_session(record, explicit=True), event_name, provider)


def run_cli(argv: list[str], provider: str) -> int:
    event = {
        "cwd": os.getcwd(),
        "session_id": os.environ.get("CLAUDE_SESSION_ID") or os.environ.get("CODEX_SESSION_ID", ""),
    }
    if argv[0] == "list":
        print(list_context(event, provider))
        return 0
    if argv[0] == "read" and len(argv) >= 2:
        record = named_session(" ".join(argv[1:]), event, provider)
        if not record:
            print(f"No previous session named: {' '.join(argv[1:])}", file=sys.stderr)
            return 1
        print(format_session(record, explicit=True))
        return 0
    print("usage: session_memory.py list | read <session-name>", file=sys.stderr)
    return 2


def main() -> int:
    # Claude Code launches Python through Node on Windows; force UTF-8 so
    # renamed sessions and Vietnamese prompts survive the hook boundary.
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    provider = os.environ.get("AI_PROVIDER", "claude")
    if "--provider" in args:
        index = args.index("--provider")
        if index + 1 < len(args):
            provider = args[index + 1]
        args = args[:index] + args[index + 2:]
    if args:
        return run_cli(args, provider)
    run_hook(_input_event(), provider)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        _log.error(str(exc))
        raise SystemExit(0)
