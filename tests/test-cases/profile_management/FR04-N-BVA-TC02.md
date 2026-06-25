# FR04-N-BVA-TC02: Biên MIN của họ tên

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management - Họ tên / Functional / Phân tích giá trị biên (Boundary Value Analysis)

## Preconditions
- Người dùng đã đăng nhập bằng tài khoản hợp lệ.
- Có JWT token hợp lệ để gọi API `GET /api/users/me` và `PUT /api/users/me`.
- Các field không nằm trong phạm vi test dùng dữ liệu hợp lệ hiện có.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Input đang kiểm thử | Họ tên |
| API field | `name` |
| Lớp/biên | MIN, độ dài 1 |
| Giá trị | `A` |

## Test steps
1. Đăng nhập bằng tài khoản hợp lệ và lấy JWT token.
2. Mở trang Hồ sơ hoặc gửi request `PUT /api/users/me`.
3. Nhập/gửi trường Họ tên (`name`) theo dữ liệu kiểm thử; các field profile còn lại dùng giá trị hợp lệ.
4. Bấm nút Cập nhật hoặc gửi request cập nhật hồ sơ.
5. Reload trang Hồ sơ hoặc gọi `GET /api/users/me` để đối chiếu kết quả.

## Expected result
- Chấp nhận cập nhật; hồ sơ lưu/hiển thị `name = "A"`.

## Actual result
- Chấp nhận cập nhật; hồ sơ lưu/hiển thị `A`.

## Status / Related bugs
Pass / None
