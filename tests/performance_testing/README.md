# HW05 Performance Testing — Task 1 (23127438 · Đặng Trường Nguyên)

**Workflow:** Category-guided buy — `login → categories → products?search → cart → checkout`
(auth-heavy + read-heavy + transactional, data-driven bằng CSV 60 user).

## Cấu trúc thư mục

```ini
tests/performance_testing/
├── testplans/
│   ├── 23127438_Load_20260815.jmx      (listener: Summary Report)
│   ├── 23127438_Stress_20260815.jmx    (listener: Aggregate Report)
│   ├── 23127438_Spike_20260815.jmx     (listener: View Results Tree)
│   ├── 23127438_Soak_20260815.jmx      (endurance, bổ sung)
│   └── nguyen_users.csv                (60 user, data-driven)
├── results/
│   ├── load/   stress/   spike/   soak/
│   │   ├── *.jtl                        (raw log — nộp đầy đủ)
│   │   ├── html_report/                 (HTML dashboard)
│   │   └── resource_*.csv               (CPU/RAM node backend theo thời gian)
├── scripts/
│   ├── gen_jmx.py                       (sinh 4 test plan)
│   ├── monitor.sh                       (log tài nguyên)
│   └── analyze_jtl.py                   (tính percentile ground-truth)
├── evidence/
│   ├── hardware_report.md               (Apple M4, 10 core, 16GB)
│   ├── lockout_probe.md                 (probe + reset lockout)
│   └── server.log
└── docs/
    ├── test_design.md                   (justify tham số từng kịch bản)
    ├── bug_report.md                    (6 bug phát hiện)
    ├── results_summary.md               (bảng kết quả + endurance threshold)
    └── ai_declaration/                  (AI Audit Report + Disclosure + Privacy Checklist)
        ├── [AI-02] ... AI Audit Report_En.md   (audit table + 7 điểm AI sai/thiếu + kết luận)
        ├── [AI-03] ... AI Disclosure Form_En.md
        ├── [AI-05] ... AI Privacy Checklist_En.md
        └── signature.png
```

## Tóm tắt kết quả

| Kịch bản | VU đỉnh | Samples | Error% | Throughput | p95 | node CPU / RAM đỉnh |
|---|---|---|---|---|---|---|
| Load  | 20  | 3,833  | 0% | 12.8 req/s | 7ms | 5.5% / 47MB |
| Stress| 200 | 63,398 | 0% | 151 req/s  | 7ms | 42% / 102MB |
| Spike | 160 | 22,080 | 0% | 74 req/s   | 6ms | 42% / 70MB |
| Soak  | 30  | 14,719 | 0% | 20.5 req/s | 6ms | 6.7% / 42MB |

__Bằng chứng chụp màn hình__ (`screenshots/`, chạy 2026-08-15 19:13–19:48): `run_{load,stress,spike,soak}_jmeter+monitor.png` (JMeter non-GUI + htop bám process node, chụp tại đỉnh tải), `hardware_screenfetch.png` (Apple M4/16GB), `lockout_reset_steps.png` (probe → reset → verify giữa Stress→Spike), `report_{load,stress,spike}.png` (HTML dashboard).

__Endurance threshold:__ breaking point > 200 VU / > 151 req/s (chưa gãy trong dải test); RAM không leak qua 12 phút soak. Chi tiết: `docs/results_summary.md`.

## Cách tái lập

```bash
# 1. chạy backend HW05
cd eshop-sut/backend && node server.js
# 2. tạo user pool + CSV (đã có sẵn nguyen_users.csv)
# 3. chạy 1 kịch bản (ví dụ Load) + monitor
cd tests/performance_testing
./scripts/monitor.sh results/load/resource_load.csv 340 &
jmeter -n -t testplans/23127438_Load_20260815.jmx \
       -l results/load/23127438_Load_20260815.jtl -e -o results/load/html_report
# 4. phân tích
python3 scripts/analyze_jtl.py results/load/23127438_Load_20260815.jtl
# reset lockout giữa các run stress/spike:
sqlite3 eshop-sut/backend/database.sqlite \
  "UPDATE users SET login_attempts=0, locked_until=NULL;"
```
