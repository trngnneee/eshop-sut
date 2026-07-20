## Test Case ID

TC-UC-FORGOT-PASSWORD-003

## Feature

Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference

FR-03

## Testing Technique

Use Case Testing

## Test Objective

Xác minh Exception Flow khi Guest nhập email chưa đăng ký ở bước 1.

## Preconditions

- Guest đang ở màn hình bước 1 của quy trình quên mật khẩu.

## Test Data

| Parameter | Value |
|-|-|
| Unregistered email | notfound@eshop.com |

## Test Steps

1. Nhập email `notfound@eshop.com` ở bước 1.
2. Gửi yêu cầu lấy OTP.

## Expected Result

- Hệ thống từ chối yêu cầu.
- Không sinh OTP.
- Hệ thống vẫn ở bước 1.

## Actual Result

Hệ thống từ chối yêu cầu và hiển thị hộp thoại cảnh báo: "Lỗi: User not found". Trạng thái được giữ nguyên ở Bước 1.

## Status

PASS

## Bug Reference

None

