# TC-PROFILE-013: Cập nhật hồ sơ thất bại do Số điện thoại chứa ký tự không phải số

## Requirement ID
FR-26: Quản lý hồ sơ cá nhân

## Module / Test type / Technique
Profile / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đăng nhập thành công và có JWT token.

## Test data
name: "Nguyen Van A", shipping_address: "123 Duong Le Loi, Q1, HCM", phone: "091234567a"

## Test steps
1. Gửi yêu cầu PUT đến /api/users/me với phone chứa chữ cái.
2. Kiểm tra phản hồi API.

## Expected result
- Trả về HTTP 400 Bad Request. Báo lỗi Số điện thoại chỉ được chứa các chữ số.

## Status / Related bugs
Fail / [BUG-PROFILE-013](../../bug-reports/BUG-PROFILE-013.md)
