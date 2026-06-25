# TC-JWT-009: Xác thực khi Refresh Token hết hạn sử dụng

## Requirement ID
SEC-02

## Module / Test type / Technique
JWT / Session Testing

## Preconditions
- Sử dụng Refresh Token đã hết hạn gửi lên API refresh.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| RefreshToken | Expired Refresh Token |

## Test steps
1. Gửi POST request tới `/api/refresh-token` kèm refresh token đã hết hạn.

## Expected result
- API từ chối cấp mới Access Token.
- Trả về HTTP 401 và yêu cầu người dùng đăng nhập lại từ đầu.

## Status / Related bugs
Failed / #51
