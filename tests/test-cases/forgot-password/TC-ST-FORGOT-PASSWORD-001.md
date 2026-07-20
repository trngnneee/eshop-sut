# TC-ST-FORGOT-PASSWORD-001

## Test Case ID
TC-ST-FORGOT-PASSWORD-001

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03

## Testing Technique
State Transition Testing

## Coverage Type
Transition Coverage (Dedicated Valid Transition)

## Covered State(s)
S0 (Trang đăng nhập), S1 (Bước 1 - Yêu cầu OTP)

## Covered Transition(s)
T1 (S0 --[A1]--> S1)

## Covered switch sequence, if applicable
Không áp dụng

## Preconditions
- Người dùng chưa đăng nhập.
- Hệ thống đang hiển thị trang đăng nhập (S0).

## Test Data
| Parameter | Value |
| --- | --- |
| Không cần dữ liệu đặc biệt | — |

## Test Steps
1. Truy cập trang đăng nhập (S0).
2. Nhấn vào liên kết hoặc nút "Quên mật khẩu" (A1).
3. Quan sát màn hình sau khi thực hiện hành động.

## Expected Result
- Hệ thống chuyển sang màn hình Bước 1/2 (S1).
- Giao diện hiển thị ô nhập địa chỉ email.
- Giao diện hiển thị chỉ báo bước "Bước 1 / 2".
- Giao diện hiển thị nút "Quay lại đăng nhập".
- Trạng thái hệ thống chuyển từ S0 → S1.

## Final State
S1 (Bước 1 - Yêu cầu OTP)

## Risk Level
Low

## Actual Result
Giao diện điều hướng từ trang đăng nhập sang màn hình Bước 1/2 thành công, nhưng màn hình nhập email không hiển thị chỉ báo bước "Bước 1 / 2" và cũng không có nút "Quay lại đăng nhập" như đặc tả FR-03.

## Status
FAIL

## Bug Reference
BUG-FR03-003: Không hiển thị chỉ báo bước và nút "Quay lại đăng nhập" ở màn hình nhập email 
