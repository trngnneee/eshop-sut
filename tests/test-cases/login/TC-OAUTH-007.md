# TC-OAUTH-007: Chặn đăng nhập Google khi tài khoản tương ứng đã bị Vô hiệu hóa (Disabled)

## Requirement ID
FR-02

## Module / Test type / Technique
OAuth / Functional Testing

## Preconditions
- Tài khoản `disableduser@gmail.com` bị Admin vô hiệu hóa (active = 0).

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OAuth Email | disableduser@gmail.com |

## Test steps
1. Click chọn đăng nhập bằng Google bằng tài khoản bị vô hiệu hóa.

## Expected result
- Hệ thống từ chối đăng nhập và trả về thông báo lỗi tài khoản đã bị vô hiệu hóa.

## Status / Related bugs
Failed / #45
