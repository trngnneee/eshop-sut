# FR04-A-TC11: Thiếu field địa chỉ trong API body

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management - Địa chỉ / Functional / Phân vùng tương đương (Domain Testing)

## Preconditions
- Người dùng đã đăng nhập bằng tài khoản hợp lệ.
- Có JWT token hợp lệ để gọi API `GET /api/users/me` và `PUT /api/users/me`.
- Các field không nằm trong phạm vi test dùng dữ liệu hợp lệ hiện có.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Input đang kiểm thử | Địa chỉ giao hàng |
| API field | `shipping_address` |
| Lớp/biên | A11 - Thiếu thuộc tính |
| Giá trị | Không gửi thuộc tính `shipping_address` |

## Test steps
1. Đăng nhập bằng tài khoản hợp lệ và lấy JWT token.
2. Gửi request `PUT /api/users/me` với các field profile còn lại hợp lệ.
3. Không gửi thuộc tính `shipping_address` trong JSON body.
4. Gửi request cập nhật hồ sơ.
5. Gọi `GET /api/users/me` để kiểm tra dữ liệu profile sau cập nhật.

## Expected result
- API từ chối request; địa chỉ cũ không đổi.

## Actual result
- API chấp nhận request và cập nhật profile.

## Status / Related bugs
Fail / BUG-FR04-A-05
