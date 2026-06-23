# Test Run - Sprint 2

**Ngày thực hiện**: 23/06/2026  
**Người thực hiện**: AI Tester (Antigravity)
**Môi trường thử nghiệm**: Local Backend API & SQLite database

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [TC-LOGIN-001](../test-cases/login/TC-LOGIN-001.md) | Login | AI Tester | Pass | None | Đăng ký tài khoản `fr02_success@eshop.com` và đăng nhập thành công, nhận JWT token. |
| [TC-LOGIN-002](../test-cases/login/TC-LOGIN-002.md) | Login | AI Tester | Fail | #1, #3 | Bộ đếm `login_attempts` tăng vọt lên 2 và có hiện tượng bất đồng bộ (race condition) khi ghi DB. |
| [TC-LOGIN-003](../test-cases/login/TC-LOGIN-003.md) | Login | AI Tester | Fail | #2 | Tài khoản bị khóa trong 180 giây (3 phút) thay vì 30 giây như đặc tả. |

### Các Bug phát hiện chi tiết:
1. **Bug #1 (Tăng bộ đếm sai):** Ở `backend/server.js:54`, code tăng bộ đếm thêm `2` đơn vị: `const newAttempts = user.login_attempts + 2;` thay vì `1`.
2. **Bug #2 (Thời gian khóa sai):** Ở `backend/server.js:57`, thời gian khóa được thiết lập là `180000` ms (3 phút) thay vì `30000` ms (30 giây): `lockedUntil = new Date(Date.now() + 180000).toISOString()`.
3. **Bug #3 (Race Condition bất đồng bộ):** Phản hồi API đăng nhập sai được gửi về client (`res.status(401)`) song song và không đợi giao dịch ghi DB (`db.run`) hoàn tất, dẫn đến việc đọc trạng thái DB ngay sau đó bị sai lệch.
