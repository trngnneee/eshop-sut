# TC-LOCK-BVA-005: Kiểm tra đăng nhập đúng chính xác tại giây thứ 30 sau khi bị khóa

## Requirement ID
FR-02

## Module / Test type / Technique
Lockout / Boundary Value Analysis (BVA)

## Preconditions
- Tài khoản đang bị khóa do nhập sai mật khẩu 3 lần liên tiếp.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu đúng | ValidPassword1! |

## Test steps
1. Chờ đúng 30 giây kể từ lúc bị khóa.
2. Gửi yêu cầu đăng nhập bằng mật khẩu đúng.

## Expected result
- Đăng nhập thành công (hoặc thất bại tùy theo logic hệ thống quy định >= 30s hay > 30s).

## Status / Related bugs
Not Run / None
