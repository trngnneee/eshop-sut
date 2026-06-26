# FR04-E-TC01: Email không thể thay đổi qua giao diện hồ sơ

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập bằng JWT hợp lệ.
- Người dùng đang ở trang Hồ sơ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| current_email | test@eshop.com |
| attempted_email | changed@eshop.com |

## Test steps
1. Mở trang Hồ sơ.
2. Quan sát trường Email.
3. Thử chỉnh sửa email qua giao diện.
4. Cập nhật các trường hồ sơ hợp lệ còn lại.

## Expected result
- Trường Email không cho phép chỉnh sửa qua giao diện.
- Sau khi cập nhật hồ sơ, email vẫn là giá trị ban đầu.

## Status / Related bugs
Passed / None
