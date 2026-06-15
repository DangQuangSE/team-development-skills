# Specification: Virtual Team Skill

**Version**: 1.0 (Draft)
**Date**: 2026-06-16
**Source**: projects/virtual-team-skill/brainstorm.md
**Status**: Ready for Planning

---

## §1 — Project Overview

### 1.1 System Name

**Virtual Team Skill** — một bộ Claude Code skills cho phép một người dùng đơn lẻ vận hành một virtual software development team đầy đủ chức năng, với mỗi thành viên là một AI agent chuyên biệt.

### 1.2 Problem Statement

Trong quá trình phát triển phần mềm thực tế, một sản phẩm chất lượng đòi hỏi sự tham gia của nhiều vai trò chuyên biệt: Business Analyst phân tích yêu cầu, Architect thiết kế hệ thống, Developer triển khai code, Tester đảm bảo chất lượng, QA/QC sign-off release. Những cá nhân solo (developer, founder, PM) hoặc team nhỏ thường phải kiêm nhiệm quá nhiều vai trò, dẫn đến:

1. **Blind spot**: Người viết requirement cũng là người review — thiếu góc nhìn phản biện
2. **Context switching overhead**: Chuyển vai trò liên tục gây mất focus và giảm chất lượng đầu ra
3. **Missing artifacts**: Không có TechLead → không có ADR; không có Tester → không có test plan
4. **No structured workflow**: Không có quy trình PM lifecycle → phát triển ad-hoc, khó maintain và scale

### 1.3 Solution Summary

Virtual Team Skill giải quyết bài toán trên bằng cách cung cấp một **hệ thống các Claude Code skills có thể tạo ra và điều phối nhiều AI agents**, mỗi agent đóng một vai trò cố định trong software development lifecycle:

- Người dùng khởi động skill với một yêu cầu (requirement text, PRD, user description)
- Skill tự động (hoặc theo lệnh) spawn các specialized agents theo đúng thứ tự workflow
- Mỗi agent đọc output của agent trước, thực hiện công việc theo vai trò của mình, ghi artifact ra file system
- Kết quả: một bộ hoàn chỉnh artifacts đại diện cho toàn bộ vòng đời phát triển phần mềm — từ requirements đến code đến test plan đến QA sign-off

**Workflow mặc định**: BA → TechLead → PM → BE Dev → FE Dev → Tester → QA/QC

**Cho ai**: Developer cá nhân, Startup Founder, Technical Lead, Product Manager — bất kỳ ai cần output chất lượng từ nhiều góc nhìn chuyên môn mà không có team thực tế.

**Kênh sử dụng**: Claude Code CLI (terminal, VS Code extension, desktop app)

### 1.4 Primary Success Metrics

| Metric                         | Target                                                  | Cách đo                              |
| ------------------------------ | ------------------------------------------------------- | ------------------------------------ |
| Artifact completeness          | 100% required sections present trong mỗi agent output   | Structural validator pass            |
| Context chain integrity        | 0 agent starts mà không đọc được output của agent trước | File existence check trước khi spawn |
| Retry success rate             | ≥ 80% agents pass validation trong lần đầu tiên         | Count retry events / total runs      |
| User time-to-full-artifact-set | < 15 phút từ lúc trigger đến khi QA sign-off            | Wall-clock time per run              |
| Multi-project isolation        | 0 cross-project context leakage                         | Per-slug directory verification      |

---

## §2 — Actors

### 2.1 Operator Actors (Người dùng trực tiếp của skill)

#### ACTOR-01: Solo Developer

- **Role**: Lập trình viên cá nhân sử dụng skill để thay thế cả team trong dự án solo hoặc side project
- **Technical proficiency**: Expert (biết code, hiểu kiến trúc, quen dùng Claude Code)
- **Domain knowledge**: Intermediate đến Expert (phụ thuộc dự án)
- **Frequency of use**: Daily đến weekly; thường trigger toàn bộ pipeline cho mỗi feature lớn
- **Channel**: Claude Code CLI (terminal hoặc VS Code extension)
- **Accessibility needs**: None (power user)
- **Data access scope**: Full operator — có thể trigger bất kỳ agent nào, override QA decision, pass extra context
- **Key need**: Nhanh, đầy đủ artifact, không phải nhập lại context thủ công giữa các bước

#### ACTOR-02: Technical Lead / Architect

- **Role**: Senior developer dùng skill để validate thiết kế, review architectural decisions, và nhận second opinion từ AI TechLead agent
- **Technical proficiency**: Expert
- **Domain knowledge**: Expert trong technical domain; intermediate trong business domain
- **Frequency of use**: Weekly; thường chạy per-agent mode (chỉ `/team-techlead`) để deep-dive một phase
- **Channel**: Claude Code CLI
- **Accessibility needs**: None
- **Data access scope**: Full operator; thường quan tâm nhất đến TechLead và QA outputs
- **Key need**: ADR chất lượng cao, architectural critique rõ ràng, có thể override với additional constraints

#### ACTOR-03: Product Manager / BA (Human)

- **Role**: PM hoặc BA thực dùng skill để simulate team estimation, feasibility check, story breakdown khi chưa có team dev
- **Technical proficiency**: Intermediate (biết dùng CLI, không nhất thiết biết code sâu)
- **Domain knowledge**: Expert trong business domain; basic trong technical domain
- **Frequency of use**: Monthly đến weekly; chạy full pipeline hoặc chỉ BA + PM phases
- **Channel**: Claude Code CLI
- **Accessibility needs**: Clear instructions in skill prompts; không assume terminal expertise
- **Data access scope**: Full operator; quan tâm nhất đến BA output (user stories) và PM output (sprint plan)
- **Key need**: User stories chuẩn format, sprint plan có story points, không cần hiểu deep technical artifacts

#### ACTOR-04: Startup Founder / Solo Maker

- **Role**: Người xây dựng sản phẩm một mình, dùng skill như là virtual CTO + team
- **Technical proficiency**: Basic đến Intermediate (biết code nhưng không phải chuyên gia)
- **Domain knowledge**: Expert trong business/product domain; intermediate trong technical
- **Frequency of use**: Frequent (multiple times per week); dùng cho mọi feature từ MVP đến launch
- **Channel**: Claude Code CLI
- **Accessibility needs**: Clear progress indicators; không muốn đọc quá nhiều technical jargon không cần thiết
- **Data access scope**: Full operator
- **Key need**: Full pipeline từ idea đến code đến test plan với minimal manual effort

---

### 2.2 Virtual Team Agent Actors (do skill tạo ra và điều phối)

#### ACTOR-05: BA Agent (Business Analyst)

- **Role**: Phân tích requirement của operator, viết user stories theo chuẩn, clarify business rules và acceptance criteria
- **Technical proficiency**: Intermediate (hiểu cả business và technical để bridge gap)
- **Domain knowledge**: Phụ thuộc input — adapts to domain
- **Channel**: Invoked via Claude Agent tool; đọc/ghi file system
- **Data access scope**: Read (input từ operator), Write (`projects/{slug}/team/ba/`)
- **Underlying model**: `claude-sonnet-4-6`
- **Can spawn sub-agents**: Yes — để phân tích domain chuyên sâu, research business rules
- **Output artifacts**: `requirements.md`, `user-stories.md`, `acceptance-criteria.md`, `business-rules.md`

#### ACTOR-06: TechLead Agent (System Designer / Senior Tech Lead)

- **Role**: Thiết kế kiến trúc hệ thống, lựa chọn và justify tech stack, viết Architecture Decision Records, tạo ERD và sequence diagrams (Mermaid)
- **Technical proficiency**: Expert
- **Domain knowledge**: Expert technical; intermediate business
- **Channel**: Invoked via Claude Agent tool; đọc BA output + ghi file system
- **Data access scope**: Read (BA artifacts + operator context), Write (`projects/{slug}/team/techlead/`)
- **Underlying model**: `claude-opus-4-8` (deep reasoning required)
- **Can spawn sub-agents**: Yes — để research specific tech decisions, generate detailed diagrams
- **Output artifacts**: `architecture.md`, `ADR-{n}.md`, `ERD.md`, `sequence-diagrams.md`, `tech-stack.md`
- **Special authority**: Tie-breaker khi có conflict giữa các agents (advisory — user vẫn là final)

#### ACTOR-07: PM Agent (Scrum Master / Project Manager)

- **Role**: Điều phối workflow giữa các agents, tạo sprint board, breakdown tasks từ user stories, assign story points, track progress qua TodoWrite
- **Technical proficiency**: Basic đến Intermediate (routing và coordination, không deep technical)
- **Domain knowledge**: Intermediate (đủ để estimate và plan)
- **Channel**: Invoked via Claude Agent tool; đọc BA + TechLead output; ghi file + gọi TodoWrite
- **Data access scope**: Read (BA + TechLead artifacts), Write (`projects/{slug}/team/pm/`), Write (TodoWrite tool)
- **Underlying model**: `claude-haiku-4-5` (fast, coordination-focused)
- **Can spawn sub-agents**: No (coordination role — light weight là ưu tiên)
- **Output artifacts**: `sprint-plan.md`, `task-breakdown.md`, `story-points.md`, TodoWrite entries

#### ACTOR-08: BE Dev Agent (Backend Developer)

- **Role**: Generate backend code theo thiết kế của TechLead và tasks trong sprint plan. Bao gồm API endpoints, database schema, migrations, business logic, và PR description
- **Technical proficiency**: Expert trong backend development
- **Domain knowledge**: Intermediate (đủ để implement business rules từ BA output)
- **Channel**: Invoked via Claude Agent tool; đọc TechLead + PM output; ghi code files
- **Data access scope**: Read (TechLead + PM artifacts), Write (`projects/{slug}/team/be/`)
- **Underlying model**: `claude-sonnet-4-6`
- **Can spawn sub-agents**: Yes — để generate từng module độc lập (e.g., sub-agent cho auth module, sub-agent cho payment module)
- **Output artifacts**: API route files, schema definition files, migration files, `pr-description.md`
- **Security constraint**: KHÔNG ĐƯỢC hardcode credentials, API keys, passwords trong bất kỳ generated file nào

#### ACTOR-09: FE Dev Agent (Frontend Developer)

- **Role**: Generate frontend code theo UI requirements và API contracts từ BE Dev. Bao gồm UI components, pages, state management, API integration
- **Technical proficiency**: Expert trong frontend development
- **Domain knowledge**: Intermediate (đủ để translate UI requirements vào components)
- **Channel**: Invoked via Claude Agent tool; đọc TechLead + BE output; ghi code files
- **Data access scope**: Read (TechLead + BE artifacts), Write (`projects/{slug}/team/fe/`)
- **Underlying model**: `claude-sonnet-4-6`
- **Can spawn sub-agents**: Yes — để generate từng page hoặc component section song song
- **Output artifacts**: Component files, page files, `pr-description.md`, `api-integration.md`
- **Security constraint**: KHÔNG ĐƯỢC hardcode credentials, environment secrets trong bất kỳ generated file nào

#### ACTOR-10: Tester Agent

- **Role**: Viết test plan đầy đủ từ BA acceptance criteria, generate test cases (unit/integration/e2e), tạo bug report template, và flag bất kỳ inconsistency logic nào giữa requirements và implementation artifacts
- **Technical proficiency**: Expert trong testing methodologies
- **Domain knowledge**: Intermediate (đủ để derive test cases từ business rules)
- **Channel**: Invoked via Claude Agent tool; đọc BA + BE + FE output; ghi test files
- **Data access scope**: Read (BA + BE + FE artifacts), Write (`projects/{slug}/team/tester/`)
- **Underlying model**: `claude-sonnet-4-6`
- **Can spawn sub-agents**: Yes — để viết test suites song song (unit tests sub-agent, e2e tests sub-agent)
- **Output artifacts**: `test-plan.md`, `test-cases-unit.md`, `test-cases-integration.md`, `test-cases-e2e.md`, `bug-report-template.md`
- **Cross-agent flag authority**: CÓ THỂ và ĐƯỢC KHUYẾN KHÍCH flag logic errors từ BA/BE/FE artifacts

#### ACTOR-11: QA/QC Agent

- **Role**: Review tất cả artifacts từ toàn bộ pipeline, kiểm tra process compliance, tạo quality report, và issue advisory sign-off hoặc rejection recommendation cho operator
- **Technical proficiency**: Expert (phải hiểu cả technical và business artifacts)
- **Domain knowledge**: Expert trong quality assurance methodologies
- **Channel**: Invoked via Claude Agent tool; đọc TẤT CẢ artifacts từ mọi agent trước; ghi QA files
- **Data access scope**: Read (ALL artifacts từ BA đến Tester), Write (`projects/{slug}/team/qa/`)
- **Underlying model**: `claude-opus-4-8` (comprehensive review requires deep reasoning)
- **Can spawn sub-agents**: Yes — để review từng domain (technical quality vs. process compliance) song song
- **Output artifacts**: `quality-report.md`, `compliance-check.md`, `sign-off.md` (APPROVED / CONDITIONAL / REJECTED với danh sách issues)
- **Authority**: Advisory only — operator là final decision maker cho sign-off

---

## §3 — Features (IN Scope)

### Feature Cluster A: Workflow Engine

#### F-A01: Dual Trigger Mode

- **Priority**: Essential
- **Description (user's words)**: "Có thể cho user sử dụng tùy chỉnh, nếu muốn các Agent tự động làm mà ko cần check thì sử dụng cm khác, còn nếu làm từng agent check thì có thể gọi tới cm của agent đó"
- **Expanded detail**:
  - **Full-auto mode** (`/team` hoặc `/team-build "{requirement}"`): Toàn bộ pipeline BA → TechLead → PM → BE → FE → Tester → QA chạy tự động từ đầu đến cuối. Mỗi agent chạy xong → flush artifacts → trigger agent kế tiếp. Operator không cần can thiệp trừ khi có validation failure.
  - **Per-agent mode**: Mỗi role có skill command riêng:
    - `/team-ba "{requirement}"` — chỉ chạy BA agent
    - `/team-techlead` — chỉ chạy TechLead agent (đọc BA output)
    - `/team-pm` — chỉ chạy PM agent
    - `/team-dev` — chỉ chạy BE Dev agent
    - `/team-fe` — chỉ chạy FE Dev agent
    - `/team-test` — chỉ chạy Tester agent
    - `/team-qa` — chỉ chạy QA/QC agent
  - Trong per-agent mode, mỗi agent đọc artifacts đã có trên disk từ agents trước đó. Nếu artifact của agent trước chưa có, skill thông báo lỗi và yêu cầu chạy agent trước trước.
- **Actors**: ACTOR-01 đến ACTOR-04 (tất cả operators)

#### F-A02: Context Chain & Persistence

- **Priority**: Essential
- **Description**: Mỗi agent đọc output của agent trước (chained context). Tất cả artifacts được flush ra disk trước khi agent kế tiếp bắt đầu.
- **Expanded detail**:
  - Context chain là cơ chế cốt lõi đảm bảo coherence giữa các agents
  - Thứ tự đọc context của mỗi agent:
    - BA: operator input (requirement text)
    - TechLead: BA artifacts + operator input
    - PM: BA artifacts + TechLead artifacts + operator input
    - BE Dev: TechLead artifacts + PM sprint plan + operator input
    - FE Dev: TechLead artifacts + BE Dev artifacts (API contracts) + operator input
    - Tester: BA artifacts + BE Dev artifacts + FE Dev artifacts + operator input
    - QA/QC: ALL artifacts từ mọi agent + operator input
  - Persistence guarantee: artifact file phải tồn tại và có content trước khi agent kế tiếp được spawn. Nếu file trống hoặc missing → trigger validation Layer 1
  - Context survives Claude Code restart — operator có thể resume từ bất kỳ phase nào sau khi restart
- **Actors**: Tất cả agent actors (ACTOR-05 đến ACTOR-11)

#### F-A03: Hybrid Agile + Waterfall Workflow Model

- **Priority**: Essential
- **Description**: Workflow theo mô hình Hybrid — sprint-based agile trong nội bộ nhưng có milestone gates (design freeze, UAT, release sign-off)
- **Expanded detail**:
  - **Agile sprints**: PM agent tổ chức tasks thành sprints với story points. BE/FE agents generate code theo sprint tasks.
  - **Waterfall checkpoints (milestone gates)**:
    - Gate 1 — Design Freeze: Sau TechLead phase, architecture được "frozen". Mọi thay đổi sau gate này phải đi qua ADR mới.
    - Gate 2 — UAT Readiness: Sau Tester phase, Tester xác nhận test coverage đủ để UAT.
    - Gate 3 — Release Sign-off: QA/QC phase — advisory sign-off (APPROVED / CONDITIONAL / REJECTED)
  - Các gates không blocking hoàn toàn (human override có thể bypass), nhưng phải được ghi nhận trong QA report
- **Actors**: ACTOR-05 đến ACTOR-11

#### F-A04: Multi-project Isolation

- **Priority**: Essential
- **Description**: Mỗi project được isolate bởi slug, nhiều dự án có thể tồn tại cùng lúc trong workspace
- **Expanded detail**:
  - Directory structure: `projects/{slug}/team/{role}/`
  - Khi trigger `/team-ba`, operator chỉ định slug (`/team-ba --project my-app "requirement"`)
  - Không có shared state giữa projects — mỗi slug là một isolated context
  - Operator có thể list tất cả projects hiện có (`/team-list`)
  - Operator có thể resume bất kỳ project nào từ bất kỳ phase nào
- **Actors**: ACTOR-01 đến ACTOR-04

---

### Feature Cluster B: Agent Roles & Artifacts

#### F-B01: BA Phase — Requirement Analysis

- **Priority**: Essential
- **Description**: BA agent phân tích requirement đầu vào, tạo user stories theo chuẩn, define acceptance criteria, clarify business rules
- **Expanded detail**:
  - Input: Free-text requirement, PRD document, hoặc SRS artifacts từ SRS workflow (`brainstorm.md`, `spec.md`)
  - BA agent phân tích và phát hiện: actors, use cases, business rules ẩn, edge cases
  - Output format theo template bắt buộc:
    - `requirements.md`: Executive summary + requirements list
    - `user-stories.md`: Mỗi story theo format "As a {actor}, I want {action} so that {benefit}" + Story ID (US-{n})
    - `acceptance-criteria.md`: Given/When/Then format cho mỗi user story
    - `business-rules.md`: Numbered list, mỗi rule phải testable
  - BA có thể spawn sub-agents để research domain-specific rules hoặc generate domain glossary
  - Nếu requirement quá vague, BA PHẢI ghi rõ assumptions trong `requirements.md`
- **Actors**: ACTOR-04 (operator), ACTOR-05 (BA agent)

#### F-B02: TechLead Phase — Architecture & Design

- **Priority**: Essential
- **Description**: TechLead agent thiết kế kiến trúc hệ thống, lựa chọn tech stack với justification, tạo ADR, ERD, sequence diagrams
- **Expanded detail**:
  - Input: BA artifacts (requirements + user stories) + operator extra context (nếu có)
  - TechLead đánh giá functional requirements và bổ sung non-functional requirements vào architectural decisions
  - Output format theo template bắt buộc:
    - `architecture.md`: High-level architecture overview, component diagram (Mermaid), deployment model
    - `tech-stack.md`: Mỗi layer (Frontend, Backend, DB, Infra) với lý do chọn và alternatives đã reject
    - `ADR-001.md` ... `ADR-{n}.md`: Mỗi major decision một ADR (Context / Decision / Consequences format)
    - `ERD.md`: Entity Relationship Diagram (Mermaid), all entities + relationships
    - `sequence-diagrams.md`: Sequence diagrams (Mermaid) cho các flows quan trọng (auth, core transaction, error paths)
  - TechLead có thể flag inconsistencies từ BA output (cross-agent verification)
  - TechLead có thể spawn sub-agents để research specific tech options
- **Actors**: ACTOR-02 (operator — high interest), ACTOR-06 (TechLead agent)

#### F-B03: PM Phase — Sprint Planning

- **Priority**: Essential
- **Description**: PM agent tạo sprint plan từ user stories và architecture, breakdown tasks, assign story points, dùng TodoWrite để track progress trong conversation
- **Expanded detail**:
  - Input: BA artifacts + TechLead artifacts
  - PM agent organize user stories thành sprints (default: 2-week sprints)
  - Output format theo template bắt buộc:
    - `sprint-plan.md`: Sprint 1..N với mỗi sprint có goals, stories, và tasks
    - `task-breakdown.md`: Mỗi task có: ID, title, description, story reference, assigned agent role, estimated effort (S/M/L/XL)
    - `story-points.md`: Velocity estimate, total story points, sprint capacity
  - PM dùng TodoWrite để tạo task list hiển thị trong Claude Code conversation (live progress tracker)
  - PM KHÔNG spawn sub-agents (lightweight coordination role)
- **Actors**: ACTOR-03 (operator — high interest), ACTOR-07 (PM agent)

#### F-B04: BE Dev Phase — Backend Code Generation

- **Priority**: Essential
- **Description**: BE Dev agent generate backend code theo tech stack đã chọn và tasks trong sprint plan
- **Expanded detail**:
  - Input: TechLead artifacts (architecture, ERD, tech-stack) + PM sprint plan
  - BE Dev đọc tech-stack.md để chọn đúng framework/language
  - Output: code files trong `projects/{slug}/team/be/` theo cấu trúc phù hợp với tech stack
    - API route/controller files
    - Database schema files (ORM models hoặc migration files)
    - Service/business logic files
    - `pr-description.md`: PR title, summary, changes, testing notes
  - BE Dev flag bất kỳ ambiguity nào trong requirements khi implement
  - BE Dev KHÔNG hardcode credentials — dùng environment variable placeholders (`.env.example`)
  - BE Dev CÓ THỂ spawn sub-agents cho từng module (e.g., sub-agent cho auth, sub-agent cho data layer)
- **Actors**: ACTOR-01 (operator), ACTOR-08 (BE Dev agent)

#### F-B05: FE Dev Phase — Frontend Code Generation

- **Priority**: Essential
- **Description**: FE Dev agent generate frontend code theo tech stack và API contracts từ BE Dev
- **Expanded detail**:
  - Input: TechLead artifacts (architecture, tech-stack) + BE Dev artifacts (API contracts, route definitions)
  - FE Dev đọc BE artifacts để align với API contracts (endpoints, request/response shapes)
  - Output: code files trong `projects/{slug}/team/fe/`
    - UI component files
    - Page/view files
    - API integration service files
    - State management files (nếu applicable)
    - `pr-description.md`
  - FE Dev flag API contract ambiguities nếu có
  - FE Dev CÓ THỂ spawn sub-agents cho từng page/section song song
  - FE Dev KHÔNG hardcode environment-specific configs — dùng config/env variable pattern
- **Actors**: ACTOR-01 (operator), ACTOR-09 (FE Dev agent)

#### F-B06: Tester Phase — Test Plan & Test Cases

- **Priority**: Essential
- **Description**: Tester agent viết test plan đầy đủ, generate test cases (unit/integration/e2e) từ acceptance criteria, tạo bug report template
- **Expanded detail**:
  - Input: BA artifacts (user stories, acceptance criteria) + BE artifacts + FE artifacts
  - Tester derive test cases từ acceptance criteria (Given/When/Then → test steps)
  - Output format theo template bắt buộc:
    - `test-plan.md`: Scope, approach, environments, entry/exit criteria, test schedule
    - `test-cases-unit.md`: Unit test cases với test ID, scenario, input, expected output
    - `test-cases-integration.md`: Integration test scenarios (API contracts, data flows)
    - `test-cases-e2e.md`: End-to-end user journey test cases theo user stories
    - `bug-report-template.md`: Template chuẩn cho bug reporting (ID, severity, steps to reproduce, expected vs actual, environment)
  - Tester flag logic inconsistencies nếu implementation artifacts không match requirements (cross-agent verification)
  - Tester CÓ THỂ spawn sub-agents để viết test suites theo loại song song
- **Actors**: ACTOR-01 đến ACTOR-04 (operators), ACTOR-10 (Tester agent)

#### F-B07: QA/QC Phase — Quality Gate & Sign-off

- **Priority**: Essential
- **Description**: QA/QC agent review toàn bộ pipeline artifacts, kiểm tra compliance với workflow rules, issue advisory sign-off
- **Expanded detail**:
  - Input: TẤT CẢ artifacts từ BA, TechLead, PM, BE, FE, Tester
  - QA/QC thực hiện:
    - **Completeness check**: Mọi required section trong mỗi artifact có đủ không?
    - **Cross-artifact consistency check**: Requirements → Architecture → Code → Tests đồng nhất không?
    - **Security artifact review**: Code có hardcoded secrets không? API có authentication không?
    - **Process compliance check**: Mọi milestone gate được pass không? ADRs có cho mọi major decision không?
  - Output format theo template bắt buộc:
    - `quality-report.md`: Detailed findings per artifact, severity level (Critical/Major/Minor)
    - `compliance-check.md`: Checklist từng process gate, PASS/FAIL/WARNING
    - `sign-off.md`: Verdict (APPROVED / CONDITIONAL / REJECTED) + danh sách conditions (nếu CONDITIONAL)
  - QA/QC KHÔNG có authority tự block pipeline — chỉ advisory
  - QA/QC CÓ THỂ spawn sub-agents để review technical artifacts và process artifacts song song
- **Actors**: ACTOR-01 đến ACTOR-04 (operators), ACTOR-11 (QA/QC agent)

---

### Feature Cluster C: Error Handling & Validation

#### F-C01: Automated Validation Layer (Layer 1)

- **Priority**: Essential
- **Description**: Skill tự kiểm tra structural completeness của mỗi artifact sau khi agent hoàn thành. Tự rerun tối đa 3 lần nếu validation fail.
- **Expanded detail**:
  - Mỗi agent có một validation schema định nghĩa required sections/headings
  - Sau khi agent ghi artifact ra disk, skill đọc lại và kiểm tra:
    - Mọi required sections có mặt không (heading-level check)?
    - File không trống không?
    - Không có placeholder chưa được fill không (e.g., "{INSERT HERE}")?
  - Nếu validation fail:
    - Attempt 1 (retry): Rerun agent với prompt bổ sung ghi rõ section nào bị thiếu
    - Attempt 2 (retry): Rerun agent với full template và strict instruction
    - Attempt 3 (retry): Final retry
    - Nếu vẫn fail sau 3 lần: Hard stop, ghi `validation-error.md` với details, thông báo operator
  - Retry counter được log để operator có thể debug
- **Actors**: Tất cả agent actors (ACTOR-05 đến ACTOR-11)

#### F-C02: Cross-agent Verification Layer (Layer 2)

- **Priority**: Essential
- **Description**: Agent sau CÓ THỂ flag logic errors trong artifacts của agent trước. Operator quyết định rerun hay override.
- **Expanded detail**:
  - Không phải automated — là part of mỗi agent's instruction: "Đọc artifacts của agent trước và flag bất kỳ inconsistency hoặc logic error nào"
  - Format flag: Trong artifact output, agent thêm section `## Flags from Previous Agents` (nếu có issues)
  - Mỗi flag phải có: ID (FLAG-{agent}-{n}), mô tả issue, artifact bị ảnh hưởng, severity (Blocker/Major/Minor), suggestion
  - Khi có flags: Skill pause (nếu per-agent mode) hoặc tạo `flags-summary.md` (nếu full-auto mode) để operator review
  - Operator decision: Rerun agent có vấn đề với adjusted context | Override và tiếp tục | Ignore (ghi lại decision)
- **Actors**: ACTOR-06 (TechLead), ACTOR-10 (Tester), ACTOR-11 (QA/QC) — có cross-agent flag authority cao nhất

#### F-C03: SRS Workflow Integration

- **Priority**: Conditional
- **Description**: Virtual Team Skill có thể nhận input từ SRS workflow artifacts (brainstorm.md, spec.md, plans/)
- **Expanded detail**:
  - Nếu operator đã có `projects/{slug}/spec.md` từ SRS workflow, BA agent đọc spec.md thay vì phân tích từ đầu
  - Mapping: SRS `spec.md` → BA artifacts (requirements, user stories, business rules được derived từ §3, §6)
  - Cho phép seamless handoff từ SRS workflow vào development team workflow
  - BA agent flag nếu SRS spec thiếu thông tin cần thiết cho development
- **Actors**: ACTOR-01 đến ACTOR-04 (operators — particularly Technical Lead và PM)

#### F-C04: TodoWrite Progress Tracking

- **Priority**: Conditional
- **Description**: PM agent dùng Claude Code TodoWrite tool để hiển thị sprint board và task progress trong conversation
- **Expanded detail**:
  - PM agent tạo todo entries cho mỗi task trong sprint plan
  - Mỗi agent khi bắt đầu mark task của mình là "in_progress"; khi hoàn thành mark "completed"
  - Operator có thể xem live progress qua TodoWrite entries trong conversation
  - TodoWrite entries không persist qua session restart (chỉ trong session); file artifacts persist
- **Actors**: ACTOR-07 (PM agent)

---

## §4 — OUT of Scope

| Feature                                                | Lý do loại trừ                                                                                                                         | Planned version                     |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| Real git push lên remote (GitHub/GitLab)               | Skill KHÔNG tự động thực hiện destructive/irreversible external actions. User tự quyết định khi nào push. An toàn và controllable hơn. | v2 (opt-in flag)                    |
| Real-time multi-user collaboration                     | Skill là single-user tool. Multi-user session architecture phức tạp và ngoài scope của Claude Code skill system.                       | v3                                  |
| DevOps/Infra phase (Dockerfile, CI/CD, GitHub Actions) | Cần định nghĩa rõ dependency với BE/FE output. Deferred để không overscope v1.                                                         | v2                                  |
| Live code execution / runtime testing                  | Skill chỉ generate và review artifacts. Running actual code đòi hỏi sandbox environment setup ngoài scope v1.                          | v2 (với Claude Code terminal tools) |
| Web app / PM dashboard UI                              | Virtual Team Skill là CLI/skill-based tool. Xây dựng web app sẽ là separate product.                                                   | v3                                  |
| Billing / cost tracking per agent run                  | Token usage per agent không tracked trong skill layer. Monitoring thuộc về Anthropic dashboard.                                        | Not planned                         |
| Agent-to-agent real-time communication                 | Agents giao tiếp qua file artifacts (async), không phải real-time message passing.                                                     | v3                                  |
| Custom agent personality/persona configuration         | Agent behavior do skill .md file định nghĩa, không có runtime personality config trong v1.                                             | v2                                  |

---

## §5 — Technical Constraints

### 5.1 Implementation Architecture

- **Skill files**: Mỗi role là một Claude Code skill file (`.md` format) trong `.claude/skills/` directory
- **Orchestration**: Orchestrator skill (`team.md`) dùng Claude Agent tool để spawn individual role agents
- **Per-agent skills**: Mỗi role có skill file riêng cho per-agent mode (`team-ba.md`, `team-techlead.md`, etc.)
- **No external framework**: Hoàn toàn dựa trên Claude Code native tools (Agent, TodoWrite, Read, Write, Glob, Grep)

### 5.2 Model Assignment

| Role Agent     | Model               | Justification                                                         |
| -------------- | ------------------- | --------------------------------------------------------------------- |
| BA Agent       | `claude-sonnet-4-6` | Balanced: cần language quality nhưng không cần extreme deep reasoning |
| TechLead Agent | `claude-opus-4-8`   | Deep reasoning cho architectural decisions, trade-off analysis        |
| PM Agent       | `claude-haiku-4-5`  | Fast, coordination-focused; tasks đơn giản hơn                        |
| BE Dev Agent   | `claude-sonnet-4-6` | Good code generation quality; cost-effective cho longer output        |
| FE Dev Agent   | `claude-sonnet-4-6` | Tương tự BE Dev                                                       |
| Tester Agent   | `claude-sonnet-4-6` | Good test case generation; balanced                                   |
| QA/QC Agent    | `claude-opus-4-8`   | Comprehensive review cần deep reasoning across all artifacts          |

### 5.3 File System Layout

```
projects/
  {slug}/
    brainstorm.md          ← SRS workflow output (optional input)
    spec.md                ← SRS workflow output (optional input)
    team/
      ba/
        requirements.md
        user-stories.md
        acceptance-criteria.md
        business-rules.md
      techlead/
        architecture.md
        tech-stack.md
        ADR-001.md
        ADR-{n}.md
        ERD.md
        sequence-diagrams.md
      pm/
        sprint-plan.md
        task-breakdown.md
        story-points.md
      be/
        {tech-appropriate structure}
        pr-description.md
      fe/
        {tech-appropriate structure}
        pr-description.md
      tester/
        test-plan.md
        test-cases-unit.md
        test-cases-integration.md
        test-cases-e2e.md
        bug-report-template.md
      qa/
        quality-report.md
        compliance-check.md
        sign-off.md
    validation-errors/
        {agent}-attempt-{n}.md   ← validation failure logs
    flags-summary.md             ← cross-agent flags (full-auto mode)
```

### 5.4 Platform Compatibility

- **Target platforms**: Windows 10/11, macOS, Linux
- **Path handling**: Skill files phải dùng relative paths hoặc cross-platform path resolution. Không hardcode OS-specific separators.
- **Shell compatibility**: Không dùng bash-only hoặc PowerShell-only commands trong skill instructions

### 5.5 Output Format

- **All artifacts**: Human-readable Markdown (`.md`)
- **Diagrams**: Mermaid syntax embedded trong Markdown (`.md` files với ```mermaid blocks)
- **Code artifacts**: Language-appropriate files trong `team/be/` và `team/fe/` (`.js`, `.ts`, `.py`, etc. — phụ thuộc tech stack)
- **No binary formats**: PDF, DOCX, Excel — không generate
- **Encoding**: UTF-8

### 5.6 Claude Code Compatibility

- Tương thích với Claude Code skill system: skill files dùng YAML frontmatter không (plain markdown format)
- Dùng Skill tool để trigger skills
- Dùng Agent tool để spawn sub-agents
- Dùng TodoWrite tool trong PM agent
- Dùng Read/Write/Glob/Grep tools cho file operations
- Không dùng external MCP servers (standalone)

### 5.7 Security

- **Data privacy**: Project context và artifacts chỉ đi qua Anthropic API. Không có external data transmission.
- **No credential storage**: Agents được instructed explicitly không hardcode secrets. Generated code dùng `.env` variable pattern.
- **Local-only**: Tất cả artifacts stored locally trong working directory — không upload lên external service.

### 5.8 Integration Points

| System                                    | Protocol                      | Direction            | Notes                                         |
| ----------------------------------------- | ----------------------------- | -------------------- | --------------------------------------------- |
| SRS Workflow (`sr-brainstorm`, `sr-spec`) | File read (Markdown)          | SRS → Virtual Team   | Optional: BA reads existing SRS artifacts     |
| Claude Code TodoWrite                     | Built-in tool call            | PM Agent → TodoWrite | Sprint board tracking in conversation         |
| Anthropic Claude API                      | HTTP (managed by Claude Code) | Skill → API          | Model calls per agent (model varies per role) |
| Local file system                         | File read/write               | Agents → Disk        | All artifact persistence                      |

---

## §6 — Business Rules

**BR-01**: Một agent KHÔNG ĐƯỢC bắt đầu thực thi nếu artifact bắt buộc của agent trước chưa tồn tại trên disk. Skill phải kiểm tra file existence và content non-empty trước khi spawn agent kế tiếp. Nếu file missing: thông báo lỗi rõ ràng, gợi ý lệnh để chạy agent còn thiếu.

**BR-02**: Mỗi artifact sau khi được ghi ra disk PHẢI được kiểm tra structural completeness (có đủ required section headings). Nếu validation fail, skill tự động rerun agent đó. Số lần retry tối đa là 3. Sau 3 lần fail: skill hard stop, ghi `validation-errors/{agent}-final-failure.md`, thông báo operator với details.

**BR-03**: Agent sau đọc artifacts của agent trước PHẢI flag bất kỳ logic inconsistency, missing information, hoặc contradictions nào mà nó phát hiện. Flag PHẢI được ghi vào section `## Flags from Previous Agents` trong artifact của mình. Nếu không có flags: section này ghi "No flags detected."

**BR-04**: QA/QC Agent có vai trò advisory. QA/QC KHÔNG có quyền tự động block pipeline. Mọi rejection hay override phải do Operator quyết định. Sign-off file phải rõ ràng: APPROVED / CONDITIONAL / REJECTED với danh sách conditions.

**BR-05**: Không có agent nào được hardcode secrets, API keys, passwords, tokens, hoặc bất kỳ sensitive credential nào trong generated artifacts. Code artifacts PHẢI dùng environment variable placeholders (e.g., `process.env.API_KEY`, `os.environ["DB_PASSWORD"]`). Nếu agent phát hiện yêu cầu cần credential: dùng placeholder và ghi chú trong artifact.

**BR-06**: Context chain thứ tự mặc định trong full-auto mode là: BA → TechLead → PM → BE Dev → FE Dev → Tester → QA/QC. Thứ tự này KHÔNG thể thay đổi trong full-auto mode. Per-agent mode không bắt buộc thứ tự nhưng agent sẽ cảnh báo nếu dependent artifacts chưa có.

**BR-07**: Mỗi sub-agent spawned bởi một role agent KHÔNG được spawn thêm sub-agents (depth tối đa: 2 levels). Sub-agent chỉ dùng Read/Write/Glob/Grep tools — không dùng Agent tool.

**BR-08**: Mọi projects phải được isolate bởi `{slug}`. Không có bất kỳ shared file hay shared state nào giữa `projects/{slug-a}/` và `projects/{slug-b}/`. Operator phải chỉ định slug rõ ràng khi trigger bất kỳ agent nào.

**BR-09**: Tất cả artifacts phải được flush ra disk (Write tool hoàn thành) TRƯỚC KHI agent kế tiếp được spawn. "Flush" nghĩa là Write tool đã return success — không chỉ là content trong memory.

**BR-10**: Trong per-agent mode, nếu operator pass extra context (`--context "..."`), extra context đó được prepend vào prompt của agent đó, nhưng KHÔNG ghi vào artifact files. Extra context là ephemeral — không persist sang agent kế tiếp trừ khi được ghi vào artifact.

**BR-11**: Retry log (`validation-errors/{agent}-attempt-{n}.md`) PHẢI ghi lại: timestamp, agent name, attempt number, sections found, sections missing, và raw validation result. Log này không bị xóa sau khi validation thành công — để phục vụ debugging.

**BR-12**: Nếu có conflict giữa SRS workflow artifacts (brainstorm.md, spec.md) và operator's runtime requirement input, BA Agent PHẢI flag conflict đó và hỏi operator để clarify. BA KHÔNG được silently override SRS artifacts.

---

## §7 — NFR Baselines

| ID     | Characteristic          | Target                                                                                                                             | Status                                                                                |
| ------ | ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| NFR-01 | Structural Completeness | 100% artifacts phải pass section validation (required headings present) trước khi agent kế tiếp bắt đầu                            | Confirmed                                                                             |
| NFR-02 | Persistence             | 100% artifacts flush ra disk thành công. Context survive Claude Code session restart — operator có thể resume từ bất kỳ phase nào. | Confirmed                                                                             |
| NFR-03 | Content Depth           | Không giới hạn dung lượng artifact. Mỗi artifact phải đầy đủ chi tiết cho mục đích sử dụng (không truncate vì context limits).     | Confirmed                                                                             |
| NFR-04 | Retry Resilience        | Auto-retry tối đa 3 lần per agent cho validation failures. Sau 3 fail → hard stop với clear error report.                          | Confirmed                                                                             |
| NFR-05 | Data Privacy            | Zero external data transmission ngoài Anthropic API. Không có artifact hoặc user data nào được gửi đến third-party services.       | Confirmed                                                                             |
| NFR-06 | Security                | Zero hardcoded credentials trong bất kỳ generated artifact nào. Credential detection là part of QA/QC review.                      | Confirmed                                                                             |
| NFR-07 | Platform Compatibility  | 100% functional trên Windows 10/11, macOS 12+, Ubuntu 20.04+. Không có OS-specific dependencies.                                   | Confirmed                                                                             |
| NFR-08 | Multi-project Isolation | Zero cross-project context leakage. Mỗi `{slug}` directory là isolated workspace.                                                  | Confirmed                                                                             |
| NFR-09 | Sub-agent Depth         | Maximum 2 levels deep (role agent → sub-agent). Sub-agents không được spawn thêm agents.                                           | Confirmed                                                                             |
| NFR-10 | Skill Compatibility     | 100% tương thích với Claude Code skill system hiện tại. Không require external MCP servers, external CLIs, hoặc custom runtimes.   | Confirmed                                                                             |
| NFR-11 | Agent Response Time     | [TBD — không đặt timeout vì operator không muốn limit. Nhưng nên document typical expected time per phase]                         | [TBD: Measure in testing — owner: v1 implementation — resolve-by: first e2e test run] |
| NFR-12 | Validation Speed        | Structural validation (heading check) phải hoàn thành < 5 giây (local file read — trivial operation).                              | Confirmed                                                                             |

---

## §8 — Assumptions

**ASS-01**: Operator đã có Claude Code CLI cài đặt và configured với Anthropic API key. Skill không handle API authentication hoặc Claude Code setup.

- _If wrong_: Skill không chạy được; cần add setup documentation hoặc prerequisite check.

**ASS-02**: Operator có đủ Anthropic API quota để chạy nhiều agent calls liên tiếp (mỗi run full pipeline có thể là 7+ LLM calls, một số dùng Opus).

- _If wrong_: Pipeline fail giữa chừng vì rate limit; cần add rate limit handling và clear error message.

**ASS-03**: Mỗi agent có thể hoàn thành nhiệm vụ của mình trong một single LLM call (hoặc một số calls nếu spawn sub-agents). Không có agent nào cần interactive back-and-forth với operator trong full-auto mode.

- _If wrong_: Full-auto mode không work cho complex requirements; cần design semi-auto checkpoint mode.

**ASS-04**: File system artifacts đủ để carry context giữa agents. Không cần conversation history sharing giữa agents.

- _If wrong_: Agents generate incoherent artifacts vì thiếu context; cần thêm context injection mechanism.

**ASS-05**: Operator's requirement input (text description, PRD) đủ cho BA agent phân tích mà không cần interactive clarification. BA sẽ document assumptions thay vì hỏi lại.

- _If wrong_: BA output có nhiều assumptions, quality thấp; khuyến khích operator dùng SRS workflow trước để tạo detailed spec.

**ASS-06**: Tech stack do TechLead agent chọn được operator chấp nhận (hoặc operator sẽ override bằng extra context khi trigger TechLead phase). Không có interactive tech stack selection dialog.

- _If wrong_: Generated code không dùng tech stack operator muốn; cần add `--tech-stack` parameter cho `/team-techlead`.

**ASS-07**: Diagrams được generated bằng Mermaid syntax có thể được rendered bởi operator's environment (VS Code Mermaid Preview, GitHub, Notion, etc.).

- _If wrong_: Diagrams không hiển thị; cần add ASCII fallback hoặc alternative diagram format option.

**ASS-08**: Sub-agents spawned bởi role agents được coi là internal implementation details — operator không trực tiếp control chúng. Sub-agent output được hợp nhất vào main agent output bởi role agent trước khi ghi ra disk.

- _If wrong_: Sub-agent outputs cần được reviewed riêng; thiết kế lại sub-agent output handling.

---

## §9 — Open Items

| ID    | Unknown                                                                                                                                                                | Owner                          | Impact if Unresolved                                                                   | Target resolve                 |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------ |
| OI-01 | **Template definitions**: Mỗi role agent cần template cụ thể với exact required section headings cho validation Layer 1. Chưa có danh sách headings bắt buộc per role. | Implementation (sr:plan phase) | Validation Layer 1 (F-C01) không thể implement mà không có templates. BLOCKER.         | sr:plan phase                  |
| OI-02 | **Skill naming convention**: `/team-ba` hay `/virtual-ba` hay `/vteam-ba`? Chưa có convention.                                                                         | Operator (user)                | Inconsistent command names gây khó nhớ và documentation khó viết.                      | Trước khi viết skill .md files |
| OI-03 | **Sub-agent depth — edge cases**: Hiện tại max depth 2. Có trường hợp nào cần depth 3 không? (e.g., Tester → sub-agent → sub-sub-agent cho specific test scenarios?)   | v2 planning                    | Nếu sub-agent cần spawn thêm, BR-07 bị violated; cần sửa rule trước khi implement.     | v2                             |
| OI-04 | **DevOps v2 scope**: Khi nào thêm DevOps phase? Dependency rõ ràng trên BE/FE artifacts là gì? Input/output cụ thể là gì?                                              | v2 planning                    | Không block v1 nhưng ảnh hưởng đến file structure design (cần reserve `team/devops/`). | v2 spec                        |
| OI-05 | **Live code execution in v2**: Cụ thể sẽ dùng Claude Code terminal tools như thế nào để actually run tests? Sandbox environment cần gì?                                | v2 planning                    | Không block v1. Cần research Claude Code Bash tool capabilities.                       | v2                             |
| OI-06 | **Typical wall-clock time per phase**: NFR-11 chưa có số cụ thể. Cần measure sau khi có e2e test run đầu tiên.                                                         | v1 testing                     | Không block development. Cần để set operator expectations.                             | After first e2e test           |
| OI-07 | **Conflict resolution khi BA và SRS spec mâu thuẫn** (BR-12): Cụ thể BA hỏi operator như thế nào trong full-auto mode mà không break automation?                       | Implementation                 | Nếu không giải quyết, full-auto mode có thể stuck khi có SRS input conflicts.          | sr:plan phase                  |
| OI-08 | **Extra context `--context` parameter UX**: Format cụ thể của extra context flag cho per-agent mode. File path? Inline text? Cả hai?                                   | Implementation                 | Operator không biết cách pass context; documentation sẽ không rõ ràng.                 | sr:plan phase                  |
