# TC-PROFILE-012: Cập nhật hồ sơ thất bại do Số điện thoại dài hơn 11 chữ số (12 chữ số)

## Requirement ID
FR-26: Quản lý hồ sơ cá nhân

## Module / Test type / Technique
Profile / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đăng nhập thành công và có JWT token.

## Test data
name: "Nguyen Van A", shipping_address: "123 Duong Le Loi, Q1, HCM", phone: "091234567890"

## Test steps
1. Gửi yêu cầu PUT đến /api/users/me với phone có 12 chữ số.
2. Kiểm tra phản hồi API.

## Expected result
- Trả về HTTP 400 Bad Request. Báo lỗi Số điện thoại phải từ 10-11 chữ số.

## Status / Related bugs
Fail / [BUG-PROFILE-012](../../bug-reports/BUG-PROFILE-012.md)
