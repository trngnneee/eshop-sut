# FR04-N-TC10: Thiếu field họ tên trong API body

## Requirement ID
FR-04

## Module / Test type / Technique
Profile Management - Họ tên / Functional / Phân vùng tương đương (Domain Testing)

## Preconditions
- Người dùng đã đăng nhập bằng tài khoản hợp lệ.
- Có JWT token hợp lệ để gọi API `GET /api/users/me` và `PUT /api/users/me`.
- Các field không nằm trong phạm vi test dùng dữ liệu hợp lệ hiện có.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Input đang kiểm thử | Họ tên |
| API field | `name` |
| Lớp/biên | N10 - Thiếu thuộc tính |
| Giá trị | Không gửi thuộc tính `name` |

## Test steps
1. Đăng nhập bằng tài khoản hợp lệ và lấy JWT token.
2. Gửi request `PUT /api/users/me` với các field profile còn lại hợp lệ.
3. Không gửi thuộc tính `name` trong JSON body.
4. Gửi request cập nhật hồ sơ.
5. Gọi `GET /api/users/me` để kiểm tra dữ liệu profile sau cập nhật.

## Expected result
- API từ chối request; họ tên cũ không đổi.

## Actual result
- API chấp nhận request và cập nhật profile thành công.

## Status / Related bugs
Fail / BUG-FR04-N-05
