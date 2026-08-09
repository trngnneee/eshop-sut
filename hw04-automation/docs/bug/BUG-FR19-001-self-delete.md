# [BUG][FR-19 Admin User Management] Admin có thể tự xóa tài khoản đang đăng nhập

## Found by Test Case

TC-FR19-07

## Requirement liên quan

FR-19

## Severity / Priority

Critical / P0

## Environment

- **OS**: Windows
- **Browser**: Chromium, Firefox, WebKit
- **URL**: http://localhost:3000/api/admin/users/:id
- **Build/Commit**: Latest

## Steps to reproduce

1. Đăng nhập bằng tài khoản admin.
2. Lấy id của chính admin đang đăng nhập.
3. Gọi `DELETE /api/admin/users/{adminId}` với token của admin đó.
4. Lấy lại danh sách user.

## Expected result

Request tự xóa bị từ chối, ví dụ status `403`, và tài khoản admin vẫn tồn tại.

## Actual result

API trả status `200` cho request tự xóa.

## Link Github Issue
https://github.com/trngnneee/eshop-sut/issues/148#issue-4761415336

