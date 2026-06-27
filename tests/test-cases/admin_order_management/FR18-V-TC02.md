# FR18-V-TC02: Danh sách đơn hàng Admin không lộ dữ liệu nhạy cảm ngoài phạm vi

## Requirement ID
FR-18

## Module / Test type / Technique
Admin Order Management / Functional / Equivalence Partitioning / Security

## Preconditions
- Admin đã đăng nhập bằng JWT hợp lệ.
- Hệ thống có đơn hàng gắn với user có password hash hoặc token trong bảng user nếu database seed có các trường này.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Endpoint | GET /api/admin/orders |
| Sensitive fields | ["password", "password_hash", "reset_token", "locked_until"] |

## Test steps
1. Đăng nhập bằng tài khoản `admin` hợp lệ.
2. Gửi request `GET /api/admin/orders`.
3. Kiểm tra payload response và dữ liệu hiển thị trên Admin UI.

## Expected result
- Response không chứa password, password hash, reset token hoặc dữ liệu xác thực nhạy cảm của user.
- Admin UI không hiển thị các trường nhạy cảm ngoài thông tin cần thiết cho quản lý đơn hàng.

## Status / Related bugs
Passed / None
