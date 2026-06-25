# TC-API-002: API Đăng nhập phản hồi lỗi khi thiếu trường password trong request body

## Requirement ID
SEC-01

## Module / Test type / Technique
API Contract / Equivalence Partitioning (EP)

## Preconditions
- Sử dụng công cụ API gửi yêu cầu.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| email | test@eshop.com |

## Test steps
1. Gửi POST request tới `/api/login` với request body chỉ chứa trường email.

## Expected result
- Backend trả về mã lỗi HTTP 400 Bad Request.
- Response chứa thông điệp lỗi chỉ rõ thiếu trường password.

## Status / Related bugs
Failed / #52
