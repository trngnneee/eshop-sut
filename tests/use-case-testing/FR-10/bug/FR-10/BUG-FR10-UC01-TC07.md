## BUG-FR10-UC01-TC07 - User thường có thể gọi Admin status API

**GitHub issue title:** `[BUG][FR-10][Order State Machine] User thường có thể gọi Admin status API`

**GitHub issue:** [TBD]

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `FR10-UC01-TC07`
- Path: `eshop-sut/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC01-TC07.md`

## Requirement liên quan

- `FR-10`
- Admin status API phải yêu cầu token có quyền Admin.
- Source: `eshop-sut/README.md:141-162`

## Severity / Priority

Major / P1

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser**: API client / source-level UI check
- **URL**: `/api/admin/orders/:id/status`
- **Build/Commit**:

## Steps to reproduce

1. Chuẩn bị fixture/order đúng precondition của `FR10-UC01-TC07`.
2. Đăng nhập đúng actor hoặc mở/kiểm tra đúng interface theo test case.
3. Thực hiện action trong test case.
4. Đọc lại response/UI condition và trạng thái đơn hàng sau action.

## Expected result

- HTTP 401/403 và trạng thái đơn hàng vẫn là `pending`.

## Actual result

- Expected HTTP 401/403 và status giữ `pending`, actual HTTP 200, final status `confirmed`, response `{'message': 'Order status updated'}`.

## Evidence

[Evidence bổ sung sau.]
