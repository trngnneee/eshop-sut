# FR04-P-TC12: Số điện thoại là kiểu số

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
| Lớp/biên | P12 - Không phải chuỗi |
| Giá trị | `9012345678` dạng number |

## Test steps
1. Đăng nhập bằng tài khoản hợp lệ và lấy JWT token.
2. Gửi request `PUT /api/users/me` với các field profile còn lại hợp lệ.
3. Gửi `phone` bằng kiểu number theo dữ liệu kiểm thử.
4. Gửi request cập nhật hồ sơ.
5. Gọi `GET /api/users/me` để kiểm tra dữ liệu profile sau cập nhật.

## Expected result
- API từ chối request; số điện thoại cũ không đổi.

## Actual result
- API chấp nhận request và cập nhật profile.

## Status / Related bugs
Fail / BUG-FR04-P-02
