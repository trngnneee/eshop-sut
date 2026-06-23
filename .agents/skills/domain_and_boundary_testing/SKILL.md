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

