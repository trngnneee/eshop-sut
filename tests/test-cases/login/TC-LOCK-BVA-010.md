# TC-LOCK-BVA-010: Kiểm tra bộ đếm đăng nhập sai không tăng vô hạn khi tài khoản đang bị khóa

## Requirement ID
FR-02

## Module / Test type / Technique
Lockout / Boundary Value Analysis (BVA)

## Preconditions
- Tài khoản đang bị khóa.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu sai | WrongPassword1! |

## Test steps
1. Tiếp tục gửi thêm 5 yêu cầu login sai khi tài khoản đang bị tạm khóa.
2. Truy vấn CSDL kiểm tra trường `login_attempts`.

## Expected result
- Mọi yêu cầu đều bị từ chối với HTTP 403.
- Bộ đếm `login_attempts` không tăng thêm vô hạn (giữ nguyên ở ngưỡng khóa).

## Status / Related bugs
Not Run / None
