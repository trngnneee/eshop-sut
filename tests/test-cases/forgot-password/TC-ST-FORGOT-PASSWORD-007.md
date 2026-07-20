# TC-ST-FORGOT-PASSWORD-007

## Test Case ID
TC-ST-FORGOT-PASSWORD-007

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03, FR-01

## Testing Technique
State Transition Testing

## Coverage Type
Invalid Transition Coverage

## Covered State(s)
S2 (Bước 2 - Đặt lại mật khẩu)

## Covered Transition(s)
T7 (S2 --[A7]--> S2): Nhập mật khẩu yếu → Báo lỗi, giữ nguyên S2

## Covered switch sequence, if applicable
Không áp dụng

## Preconditions
- Người dùng chưa đăng nhập.
- Hệ thống đang hiển thị màn hình Bước 2/2 (S2).
- Đã có mã OTP hợp lệ hiển thị trên màn hình (sinh cho `test@eshop.com`).

## Test Data
| Parameter | Value |
| --- | --- |
| OTP | Mã OTP 6 chữ số hợp lệ hiển thị trên màn hình |
| Mật khẩu mới (yếu) | abc |
| Xác nhận mật khẩu mới | abc |

## Test Steps
1. Tại màn hình Bước 2/2 (S2), nhập mã OTP hợp lệ.
2. Nhập Mật khẩu mới yếu `abc` (không đáp ứng yêu cầu FR-01: tối thiểu 8 ký tự, 1 chữ hoa, 1 chữ thường, 1 chữ số, 1 ký tự đặc biệt).
3. Nhập Xác nhận mật khẩu mới `abc`.
4. Nhấn nút xác nhận (A7).
5. Quan sát phản hồi của hệ thống.

## Expected Result
- Hệ thống từ chối yêu cầu đặt lại mật khẩu.
- Hệ thống hiển thị thông báo lỗi mật khẩu không đủ mạnh (theo tiêu chuẩn FR-01).
- Mật khẩu **không** được thay đổi.
- Hệ thống **không** chuyển sang trạng thái S3.
- Trạng thái hệ thống vẫn giữ nguyên tại S2.

## Final State
S2 (Bước 2 - Đặt lại mật khẩu)

## Risk Level
Medium

## Actual Result
API `POST /api/reset-password` với mật khẩu mới `abc` (quá ngắn, không đủ mạnh) trả về HTTP **200 OK** và message "Password reset successfully". Backend **chấp nhận mật khẩu yếu** mà không kiểm tra độ mạnh theo tiêu chuẩn FR-01. Điều này cho phép người dùng đặt mật khẩu không an toàn.

## Status
FAIL

## Bug Reference
BUG-FR03-002 — Backend không kiểm tra độ mạnh mật khẩu khi reset
