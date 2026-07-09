# TC-LOGIN-025: Kiểm tra biên thời gian khóa (không mở khóa tự động ở giây thứ 29)

## Requirement ID
FR-02

## Module / Test type / Technique
Login / Functional / Boundary Value Analysis (BVA)

## Preconditions
- Đã đăng ký tài khoản `test_tc26@eshop.com` với mật khẩu `ValidPassword1!` trên hệ thống.
- Tài khoản đã bị khóa do nhập sai mật khẩu 3 lần liên tiếp.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test_tc26@eshop.com |
| Mật khẩu đúng | ValidPassword1! |

## Test steps
1. Chờ đợi đúng 29 giây kể từ khi tài khoản bị khóa.
2. Gửi yêu cầu đăng nhập bằng mật khẩu đúng `ValidPassword1!`.
3. Kiểm tra mã phản hồi HTTP và nội dung lỗi trả về.

## Expected result
- Ở giây thứ 29 (dưới thời hạn khóa 30 giây), yêu cầu đăng nhập bằng mật khẩu đúng vẫn bị chặn.
- Server trả về HTTP 403 Forbidden cùng thông báo: "Tài khoản đã bị khóa. Vui lòng thử lại sau."

## Status / Related bugs
Fail / #32
