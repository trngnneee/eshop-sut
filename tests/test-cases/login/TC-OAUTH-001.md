# TC-OAUTH-001: Đăng nhập Google thành công với Email đã đăng ký tài khoản thường trước đó

## Requirement ID
FR-02

## Module / Test type / Technique
OAuth / Functional Testing

## Preconditions
- Tài khoản `user@gmail.com` đã đăng ký bằng mật khẩu thường trên hệ thống.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OAuth Email | user@gmail.com |

## Test steps
1. Click chọn đăng nhập bằng Google.
2. Xác thực thành công tài khoản Google của `user@gmail.com`.

## Expected result
- Đăng nhập thành công.
- Liên kết tài khoản Google với tài khoản thường và cấp JWT token.

## Status / Related bugs
Failed / #45
