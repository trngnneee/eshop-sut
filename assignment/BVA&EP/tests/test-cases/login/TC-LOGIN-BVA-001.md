# TC-LOGIN-BVA-001: Kiểm tra Email biên độ dài min - 1 (4 ký tự)

## Requirement ID
FR-02, FR-22

## Module / Test type / Technique
Login / Boundary Value Analysis (BVA)

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | a@b. |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Nhập email có tổng độ dài là 4 ký tự.
2. Nhấn 'Đăng nhập'.

## Expected result
- Hệ thống từ chối vì email không hợp lệ (không đủ độ dài tối thiểu 5 ký tự).

## Status / Related bugs
Pass / None
