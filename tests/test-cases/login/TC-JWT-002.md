# TC-JWT-002: Kiểm tra Token JWT đã hết hạn sử dụng

## Requirement ID
SEC-02

## Module / Test type / Technique
JWT / Security Testing

## Preconditions
- Có một token JWT đã hết hạn.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Payload | Expired Token |

## Test steps
1. Gửi GET request tới `/api/users/me` kèm token đã hết hạn.

## Expected result
- API trả về lỗi xác thực HTTP 401 Unauthorized.

## Status / Related bugs
Not Run / None
