# TC-LOGIN-BVA-002: Kiểm tra Email biên độ dài min (5 ký tự)

## Requirement ID
FR-02

## Module / Test type / Technique
Login / Boundary Value Analysis (BVA)

## Preconditions
- Đã đăng ký tài khoản có email dài đúng 5 ký tự `a@b.c`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | a@b.c |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Nhập email đúng 5 ký tự.
2. Nhập mật khẩu đúng.
3. Nhấn 'Đăng nhập'.

## Expected result
- Hệ thống chấp nhận độ dài và gửi yêu cầu đăng nhập lên backend thành công.

## Status / Related bugs
Not Run / None
