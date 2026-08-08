# TC-LOGIN-BVA-007: Kiểm tra Password biên độ dài min - 1 (7 ký tự)

## Requirement ID
FR-02, FR-22

## Module / Test type / Technique
Login / Boundary Value Analysis (BVA)

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu | Short1! |

## Test steps
1. Nhập email.
2. Nhập mật khẩu chỉ có độ dài 7 ký tự.
3. Nhấn 'Đăng nhập'.

## Expected result
- Hệ thống báo lỗi mật khẩu không đạt độ dài tối thiểu (yêu cầu ít nhất 8 ký tự).

## Status / Related bugs
Not Run / None
