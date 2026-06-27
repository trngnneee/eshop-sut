# TC-LOGIN-040: Đăng nhập thất bại khi Email tồn tại nhưng password sai

## Requirement ID
FR-02, FR-22

## Module / Test type / Technique
Login / Equivalence Partitioning (EP)

## Preconditions
- Tài khoản `test@eshop.com` đã tồn tại trên hệ thống.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu | IncorrectPass1! |

## Test steps
1. Nhập email đúng.
2. Nhập sai mật khẩu.
3. Nhấn 'Đăng nhập'.

## Expected result
- Đăng nhập thất bại.
- Hiển thị thông báo lỗi bảo mật chung: 'Invalid email or password'.

## Status / Related bugs
Not Run / None
