# HW05 — Kiểm Thử Hiệu Năng (Performance Testing)

> **Sinh viên:** Đặng Đăng Khoa (MSSV: **23127207**)  
> **Học phần:** Kiểm thử Phần mềm (Software Testing) · **Nhánh Git:** `HW5`  
> **Workflow:** **Browse-to-buy** (`POST /api/login` $\to$ `GET /api/products` $\to$ `GET /api/products/{id}` $\to$ `POST /api/cart` $\to$ `POST /api/checkout`)  

---

## 0. Video Demo (YouTube — Unlisted)

| Video | Nội dung | Link |
|:---|:---|:---|
| **Task 1 — Thực thi 4 kịch bản tải** | Thuyết minh tiếng Việt, JMeter và Task Manager trong cùng khung hình, đọc số liệu trực tiếp trên màn hình | https://youtu.be/9AfuhaxZ0Zk |
| **Task 4 — Demo Agent Skill** | End-to-end: dùng skill sinh test plan cho một endpoint group hoàn chỉnh, và tái sử dụng cho endpoint group thứ hai | https://youtu.be/JP2z4raDbAs |

---

## 1. Cấu trúc Thư mục Toàn bộ Đồ án

```
performance-testing/
├── 23127207_HW05_Report.md         # Báo cáo tổng kết toàn diện HW05
├── README.md                       # Tài liệu hướng dẫn này & Bảng tự đánh giá
├── baseline/
│   └── baseline.json               # Ngưỡng chuẩn so sánh CI/CD (ground-truth)
├── data/
│   └── khoa_users.csv              # Bộ 400 tài khoản test chuẩn RFC 4180
├── deliverables/
│   ├── 01_test-design.md           # Thiết kế kiểm thử chi tiết (Task 1)
│   ├── 02_ai-generation-log.md     # Nhật ký sinh kịch bản bằng AI (Task 1)
│   ├── 03_human-review-fixes.md    # Rà soát và sửa 6 lỗi AI (Task 1)
│   ├── 04_execution-report.md      # Báo cáo thực thi 4 kịch bản (Task 1)
│   ├── 05_endurance-threshold.md   # Phân tích rò rỉ RAM & Time-to-OOM (Task 1)
│   ├── 06_ai-analysis-critique.md  # Phản biện AI & Săn lỗi hiểu sai (Task 2)
│   ├── 07_continuous-performance-testing.md # Đề xuất CPT (Task 3)
│   ├── AI_AUDIT_REPORT.md          # Báo cáo kiểm toán đóng góp của AI
│   └── AI_CRITIQUE.md              # Bản tự phê bình của AI (250 từ)
├── docs/                           # 14 tài liệu đặc tả kiến trúc & runbook
├── evidence/
│   ├── hardware/
│   │   └── spec-table.md           # Bảng thông số phần cứng thực thi
│   └── skill-demo/
│       ├── generate_jmx-console.txt# Console log sinh JMX tự động
│       ├── compare_runs-console.txt# Console log so sánh baseline
│       ├── generated_browse_Load.jmx
│       └── generated_coupon_Load.jmx
├── k6/
│   └── 23127207_Load_20260814.js   # Kịch bản k6 Load Test bổ sung
├── results/
│   ├── load/                       # Log .jtl, HTML report, resource CSV, summary
│   ├── stress/
│   ├── spike/
│   └── endurance/
├── scripts/
│   ├── jmeter-user.properties      # Cấu hình JTL output chuẩn
│   ├── seed_perf_data.js           # Seed 400 user + 500 product
│   ├── reset_lockout.js            # Reset trạng thái khóa tài khoản
│   ├── monitor_backend.ps1         # Giám sát CPU/RAM backend
│   ├── analyze_jtl.py              # Phân tích percentile ISO 80000-2
│   └── run_scenario.ps1            # Script tự động thực thi kịch bản
└── test-plans/
    ├── 23127207_Load_20260814.jmx
    ├── 23127207_Stress_20260814.jmx
    ├── 23127207_Spike_20260814.jmx
    └── 23127207_Endurance_20260814.jmx
```

---

## 2. Bảng Tự Đánh Giá Theo Barem Điểm (Self-Assessment Matrix)

| Nhiệm vụ | Điểm tối đa | Tự đánh giá | Minh chứng chính |
|:---|:---:|:---:|:---|
| **Task 1 — Thực thi & Báo cáo 4 Kịch bản Tải** | **50** | **50 / 50** | Đầy đủ 4 kịch bản chạy thật Non-GUI, 0 lỗi scope, bách phân vị ISO 80000-2 khớp HTML dashboard 100%, phân tích rò rỉ RAM $6.45\text{ MB/min}$ và Time-to-OOM tại [04_execution-report.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/performance-testing/deliverables/04_execution-report.md) & [05_endurance-threshold.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/performance-testing/deliverables/05_endurance-threshold.md). |
| **Task 2 — Phản biện AI & Săn Lỗi Hiểu sai** | **20** | **20 / 20** | Nhật ký 4 vòng hội thoại có timestamp, tool name cụ thể (`Gemini 2.5 Pro via Antigravity`), ma trận 5 lỗi hiểu sai của AI tại [06_ai-analysis-critique.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/performance-testing/deliverables/06_ai-analysis-critique.md) & [AI_AUDIT_REPORT.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/performance-testing/deliverables/AI_AUDIT_REPORT.md). |
| **Task 3 — Mô hình Kiểm thử Liên tục (CPT)** | **20** | **20 / 20** | Đề xuất CPT 4 tầng (T1-T4), sơ đồ Mermaid, cơ chế 3-run median chống nhiễu, file `baseline.json` số liệu thật và workflow GitHub Actions [.github/workflows/perf-regression.yml](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/.github/workflows/perf-regression.yml). |
| **Task 4 — Kỹ năng Agent (.agents/skills)** | **10** | **10 / 10** | Đầy đủ `SKILL.md`, `generate_jmx.py` (đã sửa minidom & hỗ trợ đa nền tảng), `compare_runs.py`, sinh thành công cả 2 workflow tại `evidence/skill-demo/` chứng minh khả năng tái sử dụng. |
| **Tổng điểm** | **100** | **100 / 100** | Toàn bộ yêu cầu và tài liệu bàn giao đều đầy đủ, kiểm chứng được. |

---

## 3. Báo Lỗi GitHub Issues (Bug Reports)

Ba lỗi thật phát hiện trong quá trình kiểm thử hiệu năng đã được đăng lên GitHub Issues của SUT:

| # | Issue | Loại | Link |
|:--|:---|:---|:---|
| 1 | `[PERF] In-memory cart (userCarts) grows unbounded — memory leak under sustained load` | Performance | https://github.com/trngnneee/eshop-sut/issues/399 |
| 2 | `[FR-02] Login attempt counter increments by 2 and lockout lasts 180s instead of 30s` | Functional | https://github.com/trngnneee/eshop-sut/issues/400 |
| 3 | `[FR-06] GET /api/products/:id returns 200 with empty body for non-existent id` | Functional | https://github.com/trngnneee/eshop-sut/issues/401 |

Ảnh chụp trang danh sách Issues: `evidence/issues/github-issues-list.png`

### Issue 1: `[BUG] Memory Leak in userCarts Global Object (server.js:14,293)`
- **Mức độ:** `Critical`
- **Mô tả:** Mảng `userCarts[userId]` trong heap V8 liên tục tích lũy đối tượng giỏ hàng khi người dùng gọi `POST /api/cart` mà không hề được giải phóng sau khi `POST /api/checkout` hoàn tất.
- **Bằng chứng:** Trong bài kiểm thử Endurance (30 VU, 12 phút), RAM Private tăng liên tục từ 60.30 MB lên 137.39 MB với tốc độ $6.45\text{ MB/min}$, đẩy độ trễ p95 từ 47ms lên 2,112ms. Dự báo sập container 512MB sau 70 phút.
- **Đề xuất sửa:** Bổ sung `delete userCarts[userId];` tại callback hoàn tất thanh toán của `POST /api/checkout`.

### Issue 2: `[PERF] High Response Latency Under Concurrent Spike Load (server.js:153)`
- **Mức độ:** `High`
- **Mô tả:** Khi có đột biến 300 VU đồng thời, câu truy vấn `GET /api/products` thực hiện quét toàn bộ bảng 505 sản phẩm trả về payload 154 KB cho mỗi request, làm nghẽn hàng đợi sự kiện Node.js và đẩy p95 lên trên 1.3 giây.
- **Đề xuất sửa:** Bổ sung phân trang `LIMIT / OFFSET` cho API danh mục sản phẩm và nén gzip cho response payload.

---

## 4. Hướng Dẫn Thực Thi

### Bước 1: Khởi động Server SUT
```powershell
node backend/server.js
```

### Bước 2: Thực thi Tự Động Toàn Bộ Kịch Bản
```powershell
# Chạy Load Test (50 VU, 5 phút)
powershell -ExecutionPolicy Bypass -File performance-testing/scripts/run_scenario.ps1 -Scenario Load

# Chạy Stress Test (25 -> 200 VU, 8 phút)
powershell -ExecutionPolicy Bypass -File performance-testing/scripts/run_scenario.ps1 -Scenario Stress

# Chạy Spike Test (10 -> 300 VU, 6 phút)
powershell -ExecutionPolicy Bypass -File performance-testing/scripts/run_scenario.ps1 -Scenario Spike

# Chạy Endurance Test (30 VU, 12 phút)
powershell -ExecutionPolicy Bypass -File performance-testing/scripts/run_scenario.ps1 -Scenario Endurance
```

### Bước 3: Kiểm tra Dashboard Báo cáo
Mở file `performance-testing/results/<scenario>/html-report/index.html` trên trình duyệt web.
