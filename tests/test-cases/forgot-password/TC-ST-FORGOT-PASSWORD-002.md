# TC-ST-FORGOT-PASSWORD-002

## Test Case ID
TC-ST-FORGOT-PASSWORD-002

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03

## Testing Technique
State Transition Testing

## Coverage Type
Transition Coverage (Dedicated Valid Transition)

## Covered State(s)
S1 (Bước 1 - Yêu cầu OTP), S2 (Bước 2 - Đặt lại mật khẩu)

## Covered Transition(s)
T2 (S1 --[A2]--> S2)

## Covered switch sequence, if applicable
Không áp dụng

## Preconditions
- Người dùng chưa đăng nhập.
- Hệ thống đang hiển thị màn hình Bước 1/2 (S1).
- Tài khoản email `test@eshop.com` đã được đăng ký trong hệ thống.

## Test Data
| Parameter | Value |
| --- | --- |
| Email đã đăng ký | test@eshop.com |

## Test Steps
1. Tại màn hình Bước 1/2 (S1), nhập địa chỉ email `test@eshop.com` vào ô nhập email.
2. Nhấn nút gửi yêu cầu OTP (A2).
3. Quan sát phản hồi của hệ thống.

## Expected Result
- Hệ thống sinh mã OTP gồm 6 chữ số ngẫu nhiên.
- Mã OTP được hiển thị trực tiếp trên màn hình (môi trường demo).
- Hệ thống chuyển sang màn hình Bước 2/2 (S2).
- Giao diện hiển thị chỉ báo bước "Bước 2 / 2".
- Giao diện hiển thị các ô nhập: OTP, Mật khẩu mới, Xác nhận mật khẩu mới.
- Trạng thái hệ thống chuyển từ S1 → S2.

## Final State
S2 (Bước 2 - Đặt lại mật khẩu)

## Risk Level
Medium

## Actual Result
API `POST /api/forgot-password` trả về HTTP 200 OK. Tuy nhiên, mã OTP được sinh ra chỉ có **4 chữ số** (ví dụ: `7421`) thay vì **6 chữ số** theo đặc tả FR-03. Hệ thống vẫn chuyển sang Bước 2/2 nhưng OTP không đủ độ dài yêu cầu.

## Status
FAIL

## Bug Reference
BUG-FR03-001 — OTP sinh ra 4 chữ số thay vì 6 chữ số
