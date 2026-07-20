# TC-ST-FORGOT-PASSWORD-SW2-003

## Test Case ID
TC-ST-FORGOT-PASSWORD-SW2-003

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03, FR-01

## Testing Technique
State Transition Testing

## Coverage Type
n-switch Coverage (n=2)

## Covered State(s)
S1 (Bước 1 - Yêu cầu OTP), S0 (Trang đăng nhập), S2 (Bước 2 - Đặt lại mật khẩu)

## Covered Transition(s)
T3 (S1 → S0), T1 (S0 → S1), T2 (S1 → S2)

## Covered switch sequence, if applicable
SW2-003: T3 → T1 → T2 (S1 → S0 → S1 → S2)

## Preconditions
- Người dùng chưa đăng nhập.
- Hệ thống đang hiển thị màn hình Bước 1/2 (S1).
- Tài khoản `test@eshop.com` đã được đăng ký trong hệ thống.

## Test Data
| Parameter | Value |
| --- | --- |
| Email đã đăng ký | test@eshop.com |

## Test Steps
1. Tại màn hình Bước 1/2 (S1), nhấn nút "Quay lại đăng nhập" (A4) → Chuyển về S0.
2. Tại trang đăng nhập (S0), nhấn nút "Quên mật khẩu" (A1) → Chuyển sang S1.
3. Tại màn hình Bước 1/2 (S1), nhập email `test@eshop.com` và nhấn gửi yêu cầu OTP (A2) → Chuyển sang S2.
4. Quan sát phản hồi của hệ thống sau mỗi bước.

## Expected Result
- Sau bước 1: Hệ thống điều hướng về S0. T3 thực thi thành công.
- Sau bước 2: Hệ thống chuyển sang S1. T1 thực thi thành công.
- Sau bước 3: Hệ thống sinh OTP 6 chữ số và chuyển sang S2. T2 thực thi thành công.
- Chuỗi T3 → T1 → T2 hoàn tất — xác nhận người dùng có thể quay lại rồi tiếp tục thực hiện quy trình.

## Final State
S2 (Bước 2 - Đặt lại mật khẩu)

## Risk Level
Medium

## Actual Result
Chuỗi T3 → T1 → T2: Transitions T3 và T1 hoạt động đúng. Transition T2 gập bug: OTP sinh ra chỉ có **4 chữ số**. Chuỗi 2-switch không đạt chuẩn do OTP không đúng đặc tả tại T2.

## Status
FAIL

## Bug Reference
BUG-FR03-001 — OTP sinh ra 4 chữ số thay vì 6 chữ số
