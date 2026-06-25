# TC-REMEMBER-008: Vô hiệu hóa Remember Token cũ sau khi đổi mật khẩu

## Requirement ID
SEC-02

## Module / Test type / Technique
Remember Me / Security Testing

## Preconditions
- Đăng nhập có tick chọn Remember Me trên Thiết bị 1.
- Người dùng thực hiện đổi mật khẩu thành công trên Thiết bị 2.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |

## Test steps
1. Từ Thiết bị 1, mở trình duyệt và truy cập trang `/dashboard`.

## Expected result
- Hệ thống phải yêu cầu đăng nhập lại vì token cũ đã bị invalid/thu hồi sau khi mật khẩu thay đổi.

## Status / Related bugs
Failed / #50
