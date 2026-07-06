# Test Run - FR-18 Admin Order Management

__Ngày thực hiện__: [27/06/2026]  
__Người thực hiện__: Đặng Trường Nguyên  
__Môi trường thử nghiệm__: [Local Web/API, backend http://localhost:3000, frontend-admin http://localhost:5174]

## Tổng quan kết quả

| Nhóm kiểm thử | Domain TC | BVA TC | Tổng TC | Pass | Fail |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Admin Status Transition | 15 | 0 | 15 | 14 | 1 |
| Order ID | 0 | 3 | 3 | 3 | 0 |
| Admin Order Visibility | 2 | 0 | 2 | 2 | 0 |
| Admin Access Control | 4 | 0 | 4 | 2 | 2 |
| Shipping Address Rendering | 3 | 0 | 3 | 0 | 3 |
| **Tổng** | **24** | **3** | **27** | **21** | **6** |

## Test Case Execution Report

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [FR18-S-TC01](../test-cases/admin_order_management/FR18-S-TC01.md) | Admin Order Management - Admin Status Transition | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |
| [FR18-S-TC02](../test-cases/admin_order_management/FR18-S-TC02.md) | Admin Order Management - Admin Status Transition | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |
| [FR18-S-TC03](../test-cases/admin_order_management/FR18-S-TC03.md) | Admin Order Management - Admin Status Transition | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |
| [FR18-S-TC04](../test-cases/admin_order_management/FR18-S-TC04.md) | Admin Order Management - Admin Status Transition | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |
| [FR18-S-TC05](../test-cases/admin_order_management/FR18-S-TC05.md) | Admin Order Management - Admin Status Transition | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |
| [FR18-S-TC06](../test-cases/admin_order_management/FR18-S-TC06.md) | Admin Order Management - Admin Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR18-S-TC07](../test-cases/admin_order_management/FR18-S-TC07.md) | Admin Order Management - Admin Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR18-S-TC08](../test-cases/admin_order_management/FR18-S-TC08.md) | Admin Order Management - Admin Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR18-S-TC09](../test-cases/admin_order_management/FR18-S-TC09.md) | Admin Order Management - Admin Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR18-S-TC10](../test-cases/admin_order_management/FR18-S-TC10.md) | Admin Order Management - Admin Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR18-S-TC11](../test-cases/admin_order_management/FR18-S-TC11.md) | Admin Order Management - Admin Status Transition | Đặng Trường Nguyên | Failed | BUG-FR18-S-01 - Admin có thể chuyển final state canceled sang delivered | Đơn hàng được chuyển đổi trạng thái sang delivered. |
| [FR18-S-TC12](../test-cases/admin_order_management/FR18-S-TC12.md) | Admin Order Management - Admin Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR18-S-TC13](../test-cases/admin_order_management/FR18-S-TC13.md) | Admin Order Management - Admin Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR18-S-TC14](../test-cases/admin_order_management/FR18-S-TC14.md) | Admin Order Management - Admin Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR18-S-TC15](../test-cases/admin_order_management/FR18-S-TC15.md) | Admin Order Management - Admin Status Transition | Đặng Trường Nguyên | Passed | None | API chặn vì chuyển đổi trạng thái không hợp lệ, status đơn hàng được giữ nguyên. |
| [FR18-O-BVA-TC01](../test-cases/admin_order_management/FR18-O-BVA-TC01.md) | Admin Order Management - Order ID | Đặng Trường Nguyên | Passed | None | Hệ thống từ chối vì không có đơn hàng nào phù hợp. |
| [FR18-O-BVA-TC02](../test-cases/admin_order_management/FR18-O-BVA-TC02.md) | Admin Order Management - Order ID | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |
| [FR18-O-BVA-TC03](../test-cases/admin_order_management/FR18-O-BVA-TC03.md) | Admin Order Management - Order ID | Đặng Trường Nguyên | Passed | None | Status đơn hàng được cập nhật. |
| [FR18-V-TC01](../test-cases/admin_order_management/FR18-V-TC01.md) | Admin Order Management - Admin Order Visibility | Đặng Trường Nguyên | Passed | None | Danh sách đơn hàng được hiển thị đúng. |
| [FR18-V-TC02](../test-cases/admin_order_management/FR18-V-TC02.md) | Admin Order Management - Admin Order Visibility | Đặng Trường Nguyên | Passed | None | Response không chứa password, password hash, reset token hoặc dữ liệu xác thực nhạy cảm của user. |
| [FR18-A-TC01](../test-cases/admin_order_management/FR18-A-TC01.md) | Admin Order Management - Admin Access Control | Đặng Trường Nguyên | Failed | BUG-FR18-A-01 - API Admin không kiểm tra role admin | API trả về danh sách đơn hàng. |
| [FR18-A-TC02](../test-cases/admin_order_management/FR18-A-TC02.md) | Admin Order Management - Admin Access Control | Đặng Trường Nguyên | Passed | None | API chặn vì unauthorized. |
| [FR18-A-TC03](../test-cases/admin_order_management/FR18-A-TC03.md) | Admin Order Management - Admin Access Control | Đặng Trường Nguyên | Failed | BUG-FR18-A-01 - API Admin không kiểm tra role admin | Status đơn hàng được cập nhật thành công. |
| [FR18-A-TC04](../test-cases/admin_order_management/FR18-A-TC04.md) | Admin Order Management - Admin Access Control | Đặng Trường Nguyên | Passed | None | API chặn vì unauthorized. |
| [FR18-X-TC01](../test-cases/admin_order_management/FR18-X-TC01.md) | Admin Order Management - Shipping Address Rendering | Đặng Trường Nguyên | Failed | BUG-FR18-X-01 - Admin UI không hiển thị địa chỉ giao hàng | Địa chỉ giao hàng không được hiển thị. |
| [FR18-X-TC02](../test-cases/admin_order_management/FR18-X-TC02.md) | Admin Order Management - Shipping Address Rendering | Đặng Trường Nguyên | Failed | BUG-FR18-X-01 - Admin UI không hiển thị địa chỉ giao hàng | Địa chỉ giao hàng không được hiển thị. |
| [FR18-X-TC03](../test-cases/admin_order_management/FR18-X-TC03.md) | Admin Order Management - Shipping Address Rendering | Đặng Trường Nguyên | Failed | BUG-FR18-X-01 - Admin UI không hiển thị địa chỉ giao hàng | Địa chỉ giao hàng không được hiển thị. |

## Defect Log

Các test case `Fail` được gom theo root cause để map sang bug report riêng. Chi tiết issue template nằm tại [tests/bug/FR-18.md](../bug/FR-18.md).

| Bug ID | Related TC ID | Tóm tắt | Severity | Status | Evidence / Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| BUG-FR18-S-01 | FR18-S-TC11 | Endpoint admin status cho phép chuyển final state `canceled` sang `delivered`. | High | Open | Đơn hàng `canceled` được chuyển sang `delivered` thay vì bị từ chối. Evidence bổ sung sau. |
| BUG-FR18-A-01 | FR18-A-TC01, FR18-A-TC03 | API Admin không kiểm tra `role = 'admin'`, cho phép user thường xem danh sách đơn hàng và cập nhật trạng thái đơn hàng. | High | Open | User thường gọi được `GET /api/admin/orders` và `PUT /api/admin/orders/:id/status`. Evidence bổ sung sau. |
| BUG-FR18-X-01 | FR18-X-TC01, FR18-X-TC02, FR18-X-TC03 | Admin UI không hiển thị `shipping_address` của đơn hàng. | Medium | Open | Địa chỉ giao hàng không được hiển thị với cả dữ liệu bình thường và dữ liệu cần escape. Evidence bổ sung sau. |
