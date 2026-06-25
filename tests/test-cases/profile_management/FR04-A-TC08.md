# FR04-A-TC08: Địa chỉ chứa thẻ HTML

## Requirement ID
FR-04

## Module / Loại test / Kỹ thuật
Profile Management - Địa chỉ / Functional / Phân vùng tương đương (Domain Testing)

## Tiền điều kiện
- Người dùng đã đăng nhập bằng tài khoản hợp lệ.
- Có JWT token hợp lệ để gọi API `GET /api/users/me` và `PUT /api/users/me`.
- Các field không nằm trong phạm vi test dùng dữ liệu hợp lệ hiện có.

## Dữ liệu kiểm thử
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Input đang kiểm thử | Địa chỉ giao hàng |
| API field | `shipping_address` |
| Lớp/biên | A8 - Thẻ HTML |
| Giá trị | `<b>Home</b>` |

## Các bước kiểm thử
1. Đăng nhập bằng tài khoản hợp lệ và lấy JWT token.
2. Mở trang Hồ sơ hoặc gửi request `PUT /api/users/me`.
3. Nhập/gửi trường Địa chỉ giao hàng (`shipping_address`) theo dữ liệu kiểm thử; các field profile còn lại dùng giá trị hợp lệ.
4. Bấm nút Cập nhật hoặc gửi request cập nhật hồ sơ.
5. Reload trang Hồ sơ hoặc gọi `GET /api/users/me` để đối chiếu kết quả.

## Kết quả mong đợi
- Từ chối cập nhật; hiển thị/trả về lỗi validation; địa chỉ cũ không đổi.

## Kết quả thực tế
- Hệ thống chấp nhận/lưu giá trị dạng HTML; có lần hiển thị lại payload script đã lưu trước đó.

## Trạng thái / Bug liên quan
Fail / BUG-FR04-A-03
