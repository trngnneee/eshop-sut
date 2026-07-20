# TC-ST-FORGOT-PASSWORD-003

## Test Case ID
TC-ST-FORGOT-PASSWORD-003

## Feature
Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference
FR-03

## Testing Technique
State Transition Testing

## Coverage Type
Transition Coverage (Dedicated Valid Transition)

## Covered State(s)
S1 (Bước 1 - Yêu cầu OTP), S0 (Trang đăng nhập)

## Covered Transition(s)
T3 (S1 --[A4]--> S0)

## Covered switch sequence, if applicable
Không áp dụng

## Preconditions
- Người dùng chưa đăng nhập.
- Hệ thống đang hiển thị màn hình Bước 1/2 (S1).

## Test Data
| Parameter | Value |
| --- | --- |
| Không cần dữ liệu đặc biệt | — |

## Test Steps
1. Tại màn hình Bước 1/2 (S1), nhấn nút "Quay lại đăng nhập" (A4).
2. Quan sát phản hồi của hệ thống.

## Expected Result
- Hệ thống điều hướng người dùng trở về trang đăng nhập (S0).
- Trang đăng nhập hiển thị đầy đủ các trường Email và Mật khẩu.
- Không có lỗi hoặc cảnh báo nào xuất hiện.
- Trạng thái hệ thống chuyển từ S1 → S0.

## Final State
S0 (Trang đăng nhập)

## Risk Level
Low

## Actual Result
Màn hình Bước 1/2 không hiển thị nút "Quay lại đăng nhập" nên không thể thực hiện hành động như đặc tả FR-03. Đây là lỗi hiển thị của giao diện.

## Status
FAIL

## Bug Reference
BUG-FR03-002 — Không hiển thị nút "Quay lại đăng nhập" ở màn hình nhập email
