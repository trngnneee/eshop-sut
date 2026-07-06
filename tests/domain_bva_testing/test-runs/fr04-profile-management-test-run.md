# Test Run - FR-04 Profile Management

__Ngày thực hiện__: [26/06/2026]  
__Người thực hiện__: Đặng Trường Nguyên  
__Môi trường thử nghiệm__: [Local Web/API, backend http://localhost:3000, frontend http://localhost:5173]

## Tổng quan kết quả

| Nhóm kiểm thử | Domain TC | BVA TC | Tổng TC | Pass | Fail |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Name Input | 2 | 7 | 9 | 8 | 1 |
| Phone Input | 5 | 4 | 9 | 3 | 6 |
| Address Input | 3 | 7 | 10 | 6 | 4 |
| Email Immutability | 1 | 0 | 1 | 1 | 0 |
| Role Protection | 1 | 0 | 1 | 0 | 1 |
| User Ownership/Auth | 2 | 0 | 2 | 2 | 0 |
| **Tổng** | **14** | **18** | **32** | **20** | **12** |

## Test Case Execution Report

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [FR04-N-TC01](../test-cases/profile_management/FR04-N-TC01.md) | Profile Management - Name Input | Đặng Trường Nguyên | Passed | None | Hệ thống từ chối submit và hiển thị thông báo lỗi bắt buộc nhập cho trường Họ Tên. |
| [FR04-N-BVA-TC01](../test-cases/profile_management/FR04-N-BVA-TC01.md) | Profile Management - Name Input | Đặng Trường Nguyên | Passed | None | Hệ thống từ chối submit và hiển thị thông báo lỗi bắt buộc nhập cho trường Họ Tên. |
| [FR04-N-BVA-TC02](../test-cases/profile_management/FR04-N-BVA-TC02.md) | Profile Management - Name Input | Đặng Trường Nguyên | Passed | None | Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Họ Tên. |
| [FR04-N-BVA-TC03](../test-cases/profile_management/FR04-N-BVA-TC03.md) | Profile Management - Name Input | Đặng Trường Nguyên | Passed | None | Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Họ Tên. |
| [FR04-N-BVA-TC04](../test-cases/profile_management/FR04-N-BVA-TC04.md) | Profile Management - Name Input | Đặng Trường Nguyên | Passed | None | Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Họ Tên. |
| [FR04-N-BVA-TC05](../test-cases/profile_management/FR04-N-BVA-TC05.md) | Profile Management - Name Input | Đặng Trường Nguyên | Passed | None | Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Họ Tên. |
| [FR04-N-BVA-TC06](../test-cases/profile_management/FR04-N-BVA-TC06.md) | Profile Management - Name Input | Đặng Trường Nguyên | Passed | None | Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Họ Tên. |
| [FR04-N-BVA-TC07](../test-cases/profile_management/FR04-N-BVA-TC07.md) | Profile Management - Name Input | Đặng Trường Nguyên | Failed | BUG-FR04-N-01 - Thiếu validate độ dài tối đa Họ Tên | Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Họ Tên. |
| [FR04-P-TC01](../test-cases/profile_management/FR04-P-TC01.md) | Profile Management - Phone Input | Đặng Trường Nguyên | Passed | None | Hệ thống từ chối submit và hiển thị thông báo lỗi bắt buộc nhập cho trường Số điện thoại. |
| [FR04-P-BVA-TC01](../test-cases/profile_management/FR04-P-BVA-TC01.md) | Profile Management - Phone Input | Đặng Trường Nguyên | Passed | None | Hệ thống từ chối số điện thoại, yêu cầu nhập đúng 9-10 chữ số. |
| [FR04-P-BVA-TC02](../test-cases/profile_management/FR04-P-BVA-TC02.md) | Profile Management - Phone Input | Đặng Trường Nguyên | Failed | BUG-FR04-P-01 - Sai rule validate Số điện thoại | Hệ thống từ chối số điện thoại, yêu cầu nhập đúng 9-10 chữ số. |
| [FR04-P-BVA-TC03](../test-cases/profile_management/FR04-P-BVA-TC03.md) | Profile Management - Phone Input | Đặng Trường Nguyên | Failed | BUG-FR04-P-01 - Sai rule validate Số điện thoại | Hệ thống từ chối số điện thoại, yêu cầu nhập đúng 9-10 chữ số. |
| [FR04-P-BVA-TC04](../test-cases/profile_management/FR04-P-BVA-TC04.md) | Profile Management - Phone Input | Đặng Trường Nguyên | Failed | BUG-FR04-P-01 - Sai rule validate Số điện thoại | Hệ thống từ chối số điện thoại, yêu cầu nhập đúng 9-10 chữ số. |
| [FR04-A-TC01](../test-cases/profile_management/FR04-A-TC01.md) | Profile Management - Address Input | Đặng Trường Nguyên | Failed | BUG-FR04-A-01 - Thiếu validate Địa chỉ giao hàng | Hệ thống cập nhật thành công |
| [FR04-A-BVA-TC01](../test-cases/profile_management/FR04-A-BVA-TC01.md) | Profile Management - Address Input | Đặng Trường Nguyên | Failed | BUG-FR04-A-01 - Thiếu validate Địa chỉ giao hàng | Hệ thống cập nhật thành công |
| [FR04-A-BVA-TC02](../test-cases/profile_management/FR04-A-BVA-TC02.md) | Profile Management - Address Input | Đặng Trường Nguyên | Passed | None | Hệ thống cập nhật thành công |
| [FR04-A-BVA-TC03](../test-cases/profile_management/FR04-A-BVA-TC03.md) | Profile Management - Address Input | Đặng Trường Nguyên | Passed | None | Hệ thống cập nhật thành công |
| [FR04-A-BVA-TC04](../test-cases/profile_management/FR04-A-BVA-TC04.md) | Profile Management - Address Input | Đặng Trường Nguyên | Passed | None | Hệ thống cập nhật thành công |
| [FR04-A-BVA-TC05](../test-cases/profile_management/FR04-A-BVA-TC05.md) | Profile Management - Address Input | Đặng Trường Nguyên | Passed | None | Hệ thống cập nhật thành công |
| [FR04-A-BVA-TC06](../test-cases/profile_management/FR04-A-BVA-TC06.md) | Profile Management - Address Input | Đặng Trường Nguyên | Passed | None | Hệ thống cập nhật thành công |
| [FR04-A-BVA-TC07](../test-cases/profile_management/FR04-A-BVA-TC07.md) | Profile Management - Address Input | Đặng Trường Nguyên | Failed | BUG-FR04-A-01 - Thiếu validate Địa chỉ giao hàng | Hệ thống cập nhật thành công |
| [FR04-N-TC02](../test-cases/profile_management/FR04-N-TC02.md) | Profile Management - Name Input | Đặng Trường Nguyên | Passed | None | Hệ thống cập nhật thành công, tên mới được hiển thị trên hồ sơ người dùng |
| [FR04-P-TC02](../test-cases/profile_management/FR04-P-TC02.md) | Profile Management - Phone Input | Đặng Trường Nguyên | Failed | BUG-FR04-P-01 - Sai rule validate Số điện thoại | Hệ thống từ chối số điện thoại, yêu cầu nhập đúng 9-10 chữ số. |
| [FR04-P-TC03](../test-cases/profile_management/FR04-P-TC03.md) | Profile Management - Phone Input | Đặng Trường Nguyên | Failed | BUG-FR04-P-01 - Sai rule validate Số điện thoại | Hệ thống từ chối số điện thoại, yêu cầu nhập đúng 9-10 chữ số. |
| [FR04-P-TC04](../test-cases/profile_management/FR04-P-TC04.md) | Profile Management - Phone Input | Đặng Trường Nguyên | Passed | None | Hệ thống cập nhật thành công, số điện thoại mới được hiển thị trên hồ sơ người dùng |
| [FR04-P-TC05](../test-cases/profile_management/FR04-P-TC05.md) | Profile Management - Phone Input | Đặng Trường Nguyên | Failed | BUG-FR04-P-01 - Sai rule validate Số điện thoại | Hệ thống từ chối số điện thoại, yêu cầu nhập đúng 9-10 chữ số. |
| [FR04-A-TC02](../test-cases/profile_management/FR04-A-TC02.md) | Profile Management - Address Input | Đặng Trường Nguyên | Passed | None | Hệ thống cập nhật thành công, địa chỉ mới được hiển thị trên hồ sơ người dùng |
| [FR04-A-TC03](../test-cases/profile_management/FR04-A-TC03.md) | Profile Management - Address Input | Đặng Trường Nguyên | Failed | BUG-FR04-A-01 - Thiếu validate Địa chỉ giao hàng | Hệ thống cập nhật thành công, địa chỉ mới gồm các khoảng trắng được hiển thị trên hồ sơ người dùng |
| [FR04-E-TC01](../test-cases/profile_management/FR04-E-TC01.md) | Profile Management - Email Immutability | Đặng Trường Nguyên | Passed | None | Trường email không thể chỉnh sửa |
| [FR04-R-TC01](../test-cases/profile_management/FR04-R-TC01.md) | Profile Management - Role Protection | Đặng Trường Nguyên | Failed | BUG-FR04-R-01 - API cho phép tự đổi role | API trả về cập nhật thành công |
| [FR04-U-TC01](../test-cases/profile_management/FR04-U-TC01.md) | Profile Management - User Ownership/Auth | Đặng Trường Nguyên | Passed | None | API chặn unauthorized access |
| [FR04-U-TC02](../test-cases/profile_management/FR04-U-TC02.md) | Profile Management - User Ownership/Auth | Đặng Trường Nguyên | Passed | None | Hồ sơ của user B không thay đổi, chỉ thay đổi hồ sơ của user A |

## Defect Log

Các test case `Fail` được gom theo root cause để map sang bug report riêng. Chi tiết issue template nằm tại [tests/bug/FR-04.md](../bug/FR-04.md).

| Bug ID | Related TC ID | Tóm tắt | Severity | Status | Evidence / Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| BUG-FR04-N-01 | FR04-N-BVA-TC07 | Thiếu validate độ dài tối đa Họ Tên theo assumption BVA. | Low | Open | Hệ thống chấp nhận Họ Tên 51 ký tự. Evidence bổ sung sau. |
| BUG-FR04-P-01 | FR04-P-BVA-TC02, FR04-P-BVA-TC03, FR04-P-BVA-TC04, FR04-P-TC02, FR04-P-TC03, FR04-P-TC05 | Validation Số điện thoại sai rule FR-04: không chấp nhận số bắt đầu bằng `0` dài 10-11 chữ số và hiển thị rule 9-10 chữ số. | High | Open | Hệ thống từ chối các số hợp lệ `0123456789`, `01234567890` và thông báo sai rule. Evidence bổ sung sau. |
| BUG-FR04-A-01 | FR04-A-TC01, FR04-A-BVA-TC01, FR04-A-BVA-TC07, FR04-A-TC03 | Thiếu validate bắt buộc, trim và giới hạn độ dài cho Địa chỉ giao hàng. | Medium | Open | Hệ thống vẫn cập nhật thành công khi address rỗng, quá ngắn, quá dài hoặc chỉ gồm khoảng trắng. Evidence bổ sung sau. |
| BUG-FR04-R-01 | FR04-R-TC01 | API `PUT /api/users/me` cho phép client gửi `role` và tự thay đổi quyền. | High | Open | API trả về cập nhật thành công khi body có `role=admin`. Evidence bổ sung sau. |
