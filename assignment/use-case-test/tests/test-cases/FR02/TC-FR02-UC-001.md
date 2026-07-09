# TC-FR02-UC-001: Khách hàng đăng nhập thành công

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / Use Case Testing

## Source Use Case Scenario
- Scenario: UC-SC-01 (Khách hàng đăng nhập thành công - Main Flow)

## Preconditions
- Người dùng đã đăng ký tài khoản khách hàng `test@eshop.com` / `Test1234!`.
- Tài khoản ở trạng thái hoạt động bình thường (`login_attempts = 0`).

## Test Data
| Field | Value | Note |
| :--- | :--- | :--- |
| Email | test@eshop.com | Tài khoản khách hàng |
| Password | Test1234! | Mật khẩu đúng |

## Test Steps
1. Mở trang đăng nhập của EShop tại `http://localhost:5173/login`.
2. Nhập Email `test@eshop.com` và Password `Test1234!`.
3. Nhấp chọn nút "Đăng nhập".

## Expected Result
- Hệ thống xử lý đăng nhập thành công.
- Lưu JWT token vào bộ nhớ trình duyệt (LocalStorage/SessionStorage).
- Giao diện chuyển hướng về trang chủ (`/`).
- Tên người dùng hiển thị chính xác trên thanh Navbar.

## Status / Related Bugs
- **Result**: Passed
- **Related Bug**: None
