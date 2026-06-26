# Test Run - FR-10 Order State Machine

__Ngày thực hiện__: [26/06/2026]  
__Người thực hiện__: Đặng Trường Nguyên  
__Môi trường thử nghiệm__: [Local Web/API, backend http://localhost:3000, frontend/admin/mobile theo luồng kiểm thử]

## Tổng quan kết quả

| Nhóm kiểm thử | Domain TC | BVA TC | Tổng TC | Pass | Fail |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Status Transition | 20 | 0 | 20 | 18 | 2 |
| Order ID | 0 | 3 | 3 | 3 | 0 |
| **Tổng** | **20** | **3** | **23** | **21** | **2** |

## Test Case Execution Report

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [FR10-S-TC01](../test-cases/order_state_machine/FR10-S-TC01.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |
| [FR10-S-TC02](../test-cases/order_state_machine/FR10-S-TC02.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |
| [FR10-S-TC03](../test-cases/order_state_machine/FR10-S-TC03.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |
| [FR10-S-TC04](../test-cases/order_state_machine/FR10-S-TC04.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |
| [FR10-S-TC05](../test-cases/order_state_machine/FR10-S-TC05.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |
| [FR10-S-TC06](../test-cases/order_state_machine/FR10-S-TC06.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |
| [FR10-S-TC07](../test-cases/order_state_machine/FR10-S-TC07.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |
| [FR10-S-TC08](../test-cases/order_state_machine/FR10-S-TC08.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR10-S-TC09](../test-cases/order_state_machine/FR10-S-TC09.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR10-S-TC10](../test-cases/order_state_machine/FR10-S-TC10.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR10-S-TC11](../test-cases/order_state_machine/FR10-S-TC11.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR10-S-TC12](../test-cases/order_state_machine/FR10-S-TC12.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Failed | BUG-FR10-S-01 - User có thể hủy đơn hàng đang shipping | Đơn hàng được chuyển đổi trạng thái sang canceled. |
| [FR10-S-TC13](../test-cases/order_state_machine/FR10-S-TC13.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | API chặn, không cho hủy đơn hàng ở status này. |
| [FR10-S-TC14](../test-cases/order_state_machine/FR10-S-TC14.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | API chặn, không cho hủy đơn hàng ở status này. |
| [FR10-S-TC15](../test-cases/order_state_machine/FR10-S-TC15.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR10-S-TC16](../test-cases/order_state_machine/FR10-S-TC16.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Failed | BUG-FR10-S-02 - Admin có thể chuyển final state canceled sang delivered | Đơn hàng được chuyển đổi trạng thái sang delivered. |
| [FR10-S-TC17](../test-cases/order_state_machine/FR10-S-TC17.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR10-S-TC18](../test-cases/order_state_machine/FR10-S-TC18.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR10-S-TC19](../test-cases/order_state_machine/FR10-S-TC19.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR10-S-TC20](../test-cases/order_state_machine/FR10-S-TC20.md) | Order State Machine - Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR10-O-BVA-TC01](../test-cases/order_state_machine/FR10-O-BVA-TC01.md) | Order State Machine - Order ID | Đặng Trường Nguyên | Passed | None | Hệ thống từ chối vì không có đơn hàng nào phù hợp. |
| [FR10-O-BVA-TC02](../test-cases/order_state_machine/FR10-O-BVA-TC02.md) | Order State Machine - Order ID | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |
| [FR10-O-BVA-TC03](../test-cases/order_state_machine/FR10-O-BVA-TC03.md) | Order State Machine - Order ID | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |

## Defect Log

Các test case `Fail` được gom theo root cause để map sang bug report riêng. Chi tiết issue template nằm tại [tests/bug/FR-10.md](../bug/FR-10.md).

| Bug ID | Related TC ID | Tóm tắt | Severity | Status | Evidence / Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| BUG-FR10-S-01 | FR10-S-TC12 | Endpoint user cancel cho phép hủy đơn hàng đang ở trạng thái `shipping`. | High | Open | Đơn hàng `shipping` được chuyển sang `canceled` thay vì bị từ chối. Evidence bổ sung sau. |
| BUG-FR10-S-02 | FR10-S-TC16 | Endpoint admin status cho phép chuyển final state `canceled` sang `delivered`. | High | Open | Đơn hàng `canceled` được chuyển sang `delivered` thay vì bị từ chối. Evidence bổ sung sau. |
