# HW05 – Kiểm thử hiệu năng (Performance Testing)

**Sinh viên thực hiện:** Phan Quốc Thịnh  
**MSSV:** 23127486  
**Môn học:** CS423 / CSC13003 – Kiểm thử phần mềm (Định hướng AI · 2026)  
**Bài tập:** HW05 – Kiểm thử hiệu năng (Performance Testing)

---

## 1. Bảng tự đánh giá điểm (Self-Assessment Table)

| STT | Tiêu chí đánh giá | Thang điểm | Điểm tự đánh giá |
|:---|:------------------|:----------:|:-----------------:|
| 1 | Task 1 — Kiểm thử tải (Load testing) | 20 | 20 |
| 2 | Task 1 — Kiểm thử áp lực (Stress testing) | 20 | 20 |
| 3 | Task 1 — Kiểm thử đột biến (Spike testing) | 20 | 20 |
| 4 | Task 2 — Phân tích kết quả bằng AI + Săn lỗi suy diễn sai (kèm số liệu chính xác từ log thô) | 10 | 10 |
| 5 | Task 3 — Đề xuất quy trình Continuous Performance Testing (G9.6 Disrupt) | 10 | 10 |
| 6 | Xây dựng Agent Skills hỗ trợ quy trình tự động | 10 | 10 |
| | **Tổng cộng** | **100** | **100** |

---

## 2. Báo cáo tóm tắt kiểm thử (Test Summary Report)

### 2.1 Các kịch bản kiểm thử đã thực hiện

| Kịch bản | Tập tin Test Plan | Trạng thái thực thi |
|:---------|:------------------|:-------------------|
| Kiểm thử tải (Load Test) | `23127486_Load_20260815.jmx` | Hoàn thành (20 VU, ramp-up 60s, tổng 300s, 0% lỗi) |
| Kiểm thử áp lực (Stress Test) | `23127486_Stress_20260815.jmx` | Hoàn thành (Tăng từng bước 50→200 VU, 569s, 0% lỗi) |
| Kiểm thử đột biến (Spike Test) | `23127486_Spike_20260815.jmx` | Hoàn thành (5→100→5 VU, ramp-up spike 5s, 148s, 0% lỗi) |

### 2.2 Các nhóm endpoint được bao phủ

| Nhóm endpoint | Danh sách endpoint | Mô tả mục đích kiểm thử |
|:--------------|:-------------------|:------------------------|
| **Xác thực (Auth-heavy)** | `POST /api/login` | Đăng nhập, cấp JWT token và xử lý khóa tài khoản sau 3 lần sai liên tiếp |
| **Đọc dữ liệu (Read-heavy)** | `GET /api/products?search={keyword}`, `GET /api/products/{id}` | Tìm kiếm danh mục sản phẩm theo từ khóa và xem chi tiết từng sản phẩm |
| **Giao dịch (Transactional)** | `POST /api/cart`, `POST /api/apply-coupon`, `POST /api/checkout` | Thêm vào giỏ hàng, áp dụng mã giảm giá VIP100 và đặt hàng hoàn tất giao dịch |

### 2.3 Quy trình kiểm thử E2E (End-to-End Workflow)

Luồng kiểm thử gồm 6 bước liên hoàn mô phỏng hành vi mua hàng thực tế:
1. **Đăng nhập (`POST /api/login`):** Xác thực tài khoản từ file CSV, trích xuất `token` và `user_id` qua JSON Extractor (Think time: 1.5s).
2. **Tìm kiếm sản phẩm (`GET /api/products?search=`):** Gửi keyword tìm kiếm tiếng Việt ngẫu nhiên từ CSV.
3. **Xem chi tiết (`GET /api/products/{id}`):** Truy xuất thông tin sản phẩm theo ID tương ứng (Think time: 1.5s).
4. **Thêm vào giỏ hàng (`POST /api/cart`):** Đưa sản phẩm với số lượng và đơn giá vào giỏ hàng của user.
5. **Áp mã giảm giá (`POST /api/apply-coupon`):** Áp dụng mã `VIP100` với tổng đơn `total_before > 300,000 đ`, trích xuất `final_amount` (Think time: 1.0s).
6. **Thanh toán (`POST /api/checkout`):** Gửi yêu cầu tạo đơn hàng với địa chỉ giao hàng và số tiền sau giảm giá.

### 2.4 Ngưỡng kiểm thử độ bền (Endurance Threshold)

| Chỉ số hiệu năng | Giá trị ghi nhận |
|:-----------------|:-----------------|
| Kịch bản kiểm thử | Tái sử dụng kịch bản Load Test (20 VU), mở rộng thời gian chạy 15 phút |
| Thông lượng ổn định tối đa (Maximum Stable RPS) | **~27 RPS** (duy trì đều đặn suốt 15 phút) |
| Trần tiêu thụ bộ nhớ (Memory Ceiling) | **~40–54 MB** (Tiến trình Node.js + SQLite) |
| Thời gian kiểm thử độ bền (Duration) | 15 phút (900 giây) |
| Cấu hình phần cứng máy thử nghiệm | AMD Ryzen 5 7535HS (6 Cores / 12 Threads), 16 GB RAM, Windows 11 |

### 2.5 Danh sách lỗi và vấn đề hiệu năng phát hiện

| STT | Vấn đề phát hiện | Phân loại | Liên kết GitHub Issue |
|:---|:-----------------|:----------|:----------------------|
| 1 | Bỏ qua giới hạn lượt dùng coupon tại `POST /api/apply-coupon` | Lỗi logic (Logic Bug) | [#408](https://github.com/trngnneee/eshop-sut/issues/408) |
| 2 | Giỏ hàng lưu in-memory gây mất dữ liệu khi server khởi động lại | Lỗi kiến trúc (Architecture Bug) | [#409](https://github.com/trngnneee/eshop-sut/issues/409) |

### 2.6 Video minh họa kiểm thử (Demo Videos)

- **Video Demo Kiểm thử hiệu năng (JMeter + Resource Monitor):** [https://youtu.be/8tH_mGjYRl4](https://youtu.be/8tH_mGjYRl4)
- **Video Demo Agent Skill (Tự động hóa kiểm thử):** [https://youtu.be/n1ObWBHpbbM](https://youtu.be/n1ObWBHpbbM)

---

## 3. Liên kết Repository

- **GitHub Repository:** [https://github.com/trngnneee/eshop-sut](https://github.com/trngnneee/eshop-sut) (Nhánh: `HW5-Thinh` – [Xem trực tiếp](https://github.com/trngnneee/eshop-sut/tree/HW5-Thinh))

---

## 4. Mục lục tài liệu và tệp tin nộp bài (File Index)

| Tên tệp tin | Mô tả nội dung |
|:------------|:---------------|
| `MainReport.md` | Báo cáo chính toàn diện về kiểm thử hiệu năng (Task 1, Task 2, Task 3) |
| `AI_Audit.md` | Báo cáo kiểm toán AI chi tiết theo biểu mẫu quy định 5 mục (Phụ lục bắt buộc) |
| `AI_Critique.md` | Đoạn phê bình và đánh giá năng lực AI (200–300 từ) |
| `git_commit_log.txt` | Toàn bộ nhật ký commit Git của dự án |
| `23127486_Load_20260815.jmx` | Tập tin kịch bản kiểm thử tải (Load test plan) trong JMeter |
| `23127486_Stress_20260815.jmx` | Tập tin kịch bản kiểm thử áp lực (Stress test plan) trong JMeter |
| `23127486_Spike_20260815.jmx` | Tập tin kịch bản kiểm thử đột biến (Spike test plan) trong JMeter |
| `test_data.csv` | Tập dữ liệu đầu vào tham số hóa cho các kịch bản test (20 dòng tài khoản) |
| `23127486_Load_20260815.jtl` | File log dữ liệu thô kết quả chạy kịch bản Load test |
| `23127486_Stress_20260815.jtl` | File log dữ liệu thô kết quả chạy kịch bản Stress test |
| `23127486_Spike_20260815.jtl` | File log dữ liệu thô kết quả chạy kịch bản Spike test |
| `soak_test.jtl` | File log dữ liệu thô kịch bản kiểm thử độ bền (Soak test) |
| `bug_report.md` | Báo cáo chi tiết các lỗi logic và kiến trúc phát hiện được |
| `github_issue_1.md` | Mẫu báo cáo lỗi GitHub Issue #1 (Coupon limit bypass) |
| `github_issue_2.md` | Mẫu báo cáo lỗi GitHub Issue #2 (Cart in-memory) |
| `screenshots/` | Thư mục chứa ảnh chụp cấu hình phần cứng và theo dõi tài nguyên máy |
| `html_reports/` | Thư mục chứa báo cáo định dạng HTML trực quan do JMeter xuất ra cho từng kịch bản |
