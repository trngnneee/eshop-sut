# TC-LOGIN-024: Kiểm tra đặt lại bộ đếm đăng nhập sai khi đăng nhập đúng xen kẽ (không liên tiếp)

## Requirement ID
FR-02

## Module / Test type / Technique
Login / Functional / State Transition Testing

## Preconditions
- Đã đăng ký tài khoản `test_tc25@eshop.com` với mật khẩu `ValidPassword1!` trên hệ thống.
- Trạng thái ban đầu của tài khoản có `login_attempts = 0` và không bị khóa.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test_tc25@eshop.com |
| Mật khẩu sai | WrongPass123! |
| Mật khẩu đúng | ValidPassword1! |

## Test steps
1. Thực hiện đăng nhập sai 2 lần liên tiếp bằng `test_tc25@eshop.com` và mật khẩu sai `WrongPass123!`.
2. Đăng nhập thành công bằng mật khẩu đúng `ValidPassword1!`.
3. Kiểm tra DB xem `login_attempts` đã được reset về `0` chưa.
4. Đăng xuất (hoặc trực tiếp gửi yêu cầu login mới).
5. Thực hiện đăng nhập sai 2 lần liên tiếp bằng mật khẩu sai `WrongPass123!`.
6. Kiểm tra xem tài khoản có bị khóa không.

## Expected result
- Bộ đếm đăng nhập sai phải được reset về `0` ngay sau khi đăng nhập thành công.
- Ở các lần đăng nhập sai sau đó, tài khoản không bị khóa vì số lần sai liên tiếp mới chỉ là 2 (chưa đạt ngưỡng khóa 3 lần).

## Status / Related bugs
Failed / #33
