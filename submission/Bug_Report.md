# Báo Cáo Lỗi Phần Mềm (Bug Report) — HW04

**Khoa Công nghệ Thông tin – Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM**  
**Môn học: CS423 / CSC13003 – Kiểm thử phần mềm (AI-augmented · 2026)**

---

## Thông Tin Sinh Viên

| Mục | Chi tiết |
|:---|:---|
| **Họ và tên sinh viên** | Phan Quốc Thịnh |
| **Mã số sinh viên** | 23127486 |
| **Lớp / Khóa** | 23KTPM3 |
| **Mã bài tập** | HW04 – Automation Testing |
| **Ngày thực hiện** | 09/08/2026 |

---

## Tổng Hợp Khiếm Khuyết Phát Hiện Được

| Tổng số Bug phát hiện | Danh sách GitHub Issues |
|:---:|:---:|
| **7 lỗi (Bugs)** | [https://github.com/trngnneee/eshop-sut/issues](https://github.com/trngnneee/eshop-sut/issues) |

---

## Danh Sách Chi Tiết Các Lỗi (Bug List)

---

### Bug #1: Regex Kiểm Tra Mật Khẩu Đăng Ký Bắt Buộc Khoảng Trắng và Cấm Ký Tự Đặc Biệt

| Mục | Nội dung chi tiết |
|:---|:---|
| **Mã lỗi (Bug ID)** | **BUG-001** |
| **Tiêu đề** | Password regex trong `Register.jsx` yêu cầu khoảng trắng và từ chối ký tự đặc biệt |
| **Tính năng liên quan** | `FR-01`: Đăng ký tài khoản (Account Registration) |
| **Mức độ nghiêm trọng (Severity)** | **Major (Nghiêm trọng)** |
| **Độ ưu tiên xử lý (Priority)** | **High (Cao)** |
| **Trạng thái** | Open |
| **Phát hiện bởi test case** | `TC12 - Đăng ký với mật khẩu mạnh có ký tự đặc biệt theo chuẩn` (FAILED) |
| **GitHub Issue** | [Issue #1 - FR-01 Password Regex Defect](https://github.com/trngnneee/eshop-sut/issues/1) |

**Mô tả lỗi:**
Tại file `frontend-web/src/pages/Register.jsx` dòng 16, biểu thức chính quy (regular expression) kiểm tra độ mạnh mật khẩu được định nghĩa:
```javascript
const flawedStrongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\s)[A-Za-z\d\s]{8,}$/;
```
Biểu thức này sử dụng `(?=.*\s)` (bắt buộc phải có ít nhất 1 khoảng trắng) thay vì `(?=.*[@$!%*?&])`, đồng thời tập ký tự cho phép `[A-Za-z\d\s]` lại cấm hoàn toàn các ký tự đặc biệt thông dụng (`!`, `@`, `#`, `$`, `%`, v.v.). Khi người dùng nhập một mật khẩu mạnh chuẩn an toàn (ví dụ: `StrongPass123!@`), hệ thống từ chối và báo lỗi sai: *"Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT."*

---

### Bug #2: Trường Nhập Email Dùng `type="text"` Không Có Validation Định Dạng RFC

| Mục | Nội dung chi tiết |
|:---|:---|
| **Mã lỗi (Bug ID)** | **BUG-002** |
| **Tiêu đề** | Input Email trong form đăng ký dùng type='text' thay vì type='email' |
| **Tính năng liên quan** | `FR-01`: Đăng ký tài khoản (Account Registration) |
| **Mức độ nghiêm trọng (Severity)** | **Medium (Trung bình)** |
| **Độ ưu tiên xử lý (Priority)** | **Medium (Trung bình)** |
| **Trạng thái** | Open |
| **Phát hiện bởi test case** | `TC05 - Đăng ký với email sai cú pháp RFC thiếu domain/kí tự @` (FAILED) |
| **GitHub Issue** | [Issue #2 - FR-01 Email Input Type Defect](https://github.com/trngnneee/eshop-sut/issues/2) |

**Mô tả lỗi:**
Tại `frontend-web/src/pages/Register.jsx` dòng 48, trường nhập email được khai báo `<input type="text" ... />` thay vì `<input type="email" ... />`. Do đó, trình duyệt không kích hoạt tính năng kiểm tra tính hợp lệ email của HTML5, cho phép submit chuỗi không đúng định dạng (`invalidemailformat`) lên server.

---

### Bug #3: Bảng `users` Thiếu Ràng Buộc UNIQUE Trên Cột Email

| Mục | Nội dung chi tiết |
|:---|:---|
| **Mã lỗi (Bug ID)** | **BUG-003** |
| **Tiêu đề** | Database SQLite cho phép đăng ký nhiều tài khoản có cùng địa chỉ email |
| **Tính năng liên quan** | `FR-01`: Đăng ký tài khoản & Cơ sở dữ liệu |
| **Mức độ nghiêm trọng (Severity)** | **Major (Nghiêm trọng)** |
| **Độ ưu tiên xử lý (Priority)** | **High (Cao)** |
| **Trạng thái** | Open |
| **Phát hiện bởi test case** | `TC11 - Đăng ký với email đã tồn tại trong database` (FAILED) |
| **GitHub Issue** | [Issue #3 - FR-01 Duplicate Email Constraint Defect](https://github.com/trngnneee/eshop-sut/issues/3) |

**Mô tả lỗi:**
Trong `backend/database.js` và `backend/server.js`, bảng `users` không có ràng buộc `UNIQUE` trên cột `email`. Endpoint `POST /api/register` cũng không kiểm tra email trùng lặp trước khi thực hiện `INSERT`, cho phép tạo nhiều tài khoản cùng email `admin@eshop.com`.

---

### Bug #4: Kiểm Tra Giá Trị Đơn Hàng Tối Thiểu Dùng Bất Đẳng Thức Ngặt (`>`)

| Mục | Nội dung chi tiết |
|:---|:---|
| **Mã lỗi (Bug ID)** | **BUG-004** |
| **Tiêu đề** | Logic áp dụng coupon yêu cầu total_amount > min_order_amount thay vì >= |
| **Tính năng liên quan** | `FR-09`: Mã giảm giá (Discount Coupons) |
| **Mức độ nghiêm trọng (Severity)** | **Major (Nghiêm trọng - Lỗi giá trị biên)** |
| **Độ ưu tiên xử lý (Priority)** | **High (Cao)** |
| **Trạng thái** | Open |
| **Phát hiện bởi test case** | `TC08 - Áp dụng mã khi tổng tiền đơn hàng bằng đúng giá trị tối thiểu` (FAILED) |
| **GitHub Issue** | [Issue #4 - FR-09 Boundary Condition Defect](https://github.com/trngnneee/eshop-sut/issues/4) |

**Mô tả lỗi:**
Tại `backend/server.js` dòng 379, câu lệnh kiểm tra điều kiện áp dụng mã là `if (total_amount > coupon.min_order_amount)`. Khi đơn hàng có tổng tiền đúng bằng mức tối thiểu (ví dụ: 300.000 ₫ == 300.000 ₫), hệ thống từ chối áp dụng và báo lỗi sai: *"Đơn hàng chưa đủ giá trị tối thiểu..."*.

---

### Bug #5: Công Thức Tính Giảm Giá Phần Trăm Bị Đảo Ngược Thành Số Tiền Âm

| Mục | Nội dung chi tiết |
|:---|:---|
| **Mã lỗi (Bug ID)** | **BUG-005** |
| **Tiêu đề** | Công thức Math.floor(total_amount * (1 - coupon.discount_value)) gây sai lệch số tiền giảm |
| **Tính năng liên quan** | `FR-09`: Mã giảm giá (Discount Coupons) |
| **Mức độ nghiêm trọng (Severity)** | **Critical (Chí mạng)** |
| **Độ ưu tiên xử lý (Priority)** | **High (Cao)** |
| **Trạng thái** | Open |
| **Phát hiện bởi test case** | `TC01 - Áp dụng mã giảm giá phần trăm SAVE10` (Code Inspection) |
| **GitHub Issue** | [Issue #5 - FR-09 Percentage Calculation Formula Defect](https://github.com/trngnneee/eshop-sut/issues/5) |

**Mô tả lỗi:**
Tại `backend/server.js` dòng 399-401, công thức `discount_amount = Math.floor(total_amount * (1 - coupon.discount_value))` khi `discount_value = 10` sẽ tính ra `-9 * total_amount`, làm tăng tổng tiền phải thanh toán thay vì giảm giá.

---

### Bug #6: Tiêu Đề Trang Đăng Nhập Hiển Thị Nhầm Thành "Đăng Ký"

| Mục | Nội dung chi tiết |
|:---|:---|
| **Mã lỗi (Bug ID)** | **BUG-006** |
| **Tiêu đề** | Header trang Login.jsx hiển thị nhãn 'Đăng Ký' thay vì 'Đăng Nhập' |
| **Tính năng liên quan** | Giao diện người dùng / Xác thực |
| **Mức độ nghiêm trọng (Severity)** | **Minor (Nhỏ - UI defect)** |
| **Độ ưu tiên xử lý (Priority)** | **Low (Thấp)** |
| **Trạng thái** | Open |
| **Phát hiện bởi test case** | `TC01 - Redirect to login after registration` (UI Inspection) |
| **GitHub Issue** | [Issue #6 - Login Heading Mislabel Defect](https://github.com/trngnneee/eshop-sut/issues/6) |

**Mô tả lỗi:**
Tại `frontend-web/src/pages/Login.jsx` dòng 24, tiêu đề trang hiển thị `<h2 ...>Đăng Ký</h2>` thay vì `Đăng Nhập`.

---

### Bug #7: Thiếu Transaction Rollback Khi Import CSV Có Dòng Lỗi (Vi Phạm Tính Nguyên Tố Atomic)

| Mục | Nội dung chi tiết |
|:---|:---|
| **Mã lỗi (Bug ID)** | **BUG-007** |
| **Tiêu đề** | Endpoint import-products thực hiện partial import thay vì Rollback toàn bộ khi file CSV có lỗi |
| **Tính năng liên quan** | `FR-16`: Import sản phẩm từ CSV (Admin) & CSDL |
| **Mức độ nghiêm trọng (Severity)** | **Major (Nghiêm trọng - Tính toàn vẹn CSDL)** |
| **Độ ưu tiên xử lý (Priority)** | **High (Cao)** |
| **Trạng thái** | Open |
| **Phát hiện bởi test case** | `TC06 - Import file CSV chứa dòng dữ liệu lỗi (SRS: Phải rollback toàn bộ transaction)` (FAILED) |
| **GitHub Issue** | [Issue #7 - FR-16 Transaction Rollback Defect](https://github.com/trngnneee/eshop-sut/issues/7) |

**Mô tả lỗi:**
Tại `backend/server.js` dòng 209-240, endpoint `POST /api/admin/import-products` duyệt từng dòng trong danh sách và chèn trực tiếp vào SQLite mà không sử dụng Database Transaction (`BEGIN TRANSACTION ... COMMIT / ROLLBACK`). Khi gặp file CSV có 1 dòng bị lỗi và 2 dòng hợp lệ (`fr16_sample_mixed.csv`), hệ thống vẫn insert 2 sản phẩm vào CSDL và trả về `Import hoàn tất: 2/3 sản phẩm`.  
Theo đúng **Đặc tả SRS và Tiêu chuẩn Toàn vẹn Dữ liệu (ACID / Atomicity)**: Thao tác import theo lô (batch import) phải tuân theo nguyên tắc "All-or-Nothing" (hoặc import thành công toàn bộ, hoặc Rollback hủy bỏ toàn bộ 0 sản phẩm nếu phát hiện bất kỳ lỗi nào) để tránh tình trạng dữ liệu dở dang, thiếu nhất quán trong CSDL.

**Các bước tái hiện (Steps to Reproduce):**
1. Đăng nhập Admin và chuyển sang tab **Sản phẩm**.
2. Chọn file `fr16_sample_mixed.csv` (chứa 2 dòng hợp lệ và 1 dòng thiếu tên sản phẩm).
3. Bấm **Import sản phẩm**.

**Kết quả kỳ vọng theo SRS (Expected Result):**
Hệ thống phát hiện dòng lỗi, hủy bỏ toàn bộ transaction, không chèn bất kỳ sản phẩm nào vào CSDL (`0 sản phẩm được thêm`) và thông báo toàn bộ file bị từ chối.

**Kết quả thực tế (Actual Result):**
Hệ thống chèn 2 sản phẩm vào CSDL và hiển thị: *"✅ Import hoàn tất: 2/3 sản phẩm được thêm - Hàng 3: Thiếu tên sản phẩm"*.

---

## Kết Luận

Tổng cộng **7 lỗi phần mềm** (gồm 5 lỗi logic/nghiệp vụ bắt dính bằng Playwright assertions và 2 lỗi UI/công thức) đã được ghi nhận và phân tích chi tiết.
