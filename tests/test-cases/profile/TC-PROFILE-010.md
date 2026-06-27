# TC-PROFILE-010: Cập nhật hồ sơ thất bại do Số điện thoại không bắt đầu bằng số 0

## Requirement ID
FR-26: Quản lý hồ sơ cá nhân

## Module / Test type / Technique
Profile / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đăng nhập thành công và có JWT token.

## Test data
name: "Nguyen Van A", shipping_address: "123 Duong Le Loi, Q1, HCM", phone: "1912345678"

## Test steps
1. Truy cập giao diện trang Cá nhân (sau khi đăng nhập).
2. Nhập số điện thoại không bắt đầu bằng số 0 (ví dụ: "1912345678") vào ô Số điện thoại.
3. Nhập Họ tên và Địa chỉ hợp lệ.
4. Nhấn nút "Cập nhật".

## Expected result
- Trả về HTTP 400 Bad Request. Báo lỗi Số điện thoại không hợp lệ (phải bắt đầu bằng số 0).

## Status / Related bugs
Fail / [BUG-PROFILE-010](../../bug-reports/BUG-PROFILE-010.md)
