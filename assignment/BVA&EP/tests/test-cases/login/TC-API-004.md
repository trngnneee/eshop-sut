# TC-API-004: API Đăng nhập từ chối request có header Content-Type không hợp lệ

## Requirement ID
SEC-01

## Module / Test type / Technique
API Contract / Security Testing

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| email | test@eshop.com |
| password | ValidPassword1! |

## Test steps
1. Gửi POST request tới `/api/login` với header `Content-Type: text/plain` thay vì `application/json`.

## Expected result
- API trả về HTTP 415 Unsupported Media Type hoặc HTTP 400 Bad Request.

## Status / Related bugs
Pass / None
