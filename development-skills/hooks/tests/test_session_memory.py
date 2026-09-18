import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys

HOOK_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HOOK_DIR))
import session_memory


def write_session(path: Path, title: str, user_text: str, assistant_text: str) -> None:
    rows = [
        {"type": "ai-title", "sessionId": path.stem, "aiTitle": title},
        {
            "type": "user",
            "sessionId": path.stem,
            "timestamp": "2026-09-18T01:00:00Z",
            "message": {"role": "user", "content": user_text},
        },
        {
            "type": "assistant",
            "sessionId": path.stem,
            "message": {"role": "assistant", "content": [{"type": "text", "text": assistant_text}]},
        },
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def write_codex_session(path: Path, session_id: str, cwd: str, user_text: str, assistant_text: str) -> None:
    rows = [
        {"type": "session_meta", "payload": {"id": session_id, "cwd": cwd}},
        {"type": "turn_context", "payload": {"cwd": cwd}},
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": user_text}],
            },
        },
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": assistant_text}],
            },
        },
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


class SessionMemoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project = Path(self.temp_dir.name) / "project"
        self.project.mkdir()
        self.current = self.project / "current.jsonl"
        self.current.write_text("", encoding="utf-8")
        self.old = self.project / "old.jsonl"
        self.new = self.project / "new.jsonl"
        write_session(self.old, "Old design", "old request", "old answer")
        write_session(self.new, "Latest design", "latest request", "latest answer")
        os.utime(self.old, (100, 100))
        os.utime(self.new, (200, 200))
        self.event = {
            "cwd": self.project.as_posix(),
            "session_id": "current",
            "transcript_path": str(self.current),
        }

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_nearest_session_excludes_current_and_uses_newest_mtime(self) -> None:
        record = session_memory.nearest_session(self.event)
        self.assertIsNotNone(record)
        self.assertEqual(record.title, "Latest design")

    def test_named_session_resolves_title(self) -> None:
        record = session_memory.named_session('Old design', self.event)
        self.assertIsNotNone(record)
        self.assertEqual(record.session_id, "old")

    def test_named_session_preserves_unicode_title(self) -> None:
        unicode_session = self.project / "unicode.jsonl"
        write_session(unicode_session, "Kiểm tra session", "yêu cầu cũ", "ghi chú cũ")
        record = session_memory.named_session("Kiểm tra session", self.event)
        self.assertIsNotNone(record)
        self.assertEqual(record.name, "Kiểm tra session")

    def test_named_session_falls_back_to_another_project(self) -> None:
        projects_dir = Path(self.temp_dir.name) / "projects"
        other_project = projects_dir / "other-project"
        other_project.mkdir(parents=True)
        write_session(other_project / "other.jsonl", "Cross project session", "other request", "other answer")
        with patch.dict(os.environ, {"CLAUDE_PROJECTS_DIR": str(projects_dir)}):
            record = session_memory.named_session("Cross project session", self.event)
        self.assertIsNotNone(record)
        self.assertEqual(record.session_id, "other")

    def test_prompt_parser_supports_quoted_names_and_vietnamese(self) -> None:
        self.assertEqual(session_memory.parse_prompt('/session read "Old design"'), ("read", "Old design"))
        self.assertEqual(session_memory.parse_prompt('đọc session "Old design"'), ("read", "Old design"))
        self.assertEqual(session_memory.parse_prompt('/session list'), ("list", ""))

    def test_alias_resolves_session_id(self) -> None:
        alias_file = self.project / "aliases.json"
        alias_file.write_text(json.dumps({"aliases": {"legacy": {"sessionId": "old"}}}), encoding="utf-8")
        with patch.dict(os.environ, {"CLAUDE_SESSION_ALIASES_FILE": str(alias_file)}):
            record = session_memory.named_session("legacy", self.event)
        self.assertIsNotNone(record)
        self.assertEqual(record.session_id, "old")

    def test_session_start_only_auto_loads_on_startup(self) -> None:
        with patch("session_memory.emit_context") as emit:
            session_memory.run_hook({**self.event, "hook_event_name": "SessionStart", "source": "resume"})
        emit.assert_not_called()

    def test_user_prompt_hook_loads_named_session(self) -> None:
        with patch("session_memory.emit_context") as emit:
            session_memory.run_hook({
                **self.event,
                "hook_event_name": "UserPromptSubmit",
                "prompt": '/session read "Old design"',
            })
        emit.assert_called_once()
        context = emit.call_args.args[0]
        self.assertIn("Old design", context)
        self.assertIn("old request", context)

    def test_codex_session_index_resolves_nearest_and_named_thread(self) -> None:
        sessions_dir = Path(self.temp_dir.name) / "codex-sessions" / "2026" / "09" / "18"
        sessions_dir.mkdir(parents=True)
        index_file = Path(self.temp_dir.name) / "session_index.jsonl"
        codex_path = sessions_dir / "rollout-codex-old.jsonl"
        write_codex_session(codex_path, "codex-old", str(self.project), "Codex request", "Codex answer")
        index_file.write_text(
            json.dumps({"id": "codex-old", "thread_name": "Codex design", "updated_at": "2026-09-18T01:00:00Z"}) + "\n",
            encoding="utf-8",
        )
        env = {
            "CODEX_SESSIONS_DIR": str(Path(self.temp_dir.name) / "codex-sessions"),
            "CODEX_SESSION_INDEX": str(index_file),
            "CODEX_SESSION_ID": "codex-current",
        }
        with patch.dict(os.environ, env):
            record = session_memory.nearest_session({"cwd": str(self.project)}, provider="codex")
            named = session_memory.named_session("Codex design", {"cwd": str(self.project)}, provider="codex")
        self.assertIsNotNone(record)
        self.assertEqual(record.session_id, "codex-old")
        self.assertIsNotNone(named)
        self.assertEqual(named.first_user, "Codex request")

    def test_codex_hook_uses_plain_text_provider_output(self) -> None:
        with patch("builtins.print") as output:
            session_memory.emit_context("Codex context", "SessionStart", "codex")
        output.assert_called_once_with("Codex context")


if __name__ == "__main__":
    unittest.main()
