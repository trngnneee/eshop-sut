# FR04-A-BVA-TC01: Biên dưới MIN-1 của địa chỉ

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management - Địa chỉ / Functional / Phân tích giá trị biên (Boundary Value Analysis)

## Preconditions
- Người dùng đã đăng nhập bằng tài khoản hợp lệ.
- Có JWT token hợp lệ để gọi API `GET /api/users/me` và `PUT /api/users/me`.
- Các field không nằm trong phạm vi test dùng dữ liệu hợp lệ hiện có.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Input đang kiểm thử | Địa chỉ giao hàng |
| API field | `shipping_address` |
| Lớp/biên | MIN-1, độ dài 4 |
| Giá trị | `Addr` |

## Test steps
1. Đăng nhập bằng tài khoản hợp lệ và lấy JWT token.
2. Mở trang Hồ sơ hoặc gửi request `PUT /api/users/me`.
3. Nhập/gửi trường Địa chỉ giao hàng (`shipping_address`) theo dữ liệu kiểm thử; các field profile còn lại dùng giá trị hợp lệ.
4. Bấm nút Cập nhật hoặc gửi request cập nhật hồ sơ.
5. Reload trang Hồ sơ hoặc gọi `GET /api/users/me` để đối chiếu kết quả.

## Expected result
- Từ chối cập nhật; hiển thị/trả về lỗi dưới độ dài tối thiểu; địa chỉ cũ không đổi.

## Actual result
- Hệ thống chấp nhận và lưu/hiển thị `Addr`.

## Status / Related bugs
Fail / BUG-FR04-A-02
