# FR04-N-BVA-TC01: Biên dưới MIN-1 của họ tên

## Requirement ID
FR-04

## Module / Loại test / Kỹ thuật
Profile Management - Họ tên / Functional / Phân tích giá trị biên (Boundary Value Analysis)

## Tiền điều kiện
- Người dùng đã đăng nhập bằng tài khoản hợp lệ.
- Có JWT token hợp lệ để gọi API `GET /api/users/me` và `PUT /api/users/me`.
- Các field không nằm trong phạm vi test dùng dữ liệu hợp lệ hiện có.

## Dữ liệu kiểm thử
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Input đang kiểm thử | Họ tên |
| API field | `name` |
| Lớp/biên | MIN-1, độ dài 0 |
| Giá trị | [Rỗng] |

## Các bước kiểm thử
1. Đăng nhập bằng tài khoản hợp lệ và lấy JWT token.
2. Mở trang Hồ sơ hoặc gửi request `PUT /api/users/me`.
3. Nhập/gửi trường Họ tên (`name`) theo dữ liệu kiểm thử; các field profile còn lại dùng giá trị hợp lệ.
4. Bấm nút Cập nhật hoặc gửi request cập nhật hồ sơ.
5. Reload trang Hồ sơ hoặc gọi `GET /api/users/me` để đối chiếu kết quả.

## Kết quả mong đợi
- Từ chối cập nhật; hiển thị/trả về lỗi bắt buộc nhập; họ tên cũ không đổi.

## Kết quả thực tế
- Frontend có báo lỗi, nhưng khi thử bằng Postman/API thì profile vẫn bị cập nhật bằng giá trị rỗng.

## Trạng thái / Bug liên quan
Fail / BUG-FR04-N-02
