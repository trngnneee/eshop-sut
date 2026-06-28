## BUG-FR10-S-01 - User có thể hủy đơn hàng đang shipping

**GitHub issue title:** `[BUG][FR-10][Order State Machine] User có thể hủy đơn hàng đang shipping`

**GitHub issue:** [#58](https://github.com/trngnneee/eshop-sut/issues/58)

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `FR10-S-TC12`
- Path: `eshop-sut/tests/test-cases/order_state_machine/FR10-S-TC12.md`

## Requirement liên quan

- `FR-10`
- Khi đơn hàng đã ở trạng thái `shipping`, User không được phép tự hủy.
- Mọi chuyển đổi không hợp lệ phải trả về lỗi với thông báo phù hợp.
- Source: `eshop-sut/README.md`

## Severity / Priority

Major / P1

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser**: Brave Browser 149.1.91.178
- **URL**: `http://localhost:3000/api/orders/:id/cancel`
- **Build/Commit**:

## Steps to reproduce

1. Chuẩn bị một đơn hàng thuộc user hiện tại ở trạng thái `shipping`.
2. Đăng nhập bằng tài khoản `user` hợp lệ.
3. Gửi request `PUT /api/orders/:id/cancel` với JWT của user đó.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result

- Hệ thống trả về HTTP 400 với thông báo lỗi phù hợp.
- Trạng thái đơn hàng vẫn giữ nguyên là `shipping`.

## Actual result

- Đơn hàng được chuyển đổi trạng thái sang `canceled`.

## Evidence

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/73444965-2eae-47a7-b5ba-09cf8e47670f" />
