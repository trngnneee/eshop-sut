# TC-LOGIN-028: Đồng bộ trạng thái khóa tài khoản khi có nhiều thiết bị/phiên truy cập đồng thời

## Requirement ID
FR-02

## Module / Test type / Technique
Login / Security / Multi-client Synchronization Testing

## Preconditions
- Đã đăng ký tài khoản `test_tc28@eshop.com` với mật khẩu `ValidPassword1!` trên hệ thống.
- Sử dụng hai phiên HTTP client khác nhau (Client A và Client B) truy cập đồng thời.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test_tc28@eshop.com |
| Mật khẩu sai | WrongPass123! |
| Mật khẩu đúng | ValidPassword1! |

## Test steps
1. Client A thực hiện đăng nhập sai mật khẩu 3 lần liên tiếp, kích hoạt trạng thái khóa tài khoản.
2. Ngay lập tức, Client B gửi yêu cầu đăng nhập bằng mật khẩu đúng `ValidPassword1!`.
3. Kiểm tra phản hồi trả về từ Client B.

## Expected result
- Trạng thái khóa tài khoản lưu trữ ở DB phải có hiệu lực lập tức trên toàn hệ thống.
- Client B phải nhận được phản hồi HTTP 403 Forbidden và bị chặn đăng nhập, mặc dù Client B không phải là bên thao tác sai và nhập đúng mật khẩu.

## Status / Related bugs
Passed / None
