# TC-ERR-004: Thông báo lỗi an toàn khi tài khoản bị vô hiệu hóa (Account Disabled)

## Requirement ID
FR-22

## Module / Test type / Technique
Privacy / Security Testing

## Preconditions
- Tài khoản bị vô hiệu hóa.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | disabled@eshop.com |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Đăng nhập bằng thông tin đúng.

## Expected result
- Thông báo lỗi chung chung hoặc thông báo tài khoản bị đình chỉ.
- Không tiết lộ dữ liệu nhạy cảm của người dùng.

## Status / Related bugs
Not Run / None
