# TC-OAUTH-005: Đăng nhập Google bị từ chối khi Email Google chưa được Verified

## Requirement ID
SEC-02

## Module / Test type / Technique
OAuth / Security Testing

## Preconditions
- Tài khoản Google chưa xác minh email (`email_verified = false`).

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| email_verified | False |

## Test steps
1. Thực hiện đăng nhập bằng Google và cấp quyền.

## Expected result
- Hệ thống từ chối đăng nhập.
- Hiển thị thông báo yêu cầu xác minh email trước khi sử dụng OAuth.

## Status / Related bugs
Failed / #45
