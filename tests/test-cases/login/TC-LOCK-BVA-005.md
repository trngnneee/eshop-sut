# TC-LOCK-BVA-005: Kiểm tra gửi nhiều yêu cầu đăng nhập sai cùng lúc (Concurrent Requests)

## Requirement ID
FR-02, SEC-02

## Module / Test type / Technique
Lockout / Stress & Security Testing

## Preconditions
- Tài khoản đang hoạt động bình thường, `login_attempts = 0`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu sai | WrongPassword1! |

## Test steps
1. Sử dụng script gửi đồng thời 10 yêu cầu POST login sai trong cùng 1 giây.

## Expected result
- Bộ đếm ghi nhận chính xác trạng thái khóa và chuyển sang khóa sau 3 yêu cầu đầu tiên.
- Không xảy ra lỗi race condition hoặc crash DB.

## Status / Related bugs
Not Run / None
