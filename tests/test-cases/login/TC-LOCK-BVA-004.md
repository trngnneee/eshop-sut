# TC-LOCK-BVA-004: Kiểm tra reset bộ đếm khi hết thời gian khóa và sai tiếp lần đầu

## Requirement ID
FR-02

## Module / Test type / Technique
Lockout / Boundary Value Analysis (BVA)

## Preconditions
- Tài khoản đã bị khóa, và thời gian khóa 30 giây đã hết hoàn toàn.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu sai | WrongPassword1! |

## Test steps
1. Chờ hết 30 giây khóa.
2. Thực hiện đăng nhập sai mật khẩu 1 lần.
3. Kiểm tra bộ đếm `login_attempts` trong CSDL.

## Expected result
- Yêu cầu bị từ chối đăng nhập nhưng tài khoản không bị khóa lại ngay lập tức.
- Bộ đếm `login_attempts` được reset và tính lại từ 1.

## Status / Related bugs
Not Run / None
