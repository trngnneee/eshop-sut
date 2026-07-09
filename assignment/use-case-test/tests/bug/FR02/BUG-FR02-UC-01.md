# BUG-FR02-UC-01: Bộ đếm đăng nhập sai tăng thêm 2 đơn vị thay vì 1

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **BugID** | `BUG-FR02-UC-01` |
| **Status** | **Open** |
| **Found by Test Case** | [TC-FR02-UC-003](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/use-case-tes/tests/test-cases/FR02/TC-FR02-UC-003.md) |
| **Requirement Name** | FR-02 Đăng nhập & Khóa tài khoản |
| **Summary** | Khi nhập sai mật khẩu, backend API tăng `login_attempts` trong CSDL thêm 2 đơn vị thay vì 1 đơn vị. |
| **Steps to reproduce** | 1. Sử dụng tài khoản hoạt động bình thường.<br>2. Thực hiện đăng nhập với mật khẩu sai.<br>3. Kiểm tra trường `login_attempts` trong DB. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Date** | 2026-07-06 |
| **Reporter** | AI Tester |
