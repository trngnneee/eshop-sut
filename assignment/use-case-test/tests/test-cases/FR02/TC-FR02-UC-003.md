# TC-FR02-UC-003: Đăng nhập thất bại do thông tin sai

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / Use Case Testing

## Source Use Case Scenario
- Scenario: UC-SC-03 (Đăng nhập thất bại do thông tin sai - Exception Flow 1)

## Preconditions
- Tài khoản `test@eshop.com` tồn tại trong hệ thống.

## Test Data
| Field | Value | Note |
| :--- | :--- | :--- |
| Email | test@eshop.com | Email đúng |
| Password | WrongPass999 | Mật khẩu sai |

## Test Steps
1. Mở trang đăng nhập EShop.
2. Nhập Email `test@eshop.com` và mật khẩu sai `WrongPass999`.
3. Bấm nút "Đăng nhập".

## Expected Result
- Hệ thống từ chối đăng nhập.
- Hiển thị thông báo lỗi: "Invalid email or password" (hoặc thông báo lỗi tiếng Việt tương tự).
- Người dùng vẫn ở lại trang đăng nhập, các trường thông tin không bị xóa hoàn toàn để người dùng sửa lại.

## Status / Related Bugs
- **Result**: Failed
- **Related Bug**: None
