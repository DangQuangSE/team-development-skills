# Brainstorm: Virtual Team Skill

Date: 2026-06-16

## Topic

Xây dựng một Claude Code skill đóng vai trò là một virtual enterprise team, tạo ra nhiều agent với các vai trò khác nhau (BA, System Designer/Senior TechLead, BE Dev, FE Dev, Tester, QA/QC) và thực thi workflow lifecycle theo quy trình PM thực tế.

## Domain / Scale

Internal Tool / Developer Tooling (Claude Code Skill) / MVP → Enterprise

---

## Actors

### Operator (người dùng skill)

- [ACTOR] Developer (Solo): Lập trình viên cá nhân dùng skill thay cho cả team | access: trigger/operator
- [ACTOR] Technical Lead / Architect: Senior dev validate thiết kế, review decisions | access: trigger/operator
- [ACTOR] Product Manager / BA: PM/BA simulate team estimation, feasibility check | access: trigger/operator
- [ACTOR] Startup Founder / Solo Maker: Xây dựng sản phẩm một mình, skill đóng vai cả team | access: trigger/operator

### Virtual Team Agents (do skill tạo ra)

- [ACTOR] BA (Business Analyst): Phân tích yêu cầu, viết user story, clarify business rules, acceptance criteria | access: read/write — model: claude-sonnet-4-6
- [ACTOR] System Designer / Senior TechLead: Thiết kế kiến trúc, chọn tech stack, viết ADR, ERD, sequence diagram | access: read/write/admin — model: claude-opus-4-8
- [ACTOR] Backend Developer: Implement API endpoints, DB schema, migrations, business logic | access: read/write — model: claude-sonnet-4-6
- [ACTOR] Frontend Developer: Implement UI components, pages, API integration | access: read/write — model: claude-sonnet-4-6
- [ACTOR] Tester: Viết test plan, test cases (unit/integration/e2e), báo cáo bugs | access: read/write — model: claude-sonnet-4-6
- [ACTOR] QA/QC: Quality gate, review process compliance, advisory sign-off | access: read/write/admin — model: claude-opus-4-8
- [ACTOR] Scrum Master / PM: Điều phối workflow, tạo sprint board, task list, unblock agents | access: admin — model: claude-haiku-4-5

---

## Confirmed Features (IN Scope — v1)

### Workflow Model

- Hybrid Agile + Waterfall checkpoints
- Sprint-based với milestone gates (design freeze, UAT, release sign-off)

### Phase 1 — BA Analysis

- Input: project requirement (text, PRD, user description)
- Output: `projects/{slug}/team/ba/requirements.md` (user stories, acceptance criteria, business rules)
- Model: claude-sonnet-4-6

### Phase 2 — TechLead Architecture

- Input: BA output (chained)
- Output: `projects/{slug}/team/techlead/` (ADR.md, architecture.md, ERD.md, tech-stack.md)
- Model: claude-opus-4-8

### Phase 3 — PM Sprint Planning

- Input: BA output + TechLead output
- Output: `projects/{slug}/team/pm/sprint-plan.md` (sprint board, task list, story points)
- Model: claude-haiku-4-5
- Tool: TodoWrite để track progress

### Phase 4 — BE Development

- Input: TechLead output + PM sprint plan
- Output: `projects/{slug}/team/be/` (API files, schema files, PR description)
- Model: claude-sonnet-4-6

### Phase 5 — FE Development

- Input: TechLead output + BE output (API contracts)
- Output: `projects/{slug}/team/fe/` (UI component files, pages, PR description)
- Model: claude-sonnet-4-6

### Phase 6 — Tester

- Input: BA output + BE/FE output
- Output: `projects/{slug}/team/tester/` (test-plan.md, test-cases.md, bug-report.md)
- Model: claude-sonnet-4-6

### Phase 7 — QA/QC Review

- Input: ALL previous artifacts
- Output: `projects/{slug}/team/qa/` (quality-report.md, compliance-check.md, sign-off status)
- Model: claude-opus-4-8

### Trigger Modes

- **Full-auto mode**: `/team` hoặc `/team-build "{requirement}"` — chạy toàn bộ pipeline tự động
- **Per-agent mode**: `/team-ba`, `/team-techlead`, `/team-dev`, `/team-fe`, `/team-test`, `/team-qa` — user control từng bước
- User có thể chọn auto-chain hoặc manual checkpoint giữa các phase

### Agent Context Chain

- Mỗi agent đọc output của agent trước (chained context)
- Tất cả artifacts được flush ra disk trước khi agent kế tiếp bắt đầu (persistence guarantee)
- User có thể pass extra context khi trigger bất kỳ agent nào

### Agent Autonomy

- Tất cả role agents có thể spawn deep-dive sub-agents khi cần (high autonomy)
- Ví dụ: BA spawn sub-agent để phân tích domain sâu hơn; Tester spawn parallel sub-agents cho từng test suite

### Error Handling — 2-Layer Defense

- **Layer 1 — Automated Validation**: Skill tự kiểm tra structural completeness (required sections/headings), tự rerun agent tối đa 3 lần nếu format/structural errors
- **Layer 2 — Cross-agent Verification**: Agent sau có thể flag logic errors trong output của agent trước. User quyết định rerun agent trước với adjusted prompt.

### QA Authority

- QA/QC có vai trò advisory (flag issues)
- User có final decision: override hoặc reject phase

### Multi-project Support

- Mỗi project được isolate bởi `projects/{slug}/team/`
- Nhiều dự án có thể tồn tại cùng lúc trong cùng workspace

---

## OUT of Scope (v1)

1. **Real git push lên remote (GitHub/GitLab)**: Skill KHÔNG tự động push code — user tự quyết định push
2. **Real-time multi-user collaboration**: Không phải tool cho nhiều người dùng cùng session
3. **DevOps/Infra phase**: Dockerfile, GitHub Actions, CI/CD scripts — deferred to v2
4. **Live code execution / runtime testing**: Skill chỉ generate và review, không chạy code thực tế
5. **Web app / PM dashboard UI**: Hoàn toàn CLI/skill-based, không có giao diện web

---

## Technical Constraints

- **Implementation**: Claude Code skills (.md files) + Agent tool (sub-agents per role)
- **Model assignment**:
  - `claude-opus-4-8`: TechLead, QA/QC (deep reasoning, architectural decisions)
  - `claude-sonnet-4-6`: BA, BE Dev, FE Dev, Tester (standard execution)
  - `claude-haiku-4-5`: PM/Scrum Master (coordination, routing, fast iterations)
- **Platform**: Cross-platform — Windows (D:\...) và Mac (/home/...)
- **Output format**: Human-readable Markdown (.md) — NO binary/proprietary formats
- **Compatibility**: 100% tương thích Claude Code skill system (Skill tool, Agent tool, TodoWrite)
- **Persistence**: All artifacts flushed to disk before next agent starts; context survives Claude Code restart
- **Content**: No size/time limits on artifacts — đầy đủ chi tiết là ưu tiên

---

## Business Rules

1. **Retry logic**: Structural validation (required headings check) → auto-rerun tối đa 3 lần → nếu vẫn fail → hard stop, báo user
2. **Cross-agent review**: Agent sau ĐƯỢC PHÉP và ĐƯỢC KHUYẾN KHÍCH flag vấn đề từ agent trước
3. **Human-in-the-loop**: QA/QC flag advisory, user là final authority — không agent nào được tự reject/override user
4. **Context chain**: Thứ tự mặc định: BA → TechLead → PM → BE → FE → Tester → QA. Per-agent mode có thể bỏ qua bước
5. **Sub-agent spawning**: Tất cả agents được phép spawn sub-agents. Depth tối đa: 2 levels (role agent → sub-agent)
6. **No credentials**: Agent KHÔNG ĐƯỢC hardcode secrets/API keys/passwords trong generated code
7. **Isolation**: Mỗi project (slug) hoàn toàn độc lập, không có shared state giữa projects

---

## NFR Baselines

| NFR Category            | Target                                                                 |
| ----------------------- | ---------------------------------------------------------------------- |
| Structural Completeness | Mỗi artifact phải có đủ required sections theo template trước khi pass |
| Persistence             | 100% artifacts flushed to disk; context không bị mất khi restart       |
| Content Quality         | Không giới hạn dung lượng/thời gian — ưu tiên đầy đủ chi tiết          |
| Retry Limit             | Tối đa 3 auto-retries per agent; sau đó hard stop với error report     |
| Data Privacy            | User data chỉ đi qua Anthropic API; không gửi ra external services     |
| Security                | No hardcoded secrets/credentials trong generated artifacts             |

---

## Integrations

- **SRS workflow**: Virtual team skill CÓ THỂ nhận input từ SRS output (`brainstorm.md`, `spec.md`, `plans/`)
- **Claude Code TodoWrite tool**: PM agent dùng TodoWrite để hiển thị sprint board và progress tracking trong conversation
- **No other external integrations**: Skill hoạt động độc lập, chỉ dùng Claude Code built-in tools

---

## Compliance

- **No external data sharing**: Project context chỉ đi qua Anthropic API, không lưu trữ tập trung ở third-party server
- **No credential leakage**: Agents được instructed không hardcode secrets trong generated code
- **No regulatory compliance needed**: Đây là developer tool, không xử lý PII/financial/healthcare data

---

## Open Items

1. **Template định nghĩa**: Mỗi role agent cần có template cụ thể cho output format (headings bắt buộc) — sẽ define trong sr:spec
2. **Skill naming convention**: `/team-ba` hay `/virtual-ba` hay `/vteam-ba`? — confirm khi viết skill files
3. **Sub-agent depth limit**: Hiện tại 2 levels. Có nên cho phép level 3 không? — defer to v2
4. **DevOps v2 spec**: Khi nào thêm DevOps phase vào? Dependency trên BE/FE output cần define rõ
5. **Live code execution OUT scope v1**: Có thể integrate với Claude Code terminal tools trong v2 để thực sự chạy tests
