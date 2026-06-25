# TC-REMEMBER-001: Đăng nhập không chọn Remember Me, đóng trình duyệt và mở lại

## Requirement ID
FR-02

## Module / Test type / Technique
Remember Me / Session Testing

## Preconditions
- Tài khoản đang hoạt động.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu | ValidPassword1! |
| RememberMe | False |

## Test steps
1. Đăng nhập thành công mà không tick chọn 'Remember me'.
2. Đóng toàn bộ trình duyệt.
3. Mở lại trình duyệt và truy cập trực tiếp vào trang `/dashboard`.

## Expected result
- Hệ thống yêu cầu đăng nhập lại (phiên làm việc bị xóa sau khi đóng trình duyệt).

## Status / Related bugs
Failed / #50
