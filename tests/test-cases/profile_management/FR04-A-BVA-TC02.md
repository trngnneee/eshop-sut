# FR04-A-BVA-TC02: Biên MIN của địa chỉ

## Requirement ID
FR-04

## Module / Loại test / Kỹ thuật
Profile Management - Địa chỉ / Functional / Phân tích giá trị biên (Boundary Value Analysis)

## Tiền điều kiện
- Người dùng đã đăng nhập bằng tài khoản hợp lệ.
- Có JWT token hợp lệ để gọi API `GET /api/users/me` và `PUT /api/users/me`.
- Các field không nằm trong phạm vi test dùng dữ liệu hợp lệ hiện có.

## Dữ liệu kiểm thử
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Input đang kiểm thử | Địa chỉ giao hàng |
| API field | `shipping_address` |
| Lớp/biên | MIN, độ dài 5 |
| Giá trị | `House` |

## Các bước kiểm thử
1. Đăng nhập bằng tài khoản hợp lệ và lấy JWT token.
2. Mở trang Hồ sơ hoặc gửi request `PUT /api/users/me`.
3. Nhập/gửi trường Địa chỉ giao hàng (`shipping_address`) theo dữ liệu kiểm thử; các field profile còn lại dùng giá trị hợp lệ.
4. Bấm nút Cập nhật hoặc gửi request cập nhật hồ sơ.
5. Reload trang Hồ sơ hoặc gọi `GET /api/users/me` để đối chiếu kết quả.

## Kết quả mong đợi
- Chấp nhận cập nhật; hồ sơ lưu/hiển thị `shipping_address = "House"`.

## Kết quả thực tế
- Chấp nhận cập nhật; hồ sơ lưu/hiển thị `House`.

## Trạng thái / Bug liên quan
Pass / None
