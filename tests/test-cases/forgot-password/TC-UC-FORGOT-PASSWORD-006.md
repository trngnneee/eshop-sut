## Test Case ID

TC-UC-FORGOT-PASSWORD-006

## Feature

Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference

FR-03, FR-01

## Testing Technique

Use Case Testing

## Test Objective

Xác minh Exception Flow khi Guest nhập mật khẩu mới không đủ mạnh ở bước 2.

## Preconditions

- Guest đã đi đến bước 2 của quy trình quên mật khẩu.
- OTP hợp lệ của phiên hiện tại đã được sinh trước đó.

## Test Data

| Parameter | Value |
|-|-|
| OTP | Mã OTP 6 chữ số hợp lệ |
| Weak password | abc |
| Confirm new password | abc |

## Test Steps

1. Nhập OTP hợp lệ ở bước 2.
2. Nhập mật khẩu mới yếu `abc`.
3. Nhập xác nhận mật khẩu mới `abc`.
4. Gửi biểu mẫu đặt lại mật khẩu.

## Expected Result

- Hệ thống từ chối yêu cầu vì mật khẩu không đủ mạnh theo FR-01.
- Mật khẩu không được thay đổi.
- Hệ thống vẫn ở bước 2.

## Actual Result

Hệ thống từ chối yêu cầu và hiển thị hộp thoại alert: "Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT.", giữ nguyên trạng thái ở Bước 2. Mật khẩu không thay đổi.

## Status

PASS

## Bug Reference

None

