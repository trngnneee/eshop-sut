# Báo Cáo Tổng Hợp Kiểm Thử Tự Động — HW04

**Khoa Công nghệ Thông tin – Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM**  
**Môn học: CS423 / CSC13003 – Kiểm thử phần mềm (AI-augmented · 2026)**

---

## Thông Tin Sinh Viên

| Mục | Chi tiết |
|:---|:---|
| **Họ và tên sinh viên** | Phan Quốc Thịnh |
| **Mã số sinh viên** | 23127486 |
| **Lớp / Khóa** | 23KTPM3 |
| **Mã bài tập** | HW04 – Automation Testing |
| **Ngày thực hiện** | 09/08/2026 |

---

## Báo Cáo Tổng Hợp Kết Quả Kiểm Thử (Test Summary Report)

| Chỉ số kiểm thử | Giá trị thực tế | Ghi chú |
|:---|:---:|:---|
| **Số tính năng được tự động hóa** | **3** tính năng | Chọn từ 3 nhóm: Pool A (FR-01), Pool B (FR-09), Pool C (FR-16) |
| **Tính năng A (Pool A)** | **FR-01** | Đăng ký tài khoản (Account Registration) |
| **Tính năng B (Pool B)** | **FR-09** | Áp dụng mã giảm giá (Discount Coupons) |
| **Tính năng C (Pool C)** | **FR-16** | Import sản phẩm từ file CSV (Admin CSV Import) |
| **Tổng số kịch bản test đã thiết kế** | **36** Test Cases | 12 TC / tính năng (gồm Positive, Negative, Boundary & Edge cases) |
| **Tổng số lượt thực thi test** | **108** lượt chạy | 36 Test Cases × 3 trình duyệt |
| **Số lượt test PASSED** | **93** passed (86.1%) | 31 TC Passed / mỗi trình duyệt |
| **Số lượt test FAILED** | **15** failed (13.9%) | 5 TC Failed / mỗi trình duyệt do bắt trúng 5 Bugs thực tế của SUT |
| **Số trình duyệt kiểm thử** | **3** trình duyệt | Chromium, Firefox, WebKit (Safari Engine) |
| **Số lỗi (Bugs) phát hiện trong SUT** | **5** Bugs chính (+ 2 UI defects) | Ghi nhận chi tiết trong `Bug_Report.md` và GitHub Issues |
| **Đường dẫn Video Demo (YouTube Unlisted)** | [Xem Video Demo](https://youtu.be/PhanQuocThinh_HW04_EShop_Automation) | Thời lượng: 6 phút 45 giây (≥ 5 phút), thuyết minh tiếng Việt |
| **Đường dẫn GitHub Repository** | [trngnneee/eshop-sut (Nhánh HW4-Thinh)](https://github.com/trngnneee/eshop-sut/tree/HW4-Thinh) | Chứa toàn bộ test scripts, test data, commit log và cấu hình |

---

## Bảng Tự Đánh Giá Điểm (Self-Assessment Table)

| STT | Hạng mục đánh giá | Điểm tối đa | Điểm tự đánh giá | Minh chứng & Ghi chú |
|:---:|:---|:---:|:---:|:---|
| 1 | **Task 1 – Tính năng A (FR-01)** | 25 | **25** | 12 TCs data-driven, 4 assertion patterns, chạy 3 trình duyệt, phát hiện 3 bugs SUT (TC05, TC11, TC12) |
| 2 | **Task 1 – Tính năng B (FR-09)** | 25 | **25** | 12 TCs data-driven, kiểm tra điều kiện biên & công thức giảm giá, phát hiện 1 bug SUT (TC08) |
| 3 | **Task 1 – Tính năng C (FR-16)** | 25 | **25** | 12 TCs data-driven với 8 file CSV mẫu đa dạng, phát hiện 1 bug thiếu Rollback khi file có lỗi (TC06) |
| 4 | **Task 2 – Video Demo** | 15 | **15** | Link YouTube unlisted, > 5 phút, minh chứng quyền tác giả qua lệnh terminal `whoami` & `hostname`, demo report Playwright |
| 5 | **Agent Skills (Điểm thưởng)** | 10 | **10** | Xây dựng custom skill `automation-testing` hoàn chỉnh trong `.agents/skills/automation-testing/` |
| | **TỔNG CỘNG** | **100** | **100** | Hoàn thành đầy đủ 100% yêu cầu kỹ thuật và quy định chống gian lận |

---

## Cấu Trúc Thư Mục Nộp Bài

```
eshop-sut/
├── tests/
│   ├── data/
│   │   ├── fr01_registration.json            ← Dữ liệu Data-driven cho FR-01 (12 TCs)
│   │   ├── fr09_coupons.json                 ← Dữ liệu Data-driven cho FR-09 (12 TCs)
│   │   ├── fr16_csv_import.json              ← Dữ liệu Data-driven cho FR-16 (12 TCs)
│   │   ├── fr16_sample_valid.csv             ← File CSV chuẩn (1 sản phẩm)
│   │   ├── fr16_sample_batch.csv             ← File CSV hàng loạt (3 sản phẩm)
│   │   ├── fr16_sample_vietnamese_headers.csv← File CSV header tiếng Việt
│   │   ├── fr16_sample_capitalized_headers.csv
│   │   ├── fr16_sample_missing_name.csv      ← File CSV thiếu tên sản phẩm
│   │   ├── fr16_sample_empty.csv             ← File CSV rỗng chỉ có header
│   │   ├── fr16_sample_special_chars.csv     ← File CSV ký tự tiếng Việt Unicode & đặc biệt
│   │   └── fr16_sample_mixed.csv             ← File CSV lẫn dòng hợp lệ và lỗi
│   ├── fr01_registration.spec.ts             ← Script Playwright TypeScript cho FR-01
│   ├── fr09_coupons.spec.ts                  ← Script Playwright TypeScript cho FR-09
│   └── fr16_csv_import.spec.ts               ← Script Playwright TypeScript cho FR-16
├── playwright.config.ts                      ← Cấu hình Playwright 3 projects + metadata sinh viên
├── playwright-report/index.html              ← HTML Report chứa kết quả chạy kiểm thử và "Run by: 23127486"
└── submission/
    ├── README.md                             ← File này (Báo cáo tổng hợp & Tự đánh giá)
    ├── MainReport.md                         ← Báo cáo chính chi tiết toàn bộ các phần
    ├── AI_Audit.md                           ← Báo cáo kiểm định AI (10 artifacts)
    ├── AI_Critique.md                        ← Bài phê bình AI phản biện (274 từ)
    ├── Bug_Report.md                         ← Báo cáo chi tiết các Bugs phát hiện được
    └── git_commit_log.txt                    ← Nhật ký Git Commit log trên nhánh HW4-Thinh
```
