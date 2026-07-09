# TC-API-003: API Đăng nhập từ chối request body sai định dạng JSON

## Requirement ID
SEC-01

## Module / Test type / Technique
API Contract / Boundary Testing

## Preconditions
- Gửi raw data không đúng cấu trúc JSON.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Payload | invalid_raw_json_string |

## Test steps
1. Gửi POST request tới `/api/login` với body là chuỗi không phải định dạng JSON hợp lệ.

## Expected result
- Backend trả về lỗi HTTP 400 Bad Request.
- Không gây crash server backend.

## Status / Related bugs
Pass / None
