# TC-ST-FORGOT-PASSWORD-SW1-001

## Test Case ID
TC-ST-FORGOT-PASSWORD-SW1-001

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03

## Testing Technique
State Transition Testing

## Coverage Type
1-switch Coverage

## Covered State(s)
S0 (Trang đăng nhập), S1 (Bước 1 - Yêu cầu OTP), S2 (Bước 2 - Đặt lại mật khẩu)

## Covered Transition(s)
T1 (S0 → S1), T2 (S1 → S2)

## Covered switch sequence, if applicable
SW1-001: T1 → T2 (S0 → S1 → S2)

## Preconditions
- Người dùng chưa đăng nhập.
- Hệ thống đang hiển thị trang đăng nhập (S0).
- Tài khoản `test@eshop.com` đã được đăng ký trong hệ thống.

## Test Data
| Parameter | Value |
| --- | --- |
| Email đã đăng ký | test@eshop.com |

## Test Steps
1. Tại trang đăng nhập (S0), nhấn nút "Quên mật khẩu" (A1) → Chuyển sang S1.
2. Tại màn hình Bước 1/2 (S1), nhập email `test@eshop.com` và nhấn gửi yêu cầu OTP (A2) → Chuyển sang S2.
3. Quan sát phản hồi của hệ thống sau mỗi bước.

## Expected Result
- Sau bước 1: Hệ thống chuyển sang màn hình Bước 1/2 (S1) với chỉ báo bước và nút quay lại. T1 thực thi thành công.
- Sau bước 2: Hệ thống sinh mã OTP 6 chữ số và chuyển sang màn hình Bước 2/2 (S2). T2 thực thi thành công.
- Chuỗi chuyển đổi T1 → T2 hoàn tất không có lỗi.

## Final State
S2 (Bước 2 - Đặt lại mật khẩu)

## Risk Level
Medium

## Actual Result
Chuỗi T1 → T2: Transition T1 thành công (chuyển sang S1). Transition T2 gập lỗi: OTP được sinh ra chỉ có **4 chữ số** thay vì 6 chữ số theo yêu cầu. Chuỗi 1-switch không đạt chuẩn do bug tại T2.

## Status
FAIL

## Bug Reference
BUG-FR03-001 — OTP sinh ra 4 chữ số thay vì 6 chữ số
