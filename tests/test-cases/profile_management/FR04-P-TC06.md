# FR04-P-TC06: Thiếu field số điện thoại trong API body

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
| Lớp/biên | P6 - Thiếu thuộc tính |
| Giá trị | Không gửi thuộc tính `phone` |

## Test steps
1. Đăng nhập bằng tài khoản hợp lệ và lấy JWT token.
2. Gửi request `PUT /api/users/me` với các field profile còn lại hợp lệ.
3. Không gửi thuộc tính `phone` trong JSON body.
4. Gửi request cập nhật hồ sơ.
5. Gọi `GET /api/users/me` để kiểm tra dữ liệu profile sau cập nhật.

## Expected result
- API từ chối request; số điện thoại cũ không đổi.

## Actual result
- API chấp nhận request và cập nhật profile.

## Status / Related bugs
Fail / BUG-FR04-P-02
