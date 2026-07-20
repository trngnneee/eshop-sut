# TC-ST-FORGOT-PASSWORD-009

## Test Case ID
TC-ST-FORGOT-PASSWORD-009

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
T9 (S2 --[A9]--> S2): Dùng OTP của email khác → Báo lỗi, giữ nguyên S2

## Covered switch sequence, if applicable
Không áp dụng

## Preconditions
- Người dùng chưa đăng nhập.
- Hệ thống đang hiển thị màn hình Bước 2/2 (S2) sau khi yêu cầu OTP cho `test@eshop.com`.
- Tài khoản `other@eshop.com` cũng đã đăng ký trong hệ thống.
- Đã có mã OTP_B được sinh từ một phiên khác cho email `other@eshop.com`.

## Test Data
| Parameter | Value |
| --- | --- |
| OTP (thuộc email khác — OTP_B) | Mã OTP 6 chữ số hợp lệ của other@eshop.com |
| Mật khẩu mới | NewPass123! |
| Xác nhận mật khẩu mới | NewPass123! |

## Test Steps
1. Tại màn hình Bước 2/2 (S2) — đang trong phiên quên mật khẩu của `test@eshop.com`.
2. Nhập OTP_B (mã OTP hợp lệ được sinh cho `other@eshop.com`).
3. Nhập Mật khẩu mới `NewPass123!`.
4. Nhập Xác nhận mật khẩu mới `NewPass123!`.
5. Nhấn nút xác nhận (A9).
6. Quan sát phản hồi của hệ thống.

## Expected Result
- Hệ thống từ chối yêu cầu đặt lại mật khẩu.
- Hệ thống hiển thị thông báo lỗi OTP không hợp lệ hoặc không khớp với email đang thực hiện thao tác.
- Mật khẩu của `test@eshop.com` **không** được thay đổi.
- Hệ thống **không** chuyển sang trạng thái S3.
- Trạng thái hệ thống vẫn giữ nguyên tại S2.

## Final State
S2 (Bước 2 - Đặt lại mật khẩu)

## Risk Level
High

## Actual Result
API `POST /api/reset-password` với OTP_B (của `another@test.com`) để reset mật khẩu `test@eshop.com` trả về HTTP 400 Bad Request và message `{"error": "Invalid token or email"}`. Hệ thống từ chối, mật khẩu của `test@eshop.com` không bị thay đổi.

## Status
PASS

## Bug Reference
None
