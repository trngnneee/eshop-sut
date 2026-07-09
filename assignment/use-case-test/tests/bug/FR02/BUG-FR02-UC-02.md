# BUG-FR02-UC-02: Thời gian khóa tài khoản bị thiết lập sai thành 3 phút

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **BugID** | `BUG-FR02-UC-02` |
| **Status** | **Open** |
| **Found by Test Case** | [TC-FR02-UC-004](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/use-case-tes/tests/test-cases/FR02/TC-FR02-UC-004.md) |
| **Requirement Name** | FR-02 Đăng nhập & Khóa tài khoản |
| **Summary** | Khi tài khoản bị khóa sau 3 lần sai liên tiếp, thời gian khóa là 3 phút thay vì 30 giây. |
| **Steps to reproduce** | 1. Thực hiện nhập sai mật khẩu liên tiếp cho đến khi bị khóa.<br>2. Kiểm tra DB xem trường `locked_until` được ghi nhận giá trị bao lâu. |
| **Severity** | Medium |
| **Frequency** | Always |
| **Priority** | High |
| **Date** | 2026-07-06 |
| **Reporter** | AI Tester |
