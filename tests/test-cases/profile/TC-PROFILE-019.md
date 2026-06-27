# TC-PROFILE-019: Cập nhật hồ sơ thất bại do Địa chỉ giao hàng chứa payload SQL Injection

## Requirement ID
FR-26: Quản lý hồ sơ cá nhân

## Module / Test type / Technique
Profile / Security / SQL Injection

## Preconditions
- Người dùng đăng nhập thành công và có JWT token.

## Test data
name: "Nguyen Van A", shipping_address: "' OR 1=1 --", phone: "0912345678"

## Test steps
1. Gửi yêu cầu PUT đến /api/users/me với shipping_address chứa SQL Injection payload.
2. Kiểm tra phản hồi API.
3. Kiểm tra CSDL xem có lỗi cú pháp hoặc bị thay đổi cấu trúc truy vấn không.

## Expected result
- Trả về HTTP 400 Bad Request hoặc xử lý an toàn ngăn chặn câu truy vấn bị chèn phá.

## Status / Related bugs
Fail / [BUG-PROFILE-017](../../bug-reports/BUG-PROFILE-017.md)
