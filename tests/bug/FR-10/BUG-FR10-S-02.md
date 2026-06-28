## BUG-FR10-S-02 - Admin có thể chuyển final state canceled sang delivered

**GitHub issue title:** `[BUG][FR-10][Order State Machine] Admin có thể chuyển final state canceled sang delivered`

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `FR10-S-TC16`
- Path: `eshop-sut/tests/test-cases/order_state_machine/FR10-S-TC16.md`

## Requirement liên quan

- `FR-10`
- Trạng thái `delivered` và `canceled` là trạng thái kết thúc, không được phép chuyển sang bất kỳ trạng thái nào khác.
- Mọi chuyển đổi không hợp lệ phải trả về lỗi với thông báo phù hợp.
- Source: `eshop-sut/README.md`

## Severity / Priority

Major / P1

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser**: Brave Browser 149.1.91.178
- **URL**: `http://localhost:3000/api/admin/orders/:id/status`
- **Build/Commit**:

## Steps to reproduce

1. Chuẩn bị một đơn hàng ở trạng thái `canceled`.
2. Đăng nhập bằng tài khoản `admin` hợp lệ.
3. Gửi request `PUT /api/admin/orders/:id/status` với body `{"status": "delivered"}`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result

- Hệ thống trả về HTTP 400 với thông báo lỗi phù hợp.
- Trạng thái đơn hàng vẫn giữ nguyên là `canceled`.

## Actual result

- Đơn hàng được chuyển đổi trạng thái sang `delivered`.

## Evidence

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/0c059989-b0b6-42b8-b539-a5f54abafae9" />
