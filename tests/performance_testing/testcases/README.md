# Test cases — HW05 Task 1 (23127438 · Đặng Trường Nguyên)

Mỗi kịch bản performance test được tách thành một test case riêng (theo template GUI test case của môn, điều chỉnh cho performance testing). Kết quả **Actual result** đã điền theo số liệu thật của các lần chạy ngày 2026-08-15.

| Testcase ID | Scenario | VU đỉnh | Samples | Error | Throughput | p95 | Kết quả |
| :--- | :--- | :---: | ---: | :---: | ---: | :---: | :---: |
| [PERF-LOAD-01](PERF-LOAD-01.md) | Load (baseline) | 20 | 3,809 | 0% | 12.8 req/s | 6ms | **Passed** |
| [PERF-STRESS-01](PERF-STRESS-01.md) | Stress (50→200 VU) | 200 | 63,346 | 0% | 151 req/s | 5ms | **Passed** |
| [PERF-SPIKE-01](PERF-SPIKE-01.md) | Spike (10+150 VU) | 160 | 21,960 | 0% | 73 req/s | 5ms | **Passed** |
| [PERF-SOAK-01](PERF-SOAK-01.md) | Soak / Endurance (30 VU/12′) | 30 | 14,678 | 0% | 20 req/s | 6ms | **Passed** |

- **Endpoint groups** (mọi test case đều phủ đủ 3): Auth-heavy (`login`) · Read-heavy (`categories`, `products?search`) · Transactional (`cart`, `checkout`).
- **Endurance threshold:** breaking point > 200 VU / > 151 req/s (chưa gãy); RAM không leak qua 12 phút soak.
- **Evidence** cho mỗi test case: raw `.jtl` + HTML dashboard + resource CSV trong `results/<scenario>/`.
- **Screenshot** (`../screenshots/PERF-*.png`): chụp JMeter + Activity Monitor cùng khung hình khi quay demo — chưa đính kèm (thao tác tay).
- Bug/issue phát hiện qua đọc source & probe: xem `docs/bug_report.md`.
