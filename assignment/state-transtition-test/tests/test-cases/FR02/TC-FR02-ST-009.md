# TC-FR02-ST-009: Kịch bản kiểm thử tích hợp đầu cuối (End-to-End Path)

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / State Transition Testing

## Target Coverage
- [x] End-to-End Test Path (Active -> Failed 1st -> Failed 2nd -> Locked -> lockout_timeout -> Active -> login_success -> Active)

## Source Design Rule
- Vòng đời toàn vẹn từ hoạt động bình thường -> bị khóa -> chờ tự động mở -> đăng nhập thành công.

## Preconditions
- Tài khoản `test@eshop.com` đang ở trạng thái hoạt động bình thường (`login_attempts = 0`).

## Test Data
| Step Index | Input Password | Expected Action | Expected State |
| :--- | :--- | :--- | :--- |
| 1 | Wrong123! | Báo lỗi thông tin sai | Failed 1st |
| 2 | Wrong123! | Báo lỗi thông tin sai | Failed 2nd |
| 3 | Wrong123! | Báo lỗi tài khoản bị khóa | Locked |
| 4 (Wait 30s) | - | Không có | Active |
| 5 | Test1234! | Đăng nhập thành công | Active |

## Test Steps
1. Truy cập trang đăng nhập, nhập Email `test@eshop.com` và mật khẩu sai `Wrong123!`. Nhấp "Đăng nhập".
2. Tiếp tục nhập mật khẩu sai `Wrong123!` lần thứ 2. Nhấp "Đăng nhập".
3. Tiếp tục nhập mật khẩu sai `Wrong123!` lần thứ 3. Nhấp "Đăng nhập".
4. Đợi hết thời gian khóa (30 giây).
5. Nhập mật khẩu đúng `Test1234!`. Nhấp "Đăng nhập".

## Expected Result
- Nhập sai lần 1 & 2: Hệ thống báo lỗi thông tin sai.
- Nhập sai lần 3: Hệ thống báo lỗi khóa tài khoản. DB ghi nhận trạng thái bị khóa.
- Đăng nhập sau 30 giây với mật khẩu đúng: Hệ thống đăng nhập thành công và chuyển hướng về trang chủ. DB reset bộ đếm về 0.

## Status / Related Bugs
- **Result**: Failed
- **Related Bug**: BUG-FR02-ST-01
