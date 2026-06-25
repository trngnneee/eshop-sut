# TC-JWT-010: Kiểm tra cơ chế xoay vòng Refresh Token (Token Rotation)

## Requirement ID
SEC-02

## Module / Test type / Technique
JWT / Security Testing

## Preconditions
- Hệ thống có hỗ trợ Refresh Token Rotation.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OldRefreshToken | Already Used Refresh Token |

## Test steps
1. Sử dụng lại một Refresh Token cũ đã từng được dùng để lấy Access Token trước đó.

## Expected result
- Hệ thống từ chối cấp token mới.
- Có thể thu hồi toàn bộ session liên quan để ngăn chặn tấn công chiếm đoạt phiên.

## Status / Related bugs
Failed / #51
