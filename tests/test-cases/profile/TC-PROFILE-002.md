# TC-PROFILE-002: Cập nhật hồ sơ thất bại do Họ Tên rỗng

## Requirement ID
FR-26: Quản lý hồ sơ cá nhân

## Module / Test type / Technique
Profile / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đăng nhập thành công và có JWT token.

## Test data
name: "", shipping_address: "123 Duong Le Loi, Q1, HCM", phone: "0912345678"

## Test steps
**Cách 1: Gửi request API:**
1. Gửi yêu cầu PUT đến /api/users/me với name rỗng.
2. Kiểm tra phản hồi API.

**Cách 2: Thực hiện trên giao diện (UI):**
1. Truy cập giao diện trang Cá nhân (sau khi đăng nhập).
2. Nhập các giá trị tương ứng vào ô nhập Họ Tên, Địa chỉ.
3. Nhập số điện thoại hợp lệ vào ô Số điện thoại.
4. Nhấn nút "Cập nhật".

## Expected result
- Trả về HTTP 400 Bad Request. Báo lỗi Họ Tên không được phép để trống.

## Status / Related bugs
Fail / [BUG-PROFILE-002](../../bug-reports/BUG-PROFILE-002.md)
