# TC-ST-FORGOT-PASSWORD-006

## Test Case ID
TC-ST-FORGOT-PASSWORD-006

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03

## Testing Technique
State Transition Testing

## Coverage Type
Invalid Transition Coverage

## Covered State(s)
S2 (Bước 2 - Đặt lại mật khẩu)

## Covered Transition(s)
T6 (S2 --[A6]--> S2): Nhập OTP sai → Báo lỗi, giữ nguyên S2

## Covered switch sequence, if applicable
Không áp dụng

## Preconditions
- Người dùng chưa đăng nhập.
- Hệ thống đang hiển thị màn hình Bước 2/2 (S2).
- Đã có mã OTP hợp lệ hiển thị trên màn hình (sinh cho `test@eshop.com`).

## Test Data
| Parameter | Value |
| --- | --- |
| OTP sai | 999999 |
| Mật khẩu mới | NewPass123! |
| Xác nhận mật khẩu mới | NewPass123! |

## Test Steps
1. Tại màn hình Bước 2/2 (S2), nhập OTP sai `999999` (khác với OTP thực tế hiển thị trên màn hình).
2. Nhập Mật khẩu mới `NewPass123!`.
3. Nhập Xác nhận mật khẩu mới `NewPass123!`.
4. Nhấn nút xác nhận (A6).
5. Quan sát phản hồi của hệ thống.

## Expected Result
- Hệ thống từ chối yêu cầu đặt lại mật khẩu.
- Hệ thống hiển thị thông báo lỗi OTP không hợp lệ.
- Mật khẩu **không** được thay đổi.
- Hệ thống **không** chuyển sang trạng thái S3.
- Trạng thái hệ thống vẫn giữ nguyên tại S2.

## Final State
S2 (Bước 2 - Đặt lại mật khẩu)

## Risk Level
High

## Actual Result
API `POST /api/reset-password` với OTP sai `999999` trả về HTTP 400 Bad Request và message `{"error": "Invalid token or email"}`. Mật khẩu không bị thay đổi. Hệ thống giữ nguyên trạng thái S2.

## Status
PASS

## Bug Reference
None
