# BUG-FR02-ST-02: Thời gian khóa tài khoản bị thiết lập sai thành 3 phút

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **BugID** | `BUG-FR02-ST-02` |
| **Status** | **Open** |
| **Found by Test Case** | [TC-FR02-ST-005](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/assignment/state-transtition-test/tests/test-cases/FR02/TC-FR02-ST-005.md) |
| **Requirement Name** | FR-02 Đăng nhập & Khóa tài khoản |
| **Summary** | Khi tài khoản bị khóa, thời gian khóa bị thiết lập là 180 giây (3 phút) thay vì 30 giây theo đặc tả của môi trường thử nghiệm. |
| **Steps to reproduce** | 1. Nhập sai mật khẩu liên tiếp cho đến khi tài khoản bị khóa.<br>2. Chờ 30 giây.<br>3. Thử đăng nhập lại bằng mật khẩu đúng. |
| **Severity** | Medium |
| **Frequency** | Always |
| **Priority** | High |
| **Date** | 2026-07-06 |
| **Reporter** | AI Tester |
