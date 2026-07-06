# FR-10 - Trạng thái Đơn hàng (Order State Machine)

## Nguồn yêu cầu

- `README.md:141-162`: định nghĩa 5 trạng thái, luồng chuyển hợp lệ, final states, và ràng buộc User không được tự hủy khi đơn ở `shipping`.
- `api_specification.md:173-182`: định nghĩa Admin API `PUT /api/admin/orders/:id/status` và các giá trị status hợp lệ.
- `backend/server.js:520-559`: implementation endpoint cập nhật trạng thái đơn hàng dùng để đối chiếu trạng thái/guard.

## Assumptions

| ID | Assumption | Lý do |
| :--- | :--- | :--- |
| A1 | Admin thao tác chuyển trạng thái qua `PUT /api/admin/orders/:id/status`. | `api_specification.md` đặt endpoint trong nhóm Admin API. |
| A2 | User thao tác hủy đơn qua `PUT /api/orders/:id/cancel`. | README FR-10 nêu User/Admin có thể hủy từ `pending` hoặc `confirmed`; luồng user hiện có trong web/mobile. |
| A3 | `delivered` và `canceled` là final states cho mọi actor. | README FR-10 quy định đây là trạng thái kết thúc. |

## State Model

| Element | Value |
| :--- | :--- |
| State variable | `status` |
| Initial state | `pending` |
| Valid states | `pending`, `confirmed`, `shipping`, `delivered`, `canceled` |
| Final states | `delivered`, `canceled` |
| Actors | `admin`, `user` |
| Interfaces | `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel`, Admin UI, Web/Mobile order cancellation |

## State Transition Table

| Transition ID | Actor | Current state | Action / Requested state | Expected next state | Expected status | Reason |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| S-VALID-01 | admin | `pending` | `Update order status` / `confirmed` | `confirmed` | Accepted | Transition hợp lệ theo sơ đồ FR-10. |
| S-VALID-02 | admin | `confirmed` | `Update order status` / `shipping` | `shipping` | Accepted | Transition hợp lệ theo sơ đồ FR-10. |
| S-VALID-03 | admin | `shipping` | `Update order status` / `delivered` | `delivered` | Accepted | Transition hợp lệ đến final state `delivered`. |
| S-VALID-04 | user | `pending` | `Cancel order` / `canceled` | `canceled` | Accepted | FR-10 cho phép User/Admin hủy từ `pending`. |
| S-VALID-05 | admin | `pending` | `Update order status` / `canceled` | `canceled` | Accepted | FR-10 cho phép User/Admin hủy từ `pending`. |
| S-VALID-06 | user | `confirmed` | `Cancel order` / `canceled` | `canceled` | Accepted | FR-10 cho phép User/Admin hủy từ `confirmed`. |
| S-VALID-07 | admin | `confirmed` | `Update order status` / `canceled` | `canceled` | Accepted | FR-10 cho phép User/Admin hủy từ `confirmed`. |
| S-INVALID-01 | admin | `pending` | `Update order status` / `shipping` | `pending` | Rejected | Bỏ qua trạng thái `confirmed`. |
| S-INVALID-02 | admin | `confirmed` | `Update order status` / `delivered` | `confirmed` | Rejected | Bỏ qua trạng thái `shipping`. |
| S-INVALID-03 | admin | `shipping` | `Update order status` / `confirmed` | `shipping` | Rejected | State machine không cho quay lại trạng thái trước. |
| S-INVALID-04 | admin | `shipping` | `Update order status` / `canceled` | `shipping` | Rejected | Sơ đồ FR-10 chỉ cho `shipping -> delivered`. |
| S-INVALID-05 | user | `shipping` | `Cancel order` / `canceled` | `shipping` | Rejected | FR-10 nêu User không được phép tự hủy khi `shipping`. |
| S-INVALID-06 | user | `delivered` | `Cancel order` / `canceled` | `delivered` | Rejected | `delivered` là final state. |
| S-INVALID-07 | user | `canceled` | `Cancel order` / `canceled` | `canceled` | Rejected | `canceled` là final state. |
| S-INVALID-08 | admin | `delivered` | `Update order status` / `canceled` | `delivered` | Rejected | `delivered` là final state. |
| S-INVALID-09 | admin | `canceled` | `Update order status` / `delivered` | `canceled` | Rejected | `canceled` là final state. |
| S-INVALID-10 | admin | `pending` | `Update order status` / `pending` | `pending` | Rejected | Không phải transition được định nghĩa. |
| S-INVALID-11 | admin | `pending` | `Update order status` / `refund` | `pending` | Rejected | Không nằm trong 5 trạng thái hợp lệ. |
| S-INVALID-12 | admin | `pending` | `Update order status` / `` | `pending` | Rejected | Không phải trạng thái hợp lệ. |
| S-INVALID-13 | admin | `pending` | `Update order status` / `null` | `pending` | Rejected | Không phải trạng thái hợp lệ. |

## Generated Test Case Index

| TC ID | Transition / Class | Actor | Technique | Expected Status |
| :--- | :--- | :--- | :--- | :--- |
| FR10-S-TC01 | S-VALID-01 | admin | State Transition Testing | Accepted |
| FR10-S-TC02 | S-VALID-02 | admin | State Transition Testing | Accepted |
| FR10-S-TC03 | S-VALID-03 | admin | State Transition Testing | Accepted |
| FR10-S-TC04 | S-VALID-04 | user | State Transition Testing | Accepted |
| FR10-S-TC05 | S-VALID-05 | admin | State Transition Testing | Accepted |
| FR10-S-TC06 | S-VALID-06 | user | State Transition Testing | Accepted |
| FR10-S-TC07 | S-VALID-07 | admin | State Transition Testing | Accepted |
| FR10-S-TC08 | S-INVALID-01 | admin | State Transition Testing | Rejected |
| FR10-S-TC09 | S-INVALID-02 | admin | State Transition Testing | Rejected |
| FR10-S-TC10 | S-INVALID-03 | admin | State Transition Testing | Rejected |
| FR10-S-TC11 | S-INVALID-04 | admin | State Transition Testing | Rejected |
| FR10-S-TC12 | S-INVALID-05 | user | State Transition Testing | Rejected |
| FR10-S-TC13 | S-INVALID-06 | user | State Transition Testing | Rejected |
| FR10-S-TC14 | S-INVALID-07 | user | State Transition Testing | Rejected |
| FR10-S-TC15 | S-INVALID-08 | admin | State Transition Testing | Rejected |
| FR10-S-TC16 | S-INVALID-09 | admin | State Transition Testing | Rejected |
| FR10-S-TC17 | S-INVALID-10 | admin | State Transition Testing | Rejected |
| FR10-S-TC18 | S-INVALID-11 | admin | State Transition Testing | Rejected |
| FR10-S-TC19 | S-INVALID-12 | admin | State Transition Testing | Rejected |
| FR10-S-TC20 | S-INVALID-13 | admin | State Transition Testing | Rejected |

## TC Coverage

| Coverage item | Total items | Covered by TC | Coverage |
| :--- | ---: | :--- | :--- |
| Valid transitions | 7 | FR10-S-TC01, FR10-S-TC02, FR10-S-TC03, FR10-S-TC04, FR10-S-TC05, FR10-S-TC06, FR10-S-TC07 | 7/7 |
| Invalid transitions | 13 | FR10-S-TC08, FR10-S-TC09, FR10-S-TC10, FR10-S-TC11, FR10-S-TC12, FR10-S-TC13, FR10-S-TC14, FR10-S-TC15, FR10-S-TC16, FR10-S-TC17, FR10-S-TC18, FR10-S-TC19, FR10-S-TC20 | 13/13 |
| Final-state rejections | 4 | FR10-S-TC13, FR10-S-TC14, FR10-S-TC15, FR10-S-TC16 | 4/4 |
| Actor / permission guards | 3 | FR10-S-TC01..FR10-S-TC07, FR10-S-TC12 | 3/3 |

## TC Status

| Status | Count |
| :--- | ---: |
| Not Run | 0 |
| Passed | 18 |
| Failed | 2 |
| Blocked | 0 |
| Skipped | 0 |
| **Total TC** | **20** |

## Bug Coverage

| Metric | Count / Value |
| :--- | :--- |
| Bug Count | 2 |
| Failed TC | 2 |
| Failed TC with exactly one bug | 2/2 |
| Bug reports mapped to exactly one failed TC | 2/2 |
| Unmapped failed TC | None |
| Bug without failed TC | None |

## Generated Artifacts

| Artifact | Path |
| :--- | :--- |
| Test cases | `state-transition-testing/FR-10/test-cases/order_state_machine/` |
| Test run | `state-transition-testing/FR-10/test-runs/fr10-order-state-machine-test-run.md` |
| Traceability matrix | `state-transition-testing/FR-10/test-summary/traceability-matrix.md` |
| Bug reports | `state-transition-testing/FR-10/bug/FR-10/` |
| JSON config | `state-transition-testing/FR-10/test-configs/fr10-order-state-machine-state-transition-config.json` |

## Count Summary

| Nhóm kiểm thử | State TC | Tổng TC |
| :--- | ---: | ---: |
| Status Transition | 20 | 20 |
| **Tổng** | **20** | **20** |
