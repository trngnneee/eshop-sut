## Test Case ID

TC-UC-FORGOT-PASSWORD-007

## Feature

Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference

FR-03, FR-01

## Testing Technique

Use Case Testing

## Test Objective

Xác minh Exception Flow khi hai trường mật khẩu mới không khớp ở bước 2.

## Preconditions

- Guest đã đi đến bước 2 của quy trình quên mật khẩu.
- OTP hợp lệ của phiên hiện tại đã được sinh trước đó.

## Test Data

| Parameter | Value |
|-|-|
| OTP | Mã OTP 6 chữ số hợp lệ |
| New password | NewPass123! |
| Confirm new password | DifferentPass456@ |

## Test Steps

1. Nhập OTP hợp lệ ở bước 2.
2. Nhập mật khẩu mới `NewPass123!`.
3. Nhập xác nhận mật khẩu mới `DifferentPass456@`.
4. Gửi biểu mẫu đặt lại mật khẩu.

## Expected Result

- Hệ thống từ chối yêu cầu vì hai trường mật khẩu không khớp.
- Mật khẩu không được thay đổi.
- Hệ thống vẫn ở bước 2.

## Actual Result

Giao diện Bước 2 không có trường "Xác nhận mật khẩu mới", nên không thể nhập hai mật khẩu khác nhau để kiểm tra lỗi không khớp trên UI.

## Status

FAIL

## Bug Reference

BUG-FR03-005

