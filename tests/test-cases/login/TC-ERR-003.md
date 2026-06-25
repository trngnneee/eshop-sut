# TC-ERR-003: Thông báo lỗi an toàn khi tài khoản bị khóa (Account Locked)

## Requirement ID
FR-22

## Module / Test type / Technique
Privacy / Security Testing

## Preconditions
- Tài khoản đang bị khóa.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Đăng nhập bằng mật khẩu đúng trong thời gian khóa.

## Expected result
- Thông báo hiển thị lỗi chung: 'Tài khoản đã bị khóa. Vui lòng thử lại sau.' (hoặc tương tự).
- Không tiết lộ chi tiết số lần sai hay thời điểm chính xác mở khóa nếu không cần thiết để tránh dò xét bảo mật.

## Status / Related bugs
Not Run / None
