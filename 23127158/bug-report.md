## BUG-FR03-001: OTP sinh ra 4 chữ số thay vì 6 chữ số (FR-03)

## Found by Test Case

TC-ST-FORGOT-PASSWORD-002, TC-ST-FORGOT-PASSWORD-SW1-001, TC-ST-FORGOT-PASSWORD-SW1-003, TC-ST-FORGOT-PASSWORD-SW2-001, TC-ST-FORGOT-PASSWORD-SW2-003, TC-ST-FORGOT-PASSWORD-E2E-001, TC-ST-FORGOT-PASSWORD-E2E-002, TC-ST-FORGOT-PASSWORD-FINAL-001

## Requirement liên quan

FR-03

## Severity / Priority

High / P2

## Environment

* **OS**: Windows 11
* **Application**: EShop Backend API
* **Feature**: Quên mật khẩu — Sinh mã OTP
* **API Endpoint**:

```text
POST /api/forgot-password
```

* **Build/Commit**: Latest

## Steps to reproduce

1. Gửi request POST đến endpoint:

```http
POST /api/forgot-password
Content-Type: application/json

{"email": "test@eshop.com"}
```

2. Quan sát giá trị `resetToken` trong response body.

## Expected result

Hệ thống sinh mã OTP gồm **6 chữ số ngẫu nhiên** theo đặc tả FR-03.

Ví dụ: `{"message": "Mã đặt lại mật khẩu đã được tạo", "resetToken": "472918"}`

## Actual result

API trả về HTTP 200 OK nhưng giá trị `resetToken` chỉ có **4 chữ số**.

Ví dụ: `{"message": "Mã đặt lại mật khẩu đã được tạo", "resetToken": "7421"}`

---

## BUG-FR03-002: Backend không kiểm tra độ mạnh mật khẩu khi đặt lại mật khẩu (FR-03 + FR-01)

## Found by Test Case

TC-ST-FORGOT-PASSWORD-007

## Requirement liên quan

FR-03, FR-01

## Severity / Priority

High / P2

## Environment

* **OS**: Windows 11
* **Application**: EShop Backend API
* **Feature**: Đặt lại mật khẩu — Kiểm tra độ mạnh mật khẩu mới
* **API Endpoint**:

```text
POST /api/reset-password
```

* **Build/Commit**: Latest

## Steps to reproduce

1. Gửi yêu cầu OTP trước:

```http
POST /api/forgot-password
Content-Type: application/json

{"email": "test@eshop.com"}
```

2. Lấy `resetToken` từ response (ví dụ: `7421`).

3. Gửi request đặt lại mật khẩu với mật khẩu yếu:

```http
POST /api/reset-password
Content-Type: application/json

{
  "email": "test@eshop.com",
  "resetToken": "7421",
  "newPassword": "abc"
}
```

## Expected result

Hệ thống từ chối yêu cầu và trả về HTTP 400 Bad Request với thông báo mật khẩu không đủ mạnh.

Mật khẩu phải đáp ứng tiêu chuẩn FR-01: tối thiểu 8 ký tự, 1 chữ hoa, 1 chữ thường, 1 chữ số, 1 ký tự đặc biệt.

## Actual result

API trả về HTTP **200 OK** và message `"Password reset successfully"`. Backend **không kiểm tra độ mạnh của mật khẩu mới**, cho phép người dùng đặt mật khẩu cực kỳ yếu như `"abc"`.

---

## BUG-FR03-003: Không hiển thị chỉ báo bước và nút "Quay lại đăng nhập" ở màn hình nhập email (FR-03)

## Found by Test Case

TC-ST-FORGOT-PASSWORD-001, TC-ST-FORGOT-PASSWORD-003, TC-ST-FORGOT-PASSWORD-SW1-002, TC-ST-FORGOT-PASSWORD-SW1-004, TC-ST-FORGOT-PASSWORD-SW2-002, TC-ST-FORGOT-PASSWORD-SW2-004, TC-ST-FORGOT-PASSWORD-E2E-001, TC-ST-FORGOT-PASSWORD-E2E-002

## Requirement liên quan

FR-03

## Severity / Priority

High / P2

## Environment

* **OS**: Windows 11
* **Application**: EShop Frontend Web
* **Feature**: Quên mật khẩu — Màn hình nhập email (Bước 1/2)
* **Screen / UI**: Màn hình nhập email của quy trình quên mật khẩu

## Steps to reproduce

1. Truy cập chức năng Quên mật khẩu từ màn hình đăng nhập.
2. Quan sát màn hình nhập email ở Bước 1/2.

## Expected result

Giao diện phải hiển thị chỉ báo bước **"Bước 1 / 2"** và nút **"Quay lại đăng nhập"** theo đặc tả FR-03.

## Actual result

Giao diện vẫn điều hướng sang màn hình nhập email nhưng **không hiển thị** chỉ báo bước "Bước 1 / 2" và **không có** nút "Quay lại đăng nhập".

---

## BUG-FR03-004: Lỗi biểu thức chính quy (Regex) kiểm tra độ mạnh mật khẩu trên Frontend (FR-03 + FR-01)

## Found by Test Case

TC-UC-FORGOT-PASSWORD-001, TC-UC-FORGOT-PASSWORD-004, TC-UC-FORGOT-PASSWORD-005

## Requirement liên quan

FR-03, FR-01, FR-22

## Severity / Priority

High / P2

## Environment

* **OS**: Windows 11
* **Application**: EShop Frontend Web
* **Feature**: Đặt lại mật khẩu — Kiểm duyệt mật khẩu ở giao diện
* **Screen / UI**: Màn hình đặt lại mật khẩu (Bước 2/2)

## Steps to reproduce

1. Truy cập luồng Quên mật khẩu và điền email `test@eshop.com`.
2. Lấy mã OTP hiển thị trên màn hình.
3. Ở Bước 2/2, nhập mật khẩu mới hợp lệ theo đặc tả: `NewPass123!` (độ dài 11 ký tự, chứa chữ hoa, chữ thường, số, và ký tự đặc biệt `!`).
4. Nhấn nút "Đặt lại mật khẩu".

## Expected result

Frontend chấp nhận mật khẩu `NewPass123!` và gửi yêu cầu đặt lại lên backend, do mật khẩu này hoàn toàn thỏa mãn các điều kiện mật khẩu mạnh ở FR-01.

## Actual result

Hệ thống hiển thị hộp thoại cảnh báo: `"Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT."` và chặn không cho gửi request.
Nguyên nhân do biểu thức chính quy `flawedStrongPasswordRegex` trong file `ForgotPassword.jsx` bị viết sai:
```javascript
const flawedStrongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\s)[A-Za-z\d\s]{8,}$/;
```
Bắt buộc mật khẩu phải chứa khoảng trắng (`(?=.*\s)`) và giới hạn các ký tự trong lớp `[A-Za-z\d\s]`, dẫn đến việc từ chối tất cả các mật khẩu mạnh tiêu chuẩn chứa ký tự đặc biệt (`!`, `@`, `$`, v.v.) và không chứa khoảng trắng.

---

## BUG-FR03-005: Thiếu trường nhập "Xác nhận mật khẩu mới" ở màn hình đặt lại mật khẩu (FR-03 + FR-22)

## Found by Test Case

TC-UC-FORGOT-PASSWORD-001, TC-UC-FORGOT-PASSWORD-004, TC-UC-FORGOT-PASSWORD-005, TC-UC-FORGOT-PASSWORD-007

## Requirement liên quan

FR-03, FR-22

## Severity / Priority

High / P2

## Environment

* **OS**: Windows 11
* **Application**: EShop Frontend Web
* **Feature**: Đặt lại mật khẩu — Nhập thông tin Bước 2/2
* **Screen / UI**: Màn hình đặt lại mật khẩu (Bước 2/2)

## Steps to reproduce

1. Truy cập chức năng Quên mật khẩu, nhập email `test@eshop.com` để nhận OTP và tiến đến Bước 2/2.
2. Quan sát các trường nhập liệu xuất hiện trên màn hình Bước 2/2.

## Expected result

Theo đặc tả FR-03 và FR-22, giao diện Bước 2 phải hiển thị đầy đủ các trường nhập liệu:
- Mã OTP
- Mật khẩu mới
- Xác nhận mật khẩu mới (phải khớp và có validation lỗi nếu không khớp).

## Actual result

Giao diện chỉ hiển thị hai trường: "Mã OTP (4 số)" và "Mật khẩu mới", hoàn toàn **không có** trường nhập "Xác nhận mật khẩu mới". Người dùng không thể xác thực lại mật khẩu vừa nhập để tránh lỗi gõ sai.

---

