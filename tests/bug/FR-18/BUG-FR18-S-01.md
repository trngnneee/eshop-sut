## BUG-FR18-S-01 - Admin có thể chuyển final state canceled sang delivered

**GitHub issue title:** `[BUG][FR-18][Admin Order Management] Admin có thể chuyển final state canceled sang delivered`

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `FR18-S-TC11`
- Path: `eshop-sut/tests/test-cases/admin_order_management/FR18-S-TC11.md`

## Requirement liên quan

- `FR-18`
- Admin chỉ được chuyển đổi trạng thái đơn hàng theo đúng State Machine đã định nghĩa ở `FR-10`.
- Trạng thái `delivered` và `canceled` là trạng thái kết thúc, không được phép chuyển sang trạng thái khác.
- Source: `eshop-sut/README.md`

## Severity / Priority

Major / P1

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser**: Brave Browser 149.1.91.178
- **URL**: `http://localhost:3000/api/admin/orders/:id/status`
- **Build/Commit**: Latest

## Steps to reproduce

1. Chuẩn bị một đơn hàng đang ở trạng thái `canceled`.
2. Đăng nhập bằng tài khoản `admin` hợp lệ.
3. Gửi request `PUT /api/admin/orders/:id/status` với body `{"status": "delivered"}`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result

- Hệ thống trả về HTTP 400 với thông báo lỗi phù hợp.
- Trạng thái đơn hàng vẫn giữ nguyên là `canceled`.

## Actual result

- Đơn hàng được chuyển đổi trạng thái sang `delivered`.

## Evidence

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/cd2c14bd-287b-4201-8027-271c077185bb" />
