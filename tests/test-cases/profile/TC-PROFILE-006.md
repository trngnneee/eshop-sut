# TC-PROFILE-006: Cập nhật hồ sơ thất bại do Họ Tên chứa ký tự đặc biệt

## Requirement ID
FR-26: Quản lý hồ sơ cá nhân

## Module / Test type / Technique
Profile / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đăng nhập thành công và có JWT token.

## Test data
name: "Nguyen@Van_A", shipping_address: "123 Duong Le Loi, Q1, HCM", phone: "0912345678"

## Test steps
**Cách 1: Gửi request API:**
1. Gửi yêu cầu PUT đến /api/users/me với name chứa ký tự đặc biệt.
2. Kiểm tra phản hồi API.

**Cách 2: Thực hiện trên giao diện (UI):**
1. Truy cập giao diện trang Cá nhân (sau khi đăng nhập).
2. Nhập các giá trị tương ứng vào ô nhập Họ Tên, Địa chỉ.
3. Nhập số điện thoại hợp lệ vào ô Số điện thoại.
4. Nhấn nút "Cập nhật".

## Expected result
- Trả về HTTP 400 Bad Request. Báo lỗi Họ Tên không hợp lệ (không được chứa ký tự đặc biệt).

## Status / Related bugs
Fail / [BUG-PROFILE-006](../../bug-reports/BUG-PROFILE-006.md)
