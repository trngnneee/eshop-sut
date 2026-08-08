# TC-ERR-002: Thông báo lỗi chung khi Email tồn tại nhưng password sai

## Requirement ID
FR-22

## Module / Test type / Technique
Privacy / Security Testing

## Preconditions
- Tài khoản `test@eshop.com` có tồn tại.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu | WrongPassword1! |

## Test steps
1. Nhập email đúng.
2. Nhập mật khẩu sai.
3. Nhấp Đăng nhập.

## Expected result
- Thông báo lỗi hiển thị giống hệt kịch bản nhập sai email: 'Invalid email or password'.
- Không tiết lộ mật khẩu sai cho tài khoản tồn tại.

## Status / Related bugs
Not Run / None
