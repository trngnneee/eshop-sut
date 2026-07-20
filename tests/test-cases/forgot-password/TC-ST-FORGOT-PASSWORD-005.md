# TC-ST-FORGOT-PASSWORD-005

## Test Case ID
TC-ST-FORGOT-PASSWORD-005

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03

## Testing Technique
State Transition Testing

## Coverage Type
Invalid Transition Coverage

## Covered State(s)
S1 (Bước 1 - Yêu cầu OTP)

## Covered Transition(s)
T5 (S1 --[A3]--> S1): Nhập email chưa đăng ký → Giữ nguyên S1

## Covered switch sequence, if applicable
Không áp dụng

## Preconditions
- Người dùng chưa đăng nhập.
- Hệ thống đang hiển thị màn hình Bước 1/2 (S1).
- Email `unregistered@eshop.com` chưa được đăng ký trong hệ thống.

## Test Data
| Parameter | Value |
| --- | --- |
| Email chưa đăng ký | unregistered@eshop.com |

## Test Steps
1. Tại màn hình Bước 1/2 (S1), nhập địa chỉ email chưa đăng ký `unregistered@eshop.com`.
2. Nhấn nút gửi yêu cầu OTP (A3).
3. Quan sát phản hồi của hệ thống.

## Expected Result
- Hệ thống từ chối yêu cầu hoặc hiển thị thông báo lỗi phù hợp.
- Hệ thống **không** sinh mã OTP.
- Hệ thống **không** chuyển sang Bước 2/2 (S2).
- Trạng thái hệ thống vẫn giữ nguyên tại S1.
- **Lưu ý:** Đặc tả không định nghĩa rõ nội dung thông báo lỗi cụ thể cho trường hợp này — *"Đặc tả không định nghĩa quy tắc này."*

## Final State
S1 (Bước 1 - Yêu cầu OTP)

## Risk Level
Medium

## Actual Result
API `POST /api/forgot-password` trả về HTTP 404 Not Found và message `{"error": "User not found"}`. Hệ thống từ chối đúng đắn, không sinh OTP, không chuyển sang Bước 2.

## Status
PASS

## Bug Reference
None
