# TC-PROFILE-015: Cập nhật hồ sơ thất bại do Địa chỉ giao hàng trống

## Requirement ID
FR-26: Quản lý hồ sơ cá nhân

## Module / Test type / Technique
Profile / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đăng nhập thành công và có JWT token.

## Test data
name: "Nguyen Van A", shipping_address: "", phone: "0912345678"

## Test steps
1. Gửi yêu cầu PUT đến /api/users/me với shipping_address rỗng.
2. Kiểm tra phản hồi API.

## Expected result
- Trả về HTTP 400 Bad Request. Báo lỗi Địa chỉ giao hàng không được để trống.

## Status / Related bugs
Fail / [BUG-PROFILE-015](../../bug-reports/BUG-PROFILE-015.md)
