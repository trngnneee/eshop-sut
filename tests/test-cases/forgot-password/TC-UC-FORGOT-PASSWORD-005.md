## Test Case ID

TC-UC-FORGOT-PASSWORD-005

## Feature

Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference

FR-03

## Testing Technique

Use Case Testing

## Test Objective

Xác minh Exception Flow khi Guest dùng OTP thuộc email khác ở bước 2.

## Preconditions

- Guest đã đi đến bước 2 của quy trình quên mật khẩu cho `test@eshop.com`.
- OTP hợp lệ của một email khác đã có sẵn.

## Test Data

| Parameter | Value |
|-|-|
| OTP of other email | OTP 6 chữ số hợp lệ của email khác |
| New password | NewPass123! |
| Confirm new password | NewPass123! |

## Test Steps

1. Nhập OTP hợp lệ nhưng thuộc email khác ở bước 2.
2. Nhập mật khẩu mới `NewPass123!` và xác nhận `NewPass123!`.
3. Gửi biểu mẫu đặt lại mật khẩu.

## Expected Result

- Hệ thống từ chối yêu cầu.
- Mật khẩu của `test@eshop.com` không thay đổi.
- Hệ thống vẫn ở bước 2.

## Actual Result

- Màn hình Bước 2/2 thiếu trường "Xác nhận mật khẩu mới".
- Biểu thức chính quy ở frontend (`flawedStrongPasswordRegex`) bị lỗi (yêu cầu khoảng trắng, cấm ký tự đặc biệt), khiến mật khẩu tiêu chuẩn `NewPass123!` bị chặn ngay tại client với cảnh báo mật khẩu yếu trước khi kiểm tra OTP chéo email.

## Status

FAIL

## Bug Reference

BUG-FR03-004, BUG-FR03-005

