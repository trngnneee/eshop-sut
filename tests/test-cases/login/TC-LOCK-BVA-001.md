# TC-LOCK-BVA-001: Kiểm tra bộ đếm đăng nhập sai không khóa sau 1 lần sai

## Requirement ID
FR-02

## Module / Test type / Technique
Lockout / Boundary Value Analysis (BVA)

## Preconditions
- Tài khoản đang hoạt động bình thường, `login_attempts = 0`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu sai | WrongPassword1! |

## Test steps
1. Nhập mật khẩu sai 1 lần.
2. Kiểm tra trạng thái tài khoản trong database.

## Expected result
- Tài khoản không bị khóa.
- Bộ đếm `login_attempts` trong CSDL bằng 1 (hoặc tăng thêm 1).

## Status / Related bugs
Not Run / None
