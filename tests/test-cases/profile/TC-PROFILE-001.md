# TC-PROFILE-001: Cập nhật hồ sơ cá nhân với thông tin hợp lệ

## Requirement ID
FR-26: Quản lý hồ sơ cá nhân

## Module / Test type / Technique
Profile / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đăng nhập thành công và có JWT token.

## Test data
name: "Nguyen Van A", shipping_address: "123 Duong Le Loi, Q1, HCM", phone: "0912345678"

## Test steps
1. Truy cập giao diện trang Cá nhân (sau khi đăng nhập).
2. Nhập Họ tên hợp lệ "Nguyen Van A" vào ô Họ Tên.
3. Nhập Địa chỉ giao hàng hợp lệ "123 Duong Le Loi, Q1, HCM" vào ô Địa chỉ.
4. Nhập Số điện thoại 10 chữ số hợp lệ "0912345678" vào ô Số điện thoại.
5. Nhấn nút "Cập nhật".

## Expected result
- Trả về HTTP 200 OK. Thông tin name, shipping_address, phone được cập nhật chính xác trong CSDL.

## Status / Related bugs
Fail / [BUG-PROFILE-018](../../bug-reports/BUG-PROFILE-018.md)
