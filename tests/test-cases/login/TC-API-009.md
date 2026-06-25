# TC-API-009: API Đăng xuất phản hồi lỗi khi truyền Token xác thực không hợp lệ

## Requirement ID
SEC-01

## Module / Test type / Technique
API Contract / Security Testing

## Preconditions
- Sử dụng token hỏng.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Token | InvalidToken123 |

## Test steps
1. Gửi request POST tới `/api/logout` kèm header `Authorization: Bearer InvalidToken123`.

## Expected result
- API trả về lỗi HTTP 401 Unauthorized hoặc 403 Forbidden.

## Status / Related bugs
Not Run / None
