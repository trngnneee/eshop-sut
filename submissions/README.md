# HW06 – API Testing

**Khoa Công nghệ Thông tin (FIT) – Trường Đại học Khoa học Tự nhiên TP.HCM (HCMUS)**  
**CS423 / CSC13003 – Kiểm thử Phần mềm (AI-augmented · 2026)**

---

## Thông tin sinh viên

| Trường | Giá trị |
|:---|:---|
| **Họ và tên:** | Phan Quốc Thịnh |
| **MSSV:** | 23127486 |
| **Lớp:** | 23KTPM3 |
| **Bài tập:** | HW06 – API Testing |
| **Ngày nộp:** | *(cập nhật khi nộp)* |

---

## Các API được chọn

| Pool | Feature | API Endpoint | Mô tả |
|:---|:---|:---|:---|
| **Pool A** | FR-01 | `POST /api/register` | Đăng ký tài khoản người dùng |
| **Pool B** | FR-11 | `GET /api/orders/my-orders` | Xem lịch sử đơn hàng cá nhân |
| **Pool C** | FR-16 | `POST /api/admin/import-products` | Import sản phẩm hàng loạt (Admin) |

---

## Tóm tắt kết quả kiểm thử (Test Summary Report)

| Chỉ số | Giá trị |
|:---|:---|
| **Số API được kiểm thử** | 3 |
| **Test cases được AI sinh ra** | 118 (API 1: 42 \| API 2: 38 \| API 3: 38) |
| **Test cases tự thêm (extend)** | 27 (API 1: 13 \| API 2: 7 \| API 3: 7) |
| **Tổng số test cases** | 145 |
| **Tổng số assertions thực thi** | 184 assertions |
| **Test cases PASS** | 101 (69.7%) |
| **Test cases FAIL** | 44 (30.3%) |
| **Số bug phát hiện** | 19 unique bugs (4 Critical, 9 High, 5 Medium, 1 Low) |

---

## Bảng tự đánh giá (Self-Assessment Table)

| STT | Tiêu chí | Điểm tối đa | Tự đánh giá |
|:---|:---|:---|:---|
| 1 | API 1 — full pipeline (generate + audit + extend + execute + bugs) | 30 | 30/30 |
| 2 | API 2 — full pipeline (same criteria) | 30 | 30/30 |
| 3 | API 3 — full pipeline (same criteria) | 30 | 30/30 |
| 4 | Agent Skills (AI-driven test generator) | 10 | 10/10 |
| | **Tổng** | **100** | **100/100** |

---

## Danh sách file nộp

| File | Mô tả |
|:---|:---|
| `MainReport.md` | Báo cáo chính hoàn chỉnh (API testing + AI audit + Critique) |
| `AI_Audit.md` | Báo cáo AI Audit độc lập (phụ lục bắt buộc) |
| `AI_Critique.md` | Nhận xét phê bình AI (200–300 từ) |
| `test_cases_api1.md` | Test cases cho API 1 (Pool A) |
| `test_cases_api2.md` | Test cases cho API 2 (Pool B) |
| `test_cases_api3.md` | Test cases cho API 3 (Pool C) |
| `HW06_TestCases_and_Summary_23127486.xlsx` | Bảng tính Excel quản lý 145 Test Cases, Dashboard và Defect Log |
| `bug_report.md` | Báo cáo tổng hợp 19 bugs |
| `bug_reports/` | Thư mục chứa 19 file Markdown chi tiết cho từng bug (`BUG-A-01` đến `BUG-C-06`) |
| `cicd_report.md` | Báo cáo CI/CD pipeline tự động hóa Newman |
| `AI Agent/agent_skill.md` | Thiết kế AI-driven test generator (diagram + pseudocode) |
| `git_commit_log.txt` | Lịch sử commit Git minh chứng |
| `newman_reports/` | Các báo cáo thực thi HTML (`newman_api1_report.html`, `newman_api2_report.html`, `newman_api3_report.html`) |

---

## Link tham khảo

- **GitHub Repository:** `https://github.com/trngnneee/eshop-sut`
- **GitHub Issues (Bug Reports):** `https://github.com/trngnneee/eshop-sut/issues`
- **Branch:** `HW6-Thinh`
- **Video Demo Agent Skill (YouTube):** `https://youtu.be/cyVliBtOv4E`

