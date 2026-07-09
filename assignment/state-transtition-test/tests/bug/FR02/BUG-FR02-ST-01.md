# BUG-FR02-ST-01: Bộ đếm đăng nhập sai tăng thêm 2 đơn vị thay vì 1

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **BugID** | `BUG-FR02-ST-01` |
| **Status** | **Open** |
| **Found by Test Case** | [TC-FR02-ST-002](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/assignment/state-transtition-test/tests/test-cases/FR02/TC-FR02-ST-002.md) |
| **Requirement Name** | FR-02 Đăng nhập & Khóa tài khoản |
| **Summary** | Khi người dùng nhập sai mật khẩu, backend API tăng `login_attempts` trong CSDL thêm 2 đơn vị thay vì 1 đơn vị, dẫn đến việc tài khoản bị khóa nhanh hơn dự kiến (chỉ sau 2 lần sai). |
| **Steps to reproduce** | 1. Dùng tài khoản đang hoạt động (`login_attempts = 0`).<br>2. Nhập Email đúng và mật khẩu sai.<br>3. Kiểm tra DB: Trường `login_attempts` có giá trị là 2 thay vì 1. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Date** | 2026-07-06 |
| **Reporter** | AI Tester |
