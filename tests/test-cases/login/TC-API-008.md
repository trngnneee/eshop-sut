# TC-API-008: API Đăng xuất phản hồi lỗi khi không truyền Token xác thực

## Requirement ID
SEC-01

## Module / Test type / Technique
API Contract / Security Testing

## Preconditions
- Người dùng đang gửi request tới API đăng xuất.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |

## Test steps
1. Gửi request POST tới `/api/logout` không đính kèm header `Authorization`.

## Expected result
- API trả về lỗi HTTP 401 Unauthorized.

## Status / Related bugs
Not Run / None
