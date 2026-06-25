# TC-LOGIN-BVA-005: Kiểm tra Email biên độ dài max (254 ký tự)

## Requirement ID
FR-02

## Module / Test type / Technique
Login / Boundary Value Analysis (BVA)

## Preconditions
- Đã đăng ký tài khoản có email dài đúng 254 ký tự.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@eshop.com |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Nhập email đúng 254 ký tự.
2. Nhập mật khẩu đúng.
3. Nhấn 'Đăng nhập'.

## Expected result
- Hệ thống chấp nhận và đăng nhập thành công.

## Status / Related bugs
Not Run / None
