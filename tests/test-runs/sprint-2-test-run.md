# Test Run - Sprint 2

**Ngày thực hiện**: 23/06/2026  
**Người thực hiện**: AI Tester (Antigravity)
**Môi trường thử nghiệm**: Local Backend API & SQLite database

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [TC-LOGIN-001](../test-cases/login/TC-LOGIN-001.md) | Login | AI Tester | Pass | None | Đăng nhập thành công với tài khoản đúng và nhận JWT token. |
| [TC-LOGIN-002](../test-cases/login/TC-LOGIN-002.md) | Login | AI Tester | Fail | #1, #3 | Bộ đếm `login_attempts` tăng thêm 2 sau mỗi lần sai và ghi DB bất đồng bộ gây race condition. |
| [TC-LOGIN-003](../test-cases/login/TC-LOGIN-003.md) | Login | AI Tester | Fail | #2 | Tài khoản bị khóa trong 180 giây (3 phút) thay vì 30 giây như đặc tả. |
| [TC-LOGIN-004](../test-cases/login/TC-LOGIN-004.md) | Login | AI Tester | Fail | #4, #5, #6, #7, #8 | Hàng loạt lỗi UI: tiêu đề sai, nhãn Username thay vì Email, nút tiếng Anh, mật khẩu không ẩn, thiếu dấu * bắt buộc. |
| [TC-LOGIN-005](../test-cases/login/TC-LOGIN-005.md) | Login | AI Tester | Fail | #9 | Hệ thống không trim khoảng trắng ở email khi gửi login lên backend. |
| [TC-LOGIN-006](../test-cases/login/TC-LOGIN-006.md) | Login | AI Tester | Pass | None | Token JWT được tạo hợp lệ và dùng để xác thực API /api/users/me thành công. |
| [TC-LOGIN-007](../test-cases/login/TC-LOGIN-007.md) | Login | AI Tester | Pass | None | Hệ thống sử dụng Parameterized Query nên chống tấn công SQL Injection thành công. |
| [TC-LOGIN-008](../test-cases/login/TC-LOGIN-008.md) | Login | AI Tester | Fail | #10 | Không cấu hình middleware Rate Limiting ở API Đăng nhập. |
| [TC-LOGIN-009](../test-cases/login/TC-LOGIN-009.md) | Login | AI Tester | Fail | #11 | Nút Đăng nhập không hiển thị trạng thái loading và không bị vô hiệu hóa khi đang gửi yêu cầu. |
| [TC-LOGIN-010](../test-cases/login/TC-LOGIN-010.md) | Login | AI Tester | Fail | #12 | Không có nút Toggle ẩn/hiện mật khẩu trên giao diện. |
| [TC-LOGIN-011](../test-cases/login/TC-LOGIN-011.md) | Login | AI Tester | Fail | #13 | Token JWT được ký không có thời gian hết hạn (exp), tồn tại vĩnh viễn. |
| [TC-LOGIN-012](../test-cases/login/TC-LOGIN-012.md) | Login | AI Tester | Fail | #14 | Đã đăng nhập nhưng vẫn truy cập được bình thường vào trang Đăng nhập (thiếu Route Guard). |
| [TC-LOGIN-013](../test-cases/login/TC-LOGIN-013.md) | Login | AI Tester | Fail | #15 | Tính năng đăng nhập qua bên thứ ba (Google OAuth) chưa được phát triển. |

### Các Bug phát hiện chi tiết:
1. **Bug #1 (Tăng bộ đếm sai):** Ở `backend/server.js:54`, code tăng bộ đếm thêm `2` đơn vị: `const newAttempts = user.login_attempts + 2;` thay vì `1`.
2. **Bug #2 (Thời gian khóa sai):** Ở `backend/server.js:57`, thời gian khóa được thiết lập là `180000` ms (3 phút) thay vì `30000` ms (30 giây): `lockedUntil = new Date(Date.now() + 180000).toISOString()`.
3. **Bug #3 (Race Condition bất đồng bộ):** Phản hồi API đăng nhập sai được gửi về client (`res.status(401)`) song song và không đợi giao dịch ghi DB (`db.run`) hoàn tất, dẫn đến việc đọc trạng thái DB ngay sau đó bị sai lệch.
4. **Bug #4 (Sai tiêu đề trang):** Tiêu đề trang Đăng nhập hiển thị sai thành `"Đăng Ký"` gây hiểu lầm lớn cho người dùng.
5. **Bug #5 (Sai nhãn trường nhập liệu):** Trường nhập địa chỉ email hiển thị nhãn là `"Username"` thay vì `"Email"`.
6. **Bug #6 (Không nhất quán ngôn ngữ):** Nút đăng nhập hiển thị tiếng Anh là `"Sign In"` thay vì tiếng Việt `"Đăng nhập"` (vi phạm quy định ngôn ngữ FR-21).
7. **Bug #7 (Lộ mật khẩu - Bảo mật):** Ô nhập mật khẩu có thuộc tính `type="text"` thay vì `type="password"`, khiến mật khẩu của người dùng bị hiển thị rõ ràng trên màn hình dưới dạng văn bản thường (vi phạm FR-22 và SEC-04).
8. **Bug #8 (Thiếu ký hiệu bắt buộc):** Các trường bắt buộc (Email và Mật khẩu) thiếu ký hiệu bắt buộc `*` bên cạnh nhãn (vi phạm FR-22).
9. **Bug #9 (Thiếu trim email ở backend):** Gửi email có khoảng trắng đầu/cuối sẽ đăng nhập thất bại do backend so khớp trực tiếp chuỗi gốc với database.
10. **Bug #10 (Thiếu Rate Limiting):** Không có middleware kiểm soát tần suất yêu cầu ở backend API, cho phép spam brute-force mật độ cao.
11. **Bug #11 (Thiếu Loading state):** Nút Đăng nhập không đổi trạng thái và không disable khi đang gửi API.
12. **Bug #12 (Thiếu nút Toggle Show/Hide):** Mật khẩu cố định hiển thị text và không có nút ẩn hiện.
13. **Bug #13 (Token vô hạn hạn):** Token JWT không được thiết lập trường `exp` khi ký, tồn tại vô thời hạn.
14. **Bug #14 (Thiếu Route Guard):** Đã đăng nhập nhưng vẫn vào được trang `/login` bình thường.
15. **Bug #15 (Thiếu OAuth):** Tính năng đăng nhập Google chưa được tích hợp như đặc tả hoặc mong đợi của hệ thống kiểm thử.
