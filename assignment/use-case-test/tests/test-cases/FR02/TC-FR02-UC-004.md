# TC-FR02-UC-004: Bị khóa tài khoản khi nhập sai 3 lần liên tiếp

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / Use Case Testing

## Source Use Case Scenario
- Scenario: UC-SC-04 (Bị khóa tài khoản khi nhập sai 3 lần liên tiếp - Exception Flow 2)

## Preconditions
- Tài khoản `test@eshop.com` đang có 2 lần nhập sai trước đó.

## Test Data
| Field | Value | Note |
| :--- | :--- | :--- |
| Email | test@eshop.com | Email đúng |
| Password | WrongPass999 | Mật khẩu sai lần 3 |

## Test Steps
1. Truy cập trang đăng nhập EShop.
2. Nhập Email `test@eshop.com` và Password sai `WrongPass999`.
3. Bấm nút "Đăng nhập".

## Expected Result
- Đăng nhập thất bại.
- Hệ thống hiển thị thông báo tài khoản bị khóa tạm thời (ví dụ: "Tài khoản bị khóa do nhập sai nhiều lần. Vui lòng thử lại sau 30 giây").
- Database: Ghi nhận `login_attempts = 3` và trường `locked_until` được thiết lập thời gian mở khóa ở tương lai.

## Status / Related Bugs
- **Result**: Failed
- **Related Bug**: None
