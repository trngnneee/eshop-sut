# TC-LOCK-BVA-007: Kiểm tra bộ đếm đăng nhập sai không tăng vô hạn khi tài khoản đang bị khóa

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
2. Kiểm tra số lần đăng nhập sai tối đa trước khi bị khóa.

## Expected result
- Mọi yêu cầu đều bị từ chối với HTTP 403.
- Bộ đếm bộ đếm đăng nhập sai không tăng thêm vô hạn (giữ nguyên ở ngưỡng khóa).

## Status / Related bugs
Not Run / None
