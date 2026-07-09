# TC-LOGIN-041: Đăng nhập thất bại khi Email có khoảng trắng ở giữa

## Requirement ID
FR-02, FR-22

## Module / Test type / Technique
Login / Equivalence Partitioning (EP)

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | user name@gmail.com |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Nhập email có chứa khoảng trắng ở giữa phần local-part.
2. Nhấn 'Đăng nhập'.

## Expected result
- Hệ thống báo lỗi định dạng email không hợp lệ và chặn submit.

## Status / Related bugs
Pass / None
