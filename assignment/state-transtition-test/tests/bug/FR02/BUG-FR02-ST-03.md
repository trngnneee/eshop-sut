# BUG-FR02-ST-03: Đặt lại mật khẩu thành công không giải phóng trạng thái khóa tài khoản

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **BugID** | `BUG-FR02-ST-03` |
| **Status** | **Open** |
| **Found by Test Case** | [TC-FR02-ST-006](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/assignment/state-transtition-test/tests/test-cases/FR02/TC-FR02-ST-006.md) |
| **Requirement Name** | FR-02 Đăng nhập & Khóa tài khoản |
| **Summary** | Sau khi người dùng đặt lại mật khẩu thành công qua API `/api/reset-password`, hệ thống cập nhật mật khẩu mới nhưng không reset trường `login_attempts` về 0 và `locked_until` về NULL. Điều này làm tài khoản vẫn tiếp tục bị khóa. |
| **Steps to reproduce** | 1. Nhập sai 3 lần để khóa tài khoản.<br>2. Gọi quên mật khẩu và đặt lại mật khẩu mới thành công.<br>3. Thử đăng nhập ngay bằng mật khẩu mới. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Date** | 2026-07-06 |
| **Reporter** | AI Tester |
