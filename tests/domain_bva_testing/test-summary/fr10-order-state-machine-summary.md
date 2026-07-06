# FR-10 - Trạng thái Đơn hàng (Order State Machine)

## Nguồn yêu cầu

README.md, dòng 141-162:

- Đơn hàng có 5 trạng thái: `pending`, `confirmed`, `shipping`, `delivered`, `canceled`.
- Luồng hợp lệ: `pending -> confirmed -> shipping -> delivered`.
- User/Admin có thể hủy đơn từ `pending` hoặc `confirmed` sang `canceled`.
- `delivered` và `canceled` là final states, không được chuyển sang trạng thái khác.
- Khi đơn hàng ở `shipping`, User không được phép tự hủy.
- Mọi chuyển đổi không hợp lệ phải trả về lỗi với thông báo phù hợp.

## Assumptions

| ID | Assumption | Lý do |
| :--- | :--- | :--- |
| A1 | Admin thao tác chuyển trạng thái qua `PUT /api/admin/orders/:id/status`. | `api_specification.md` định nghĩa endpoint cập nhật trạng thái đơn hàng cho Admin. |
| A2 | User thao tác hủy đơn qua `PUT /api/orders/:id/cancel`. | `api_specification.md` định nghĩa endpoint hủy đơn hàng của User. |
| A3 | Order ID trên path parameter phải là số nguyên dương đại diện cho đơn hàng tồn tại. | Cần một miền dữ liệu cụ thể để áp dụng BVA cho FR-10. |
| A4 | Không có biên trên cho Order ID trong README/API, nên BVA chỉ xét biên dưới tối thiểu `1`. | Không tự đặt giới hạn tối đa khi đặc tả không nêu. |

## Input / Output Variables

| Variable | Loại | Ghi chú |
| :--- | :--- | :--- |
| `actor` | System state | `admin` hoặc `user`, quyết định endpoint/quyền thao tác. |
| `current_status` | System state | Trạng thái hiện tại của đơn hàng trước khi thao tác. |
| `requested_status/action` | Request input | Trạng thái muốn cập nhật hoặc hành động hủy đơn. |
| `order_id` | Path parameter | ID đơn hàng cần cập nhật/hủy. |
| Endpoint/API | Interface | `PUT /api/admin/orders/:id/status` hoặc `PUT /api/orders/:id/cancel`. |
| Final state | Expected output | Trạng thái sau request phải đúng state machine hoặc giữ nguyên nếu bị từ chối. |

## Equivalence Partitions

| Class ID | Domain Class | Representative Values | Expected Status | Reason |
| :--- | :--- | :--- | :--- | :--- |
| S-VALID-01 | Admin xác nhận đơn | `pending -> confirmed` | Accepted | Transition hợp lệ theo sơ đồ FR-10. |
| S-VALID-02 | Admin giao hàng | `confirmed -> shipping` | Accepted | Transition hợp lệ theo sơ đồ FR-10. |
| S-VALID-03 | Admin hoàn tất đơn | `shipping -> delivered` | Accepted | Transition hợp lệ đến final state `delivered`. |
| S-VALID-04 | User hủy đơn pending | `pending -> canceled` | Accepted | FR-10 cho phép User/Admin hủy từ `pending`. |
| S-VALID-05 | Admin hủy đơn pending | `pending -> canceled` | Accepted | FR-10 cho phép User/Admin hủy từ `pending`. |
| S-VALID-06 | User hủy đơn confirmed | `confirmed -> canceled` | Accepted | FR-10 cho phép User/Admin hủy từ `confirmed`. |
| S-VALID-07 | Admin hủy đơn confirmed | `confirmed -> canceled` | Accepted | FR-10 cho phép User/Admin hủy từ `confirmed`. |
| S-INVALID-01 | Chuyển tắt từ pending | `pending -> shipping` | Rejected | Bỏ qua trạng thái `confirmed`. |
| S-INVALID-02 | Chuyển tắt từ confirmed | `confirmed -> delivered` | Rejected | Bỏ qua trạng thái `shipping`. |
| S-INVALID-03 | Chuyển ngược từ shipping | `shipping -> confirmed` | Rejected | State machine không cho quay lại trạng thái trước. |
| S-INVALID-04 | Admin hủy shipping | `shipping -> canceled` | Rejected | Sơ đồ FR-10 chỉ cho `shipping -> delivered`. |
| S-INVALID-05 | User hủy shipping | `shipping -> canceled` | Rejected | FR-10 nêu User không được phép tự hủy khi `shipping`. |
| S-INVALID-06 | User hủy delivered | `delivered -> canceled` | Rejected | `delivered` là final state. |
| S-INVALID-07 | User hủy lại canceled | `canceled -> canceled` | Rejected | `canceled` là final state. |
| S-INVALID-08 | Admin đổi delivered sang canceled | `delivered -> canceled` | Rejected | `delivered` là final state. |
| S-INVALID-09 | Admin đổi canceled sang delivered | `canceled -> delivered` | Rejected | `canceled` là final state. |
| S-INVALID-10 | Cập nhật no-op | `pending -> pending` | Rejected | Không phải transition được định nghĩa. |
| S-INVALID-11 | Status ngoài state machine | `refund` | Rejected | Không nằm trong 5 trạng thái hợp lệ. |
| S-INVALID-12 | Status rỗng | `""` | Rejected | Không phải trạng thái hợp lệ. |
| S-INVALID-13 | Status null | `null` | Rejected | Không phải trạng thái hợp lệ. |

## Boundary Values

| Field | Boundary Type | Value | Expected Status | Test Case |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | Min-1 | `0` | Rejected | FR10-O-BVA-TC01 |
| `order_id` | Min | `1` | Accepted | FR10-O-BVA-TC02 |
| `order_id` | Min+1 | `2` | Accepted | FR10-O-BVA-TC03 |

## Generated Test Case Index

| TC ID | Class / Boundary | Technique | Expected Status |
| :--- | :--- | :--- | :--- |
| FR10-S-TC01 | S-VALID-01 | Equivalence Partitioning / State Transition | Accepted |
| FR10-S-TC02 | S-VALID-02 | Equivalence Partitioning / State Transition | Accepted |
| FR10-S-TC03 | S-VALID-03 | Equivalence Partitioning / State Transition | Accepted |
| FR10-S-TC04 | S-VALID-04 | Equivalence Partitioning / State Transition | Accepted |
| FR10-S-TC05 | S-VALID-05 | Equivalence Partitioning / State Transition | Accepted |
| FR10-S-TC06 | S-VALID-06 | Equivalence Partitioning / State Transition | Accepted |
| FR10-S-TC07 | S-VALID-07 | Equivalence Partitioning / State Transition | Accepted |
| FR10-S-TC08 | S-INVALID-01 | Equivalence Partitioning / State Transition | Rejected |
| FR10-S-TC09 | S-INVALID-02 | Equivalence Partitioning / State Transition | Rejected |
| FR10-S-TC10 | S-INVALID-03 | Equivalence Partitioning / State Transition | Rejected |
| FR10-S-TC11 | S-INVALID-04 | Equivalence Partitioning / State Transition | Rejected |
| FR10-S-TC12 | S-INVALID-05 | Equivalence Partitioning / State Transition | Rejected |
| FR10-S-TC13 | S-INVALID-06 | Equivalence Partitioning / State Transition | Rejected |
| FR10-S-TC14 | S-INVALID-07 | Equivalence Partitioning / State Transition | Rejected |
| FR10-S-TC15 | S-INVALID-08 | Equivalence Partitioning / State Transition | Rejected |
| FR10-S-TC16 | S-INVALID-09 | Equivalence Partitioning / State Transition | Rejected |
| FR10-S-TC17 | S-INVALID-10 | Equivalence Partitioning / State Transition | Rejected |
| FR10-S-TC18 | S-INVALID-11 | Equivalence Partitioning | Rejected |
| FR10-S-TC19 | S-INVALID-12 | Equivalence Partitioning | Rejected |
| FR10-S-TC20 | S-INVALID-13 | Equivalence Partitioning | Rejected |
| FR10-O-BVA-TC01 | `order_id` Min-1 | Boundary Value Analysis | Rejected |
| FR10-O-BVA-TC02 | `order_id` Min | Boundary Value Analysis | Accepted |
| FR10-O-BVA-TC03 | `order_id` Min+1 | Boundary Value Analysis | Accepted |

## Generated Artifacts

| Artifact | Path |
| :--- | :--- |
| JSON config | `tests/test-configs/fr10-config.json` |
| Test cases | `tests/test-cases/order_state_machine/` |
| Test run template | `tests/test-runs/fr10-order-state-machine-test-run.md` |
| Traceability matrix | `tests/test-summary/traceability-matrix.md` |

## Count Summary

| Nhóm kiểm thử | Domain TC | BVA TC | Tổng TC |
| :--- | ---: | ---: | ---: |
| Status Transition | 20 | 0 | 20 |
| Order ID | 0 | 3 | 3 |
| **Tổng** | **20** | **3** | **23** |
