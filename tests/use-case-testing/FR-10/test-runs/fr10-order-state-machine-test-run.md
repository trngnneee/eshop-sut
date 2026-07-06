# Test Run - FR-10 Order State Machine

__Ngày thực hiện__: 06/07/2026  
__Người thực hiện__: Đặng Trường Nguyên  
__Môi trường thử nghiệm__: Local API http://localhost:3000 + SQLite fixture per API case; source-level UI render-condition check for UI-only cases  

## Tổng quan kết quả

| Nhóm kiểm thử | Main TC | Alternate TC | Exception TC | Tổng TC | Pass | Fail | Blocked | Skipped |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Admin Fulfillment | 1 | 2 | 5 | 8 | 5 | 3 | 0 | 0 |
| User Cancellation | 1 | 2 | 5 | 8 | 6 | 2 | 0 | 0 |
| Admin Cancellation | 1 | 1 | 2 | 4 | 4 | 0 | 0 | 0 |
| **Tổng** | **3** | **5** | **12** | **20** | **15** | **5** | **0** | **0** |

## TC Coverage

| Coverage item | Total items | Covered by TC | Coverage |
| :--- | ---: | :--- | :--- |
| Use cases | 3 | FR10-UC01-TC01, FR10-UC01-TC02, FR10-UC01-TC03, FR10-UC01-TC04, FR10-UC01-TC05, FR10-UC01-TC06, FR10-UC01-TC07, FR10-UC01-TC08, FR10-UC02-TC01, FR10-UC02-TC02, FR10-UC02-TC03, FR10-UC02-TC04, FR10-UC02-TC05, FR10-UC02-TC06, FR10-UC02-TC07, FR10-UC02-TC08, FR10-UC03-TC01, FR10-UC03-TC02, FR10-UC03-TC03, FR10-UC03-TC04 | 3/3 |
| Main flows | 3 | FR10-UC01-TC01, FR10-UC02-TC01, FR10-UC03-TC01 | 3/3 |
| Alternate flows | 5 | FR10-UC01-TC02, FR10-UC01-TC03, FR10-UC02-TC02, FR10-UC02-TC03, FR10-UC03-TC02 | 5/5 |
| Exception flows | 12 | FR10-UC01-TC04, FR10-UC01-TC05, FR10-UC01-TC06, FR10-UC01-TC07, FR10-UC01-TC08, FR10-UC02-TC04, FR10-UC02-TC05, FR10-UC02-TC06, FR10-UC02-TC07, FR10-UC02-TC08, FR10-UC03-TC03, FR10-UC03-TC04 | 12/12 |
| Requirement bullets | 8 | FR10-UC01-TC01, FR10-UC01-TC02, FR10-UC01-TC03, FR10-UC01-TC04, FR10-UC01-TC05, FR10-UC01-TC06, FR10-UC01-TC07, FR10-UC01-TC08, FR10-UC02-TC01, FR10-UC02-TC02, FR10-UC02-TC03, FR10-UC02-TC04, FR10-UC02-TC05, FR10-UC02-TC06, FR10-UC02-TC07, FR10-UC02-TC08, FR10-UC03-TC01, FR10-UC03-TC02, FR10-UC03-TC03, FR10-UC03-TC04 | 8/8 |

## Test Case Execution Report

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [FR10-UC01-TC01](../test-cases/order_state_machine/FR10-UC01-TC01.md) | Order State Machine - Admin Fulfillment | Đặng Trường Nguyên | Passed | None | HTTP 200; final status `confirmed` đúng expected `confirmed`. |
| [FR10-UC01-TC02](../test-cases/order_state_machine/FR10-UC01-TC02.md) | Order State Machine - Admin Fulfillment | Đặng Trường Nguyên | Passed | None | HTTP 200; final status `shipping` đúng expected `shipping`. |
| [FR10-UC01-TC03](../test-cases/order_state_machine/FR10-UC01-TC03.md) | Order State Machine - Admin Fulfillment | Đặng Trường Nguyên | Passed | None | HTTP 200; final status `delivered` đúng expected `delivered`. |
| [FR10-UC01-TC04](../test-cases/order_state_machine/FR10-UC01-TC04.md) | Order State Machine - Admin Fulfillment | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `pending` giữ nguyên đúng expected `pending`. |
| [FR10-UC01-TC05](../test-cases/order_state_machine/FR10-UC01-TC05.md) | Order State Machine - Admin Fulfillment | Đặng Trường Nguyên | Failed | BUG-FR10-UC01-TC05 - Admin API cho phép chuyển final state canceled sang delivered | Expected HTTP lỗi và status giữ `canceled`, actual HTTP 200, final status `delivered`, response `{'message': 'Order status updated'}`. |
| [FR10-UC01-TC06](../test-cases/order_state_machine/FR10-UC01-TC06.md) | Order State Machine - Admin Fulfillment | Đặng Trường Nguyên | Failed | BUG-FR10-UC01-TC06 - Admin UI hiển thị action chuyển tiếp cho đơn đã canceled | Actual source `frontend-admin/src/App.jsx:862` render nút cho `canceled` và gọi `updateOrderStatus(o.id, "delivered")`, nên final state vẫn có action chuyển tiếp. |
| [FR10-UC01-TC07](../test-cases/order_state_machine/FR10-UC01-TC07.md) | Order State Machine - Admin Fulfillment | Đặng Trường Nguyên | Failed | BUG-FR10-UC01-TC07 - User thường có thể gọi Admin status API | Expected HTTP 401/403 và status giữ `pending`, actual HTTP 200, final status `confirmed`, response `{'message': 'Order status updated'}`. |
| [FR10-UC01-TC08](../test-cases/order_state_machine/FR10-UC01-TC08.md) | Order State Machine - Admin Fulfillment | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `pending` giữ nguyên đúng expected `pending`. |
| [FR10-UC02-TC01](../test-cases/order_state_machine/FR10-UC02-TC01.md) | Order State Machine - User Cancellation | Đặng Trường Nguyên | Passed | None | HTTP 200; final status `canceled` đúng expected `canceled`. |
| [FR10-UC02-TC02](../test-cases/order_state_machine/FR10-UC02-TC02.md) | Order State Machine - User Cancellation | Đặng Trường Nguyên | Passed | None | HTTP 200; final status `canceled` đúng expected `canceled`. |
| [FR10-UC02-TC03](../test-cases/order_state_machine/FR10-UC02-TC03.md) | Order State Machine - User Cancellation | Đặng Trường Nguyên | Passed | None | Mobile render nút hủy chỉ khi `status` là `pending` hoặc `confirmed`. |
| [FR10-UC02-TC04](../test-cases/order_state_machine/FR10-UC02-TC04.md) | Order State Machine - User Cancellation | Đặng Trường Nguyên | Failed | BUG-FR10-UC02-TC04 - User có thể hủy đơn hàng đang shipping | Expected HTTP lỗi và status giữ `shipping`, actual HTTP 200, final status `canceled`, response `{'message': 'Order canceled successfully'}`. |
| [FR10-UC02-TC05](../test-cases/order_state_machine/FR10-UC02-TC05.md) | Order State Machine - User Cancellation | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `delivered` giữ nguyên đúng expected `delivered`. |
| [FR10-UC02-TC06](../test-cases/order_state_machine/FR10-UC02-TC06.md) | Order State Machine - User Cancellation | Đặng Trường Nguyên | Passed | None | HTTP 404; final status `pending` giữ nguyên đúng expected `pending`. |
| [FR10-UC02-TC07](../test-cases/order_state_machine/FR10-UC02-TC07.md) | Order State Machine - User Cancellation | Đặng Trường Nguyên | Passed | None | HTTP 401; final status `pending` giữ nguyên đúng expected `pending`. |
| [FR10-UC02-TC08](../test-cases/order_state_machine/FR10-UC02-TC08.md) | Order State Machine - User Cancellation | Đặng Trường Nguyên | Failed | BUG-FR10-UC02-TC08 - Web UI hiển thị nút hủy cho đơn đang shipping | Actual source `frontend-web/src/pages/Profile.jsx:201` render nút hủy cho mọi trạng thái khác `delivered`/`canceled`, nên `shipping` vẫn hiện nút `Hủy đơn`. |
| [FR10-UC03-TC01](../test-cases/order_state_machine/FR10-UC03-TC01.md) | Order State Machine - Admin Cancellation | Đặng Trường Nguyên | Passed | None | HTTP 200; final status `canceled` đúng expected `canceled`. |
| [FR10-UC03-TC02](../test-cases/order_state_machine/FR10-UC03-TC02.md) | Order State Machine - Admin Cancellation | Đặng Trường Nguyên | Passed | None | HTTP 200; final status `canceled` đúng expected `canceled`. |
| [FR10-UC03-TC03](../test-cases/order_state_machine/FR10-UC03-TC03.md) | Order State Machine - Admin Cancellation | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `shipping` giữ nguyên đúng expected `shipping`. |
| [FR10-UC03-TC04](../test-cases/order_state_machine/FR10-UC03-TC04.md) | Order State Machine - Admin Cancellation | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `delivered` giữ nguyên đúng expected `delivered`. |

## TC Status

| Status | Count |
| :--- | ---: |
| Not Run | 0 |
| Passed | 15 |
| Failed | 5 |
| Blocked | 0 |
| Skipped | 0 |
| **Total TC** | **20** |

## Defect Log

Mỗi failed TC phải map sang đúng một bug report riêng.

| Bug ID | Related TC ID | Tóm tắt | Severity | Status | Evidence / Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| BUG-FR10-UC01-TC05 | FR10-UC01-TC05 | Admin API cho phép chuyển final state canceled sang delivered | High | Open | Expected HTTP lỗi và status giữ `canceled`, actual HTTP 200, final status `delivered`, response `{'message': 'Order status updated'}`. |
| BUG-FR10-UC01-TC06 | FR10-UC01-TC06 | Admin UI hiển thị action chuyển tiếp cho đơn đã canceled | High | Open | Actual source `frontend-admin/src/App.jsx:862` render nút cho `canceled` và gọi `updateOrderStatus(o.id, "delivered")`, nên final state vẫn có action chuyển tiếp. |
| BUG-FR10-UC01-TC07 | FR10-UC01-TC07 | User thường có thể gọi Admin status API | High | Open | Expected HTTP 401/403 và status giữ `pending`, actual HTTP 200, final status `confirmed`, response `{'message': 'Order status updated'}`. |
| BUG-FR10-UC02-TC04 | FR10-UC02-TC04 | User có thể hủy đơn hàng đang shipping | High | Open | Expected HTTP lỗi và status giữ `shipping`, actual HTTP 200, final status `canceled`, response `{'message': 'Order canceled successfully'}`. |
| BUG-FR10-UC02-TC08 | FR10-UC02-TC08 | Web UI hiển thị nút hủy cho đơn đang shipping | High | Open | Actual source `frontend-web/src/pages/Profile.jsx:201` render nút hủy cho mọi trạng thái khác `delivered`/`canceled`, nên `shipping` vẫn hiện nút `Hủy đơn`. |

## Bug Coverage

| Metric | Count / Value |
| :--- | :--- |
| Bug Count | 5 |
| Failed TC | 5 |
| Failed TC with exactly one bug | 5/5 |
| Bug reports mapped to exactly one failed TC | 5/5 |
| Unmapped failed TC | None |
| Bug without failed TC | None |
