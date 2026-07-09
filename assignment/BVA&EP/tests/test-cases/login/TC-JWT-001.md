# TC-JWT-001: Xử lý Token JWT thiếu trường exp (Expiration Time)

## Requirement ID
SEC-02

## Module / Test type / Technique
JWT / Security Testing

## Preconditions
- Sử dụng token JWT được ký không có trường exp gửi lên API.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Payload | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MX0... |

## Test steps
1. Gửi GET request tới `/api/users/me` kèm token JWT thiếu trường `exp`.

## Expected result
- Backend từ chối token (HTTP 401 hoặc 403) vì lý do bảo mật, hoặc token không được xem là hợp lệ.

## Status / Related bugs
Pass / None
