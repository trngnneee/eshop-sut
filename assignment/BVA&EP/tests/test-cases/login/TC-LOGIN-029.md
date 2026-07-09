# TC-LOGIN-029: Kiểm tra bộ đếm đăng nhập sai không tăng khi đăng nhập thành công

## Requirement ID
FR-02

## Module / Test type / Technique
Login / Functional / Positive Testing

## Preconditions
- Đã đăng ký tài khoản `test_tc30@eshop.com` với mật khẩu `ValidPassword1!` trên hệ thống.
- Trạng thái ban đầu: chưa nhập sai lần nào.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test_tc30@eshop.com |
| Mật khẩu đúng | ValidPassword1! |

## Test steps
1. Gửi yêu cầu đăng nhập POST tới `/api/login` với email và mật khẩu đúng.
2. Kiểm tra phản hồi HTTP thành công.
3. Kiểm tra trạng thái tài khoản bằng cách đăng nhập thử qua API.

## Expected result
- Đăng nhập thành công (HTTP 200).
- Số lần đăng nhập sai của tài khoản phải giữ nguyên bằng `0` (không tăng).

## Status / Related bugs
Pass / None
