# TC-LOGIN-040: Đăng nhập thất bại khi Email hợp lệ nhưng chưa tồn tại

## Requirement ID
FR-02, FR-22

## Module / Test type / Technique
Login / Equivalence Partitioning (EP)

## Preconditions
- Email `notexist@eshop.com` chưa đăng ký trên hệ thống.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | notexist@eshop.com |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Nhập email hợp lệ nhưng chưa được đăng ký.
2. Nhập mật khẩu bất kỳ.
3. Nhấn 'Đăng nhập'.

## Expected result
- Đăng nhập thất bại.
- Hiển thị thông báo lỗi chung chung để đảm bảo bảo mật: 'Invalid email or password'.

## Status / Related bugs
Not Run / None
