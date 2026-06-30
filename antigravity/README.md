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

## 2. Hướng Dẫn Sử Dụng Các Câu Lệnh (CLI Commands)

Chúng ta có một bộ chạy lệnh bằng Python tại [run.py](file:///d:/GitHub/MySkills/antigravity/run.py) thay thế cho các lệnh `/cl:` hay `/ck:` của Claude Code. 

Bạn có thể chạy các lệnh này trực tiếp từ **Terminal của IDE** ở thư mục gốc của dự án:

### A. Thiết lập Cấp độ Giải thích Code (`coding-level`)
Lệnh này cho phép bạn cấu hình mức độ sâu và chi tiết của AI khi giải thích hoặc hướng dẫn lập trình cho bạn (lưu vào tệp `.ck.json`).
*   **Hiển thị bảng cấp độ và chọn tương tác:**
    ```bash
    python antigravity/run.py coding-level
    ```
*   **Thiết lập trực tiếp một cấp độ cụ thể (từ -1 đến 5):**
    ```bash
    python antigravity/run.py coding-level 3
    ```
    *(Cấp độ 3 là Senior - tập trung vào trade-off, cấu trúc hệ thống, không giải thích dài dòng).*
*   **Reset cấu hình về mặc định:**
    ```bash
    python antigravity/run.py coding-level reset
    ```

### B. Chạy Đánh giá & Kiểm thử mã nguồn (`code-review`)
Lệnh này tự động quét các file bạn đã chỉnh sửa cục bộ (chưa commit) và thực hiện đánh giá.
*   **Chạy đánh giá:**
    ```bash
    python antigravity/run.py code-review
    ```
    *   Tự động chạy `git diff` tìm file thay đổi.
    *   Chạy kiểm thử bảo mật, rà soát credentials và format.
    *   Tự động tìm kiếm dự án Node/TS, .NET hoặc Python để chạy các lệnh build và test tự động.

### C. Xem hướng dẫn các lệnh Workflow (`brainstorm` & `plan`)
Đây là các lệnh hướng dẫn quy trình, bạn chạy qua Terminal để xem thông tin:
```bash
python antigravity/run.py brainstorm
python antigravity/run.py plan
```

---

## 3. Hệ Thống Skill & Agent chuyển đổi

Các Agent và Skill của Claude Code đã được thiết kế lại để tương thích hoàn toàn với các công cụ của Antigravity (như `view_file`, `write_to_file`, `replace_file_content`, `run_command`...):

*   **Các Agent cấu hình:** Nằm trong thư mục [antigravity/.agents/](file:///d:/GitHub/MySkills/antigravity/.agents) (ví dụ: `planner.md`, `code-reviewer.md`, `tester.md`).
*   **Các Skill chi tiết:** Nằm trong thư mục [antigravity/.agents/skills/](file:///d:/GitHub/MySkills/antigravity/.agents/skills/) (ví dụ: `srs-workflow`, `srs-generator`, `team`).
    *   *Cách gọi trực tiếp trong chat:* Nhắn tin chứa từ khóa kích hoạt, ví dụ: `/at:srs-flow` hoặc `/at:srs` để chạy quy trình tương ứng.

---

## 4. Quản Lý Vòng Đời Tệp (Artifacts)

*   **`implementation_plan.md`**: Kế hoạch thiết kế được AI tạo ra ở bước đầu tiên, nằm trong thư mục `brain/` của phiên chat.
*   **`task.md`**: Danh sách đầu việc cần làm (chỉ được tạo sau khi kế hoạch được phê duyệt). **Pre-commit hook** sẽ dựa trên tệp này để biết dự án đang ở giai đoạn viết code.
*   **`walkthrough.md`**: Báo cáo tổng kết các thay đổi, kết quả kiểm thử khi kết thúc nhiệm vụ.
*   *Chi tiết hướng dẫn:* Đọc thêm tại [artifacts/README.md](file:///d:/GitHub/MySkills/antigravity/artifacts/README.md).
