# TC-PROFILE-018: Cập nhật hồ sơ thất bại do Địa chỉ giao hàng chứa mã độc Stored XSS

## Requirement ID
FR-26: Quản lý hồ sơ cá nhân

## Module / Test type / Technique
Profile / Security / Stored XSS

## Preconditions
- Người dùng đăng nhập thành công và có JWT token.

## Test data
name: "Nguyen Van A", shipping_address: "<script>alert('XSS_addr')</script>", phone: "0912345678"

## Test steps
1. Gửi yêu cầu PUT đến /api/users/me với shipping_address chứa mã script.
2. Kiểm tra phản hồi API.
3. Kiểm tra xem script có được lưu thô vào CSDL hay không.

## Expected result
- Trả về HTTP 400 Bad Request hoặc thực hiện mã hóa HTML Entity an toàn trước khi lưu CSDL.

## Status / Related bugs
Fail / [BUG-PROFILE-016](../../bug-reports/BUG-PROFILE-016.md)
