# PERF-SOAK-01: Soak / Endurance test — Category-guided buy (30 VU / 12 phút)

## Requirement ID
HW05 Task 1 — Endurance threshold; soak ~10–15 phút để tìm ngưỡng chịu tải & rò rỉ bộ nhớ

## Module / Test type / Technique
Backend API (EShop) / Performance — Soak / Endurance Testing / JMeter 5.6.3 (non-GUI), data-driven CSV

## Testcase coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Testcase ID | PERF-SOAK-01 |
| Scenario type | Soak / Endurance (tải bền vững kéo dài) |
| Actor | Virtual User đã có tài khoản (pool `nguyen01..60`) |
| Goal | Giữ tải đều 12 phút để xác định RPS ổn định bền vững, RAM ceiling và phát hiện memory leak (cart in-memory). |
| Endpoint(s) | `POST /api/login` → `GET /api/categories` → `GET /api/products?search=` → `POST /api/cart` → `POST /api/checkout` |
| Endpoint groups | Auth-heavy + Read-heavy + Transactional |
| Test plan | `testplans/23127438_Soak_20260815.jmx` (listener: Graph Results) |
| Traced to | Đề HW05 §6 Task 1 — "Determine the endurance threshold" |

## Preconditions
- Backend chạy tại `localhost:3000`, DB đã seed (đã tích lũy orders từ các run trước — đúng điều kiện quan sát bảng `orders` phình to).
- User pool đã đăng ký; **lockout đã reset trước run** (SQL).
- CSV recycle.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Threads (VU) | 30 (giữ nguyên) |
| Ramp-up | 60s |
| Duration | 720s (12 phút) |
| Think-time | như Load (1–3s) |
| CSV | `nguyen_users.csv` (60 dòng, recycle) |
| Listener | Graph Results + raw `.jtl` + HTML dashboard |
| Monitor | node RSS/CPU mỗi 5s suốt 12 phút (theo dõi xu hướng RAM) |

## Test steps
1. Reset lockout: `sqlite3 ... "UPDATE users SET login_attempts=0, locked_until=NULL;"`.
2. Monitor: `./scripts/monitor.sh results/soak/resource_soak.csv 760 &`.
3. Chạy: `jmeter -n -t testplans/23127438_Soak_20260815.jmx -l results/soak/23127438_Soak_20260815.jtl -e -o results/soak/html_report`.
4. Phân tích + xu hướng RAM: `python3 scripts/analyze_jtl.py results/soak/23127438_Soak_20260815.jtl`; đọc `resource_soak.csv` đầu→cuối.

## Expected result
- Throughput & p95 ổn định suốt 12 phút (không drift tăng theo thời gian → không suy giảm bền).
- node RSS **không leo dốc** liên tục (không memory leak); xác định được RAM ceiling.
- Báo cáo endurance threshold bằng số cụ thể (RPS ổn định, RAM ceiling).

## Status / Related bugs
Passed — 0 lỗi, RPS/p95 phẳng, **không phát hiện memory leak** ở mức 30 VU. Ghi chú: cart in-memory (BUG-5 trong `docs/bug_report.md`) chưa gây leak đáng kể ở tải này vì GC của V8 thu hồi kịp.

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-08-15
- Execution interface: JMeter 5.6.3 non-GUI + Activity Monitor, máy Apple M4 / 16GB / macOS 15.5
- Observed:
  - Samples: **14,678** | Error: **0 (0.00%)** | Throughput ổn định **20.44 req/s** | Wall: 718s
  - Latency (ms): mean 2.5 | p90 5 | **p95 6** | p99 7 | max 118 (GC pause lẻ tẻ, không drift)
  - node RSS dao động **17–63 MB** quanh ~30MB, **không xu hướng leo dốc** → không leak; CPU đỉnh **7.0%**
  - **Endurance threshold (Apple M4 / 16GB):** RPS ổn định bền vững ~**20 req/s @ 30 VU** (soak 12 phút, 0 lỗi); và cao hơn nhiều — Stress đạt **151 req/s @ 200 VU vẫn 0 lỗi**. Trần CPU ~30% / RAM ~125MB → SUT không phải nút cổ chai; breaking point > 200 VU.
- Execution result: **Passed**
- Evidence: `results/soak/23127438_Soak_20260815.jtl`, `results/soak/html_report/`, `results/soak/resource_soak.csv`
- Screenshot: ![PERF-SOAK-01](../screenshots/PERF-SOAK-01.png)
