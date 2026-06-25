# TC-REMEMBER-005: Kiểm tra khi Remember Token bị chỉnh sửa hoặc giả mạo

## Requirement ID
SEC-02

## Module / Test type / Technique
Remember Me / Security Testing

## Preconditions
- Người dùng chỉnh sửa Remember token trong cookie hoặc localStorage bằng tay.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| RememberToken | TamperedRememberToken |

## Test steps
1. Truy cập trang `/dashboard` để kích hoạt tự động đăng nhập bằng token lỗi.

## Expected result
- Hệ thống phát hiện token không hợp lệ, xóa token lỗi và yêu cầu đăng nhập lại.

## Status / Related bugs
Not Run / None
