# TC-LOGIN-003: Tạm khóa tài khoản trong 30 giây sau khi đăng nhập sai 3 lần liên tiếp
## Requirement ID
FR-02
## Module / Test type / Technique
Login / Functional / Boundary Value Analysis / State Transition Testing
## Preconditions
- Đã đăng ký tài khoản `test@eshop.com` trên hệ thống.
- Trạng thái ban đầu của tài khoản có `login_attempts = 0` và không bị khóa.
- Người dùng đang ở trang đăng nhập.
## Test data
| Email | test@eshop.com |
| Password | WrongPassword123! |
## Test steps
1. Thực hiện đăng nhập sai liên tiếp 3 lần bằng tài khoản `test@eshop.com` và mật khẩu sai `WrongPassword123!`.
2. Kiểm tra thông báo của hệ thống ở lần đăng nhập sai thứ 3.
3. Kiểm tra trạng thái khóa của tài khoản trong cơ sở dữ liệu (xác minh trường `locked_until`).
4. Thử đăng nhập lại bằng thông tin đăng nhập đúng ngay lập tức (trong vòng dưới 30 giây) để xác minh tài khoản vẫn bị khóa.
5. Đợi qua 30 giây và thử đăng nhập lại bằng mật khẩu đúng để xác minh tài khoản tự động mở khóa.
## Expected result
- Ở lần đăng nhập sai thứ 3, hệ thống tạm khóa tài khoản.
- Thời gian khóa tài khoản là đúng **30 giây** kể từ lúc thực hiện lần đăng nhập sai thứ 3.
- Khi tài khoản đang bị khóa, bất kỳ nỗ lực đăng nhập nào (kể cả dùng đúng mật khẩu) đều phải bị từ chối với thông báo lỗi phù hợp (ví dụ: "Tài khoản đã bị khóa. Vui lòng thử lại sau.").
- Sau 30 giây, tài khoản được mở khóa tự động và đăng nhập bình thường khi nhập đúng mật khẩu.
## Status / Related bugs
Failed / Bug #2: Account locked for 180 seconds instead of 30 seconds
