# TC-PROFILE-003: Cập nhật hồ sơ thất bại do Họ Tên quá ngắn (1 ký tự)

## Requirement ID
FR-26: Quản lý hồ sơ cá nhân

## Module / Test type / Technique
Profile / Functional / Boundary Value Analysis

## Preconditions
- Người dùng đăng nhập thành công và có JWT token.

## Test data
name: "A", shipping_address: "123 Duong Le Loi, Q1, HCM", phone: "0912345678"

## Test steps
1. Gửi yêu cầu PUT đến /api/users/me với name dài 1 ký tự.
2. Kiểm tra phản hồi API.

## Expected result
- Trả về HTTP 400 Bad Request. Báo lỗi Họ Tên phải có độ dài tối thiểu là 2 ký tự.

## Status / Related bugs
Fail / [BUG-PROFILE-003](../../bug-reports/BUG-PROFILE-003.md)
