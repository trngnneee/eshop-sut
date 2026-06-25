---
name: Domain and Boundary Testing Skill
description: Kỹ năng hỗ trợ thiết kế test case tự động sử dụng kỹ thuật Phân vùng tương đương (Equivalence Partitioning) và Phân tích giá trị biên (Boundary Value Analysis) cho các yêu cầu chức năng (FR) của hệ thống EShop.
---

# Kỹ năng Kiểm thử Miền & Giá trị Biên (Domain & Boundary Testing Skill)

Kỹ năng này hướng dẫn Agent cách phân tích một Yêu cầu Chức năng (Functional Requirement - FR), xác định các miền dữ liệu, phân vùng tương đương, các giá trị biên và tự động sinh ra các test case chuẩn hóa dưới định dạng Markdown.

---

## 1. Quy trình Áp dụng Kỹ thuật Kiểm thử

Khi nhận được yêu cầu thiết kế test case cho một FR cụ thể, Agent phải tuân thủ nghiêm ngặt quy trình 4 bước sau:

### Bước 1: Xác định các Tham số đầu vào & Trạng thái (Inputs & States)
* Xác định tất cả các trường dữ liệu người dùng nhập (ví dụ: Email, Mật khẩu, Số lượng, Mã giảm giá).
* Xác định các trạng thái hệ thống cần thiết (ví dụ: Người dùng đã đăng nhập/chưa đăng nhập, giỏ hàng trống/có sản phẩm, trạng thái đơn hàng hiện tại).

### Bước 2: Phân tích Phân vùng tương đương (Equivalence Partitioning - EP)
* Phân chia mỗi tham số đầu vào hoặc điều kiện thành các phân vùng tương đương:
  * **Phân vùng hợp lệ (Valid Partitions):** Các giá trị được hệ thống chấp nhận và xử lý bình thường.
  * **Phân vùng không hợp lệ (Invalid Partitions):** Các giá trị bị hệ thống từ chối hoặc báo lỗi.
* Lập bảng phân vùng tương đương để tiện theo dõi.

### Bước 3: Phân tích Giá trị biên (Boundary Value Analysis - BVA)
* Đối với các tham số có tính chất số học, độ dài chuỗi, hoặc giới hạn số lượng, xác định các giá trị biên:
  * **Biên dưới (Min):** Giá trị nhỏ nhất hợp lệ.
  * **Ngay dưới biên dưới (Min - 1):** Giá trị không hợp lệ.
  * **Ngay trên biên dưới (Min + 1):** Giá trị hợp lệ.
  * **Biên trên (Max):** Giá trị lớn nhất hợp lệ.
  * **Ngay dưới biên trên (Max - 1):** Giá trị hợp lệ.
  * **Ngay trên biên trên (Max + 1):** Giá trị không hợp lệ.
  * **Giá trị danh nghĩa (Nominal):** Một giá trị bình thường nằm giữa khoảng Min và Max.

### Bước 4: Thiết kế Test Cases & Ghi nhận
* Ghép các phân vùng và giá trị biên để tạo thành danh sách test case.
* Đảm bảo bao phủ tối thiểu:
  * Tất cả các phân vùng hợp lệ ít nhất một lần.
  * Mỗi phân vùng không hợp lệ được kiểm thử bằng một test case riêng biệt (để tránh lỗi này che lấp lỗi khác).
  * Tất cả các giá trị biên đã xác định.

---

## 2. Quy ước đặt mã và Thư mục Lưu trữ

* **Thư mục lưu trữ:** Lưu các file test case dưới định dạng Markdown (`.md`) vào thư mục `tests/test-cases/[tên-module]/`.
  * Ví dụ: `tests/test-cases/register/TC-REGISTER-001.md`
* **Quy ước mã Test Case:** `TC-[MODULE]-[NUMBER]`
  * Ví dụ: `TC-REGISTER-001`, `TC-REGISTER-002`, `TC-CART-001`.

---

## 3. Template File Test Case chuẩn Markdown

Mỗi file test case được tạo ra phải tuân thủ chính xác định dạng sau:

```markdown
# TC-[MODULE]-[NUMBER]: [Tiêu đề ngắn gọn mô tả mục đích test]

## Requirement ID
[Mã FR liên quan, ví dụ: FR-01]

## Module / Test type / Technique
[Tên Module] / [Loại kiểm thử, vd: Functional] / [Kỹ thuật áp dụng, vd: Equivalence Partitioning hoặc Boundary Value Analysis]

## Preconditions
- [Điều kiện tiền quyết 1]
- [Điều kiện tiền quyết 2]

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| [Tên tham số 1] | [Giá trị] |
| [Tên tham số 2] | [Giá trị] |

## Test steps
1. [Bước thực hiện 1]
2. [Bước thực hiện 2]
3. [Bước thực hiện 3]

## Expected result
- [Kết quả mong đợi 1]
- [Kết quả mong đợi 2]

## Status / Related bugs
Not Run / None
```

---

## 4. Hướng dẫn Tương tác cho Agent (Prompt Guidelines)

Khi kích hoạt kỹ năng này, Agent sẽ:
1. Hỏi người dùng cung cấp tài liệu đặc tả hoặc mô tả yêu cầu của chức năng cần test (nếu chưa có trong README.md).
2. Tự động liệt kê các phân vùng tương đương và các giá trị biên dưới dạng bảng để người dùng xác nhận.
3. Sau khi người dùng xác nhận, Agent sẽ tạo các file test case tương ứng vào đúng thư mục `tests/test-cases/[module]/`.
4. Cập nhật ma trận truy vết `tests/test-summary/traceability-matrix.md`.
5. **Đăng ký Bug khi phát hiện lỗi:** Khi phát hiện ra bất kỳ lỗi (bug) nào trong quá trình thực thi test case, Agent bắt buộc phải:
   * Tạo một **Bug Issue** tương ứng trên trang GitHub Issues của nhóm (đính kèm mô tả chi tiết, các bước tái hiện và ảnh chụp màn hình làm minh chứng).
   * Cập nhật mã Bug (ví dụ: `#18`) vào mục `Status / Related bugs` trong file test case bị Fail.
   * Đồng bộ liên kết Bug này vào báo cáo lượt chạy test `sprint-X-test-run.md` và ma trận truy vết `traceability-matrix.md`.

---

## 5. Hướng dẫn Sử dụng Công cụ Tự động hóa (Automation Script)

Để tối ưu hóa hiệu suất và đảm bảo tính nhất quán của các file test case, Agent nên ưu tiên sử dụng script Python tự động hóa được tích hợp sẵn.

### Các bước thực hiện:
1. **Xác định các tham số đầu vào** của form/chức năng cần test.
2. **Tạo một file cấu hình JSON** tạm thời mô tả các tham số đó (tham khảo cấu trúc của [register_config.json](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/.agents/skills/domain_and_boundary_testing/examples/register_config.json)). File JSON này chứa thông tin về `feature_name`, `module_name`, và mảng `inputs` (với các trường dữ liệu bao gồm `name`, `type`, `required`, giới hạn `min_length`, `max_length` cho chuỗi, hoặc `min_value`, `max_value` cho số).
3. **Chạy script tự động hóa** bằng lệnh:
   ```powershell
   python ".agents/skills/domain_and_boundary_testing/scripts/generate_test_cases.py" --config "[đường-dẫn-đến-file-json-cấu-hình]"
   ```
4. **Hậu xử lý (Post-processing):**
   * Script sẽ tự động tạo các test case biên cơ bản tại thư mục `tests/test-cases/[module_name]/`.
   * Agent cần đọc và bổ sung các test case kiểm thử logic phức tạp hơn (ví dụ: định dạng email hợp lệ, so sánh trường mật khẩu nhập lại có trùng khớp không, kiểm tra các trạng thái nghiệp vụ đặc thù) bằng tay vào các file test case tương ứng hoặc tạo mới.
   * Xóa file cấu hình JSON tạm sau khi hoàn tất để giữ thư mục sạch sẽ.

---

## 6. Quy trình & Template Báo cáo Lỗi (Bug Report)

Khi phát hiện ra lỗi (bug) trong quá trình kiểm thử, bên cạnh việc đăng ký GitHub Issue, Agent phải lập báo cáo lỗi chi tiết.

### Quy ước đặt mã và Thư mục Lưu trữ Lỗi (Bug Files)
* **Thư mục lưu trữ lỗi:** Lưu vào thư mục `tests/bug/[tên-feature]/` ở thư mục gốc của dự án.
  * Ví dụ: `tests/bug/login/`
* **Quy ước đặt tên file lỗi (viết liền không dấu ngoặc vuông):** `BUG-[Mã FR]-[Ký tự Pool]-[Số thứ tự].md`
  * Ví dụ: `BUG-FR02-A-01.md`
  * Trong đó: Pool được tra cứu trong tài liệu [Requirements.pdf](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/Requirements/Requirements.pdf) (ví dụ: `FR-02` thuộc `Pool A` nên ký tự pool là `A`).

### Template Chi Tiết Lỗi (Bug Report Template)

| Tên trường (Field) | Mô tả & Định dạng (Description & Format) |
| :--- | :--- |
| **No.** | Số thứ tự của lỗi phát hiện (ví dụ: `01`, `02`) |
| **BugID** | Mã định danh lỗi duy nhất (định dạng: `BUG-[Mã FR]-[Ký tự Pool]-[Số thứ tự]`, ví dụ: `BUG-FR02-A-01`) |
| **Status** | Trạng thái hiện tại của lỗi (ví dụ: `New`, `Open`, `In Progress`, `Resolved`, `Closed`) |
| **Requirement Name** | Tên yêu cầu nghiệp vụ bị lỗi (ví dụ: `FR-02 Đăng nhập & Khóa tài khoản`) |
| **Summary** | Tiêu đề tóm tắt ngắn gọn lỗi (ví dụ: `Mật khẩu hiển thị dạng clear text thay vì dấu chấm ẩn`) |
| **Steps to reproduce** | Các bước chi tiết để tái hiện lỗi:<br>1. Truy cập vào trang...<br>2. Điền thông tin...<br>3. Bấm vào nút... |
| **Severity** | Mức độ nghiêm trọng của lỗi (ví dụ: `Critical`, `Major`, `Minor`, `Cosmetic`) |
| **Frequency** | Tần suất lặp lại của lỗi (ví dụ: `Always`, `Intermittent`, `Rare`) |
| **Priority** | Độ ưu tiên xử lý của lỗi (ví dụ: `High`, `Medium`, `Low`) |
| **Attachment (Link to file)** | Ảnh chụp màn hình, video hoặc log lỗi ([Link to file](file:///path/to/attachment)) |
| **Date** | Ngày phát hiện lỗi (định dạng: `YYYY-MM-DD`, ví dụ: `2026-06-25`) |
| **Reporter** | Tên người thực hiện test và phát hiện lỗi (ví dụ: `AI Tester (Antigravity)`) |

