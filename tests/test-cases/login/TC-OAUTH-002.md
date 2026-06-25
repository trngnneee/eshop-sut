# TC-OAUTH-002: Đăng nhập Google thành công với Email chưa từng tồn tại trên hệ thống

## Requirement ID
FR-02

## Module / Test type / Technique
OAuth / Functional Testing

## Preconditions
- Email Google `newuser@gmail.com` chưa từng đăng ký trên hệ thống.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OAuth Email | newuser@gmail.com |

## Test steps
1. Click chọn đăng nhập bằng Google.
2. Xác thực thành công tài khoản Google.

## Expected result
- Hệ thống tự động đăng ký tài khoản mới cho `newuser@gmail.com`.
- Đăng nhập thành công và chuyển hướng về Dashboard.

## Status / Related bugs
Not Run / None
