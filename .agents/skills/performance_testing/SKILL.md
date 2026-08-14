---
name: Performance Testing and Log Analysis Skill
description: Kỹ năng hỗ trợ thiết kế, sinh và phân tích kiểm thử hiệu năng (Load / Stress / Spike / Endurance) cho các nhóm endpoint REST API bằng Apache JMeter, từ file cấu hình JSON mô tả workflow, kèm phân tích log .jtl và sinh báo cáo.
---

# Performance Testing and Log Analysis Skill

## 1. Giới thiệu
Kỹ năng này cung cấp quy trình và bộ công cụ tự động hóa từ đầu đến cuối cho kiểm thử hiệu năng REST API:
1. **Thiết kế & Sinh Test Plan:** Tự động chuyển đổi file cấu hình JSON mô tả workflow thành file `.jmx` chuẩn cho Apache JMeter 5.6.3 mà không hard-code endpoint hay tham số tải.
2. **Phân tích Log Định lượng:** Đọc log raw `.jtl`, tính toán bách phân vị p50/p90/p95/p99 theo chuẩn **nearest-rank (ISO 80000-2)** khớp 100% với JMeter HTML dashboard.
3. **So sánh Phát hiện Regression:** Tự động so sánh hai lần chạy hoặc so sánh với baseline để cảnh báo suy thoái hiệu năng theo cơ chế delta tương đối.

---

## 2. Cấu trúc Kỹ năng

```
.agents/skills/performance_testing/
├── SKILL.md
├── scripts/
│   ├── generate_jmx.py        # Config JSON -> .jmx test plan
│   ├── analyze_jtl.py         # .jtl raw CSV -> summary.json + summary.md
│   └── compare_runs.py        # So sánh 2 run bắt regression
├── examples/
│   ├── browse_to_buy_config.json      # Workflow Browse-to-buy (Khoa)
│   └── coupon_checkout_config.json    # Workflow Coupon Checkout (Thịnh) — chứng minh tái sử dụng
└── templates/
    └── report_template.md
```

---

## 3. Quy trình 6 Bước Chuẩn mực

### Bước 1 — Phân loại Endpoint & Ranh giới Scope
- Phân loại endpoint theo 3 nhóm: **Auth-heavy**, **Read-heavy**, **Transactional**.
- Xác định rõ danh sách `excluded_endpoints` để tránh vi phạm phân công nhóm.

### Bước 2 — Khảo sát Đặc thù Cài đặt SUT
- Đọc mã nguồn backend để kiểm tra cơ chế lockout (ngưỡng và thời gian khóa thật), các endpoint trả `200` khi rỗng, tình trạng rò rỉ bộ nhớ in-memory và tranh chấp khóa SQLite.

### Bước 3 — Chuẩn bị Dữ liệu CSV
- Sinh số lượng tài khoản $\ge$ số VU đỉnh của mọi kịch bản.
- Cấu hình `Sharing mode = All threads` và `Allow quoted data = true`.

### Bước 4 — Sinh Test Plan bằng `generate_jmx.py`
```powershell
python .agents/skills/performance_testing/scripts/generate_jmx.py `
  --config .agents/skills/performance_testing/examples/browse_to_buy_config.json `
  --scenario Load `
  --out performance-testing/test-plans/23127207_Load_20260814.jmx
```

### Bước 5 — Thực thi & Giám sát Tài nguyên
- Chạy JMeter ở chế độ **Non-GUI** (`-n`).
- Thu thập raw `.jtl`, HTML dashboard và log CPU/RAM song song.

### Bước 6 — Phân tích Kết quả & So sánh
```powershell
python .agents/skills/performance_testing/scripts/analyze_jtl.py `
  --jtl results/load/run.jtl --out-dir results/load --slice-sec 60

python .agents/skills/performance_testing/scripts/compare_runs.py `
  --baseline baseline.json --current results/load/summary.json
```

---

## 4. Hướng dẫn Tương tác cho AI Agent

Khi Agent nhận nhiệm vụ kiểm thử hiệu năng cho một endpoint group mới:
1. **Tuyệt đối không hard-code** đường dẫn XML thủ công. Hãy yêu cầu hoặc tự soạn file cấu hình `workflow_config.json`.
2. **Luôn chạy `generate_jmx.py`** để tạo file `.jmx` hợp lệ.
3. Khi phân tích log, **luôn chạy `analyze_jtl.py`** để lấy số liệu ground-truth từ `.jtl` thay vì đoán mò số liệu từ trí nhớ.
4. Đối chiếu các đề xuất tối ưu hóa với đặc tính công nghệ của hệ thống (ví dụ: không đề xuất Connection Pool cho SQLite, không đề xuất Index cho truy vấn không có WHERE).
