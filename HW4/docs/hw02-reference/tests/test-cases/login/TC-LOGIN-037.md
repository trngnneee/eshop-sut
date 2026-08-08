# TC-LOGIN-037: Đăng nhập với Email có ký tự Unicode

## Requirement ID
FR-02, FR-22

## Module / Test type / Technique
Login / Equivalence Partitioning (EP)

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | tést@gmail.com |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Nhập email chứa ký tự Unicode tiếng Việt có dấu.
2. Nhấn 'Đăng nhập'.

## Expected result
- Hệ thống chấp nhận nếu cấu hình hỗ trợ Unicode, hoặc báo lỗi định dạng email không hợp lệ.

## Status / Related bugs
Not Run / None
