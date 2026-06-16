# team-development-skills

Bộ AI skill packages cho Claude Code, hỗ trợ phân tích yêu cầu phần mềm và mô phỏng quy trình phát triển theo team.

*A collection of AI skill packages for Claude Code — software requirements analysis and full-team development simulation.*

---

## Skills

### [srs-skills](./srs-skills/)

Tạo tài liệu **Software Requirements Specification (IEEE 830-1998)** từ ý tưởng thô đến SRS hoàn chỉnh, qua pipeline 7 bước có validation tự động.

*Generates a complete IEEE 830-1998 SRS from a raw idea through a 7-step pipeline with automated validation.*

| Command | Tiếng Việt | English |
|---|---|---|
| `/cl:srs` | Tạo SRS nhanh từ requirements text có sẵn | Quick SRS from existing requirements text |
| `/cl:srs-flow` | Pipeline đầy đủ: brainstorm → generate → validate | Full pipeline: brainstorm → spec → plan → generate → validate → improve → save |

Hỗ trợ Claude Code, Gemini CLI, GitHub Copilot và mọi LLM đọc được markdown.
*Compatible with Claude Code, Gemini CLI, GitHub Copilot, and any markdown-capable LLM.*

→ [Hướng dẫn tiếng Việt](./srs-skills/README.md) · [English guide](./srs-skills/README.en.md)

---

### [virtual-team-skill](./virtual-team-skill/)

Mô phỏng một đội phát triển phần mềm gồm **7 vai trò AI** (BA → TechLead → PM → BE Dev → FE Dev → Tester → QA/QC), tạo đầy đủ tài liệu từ yêu cầu đến ký duyệt phát hành.

*Simulates a full software development team of **7 AI agents** (BA → TechLead → PM → BE Dev → FE Dev → Tester → QA/QC), producing all artifacts from requirements to release sign-off.*

| Command | Tiếng Việt | English |
|---|---|---|
| `/team "..." --level {level}` | Chạy toàn bộ pipeline 7 vai trò | Run the full 7-agent pipeline |
| `/team-ba` `/team-techlead` `/team-pm` ... | Chạy từng vai trò riêng lẻ | Run individual agents manually |

Mức độ kiến trúc và tiêu chuẩn chất lượng được kiểm soát qua `--level`: `fresh` · `junior` · `mid` · `senior`.

*Architecture style and quality standards are controlled by `--level`: `fresh` · `junior` · `mid` · `senior`.*

→ [Hướng dẫn tiếng Việt](./virtual-team-skill/README.vi.md) · [English guide](./virtual-team-skill/README.md)

---

## Kết hợp cả hai / Using both together

Dùng `srs-skills` để elicit và validate yêu cầu trước, sau đó đưa kết quả vào `virtual-team-skill`.

*Use `srs-skills` to elicit and validate requirements first, then feed the output into `virtual-team-skill`.*

```
/cl:srs-flow                    ← tạo spec từ ý tưởng / generate spec from idea
/team-ba --srs --level mid      ← BA đọc spec, pipeline team bắt đầu / BA reads spec, team pipeline starts
```
