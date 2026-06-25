# TC-API-007: API Đăng nhập thất bại phản hồi cấu trúc JSON an toàn (không chứa thông tin nhạy cảm)

## Requirement ID
SEC-01

## Module / Test type / Technique
API Contract / Security Testing

## Preconditions
- Tài khoản hoạt động.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| email | test@eshop.com |
| password | WrongPassword1! |

## Test steps
1. Gửi POST request login sai.
2. Kiểm tra response body nhận được.

## Expected result
- Đăng nhập thất bại (HTTP 401).
- Response JSON chỉ chứa thông điệp lỗi chung chung, không được lộ thông tin debug hoặc stack trace hệ thống.

## Status / Related bugs
Not Run / None
