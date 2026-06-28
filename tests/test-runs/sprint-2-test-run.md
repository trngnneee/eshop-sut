# Test Run - Sprint 2

**Ngày thực hiện**: 26/06/2026  
**Người thực hiện**: Khoa
**Môi trường thử nghiệm**: Local Backend API & SQLite database

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
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

### Các Bug phát hiện chi tiết:
1. **Bug #31 (Tăng bộ đếm sai):** Mỗi lần đăng nhập sai, hệ thống ghi nhận tăng số lần đăng nhập sai lên `2` đơn vị thay vì `1`.
2. **Bug #32 (Thời gian khóa sai):** Thời gian tài khoản bị khóa sau khi nhập sai 3 lần liên tiếp là `180` giây (3 phút) thay vì `30` giây theo đặc tả.
3. **Bug #33 (Không nhất quán trạng thái đăng nhập):** Giao dịch ghi nhận trạng thái đăng nhập sai của người dùng không được hoàn thành kịp thời, dẫn đến kết quả đọc số lần đăng nhập sai tiếp theo bị sai lệch.
4. **Bug #34 (Sai tiêu đề trang):** Tiêu đề trang Đăng nhập hiển thị sai thành `"Đăng Ký"` gây hiểu lầm lớn cho người dùng.
5. **Bug #35 (Sai nhãn trường nhập liệu):** Trường nhập địa chỉ email hiển thị nhãn là `"Username"` thay vì `"Email"`.
6. **Bug #36 (Không nhất quán ngôn ngữ):** Nút đăng nhập hiển thị tiếng Anh là `"Sign In"` thay vì tiếng Việt `"Đăng nhập"` (vi phạm quy định ngôn ngữ FR-21).
7. **Bug #37 (Lộ mật khẩu - Bảo mật):** Ô nhập mật khẩu hiển thị rõ ràng trên màn hình dưới dạng văn bản thường thay vì ký tự che dấu (vi phạm FR-22 và SEC-04).
8. **Bug #38 (Thiếu ký hiệu bắt buộc):** Các trường bắt buộc (Email và Mật khẩu) thiếu ký hiệu bắt buộc `*` bên cạnh nhãn (vi phạm FR-22).
9. **Bug #39 (Không xử lý khoảng trắng đầu/cuối của email):** Đăng nhập thất bại khi email nhập vào có chứa khoảng trắng thừa ở đầu hoặc cuối chuỗi.
10. **Bug #40 (Thiếu Rate Limiting):** Hệ thống không giới hạn số lượng yêu cầu đăng nhập liên tiếp từ cùng một nguồn trong khoảng thời gian ngắn, cho phép thực hiện spam/brute-force.
11. **Bug #41 (Thiếu Loading state):** Nút Đăng nhập không đổi trạng thái và không disable khi đang gửi API.
12. **Bug #42 (Thiếu nút Toggle Show/Hide):** Mật khẩu cố định hiển thị text và không có nút ẩn hiện.
13. **Bug #43 (Token đăng nhập không hết hạn):** Chuỗi token xác thực sau khi đăng nhập thành công không có thời hạn hết hạn, giúp người dùng duy trì phiên đăng nhập vô thời hạn.
14. **Bug #44 (Thiếu Route Guard):** Đã đăng nhập nhưng vẫn vào được trang `/login` bình thường.
15. **Bug #46 (Giao diện Admin Login lỗi UI/UX):** Giao diện đăng nhập trang Web Admin thiếu nhãn label bên ngoài (khiến placeholder biến mất khi nhập liệu), thiếu dấu hoa thị `*` bắt buộc, thiếu nút Toggle ẩn/hiện mật khẩu, nút submit tiếng Anh `"Login"` và thiếu thuộc tính `type="email"` ở trường Email.
16. **Bug #47 (Thông báo lỗi bằng alert() ở Admin):** Khi đăng nhập thất bại ở Web Admin, hệ thống hiển thị thông báo lỗi bằng hộp thoại pop-up mặc định của trình duyệt (alert dialog) khiến tiêu đề hiển thị chữ `"Code"` hoặc domain name chạy local, vi phạm quy tắc hiển thị thông báo lỗi phía trên nút submit của FR-22.
17. **Bug #47 (Reset mật khẩu không mở khóa tài khoản):** Sau khi thực hiện khôi phục/đổi mật khẩu thành công, tài khoản bị khóa trước đó vẫn ở trạng thái bị khóa và không thể đăng nhập.
