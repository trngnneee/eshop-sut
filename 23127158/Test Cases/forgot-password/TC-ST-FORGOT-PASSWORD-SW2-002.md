# TC-ST-FORGOT-PASSWORD-SW2-002

## Test Case ID
TC-ST-FORGOT-PASSWORD-SW2-002

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03

## Testing Technique
State Transition Testing

## Coverage Type
n-switch Coverage (n=2)

## Covered State(s)
S0 (Trang đăng nhập), S1 (Bước 1 - Yêu cầu OTP)

## Covered Transition(s)
T1 (S0 → S1), T3 (S1 → S0), T1 (S0 → S1)

## Covered switch sequence, if applicable
SW2-002: T1 → T3 → T1 (S0 → S1 → S0 → S1)

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
3. Tại trang đăng nhập (S0), nhấn nút "Quên mật khẩu" lần nữa (A1) → Chuyển sang S1.
4. Quan sát phản hồi của hệ thống sau mỗi bước.

## Expected Result
- Sau bước 1: Hệ thống chuyển sang S1. T1 thực thi thành công.
- Sau bước 2: Hệ thống điều hướng về S0. T3 thực thi thành công.
- Sau bước 3: Hệ thống chuyển lại sang S1 thành công, form nhập email hiển thị đúng. T1 thực thi lại thành công.
- Chuỗi T1 → T3 → T1 hoàn tất — xác nhận hệ thống có thể khởi động lại quy trình từ đầu sau khi quay lại.

## Final State
S1 (Bước 1 - Yêu cầu OTP)

## Risk Level
Low

## Actual Result
Chuỗi T1 → T3 → T1 thực hiện được, nhưng các lần hiển thị S1 đều không có chỉ báo bước "Bước 1 / 2" và không có nút "Quay lại đăng nhập" như đặc tả FR-03.

## Status
FAIL

## Bug Reference
BUG-FR03-003 — Không hiển thị chỉ báo bước và nút "Quay lại đăng nhập" ở màn hình nhập email
