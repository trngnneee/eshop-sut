# TC-PROFILE-017: Cố gắng thay đổi trường email của hồ sơ cá nhân

## Requirement ID
FR-26: Quản lý hồ sơ cá nhân

## Module / Test type / Technique
Profile / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đăng nhập thành công và có JWT token.

## Test data
name: "Nguyen Van A", shipping_address: "123 Duong Le Loi, Q1, HCM", phone: "0912345678", email: "new_email@eshop.com"

## Test steps
1. Gửi yêu cầu PUT đến /api/users/me chứa email mới.
2. Kiểm tra phản hồi API.
3. Kiểm tra trường email trong CSDL xem có bị thay đổi không.

## Expected result
- Hệ thống bỏ qua thuộc tính email (không cho phép thay đổi email qua giao diện) hoặc trả về lỗi. Email trong CSDL giữ nguyên.

## Status / Related bugs
Pass / None
