# TC-LOGIN-034: Đăng nhập thất bại khi Email thiếu ký tự @

## Requirement ID
FR-02, FR-22

## Module / Test type / Technique
Login / Equivalence Partitioning (EP)

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | invalidemail.com |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Nhập email thiếu ký tự '@'.
2. Nhập mật khẩu.
3. Nhấp nút 'Đăng nhập'.

## Expected result
- Hệ thống báo lỗi định dạng email không hợp lệ (ví dụ: 'Please enter a valid email address').

## Status / Related bugs
Not Run / None
