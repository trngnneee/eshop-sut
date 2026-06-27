# TC-LOGIN-035: Đăng nhập thất bại khi Email thiếu local-part

## Requirement ID
FR-02, FR-22

## Module / Test type / Technique
Login / Equivalence Partitioning (EP)

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | @gmail.com |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Nhập email bắt đầu bằng dấu '@' và domain nhưng thiếu local-part.
2. Nhấn 'Đăng nhập'.

## Expected result
- Hệ thống báo lỗi định dạng email không hợp lệ.

## Status / Related bugs
Not Run / None
