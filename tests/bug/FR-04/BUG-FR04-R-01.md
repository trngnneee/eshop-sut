## BUG-FR04-R-01 - API cho phép tự đổi role

**GitHub issue title:** `[BUG][FR-04][Security] API cập nhật hồ sơ cho phép client tự thay đổi role`

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `FR04-R-TC01`
- Path: `eshop-sut/tests/test-cases/profile_management/FR04-R-TC01.md`

## Requirement liên quan

- `FR-04`
- `SEC-06`
- Người dùng không thể tự thay đổi thuộc tính `role`.
- Source: `eshop-sut/README.md`

## Severity / Priority

Critical / P0

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser**: Brave Browser 149.1.91.178 
- **URL**: `http://localhost:3000/api/users/me`
- **Build/Commit**: Latest

## Steps to reproduce

1. Đăng nhập bằng user thường có `role=user`.
2. Gửi request `PUT /api/users/me` kèm JWT của user thường.
3. Trong body gửi các trường hồ sơ hợp lệ và thêm `"role": "admin"`.
4. Gọi lại `GET /api/users/me` hoặc kiểm tra dữ liệu user sau khi cập nhật.

## Expected result

- Hệ thống từ chối hoặc bỏ qua trường `role` từ client.
- Role của user vẫn là `user` và không bị nâng thành `admin`.

## Actual result

- API trả về cập nhật thành công khi body có `role=admin`.

## Evidence

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/e53c7182-6d2b-432d-b391-d80018420637" />
