# Virtual Team Skill — Hướng dẫn tiếng Việt

[Tiếng Việt](./README.vi.md) · [English](./README.md)

Bộ công cụ AI mô phỏng một đội phát triển phần mềm hoàn chỉnh gồm 7 vai trò. Bạn chỉ cần nhập ý tưởng — hệ thống tự động tạo ra toàn bộ tài liệu từ phân tích yêu cầu đến ký duyệt phát hành.

## Mục lục agent skill

| Skill | Trách nhiệm |
|---|---|
| [team](./skills/team/) | Điều phối toàn bộ pipeline |
| [team-ba](./skills/team-ba/) | Phân tích yêu cầu và nghiệp vụ |
| [team-techlead](./skills/team-techlead/) | Kiến trúc và Design Freeze |
| [team-pm](./skills/team-pm/) | Sprint plan và task breakdown |
| [team-dev](./skills/team-dev/) | Triển khai backend |
| [team-fe](./skills/team-fe/) | Triển khai frontend |
| [team-test](./skills/team-test/) | Thiết kế test và UAT Readiness |
| [team-qa](./skills/team-qa/) | Audit cuối và release sign-off |
| [team-list](./skills/team-list/) | Trạng thái project và phase |

---

## Hệ thống làm được gì?

Nhập một câu mô tả project → nhận về đầy đủ:

| Vai trò | Tài liệu tạo ra |
|---|---|
| BA (Phân tích nghiệp vụ) | Yêu cầu hệ thống, user stories, tiêu chí chấp nhận, business rules |
| TechLead (Trưởng kỹ thuật) | Kiến trúc hệ thống, tech stack, ERD, sequence diagrams, ADRs |
| PM (Quản lý dự án) | Kế hoạch sprint, phân rã công việc, ước tính story points |
| BE Dev (Lập trình viên Backend) | Code backend, file .env.example, mô tả pull request |
| FE Dev (Lập trình viên Frontend) | Code frontend, mô tả pull request |
| Tester (Kiểm thử) | Kế hoạch test, test cases, template báo cáo lỗi |
| QA/QC (Đảm bảo chất lượng) | Báo cáo chất lượng, kiểm tra tuân thủ, phiếu ký duyệt |

Tất cả tài liệu được lưu vào thư mục `projects/{tên-project}/team/` trên máy bạn.

---

## Yêu cầu cài đặt

Trước khi dùng, bạn cần có:

- **Claude Code CLI** — đã cài và đang chạy (bạn đang đọc file này nghĩa là đã có ✓)
- **Python 3.8 trở lên** — dùng để chạy các hook kiểm tra tự động

Kiểm tra Python:
```
python --version
```

Nếu chưa có, tải tại [python.org/downloads](https://python.org/downloads) — nhớ tick **"Add Python to PATH"** khi cài.

---

## Cài đặt

Mở thư mục `virtual-team-skill/` trong Claude Code là dùng được ngay — toàn bộ skills và hooks đã có sẵn.

Nếu muốn dùng ở project khác, copy skills và hooks:

```bash
cp -r virtual-team-skill/skills/ ten-project-cua-ban/skills/
cp -r virtual-team-skill/hooks/ ten-project-cua-ban/hooks/
cp virtual-team-skill/settings.json ten-project-cua-ban/settings.json
```

---

## Bắt đầu nhanh

**Chạy toàn bộ pipeline (7 vai trò, 1 lệnh):**

```
/team "mô tả project của bạn" --project ten-project --level fresh
```

Ví dụ thực tế:

```
/team "app quản lý chi tiêu cá nhân, thêm giao dịch thu/chi, xem lịch sử và thống kê theo tháng" --project expense-tracker --level fresh
```

**Chạy từng vai trò thủ công:**

```
/team-ba "mô tả project" --project ten-project --level fresh
/team-techlead --project ten-project
/team-pm --project ten-project
/team-dev --project ten-project
/team-fe --project ten-project
/team-test --project ten-project
/team-qa --project ten-project
```

---

## Chọn Level phù hợp

`--level` là tham số **bắt buộc**. Nó xác định độ phức tạp của kiến trúc, code và tiêu chuẩn kiểm thử.

| Level | Dùng khi nào | Kiến trúc |
|---|---|---|
| `fresh` | Bài tập môn học, project học thử | Monolith đơn giản, MVC cơ bản |
| `junior` | Đồ án tốt nghiệp, internship | Layered MVC (Controller → Service → Repository) |
| `mid` | Sản phẩm thật, team nhỏ, startup | Clean / Hexagonal Architecture |
| `senior` | Hệ thống lớn, production nghiêm túc | DDD + Clean Architecture, enterprise patterns |

**Không chắc chọn gì?** → Chọn `junior` nếu bạn đang học, `mid` nếu làm product thật.

### Level ảnh hưởng đến những gì?

- **BA** — `fresh`: viết 2 kịch bản/user story. `senior`: viết 5+ kịch bản bao gồm cả hiệu năng và bảo mật
- **TechLead** — `fresh`: thiết kế Monolith đơn giản. `senior`: DDD đầy đủ với bounded contexts
- **PM** — `fresh`: chia task ≤ 4 giờ, nhân hệ số 2.5 cho story points. `senior`: task mức epic, hệ số 0.75
- **BE/FE Dev** — `fresh`: code thẳng vào route handler. `mid`+: bắt buộc phân tách layer, xử lý lỗi có taxonomy
- **Tester** — `fresh`: test happy path. `senior`: test đầy đủ pyramid + mutation testing ≥ 80% coverage
- **QA/QC** — `fresh`: pass nếu CRUD chạy đúng. `senior`: fail nếu thiếu Circuit Breaker hoặc distributed tracing

---

## Danh sách lệnh

| Lệnh | Mô tả |
|---|---|
| `/team "mô tả" --level {level} [--project slug]` | Chạy toàn bộ pipeline 7 vai trò |
| `/team-ba "mô tả" --level {level} [--project slug]` | Chỉ chạy BA |
| `/team-techlead [--project slug]` | Chỉ chạy TechLead |
| `/team-pm [--project slug]` | Chỉ chạy PM |
| `/team-dev [--project slug]` | Chỉ chạy BE Dev |
| `/team-fe [--project slug]` | Chỉ chạy FE Dev |
| `/team-test [--project slug]` | Chỉ chạy Tester |
| `/team-qa [--project slug]` | Chỉ chạy QA/QC |
| `/team-list` | Xem trạng thái tất cả các project |

### Các tham số

**`--level {level}`** *(bắt buộc khi chạy `/team` hoặc `/team-ba`)*
Sau lần đầu chạy, level được lưu vào `.project-config.md` — các lệnh sau không cần nhập lại.

**`--project {slug}`**
Tên định danh project (viết liền, không dấu, dùng dấu gạch ngang). Ví dụ: `my-app`, `quan-ly-don-hang`. Nếu không nhập, hệ thống tự dùng tên thư mục hiện tại.

**`--context "nội dung hoặc đường dẫn"`**
Thông tin bổ sung cho BA. Có thể là text thẳng hoặc đường dẫn file (bắt đầu bằng `./` hoặc `/`).

**`--spec <path>`**
BA đọc từ file markdown bất kỳ tại `{path}` làm input chính. Hỗ trợ mọi định dạng markdown — SRS spec, brainstorm notes, PRD, yêu cầu thô.

---

## Cấu trúc thư mục output

```
projects/{ten-project}/
└── team/
    ├── .project-config.md         ← Cấu hình level — tất cả agents đọc từ đây
    ├── ba/
    │   ├── requirements.md        ← Danh sách yêu cầu
    │   ├── user-stories.md        ← User stories theo format As a / I want / So that
    │   ├── acceptance-criteria.md ← Tiêu chí chấp nhận (Given / When / Then)
    │   └── business-rules.md      ← Quy tắc nghiệp vụ
    ├── techlead/
    │   ├── architecture.md        ← Kiến trúc hệ thống + [Gate 1: Design Freeze]
    │   ├── tech-stack.md          ← Bảng công nghệ được chọn và lý do
    │   ├── ERD.md                 ← Sơ đồ quan hệ thực thể
    │   ├── sequence-diagrams.md   ← Sơ đồ tuần tự cho các luồng chính
    │   └── ADR-001.md ...         ← Quyết định kiến trúc (Architecture Decision Records)
    ├── pm/
    │   ├── sprint-plan.md         ← Kế hoạch sprint
    │   ├── task-breakdown.md      ← Phân rã task chi tiết
    │   └── story-points.md        ← Ước tính điểm
    ├── be/
    │   ├── src/...                ← Code backend
    │   ├── .env.example           ← Template biến môi trường
    │   └── pr-description.md      ← Mô tả pull request
    ├── fe/
    │   ├── src/...                ← Code frontend
    │   └── pr-description.md
    ├── tester/
    │   ├── test-plan.md           ← Kế hoạch kiểm thử + [Gate 2: UAT Readiness]
    │   ├── test-cases-unit.md
    │   ├── test-cases-integration.md
    │   ├── test-cases-e2e.md
    │   └── bug-report-template.md
    ├── qa/
    │   ├── quality-report.md      ← Báo cáo chất lượng toàn bộ pipeline
    │   ├── compliance-check.md    ← Kiểm tra tuân thủ
    │   └── sign-off.md            ← Phiếu ký duyệt [Gate 3: Release Sign-off]
    ├── validation-errors/         ← Chỉ tạo khi có lỗi validation
    └── flags-summary.md           ← Tổng hợp cảnh báo xuyên-agent (nếu có)
```

---

## Các cột mốc chất lượng (Milestone Gates)

Pipeline có 3 cột mốc tự động:

| Cột mốc | Sau phase | Ý nghĩa |
|---|---|---|
| Gate 1: Design Freeze | TechLead | Kiến trúc đã được chốt — mọi thay đổi sau cần có ADR mới |
| Gate 2: UAT Readiness | Tester | Test coverage đã đủ để bắt đầu UAT |
| Gate 3: Release Sign-off | QA/QC | Verdict cuối: **APPROVED** / **CONDITIONAL** / **REJECTED** |

Gate 3 là **tư vấn** — người vận hành có toàn quyền chấp nhận hoặc bác bỏ.

---

## Xử lý lỗi

### Lớp 0 — Kiểm tra Level (level_gate.py)

Chạy trước mọi lần ghi file. Chặn nếu `.project-config.md` chưa tồn tại hoặc level không hợp lệ.

```
[Level Gate] ✗ Chưa cấu hình level cho project này.
Chạy: /team "yêu cầu" --project {slug} --level mid
```

### Lớp 1 — Kiểm tra cấu trúc tài liệu (pre_write_validator.py)

Chạy sau Layer 0. Chặn nếu file thiếu heading bắt buộc hoặc code chứa thông tin nhạy cảm hardcode.

- Agent tự retry tối đa **3 lần**
- Lần thứ 3 thất bại → **HARD STOP** → ghi log vào `validation-errors/{agent}-attempt-3.md`

### Lớp 2 — Cờ xuyên-agent (advisory)

TechLead, Tester, QA/QC ghi cảnh báo vào phần `## Flags from Previous Agents` trong artifact của mình. Khi QA/QC xong, hook tổng hợp tất cả vào `flags-summary.md`.

---

## Tiếp tục khi bị gián đoạn

File tài liệu và `.project-config.md` tồn tại vĩnh viễn giữa các session. Để tiếp tục từ bước bị dừng:

```
/team-list                          ← xem phase nào đã xong
/team-techlead --project ten-project ← tiếp tục từ TechLead
```

Level được đọc tự động từ `.project-config.md` — không cần nhập lại `--level`.

---

## Bảo mật

- Code được tạo ra **không bao giờ chứa** mật khẩu, API key, token hardcode
- Mọi giá trị nhạy cảm đều dùng biến môi trường (`process.env.X`, `os.getenv('X')`)
- File `.env.example` liệt kê đầy đủ các biến cần cấu hình
- Hook `pre_write_validator.py` **chặn** mọi file chứa pattern credential trước khi lưu xuống đĩa

---

## Dùng file spec làm input

Truyền file markdown bất kỳ qua `--spec`:

```
/team-ba --project ten-project --level mid --spec projects/ten-project/spec.md
```

Hỗ trợ SRS specs, brainstorm outputs, PRD — bất kỳ định dạng markdown nào.

---

## Câu hỏi thường gặp

### Chọn level nào cho đúng?

| Tình huống | Level |
|---|---|
| Bài tập môn học, học thử | `fresh` |
| Đồ án tốt nghiệp, intern | `junior` |
| Startup, sản phẩm thật nhỏ-vừa | `mid` |
| Hệ thống lớn, production nghiêm túc | `senior` |

Nếu không chắc → chọn cao hơn 1 bậc so với ước tính. Tốn thêm chút token nhưng output chất lượng hơn.

### Có thể đổi level sau khi đã chạy không?

Được. Sửa trường `**level:**` trong `projects/{slug}/team/.project-config.md`, sau đó re-run các agent chưa chạy.

### Pipeline dừng với HARD STOP — làm gì?

1. Đọc `projects/{slug}/validation-errors/{agent}-attempt-3.md` để xem lỗi cụ thể
2. Re-run agent đó:
   ```
   /team-{role} --project {slug}
   ```

### QA/QC trả về REJECTED — làm gì?

1. Đọc `projects/{slug}/team/qa/sign-off.md` để xem danh sách vấn đề Critical/Major
2. Re-run agent bị lỗi để sửa
3. Re-run QA để lấy verdict mới:
   ```
   /team-qa --project ten-project
   ```

### Pipeline mất bao lâu?

| Agent | Thời gian ước tính |
|---|---|
| PM | 15–60 giây |
| BA, BE Dev, FE Dev, Tester | 30–180 giây mỗi agent |
| TechLead, QA/QC | 60–180 giây |
| **Toàn bộ pipeline** | **5–20 phút** (project trung bình) |

Với level `mid` và `senior`, bước Pre-Analysis thêm 30–60 giây/agent nhưng giảm đáng kể số lần phải chạy lại do lỗi thiết kế.

### Có thể chạy nhiều project cùng lúc không?

Mỗi project được cô lập trong thư mục `projects/{slug}/` riêng. Tuy nhiên một session Claude Code chỉ chạy được một pipeline tại một thời điểm. Mở nhiều session Claude Code để chạy song song.
