# TC-LOGIN-026: Chặn tạo mới token JWT khi đang đăng nhập bằng mật khẩu đúng trong thời gian khóa

## Requirement ID
FR-02

## Module / Test type / Technique
Login / Security / Negative Testing

## Preconditions
- Đã đăng ký tài khoản `test_tc27@eshop.com` với mật khẩu `ValidPassword1!` trên hệ thống.
- Tài khoản đã bị khóa do nhập sai mật khẩu 3 lần liên tiếp.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test_tc27@eshop.com |
| Mật khẩu đúng | ValidPassword1! |

## Test steps
1. Gửi yêu cầu đăng nhập POST tới `/api/login` bằng mật khẩu đúng `ValidPassword1!` trong khi tài khoản đang bị khóa.
2. Kiểm tra xem phản hồi HTTP có chứa Token JWT hay không.

## Expected result
- API trả về HTTP 403 Forbidden.
- Phản hồi tuyệt đối không chứa trường `token` hoặc bất cứ thông tin xác thực nào.

## Status / Related bugs
Passed / None
