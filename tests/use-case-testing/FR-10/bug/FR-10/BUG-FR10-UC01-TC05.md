## BUG-FR10-UC01-TC05 - Admin API cho phép chuyển final state canceled sang delivered

**GitHub issue title:** `[BUG][FR-10][Order State Machine] Admin API cho phép chuyển final state canceled sang delivered`

**GitHub issue:** [TBD]

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `FR10-UC01-TC05`
- Path: `eshop-sut/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC01-TC05.md`

## Requirement liên quan

- `FR-10`
- `canceled` là final state và không được chuyển tiếp sang `delivered`.
- Source: `eshop-sut/README.md:141-162`

## Severity / Priority

Major / P1

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser**: API client / source-level UI check
- **URL**: `/api/admin/orders/:id/status`
- **Build/Commit**:

## Steps to reproduce

1. Chuẩn bị fixture/order đúng precondition của `FR10-UC01-TC05`.
2. Đăng nhập đúng actor hoặc mở/kiểm tra đúng interface theo test case.
3. Thực hiện action trong test case.
4. Đọc lại response/UI condition và trạng thái đơn hàng sau action.

## Expected result

- HTTP lỗi và trạng thái đơn hàng vẫn là `canceled`.

## Actual result

- Expected HTTP lỗi và status giữ `canceled`, actual HTTP 200, final status `delivered`, response `{'message': 'Order status updated'}`.

## Evidence

[Evidence bổ sung sau.]
