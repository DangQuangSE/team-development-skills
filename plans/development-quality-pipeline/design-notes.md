# Design Notes: Quality Pipeline (ck:quality / ck:test / ck:cook / ck:fix / code-review)

> Tổng hợp toàn bộ quyết định thiết kế (kể cả phần thảo luận ở agent khác) + phần đối chiếu với `spec.md` và các phase file trong thư mục này.

## 0. Quyết định đã chốt

- Model là **hybrid**, không hook-only: hook cưỡng chế rule deterministic; AI quality reviewer đánh giá rule semantic (SOLID/ownership/abstraction).
- Vi phạm quality (semantic) → **BLOCK và yêu cầu Cook sửa ngay**, không để QA quyết định sau.
- `ck:test` fail → **dừng lại, không tự gọi `ck:fix`**; người dùng chủ động chạy `/ck:fix --from-test ...` rồi `/ck:test --verify`.
- `ck:quality` là skill độc lập, không dùng tên `ck:review` (đã có `code-review`, tránh chồng khái niệm).
- `ck:quality` không có `--fix`; sửa luôn thuộc `ck:cook`/`ck:fix`.
- TDD có hai chế độ: mặc định là **test-after** (Tester chạy sau Cook); `--tdd` là **Tester orchestration hai lượt** (prepare RED trước Cook, verify GREEN sau Cook).
- Không ép mọi dự án phải có thư mục `common/`/`shared/` hay interface cho mọi service — abstraction phải có bằng chứng (2-3 consumer độc lập, cùng semantic, cùng owner, cùng lifecycle thay đổi).

## 1. Kiến trúc pipeline tổng thể

```
/ck:plan
    ↓
Engineering Preflight   (đọc convention, chọn quality module liên quan, tạo quality_profile cho phase)
    ↓
/ck:cook                (chỉ implement — không viết/chạy test, không tự đổi architecture contract)
    ↓
Quality Gate (hybrid)
    ├─ Hook: deterministic rules → ALLOW / WARN / BLOCK
    └─ AI reviewer (ck:quality): semantic rules → APPROVED / CHANGES_REQUIRED
    ├── CHANGES_REQUIRED → Cook/Fix sửa ngay → gate chạy lại
    └── APPROVED (receipt được phát)
          ↓
/ck:test                (sở hữu toàn bộ verification — không sửa production code)
    ├── FAILED → dừng, chờ /ck:fix --from-test → /ck:test --verify
    └── PASSED
          ↓
code-review / QA        (correctness, security, regression, readiness — không chấm lại maintainability)
```

Trạng thái phase sau Cook không được ghi `COMPLETED`; chỉ là `IMPLEMENTED_AWAITING_QUALITY_GATE` → sau khi quality approve mới là `IMPLEMENTED_AWAITING_TEST` → sau test pass mới coi là hoàn tất chờ review.

## 2. Phân chia trách nhiệm

| Skill | Trách nhiệm | Không được làm |
|---|---|---|
| `ck:cook` | Preflight, implement, compile/syntax check | Viết/chạy test, tự phát minh requirement, refactor ngoài scope, review toàn repo |
| `ck:quality` | Đánh giá kiến trúc, maintainability, engineering rules; trả finding có cấu trúc | Viết test, tự sửa production code, tự phê duyệt thay đổi của chính nó |
| `ck:test` | Viết/chạy test, xác minh behavior, sở hữu TDD | Sửa production code, làm yếu assertion, xóa test đang fail, tự đổi acceptance criteria |
| `ck:fix` | Sửa lỗi từ quality report hoặc test report | Mở rộng sửa ngoài scope của report |
| `code-review` | Final review: correctness, security, regression, readiness | Đánh giá lại maintainability đã có verdict từ `ck:quality` |

## 3. Engineering Quality Contract dùng chung

Một nguồn quy tắc duy nhất, được `ck:cook`, `ck:quality`, `ck:fix`, `code-review` cùng dùng — tránh mỗi agent hiểu "clean code" một kiểu và tránh copy "follow SOLID, DRY" vào mọi prompt.

**Nạp theo 3 tầng để tiết kiệm token** (không nạp toàn bộ contract vào mọi phase):
1. **Core — luôn nạp:** correctness, domain integrity, ownership/boundaries, error handling, security, readability, change safety.
2. **Context modules — nạp theo stack/loại thay đổi:** data consistency/transaction, concurrency/async, API/compatibility, observability, performance, dependency hygiene, documentation.
3. **Review triggers — chỉ dùng khi review, không cần nạp trước:** constants/messages, duplication, function size, nesting, coupling, dependency direction, abstraction discipline, testing discipline (thuộc `ck:test`).

Nội dung 17 nhóm rule (rút gọn, đầy đủ nằm trong lịch sử thiết kế):

1. **Correctness** — validate ở boundary, không tin input từ ngoài, phân biệt thiếu/sai/không quyền/không tồn tại/conflict/lỗi hệ thống, không swallow exception, không dùng exception làm control flow, xử lý rõ null/empty/timeout/partial failure, đúng data type cho tiền tệ/thời gian/timezone.
2. **Domain integrity** — one source of truth cho business rule; domain logic không nằm trong controller/UI/ORM model nếu kiến trúc không chủ đích; backend là authority; state transition được mô hình hóa rõ, không cho chuyển trạng thái bất hợp lệ.
3. **Module ownership & boundaries** — mỗi concern có owner rõ (controller/application/domain/repository/infrastructure/presenter); dependency đi một chiều đã khai báo; không import ngược domain→infrastructure; không truy cập DB thẳng từ controller nếu có boundary; không leak ORM entity/SDK object/infra exception qua public boundary.
4. **Abstraction discipline** — không tạo interface chỉ vì "SOLID"; interface hợp lý khi có nhiều implementation, là system boundary, cần thay dependency, cần test isolation thật; không tạo `BaseService`/`Helper`/`Manager` vô nghĩa; rule mặc định 1 lần = local, 2 lần = quan sát, 3 lần = cân nhắc extract; abstraction sai tốn kém hơn duplication nhỏ.
5. **Constants, messages, configuration** — centralize khi: lặp lại, có ý nghĩa domain, là error code/event name/route/permission/config key, cần localization, thay đổi theo environment, tham gia protocol; không constant hóa literal vô nghĩa (`ONE = 1`); tách domain constants / error codes / user-facing message / internal log / config / protocol constants; message hiển thị ≠ error code.
6. **Error handling** — error taxonomy thống nhất; preserve root cause khi wrap; mapping lỗi chỉ tại boundary phù hợp; không trả stack trace cho client; không log trùng lỗi nhiều layer; phân biệt retryable/non-retryable (không retry validation/authorization/conflict); retry có limit/backoff/jitter; external call có timeout; cleanup chạy trong finally/context manager.
7. **Data consistency & transaction** — transaction boundary theo business operation, không theo từng repository call; tránh giữ transaction khi gọi external API; race condition xử lý bằng DB constraint/locking/optimistic concurrency, không chỉ `if` trong code; operation nhận lại request phải idempotent; không thay application validation cho unique/check/FK constraint; migration cân nhắc backward-compat/rollback; queue/event: giả định delivery nhiều lần, consumer idempotent, có dead-letter handling.
8. **Concurrency & async** — không shared mutable state nếu không cần; không block thread trong async flow; không unbounded parallelism; có cancellation propagation và timeout cho I/O; xác định ordering requirement; không giả định request/event chỉ chạy một lần; cache update/read-modify-write xét race condition; background task quan trọng không fire-and-forget thiếu error handling.
9. **Security by default** — không hardcode secret/token; authorization ở server cho mọi protected operation (authN ≠ authZ); parameterized query; encode output theo context; không log password/token/PII; least privilege; dependency mới phải có lý do; giới hạn file upload (type/size/filename/path); xét SSRF/open redirect cho URL fetch/webhook/redirect; error response không lộ internal structure; randomness cho security phải cryptographically secure.
10. **API & compatibility** — public contract ổn định, có versioning; không đổi ý nghĩa field hiện hữu âm thầm; phân biệt required/optional/nullable/omitted; error response schema nhất quán; pagination có giới hạn; mutation cân nhắc idempotency; không expose DB schema thành API contract; breaking change khai báo rõ trong plan.
11. **Observability** — structured logging, có correlation/trace ID, đúng log level; không dùng log thay metrics; metrics đo success/failure/latency/saturation; external call có duration/status; background job có trạng thái hoàn thành/thất bại; audit log tách khỏi diagnostic log khi cần.
12. **Performance có bằng chứng** — không tối ưu theo cảm giác; tránh N+1; paginate/stream thay vì load toàn bộ dataset; batch thay vì gọi external service trong loop; cache chỉ thêm khi xác định được key/TTL/invalidation/consistency/failure behavior; không hy sinh correctness/readability cho micro-optimization không đo được.
13. **Testing discipline** (chi tiết thuộc `ck:test`, xem mục 7) — không chỉ happy path; cân nhắc boundary/invalid input/authorization failure/dependency failure/timeout/retry/concurrency/state transition bất hợp lệ/regression; test behavior không khóa implementation detail; deterministic, không sleep tùy tiện; mock system boundary chứ không mock mọi class.
14. **Readability & maintainability** — tên thể hiện intent; function một việc một abstraction level; tránh boolean parameter khó hiểu; early return giảm nesting; comment giải thích "vì sao"; xóa dead code, không comment-out để dành; Boy Scout Rule không mở rộng thành refactor toàn repo; số dòng/nesting chỉ là review trigger, không phải failure tuyệt đối.
15. **Change safety** — backward-compatible khi rollout nhiều instance; migration/deploy chịu được thứ tự triển khai; feature lớn cân nhắc feature flag; có rollback/mitigation; không trộn feature + refactor lớn + reformat hàng loạt; không sửa file ngoài scope không lý do; config mới có default an toàn + tài liệu.
16. **Dependency hygiene** — không thêm package cho việc nhỏ có thể viết rõ ràng; kiểm tra maintenance/license/security/kích thước; business logic không phụ thuộc thẳng API đặc thù vendor; pin version theo chiến lược dự án; wrapper phải bảo vệ boundary thật, không vô nghĩa; xóa dependency không dùng.
17. **Documentation & decision trace** — public API/non-obvious contract có doc; quyết định kiến trúc quan trọng ghi lại context/lựa chọn/trade-off/hậu quả; không document điều đọc thẳng từ code được; giới hạn chủ ý ghi thành non-goal.

**Nguyên tắc trung tâm:** mỗi quyết định code phải làm rõ **ownership, dependency, failure behavior, và lý do thay đổi**; nếu một trong bốn thứ này mơ hồ, thiết kế chưa hoàn tất.

## 4. Engineering Preflight (trước khi Cook viết code)

Preflight đọc convention thật của repo (naming, constants/messages/errors, cấu trúc module, shared utilities đã có, DI pattern, test convention) và tạo context ngắn riêng cho phase — không phải tuôn cả contract vào prompt:

```yaml
quality_profile:
  repository_conventions:
    constants: src/shared/constants
    errors: src/domain/errors
    dependency_injection: constructor
  boundaries:
    domain_cannot_import:
      - infrastructure
      - controllers
  applicable_rules:
    - no_new_magic_domain_values
    - no_raw_user_facing_messages
    - no_duplicate_business_rules
    - no_direct_infrastructure_construction
  allowed_exceptions: []
```

Nếu bỏ qua bước này, AI thường tạo kiến trúc "hợp lý nói chung" nhưng không khớp với chính codebase.

## 5. Quality Gate: hook (deterministic) vs AI reviewer (semantic)

| Loại vi phạm | Cơ chế | Kết quả |
|---|---|---|
| Secret, forbidden import/path, invalid config key, error code ngoài registry, lint/typecheck/syntax | Hook | `ALLOW` / `WARN` / `BLOCK` |
| Format, naming nhẹ | Hook | `WARN` hoặc auto-fix |
| SOLID, cohesion, ownership, abstraction, duplication | AI quality reviewer (`ck:quality --gate`) | `APPROVED` / `CHANGES_REQUIRED` |
| Functional behavior, regression, edge case | `ck:test` | `PASSED` / `FAILED` |
| Release readiness | `code-review` / QA | `APPROVED` / `BLOCKED` |

Hook chỉ nên `BLOCK` cho rule có độ tin cậy cao — false positive ở hook khiến AI tìm cách lách rule hoặc viết code méo mó. Hook **không** cố đóng vai senior architect (không chấm SOLID/ownership); AI reviewer **không** phí token kiểm tra thứ máy đã xác định chắc chắn được.

## 6. `ck:quality` — skill độc lập

Đặt tên `ck:quality` chứ không phải `ck:review` để tránh chồng khái niệm với `code-review` đã có. Dùng được cả trong Cook pipeline lẫn gọi độc lập để audit dự án bất kỳ.

### Gate mode

```
/ck:quality --gate plans/my-feature/phases/phase-02.md
```

Chỉ kiểm tra code phase hiện tại tạo/sửa, đọc quality contract của phase, so convention hiện hữu, phân biệt lỗi mới vs debt cũ, sinh receipt cho hook. Nếu Cook tự sửa ngay khi có finding, vẫn phải chạy lại `--verify` — quyền đánh giá và quyền sửa luôn tách biệt.

### Audit mode (dự án bất kỳ)

```
/ck:quality --audit .
/ck:quality --audit src/payments
/ck:quality --diff main
/ck:quality --changed
```

Mặc định `--audit` chỉ báo cáo trong session, không tạo file, không sửa code; chỉ ghi file khi có `--save <path>` tường minh. Riêng `--gate` bắt buộc ghi report + receipt vì hook cần xác minh trạng thái. Report của planned work nằm ở `plans/{slug}/quality/`.

### Severity

`BLOCKER` / `HIGH` → block. `MEDIUM` → block nếu là vi phạm contract của phase hiện tại (current-change). `LOW` → không block. `NOTED` → debt cũ hoặc suggestion ngoài scope.

Finding phải có rule, bằng chứng, vị trí, lý do nguy hiểm, hành động bắt buộc, có phải lỗi mới không, ai sửa, mức `applicable`/`confidence` (tránh rule bị ép cứng gây false positive):

```json
{
  "id": "QUAL-007",
  "severity": "HIGH",
  "rule": "DOMAIN_RULE_SINGLE_SOURCE",
  "status": "OPEN",
  "introduced_by_current_change": true,
  "applicable": true,
  "confidence": "high",
  "location": "src/orders/create-order.ts:48",
  "evidence": "The eligibility rule duplicates OrderPolicy.isEligible",
  "required_action": "Reuse the existing domain policy",
  "owner": "cook"
}
```

### Receipt (đối tượng hook xác minh)

```json
{
  "target": "phase-02",
  "verdict": "APPROVED",
  "policy_version": "1.0.0",
  "source_fingerprint": "sha256:...",
  "reviewed_at": "2026-07-10T10:30:00Z",
  "open_blocking_findings": 0
}
```

Hook kiểm tra: receipt tồn tại, verdict `APPROVED`, policy version đúng, fingerprint khớp code hiện tại (hash nội dung report + nội dung chính xác từng file đã review, không chỉ tên/mtime), không có file bị đổi sau review, không còn blocking finding mở, và mọi path phải nằm trong repo (reject path traversal). Hook fail-closed ở điểm chuyển trạng thái "completed" nhưng vẫn cho sửa file bình thường để remediate. Code đổi sau khi pass → receipt hết hiệu lực, phải `--verify` lại.

`ck:quality` không có `--fix` — tránh reviewer tự sửa rồi tự phê duyệt thay đổi của chính nó.

## 7. `ck:test` — skill độc lập cho verification

### Giao diện lệnh

```
/ck:test <plan-or-phase>              # mặc định: phân tích changed scope, viết test thiếu, chạy unit+integration liên quan
/ck:test --unit <target>
/ck:test --integration <target>
/ck:test --e2e <target>
/ck:test --all <target>               # tất cả test phù hợp scope, không nhất thiết cả repo
/ck:test --verify <target>            # chạy lại test đã fail + regression liên quan, không thiết kế lại suite
/ck:test --all-phases plans/my-feature/plan.md
```

### TDD — hai chế độ

- **Mặc định (test-after):** `/ck:cook` → `/ck:test`. Đơn giản, Cook tập trung implement.
- **`--tdd` (Tester orchestration hai lượt):**
  ```
  /ck:test --tdd --prepare phase-02.md   # viết test trước, xác nhận RED vì chưa có code, lưu RED_READY
  /ck:cook phase-02.md                    # implement tới khi RED→GREEN, không đổi/làm yếu test, qua hard quality gate
  /ck:test --tdd --verify phase-02.md     # chạy lại, xác nhận pass + regression, phát hiện test bị làm yếu/xóa/sửa để né lỗi
  ```

### Trạng thái hai cấp

Master plan chỉ giữ tóm tắt:
```yaml
phase_02:
  implementation: quality_approved
  testing: failed
```
Phase artifact giữ chi tiết (`implementation.quality_gate.verdict`, `testing.status`, `testing.report`, `testing.failed_cases`) — AI chỉ cần mở report của phase đang làm, không đọc lại lịch sử toàn feature.

### Report thất bại (máy đọc được)

```json
{
  "phase": "phase-02",
  "verdict": "FAILED",
  "summary": { "passed": 12, "failed": 2, "skipped": 0 },
  "failures": [
    {
      "id": "TEST-004",
      "severity": "HIGH",
      "type": "BEHAVIOR",
      "expected": "Duplicate request returns the existing result",
      "actual": "A duplicate record was created",
      "likely_owner": "production_code",
      "related_files": ["src/orders/create-order.ts"]
    }
  ]
}
```

Sau đó người dùng chủ động chạy `/ck:fix --from-test plans/my-feature/tests/phase-02-test.json` rồi `/ck:test --verify ...` — `ck:test` **không tự động gọi `ck:fix`**.

### Quyền hạn

Được: tạo/sửa test code, fixtures, mocks, test helpers; chạy test; cập nhật report/status; đề xuất nguyên nhân lỗi.
Không được: sửa production code; làm yếu assertion để pass; xóa test đang fail; đổi acceptance criteria; mark pass khi chưa chạy; mở rộng test ngoài scope không lý do.

### Gate trước Tester

Nếu quality gate chưa `APPROVED`, `/ck:test` phải trả:
```
BLOCKED: phase implementation has not passed the Code Quality Gate.
Run or resume /ck:cook for the current phase.
```

## 8. Ownership cho common/shared

Không ép mọi dự án có một thư mục `common/`/`shared/` chung — dễ biến thành "sọt rác". Ưu tiên đặt theo domain:

```
orders/      order-errors, order-messages, order-policy
identity/    permissions, authentication-errors
platform/    logging, clock, identifiers
```

Chỉ chuyển sang shared khi: có ≥2-3 consumer độc lập, semantic thực sự giống nhau, có owner rõ ràng, lifecycle thay đổi giống nhau.

## 9. Quan hệ với `code-review`

Trích một quality engine dùng chung, không duy trì hai bộ rule song song:

```
engineering-quality/
├── core-contract
├── severity-rules
├── stack-adapters
├── report-schema
└── evaluation-checklist
```

`ck:quality` dùng toàn bộ engine; `code-review` đọc kết quả từ `ck:quality`, không chấm lại maintainability (chỉ correctness/security/regression/readiness); `ck:cook` đọc contract ở preflight; hook đọc receipt; `ck:test` chỉ kiểm tra functional behavior.

## 10. Vận hành khác

- **Fast mode:** giảm ceremony, không được bỏ qua quality gate. `ck:cook --no-test` bị deprecate vì Cook không còn sở hữu test.
- **Tương thích plan cũ (v1):** thiếu field quality/test nhận runtime default, không migrate phá hủy.
- **Đồng bộ đa nền tảng:** `ck:quality`/`ck:test` mirror nguyên vẹn sang `.claude/`, `.codex/`, `.agents/`; chỉ hook adapter khác nhau theo format từng client.
- **Adapter theo stack:** core rule trung lập ngôn ngữ, nạp thêm adapter TypeScript/Node, Python, .NET, Java, Frontend, Database, Event-driven theo phase — không nhồi mọi rule của mọi ngôn ngữ vào một prompt.

## 11. Còn cần chốt

- Output style: enterprise nghiêm ngặt hay cân bằng "abstraction chỉ khi có bằng chứng" (khuyến nghị: cân bằng, đã phản ánh ở mục 3.4 và mục 8).
- Stack ưu tiên tối ưu trước: .NET, TypeScript/Node, Python, hay hoàn toàn trung lập — ảnh hưởng đến việc viết adapter nào trước ở Phase 1.
