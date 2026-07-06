# Test Run - FR-10 Order State Machine

__Ngày thực hiện__: 06/07/2026  
__Người thực hiện__: Đặng Trường Nguyên  
__Môi trường thử nghiệm__: Local API, backend http://localhost:3000, SQLite fixture per test case  

## Tổng quan kết quả

| Nhóm kiểm thử | State TC | Tổng TC | Pass | Fail | Blocked | Skipped |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Status Transition | 20 | 20 | 18 | 2 | 0 | 0 |
| **Tổng** | **20** | **20** | **18** | **2** | **0** | **0** |

## TC Coverage

| Coverage item | Total items | Covered by TC | Coverage |
| :--- | ---: | :--- | :--- |
| State variables | 1 | FR10-S-TC01, FR10-S-TC02, FR10-S-TC03, FR10-S-TC04, FR10-S-TC05, FR10-S-TC06, FR10-S-TC07, FR10-S-TC08, FR10-S-TC09, FR10-S-TC10, FR10-S-TC11, FR10-S-TC12, FR10-S-TC13, FR10-S-TC14, FR10-S-TC15, FR10-S-TC16, FR10-S-TC17, FR10-S-TC18, FR10-S-TC19, FR10-S-TC20 | 1/1 |
| Valid transitions | 7 | FR10-S-TC01, FR10-S-TC02, FR10-S-TC03, FR10-S-TC04, FR10-S-TC05, FR10-S-TC06, FR10-S-TC07 | 7/7 |
| Invalid transitions | 13 | FR10-S-TC08, FR10-S-TC09, FR10-S-TC10, FR10-S-TC11, FR10-S-TC12, FR10-S-TC13, FR10-S-TC14, FR10-S-TC15, FR10-S-TC16, FR10-S-TC17, FR10-S-TC18, FR10-S-TC19, FR10-S-TC20 | 13/13 |
| Final-state rejections | 4 | FR10-S-TC13, FR10-S-TC14, FR10-S-TC15, FR10-S-TC16 | 4/4 |
| Actor / permission guards | 3 | FR10-S-TC01..FR10-S-TC07, FR10-S-TC12 | 3/3 |
| Requirement bullets | 6 | FR10-S-TC01, FR10-S-TC02, FR10-S-TC03, FR10-S-TC04, FR10-S-TC05, FR10-S-TC06, FR10-S-TC07, FR10-S-TC08, FR10-S-TC09, FR10-S-TC10, FR10-S-TC11, FR10-S-TC12, FR10-S-TC13, FR10-S-TC14, FR10-S-TC15, FR10-S-TC16, FR10-S-TC17, FR10-S-TC18, FR10-S-TC19, FR10-S-TC20 | 6/6 |

## Test Case Execution Report

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [FR10-S-TC01](../test-cases/order_state_machine/FR10-S-TC01.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 200; final status `confirmed` đúng expected `confirmed`. |
| [FR10-S-TC02](../test-cases/order_state_machine/FR10-S-TC02.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 200; final status `shipping` đúng expected `shipping`. |
| [FR10-S-TC03](../test-cases/order_state_machine/FR10-S-TC03.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 200; final status `delivered` đúng expected `delivered`. |
| [FR10-S-TC04](../test-cases/order_state_machine/FR10-S-TC04.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 200; final status `canceled` đúng expected `canceled`. |
| [FR10-S-TC05](../test-cases/order_state_machine/FR10-S-TC05.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 200; final status `canceled` đúng expected `canceled`. |
| [FR10-S-TC06](../test-cases/order_state_machine/FR10-S-TC06.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 200; final status `canceled` đúng expected `canceled`. |
| [FR10-S-TC07](../test-cases/order_state_machine/FR10-S-TC07.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 200; final status `canceled` đúng expected `canceled`. |
| [FR10-S-TC08](../test-cases/order_state_machine/FR10-S-TC08.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `pending` giữ nguyên đúng expected `pending`. |
| [FR10-S-TC09](../test-cases/order_state_machine/FR10-S-TC09.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `confirmed` giữ nguyên đúng expected `confirmed`. |
| [FR10-S-TC10](../test-cases/order_state_machine/FR10-S-TC10.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `shipping` giữ nguyên đúng expected `shipping`. |
| [FR10-S-TC11](../test-cases/order_state_machine/FR10-S-TC11.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `shipping` giữ nguyên đúng expected `shipping`. |
| [FR10-S-TC12](../test-cases/order_state_machine/FR10-S-TC12.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Failed | BUG-FR10-S-01 - User có thể hủy đơn hàng đang shipping | Expected HTTP lỗi và status giữ `shipping`, actual HTTP 200, final status `canceled`, response `{'message': 'Order canceled successfully'}`. |
| [FR10-S-TC13](../test-cases/order_state_machine/FR10-S-TC13.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `delivered` giữ nguyên đúng expected `delivered`. |
| [FR10-S-TC14](../test-cases/order_state_machine/FR10-S-TC14.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `canceled` giữ nguyên đúng expected `canceled`. |
| [FR10-S-TC15](../test-cases/order_state_machine/FR10-S-TC15.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `delivered` giữ nguyên đúng expected `delivered`. |
| [FR10-S-TC16](../test-cases/order_state_machine/FR10-S-TC16.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Failed | BUG-FR10-S-02 - Admin có thể chuyển final state canceled sang delivered | Expected HTTP lỗi và status giữ `canceled`, actual HTTP 200, final status `delivered`, response `{'message': 'Order status updated'}`. |
| [FR10-S-TC17](../test-cases/order_state_machine/FR10-S-TC17.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `pending` giữ nguyên đúng expected `pending`. |
| [FR10-S-TC18](../test-cases/order_state_machine/FR10-S-TC18.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `pending` giữ nguyên đúng expected `pending`. |
| [FR10-S-TC19](../test-cases/order_state_machine/FR10-S-TC19.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `pending` giữ nguyên đúng expected `pending`. |
| [FR10-S-TC20](../test-cases/order_state_machine/FR10-S-TC20.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | HTTP 400; final status `pending` giữ nguyên đúng expected `pending`. |

## TC Status

| Status | Count |
| :--- | ---: |
| Not Run | 0 |
| Passed | 18 |
| Failed | 2 |
| Blocked | 0 |
| Skipped | 0 |
| **Total TC** | **20** |

## Defect Log

Mỗi failed TC phải map sang đúng một bug report riêng.

| Bug ID | Related TC ID | Tóm tắt | Severity | Status | Evidence / Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| BUG-FR10-S-01 | FR10-S-TC12 | User có thể hủy đơn hàng đang shipping | High | Open | Expected HTTP lỗi và status giữ `shipping`, actual HTTP 200, final status `canceled`, response `{'message': 'Order canceled successfully'}`. |
| BUG-FR10-S-02 | FR10-S-TC16 | Admin có thể chuyển final state canceled sang delivered | High | Open | Expected HTTP lỗi và status giữ `canceled`, actual HTTP 200, final status `delivered`, response `{'message': 'Order status updated'}`. |

## Bug Coverage

| Metric | Count / Value |
| :--- | :--- |
| Bug Count | 2 |
| Failed TC | 2 |
| Failed TC with exactly one bug | 2/2 |
| Bug reports mapped to exactly one failed TC | 2/2 |
| Unmapped failed TC | None |
| Bug without failed TC | None |
