# TC-ST-FORGOT-PASSWORD-SW2-001

## Test Case ID
TC-ST-FORGOT-PASSWORD-SW2-001

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03, FR-01

## Testing Technique
State Transition Testing

## Coverage Type
n-switch Coverage (n=2)

## Covered State(s)
S0 (Trang đăng nhập), S1 (Bước 1 - Yêu cầu OTP), S2 (Bước 2 - Đặt lại mật khẩu), S3 (Đặt lại mật khẩu thành công)

## Covered Transition(s)
T1 (S0 → S1), T2 (S1 → S2), T4 (S2 → S3)

## Covered switch sequence, if applicable
SW2-001: T1 → T2 → T4 (S0 → S1 → S2 → S3)

## Preconditions
- Người dùng chưa đăng nhập.
- Hệ thống đang hiển thị trang đăng nhập (S0).
- Tài khoản `test@eshop.com` đã được đăng ký trong hệ thống.

## Test Data
| Parameter | Value |
| --- | --- |
| Email đã đăng ký | test@eshop.com |
| OTP | Mã OTP 6 chữ số hiển thị trên màn hình |
| Mật khẩu mới | NewPass123! |
| Xác nhận mật khẩu mới | NewPass123! |

## Test Steps
1. Tại trang đăng nhập (S0), nhấn nút "Quên mật khẩu" (A1) → Chuyển sang S1.
2. Tại màn hình Bước 1/2 (S1), nhập email `test@eshop.com` và nhấn gửi yêu cầu OTP (A2) → Chuyển sang S2. Ghi lại mã OTP hiển thị.
3. Tại màn hình Bước 2/2 (S2), nhập OTP hợp lệ, Mật khẩu mới `NewPass123!`, Xác nhận `NewPass123!`, và nhấn xác nhận (A5) → Chuyển sang S3.
4. Quan sát phản hồi của hệ thống sau mỗi bước.

## Expected Result
- Sau bước 1: Hệ thống chuyển sang S1. T1 thực thi thành công.
- Sau bước 2: Hệ thống sinh OTP 6 chữ số và chuyển sang S2. T2 thực thi thành công.
- Sau bước 3: Hệ thống đặt lại mật khẩu thành công và chuyển sang trạng thái kết thúc S3. T4 thực thi thành công.
- Chuỗi chuyển đổi 3 bước T1 → T2 → T4 hoàn tất không có lỗi.

## Final State
S3 (Đặt lại mật khẩu thành công)

## Risk Level
High

## Actual Result
Chuỗi T1 → T2 → T4: Transitions T1 và T4 hoạt động đúng. Transition T2 gập bug: OTP sinh ra chỉ có **4 chữ số**. Chuỗi 2-switch không đạt chuẩn do OTP không đúng đặc tả tại T2.

## Status
FAIL

## Bug Reference
BUG-FR03-001 — OTP sinh ra 4 chữ số thay vì 6 chữ số
