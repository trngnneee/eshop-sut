# Test Run - Sprint 2

**Ngày thực hiện**: 26/06/2026  
**Người thực hiện**: AI Tester (Antigravity)
**Môi trường thử nghiệm**: Local Backend API & SQLite database

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [TC-LOGIN-001](../test-cases/login/TC-LOGIN-001.md) | Login | AI Tester | Pass | None | Đăng nhập thành công với tài khoản đúng và nhận JWT token. |
| [TC-LOGIN-002](../test-cases/login/TC-LOGIN-002.md) | Login | AI Tester | Fail | #31, #33 | Bộ đếm `login_attempts` tăng thêm 2 sau mỗi lần sai và ghi DB bất đồng bộ gây race condition. |
| [TC-LOGIN-003](../test-cases/login/TC-LOGIN-003.md) | Login | AI Tester | Fail | #32 | Tài khoản bị khóa trong 180 giây (3 phút) thay vì 30 giây như đặc tả. |
| [TC-LOGIN-004](../test-cases/login/TC-LOGIN-004.md) | Login | AI Tester | Fail | #34, #35, #36, #37, #38, #45, #46 | Hàng loạt lỗi UI: tiêu đề sai, nhãn Username thay vì Email, nút tiếng Anh, mật khẩu không ẩn, thiếu dấu * bắt buộc. |
| [TC-LOGIN-005](../test-cases/login/TC-LOGIN-005.md) | Login | AI Tester | Fail | #39 | Hệ thống không trim khoảng trắng ở email khi gửi login lên backend. |
| [TC-LOGIN-006](../test-cases/login/TC-LOGIN-006.md) | Login | AI Tester | Pass | None | Token JWT được tạo hợp lệ và dùng để xác thực API /api/users/me thành công. |
| [TC-LOGIN-007](../test-cases/login/TC-LOGIN-007.md) | Login | AI Tester | Pass | None | Hệ thống sử dụng Parameterized Query nên chống tấn công SQL Injection thành công. |
| [TC-LOGIN-008](../test-cases/login/TC-LOGIN-008.md) | Login | AI Tester | Fail | #40 | Không cấu hình middleware Rate Limiting ở API Đăng nhập. |
| [TC-LOGIN-009](../test-cases/login/TC-LOGIN-009.md) | Login | AI Tester | Fail | #41 | Nút Đăng nhập không hiển thị trạng thái loading và không bị vô hiệu hóa khi đang gửi yêu cầu. |
| [TC-LOGIN-010](../test-cases/login/TC-LOGIN-010.md) | Login | AI Tester | Fail | #42 | Không có nút Toggle ẩn/hiện mật khẩu trên giao diện. |
| [TC-LOGIN-011](../test-cases/login/TC-LOGIN-011.md) | Login | AI Tester | Fail | #43 | Token JWT được ký không có thời gian hết hạn (exp), tồn tại vĩnh viễn. |
| [TC-LOGIN-012](../test-cases/login/TC-LOGIN-012.md) | Login | AI Tester | Fail | #44 | Đã đăng nhập nhưng vẫn truy cập được bình thường vào trang Đăng nhập (thiếu Route Guard). |
| [TC-LOGIN-013](../test-cases/login/TC-LOGIN-013.md) | Login | AI Tester | Fail | #33 | Bộ đếm `login_attempts` không được cập nhật đồng bộ về 0 ngay sau khi login thành công do race condition. |
| [TC-LOGIN-014](../test-cases/login/TC-LOGIN-014.md) | Login | AI Tester | Fail | #32 | Thời gian khóa thực tế là 180 giây khiến việc tự động mở khóa ở giây thứ 30 bị thất bại. |
| [TC-LOGIN-015](../test-cases/login/TC-LOGIN-015.md) | Login | AI Tester | Fail | None | Backend không kiểm tra định dạng email và trực tiếp thực hiện truy vấn CSDL. |
| [TC-LOGIN-016](../test-cases/login/TC-LOGIN-016.md) | Login | AI Tester | Pass | None | Các trường nhập liệu được mã hóa đầu ra an toàn bởi React và không thực thi mã script. |
| [TC-LOGIN-017](../test-cases/login/TC-LOGIN-017.md) | Login | AI Tester | Pass | None | Giao diện khôi phục trạng thái nút bấm và báo lỗi kết nối mạng an toàn khi mất mạng. |
| [TC-LOGIN-018](../test-cases/login/TC-LOGIN-018.md) | Login | AI Tester | Pass | None | Hệ thống không tự động điền hay thực hiện đăng nhập từ các tham số email/mật khẩu trên URL. |
| [TC-LOGIN-019](../test-cases/login/TC-LOGIN-019.md) | Login | AI Tester | Pass | None | Backend tự động từ chối thuật toán ký JWT giả mạo 'none' bảo vệ API. |
| [TC-LOGIN-020](../test-cases/login/TC-LOGIN-020.md) | Login | AI Tester | Fail | #45 | Thứ tự tab di chuyển bị lỗi (nút submit focus trước) và thiếu hoàn toàn aria-label trên các input. |
| [TC-LOGIN-021](../test-cases/login/TC-LOGIN-021.md) | Login | AI Tester | Fail | #45 | Các input thiếu thuộc tính autocomplete và name tiêu chuẩn tương thích trình quản lý mật khẩu. |
| [TC-LOGIN-022](../test-cases/login/TC-LOGIN-022.md) | Login | AI Tester | Pass | None | Express body-parser mặc định từ chối các request body vượt quá 100kb bằng HTTP 413. |
| [TC-LOGIN-023](../test-cases/login/TC-LOGIN-023.md) | Login | AI Tester | Fail | #31, #33 | Bộ đếm `login_attempts` tăng thêm 2 sau mỗi lần sai khiến lockout xảy ra sau 2 lần sai thay vì 3. |
| [TC-LOGIN-024](../test-cases/login/TC-LOGIN-024.md) | Login | AI Tester | Fail | #33 | Race condition bất đồng bộ khiến `login_attempts` không được reset về 0 kịp thời khi đăng nhập đúng xen kẽ. |
| [TC-LOGIN-025](../test-cases/login/TC-LOGIN-025.md) | Login | AI Tester | Fail | #32 | Tổng thời gian khóa thực tế là 180s thay vì 30s. |
| [TC-LOGIN-026](../test-cases/login/TC-LOGIN-026.md) | Login | AI Tester | Pass | None | Đăng nhập đúng khi đang khóa trả về HTTP 403 Forbidden và không sinh JWT token. |
| [TC-LOGIN-027](../test-cases/login/TC-LOGIN-027.md) | Login | AI Tester | Pass | None | Trạng thái khóa đồng bộ lập tức qua DB giúp ngăn các client/tab khác truy cập. |
| [TC-LOGIN-028](../test-cases/login/TC-LOGIN-028.md) | Login | AI Tester | Pass | None | Đăng nhập với email khác casing sẽ bị từ chối đăng nhập (đây là hành vi được thiết kế của hệ thống). |
| [TC-LOGIN-029](../test-cases/login/TC-LOGIN-029.md) | Login | AI Tester | Pass | None | Bộ đếm `login_attempts` giữ nguyên bằng 0 khi đăng nhập thành công. |
| [TC-LOGIN-030](../test-cases/login/TC-LOGIN-030.md) | Login | AI Tester | Fail | #47 | API reset mật khẩu thành công nhưng không giải phóng `locked_until` và `login_attempts` trong CSDL. |

### Các Bug phát hiện chi tiết:
1. **Bug #31 (Tăng bộ đếm sai):** Ở `backend/server.js:54`, code tăng bộ đếm thêm `2` đơn vị: `const newAttempts = user.login_attempts + 2;` thay vì `1`.
2. **Bug #32 (Thời gian khóa sai):** Ở `backend/server.js:57`, thời gian khóa được thiết lập là `180000` ms (3 phút) thay vì `30000` ms (30 giây): `lockedUntil = new Date(Date.now() + 180000).toISOString()`.
3. **Bug #33 (Race Condition bất đồng bộ):** Phản hồi API đăng nhập sai được gửi về client (`res.status(401)`) song song và không đợi giao dịch ghi DB (`db.run`) hoàn tất, dẫn đến việc đọc trạng thái DB ngay sau đó bị sai lệch.
4. **Bug #34 (Sai tiêu đề trang):** Tiêu đề trang Đăng nhập hiển thị sai thành `"Đăng Ký"` gây hiểu lầm lớn cho người dùng.
5. **Bug #35 (Sai nhãn trường nhập liệu):** Trường nhập địa chỉ email hiển thị nhãn là `"Username"` thay vì `"Email"`.
6. **Bug #36 (Không nhất quán ngôn ngữ):** Nút đăng nhập hiển thị tiếng Anh là `"Sign In"` thay vì tiếng Việt `"Đăng nhập"` (vi phạm quy định ngôn ngữ FR-21).
7. **Bug #37 (Lộ mật khẩu - Bảo mật):** Ô nhập mật khẩu có thuộc tính `type="text"` thay vì `type="password"`, khiến mật khẩu của người dùng bị hiển thị rõ ràng trên màn hình dưới dạng văn bản thường (vi phạm FR-22 và SEC-04).
8. **Bug #38 (Thiếu ký hiệu bắt buộc):** Các trường bắt buộc (Email và Mật khẩu) thiếu ký hiệu bắt buộc `*` bên cạnh nhãn (vi phạm FR-22).
9. **Bug #39 (Thiếu trim email ở backend):** Gửi email có khoảng trắng đầu/cuối sẽ đăng nhập thất bại do backend so khớp trực tiếp chuỗi gốc với database.
10. **Bug #40 (Thiếu Rate Limiting):** Không có middleware kiểm soát tần suất yêu cầu ở backend API, cho phép spam brute-force mật độ cao.
11. **Bug #41 (Thiếu Loading state):** Nút Đăng nhập không đổi trạng thái và không disable khi đang gửi API.
12. **Bug #42 (Thiếu nút Toggle Show/Hide):** Mật khẩu cố định hiển thị text và không có nút ẩn hiện.
13. **Bug #43 (Token vô hạn hạn):** Token JWT không được thiết lập trường `exp` khi ký, tồn tại vô thời hạn.
14. **Bug #44 (Thiếu Route Guard):** Đã đăng nhập nhưng vẫn vào được trang `/login` bình thường.
15. **Bug #46 (Giao diện Admin Login lỗi UI/UX):** Giao diện đăng nhập trang Web Admin (port 5174) thiếu nhãn label bên ngoài (khiến placeholder biến mất khi nhập liệu), thiếu dấu hoa thị `*` bắt buộc, thiếu nút Toggle ẩn/hiện mật khẩu, nút submit tiếng Anh `"Login"` và thiếu thuộc tính `type="email"` ở trường Email.
16. **Bug #47 (Thông báo lỗi bằng alert() ở Admin):** Khi đăng nhập thất bại ở Web Admin, hệ thống gọi hàm `alert()` hiển thị hộp thoại trình duyệt với tiêu đề `"Code"` (do host editor) hoặc domain name, vi phạm quy tắc hiển thị thông báo lỗi phía trên nút submit của FR-22.
17. **Bug #47 (Reset mật khẩu không mở khóa):** Ở `backend/server.js:89`, API cập nhật mật khẩu mới chỉ set `password` và `reset_token = NULL`, không reset `login_attempts` and `locked_until`. Tài khoản vẫn bị khóa sau khi đổi mật khẩu thành công.
