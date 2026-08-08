# TC-API-001: API Đăng nhập phản hồi lỗi khi thiếu trường email trong request body

## Requirement ID
SEC-01

## Module / Test type / Technique
API Contract / Equivalence Partitioning (EP)

## Preconditions
- Sử dụng công cụ API gửi yêu cầu.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| password | ValidPassword1! |

## Test steps
1. Gửi POST request tới `/api/login` với request body chỉ chứa trường password.

## Expected result
- Backend trả về mã lỗi HTTP 400 Bad Request.
- Response chứa thông điệp lỗi chỉ rõ thiếu trường email.

## Status / Related bugs
Passed / None
