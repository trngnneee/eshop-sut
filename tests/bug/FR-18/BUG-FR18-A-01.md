## BUG-FR18-A-01 - API Admin không kiểm tra role admin

**GitHub issue title:** `[BUG][FR-18][Security] API Admin không kiểm tra role admin khi quản lý đơn hàng`

**Labels:** `type: bug`, `status: new`, `found-by: test-case`, `security`

## Found by Test Case

- `FR18-A-TC01`
- `FR18-A-TC03`
- Paths:
  - `eshop-sut/tests/test-cases/admin_order_management/FR18-A-TC01.md`
  - `eshop-sut/tests/test-cases/admin_order_management/FR18-A-TC03.md`

## Requirement liên quan

- `FR-18`
- Admin xem toàn bộ đơn hàng của tất cả người dùng.
- Admin có thể chuyển đổi trạng thái đơn hàng theo đúng State Machine đã định nghĩa ở `FR-10`.
- `SEC-03`: API Admin phải kiểm tra `role = 'admin'` trong Token, không chỉ kiểm tra sự tồn tại của Token.
- Source: `eshop-sut/README.md`
- Source: `eshop-sut/api_specification.md`

## Severity / Priority

Critical / P0

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser**: Brave Browser 149.1.91.178
- **URL**: `http://localhost:3000/api/admin/orders`, `http://localhost:3000/api/admin/orders/:id/status`
- **Build/Commit**: Latest

## Steps to reproduce

1. Đăng nhập bằng tài khoản user thường có JWT hợp lệ với `role = user`.
2. Gửi request `GET /api/admin/orders` với token của user thường.
3. Gửi request `PUT /api/admin/orders/:id/status` với token của user thường và body `{"status": "confirmed"}`.
4. Kiểm tra response và trạng thái đơn hàng sau request.

## Expected result

- Hệ thống trả về HTTP 403 hoặc lỗi quyền truy cập phù hợp cho user không có quyền admin.
- Response không chứa danh sách đơn hàng toàn hệ thống.
- Trạng thái đơn hàng không bị cập nhật bởi user thường.

## Actual result

- API trả về danh sách đơn hàng khi user thường gọi `GET /api/admin/orders`.
- API cập nhật trạng thái đơn hàng thành công khi user thường gọi `PUT /api/admin/orders/:id/status`.

## Evidence
- User có thể lấy ra danh sách đơn hàng:
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/bbce6f07-d0f2-414e-b003-b54a55525761" />
- Trạng thái đơn hàng được cập nhật bởi User: 
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/bd969d02-db72-43af-870b-7a49726fa9c3" />
