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
| **6 lỗi (Bugs)** | [https://github.com/trngnneee/eshop-sut/issues](https://github.com/trngnneee/eshop-sut/issues) |

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
Tại file `frontend-web/src/pages/Register.jsx` dòng 16, biểu thức chính quy (regular expression) kiểm tra độ mạnh mật khẩu được định nghĩa như sau:
```javascript
const flawedStrongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\s)[A-Za-z\d\s]{8,}$/;
```
Biểu thức này sử dụng `(?=.*\s)` (bắt buộc phải có ít nhất 1 khoảng trắng) thay vì `(?=.*[@$!%*?&])`, đồng thời tập ký tự cho phép `[A-Za-z\d\s]` lại cấm hoàn toàn các ký tự đặc biệt thông dụng (`!`, `@`, `#`, `$`, `%`, v.v.). Khi người dùng nhập một mật khẩu mạnh chuẩn an toàn (ví dụ: `StrongPass123!@`), hệ thống từ chối và báo lỗi sai: *"Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT."*

**Các bước tái hiện (Steps to Reproduce):**
1. Truy cập trang đăng ký: `http://localhost:5173/register`.
2. Nhập Họ Tên: `Nguyễn Văn A`, Email: `testuser@example.com`.
3. Nhập Mật khẩu: `StrongPass123!@` (mật khẩu có chữ hoa, chữ thường, số và ký tự đặc biệt `@`, `!`).
4. Nhấn nút **Đăng Ký**.

**Kết quả kỳ vọng (Expected Result):**
Mật khẩu được chấp nhận hợp lệ, hệ thống gửi request đăng ký lên server và chuyển hướng sang trang `/login`.

**Kết quả thực tế (Actual Result):**
Giao diện hiển thị banner lỗi đỏ: *"Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT."* và không cho phép gửi form.

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
Tại `frontend-web/src/pages/Register.jsx` dòng 48, trường nhập email được khai báo:
```jsx
<input type="text" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full border p-2 rounded" required />
```
Do sử dụng `type="text"`, trình duyệt không thể kích hoạt tính năng kiểm tra tính hợp lệ của email (HTML5 email constraint validation). Người dùng có thể nhập chuỗi bất kỳ không có ký tự `@` hoặc tên miền (ví dụ: `invalidemailformat`) và form vẫn gửi thành công lên server.

**Các bước tái hiện (Steps to Reproduce):**
1. Truy cập `http://localhost:5173/register`.
2. Nhập Họ Tên: `Le Van C`, Email: `invalidemailformat`, Mật khẩu: `ValidPass123 `.
3. Nhấn nút **Đăng Ký**.

**Kết quả kỳ vọng (Expected Result):**
Trình duyệt chặn gửi form và hiển thị tooltip thông báo email không đúng định dạng.

**Kết quả thực tế (Actual Result):**
Form gửi thành công và hệ thống chuyển hướng sang `/login`.

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
Trong `backend/database.js` và `backend/server.js`, bảng `users` được tạo với câu lệnh:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT,
    role TEXT DEFAULT 'user',
    ...
);
```
Cột `email` không có ràng buộc `UNIQUE`. Endpoint `POST /api/register` cũng không kiểm tra email đã tồn tại trước khi thực hiện `INSERT`. Do đó, người dùng có thể đăng ký nhiều tài khoản khác nhau với cùng email (ví dụ: `admin@eshop.com`), gây xung đột dữ liệu nghiêm trọng khi đăng nhập hoặc khôi phục mật khẩu.

**Các bước tái hiện (Steps to Reproduce):**
1. Đăng ký tài khoản với email `admin@eshop.com` và mật khẩu `ValidPass123 `.
2. Nhấn nút **Đăng Ký**.

**Kết quả kỳ vọng (Expected Result):**
Backend trả về mã lỗi 400/409 với thông báo: *"Email đã được sử dụng"*, giao diện giữ nguyên ở trang `/register`.

**Kết quả thực tế (Actual Result):**
Backend trả về HTTP 200 tạo bản ghi mới và chuyển sang `/login`.

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
Tại `backend/server.js` dòng 379:
```javascript
if (total_amount > coupon.min_order_amount) { ... }
```
Toán tử so sánh sử dụng `>` (lớn hơn tuyệt đối) thay vì `>=` (lớn hơn hoặc bằng). Khi người dùng có giá trị đơn hàng bằng đúng mức tối thiểu quy định của mã (ví dụ mã `SAVE10` có `min_order_amount = 300000` và giỏ hàng có giá trị `300.000 ₫`), hệ thống từ chối áp dụng mã và báo lỗi sai.

**Các bước tái hiện (Steps to Reproduce):**
1. Truy cập `http://localhost:5173/checkout`.
2. Đặt tổng tiền đơn hàng là `300000`.
3. Nhập mã giảm giá: `SAVE10`.
4. Nhấn nút **Áp dụng**.

**Kết quả kỳ vọng (Expected Result):**
Mã giảm giá được áp dụng thành công và hiển thị mức giảm 10%.

**Kết quả thực tế (Actual Result):**
Giao diện báo lỗi: *"Đơn hàng chưa đủ giá trị tối thiểu 300.000 ₫ để áp dụng mã này"*.

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
| **Phát hiện bởi test case** | `TC01 - Áp dụng mã giảm giá phần trăm SAVE10` (Kiểm tra công thức backend) |
| **GitHub Issue** | [Issue #5 - FR-09 Percentage Calculation Formula Defect](https://github.com/trngnneee/eshop-sut/issues/5) |

**Mô tả lỗi:**
Tại `backend/server.js` dòng 399-401 và 419-421:
```javascript
if (coupon.type === "percent") {
  discount_amount = Math.floor(total_amount * (1 - coupon.discount_value));
}
```
Khi `coupon.discount_value` được lưu dưới dạng số nguyên (ví dụ: `10` cho 10%), công thức tính toán thành `total_amount * (1 - 10) = -9 * total_amount`. Thay vì giảm 50.000 ₫ cho đơn 500.000 ₫, số tiền giảm bị tính thành `-4.500.000 ₫` và tổng thanh toán bị đội lên thành `5.000.000 ₫`. Công thức đúng phải là `Math.floor(total_amount * (coupon.discount_value / 100))`.

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
Tại `frontend-web/src/pages/Login.jsx` dòng 24:
```jsx
<h2 className="text-2xl font-bold mb-6 text-center">Đăng Ký</h2>
```
Tiêu đề trang hiển thị "Đăng Ký" thay vì "Đăng Nhập", gây nhầm lẫn cho người dùng khi được chuyển hướng từ trang đăng ký sang đăng nhập.

---

## Kết Luận

Tất cả 6 lỗi trên đã được ghi nhận trực tiếp qua quá trình thực thi kiểm thử tự động với Playwright. Các lỗi này chứng minh giá trị thực tế của kịch bản kiểm thử được thiết kế theo đúng đặc tả SRS khi đối chiếu với mã nguồn thực tế của hệ thống SUT.
