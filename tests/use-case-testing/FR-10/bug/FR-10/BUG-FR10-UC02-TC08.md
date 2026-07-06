## BUG-FR10-UC02-TC08 - Web UI hiển thị nút hủy cho đơn đang shipping

**GitHub issue title:** `[BUG][FR-10][Order State Machine] Web UI hiển thị nút hủy cho đơn đang shipping`

**GitHub issue:** [TBD]

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `FR10-UC02-TC08`
- Path: `eshop-sut/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC02-TC08.md`

## Requirement liên quan

- `FR-10`
- Web UI không được hiển thị nút `Hủy đơn` cho đơn đang `shipping`.
- Source: `eshop-sut/README.md:141-162`

## Severity / Priority

Major / P1

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser**: API client / source-level UI check
- **URL**: `Profile / Lịch sử đơn hàng`
- **Build/Commit**:

## Steps to reproduce

1. Chuẩn bị fixture/order đúng precondition của `FR10-UC02-TC08`.
2. Đăng nhập đúng actor hoặc mở/kiểm tra đúng interface theo test case.
3. Thực hiện action trong test case.
4. Đọc lại response/UI condition và trạng thái đơn hàng sau action.

## Expected result

- Không có action hủy đơn được render cho trạng thái `shipping`.

## Actual result

- Actual source `frontend-web/src/pages/Profile.jsx:201` render nút hủy cho mọi trạng thái khác `delivered`/`canceled`, nên `shipping` vẫn hiện nút `Hủy đơn`.
- Evidence source: frontend-web/src/pages/Profile.jsx

## Evidence

[Evidence bổ sung sau.]
