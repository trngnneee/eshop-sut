# TC-LOGIN-BVA-004: Kiểm tra Email biên độ dài max - 1 (253 ký tự)

## Requirement ID
FR-02

## Module / Test type / Technique
Login / Boundary Value Analysis (BVA)

## Preconditions
- Đã đăng ký tài khoản có email dài 253 ký tự.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@eshop.com |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Nhập email dài 253 ký tự.
2. Nhập mật khẩu đúng.
3. Nhấn 'Đăng nhập'.

## Expected result
- Hệ thống chấp nhận và đăng nhập thành công.

## Status / Related bugs
Not Run / None
