# TC-ST-FORGOT-PASSWORD-SW2-004

## Test Case ID
TC-ST-FORGOT-PASSWORD-SW2-004

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03

## Testing Technique
State Transition Testing

## Coverage Type
n-switch Coverage (n=2)

## Covered State(s)
S1 (Bước 1 - Yêu cầu OTP), S0 (Trang đăng nhập)

## Covered Transition(s)
T3 (S1 → S0), T1 (S0 → S1), T3 (S1 → S0)

## Covered switch sequence, if applicable
SW2-004: T3 → T1 → T3 (S1 → S0 → S1 → S0)

## Preconditions
- Người dùng chưa đăng nhập.
- Hệ thống đang hiển thị màn hình Bước 1/2 (S1).

## Test Data
| Parameter | Value |
| --- | --- |
| Không cần dữ liệu đặc biệt | — |

## Test Steps
1. Tại màn hình Bước 1/2 (S1), nhấn nút "Quay lại đăng nhập" (A4) → Chuyển về S0.
2. Tại trang đăng nhập (S0), nhấn nút "Quên mật khẩu" (A1) → Chuyển sang S1.
3. Tại màn hình Bước 1/2 (S1), nhấn nút "Quay lại đăng nhập" (A4) → Chuyển về S0 lần nữa.
4. Quan sát phản hồi của hệ thống sau mỗi bước.

## Expected Result
- Sau bước 1: Hệ thống điều hướng về S0. T3 thực thi thành công.
- Sau bước 2: Hệ thống chuyển sang S1. T1 thực thi thành công.
- Sau bước 3: Hệ thống điều hướng về S0 lần nữa, không gặp lỗi. T3 thực thi lại thành công.
- Chuỗi T3 → T1 → T3 hoàn tất — xác nhận hệ thống xử lý đúng vòng lặp quay lại nhiều lần.

## Final State
S0 (Trang đăng nhập)

## Risk Level
Low

## Actual Result
Chuỗi T3 → T1 → T3 thực hiện được, nhưng mỗi lần quay lại S1 giao diện không hiển thị chỉ báo bước "Bước 1 / 2" và không có nút "Quay lại đăng nhập" như đặc tả FR-03.

## Status
FAIL

## Bug Reference
BUG-FR03-003 — Không hiển thị chỉ báo bước và nút "Quay lại đăng nhập" ở màn hình nhập email
