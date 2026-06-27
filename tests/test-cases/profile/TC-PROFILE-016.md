# TC-PROFILE-016: Cập nhật hồ sơ thất bại khi cố tình tự ý sửa đổi quyền hạn (role)

## Requirement ID
FR-26: Quản lý hồ sơ cá nhân

## Module / Test type / Technique
Profile / Security / Privilege Escalation

## Preconditions
- Người dùng đăng nhập thành công (role='user') và có JWT token.

## Test data
name: "Nguyen Van A", shipping_address: "123 Duong Le Loi, Q1, HCM", phone: "0912345678", role: "admin"

## Test steps
1. Gửi yêu cầu PUT đến /api/users/me mang theo thuộc tính role: 'admin'.
2. Kiểm tra phản hồi API.
3. Kiểm tra trường role của người dùng trong CSDL.

## Expected result
- Hệ thống từ chối cập nhật thuộc tính role của người dùng (giữ nguyên 'user'). Trả về HTTP 400 hoặc bỏ qua thuộc tính role.

## Status / Related bugs
Fail / [BUG-PROFILE-001](../../bug-reports/BUG-PROFILE-001.md)
