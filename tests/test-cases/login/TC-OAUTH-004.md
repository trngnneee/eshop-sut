# TC-OAUTH-004: Đăng nhập Google thất bại khi Google trả về Authorization Code không hợp lệ

## Requirement ID
FR-02, SEC-02

## Module / Test type / Technique
OAuth / Security Testing

## Preconditions
- Gửi giả mạo request callback OAuth.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Invalid Code | fake_auth_code_123 |

## Test steps
1. Gửi POST/GET request callback tới `/api/auth/google/callback` kèm code giả mạo.

## Expected result
- Backend từ chối xác thực và trả về lỗi HTTP 400 hoặc 401.

## Status / Related bugs
Not Run / None
