# TC-REMEMBER-007: Kiểm tra các thuộc tính bảo mật của Remember Me Cookie

## Requirement ID
SEC-01

## Module / Test type / Technique
Remember Me / Cookie Security

## Preconditions
- Đăng nhập thành công có tick chọn Remember Me.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |

## Test steps
1. Mở DevTools kiểm tra thuộc tính của cookie Remember Me.

## Expected result
- Cookie phải được thiết lập các cờ bảo mật: HttpOnly (ngăn XSS đọc cookie), Secure (chỉ gửi qua HTTPS), và SameSite (chống CSRF).

## Status / Related bugs
Not Run / None
