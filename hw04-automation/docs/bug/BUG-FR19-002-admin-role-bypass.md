# [BUG][FR-19 Admin User Management] User thường có token hợp lệ gọi được Admin API

## Found by Test Case

TC-FR19-10, TC-FR19-11

## Requirement liên quan

FR-12, FR-19, SEC-03

## Severity / Priority

Critical / P0

## Environment

- **OS**: Windows
- **Browser**: Chromium, Firefox, WebKit
- **URL**: http://localhost:3000/api/admin/users
- **Build/Commit**: Latest

## Steps to reproduce

1. Tạo hoặc đăng nhập một user thường có `role = user`.
2. Gọi `GET /api/admin/users` bằng token của user thường.
3. Gọi `DELETE /api/admin/users/{targetId}` bằng token của user thường.

## Expected result

Các Admin API phải kiểm tra `role = admin`; user thường bị từ chối với status `403` và không xem/xóa được user.

## Actual result

`GET /api/admin/users` trả status `200` cho user thường. `DELETE /api/admin/users/{targetId}` cũng trả status `200`, cho phép user thường xóa user khác.

## Link Github Issue
- https://github.com/trngnneee/eshop-sut/issues/147#issue-4761377756

- https://github.com/trngnneee/eshop-sut/issues/152#issue-4762394237
