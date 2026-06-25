# Test Run - FR-04 Profile Management

**Ngày thực hiện**: 25/06/2026  
**Người thực hiện**: Dang Truong Nguyen (23127438)  
**Môi trường thử nghiệm**: Local Frontend Web, Backend API, SQLite database, Postman/API check khi cần  
**Nguồn thiết kế test**: `23127438/23127438.md`  
**Nguồn kết quả chạy test & bug report**: `23127438/bug_report/FR-04.md`

## Tổng quan kết quả

| Nhóm input | Domain TC | BVA TC | Tổng TC | Pass | Fail |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Họ tên | 11 | 7 | 18 | 7 | 11 |
| Số điện thoại | 12 | 7 | 19 | 0 | 19 |
| Địa chỉ | 12 | 7 | 19 | 7 | 12 |
| **Tổng** | **35** | **21** | **56** | **14** | **42** |

## Test Case Execution Report

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [FR04-N-TC01](../test-cases/profile_management/FR04-N-TC01.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Pass | None | Chấp nhận cập nhật; hồ sơ lưu/hiển thị đúng họ tên này. |
| [FR04-N-TC02](../test-cases/profile_management/FR04-N-TC02.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Pass | None | Chấp nhận cập nhật; hồ sơ lưu/hiển thị đúng họ tên này. |
| [FR04-N-TC03](../test-cases/profile_management/FR04-N-TC03.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-N-01 | Hệ thống chấp nhận nhưng giá trị lưu/hiển thị không được chuẩn hóa trim như kỳ vọng. (BUG-FR04-N-01) |
| [FR04-N-TC04](../test-cases/profile_management/FR04-N-TC04.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-N-02 | Frontend có báo lỗi, nhưng khi thử bằng Postman/API thì profile vẫn bị cập nhật bằng giá trị rỗng. (BUG-FR04-N-02) |
| [FR04-N-TC05](../test-cases/profile_management/FR04-N-TC05.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-N-02 | Hệ thống chấp nhận và lưu/hiển thị họ tên chỉ gồm khoảng trắng. (BUG-FR04-N-02) |
| [FR04-N-TC06](../test-cases/profile_management/FR04-N-TC06.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-N-03 | Hệ thống chấp nhận và lưu/hiển thị họ tên có chữ số. (BUG-FR04-N-03) |
| [FR04-N-TC07](../test-cases/profile_management/FR04-N-TC07.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-N-03 | Hệ thống chấp nhận và lưu/hiển thị họ tên có ký tự đặc biệt. (BUG-FR04-N-03) |
| [FR04-N-TC08](../test-cases/profile_management/FR04-N-TC08.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-N-03 | Hệ thống chấp nhận và lưu/hiển thị họ tên có emoji. (BUG-FR04-N-03) |
| [FR04-N-TC09](../test-cases/profile_management/FR04-N-TC09.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-N-04 | Hệ thống chấp nhận và lưu/hiển thị payload script trong họ tên; script không thực thi. (BUG-FR04-N-04) |
| [FR04-N-TC10](../test-cases/profile_management/FR04-N-TC10.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-N-05 | API chấp nhận request và cập nhật profile thành công. (BUG-FR04-N-05) |
| [FR04-N-TC11](../test-cases/profile_management/FR04-N-TC11.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-N-05 | API chấp nhận request và lưu/hiển thị họ tên dạng số. (BUG-FR04-N-05) |
| [FR04-N-BVA-TC01](../test-cases/profile_management/FR04-N-BVA-TC01.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-N-02 | Frontend có báo lỗi, nhưng khi thử bằng Postman/API thì profile vẫn bị cập nhật bằng giá trị rỗng. (BUG-FR04-N-02) |
| [FR04-N-BVA-TC02](../test-cases/profile_management/FR04-N-BVA-TC02.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Pass | None | Chấp nhận cập nhật; hồ sơ lưu/hiển thị `A`. |
| [FR04-N-BVA-TC03](../test-cases/profile_management/FR04-N-BVA-TC03.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Pass | None | Chấp nhận cập nhật; hồ sơ lưu/hiển thị `An`. |
| [FR04-N-BVA-TC04](../test-cases/profile_management/FR04-N-BVA-TC04.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Pass | None | Chấp nhận cập nhật; hồ sơ lưu/hiển thị họ tên 25 ký tự. |
| [FR04-N-BVA-TC05](../test-cases/profile_management/FR04-N-BVA-TC05.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Pass | None | Chấp nhận cập nhật; hồ sơ lưu/hiển thị họ tên 49 ký tự. |
| [FR04-N-BVA-TC06](../test-cases/profile_management/FR04-N-BVA-TC06.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Pass | None | Chấp nhận cập nhật; hồ sơ lưu/hiển thị họ tên 50 ký tự. |
| [FR04-N-BVA-TC07](../test-cases/profile_management/FR04-N-BVA-TC07.md) | Profile Management - Họ tên | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-N-06 | Hệ thống chấp nhận và lưu/hiển thị họ tên 51 ký tự. (BUG-FR04-N-06) |
| [FR04-P-TC01](../test-cases/profile_management/FR04-P-TC01.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-01 | Bị từ chối với thông báo `Invalid phone number format`. (BUG-FR04-P-01) |
| [FR04-P-TC02](../test-cases/profile_management/FR04-P-TC02.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-01 | Bị từ chối với thông báo `Invalid phone number format`. (BUG-FR04-P-01) |
| [FR04-P-TC03](../test-cases/profile_management/FR04-P-TC03.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-01 | Bị từ chối với thông báo `Invalid phone number format`. (BUG-FR04-P-01) |
| [FR04-P-TC04](../test-cases/profile_management/FR04-P-TC04.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-04 | Bị từ chối với thông báo chung `Invalid phone number format`. (BUG-FR04-P-04) |
| [FR04-P-TC05](../test-cases/profile_management/FR04-P-TC05.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-04 | Bị từ chối với thông báo chung `Invalid phone number format`. (BUG-FR04-P-04) |
| [FR04-P-TC06](../test-cases/profile_management/FR04-P-TC06.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-02 | API chấp nhận request và cập nhật profile. (BUG-FR04-P-02) |
| [FR04-P-TC07](../test-cases/profile_management/FR04-P-TC07.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-04 | Bị từ chối với thông báo chung `Invalid phone number format`. (BUG-FR04-P-04) |
| [FR04-P-TC08](../test-cases/profile_management/FR04-P-TC08.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-04 | Bị từ chối với thông báo chung `Invalid phone number format`. (BUG-FR04-P-04) |
| [FR04-P-TC09](../test-cases/profile_management/FR04-P-TC09.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-03 | Hệ thống chấp nhận và cập nhật profile. (BUG-FR04-P-03) |
| [FR04-P-TC10](../test-cases/profile_management/FR04-P-TC10.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-04 | Bị từ chối với thông báo chung `Invalid phone number format`. (BUG-FR04-P-04) |
| [FR04-P-TC11](../test-cases/profile_management/FR04-P-TC11.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-04 | Bị từ chối với thông báo chung `Invalid phone number format`. (BUG-FR04-P-04) |
| [FR04-P-TC12](../test-cases/profile_management/FR04-P-TC12.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-02 | API chấp nhận request và cập nhật profile. (BUG-FR04-P-02) |
| [FR04-P-BVA-TC01](../test-cases/profile_management/FR04-P-BVA-TC01.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-03 | Hệ thống chấp nhận và cập nhật profile. (BUG-FR04-P-03) |
| [FR04-P-BVA-TC02](../test-cases/profile_management/FR04-P-BVA-TC02.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-01 | Bị từ chối với thông báo `Invalid phone number format`. (BUG-FR04-P-01) |
| [FR04-P-BVA-TC03](../test-cases/profile_management/FR04-P-BVA-TC03.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-01 | Bị từ chối với thông báo `Invalid phone number format`. (BUG-FR04-P-01) |
| [FR04-P-BVA-TC04](../test-cases/profile_management/FR04-P-BVA-TC04.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-01 | Bị từ chối với thông báo `Invalid phone number format`. (BUG-FR04-P-01) |
| [FR04-P-BVA-TC05](../test-cases/profile_management/FR04-P-BVA-TC05.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-01 | Bị từ chối với thông báo `Invalid phone number format`. (BUG-FR04-P-01) |
| [FR04-P-BVA-TC06](../test-cases/profile_management/FR04-P-BVA-TC06.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-01 | Bị từ chối với thông báo `Invalid phone number format`. (BUG-FR04-P-01) |
| [FR04-P-BVA-TC07](../test-cases/profile_management/FR04-P-BVA-TC07.md) | Profile Management - Số điện thoại | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-P-04 | Bị từ chối với thông báo chung `Invalid phone number format`. (BUG-FR04-P-04) |
| [FR04-A-TC01](../test-cases/profile_management/FR04-A-TC01.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Pass | None | Chấp nhận cập nhật; hồ sơ lưu/hiển thị đúng địa chỉ này. |
| [FR04-A-TC02](../test-cases/profile_management/FR04-A-TC02.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Pass | None | Chấp nhận cập nhật; hồ sơ lưu/hiển thị đúng địa chỉ này. |
| [FR04-A-TC03](../test-cases/profile_management/FR04-A-TC03.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-A-01 | Hệ thống chấp nhận nhưng địa chỉ lưu/hiển thị không được trim. (BUG-FR04-A-01) |
| [FR04-A-TC04](../test-cases/profile_management/FR04-A-TC04.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-A-02 | Hệ thống chấp nhận và lưu/hiển thị địa chỉ rỗng. (BUG-FR04-A-02) |
| [FR04-A-TC05](../test-cases/profile_management/FR04-A-TC05.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-A-02 | Hệ thống chấp nhận và lưu/hiển thị địa chỉ chỉ gồm khoảng trắng. (BUG-FR04-A-02) |
| [FR04-A-TC06](../test-cases/profile_management/FR04-A-TC06.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-A-02 | Hệ thống chấp nhận và lưu/hiển thị địa chỉ này. (BUG-FR04-A-02) |
| [FR04-A-TC07](../test-cases/profile_management/FR04-A-TC07.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-A-03 | Hệ thống chấp nhận và lưu/hiển thị payload script trong địa chỉ. (BUG-FR04-A-03) |
| [FR04-A-TC08](../test-cases/profile_management/FR04-A-TC08.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-A-03 | Hệ thống chấp nhận/lưu giá trị dạng HTML; có lần hiển thị lại payload script đã lưu trước đó. (BUG-FR04-A-03) |
| [FR04-A-TC09](../test-cases/profile_management/FR04-A-TC09.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-A-04 | Hệ thống chấp nhận và lưu/hiển thị địa chỉ có emoji. (BUG-FR04-A-04) |
| [FR04-A-TC10](../test-cases/profile_management/FR04-A-TC10.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-A-04 | Hệ thống chấp nhận và lưu/hiển thị địa chỉ có ký hiệu `@` và `#`. (BUG-FR04-A-04) |
| [FR04-A-TC11](../test-cases/profile_management/FR04-A-TC11.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-A-05 | API chấp nhận request và cập nhật profile. (BUG-FR04-A-05) |
| [FR04-A-TC12](../test-cases/profile_management/FR04-A-TC12.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-A-05 | API chấp nhận request và cập nhật profile. (BUG-FR04-A-05) |
| [FR04-A-BVA-TC01](../test-cases/profile_management/FR04-A-BVA-TC01.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-A-02 | Hệ thống chấp nhận và lưu/hiển thị `Addr`. (BUG-FR04-A-02) |
| [FR04-A-BVA-TC02](../test-cases/profile_management/FR04-A-BVA-TC02.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Pass | None | Chấp nhận cập nhật; hồ sơ lưu/hiển thị `House`. |
| [FR04-A-BVA-TC03](../test-cases/profile_management/FR04-A-BVA-TC03.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Pass | None | Chấp nhận cập nhật; hồ sơ lưu/hiển thị `House1`. |
| [FR04-A-BVA-TC04](../test-cases/profile_management/FR04-A-BVA-TC04.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Pass | None | Chấp nhận cập nhật; hồ sơ lưu/hiển thị địa chỉ 130 ký tự. |
| [FR04-A-BVA-TC05](../test-cases/profile_management/FR04-A-BVA-TC05.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Pass | None | Chấp nhận cập nhật; hồ sơ lưu/hiển thị địa chỉ 254 ký tự. |
| [FR04-A-BVA-TC06](../test-cases/profile_management/FR04-A-BVA-TC06.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Pass | None | Chấp nhận cập nhật; hồ sơ lưu/hiển thị địa chỉ 255 ký tự. |
| [FR04-A-BVA-TC07](../test-cases/profile_management/FR04-A-BVA-TC07.md) | Profile Management - Địa chỉ | Dang Truong Nguyen (23127438) | Fail | BUG-FR04-A-06 | Hệ thống chấp nhận và lưu/hiển thị địa chỉ 256 ký tự. (BUG-FR04-A-06) |

## Defect Log

Kết quả chạy có **56** test case: **14 Pass** và **42 Fail**. Các lỗi fail được gom thành **16** defect để tránh lặp root cause.

### Thống kê severity

| Severity | Count |
| :--- | ---: |
| High | 9 |
| Medium | 6 |
| Low | 1 |
| **Total Open Defects** | **16** |

### Danh sách defect

| Bug ID | Related TC ID | Tóm tắt | Severity | Status | Evidence / Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| BUG-FR04-N-01 | FR04-N-TC03 | Họ tên có khoảng trắng đầu/cuối không được chuẩn hóa trim | Medium | Open | Giá trị có khoảng trắng đầu/cuối được chấp nhận nhưng không khớp kỳ vọng trim trước khi lưu/hiển thị. |
| BUG-FR04-N-02 | FR04-N-TC04, FR04-N-TC05, FR04-N-BVA-TC01 | API thiếu hoặc không nhất quán validation bắt buộc nhập họ tên | High | Open | Giá trị rỗng/chỉ khoảng trắng có thể được cập nhật qua API/Postman dù frontend có validation. |
| BUG-FR04-N-03 | FR04-N-TC06, FR04-N-TC07, FR04-N-TC08 | Họ tên chấp nhận ký tự không hợp lệ | Medium | Open | Họ tên chứa chữ số, ký hiệu và emoji vẫn được lưu/hiển thị. |
| BUG-FR04-N-04 | FR04-N-TC09 | Họ tên chấp nhận payload dạng script | High | Open | `<script>alert(1)</script>` được lưu/hiển thị trong họ tên, dù không thực thi. |
| BUG-FR04-N-05 | FR04-N-TC10, FR04-N-TC11 | API chấp nhận họ tên bị thiếu hoặc không phải chuỗi | High | Open | Request thiếu `name` hoặc gửi `name` dạng number vẫn được cập nhật thành công. |
| BUG-FR04-N-06 | FR04-N-BVA-TC07 | Không enforce độ dài tối đa 50 ký tự cho họ tên | Medium | Open | Họ tên 51 ký tự vẫn được lưu/hiển thị. |
| BUG-FR04-P-01 | FR04-P-TC01, FR04-P-TC02, FR04-P-TC03, FR04-P-BVA-TC02, FR04-P-BVA-TC03, FR04-P-BVA-TC04, FR04-P-BVA-TC05, FR04-P-BVA-TC06 | Số điện thoại Việt Nam hợp lệ bị từ chối | High | Open | Các format bắt đầu bằng `0` hoặc `+84` bị báo `Invalid phone number format`. |
| BUG-FR04-P-02 | FR04-P-TC06, FR04-P-TC12 | API chấp nhận số điện thoại bị thiếu hoặc không phải chuỗi | High | Open | Request thiếu `phone` hoặc gửi `phone` dạng number vẫn cập nhật profile. |
| BUG-FR04-P-03 | FR04-P-TC09, FR04-P-BVA-TC01 | Số điện thoại sai prefix hoặc dưới minimum vẫn được chấp nhận | High | Open | Số bắt đầu bằng `1` và số 9 chữ số bắt đầu bằng `9` vẫn được cập nhật. |
| BUG-FR04-P-04 | FR04-P-TC04, FR04-P-TC05, FR04-P-TC07, FR04-P-TC08, FR04-P-TC10, FR04-P-TC11, FR04-P-BVA-TC07 | Thông báo lỗi số điện thoại quá chung chung | Low | Open | Nhiều nguyên nhân invalid khác nhau đều trả về `Invalid phone number format`. |
| BUG-FR04-A-01 | FR04-A-TC03 | Địa chỉ có khoảng trắng đầu/cuối không được trim | Medium | Open | Địa chỉ có leading/trailing spaces được chấp nhận nhưng không chuẩn hóa như kỳ vọng. |
| BUG-FR04-A-02 | FR04-A-TC04, FR04-A-TC05, FR04-A-TC06, FR04-A-BVA-TC01 | Không enforce required/min length cho địa chỉ | High | Open | Địa chỉ rỗng, chỉ khoảng trắng, 4 ký tự và dưới minimum vẫn được lưu/hiển thị. |
| BUG-FR04-A-03 | FR04-A-TC07, FR04-A-TC08 | Địa chỉ chấp nhận payload script/HTML | High | Open | Giá trị dạng `<script>` và thẻ HTML vẫn được lưu/hiển thị. |
| BUG-FR04-A-04 | FR04-A-TC09, FR04-A-TC10 | Địa chỉ chấp nhận emoji và ký hiệu không hỗ trợ | Medium | Open | Địa chỉ chứa emoji, `@`, `#` vẫn được lưu/hiển thị. |
| BUG-FR04-A-05 | FR04-A-TC11, FR04-A-TC12 | API chấp nhận địa chỉ bị thiếu hoặc không phải chuỗi | High | Open | Request thiếu `shipping_address` hoặc gửi dạng number vẫn cập nhật profile. |
| BUG-FR04-A-06 | FR04-A-BVA-TC07 | Không enforce độ dài tối đa 255 ký tự cho địa chỉ | Medium | Open | Địa chỉ 256 ký tự vẫn được lưu/hiển thị. |
