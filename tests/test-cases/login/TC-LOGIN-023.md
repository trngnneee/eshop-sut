# TC-LOGIN-023: Kiểm tra biên dưới của số lần đăng nhập sai (2 lần liên tiếp không làm khóa tài khoản)

## Requirement ID
FR-02

## Module / Test type / Technique
Login / Functional / Boundary Value Analysis (BVA)

## Preconditions
- Đã đăng ký tài khoản `test_tc24@eshop.com` với mật khẩu `ValidPassword1!` trên hệ thống.
- Trạng thái ban đầu của tài khoản có `login_attempts = 0` và không bị khóa.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test_tc24@eshop.com |
| Mật khẩu sai | WrongPass123! |
| Mật khẩu đúng | ValidPassword1! |

## Test steps
1. Thực hiện đăng nhập sai 2 lần liên tiếp bằng `test_tc24@eshop.com` và mật khẩu sai `WrongPass123!`.
2. Kiểm tra trạng thái tài khoản trong Database để đảm bảo `login_attempts = 2` và `locked_until` vẫn là `NULL`.
3. Gửi yêu cầu đăng nhập thứ 3 bằng mật khẩu đúng `ValidPassword1!`.

## Expected result
- Sau 2 lần đăng nhập sai, tài khoản không bị khóa.
- Ở lần thứ 3, người dùng đăng nhập thành công với mật khẩu đúng.

## Status / Related bugs
Failed / #31, #33
