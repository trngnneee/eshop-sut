# FR-10 - Trạng thái Đơn hàng (Order State Machine)

## Nguồn yêu cầu

- `README.md:141-162`: định nghĩa 5 trạng thái, luồng chuyển hợp lệ, final states, và rule User không được tự hủy khi đơn ở `shipping`.
- `README.md:218-222`: Admin quản lý đơn hàng phải tuân theo State Machine FR-10.
- `README.md:233-236`: Mobile hủy đơn phải tuân theo FR-10, chỉ `pending` hoặc `confirmed`.
- `api_specification.md:141-148`: User hủy đơn qua `PUT /api/orders/:id/cancel`.
- `api_specification.md:173-182`: Admin cập nhật trạng thái qua `PUT /api/admin/orders/:id/status`.
- `backend/server.js:321-341` và `backend/server.js:525-559`: implementation liên quan để xác định setup/guard cần kiểm thử.

## Assumptions

| ID | Assumption | Lý do |
| :--- | :--- | :--- |
| A1 | FR-10 có thể được kiểm bằng Use Case Testing vì mỗi actor theo đuổi goal rõ ràng: Admin cập nhật trạng thái, User hủy đơn, Admin hủy đơn. | User yêu cầu áp dụng skill Use Case cho FR-10. |
| A2 | Các trạng thái `delivered` và `canceled` là final states cho cả Admin và User. | README.md:141-162 quy định final states. |
| A3 | User chỉ được hủy đơn của chính mình qua `PUT /api/orders/:id/cancel`. | Backend lọc `id` theo `user_id` tại `backend/server.js:321-326`. |
| A4 | Admin API phải yêu cầu role Admin dù backend evidence cần kiểm chứng khi execute. | `api_specification.md:173` ghi rõ Admin API yêu cầu token và quyền Admin. |

## Use Case Model

| Use case ID | Actor | Goal | Trigger | Preconditions | Success postcondition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| UC-01 | admin | Cập nhật tiến trình xử lý đơn hàng theo đúng state machine. | Admin chọn action trạng thái trong Admin UI hoặc gọi Admin API. | Admin đã đăng nhập; đơn hàng tồn tại ở trạng thái nguồn của flow. | Đơn hàng chuyển sang trạng thái kế tiếp hợp lệ hoặc bị từ chối và giữ nguyên trạng thái. |
| UC-02 | user | Hủy đơn hàng của chính mình khi đơn còn ở trạng thái được phép hủy. | User bấm Hủy đơn trên Web/Mobile hoặc gọi API hủy đơn. | User đã đăng nhập; đơn hàng thuộc user hiện tại. | Đơn hợp lệ được chuyển sang `canceled`; flow không hợp lệ bị từ chối và giữ nguyên trạng thái. |
| UC-03 | admin | Hủy đơn hàng cho khách khi đơn còn ở trạng thái được phép hủy. | Admin chọn Hủy trong Admin UI hoặc gọi Admin status API. | Admin đã đăng nhập; đơn hàng tồn tại. | Đơn đủ điều kiện được chuyển sang `canceled`; đơn không đủ điều kiện bị từ chối và giữ nguyên trạng thái. |

## Flow Inventory

| Flow ID | Use case ID | Flow type | Steps / Condition | Expected result | Requirement source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| UC-01-MAIN | UC-01 | Main success | Admin xác nhận đơn hàng pending | Accepted | FR-10 định nghĩa luồng `pending -> confirmed -> shipping -> delivered`. Source: README.md:141-162. |
| UC-01-ALT-01 | UC-01 | Alternate | Admin chuyển đơn hàng confirmed sang shipping | Accepted | FR-10 định nghĩa luồng `pending -> confirmed -> shipping -> delivered`. Source: README.md:141-162. |
| UC-01-ALT-02 | UC-01 | Alternate | Admin hoàn tất đơn hàng shipping sang delivered | Accepted | FR-10 định nghĩa luồng `pending -> confirmed -> shipping -> delivered`. Source: README.md:141-162. |
| UC-01-EXC-01 | UC-01 | Exception | Admin bị từ chối khi chuyển tắt pending sang shipping | Rejected | Mọi chuyển đổi không hợp lệ phải trả về lỗi phù hợp. Source: README.md:141-162. |
| UC-01-EXC-02 | UC-01 | Exception | Admin bị từ chối khi chuyển final state canceled sang delivered | Rejected | `delivered` và `canceled` là final states, không được phép chuyển tiếp. Source: README.md:141-162. |
| UC-01-EXC-03 | UC-01 | Exception | Admin UI không hiển thị action chuyển tiếp cho final state | Rejected | `delivered` và `canceled` là final states, không được phép chuyển tiếp. Source: README.md:141-162. |
| UC-01-EXC-04 | UC-01 | Exception | User thường bị từ chối khi gọi Admin status API | Rejected | Admin API yêu cầu Authorization Bearer token và tài khoản có quyền Admin. Source: api_specification.md:173. |
| UC-01-EXC-05 | UC-01 | Exception | Admin bị từ chối khi gửi status ngoài state machine | Rejected | Mọi chuyển đổi không hợp lệ phải trả về lỗi phù hợp. Source: README.md:141-162. |
| UC-02-MAIN | UC-02 | Main success | User hủy đơn hàng của mình khi đơn pending | Accepted | FR-10 cho phép User/Admin hủy từ `pending` hoặc `confirmed`. Source: README.md:141-162. |
| UC-02-ALT-01 | UC-02 | Alternate | User hủy đơn hàng của mình khi đơn confirmed | Accepted | FR-10 cho phép User/Admin hủy từ `pending` hoặc `confirmed`. Source: README.md:141-162. |
| UC-02-ALT-02 | UC-02 | Alternate | Mobile chỉ hiển thị nút hủy cho đơn pending hoặc confirmed | Accepted | Mobile hủy đơn phải tuân theo FR-10, chỉ `pending` hoặc `confirmed`. Source: README.md:233-236. |
| UC-02-EXC-01 | UC-02 | Exception | User bị từ chối khi hủy đơn đang shipping | Rejected | User không được phép tự hủy khi đơn ở `shipping`. Source: README.md:141-162. |
| UC-02-EXC-02 | UC-02 | Exception | User bị từ chối khi hủy đơn đã delivered | Rejected | `delivered` và `canceled` là final states, không được phép chuyển tiếp. Source: README.md:141-162. |
| UC-02-EXC-03 | UC-02 | Exception | User bị từ chối khi hủy đơn của user khác | Rejected | User hủy đơn qua `PUT /api/orders/:id/cancel`; chỉ khi đơn chưa giao. Source: api_specification.md:141-148. |
| UC-02-EXC-04 | UC-02 | Exception | Guest bị từ chối khi gọi API hủy đơn | Rejected | User hủy đơn qua `PUT /api/orders/:id/cancel`; chỉ khi đơn chưa giao. Source: api_specification.md:141-148. |
| UC-02-EXC-05 | UC-02 | Exception | Web UI không hiển thị nút hủy cho đơn shipping | Rejected | User không được phép tự hủy khi đơn ở `shipping`. Source: README.md:141-162. |
| UC-03-MAIN | UC-03 | Main success | Admin hủy đơn pending | Accepted | FR-10 cho phép User/Admin hủy từ `pending` hoặc `confirmed`. Source: README.md:141-162. |
| UC-03-ALT-01 | UC-03 | Alternate | Admin hủy đơn confirmed | Accepted | FR-10 cho phép User/Admin hủy từ `pending` hoặc `confirmed`. Source: README.md:141-162. |
| UC-03-EXC-01 | UC-03 | Exception | Admin bị từ chối khi hủy đơn shipping | Rejected | Mọi chuyển đổi không hợp lệ phải trả về lỗi phù hợp. Source: README.md:141-162. |
| UC-03-EXC-02 | UC-03 | Exception | Admin bị từ chối khi hủy đơn delivered | Rejected | `delivered` và `canceled` là final states, không được phép chuyển tiếp. Source: README.md:141-162. |

## Generated Test Case Index

| TC ID | Use case | Flow ID | Actor | Technique | Expected Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| FR10-UC01-TC01 | UC-01 | UC-01-MAIN | admin | Use Case Testing | Accepted |
| FR10-UC01-TC02 | UC-01 | UC-01-ALT-01 | admin | Use Case Testing | Accepted |
| FR10-UC01-TC03 | UC-01 | UC-01-ALT-02 | admin | Use Case Testing | Accepted |
| FR10-UC01-TC04 | UC-01 | UC-01-EXC-01 | admin | Use Case Testing | Rejected |
| FR10-UC01-TC05 | UC-01 | UC-01-EXC-02 | admin | Use Case Testing | Rejected |
| FR10-UC01-TC06 | UC-01 | UC-01-EXC-03 | admin | Use Case Testing | Rejected |
| FR10-UC01-TC07 | UC-01 | UC-01-EXC-04 | user | Use Case Testing | Rejected |
| FR10-UC01-TC08 | UC-01 | UC-01-EXC-05 | admin | Use Case Testing | Rejected |
| FR10-UC02-TC01 | UC-02 | UC-02-MAIN | user | Use Case Testing | Accepted |
| FR10-UC02-TC02 | UC-02 | UC-02-ALT-01 | user | Use Case Testing | Accepted |
| FR10-UC02-TC03 | UC-02 | UC-02-ALT-02 | user | Use Case Testing | Accepted |
| FR10-UC02-TC04 | UC-02 | UC-02-EXC-01 | user | Use Case Testing | Rejected |
| FR10-UC02-TC05 | UC-02 | UC-02-EXC-02 | user | Use Case Testing | Rejected |
| FR10-UC02-TC06 | UC-02 | UC-02-EXC-03 | user | Use Case Testing | Rejected |
| FR10-UC02-TC07 | UC-02 | UC-02-EXC-04 | guest | Use Case Testing | Rejected |
| FR10-UC02-TC08 | UC-02 | UC-02-EXC-05 | user | Use Case Testing | Rejected |
| FR10-UC03-TC01 | UC-03 | UC-03-MAIN | admin | Use Case Testing | Accepted |
| FR10-UC03-TC02 | UC-03 | UC-03-ALT-01 | admin | Use Case Testing | Accepted |
| FR10-UC03-TC03 | UC-03 | UC-03-EXC-01 | admin | Use Case Testing | Rejected |
| FR10-UC03-TC04 | UC-03 | UC-03-EXC-02 | admin | Use Case Testing | Rejected |

## TC Coverage

| Coverage item | Total items | Covered by TC | Coverage |
| :--- | ---: | :--- | :--- |
| Use cases | 3 | FR10-UC01-TC01, FR10-UC01-TC02, FR10-UC01-TC03, FR10-UC01-TC04, FR10-UC01-TC05, FR10-UC01-TC06, FR10-UC01-TC07, FR10-UC01-TC08, FR10-UC02-TC01, FR10-UC02-TC02, FR10-UC02-TC03, FR10-UC02-TC04, FR10-UC02-TC05, FR10-UC02-TC06, FR10-UC02-TC07, FR10-UC02-TC08, FR10-UC03-TC01, FR10-UC03-TC02, FR10-UC03-TC03, FR10-UC03-TC04 | 3/3 |
| Main flows | 3 | FR10-UC01-TC01, FR10-UC02-TC01, FR10-UC03-TC01 | 3/3 |
| Alternate flows | 5 | FR10-UC01-TC02, FR10-UC01-TC03, FR10-UC02-TC02, FR10-UC02-TC03, FR10-UC03-TC02 | 5/5 |
| Exception flows | 12 | FR10-UC01-TC04, FR10-UC01-TC05, FR10-UC01-TC06, FR10-UC01-TC07, FR10-UC01-TC08, FR10-UC02-TC04, FR10-UC02-TC05, FR10-UC02-TC06, FR10-UC02-TC07, FR10-UC02-TC08, FR10-UC03-TC03, FR10-UC03-TC04 | 12/12 |
| Actors / permission branches | 5 | FR10-UC01-TC01, FR10-UC01-TC02, FR10-UC01-TC03, FR10-UC01-TC04, FR10-UC01-TC05, FR10-UC01-TC06, FR10-UC01-TC07, FR10-UC01-TC08, FR10-UC02-TC01, FR10-UC02-TC02, FR10-UC02-TC03, FR10-UC02-TC04, FR10-UC02-TC05, FR10-UC02-TC06, FR10-UC02-TC07, FR10-UC02-TC08, FR10-UC03-TC01, FR10-UC03-TC02, FR10-UC03-TC03, FR10-UC03-TC04 | 5/5 |
| Requirement bullets | 8 | FR10-UC01-TC01, FR10-UC01-TC02, FR10-UC01-TC03, FR10-UC01-TC04, FR10-UC01-TC05, FR10-UC01-TC06, FR10-UC01-TC07, FR10-UC01-TC08, FR10-UC02-TC01, FR10-UC02-TC02, FR10-UC02-TC03, FR10-UC02-TC04, FR10-UC02-TC05, FR10-UC02-TC06, FR10-UC02-TC07, FR10-UC02-TC08, FR10-UC03-TC01, FR10-UC03-TC02, FR10-UC03-TC03, FR10-UC03-TC04 | 8/8 |

## TC Status

| Status | Count |
| :--- | ---: |
| Not Run | 0 |
| Passed | 15 |
| Failed | 5 |
| Blocked | 0 |
| Skipped | 0 |
| **Total TC** | **20** |

## Bug Coverage

| Metric | Count / Value |
| :--- | :--- |
| Bug Count | 5 |
| Failed TC | 5 |
| Failed TC with exactly one bug | 5/5 |
| Bug reports mapped to exactly one failed TC | 5/5 |
| Unmapped failed TC | None |
| Bug without failed TC | None |

## Generated Artifacts

| Artifact | Path |
| :--- | :--- |
| Test cases | `use-case-testing/FR-10/test-cases/order_state_machine/` |
| Test run | `use-case-testing/FR-10/test-runs/fr10-order-state-machine-test-run.md` |
| Traceability matrix | `use-case-testing/FR-10/test-summary/traceability-matrix.md` |
| Bug reports | `use-case-testing/FR-10/bug/FR-10/` |
| JSON config | `use-case-testing/FR-10/test-configs/fr10-order-state-machine-use-case-config.json` |

## Count Summary

| Nhóm kiểm thử | Main TC | Alternate TC | Exception TC | Tổng TC |
| :--- | ---: | ---: | ---: | ---: |
| Admin Fulfillment | 1 | 2 | 5 | 8 |
| User Cancellation | 1 | 2 | 5 | 8 |
| Admin Cancellation | 1 | 1 | 2 | 4 |
| **Tổng** | **3** | **5** | **12** | **20** |
