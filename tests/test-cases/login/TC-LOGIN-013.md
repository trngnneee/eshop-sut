# TC-LOGIN-013: Kiểm tra tính năng Đăng nhập bên thứ ba (Google OAuth)

## Requirement ID
FR-02

## Module / Test type / Technique
Login / OAuth / Integration Testing

## Preconditions
- Người dùng ở trang Đăng nhập.

## Test data
- Tài khoản Google hợp lệ.

## Test steps
1. Tìm nút bấm Đăng nhập bằng Google trên màn hình đăng nhập.
2. Click chọn và thực hiện luồng đăng nhập của Google.

## Expected result
- Hệ thống tích hợp thành công Google OAuth, cho phép xác thực tài khoản Google và điều hướng về trang chủ EShop với token hợp lệ.

## Status / Related bugs
Failed / #15
