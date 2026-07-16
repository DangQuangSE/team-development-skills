# srs-skills

[Tiếng Việt](./README.md) · [English](./README.en.md)

AI skill package tạo **Software Requirements Specification (IEEE 830-1998)** từ ý tưởng đến tài liệu hoàn chỉnh.

## Mục lục skill

| Skill | Vai trò |
|---|---|
| [srs-workflow](./skills/srs-workflow/) | Điều phối toàn bộ pipeline từ ý tưởng đến handoff |
| [srs-generator](./skills/srs-generator/) | Tạo nhanh SRS từ requirements có sẵn |
| [sr-brainstorm](./skills/sr-brainstorm/) | Khai thác yêu cầu qua 5 vòng |
| [sr-spec](./skills/sr-spec/) | Tổng hợp brainstorm thành spec |
| [sr-plan](./skills/sr-plan/) | Lập blueprint cho từng section SRS |
| [sr-generate](./skills/sr-generate/) | Sinh tài liệu IEEE 830 |
| [sr-validate](./skills/sr-validate/) | Validate và tự sửa lỗi cấu trúc |
| [sr-improve](./skills/sr-improve/) | Lập backlog cải tiến |
| [sr-save](./skills/sr-save/) | Lưu context để tiếp tục ở session sau |

---

## Cài đặt

Copy skills vào project của bạn:

```bash
cp -r srs-skills/skills/sr-* <your-project>/skills/
cp -r srs-skills/skills/srs-workflow/references <your-project>/skills/srs-workflow/
cp -r srs-skills/skills/srs-generator/references <your-project>/skills/srs-generator/
```

Hoặc mở thẳng thư mục `srs-skills/` trong Claude Code là dùng được ngay.

---

## Chọn workflow phù hợp

| Tình huống | Command |
|-----------|---------|
| Có ý tưởng / topic, chưa có requirements | Dùng pipeline `/sr:*` bên dưới |
| Đã có sẵn requirements text | `/cl:srs` — phân tích và tạo SRS luôn |

---

## Pipeline đầy đủ: `/sr:*`

Chạy từng bước theo thứ tự. Mỗi bước đọc output của bước trước.

### `/sr:brainstorm`

Nhập topic của bạn. AI sẽ hỏi 5 vòng câu hỏi có options để chọn:

- Vòng 1 — Actors & Users
- Vòng 2 — Core Features
- Vòng 3 — Scope (IN / OUT)
- Vòng 4 — Tech Constraints + NFR targets
- Vòng 5 — Business Rules & Edge Cases

AI **không được đoán** — bắt buộc hỏi lại nếu chưa rõ. Kết thúc khi không còn open item nào.

> Output: `projects/{slug}/brainstorm.md`

---

### `/sr:spec`

Đọc `brainstorm.md`, viết spec đầy đủ: actors, features, business rules, NFR baselines, assumptions, open items. Không giới hạn từ.

> Output: `projects/{slug}/spec.md`

---

### `/sr:plan`

Đọc `spec.md`, tạo **12 file plan riêng biệt** — mỗi file là blueprint chi tiết cho từng section của SRS (§1–§3, Appendix A/B). Bao gồm FR stubs và NFR targets.

Sau khi xong, `plan_validator.py` chạy để đếm FR/NFR (tránh đếm tay sai), rồi AI hỏi bạn review và approve trước khi generate SRS.

> Output: `projects/{slug}/plan/` (12 files)

---

### `/sr:generate`

Trước khi viết, chạy gate `plan_validator.py --dir projects/{slug}/plan/`:
- **BLOCKED** (thiếu file, FR numbering gap, thiếu "shall"...) → dừng, yêu cầu sửa ở `/sr:plan`
- **READY WITH WARNINGS** (còn `[NEEDS USER INPUT]` chưa track) → hỏi xác nhận tiếp tục
- **READY** → generate

Mục đích: bắt lỗi cấu trúc trên plan (rẻ) trước khi tốn token viết lại SRS 300+ trang.

Đọc plan files đã được approve, tạo SRS hoàn chỉnh — **không giới hạn từ**, có thể lên tới 300+ trang. Mỗi section là 1 file riêng.

Mỗi FR bắt buộc có:
- `The system shall ...` clause
- Given / When / Then acceptance criteria

Mỗi NFR bắt buộc có numeric Response Measure (không dùng adjective như "fast", "good").

> Output: `projects/{slug}/srs/` (11 files + master index)

---

### `/sr:validate`

Chạy `srs_validator.py` trên toàn bộ thư mục `srs/`. Kiểm tra theo IEEE 830:
- Đủ sections bắt buộc
- FR numbering không bị gap
- Mỗi FR có "shall" + GWT
- NFR có numeric target
- Không còn tag `[TBD]` / `[CONTEXT-GAP]` chưa resolve

ERRORs được fix ngay trong session. WARNs chuyển sang bước sau.

Verdict: **COMPLIANT** / **PARTIALLY COMPLIANT** / **NON-COMPLIANT**

---

### `/sr:improve`

Tạo báo cáo cải thiện: features bị defer, technical risks, NFR gaps, FR cần tách nhỏ hơn, warnings từ bước validate.

> Output: `projects/{slug}/improvement-report.md`

---

### `/sr:save`

Lưu toàn bộ context của project vào 6 file nhỏ để các session Claude sau load lại không cần đọc lại toàn bộ SRS.

> Output: `projects/{slug}/_context/` (vision, features, tech stack, glossary, quality standards, session notes)

---

## Quick SRS: `/cl:srs`

Dùng khi đã có requirements text sẵn. Paste text vào, AI sẽ:

1. Scan 7 loại ambiguity (vague quantifiers, undefined actors, contradictions…)
2. Hỏi clarification theo priority (P1 blockers trước)
3. Tạo SRS single-file chuẩn IEEE 830

---

## Scripts CLI (tùy chọn)

```bash
# Scan requirements text trước khi đưa vào AI
python scripts/gap_scanner.py requirements.txt

# Validate plan/ trước khi generate (Phase 4 gate)
python scripts/plan_validator.py --dir projects/{slug}/plan/
python scripts/plan_validator.py --dir projects/{slug}/plan/ --stats   # đếm FR/NFR/open items

# Validate SRS thủ công
python scripts/srs_validator.py --dir projects/{slug}/srs/
python scripts/srs_validator.py --dir projects/{slug}/srs/ --strict   # WARN = ERROR
python scripts/srs_validator.py --dir projects/{slug}/srs/ --format json
python scripts/srs_validator.py --dir projects/{slug}/srs/ --stats    # đếm FR/NFR/open items

# Khởi tạo context scaffold cho project mới
python scripts/init_project.py {slug}
```

---

## Tóm tắt commands

```
/sr:brainstorm  →  /sr:spec  →  /sr:plan  →  /sr:generate  →  /sr:validate  →  /sr:improve  →  /sr:save

hoặc: /cl:srs   (nếu đã có requirements text)
```
