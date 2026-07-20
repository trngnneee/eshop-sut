# TC-ST-FORGOT-PASSWORD-004

## Test Case ID
TC-ST-FORGOT-PASSWORD-004

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03, FR-01

## Testing Technique
State Transition Testing

## Coverage Type
Transition Coverage (Dedicated Valid Transition)

## Covered State(s)
S2 (Bước 2 - Đặt lại mật khẩu), S3 (Đặt lại mật khẩu thành công)

## Covered Transition(s)
T4 (S2 --[A5]--> S3)

## Covered switch sequence, if applicable
Không áp dụng

## Preconditions
- Người dùng chưa đăng nhập.
- Hệ thống đang hiển thị màn hình Bước 2/2 (S2).
- Đã có mã OTP hợp lệ hiển thị trên màn hình (sinh bởi hệ thống cho `test@eshop.com`).

## Test Data
| Parameter | Value |
| --- | --- |
| OTP | Mã OTP 6 chữ số được hiển thị trên màn hình |
| Mật khẩu mới | NewPass123! |
| Xác nhận mật khẩu mới | NewPass123! |

## Test Steps
1. Tại màn hình Bước 2/2 (S2), nhập mã OTP hợp lệ vừa nhận.
2. Nhập Mật khẩu mới `NewPass123!`.
3. Nhập Xác nhận mật khẩu mới `NewPass123!`.
4. Nhấn nút xác nhận để gửi thông tin đặt lại mật khẩu (A5).
5. Quan sát phản hồi của hệ thống.

## Expected Result
- Hệ thống chấp nhận thông tin đầu vào.
- Mật khẩu được cập nhật thành công trong hệ thống.
- Hệ thống hiển thị thông báo đặt lại mật khẩu thành công.
- Workflow hoàn tất, chuyển sang trạng thái kết thúc (S3).
- Trạng thái hệ thống chuyển từ S2 → S3.

## Final State
S3 (Đặt lại mật khẩu thành công)

## Risk Level
High

## Actual Result
API `POST /api/reset-password` trả về HTTP 200 OK và message "Password reset successfully". Đăng nhập lại bằng mật khẩu mới `NewPass123!` thành công (HTTP 200). Transition S2 → S3 hoạt động đúng. **Lưu ý:** mã OTP sử dụng trong quá trình chỉ có 4 chữ số (bug riêng ở T2).

## Status
PASS

## Bug Reference
BUG-FR03-001 (liên quan — OTP dùng trong test là 4 chữ số)
