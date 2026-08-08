# TC-LOCK-BVA-002: Kiểm tra đăng nhập sai 3 lần nhưng ngoài cửa sổ 30 giây

## Requirement ID
FR-02

## Module / Test type / Technique
Lockout / Boundary Value Analysis (BVA)

## Preconditions
- Tài khoản đang hoạt động bình thường.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu sai | WrongPassword1! |

## Test steps
1. Nhập sai mật khẩu lần 1.
2. Chờ 35 giây.
3. Nhập sai mật khẩu lần 2.
4. Chờ 35 giây.
5. Nhập sai mật khẩu lần 3.

## Expected result
- Tài khoản không bị khóa vì các lần sai không diễn ra liên tiếp trong cửa sổ 30 giây (hoặc reset bộ đếm theo thiết kế thời gian thực).

## Status / Related bugs
Not Run / None
