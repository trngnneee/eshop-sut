## BUG-FR10-UC01-TC06 - Admin UI hiển thị action chuyển tiếp cho đơn đã canceled

**GitHub issue title:** `[BUG][FR-10][Order State Machine] Admin UI hiển thị action chuyển tiếp cho đơn đã canceled`

**GitHub issue:** [TBD]

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `FR10-UC01-TC06`
- Path: `eshop-sut/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC01-TC06.md`

## Requirement liên quan

- `FR-10`
- Admin UI không được hiển thị action chuyển tiếp cho final state `delivered` hoặc `canceled`.
- Source: `eshop-sut/README.md:141-162`

## Severity / Priority

Major / P1

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser**: API client / source-level UI check
- **URL**: `Admin Orders table`
- **Build/Commit**:

## Steps to reproduce

1. Chuẩn bị fixture/order đúng precondition của `FR10-UC01-TC06`.
2. Đăng nhập đúng actor hoặc mở/kiểm tra đúng interface theo test case.
3. Thực hiện action trong test case.
4. Đọc lại response/UI condition và trạng thái đơn hàng sau action.

## Expected result

- Không có action cập nhật trạng thái nào được render cho final state.

## Actual result

- Actual source `frontend-admin/src/App.jsx:862` render nút cho `canceled` và gọi `updateOrderStatus(o.id, "delivered")`, nên final state vẫn có action chuyển tiếp.
- Evidence source: frontend-admin/src/App.jsx

## Evidence

[Evidence bổ sung sau.]
