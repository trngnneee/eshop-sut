## Test Case ID

TC-UC-FORGOT-PASSWORD-004

## Feature

Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference

FR-03

## Testing Technique

Use Case Testing

## Test Objective

Xác minh Exception Flow khi Guest nhập OTP không hợp lệ ở bước 2.

## Preconditions

- Guest đã đi đến bước 2 của quy trình quên mật khẩu.
- OTP hợp lệ của phiên hiện tại đã được sinh trước đó.

## Test Data

| Parameter | Value |
|-|-|
| Invalid OTP | 123456 |
| New password | NewPass123! |
| Confirm new password | NewPass123! |

## Test Steps

1. Nhập OTP không hợp lệ `123456` ở bước 2.
2. Nhập mật khẩu mới `NewPass123!` và xác nhận `NewPass123!`.
3. Gửi biểu mẫu đặt lại mật khẩu.

## Expected Result

- Hệ thống từ chối yêu cầu.
- Mật khẩu không được thay đổi.
- Hệ thống vẫn ở bước 2.

## Actual Result

- Màn hình Bước 2/2 thiếu trường "Xác nhận mật khẩu mới".
- Biểu thức chính quy ở frontend (`flawedStrongPasswordRegex`) bị lỗi (yêu cầu khoảng trắng, cấm ký tự đặc biệt), khiến mật khẩu tiêu chuẩn `NewPass123!` bị chặn ngay tại client với cảnh báo mật khẩu yếu trước khi kiểm tra OTP sai.

## Status

FAIL

## Bug Reference

BUG-FR03-004, BUG-FR03-005

