# TC-REMEMBER-006: Chặn sử dụng Remember Token của User A gán sang User B

## Requirement ID
SEC-02

## Module / Test type / Technique
Remember Me / Security Testing

## Preconditions
- Sao chép Remember Token hợp lệ của User A gán vào cookie/localStorage của trình duyệt User B.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| TokenA | RememberTokenA |

## Test steps
1. Mở trình duyệt từ máy User B và truy cập `/dashboard`.

## Expected result
- Hệ thống từ chối hoặc phát hiện bất thường (ví dụ thay đổi IP/User-Agent bất ngờ) và yêu cầu xác thực lại.

## Status / Related bugs
Not Run / None
