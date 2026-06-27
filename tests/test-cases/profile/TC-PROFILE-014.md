# TC-PROFILE-014: Cập nhật hồ sơ thất bại do Số điện thoại chứa khoảng trắng

## Requirement ID
FR-26: Quản lý hồ sơ cá nhân

## Module / Test type / Technique
Profile / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đăng nhập thành công và có JWT token.

## Test data
name: "Nguyen Van A", shipping_address: "123 Duong Le Loi, Q1, HCM", phone: "0912 345 678"

## Test steps
1. Gửi yêu cầu PUT đến /api/users/me với phone chứa khoảng trắng.
2. Kiểm tra phản hồi API.

## Expected result
- Trả về HTTP 400 Bad Request. Báo lỗi Số điện thoại không được chứa khoảng trắng.

## Status / Related bugs
Fail / [BUG-PROFILE-014](../../bug-reports/BUG-PROFILE-014.md)
