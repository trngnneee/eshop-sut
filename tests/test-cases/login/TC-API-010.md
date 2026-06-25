# TC-API-010: API Đăng xuất phản hồi thành công cấu trúc JSON chuẩn

## Requirement ID
SEC-01

## Module / Test type / Technique
API Contract / Functional Testing

## Preconditions
- Có token JWT đăng nhập hợp lệ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Token | ValidToken |

## Test steps
1. Gửi request POST tới `/api/logout` kèm token hợp lệ.

## Expected result
- Đăng xuất thành công (HTTP 200).
- Response JSON trả về thông điệp xác nhận đăng xuất thành công.

## Status / Related bugs
Not Run / None
