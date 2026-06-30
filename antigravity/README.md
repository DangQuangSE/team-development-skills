# Antigravity IDE Integration Guide

Chào mừng bạn đến với cấu hình tích hợp **Antigravity IDE** cho dự án `MySkills`. Thư mục này định nghĩa các quy tắc hoạt động, hệ thống Skill/Agent chuyển đổi từ `.claude` và cung cấp bộ chạy lệnh CLI cùng các Hook xác thực mã nguồn.

---

## 1. Các Quy Tắc Hoạt Động Của AI Agent (Rules)

Các quy tắc dưới đây được quy định trong cấu hình hệ thống [`.antigravityrules`](file:///d:/GitHub/MySkills/.antigravityrules) và bắt buộc AI Agent tuân thủ:

### A. Quy tắc Lập kế hoạch (Planning Gate - STOP & Ask)
- Đối với bất kỳ yêu cầu lập trình hoặc chỉnh sửa hệ thống phức tạp nào, AI **bắt buộc phải sử dụng Planning Mode**.
- AI phải tạo hoặc cập nhật tệp `implementation_plan.md` trong thư mục `brain/` của phiên chat và bật cờ `requestFeedback: true`.
- **QUAN TRỌNG:** Ngay sau khi đề xuất kế hoạch, AI **phải dừng ngay lập tức mọi tool calls** và chờ ý kiến phê duyệt của người dùng (bạn gõ "Approve", "Đồng ý", "Go ahead"...).
- Khi bạn đồng ý, AI sẽ tạo tệp `task.md` để theo dõi tiến độ và chuyển sang Phase viết code.

### B. Quy tắc Chạy Hook kiểm tra (Pre-Tool Validation)
- Trước khi thực thi bất kỳ thao tác ghi/sửa tệp nguồn nào, AI phải tự chạy công cụ kiểm duyệt:
  ```bash
  python antigravity/hooks/pre_tool_validator.py --tool <tên_tool> --file <đường_dẫn_file>
  ```
- Nếu kiểm tra thất bại, AI không được sửa file nguồn và phải tự khắc phục lỗi.

---

## 2. Danh Sách Đầy Đủ Các Lệnh Custom (All Commands)

Dưới đây là bảng tra cứu nhanh toàn bộ 10 lệnh custom được hỗ trợ. Các lệnh này được định cấu hình dưới dạng đặc tả tại [antigravity/commands/](file:///d:/GitHub/MySkills/antigravity/commands/) và được thực thi thông qua bộ chạy lệnh CLI [antigravity/run.py](file:///d:/GitHub/MySkills/antigravity/run.py) hoặc trong khung chat của Agent.

| Lệnh (CLI/Chat) | Loại | Công dụng & Mô tả chi tiết |
|---|---|---|
| **`coding-level`** | CLI | Cấu hình cấp độ giải thích code của AI Agent (từ -1 đến 5). Lưu vào `.ck.json`. |
| **`code-review`** | CLI | Tự động quét `git diff` để tìm các file thay đổi, rà soát credentials, format và chạy build/test dự án. |
| **`/at:brainstorm`** | Chat | Khảo sát cấu trúc mã nguồn hiện tại, đặt câu hỏi làm rõ và thảo luận thiết kế trước khi lập kế hoạch (không sửa code). |
| **`/at:plan`** | Chat | Tạo tệp kế hoạch triển khai chi tiết cho tính năng (`plan.md` + các tệp phase) với chế độ `--fast` hoặc `--hard`. |
| **`/at:cook`** | Chat | Thực thi viết code nguồn theo từng Phase đã được phê duyệt trong kế hoạch triển khai. |
| **`/at:fix`** | Chat | Tự động chẩn đoán và sửa lỗi compiler, build, lint hoặc unit test đang thất bại. |
| **`init`** | CLI | Wizard cấu hình nhanh cho dự án mới: chọn bundle, setup skill, thiết lập `.ck.json` và tạo `CLAUDE.md`. |
| **`learn`** | CLI | Phân tích session hiện tại và đúc kết các pattern xử lý lỗi/kỹ thuật hay thành tệp skill để tái sử dụng trong tương lai. |
| **`docs-fe`** | CLI | Tự động sinh tài liệu bàn giao Frontend (Markdown/HTML) cho các API thay đổi (routes, request/response DTOs, query, error codes). |
| **`show-off`** | CLI | Sinh bài thuyết trình HTML ấn tượng từ mã nguồn hiện có và tự động dùng Playwright chụp ảnh mockups đa khung hình (16:9, 9:16, 1:1). |

---

## 3. Chi Tiết Hướng Dẫn Sử Dụng Từng Lệnh

### 1. `coding-level`
Thiết lập độ sâu giải thích code của AI Agent.
*   **Menu tương tác:** `python antigravity/run.py coding-level`
*   **Đặt trực tiếp level:** `python antigravity/run.py coding-level [level_number]` (Ví dụ: `python antigravity/run.py coding-level 3` cho mức Senior).
*   **Reset:** `python antigravity/run.py coding-level reset`

### 2. `code-review`
Đánh giá chất lượng và kiểm thử cục bộ hoặc qua PR.
*   **Review cục bộ:** `python antigravity/run.py code-review` (Quét diff và tự động chạy test/build).
*   **Review PR trên GitHub:** `python antigravity/run.py code-review [pr_number_or_url]` (Cần cài đặt GitHub CLI `gh`).

### 3. `init`
Khởi tạo cấu hình nhanh cho dự án mới.
*   **Chạy Wizard:** `python antigravity/run.py init [target_path]`
*   **Hiển thị cấu hình hiện tại:** `python antigravity/run.py init --show`
*   **Reset cấu hình:** `python antigravity/run.py init --reset`

### 4. `docs-fe`
Sinh tài liệu bàn giao API cho Frontend.
*   **Mặc định (Markdown):** `python antigravity/run.py docs-fe`
*   **Xuất bản HTML tĩnh:** `python antigravity/run.py docs-fe --html`
*   *Lọc theo từ khoá/file:* `python antigravity/run.py docs-fe [feature_name | file_path | keyword]`

### 5. `show-off`
Tạo slide thuyết trình và hình ảnh mockup mạng xã hội.
*   **Interactive Mode:** `python antigravity/run.py show-off`
*   **Tự động hoàn toàn (Auto Mode):** `python antigravity/run.py show-off --auto <chủ_đề>`
*   **Chụp lại HTML có sẵn:** `python antigravity/run.py show-off --clone`

### 6. `learn`
Đúc kết bài học kinh nghiệm từ session.
*   **Thực thi:** `python antigravity/run.py learn`
*   *Lưu trữ:* File skill học được sẽ tự động lưu vào thư mục `antigravity/.agents/skills/learned/` để hệ thống tự nhận diện sau này.

### 7. `/at:brainstorm` (Chat)
Bắt đầu một cuộc thảo luận giải pháp kỹ thuật trước khi làm.
*   **Cú pháp:** `/at:brainstorm`

### 8. `/at:plan` (Chat)
Lập kế hoạch triển khai dự án.
*   **Cú pháp:** `/at:plan --fast` (lập kế hoạch nhanh) hoặc `/at:plan --hard` (nghiên cứu sâu + Red-team phản biện).

### 9. `/at:cook` (Chat)
Triển khai viết code theo kế hoạch.
*   **Cú pháp:** `/at:cook`

### 10. `/at:fix` (Chat)
Sửa lỗi nhanh compiler/test.
*   **Cú pháp:** `/at:fix`

---

## 4. Quản Lý Vòng Đời Tệp (Artifacts)

*   **`implementation_plan.md`**: Kế hoạch thiết kế được AI tạo ra ở bước đầu tiên, nằm trong thư mục `brain/` của phiên chat.
*   **`task.md`**: Danh sách đầu việc cần làm (chỉ được tạo sau khi kế hoạch được phê duyệt). **Pre-commit hook** sẽ dựa trên tệp này để biết dự án đang ở giai đoạn viết code.
*   **`walkthrough.md`**: Báo cáo tổng kết các thay đổi, kết quả kiểm thử khi kết thúc nhiệm vụ.
*   *Chi tiết hướng dẫn:* Đọc thêm tại [artifacts/README.md](file:///d:/GitHub/MySkills/antigravity/artifacts/README.md).
