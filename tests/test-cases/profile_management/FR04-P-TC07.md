# FR04-P-TC07: Số điện thoại chứa chữ cái

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management - Số điện thoại / Functional / Phân vùng tương đương (Domain Testing)

## Preconditions
- Người dùng đã đăng nhập bằng tài khoản hợp lệ.
- Có JWT token hợp lệ để gọi API `GET /api/users/me` và `PUT /api/users/me`.
- Các field không nằm trong phạm vi test dùng dữ liệu hợp lệ hiện có.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Input đang kiểm thử | Số điện thoại |
| API field | `phone` |
| Lớp/biên | P7 - Chứa chữ cái |
| Giá trị | `09012abc67` |

## Test steps
1. Đăng nhập bằng tài khoản hợp lệ và lấy JWT token.
2. Mở trang Hồ sơ hoặc gửi request `PUT /api/users/me`.
3. Nhập/gửi trường Số điện thoại (`phone`) theo dữ liệu kiểm thử; các field profile còn lại dùng giá trị hợp lệ.
4. Bấm nút Cập nhật hoặc gửi request cập nhật hồ sơ.
5. Reload trang Hồ sơ hoặc gọi `GET /api/users/me` để đối chiếu kết quả.

## Expected result
- Từ chối cập nhật; hiển thị/trả về lỗi validation; số điện thoại cũ không đổi.

## Actual result
- Bị từ chối với thông báo chung `Invalid phone number format`.

## Status / Related bugs
Fail / BUG-FR04-P-04
