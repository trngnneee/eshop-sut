# TC-ST-FORGOT-PASSWORD-SW1-002

## Test Case ID
TC-ST-FORGOT-PASSWORD-SW1-002

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03

## Testing Technique
State Transition Testing

## Coverage Type
1-switch Coverage

## Covered State(s)
S0 (Trang đăng nhập), S1 (Bước 1 - Yêu cầu OTP)

## Covered Transition(s)
T1 (S0 → S1), T3 (S1 → S0)

## Covered switch sequence, if applicable
SW1-002: T1 → T3 (S0 → S1 → S0)

## Preconditions
- Người dùng chưa đăng nhập.
- Hệ thống đang hiển thị trang đăng nhập (S0).

## Test Data
| Parameter | Value |
| --- | --- |
| Không cần dữ liệu đặc biệt | — |

## Test Steps
1. Tại trang đăng nhập (S0), nhấn nút "Quên mật khẩu" (A1) → Chuyển sang S1.
2. Tại màn hình Bước 1/2 (S1), nhấn nút "Quay lại đăng nhập" (A4) → Chuyển về S0.
3. Quan sát phản hồi của hệ thống sau mỗi bước.

## Expected Result
- Sau bước 1: Hệ thống chuyển sang màn hình Bước 1/2 (S1) với chỉ báo "Bước 1 / 2" và nút quay lại. T1 thực thi thành công.
- Sau bước 2: Hệ thống điều hướng người dùng trở về trang đăng nhập (S0) không có lỗi. T3 thực thi thành công.
- Chuỗi chuyển đổi T1 → T3 hoàn tất.

## Final State
S0 (Trang đăng nhập)

## Risk Level
Low

## Actual Result
Chuỗi T1 → T3 thực hiện được, nhưng ở S1 giao diện không hiển thị chỉ báo bước "Bước 1 / 2" và không có nút "Quay lại đăng nhập" như đặc tả FR-03.

## Status
FAIL

## Bug Reference
BUG-FR03-003 — Không hiển thị chỉ báo bước và nút "Quay lại đăng nhập" ở màn hình nhập email
