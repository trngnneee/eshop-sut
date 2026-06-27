# FR-18 - Quản lý Đơn hàng (Admin)

## Nguồn yêu cầu

README.md, dòng 218-222:

- Admin xem toàn bộ đơn hàng của tất cả người dùng.
- Admin có thể chuyển đổi trạng thái đơn hàng theo đúng State Machine đã định nghĩa ở FR-10.
- Địa chỉ giao hàng phải được hiển thị an toàn, không render HTML.

Yêu cầu liên quan:

- README.md, dòng 141-162: State Machine của đơn hàng trong FR-10.
- README.md, dòng 174-179: API Admin yêu cầu JWT hợp lệ và `role = 'admin'`.
- README.md, dòng 274-281: SEC-04 yêu cầu escape dữ liệu user nhập khi hiển thị UI, không dùng `innerHTML` trực tiếp.
- `api_specification.md`, dòng 173-182: endpoint `GET /api/admin/orders` và `PUT /api/admin/orders/:id/status`.

## Assumptions

| ID | Assumption | Lý do |
| :--- | :--- | :--- |
| A1 | Admin xem danh sách đơn hàng qua `GET /api/admin/orders` hoặc tab Quản lý Đơn hàng trong Admin UI. | `api_specification.md` định nghĩa endpoint quản lý đơn hàng toàn hệ thống cho Admin. |
| A2 | Admin chuyển trạng thái qua `PUT /api/admin/orders/:id/status` với body `{"status":"..."}`. | `api_specification.md` định nghĩa endpoint cập nhật trạng thái đơn hàng cho Admin. |
| A3 | Chỉ tài khoản có JWT hợp lệ và `role = 'admin'` được gọi các endpoint `/api/admin/*`. | FR-12 áp dụng cho toàn bộ Admin API, trong đó có FR-18. |
| A4 | Order ID trên path parameter phải là số nguyên dương đại diện cho đơn hàng tồn tại. | Cần một miền dữ liệu cụ thể để áp dụng BVA cho FR-18. |
| A5 | Không có biên trên cho Order ID trong README/API, nên BVA chỉ xét biên dưới tối thiểu `1`. | Không tự đặt giới hạn tối đa khi đặc tả không nêu. |
| A6 | Địa chỉ giao hàng là dữ liệu do user nhập và phải được render như text đã escape trên Admin UI. | FR-18 và SEC-04 yêu cầu không render HTML từ dữ liệu user nhập. |

## Input / Output Variables

| Variable | Loại | Ghi chú |
| :--- | :--- | :--- |
| `actor` | System state | `admin`, `user`, hoặc anonymous, quyết định quyền truy cập endpoint Admin. |
| JWT / role | System state | JWT hợp lệ với `role = 'admin'` mới được xem/cập nhật đơn hàng Admin. |
| `current_status` | System state | Trạng thái hiện tại của đơn hàng trước khi Admin thao tác. |
| `requested_status` | Request input | Trạng thái Admin muốn cập nhật qua body request. |
| `order_id` | Path parameter | ID đơn hàng cần cập nhật trạng thái. |
| `shipping_address` | User-controlled display data | Phải hiển thị an toàn, không render HTML/script. |
| Endpoint/API | Interface | `GET /api/admin/orders`, `PUT /api/admin/orders/:id/status`. |
| Final state / UI display | Expected output | Trạng thái sau request đúng state machine; danh sách đơn đầy đủ; địa chỉ hiển thị an toàn. |

## Equivalence Partitions

| Class ID | Domain Class | Representative Values | Expected Status | Reason |
| :--- | :--- | :--- | :--- | :--- |
| S-VALID-01 | Admin xác nhận đơn | `pending -> confirmed` | Accepted | Transition hợp lệ theo FR-10. |
| S-VALID-02 | Admin hủy đơn pending | `pending -> canceled` | Accepted | FR-10 cho phép User/Admin hủy từ `pending`. |
| S-VALID-03 | Admin giao hàng | `confirmed -> shipping` | Accepted | Transition hợp lệ theo FR-10. |
| S-VALID-04 | Admin hủy đơn confirmed | `confirmed -> canceled` | Accepted | FR-10 cho phép User/Admin hủy từ `confirmed`. |
| S-VALID-05 | Admin hoàn tất đơn | `shipping -> delivered` | Accepted | Transition hợp lệ đến final state `delivered`. |
| S-INVALID-01 | Chuyển tắt từ pending | `pending -> shipping` | Rejected | Bỏ qua trạng thái `confirmed`. |
| S-INVALID-02 | Chuyển tắt từ confirmed | `confirmed -> delivered` | Rejected | Bỏ qua trạng thái `shipping`. |
| S-INVALID-03 | Chuyển ngược từ shipping | `shipping -> confirmed` | Rejected | State machine không cho quay lại trạng thái trước. |
| S-INVALID-04 | Admin hủy shipping | `shipping -> canceled` | Rejected | Sơ đồ FR-10 chỉ cho `shipping -> delivered`. |
| S-INVALID-05 | Admin đổi delivered sang canceled | `delivered -> canceled` | Rejected | `delivered` là final state. |
| S-INVALID-06 | Admin đổi canceled sang delivered | `canceled -> delivered` | Rejected | `canceled` là final state. |
| S-INVALID-07 | Cập nhật no-op | `pending -> pending` | Rejected | Không phải transition được định nghĩa. |
| S-INVALID-08 | Status ngoài state machine | `refund` | Rejected | Không nằm trong 5 trạng thái hợp lệ. |
| S-INVALID-09 | Status rỗng | `""` | Rejected | Không phải trạng thái hợp lệ. |
| S-INVALID-10 | Status null | `null` | Rejected | Không phải trạng thái hợp lệ. |
| V-VALID-01 | Admin xem toàn bộ đơn hàng | Đơn của nhiều user | Accepted | FR-18 yêu cầu Admin xem toàn bộ đơn hàng của tất cả người dùng. |
| V-INVALID-01 | Response lộ dữ liệu nhạy cảm | `password`, `password_hash`, `reset_token` | Rejected | Danh sách order không cần dữ liệu xác thực nhạy cảm của user. |
| A-INVALID-01 | User thường gọi Admin API xem đơn | `role = user`, `GET /api/admin/orders` | Rejected | FR-12 yêu cầu Admin API kiểm tra role. |
| A-INVALID-02 | Anonymous gọi Admin API xem đơn | Không có token | Rejected | FR-12 yêu cầu JWT hợp lệ. |
| A-INVALID-03 | User thường cập nhật trạng thái qua Admin API | `role = user`, `PUT /api/admin/orders/:id/status` | Rejected | FR-12 yêu cầu Admin API kiểm tra role. |
| A-INVALID-04 | Anonymous cập nhật trạng thái qua Admin API | Không có token | Rejected | FR-12 yêu cầu JWT hợp lệ. |
| X-INVALID-01 | Địa chỉ chứa thẻ script | `<script>alert("xss")</script>12 Le Loi` | Rendered safely | FR-18 yêu cầu không render HTML. |
| X-INVALID-02 | Địa chỉ chứa HTML event handler | `<img src=x onerror=alert("xss")>34 Nguyen Hue` | Rendered safely | SEC-04 yêu cầu escape dữ liệu user nhập. |
| X-VALID-01 | Địa chỉ văn bản bình thường | `12 Le Loi, Quan 1, TP.HCM` | Rendered correctly | Giá trị hợp lệ vẫn phải hiển thị đúng. |

## Boundary Values

| Field | Boundary Type | Value | Expected Status | Test Case |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | Min-1 | `0` | Rejected | FR18-O-BVA-TC01 |
| `order_id` | Min | `1` | Accepted | FR18-O-BVA-TC02 |
| `order_id` | Min+1 | `2` | Accepted | FR18-O-BVA-TC03 |

## Generated Test Case Index

| TC ID | Class / Boundary | Technique | Expected Status |
| :--- | :--- | :--- | :--- |
| FR18-S-TC01 | S-VALID-01 | Equivalence Partitioning / State Transition | Accepted |
| FR18-S-TC02 | S-VALID-02 | Equivalence Partitioning / State Transition | Accepted |
| FR18-S-TC03 | S-VALID-03 | Equivalence Partitioning / State Transition | Accepted |
| FR18-S-TC04 | S-VALID-04 | Equivalence Partitioning / State Transition | Accepted |
| FR18-S-TC05 | S-VALID-05 | Equivalence Partitioning / State Transition | Accepted |
| FR18-S-TC06 | S-INVALID-01 | Equivalence Partitioning / State Transition | Rejected |
| FR18-S-TC07 | S-INVALID-02 | Equivalence Partitioning / State Transition | Rejected |
| FR18-S-TC08 | S-INVALID-03 | Equivalence Partitioning / State Transition | Rejected |
| FR18-S-TC09 | S-INVALID-04 | Equivalence Partitioning / State Transition | Rejected |
| FR18-S-TC10 | S-INVALID-05 | Equivalence Partitioning / State Transition | Rejected |
| FR18-S-TC11 | S-INVALID-06 | Equivalence Partitioning / State Transition | Rejected |
| FR18-S-TC12 | S-INVALID-07 | Equivalence Partitioning / State Transition | Rejected |
| FR18-S-TC13 | S-INVALID-08 | Equivalence Partitioning | Rejected |
| FR18-S-TC14 | S-INVALID-09 | Equivalence Partitioning | Rejected |
| FR18-S-TC15 | S-INVALID-10 | Equivalence Partitioning | Rejected |
| FR18-O-BVA-TC01 | `order_id` Min-1 | Boundary Value Analysis | Rejected |
| FR18-O-BVA-TC02 | `order_id` Min | Boundary Value Analysis | Accepted |
| FR18-O-BVA-TC03 | `order_id` Min+1 | Boundary Value Analysis | Accepted |
| FR18-V-TC01 | V-VALID-01 | Equivalence Partitioning | Accepted |
| FR18-V-TC02 | V-INVALID-01 | Equivalence Partitioning / Security | Rejected |
| FR18-A-TC01 | A-INVALID-01 | Equivalence Partitioning / Authorization | Rejected |
| FR18-A-TC02 | A-INVALID-02 | Equivalence Partitioning / Authorization | Rejected |
| FR18-A-TC03 | A-INVALID-03 | Equivalence Partitioning / Authorization | Rejected |
| FR18-A-TC04 | A-INVALID-04 | Equivalence Partitioning / Authorization | Rejected |
| FR18-X-TC01 | X-INVALID-01 | Equivalence Partitioning / Security | Rendered safely |
| FR18-X-TC02 | X-INVALID-02 | Equivalence Partitioning / Security | Rendered safely |
| FR18-X-TC03 | X-VALID-01 | Equivalence Partitioning | Rendered correctly |

## Generated Artifacts

| Artifact | Path |
| :--- | :--- |
| JSON config | `tests/test-configs/fr18-config.json` |
| Test cases | `tests/test-cases/admin_order_management/` |
| Test run template | `tests/test-runs/fr18-admin-order-management-test-run.md` |
| Traceability matrix | `tests/test-summary/traceability-matrix.md` |

## Count Summary

| Nhóm kiểm thử | Domain TC | BVA TC | Tổng TC |
| :--- | ---: | ---: | ---: |
| Admin Status Transition | 15 | 0 | 15 |
| Order ID | 0 | 3 | 3 |
| Admin Order Visibility | 2 | 0 | 2 |
| Admin Access Control | 4 | 0 | 4 |
| Shipping Address Rendering | 3 | 0 | 3 |
| **Tổng** | **24** | **3** | **27** |
