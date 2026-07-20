# TC-ST-FORGOT-PASSWORD-008

## Test Case ID
TC-ST-FORGOT-PASSWORD-008

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
T8 (S2 --[A8]--> S2): Xác nhận mật khẩu không khớp → Báo lỗi, giữ nguyên S2

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
| Mật khẩu mới | NewPass123! |
| Xác nhận mật khẩu mới (không khớp) | DifferentPass456@ |

## Test Steps
1. Tại màn hình Bước 2/2 (S2), nhập mã OTP hợp lệ.
2. Nhập Mật khẩu mới `NewPass123!`.
3. Nhập Xác nhận mật khẩu mới `DifferentPass456@` (khác với mật khẩu mới ở bước 2).
4. Nhấn nút xác nhận (A8).
5. Quan sát phản hồi của hệ thống.

## Expected Result
- Hệ thống từ chối yêu cầu đặt lại mật khẩu.
- Hệ thống hiển thị thông báo lỗi hai trường mật khẩu không khớp nhau.
- Mật khẩu **không** được thay đổi.
- Hệ thống **không** chuyển sang trạng thái S3.
- Trạng thái hệ thống vẫn giữ nguyên tại S2.

## Final State
S2 (Bước 2 - Đặt lại mật khẩu)

## Risk Level
Medium

## Actual Result
Xác nhận UI: Trường xác nhận mật khẩu không khớp được ngăn chặn nhập tại lớp UI (frontend), không gửi request lên API. Backend không có endpoint kiểm tra điều này nên validation này thuộc phám vi frontend.

## Status
PASS

## Bug Reference
None
