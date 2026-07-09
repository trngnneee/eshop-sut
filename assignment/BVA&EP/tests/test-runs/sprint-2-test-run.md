# Test Run - Sprint 2 (Login Module FR-02)

**Ngày thực hiện**: 26/06/2026  
**Người thực hiện**: Đặng Đăng Khoa  
**Môi trường thử nghiệm**: Local Backend API & SQLite database

## Bảng kết quả thực thi (Test Run Table)

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [TC-API-001](../test-cases/login/TC-API-001.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-API-002](../test-cases/login/TC-API-002.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-API-003](../test-cases/login/TC-API-003.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-API-004](../test-cases/login/TC-API-004.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-API-005](../test-cases/login/TC-API-005.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-API-006](../test-cases/login/TC-API-006.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-API-007](../test-cases/login/TC-API-007.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-ERR-001](../test-cases/login/TC-ERR-001.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-ERR-002](../test-cases/login/TC-ERR-002.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-ERR-003](../test-cases/login/TC-ERR-003.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-ERR-004](../test-cases/login/TC-ERR-004.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-ERR-005](../test-cases/login/TC-ERR-005.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-ERR-006](../test-cases/login/TC-ERR-006.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-ERR-007](../test-cases/login/TC-ERR-007.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-JWT-001](../test-cases/login/TC-JWT-001.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-JWT-002](../test-cases/login/TC-JWT-002.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-JWT-003](../test-cases/login/TC-JWT-003.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-JWT-004](../test-cases/login/TC-JWT-004.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-JWT-005](../test-cases/login/TC-JWT-005.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-JWT-006](../test-cases/login/TC-JWT-006.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOCK-BVA-001](../test-cases/login/TC-LOCK-BVA-001.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOCK-BVA-002](../test-cases/login/TC-LOCK-BVA-002.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOCK-BVA-003](../test-cases/login/TC-LOCK-BVA-003.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOCK-BVA-004](../test-cases/login/TC-LOCK-BVA-004.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOCK-BVA-005](../test-cases/login/TC-LOCK-BVA-005.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOCK-BVA-006](../test-cases/login/TC-LOCK-BVA-006.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOCK-BVA-007](../test-cases/login/TC-LOCK-BVA-007.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-001](../test-cases/login/TC-LOGIN-001.md) | Login | Khoa | Pass | None | Đăng nhập thành công với tài khoản đúng và nhận JWT token. |
| [TC-LOGIN-002](../test-cases/login/TC-LOGIN-002.md) | Login | Khoa | Fail | #31, #33 | Bộ đếm đăng nhập sai tăng thêm 2 sau mỗi lần nhập sai, khiến tài khoản bị khóa nhanh hơn quy trình. |
| [TC-LOGIN-003](../test-cases/login/TC-LOGIN-003.md) | Login | Khoa | Fail | #32 | Tài khoản bị khóa trong 180 giây (3 phút) thay vì 30 giây như đặc tả. |
| [TC-LOGIN-004](../test-cases/login/TC-LOGIN-004.md) | Login | Khoa | Fail | #34, #35, #36, #37, #38, #45, #46 | Hàng loạt lỗi UI: tiêu đề sai, nhãn Username thay vì Email, nút tiếng Anh, mật khẩu không ẩn, thiếu dấu * bắt buộc. |
| [TC-LOGIN-005](../test-cases/login/TC-LOGIN-005.md) | Login | Khoa | Fail | #39 | Hệ thống không tự động loại bỏ khoảng trắng thừa ở email khi gửi yêu cầu đăng nhập. |
| [TC-LOGIN-006](../test-cases/login/TC-LOGIN-006.md) | Login | Khoa | Pass | None | Token xác thực đăng nhập được tạo hợp lệ và truy cập được thông tin cá nhân. |
| [TC-LOGIN-007](../test-cases/login/TC-LOGIN-007.md) | Login | Khoa | Pass | None | Hệ thống chống tấn công SQL Injection thành công khi gửi các payload độc hại qua form đăng nhập. |
| [TC-LOGIN-008](../test-cases/login/TC-LOGIN-008.md) | Login | Khoa | Fail | #40 | Không giới hạn số lần yêu cầu (Rate Limiting) liên tiếp gửi lên API Đăng nhập. |
| [TC-LOGIN-009](../test-cases/login/TC-LOGIN-009.md) | Login | Khoa | Fail | #41 | Nút Đăng nhập không hiển thị trạng thái loading và không bị vô hiệu hóa khi đang gửi yêu cầu. |
| [TC-LOGIN-010](../test-cases/login/TC-LOGIN-010.md) | Login | Khoa | Fail | #42 | Không có nút Toggle ẩn/hiện mật khẩu trên giao diện. |
| [TC-LOGIN-011](../test-cases/login/TC-LOGIN-011.md) | Login | Khoa | Fail | #43 | Token xác thực đăng nhập không có thời gian hết hạn, tồn tại vĩnh viễn. |
| [TC-LOGIN-012](../test-cases/login/TC-LOGIN-012.md) | Login | Khoa | Fail | #44 | Đã đăng nhập nhưng vẫn truy cập được bình thường vào trang Đăng nhập (thiếu Route Guard). |
| [TC-LOGIN-013](../test-cases/login/TC-LOGIN-013.md) | Login | Khoa | Fail | #33 | Bộ đếm lần đăng nhập sai không được hoàn tác về 0 kịp thời ngay sau khi đăng nhập thành công. |
| [TC-LOGIN-014](../test-cases/login/TC-LOGIN-014.md) | Login | Khoa | Fail | #32 | Thời gian khóa thực tế là 180 giây khiến việc tự động mở khóa ở giây thứ 30 bị thất bại. |
| [TC-LOGIN-015](../test-cases/login/TC-LOGIN-015.md) | Login | Khoa | Fail | None | Hệ thống chấp nhận định dạng email không hợp lệ khi kiểm tra dữ liệu đầu vào. |
| [TC-LOGIN-016](../test-cases/login/TC-LOGIN-016.md) | Login | Khoa | Pass | None | Các trường nhập liệu được xử lý an toàn và không thực thi mã script chèn vào. |
| [TC-LOGIN-017](../test-cases/login/TC-LOGIN-017.md) | Login | Khoa | Pass | None | Giao diện khôi phục trạng thái nút bấm và báo lỗi kết nối mạng an toàn khi mất mạng. |
| [TC-LOGIN-018](../test-cases/login/TC-LOGIN-018.md) | Login | Khoa | Pass | None | Hệ thống không tự động điền hay thực hiện đăng nhập từ các tham số email/mật khẩu trên URL. |
| [TC-LOGIN-019](../test-cases/login/TC-LOGIN-019.md) | Login | Khoa | Pass | None | Hệ thống từ chối các token xác thực có thuật toán ký giả mạo 'none'. |
| [TC-LOGIN-020](../test-cases/login/TC-LOGIN-020.md) | Login | Khoa | Fail | #45 | Thứ tự tab di chuyển bị lỗi (nút submit focus trước) và thiếu hoàn toàn nhãn hỗ trợ accessibility trên các trường nhập. |
| [TC-LOGIN-021](../test-cases/login/TC-LOGIN-021.md) | Login | Khoa | Fail | #45 | Các trường nhập liệu thiếu thuộc tính autocomplete và name tương thích trình quản lý mật khẩu. |
| [TC-LOGIN-022](../test-cases/login/TC-LOGIN-022.md) | Login | Khoa | Pass | None | API từ chối các gói tin request body vượt quá 100kb bằng mã phản hồi HTTP 413. |
| [TC-LOGIN-023](../test-cases/login/TC-LOGIN-023.md) | Login | Khoa | Fail | #31, #33 | Số lần đăng nhập sai tăng quá nhanh khiến tài khoản bị khóa sai quy trình. |
| [TC-LOGIN-024](../test-cases/login/TC-LOGIN-024.md) | Login | Khoa | Fail | #33 | Số lần đăng nhập sai không được hoàn tác về 0 kịp thời khi đăng nhập đúng xen kẽ. |
| [TC-LOGIN-025](../test-cases/login/TC-LOGIN-025.md) | Login | Khoa | Fail | #32 | Tổng thời gian khóa thực tế là 180s thay vì 30s. |
| [TC-LOGIN-026](../test-cases/login/TC-LOGIN-026.md) | Login | Khoa | Pass | None | Đăng nhập đúng khi đang khóa trả về HTTP 403 Forbidden và không cho phép truy cập. |
| [TC-LOGIN-027](../test-cases/login/TC-LOGIN-027.md) | Login | Khoa | Pass | None | Trạng thái khóa đồng bộ lập tức giúp ngăn các thiết bị khác truy cập tài khoản đang khóa. |
| [TC-LOGIN-028](../test-cases/login/TC-LOGIN-028.md) | Login | Khoa | Pass | None | Đăng nhập với email khác casing sẽ bị từ chối đăng nhập (đây là hành vi được thiết kế của hệ thống). |
| [TC-LOGIN-029](../test-cases/login/TC-LOGIN-029.md) | Login | Khoa | Pass | None | Bộ đếm lần đăng nhập sai giữ nguyên bằng 0 khi đăng nhập thành công. |
| [TC-LOGIN-030](../test-cases/login/TC-LOGIN-030.md) | Login | Khoa | Fail | #47 | Reset mật khẩu thành công nhưng tài khoản vẫn bị giữ trạng thái khóa và không thể đăng nhập. |
| [TC-LOGIN-031](../test-cases/login/TC-LOGIN-031.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-032](../test-cases/login/TC-LOGIN-032.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-033](../test-cases/login/TC-LOGIN-033.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-034](../test-cases/login/TC-LOGIN-034.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-035](../test-cases/login/TC-LOGIN-035.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-036](../test-cases/login/TC-LOGIN-036.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-037](../test-cases/login/TC-LOGIN-037.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-038](../test-cases/login/TC-LOGIN-038.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-039](../test-cases/login/TC-LOGIN-039.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-040](../test-cases/login/TC-LOGIN-040.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-041](../test-cases/login/TC-LOGIN-041.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-BVA-001](../test-cases/login/TC-LOGIN-BVA-001.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-BVA-002](../test-cases/login/TC-LOGIN-BVA-002.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-BVA-003](../test-cases/login/TC-LOGIN-BVA-003.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-BVA-004](../test-cases/login/TC-LOGIN-BVA-004.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-BVA-005](../test-cases/login/TC-LOGIN-BVA-005.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-BVA-006](../test-cases/login/TC-LOGIN-BVA-006.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-BVA-007](../test-cases/login/TC-LOGIN-BVA-007.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-BVA-008](../test-cases/login/TC-LOGIN-BVA-008.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-BVA-009](../test-cases/login/TC-LOGIN-BVA-009.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-BVA-010](../test-cases/login/TC-LOGIN-BVA-010.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-BVA-011](../test-cases/login/TC-LOGIN-BVA-011.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
| [TC-LOGIN-BVA-012](../test-cases/login/TC-LOGIN-BVA-012.md) | Login | Khoa | Pass | None | Thành công (kiểm thử thông thường / xử lý biên). |
