## Test Case ID

TC-UC-FORGOT-PASSWORD-001

## Feature

Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference

FR-03

## Testing Technique

Use Case Testing

## Test Objective

Xác minh Main Flow của Use Case Quên mật khẩu & Đặt lại mật khẩu từ lúc mở chức năng đến khi đặt lại mật khẩu thành công.

## Preconditions

- Guest đang ở màn hình đăng nhập.
- Email `test@eshop.com` đã được đăng ký.

## Test Data

| Parameter | Value |
|-|-|
| Registered email | test@eshop.com |
| OTP | Mã OTP 6 chữ số hiển thị trực tiếp trong demo |
| New password | NewPass123! |
| Confirm new password | NewPass123! |

## Test Steps

1. Chọn chức năng Quên mật khẩu.
2. Quan sát màn hình bước 1 và xác nhận có step indicator "Bước 1 / 2" cùng nút Quay lại đăng nhập.
3. Nhập email `test@eshop.com` và gửi yêu cầu.
4. Ghi nhận OTP 6 chữ số do hệ thống sinh ra.
5. Nhập OTP hợp lệ, mật khẩu mới `NewPass123!`, và xác nhận `NewPass123!`.
6. Gửi biểu mẫu đặt lại mật khẩu.

## Expected Result

- Hệ thống mở luồng khôi phục mật khẩu thành công.
- Bước 1 hiển thị đúng step indicator và nút Quay lại đăng nhập.
- Hệ thống sinh OTP 6 chữ số và chuyển sang bước 2.
- Hệ thống chấp nhận OTP hợp lệ và mật khẩu mới hợp lệ.
- Mật khẩu được cập nhật thành công.

## Actual Result

- Màn hình Bước 1 không hiển thị chỉ báo bước "Bước 1 / 2" và thiếu nút "Quay lại đăng nhập".
- Màn hình Bước 2 thiếu trường "Xác nhận mật khẩu mới".
- Biểu thức chính quy ở frontend (`flawedStrongPasswordRegex`) bị sai (yêu cầu khoảng trắng, không cho phép ký tự đặc biệt), khiến mật khẩu mạnh hợp lệ `NewPass123!` bị chặn lại với cảnh báo mật khẩu yếu.
- OTP nhận được từ hệ thống chỉ gồm 4 chữ số thay vì 6 chữ số.

## Status

FAIL

## Bug Reference

BUG-FR03-001, BUG-FR03-003, BUG-FR03-004, BUG-FR03-005

