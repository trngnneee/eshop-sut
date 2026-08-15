# PERF-SPIKE-01: Spike test — Category-guided buy (nền 10 VU + đột biến 150 VU)

## Requirement ID
HW05 Task 1 — Spike testing; đo phản ứng & hồi phục của workflow phủ 3 nhóm endpoint

## Module / Test type / Technique
Backend API (EShop) / Performance — Spike Testing / JMeter 5.6.3 (non-GUI), data-driven CSV

## Testcase coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Testcase ID | PERF-SPIKE-01 |
| Scenario type | Spike (tải đột biến rồi rút) |
| Actor | Virtual User đã có tài khoản (pool `nguyen01..60`) |
| Goal | Mô phỏng flash-sale: hệ đang chạy êm thì tải tăng ~16× trong 10s; đo độ trễ đỉnh, error burst và thời gian hồi phục. |
| Endpoint(s) | `POST /api/login` → `GET /api/categories` → `GET /api/products?search=` → `POST /api/cart` → `POST /api/checkout` |
| Endpoint groups | Auth-heavy + Read-heavy + Transactional |
| Test plan | `testplans/23127438_Spike_20260815.jmx` (listener: View Results Tree) |
| Traced to | Đề HW05 §6 Task 1 — Spike; quy ước nhóm workflow #3 |

## Preconditions
- Backend chạy tại `localhost:3000`, DB đã seed.
- User pool đã đăng ký; **lockout đã reset ngay trước run** (SQL).
- CSV recycle.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Threads (VU) | Nền **10** suốt 5 phút + **+150** đột biến tại t=90s trong 60s |
| Ramp-up | 10s (rất ngắn cho cú spike) |
| Duration | ~300s (5 phút) |
| Think-time | ~0.3–0.7s |
| CSV | `nguyen_users.csv` (60 dòng, recycle) |
| Listener | View Results Tree (spike ngắn, ít sample nhất) + raw `.jtl` + HTML dashboard |

## Test steps
1. Reset lockout: `sqlite3 ... "UPDATE users SET login_attempts=0, locked_until=NULL;"`.
2. Monitor: `./scripts/monitor.sh results/spike/resource_spike.csv 340 &`.
3. Chạy: `jmeter -n -t testplans/23127438_Spike_20260815.jmx -l results/spike/23127438_Spike_20260815.jtl -e -o results/spike/html_report`.
4. Phân tích: `python3 scripts/analyze_jtl.py results/spike/23127438_Spike_20260815.jtl`.

## Expected result
- Trong đột biến: có thể xuất hiện độ trễ đuôi (max tăng) nhưng error-rate không tăng vọt.
- Sau khi spike rút: latency trở lại mức nền nhanh (hệ hồi phục), không kẹt/không crash.

## Status / Related bugs
Passed — hấp thụ cú sốc 16×, 0 lỗi, hồi phục ngay. Không phát sinh bug chức năng mới.

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-08-15
- Execution interface: JMeter 5.6.3 non-GUI + htop (bám PID node backend), máy Apple M4 / 16GB / macOS 15.5
- Execution time: 19:28–19:33 ICT (lockout reset giữa Stress→Spike, xem `screenshots/lockout_reset_steps.png`)
- Observed:
  - Samples: **22,080** | Error: **0 (0.00%)** | Throughput: **73.71 req/s** | Wall: 300s
  - Latency (ms): mean 2.5 | p90 5 | **p95 6** | p99 10 | **max 33** (đúng thời điểm bơm +150 VU)
  - Per-request p95: login 6 · categories 5 · search 5 · cart 3 · **checkout 8**
  - Node backend: CPU đỉnh **41.5%** · RSS đỉnh **70 MB**
  - **Nhận xét:** p95 vẫn 6ms xuyên suốt, chỉ `max` nhảy lên 33ms lúc spike (throughput tức thời ~222 req/s trong cửa sổ burst); không request nào fail → event-loop Node + SQLite hấp thụ burst tốt và hồi phục ngay sau khi tải rút.
- Execution result: **Passed**
- Evidence: `results/spike/23127438_Spike_20260815.jtl`, `results/spike/html_report/`, `results/spike/resource_spike.csv`, `screenshots/report_spike.png`
- Screenshot: ![PERF-SPIKE-01](../screenshots/run_spike_jmeter+monitor.png) — chụp tại t≈125s giữa cửa sổ spike, Active: 160, node 36.9% CPU
