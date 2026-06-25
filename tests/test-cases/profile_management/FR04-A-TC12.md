# FR04-A-TC12: Địa chỉ là kiểu số

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
| Lớp/biên | A12 - Không phải chuỗi |
| Giá trị | `12345` dạng number |

## Các bước kiểm thử
1. Đăng nhập bằng tài khoản hợp lệ và lấy JWT token.
2. Gửi request `PUT /api/users/me` với các field profile còn lại hợp lệ.
3. Gửi `shipping_address` bằng kiểu number theo dữ liệu kiểm thử.
4. Gửi request cập nhật hồ sơ.
5. Gọi `GET /api/users/me` để kiểm tra dữ liệu profile sau cập nhật.

## Kết quả mong đợi
- API từ chối request; địa chỉ cũ không đổi.

## Kết quả thực tế
- API chấp nhận request và cập nhật profile.

## Trạng thái / Bug liên quan
Fail / BUG-FR04-A-05
