# Development Skills

> **VI:** Bộ skill phát triển phần mềm từ brainstorm, plan và implementation đến quality, testing, review, browser automation và quản lý context.
>
> **EN:** A software-development skill pack spanning brainstorming, planning, implementation, quality, testing, review, browser automation, and context management.

Mỗi skill hoạt động độc lập và có README song ngữ riêng. Bạn có thể kết hợp chúng thành pipeline hoặc chỉ cài đúng skill mình cần.

Each skill is self-contained and has its own bilingual README. Use the full pipeline or install only what you need.

## Included Skills

| Skill | Invoke | Use when |
|-------|--------|----------|
| [backend-mindset](./skills/backend-mindset/) | `/backend-mindset` | Production-ready backend design |
| [caveman](./skills/caveman/) | _(auto-triggered)_ | Terse output for context efficiency |
| [ck:brainstorm](./skills/ck-brainstorm/) | `/ck:brainstorm` | Explore before committing to code |
| [ck:cook](./skills/ck-cook/) | `/ck:cook` | Execute Markdown or phased JSON plans |
| [ck:fix](./skills/ck-fix/) | `/ck:fix` | Diagnose and fix bugs |
| [ck:plan](./skills/ck-plan/) | `/ck:plan` | Create implementation plans |
| [ck:plan-json](./skills/ck-plan-json/) | `/ck:plan-json` | Create resumable JSON plan bundles |
| [ck:quality](./skills/ck-quality/) | `/ck:quality` | Audit architecture and maintainability |
| [ck:test](./skills/ck-test/) | `/ck:test` | Testing and two-pass TDD |
| [code-review](./skills/code-review/) | `/code-review` | Risk-driven code review |
| [mermaidjs-v11](./skills/mermaidjs-v11/) | `/mermaidjs-v11` | Technical diagrams |
| [playwright-skill](./skills/playwright-skill/) | `/playwright-skill` | Browser automation and UI testing |
| [problem-solving](./skills/problem-solving/) | `/problem-solving` | Six breakthrough techniques |
| [sequential-thinking](./skills/sequential-thinking/) | `/sequential-thinking` | Structured reasoning |
| [skill-creator](./skills/skill-creator/) | _(meta-skill)_ | Create and improve skills |
| [strategic-compact](./skills/strategic-compact/) | `/strategic-compact` | Context-window management |

## Commands / Danh sách lệnh

The table below lists every command provided under `commands/ck/`.
Bảng dưới đây liệt kê toàn bộ lệnh được cung cấp trong `commands/ck/`.

| Command / Lệnh | English | Tiếng Việt |
|---|---|---|
| `/ck:brainstorm` | Explore requirements and possible solutions before implementation. It asks clarifying questions, compares approaches, and produces a decision/specification without writing code. | Khám phá yêu cầu và các hướng giải quyết trước khi triển khai. Lệnh đặt câu hỏi làm rõ, so sánh phương án và tạo quyết định/đặc tả mà không viết code. |
| `/ck:code-review [PR]` | Review local changes or a GitHub pull request for correctness, security, regressions, and release readiness. It consumes current quality/test evidence instead of duplicating those gates. | Review thay đổi local hoặc GitHub pull request về tính đúng đắn, bảo mật, regression và khả năng phát hành. Lệnh sử dụng kết quả quality/test hiện có thay vì kiểm tra trùng lặp. |
| `/ck:coding-level <level>` | Set the coding explanation depth for the current session or project, from default through junior, senior, tech-lead, and god-mode levels. | Thiết lập mức độ giải thích code cho session hoặc dự án, từ mặc định đến junior, senior, tech lead và god mode. |
| `/ck:cook [--fast\|--hard] [--tdd]` | Implement a Markdown or phased JSON plan one phase at a time. Cook writes production code and runs compile/syntax checks, but never writes or runs tests; every phase must pass `ck:quality`. | Triển khai plan Markdown hoặc JSON theo từng phase. Cook viết production code và kiểm tra compile/cú pháp nhưng không viết hay chạy test; mỗi phase bắt buộc phải qua `ck:quality`. |
| `/ck:docs-fe [target] [--html]` | Generate a concise frontend handoff document for changed endpoints, including API contracts, parameters, responses, and error codes. | Tạo tài liệu bàn giao ngắn gọn cho frontend về các endpoint thay đổi, gồm API contract, tham số, response và error code. |
| `/ck:fix [--fast\|--hard]` | Diagnose and fix a bug through scoped investigation. It can also consume `--from-quality <report>` or `--from-test <report>` and re-verifies quality after production changes. | Chẩn đoán và sửa bug theo phạm vi đã xác định. Lệnh cũng có thể nhận `--from-quality <report>` hoặc `--from-test <report>` và kiểm tra lại quality sau khi sửa production code. |
| `/ck:init [path]` | Bootstrap or reconfigure `.claude/` for another project, including selected workflows, skills, agents, hooks, `CLAUDE.md`, and `.ck.json`. Use `--show` to inspect configuration or `--reset` to reset it. | Khởi tạo hoặc cấu hình lại `.claude/` cho dự án khác, gồm workflow, skill, agent, hook, `CLAUDE.md` và `.ck.json`. Dùng `--show` để xem cấu hình hoặc `--reset` để đặt lại. |
| `/ck:learn` | Extract reusable patterns from a completed non-trivial session and save them as skill files for future use. | Trích xuất các pattern có thể tái sử dụng từ một session phức tạp đã hoàn tất và lưu thành skill cho những lần sau. |
| `/ck:plan [--fast\|--hard] [--tdd]` | Create a Markdown implementation plan with scope challenge, per-phase design constraints, and separate quality/testing state. Hard mode adds research and red-team validation. | Tạo implementation plan dạng Markdown, gồm kiểm tra phạm vi, design constraint cho từng phase và trạng thái quality/testing riêng. Hard mode bổ sung nghiên cứu và red-team validation. |
| `/ck:plan-json [options]` | Create a machine-readable phased plan bundle with a compact master `plan.json` and detailed sibling phase files. Supports a spec, inline requirements, and custom output path. | Tạo bộ plan theo phase có thể đọc bằng máy, gồm master `plan.json` gọn và các file phase chi tiết cùng thư mục. Hỗ trợ spec, yêu cầu nhập trực tiếp và đường dẫn output tùy chỉnh. |
| `/ck:quality --audit <path>` | Independently audit architecture, ownership, boundaries, abstraction, and maintainability without modifying code. Use `--gate <phase>` inside Cook, `--changed`/`--diff` for changes, and `--verify` after remediation. | Đánh giá độc lập kiến trúc, ownership, boundary, abstraction và maintainability mà không sửa code. Dùng `--gate <phase>` trong Cook, `--changed`/`--diff` cho phần thay đổi và `--verify` sau khi khắc phục. |
| `/ck:show-off [--auto\|--fast\|--clone] <topic>` | Build a polished bilingual HTML presentation and optionally capture social-ready images in 16:9, 9:16, and 1:1 formats. | Tạo presentation HTML song ngữ có giao diện hoàn chỉnh và tùy chọn chụp ảnh dùng cho mạng xã hội theo tỷ lệ 16:9, 9:16 và 1:1. |
| `/ck:test <target>` | Independently write and run scoped unit, integration, E2E, regression, or all-phase tests. It supports two-pass TDD with `--tdd --prepare` before Cook and `--tdd --verify` afterward, and never edits production code. | Viết và chạy độc lập unit test, integration test, E2E, regression hoặc test toàn bộ phase theo phạm vi. Hỗ trợ TDD hai lượt bằng `--tdd --prepare` trước Cook và `--tdd --verify` sau đó, đồng thời không sửa production code. |

Commands are invoked as `/ck:<name>` in Claude Code. Codex uses the corresponding `$ck:<name>` skill invocation, while Antigravity exposes the workflows installed under `.agents/workflows/`.
Trong Claude Code, các lệnh được gọi bằng `/ck:<tên>`. Codex sử dụng skill tương ứng theo dạng `$ck:<tên>`, còn Antigravity sử dụng workflow được cài trong `.agents/workflows/`.

## Usage

Open `development-skills/` directly in Claude Code — skills, hooks, agents, and commands are auto-detected from `settings.json` at pack root.

### Copy to another project

```bash
# Full pack
cp -r development-skills/skills/ <your-project>/skills/
cp -r development-skills/hooks/ <your-project>/hooks/
cp -r development-skills/agents/ <your-project>/agents/
cp -r development-skills/rules/ <your-project>/rules/
cp -r development-skills/commands/ <your-project>/commands/
cp -r development-skills/contexts/ <your-project>/contexts/
cp development-skills/settings.json <your-project>/settings.json
```

### Quick install (skills only)

```bash
cp -r development-skills/skills/* <your-project>/skills/
```

The guided pipeline is `ck:plan → ck:test --tdd --prepare` (optional) `→ ck:cook → ck:quality → ck:test → code-review`. `ck:cook` never owns tests, and phase completion requires a fresh `ck:quality` receipt.
