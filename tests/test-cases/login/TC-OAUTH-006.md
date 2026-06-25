# TC-OAUTH-006: Chặn đăng nhập Google khi tài khoản tương ứng đang bị Khóa (Lockout)

## Requirement ID
FR-02

## Module / Test type / Technique
OAuth / Functional Testing

## Preconditions
- Tài khoản `lockeduser@gmail.com` đang bị khóa do trước đó nhập sai mật khẩu thường 3 lần.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OAuth Email | lockeduser@gmail.com |

## Test steps
1. Click chọn đăng nhập bằng Google bằng tài khoản bị khóa.

## Expected result
- Hệ thống từ chối đăng nhập kể cả qua Google OAuth.
- Trả về mã lỗi HTTP 403 và báo tài khoản đang bị khóa.

## Status / Related bugs
Failed / #45
