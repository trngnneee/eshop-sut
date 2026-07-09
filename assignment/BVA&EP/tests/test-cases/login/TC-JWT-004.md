# TC-JWT-004: Kiểm tra Token JWT ký sai Secret Key

## Requirement ID
SEC-02

## Module / Test type / Technique
JWT / Security Testing

## Preconditions
- Tự ký một token JWT bằng một khóa bí mật (Secret Key) khác.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Payload | Signed with fake key |

## Test steps
1. Gửi yêu cầu API private kèm token giả ký sai key.

## Expected result
- Backend từ chối token và trả về HTTP 401 Unauthorized.

## Status / Related bugs
Pass / None
