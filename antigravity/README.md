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

## 2. Hướng Dẫn Sử Dụng Các Câu Lệnh CLI (Terminal Commands)

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

---

## 3. Các Lệnh Chat Workflows (Slash Commands / Skills)

Đây là các lệnh và quy trình bạn có thể **gõ trực tiếp trong ô chat** để điều khiển Antigravity Agent. Agent sẽ nhận diện từ khóa và tự động nạp các Skill/Agent tương ứng trong [antigravity/.agents/](file:///d:/GitHub/MySkills/antigravity/.agents).

### A. Nhóm lệnh đặc tả yêu cầu (SRS Skills)
*   **`/at:srs-flow` (Quy trình SRS đầy đủ - Khuyên dùng)**
    *   *Công dụng:* Khảo sát yêu cầu sâu end-to-end từ một ý tưởng thô và sinh ra tài liệu đặc tả chuẩn IEEE 830-1998 hoàn chỉnh.
    *   *Quy trình:* Brainstorm (phỏng vấn nhiều vòng) $\rightarrow$ Viết Spec nháp $\rightarrow$ Phân chia Plan $\rightarrow$ Sinh tài liệu SRS $\rightarrow$ Auto-Validate bằng code $\rightarrow$ Viết báo cáo cải tiến $\rightarrow$ Lưu ngữ cảnh dự án.
*   **`/at:srs` (Sinh nhanh tài liệu SRS)**
    *   *Công dụng:* Sinh nhanh tài liệu đặc tả IEEE 830-1998 từ một danh sách các yêu cầu có sẵn (không qua các vòng phỏng vấn brainstorm).

### B. Nhóm lệnh mô phỏng đội dự án (Virtual Team Skills)
*   **`/team` (Chạy toàn bộ đội dự án)**
    *   *Công dụng:* Mô phỏng đội phát triển phần mềm gồm 7 vai trò AI chạy tự động từ đầu đến cuối để xây dựng dự án.
    *   *Cú pháp:* `/team "yêu cầu tính năng" --project {tên_dự_án} --level {fresh|junior|mid|senior}`
*   **Các lệnh gọi vai trò đơn lẻ:**
    *   `/team-ba`: Khảo sát, phân tích nghiệp vụ và viết User Stories.
    *   `/team-techlead`: Thiết kế kiến trúc, Tech-stack, sơ đồ ERD/Sequence và viết ADR (Architecture Decision Record).
    *   `/team-pm`: Lập kế hoạch Sprint, chia nhỏ Task và ước lượng Story Points.
    *   `/team-dev` (hoặc `/team-be`, `/team-fe`): Lập trình mã nguồn Frontend/Backend và viết PR (Pull Request) description.
    *   `/team-test`: Lập kế hoạch kiểm thử, sinh test case (Unit, Integration, E2E) và mẫu báo cáo bug.
    *   `/team-qa`: Đánh giá mức độ tuân thủ quy trình, bảo mật và phê duyệt phát hành dự án (Sign-off).

### C. Nhóm lệnh quy trình phát triển cốt lõi (Core Commands)
*   **`/at:brainstorm` (Khảo sát và thảo luận giải pháp)**
    *   *Công dụng:* Khảo sát cấu trúc mã nguồn hiện tại, đặt câu hỏi làm rõ thiết kế trước khi bắt đầu code. Không viết code ở bước này.
*   **`/at:plan` (Lập kế hoạch triển khai)**
    *   *Công dụng:* Sinh tài liệu kế hoạch triển khai chi tiết cho một tính năng.
    *   *Các chế độ:* `--fast` (lập plan nhanh trực tiếp), `--hard` (plan nghiên cứu kỹ + red-team kiểm định).
*   **`/at:cook` (Bắt đầu viết code)**
    *   *Công dụng:* Từng bước đọc kế hoạch và tiến hành sửa đổi, bổ sung code nguồn cho dự án theo đúng thiết kế.
*   **`/at:fix` (Sửa lỗi tự động)**
    *   *Công dụng:* Tự động quét và phát hiện các lỗi build, lint, compiler hoặc test đang thất bại và đề xuất sửa chữa.

---

## 4. Quản Lý Vòng Đời Tệp (Artifacts)

*   **`implementation_plan.md`**: Kế hoạch thiết kế được AI tạo ra ở bước đầu tiên, nằm trong thư mục `brain/` của phiên chat.
*   **`task.md`**: Danh sách đầu việc cần làm (chỉ được tạo sau khi kế hoạch được phê duyệt). **Pre-commit hook** sẽ dựa trên tệp này để biết dự án đang ở giai đoạn viết code.
*   **`walkthrough.md`**: Báo cáo tổng kết các thay đổi, kết quả kiểm thử khi kết thúc nhiệm vụ.
*   *Chi tiết hướng dẫn:* Đọc thêm tại [artifacts/README.md](file:///d:/GitHub/MySkills/antigravity/artifacts/README.md).
