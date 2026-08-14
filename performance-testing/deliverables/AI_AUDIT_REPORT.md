# Báo Cáo Kiểm Toán AI (AI Audit Report)

> **Mã số sinh viên:** 23127207 (Khoa)  
> **Kịch bản kiểm thử:** Browse-to-buy (`POST /api/login` $\to$ `GET /api/products` $\to$ `GET /api/products/{id}` $\to$ `POST /api/cart` $\to$ `POST /api/checkout`)  
> **Công cụ AI sử dụng:** `Gemini 2.5 Pro (via Antigravity Engine)`  
> **Thời điểm tương tác chính:** `2026-08-14T07:00:00Z` đến `2026-08-14T17:30:00Z`  
> **Ngày lập báo cáo:** 2026-08-15  

---

## 1. Mục Đích và Phạm Vi Kiểm Toán
Báo cáo này kiểm toán toàn diện sự can thiệp của Trí tuệ Nhân tạo (AI) trong toàn bộ quy trình kiểm thử hiệu năng HW05, phân định rõ ranh giới giữa phần do AI sinh tự động và phần do Kỹ sư Con người phát hiện, hiệu chỉnh và nghiệm thu.

---

## 2. Bảng Thống Kê Đóng Góp và Tương Tác Cụ Thể

| Hạng mục công việc | Công cụ AI & Timestamp | Đóng góp của AI | Đóng góp & Hiệu chỉnh của Con người | Đánh giá chất lượng đầu ra |
|:---|:---|:---|:---|:---|
| **1. Thiết kế Kịch bản Tải (Test Design)** | Gemini 2.5 Pro<br>`2026-08-14 07:15` | Đề xuất khung 4 kịch bản tải và cấu trúc 5 endpoint tuần tự | Giới hạn ranh giới scope nhóm, bổ sung think time thực tế (1-2s, 2-4s) và chuẩn hóa payload | Tốt về cấu trúc, cần con người khóa chặt scope |
| **2. Sinh Test Plan JMeter (.jmx)** | Gemini 2.5 Pro<br>`2026-08-14 07:45` | Sinh cấu trúc XML JMeter ban đầu cho 4 file `.jmx` | Phát hiện và sửa **6 lỗi nghiêm trọng**: CSV quotedData, JWT auth header, dynamic pid extractor, ModuleController cho Stress, sửa cú pháp import minidom | Mắc nhiều lỗi cấu hình, con người bắt buộc phải review |
| **3. Xây dựng Script Phân tích (.py / .ps1)** | Gemini 2.5 Pro<br>`2026-08-14 08:30` | Viết script phân tích `.jtl` và script giám sát tài nguyên CPU/RAM | Chuẩn hóa công thức percentile sang **ISO 80000-2 nearest-rank**, thêm `overall_elapsed` khớp 100% với JMeter HTML dashboard | Script logic tốt sau khi chuẩn hóa chuẩn toán học |
| **4. Thực thi & Giám sát Hệ thống** | Con người trực tiếp<br>`2026-08-14 09:00 - 17:30` | Hỗ trợ phân tích log run | Quản lý tiến trình backend Node.js, giải phóng xung đột port 3000, seed 400 user + 505 product | Con người thực hiện 100% việc quản lý môi trường |
| **5. Phân tích Nguyên nhân Gốc rễ (Root Cause)** | Gemini 2.5 Pro<br>`2026-08-14 22:30` | Đưa ra nhận định ban đầu về bottleneck | Vạch trần 5 ảo giác của AI (Index vô nghĩa trên full table scan, Connection Pool cho SQLite, nhầm rò rỉ bộ nhớ) và chứng minh leak `userCarts` | Con người làm chủ phân tích mã nguồn |
| **6. Đề xuất Mô hình CPT & CI/CD** | Gemini 2.5 Pro<br>`2026-08-14 23:00` | Soạn thảo workflow GitHub Actions và sơ đồ Mermaid | Đề xuất cơ chế **3-run median** và ngưỡng relative delta (+10%/+20%) chống nhiễu runner | Thiết kế hoàn chỉnh, áp dụng được ngay |

---

## 3. Nhật Ký Tương Tác Mẫu (Raw Prompt & Output Reference)
Toàn bộ chuỗi 4 tương tác nguyên văn giữa Kỹ sư và AI được lưu trữ đầy đủ tại tài liệu [06_ai-analysis-critique.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/performance-testing/deliverables/06_ai-analysis-critique.md).

---

## 4. Kết Luận
AI là một trợ lý tăng tốc mạnh mẽ (giúp giảm ~70% thời gian viết boilerplate XML và script), nhưng **bắt buộc phải có kỹ sư con người có chuyên môn sâu làm chốt chặn kiểm soát chất lượng**.
