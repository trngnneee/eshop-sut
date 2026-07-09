# TC-FR02-UC-005: Chặn đăng nhập khi tài khoản đang bị khóa

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / Use Case Testing

## Source Use Case Scenario
- Scenario: UC-SC-05 (Chặn đăng nhập khi tài khoản đang bị khóa - Exception Flow 3)

## Preconditions
- Tài khoản `test@eshop.com` đang bị khóa (`locked_until` ở tương lai).

## Test Data
| Field | Value | Note |
| :--- | :--- | :--- |
| Email | test@eshop.com | Tài khoản đang bị khóa |
| Password | Test1234! | Mật khẩu đúng |

## Test Steps
1. Thực hiện đăng nhập ngay sau khi tài khoản vừa bị khóa (chưa quá 30s).
2. Nhập Email `test@eshop.com` và Password đúng `Test1234!`.
3. Bấm nút "Đăng nhập".

## Expected Result
- Hệ thống từ chối đăng nhập ngay tại backend, trả về lỗi HTTP 403.
- Giao diện hiển thị thông báo lỗi rõ ràng thông báo tài khoản đang bị khóa và thời gian còn lại (nếu có).
- Database: Trạng thái tài khoản giữ nguyên bị khóa, không reset bộ đếm hay thay đổi gì.

## Status / Related Bugs
- **Result**: Passed
- **Related Bug**: None
