# TC-LOGIN-038: Đăng nhập thành công với Email chứa subdomain

## Requirement ID
FR-02

## Module / Test type / Technique
Login / Equivalence Partitioning (EP)

## Preconditions
- Tài khoản với email `user@mail.company.com` đã đăng ký thành công.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | user@mail.company.com |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Nhập email có định dạng chứa subdomain.
2. Nhập mật khẩu đúng.
3. Nhấn 'Đăng nhập'.

## Expected result
- Hệ thống cho phép đăng nhập thành công và cấp JWT token.

## Status / Related bugs
Pass / None
