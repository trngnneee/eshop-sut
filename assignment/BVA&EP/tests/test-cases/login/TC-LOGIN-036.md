# TC-LOGIN-036: Đăng nhập thất bại khi Email có nhiều ký tự @

## Requirement ID
FR-02, FR-22

## Module / Test type / Technique
Login / Equivalence Partitioning (EP)

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | user@@gmail.com |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Nhập email chứa 2 dấu '@' liên tiếp.
2. Nhấn 'Đăng nhập'.

## Expected result
- Hệ thống báo lỗi định dạng email không hợp lệ.

## Status / Related bugs
Pass / None
