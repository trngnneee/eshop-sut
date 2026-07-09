# Báo Cáo Tổng Hợp Kết Quả & Tự Đánh Giá (Test Summary & Self-Assessment)

Tài liệu này tổng hợp thông tin sinh viên, thống kê kết quả thực hiện kiểm thử bài tập HW02 và bảng tự đánh giá điểm số cho 4 tính năng đã chọn từ các pool của hệ thống EShop.

## Thông Tin Sinh Viên

- **Họ và tên:** Đặng Đăng Khoa
- **Mã số sinh viên (MSSV):** 23127207

---

## 1. Thống Kê Kết Quả Thực Thi (Execution Summary)

- **Số lượng tính năng đã chọn (Selected Features):** 4 tính năng.
- **Tổng số test cases đã thiết kế (Designed):** 259 test cases (gồm 159 Domain Testing và 100 BVA).
- **Tổng số test cases đã thực thi (Executed):** 259 test cases.
- **Số lượng Pass:** 168 test cases.
- **Số lượng Fail:** 91 test cases.
- **Số lượng Blocked:** 0.
- **Số lượng Not Executed (Chưa thực thi):** 0 test cases.
- **Tổng số lỗi phát hiện (Bugs Found):** 49 bugs.

### Chi tiết phân bổ theo tính năng (Feature Breakdown)

| Feature ID                                             | Feature Name               | Pool   | Designed | Executed |  Pass   |  Fail  | Blocked | Not Executed | Bugs Found |
| :----------------------------------------------------- | :------------------------- | :----- | :------: | :------: | :-----: | :----: | :-----: | :----------: | :--------: |
| [FR-02](main-report.md#fr-02--authentication--lockout) | Đăng nhập & Khóa tài khoản | Pool A |    80    |    80    |   61    |   19   |    0    |      0       |     19     |
| [FR-07](main-report.md#fr-07--shopping-cart)           | Giỏ hàng                   | Pool B |    90    |    90    |   35    |   55   |    0    |      0       |     19     |
| [FR-13](main-report.md#fr-13--dashboard)               | Dashboard                  | Pool C |    46    |    46    |   36    |   10   |    0    |      0       |     5      |
| [FR-21](main-report.md#fr-21--mobile-cart--checkout)   | Mobile Cart & Checkout     | Pool D |    43    |    43    |   36    |   7    |    0    |      0       |     6      |
| **Tổng cộng**                                          |                            |        | **259**  | **259**  | **168** | **91** |  **0**  |    **0**     |   **49**   |

---

## 2. Liên Kết Bằng Chứng & Sản Phẩm (Evidence & Deliverables Links)

- **Báo cáo chính (Main Report):** [main-report.md](main-report.md)
- **Báo cáo lỗi tổng hợp (Master Bug Report):** [bug_report.md](bug_report.md)
- **Báo cáo tương tác AI (AI Audit Report):** [ai-audit-report.md](ai-audit-report.md)
- **Tự phê bình AI (AI Critique):** [ai-critique.md](ai-critique.md)
- **Nhật ký commit Git (Git Commit Log):** [commit_log.txt](commit_log.txt)
- **Thư mục bug reports chi tiết:** [tests/bug/](tests/bug/)
- **Thư mục test cases thiết kế:** [tests/test-cases/](tests/test-cases/)
- **Thư mục kết quả test run:** [tests/test-runs/](tests/test-runs/)
- **GitHub Repository Issues:** [trngnneee/eshop-sut Issues](https://github.com/trngnneee/eshop-sut/issues)
- **Demo Video Link (YouTube):** [https://youtu.be/9nTGFFD4x-0](https://youtu.be/9nTGFFD4x-0).

---

## 3. Bảng Tự Đánh Giá Điểm Số (Self-Assessment Table)

| No. | Criteria                                                     | Max Grade | Self-Assessed Grade | Evidence & Rationale                                                                                                                                    |
| --- | ------------------------------------------------------------ | --------: | ------------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Feature A – FR-02 Login & Lockout (Domain + Boundary)        |        25 |                  25 | Đã thiết kế 80 test cases, thực thi 80/80, phát hiện 19 bugs, có test cases, test run, bug report, evidence và GitHub Issues tương ứng.                 |
| 2   | Feature B – FR-07 Shopping Cart (Domain + Boundary)          |        25 |                  25 | Đã thiết kế 90 test cases, thực thi 90/90, phát hiện 19 bugs, bao phủ UI, API, validation, BVA quantity/price và security cases.                        |
| 3   | Feature C – FR-13 Dashboard (Domain + Boundary)              |        25 |                  25 | Đã thiết kế 46 test cases, thực thi 46/46, phát hiện 5 bugs, bao phủ role access, dashboard metrics, API failure, invalid data và responsive UI.        |
| 4   | Feature D – FR-21 Mobile Cart & Checkout (Domain + Boundary) |        15 |                  15 | Đã thiết kế 43 test cases, thực thi 43/43, phát hiện 6 bugs, bao phủ mobile cart, checkout, profile validation, coupon boundary và API price tampering. |
| 5   | Agent Skills                                                 |        10 |                  10 | Có thư mục `.agents`, có demo video YouTube, có minh chứng quy trình sử dụng skill để hỗ trợ thiết kế Domain Testing/BVA và sinh báo cáo.               |
|     | **Total**                                                    |   **100** |             **100** | **Self-Assessed Grade: 100/100**                                                                                                                        |
|  |
