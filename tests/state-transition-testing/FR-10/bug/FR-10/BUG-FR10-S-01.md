## BUG-FR10-S-01 - User có thể hủy đơn hàng đang shipping

**GitHub issue title:** `[BUG][FR-10][Order State Machine] User có thể hủy đơn hàng đang shipping`

**GitHub issue:** [TBD]

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `FR10-S-TC12`
- Path: `eshop-sut/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC12.md`

## Requirement liên quan

- `FR-10`
- User không được phép tự hủy khi đơn ở `shipping`; invalid transition phải bị từ chối và giữ nguyên state.
- Source: `eshop-sut/README.md:141-162`

## Severity / Priority

Major / P1

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser**: API client / source-level UI check
- **URL**: `/api/orders/:id/cancel`
- **Build/Commit**:

## Steps to reproduce

1. Chuẩn bị fixture/order đúng precondition của `FR10-S-TC12`.
2. Đăng nhập đúng actor hoặc mở/kiểm tra đúng interface theo test case.
3. Thực hiện action trong test case.
4. Đọc lại response/UI condition và trạng thái đơn hàng sau action.

## Expected result

- HTTP lỗi và trạng thái đơn hàng vẫn là `shipping`.

## Actual result

- Expected HTTP lỗi và status giữ `shipping`, actual HTTP 200, final status `canceled`, response `{'message': 'Order canceled successfully'}`.

## Evidence

[Evidence bổ sung sau.]
