# TC-LOGIN-030: Đặt lại mật khẩu thành công phải giải phóng trạng thái khóa tài khoản và reset bộ đếm lần đăng nhập sai

## Requirement ID
FR-02

## Module / Test type / Technique
Login / Functional / State Transition Testing

## Preconditions
- Đã đăng ký tài khoản `test_tc31@eshop.com` với mật khẩu `ValidPassword1!` trên hệ thống.
- Tài khoản đã bị khóa do đăng nhập sai mật khẩu 3 lần liên tiếp.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test_tc31@eshop.com |
| Mật khẩu mới | NewPassword123! |

## Test steps
1. Tài khoản đang bị khóa (kiểm tra tài khoản hiển thị thông báo bị khóa do đăng nhập sai quá số lần quy định).
2. Thực hiện yêu cầu đặt lại mật khẩu thông qua API `/api/forgot-password` để nhận reset token.
3. Thực hiện cập nhật mật khẩu mới thông qua API `/api/reset-password` bằng reset token vừa nhận.
4. Gửi yêu cầu đăng nhập POST tới `/api/login` với mật khẩu mới.
5. Kiểm tra xem đăng nhập có thành công ngay lập tức không và xác minh trạng thái đăng nhập và khả năng tự động mở khóa của tài khoản.

## Expected result
- Đặt lại mật khẩu thành công.
- Trạng thái khóa tài khoản phải bị loại bỏ lập tức (tài khoản hết bị khóa, bộ đếm đăng nhập sai reset về `0`).
- Người dùng có thể đăng nhập ngay lập tức bằng mật khẩu mới mà không cần chờ hết thời gian khóa.

## Status / Related bugs
Failed / #49
