# TC-FR02-UC-002: Admin đăng nhập thành công

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / Use Case Testing

## Source Use Case Scenario
- Scenario: UC-SC-02 (Admin đăng nhập thành công - Alternate Flow 1)

## Preconditions
- Tài khoản Admin `admin@eshop.com` / `Admin123!` tồn tại trong database.

## Test Data
| Field | Value | Note |
| :--- | :--- | :--- |
| Email | admin@eshop.com | Tài khoản quản trị |
| Password | Admin123! | Mật khẩu Admin đúng |

## Test Steps
1. Truy cập giao diện Admin Đăng nhập tại `http://localhost:5174/login` (hoặc cổng tương ứng của Admin).
2. Nhập Email `admin@eshop.com` và Password `Admin123!`.
3. Bấm nút "Đăng nhập".

## Expected Result
- Đăng nhập thành công với vai trò Admin.
- Hệ thống chuyển hướng người dùng sang trang Dashboard quản trị (`/admin/dashboard`).
- Menu hiển thị các tính năng quản lý dành riêng cho Admin (Categories, Products, Coupons, Orders, Users).

## Status / Related Bugs
- **Result**: Passed
- **Related Bug**: None
