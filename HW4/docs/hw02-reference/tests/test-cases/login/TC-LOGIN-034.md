# TC-LOGIN-034: Đăng nhập thất bại khi Email thiếu domain

## Requirement ID
FR-02, FR-22

## Module / Test type / Technique
Login / Equivalence Partitioning (EP)

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | user@ |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Nhập email có phần local-part và dấu '@' nhưng thiếu phần domain.
2. Nhấn 'Đăng nhập'.

## Expected result
- Hệ thống trả về thông báo lỗi định dạng email không hợp lệ.

## Status / Related bugs
Not Run / None
