## Test Case ID

TC-UC-FORGOT-PASSWORD-002

## Feature

Quên mật khẩu & Đặt lại mật khẩu (FR-03)

## Requirement Reference

FR-03

## Testing Technique

Use Case Testing

## Test Objective

Xác minh Alternative Flow khi Guest quay lại đăng nhập từ bước nhập email.

## Preconditions

- Guest đang ở màn hình bước 1 của quy trình quên mật khẩu.

## Test Data

| Parameter | Value |
|-|-|
| Input | Không cần dữ liệu đặc biệt |

## Test Steps

1. Quan sát màn hình bước 1 của quy trình quên mật khẩu.
2. Nhấn nút Quay lại đăng nhập.

## Expected Result

- Hệ thống quay về màn hình đăng nhập.
- Không sinh OTP.
- Quy trình quên mật khẩu kết thúc.

## Actual Result

Màn hình nhập email (Bước 1) không hiển thị nút "Quay lại đăng nhập", do đó người dùng không thể thực hiện thao tác này.

## Status

FAIL

## Bug Reference

BUG-FR03-003

