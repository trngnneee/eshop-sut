# TC-REMEMBER-002: Đăng nhập có chọn Remember Me, đóng trình duyệt và mở lại

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
| RememberMe | True |

## Test steps
1. Đăng nhập thành công và tick chọn 'Remember me'.
2. Đóng toàn bộ trình duyệt.
3. Mở lại trình duyệt và truy cập trực tiếp vào trang `/dashboard`.

## Expected result
- Người dùng vẫn ở trạng thái đăng nhập và truy cập thành công vào Dashboard mà không cần login lại.

## Status / Related bugs
Not Run / None
