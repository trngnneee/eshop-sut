# TC-LOGIN-BVA-003: Kiểm tra Email biên độ dài min + 1 (6 ký tự)

## Requirement ID
FR-02

## Module / Test type / Technique
Login / Boundary Value Analysis (BVA)

## Preconditions
- Đã đăng ký tài khoản có email dài 6 ký tự `ab@b.c`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | ab@b.c |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Nhập email dài 6 ký tự.
2. Nhập mật khẩu đúng.
3. Nhấn 'Đăng nhập'.

## Expected result
- Hệ thống chấp nhận và đăng nhập thành công.

## Status / Related bugs
Not Run / None
