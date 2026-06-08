# Test Run - Sprint 1

**Ngày thực hiện**: 08/06/2026  
**Người thực hiện**: Khoa
**Môi trường thử nghiệm**: Local Backend API & Frontend Web (demo)

| Test Case ID                                        | Module | Tester | Result | Related Bug                  | Note                                                                   |
| :-------------------------------------------------- | :----- | :----- | :----- | :--------------------------- | :--------------------------------------------------------------------- |
| [TC-LOGIN-001](../test-cases/login/TC-LOGIN-001.md) | Login  | Khoa   | Pass   | None                         | Đăng nhập thành công với tài khoản đúng và trả về JWT.                 |
| [TC-LOGIN-002](../test-cases/login/TC-LOGIN-002.md) | Login  | Khoa   | Fail   | [Bug #1](../bugs/BUG-001.md) | Bộ đếm `login_attempts` tăng thêm 2 đơn vị sau mỗi lần sai thay vì 1.  |
| [TC-LOGIN-003](../test-cases/login/TC-LOGIN-003.md) | Login  | Khoa   | Fail   | [Bug #2](../bugs/BUG-002.md) | Tài khoản bị khóa trong 180 giây (3 phút) thay vì 30 giây theo đặc tả. |
