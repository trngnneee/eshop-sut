# Task 2 — AI Analysis & Misinterpretation Hunt

- Họ và tên: Đặng Trường Nguyên
- MSSV: 23127438
- AI tool: Claude Code (Claude Opus 4.8) · ngày 15/08/2026
- Ground truth: `scripts/analyze_jtl.py` chạy trực tiếp trên 4 file `.jtl` thô (độc lập với dashboard JMeter)

> **Quy trình AI-first:** (1) đưa log `.jtl` cho AI, prompt nó phân tích + đề xuất threshold → **output là của AI**; (2) tôi đối chiếu từng con số với `.jtl` thô để **săn lỗi diễn giải** → phần review là của tôi; (3) prompt AI đề xuất optimization rồi tự phân loại **feasible / hallucinated**.

---

## 0. Ground truth — số thật tính từ `.jtl` thô

Chạy `python3 scripts/analyze_jtl.py results/<scenario>/<file>.jtl`. Đây là "sự thật" để chấm mọi phát biểu của AI:

| Kịch bản | Samples | Error % | Wall | Throughput | mean | median | p90 | p95 | p99 | max |
|---|---|---|---|---|---|---|---|---|---|---|
| Load  | 3,833  | 0.00% | 298.4s | **12.84 req/s** | 3.2 | 3 | 6 | **7** | 8 | 27 |
| Stress| 63,398 | 0.00% | 419.3s | **151.20 req/s**| 2.6 | 2 | 5 | **7** | 11 | 51 |
| Spike | 22,080 | 0.00% | 299.6s | **73.71 req/s** | 2.5 | 2 | 5 | **6** | 10 | 33 |
| Soak  | 14,719 | 0.00% | 717.9s | **20.50 req/s** | 2.6 | 2 | 5 | **6** | 7 | 23 |

Per-request (đơn vị **ms**), trích từ output script:

| Endpoint | Load mean/p95/max | Stress mean/p95/max |
|---|---|---|
| 01 POST /api/login          | 3.2 / 5 / 27 | 2.7 / 6 / 51 |
| 02 GET /api/categories      | 2.4 / 4 / 13 | 2.0 / 5 / 32 |
| 03 GET /api/products?search | 2.4 / 4 / 7  | 2.0 / 5 / 42 |
| 04 POST /api/cart           | 2.4 / 4 / 9  | 1.4 / 3 / 35 |
| 05 POST /api/checkout       | **5.9 / 8 / 21** | **5.2 / 9 / 38** |

**Kết luận ground truth:** 0 lỗi trên toàn bộ 104,030 request; đơn vị latency là **mili-giây**; endpoint nặng nhất là **checkout** (ghi đĩa), không phải search.

---

## 1. Phân tích của AI (output nguyên trạng)

**Prompt (verbatim):** *"Đây là kết quả JMeter cho 4 kịch bản Load/Stress/Spike/Soak của workflow login→categories→search→cart→checkout (trích header + summary của file .jtl đính kèm). Phân tích hiệu năng và đề xuất performance threshold (p95, throughput, error rate). Chỉ ra endpoint bottleneck."*

**AI trả về:**

> **Phân tích hiệu năng — EShop backend**
>
> 1. **Load:** throughput **12.84 req/s**, thời gian phản hồi **trung bình ~7ms**. Hệ thống ổn định.
> 2. **Stress (200 VU):** độ trễ đuôi **chạm 51ms** → có dấu hiệu **suy giảm (degradation)** khi tải cao.
> 3. **CPU node đạt 42%** ở mức Stress → hệ thống đã **gần bão hòa (saturated)**; xem như **breaking point** của SUT.
> 4. **Bottleneck** là endpoint `GET /api/products?search` do dùng `LIKE '%...%'` quét toàn bảng — request chậm nhất, cần tối ưu trước.
> 5. **Công suất tối đa** quan sát được ~**12.8 req/s** (đo ở Load).
>
> **Đề xuất threshold:** p95 < 500ms; error rate < 5%; throughput mục tiêu ≥ 100 req/s.
>
> **Đề xuất tối ưu:** (a) thêm index cho `products.name` để tăng tốc search; (b) thêm index cho `users.email`; (c) bật SQLite WAL; (d) thêm **connection pool** cho SQLite; (e) thêm **Redis cache** cho categories/products; (f) chạy **Node cluster / PM2** đa nhân; (g) tăng **DB connection timeout** để hết các spike 51ms.

---

## 2. Human review — Misinterpretation hunt

Đối chiếu từng phát biểu với `.jtl` thô. **5 lỗi diễn giải:**

| # | AI nói | Giá trị đúng (từ `.jtl`) | Loại lỗi | Vì sao AI sai |
|---|---|---|---|---|
| __M1__ | Thời gian phản hồi __trung bình ~7ms__ (Load) | 7ms là __p95__; __mean = 3.2ms, median = 3ms__ | __Nhầm p95 với mean__ | AI lấy đường 95%-line trên dashboard gọi thành "average"; không phân biệt phân vị với trung bình. mean ≠ p95. |
| __M2__ | Đuôi __51ms → suy giảm khi tải cao__ (Stress) | 51ms là __max của 1 sample__ (1/63,398); __p99 chỉ 11ms__; 0 lỗi | __Đọc max lẻ thành xu hướng hệ thống__ | AI thấy số lớn nhất trong summary rồi suy ra degradation, không xét đó là điểm ngoại lai đơn lẻ (GC pause / SQLite checkpoint). |
| __M3__ | CPU 42% → hệ thống __bão hòa / breaking point__ | 42% là của __1 process trên máy 10 core__ (~4% tổng CPU); RSS 102MB; __0 lỗi, p95 không đổi__ | __Diễn giải sai bão hòa__ | AI coi "42%" là 42% toàn máy. Bão hòa phải kèm error tăng / latency leo dốc — cả hai đều không xảy ra. |
| __M4__ | Bottleneck là __search__ (`LIKE` full scan) | Nặng nhất là __checkout__: mean 5.2ms vs search 2.0ms (Stress) | __Suy từ code, trái số đo__ | AI suy từ `LIKE '%q%'` mà bỏ qua số đo per-request; bảng products chỉ 5 dòng nên full-scan không tốn, còn checkout ghi đĩa (`INSERT orders` + fsync) mới chậm nhất. |
| __M5__ | Công suất __tối đa__ ~12.8 req/s | 12.8 req/s là __baseline có think-time__ (Load); Stress đã đạt __151 req/s__ vẫn 0 lỗi | __Bỏ qua think-time / nhầm baseline với capacity__ | AI lấy số của kịch bản tải nhẹ làm "trần". Trần thật > 151 req/s; giới hạn là think-time + JMeter 1 máy, không phải SUT. |

**Ba lỗi ảnh hưởng nhất:** M3 (kết luận sai breaking point), M4 (sai bottleneck), M5 (báo sai công suất hệ thống thấp 12× so với thực đo)

---

## 3. Chốt lại threshold (sau review)

Threshold AI đề xuất **quá lỏng và không bám dữ liệu** (p95 < 500ms trong khi p95 thật chỉ 6–7ms → không bao giờ báo động; error < 5% che mất mọi lỗi thật). Ngưỡng đúng phải neo vào **baseline đo được** (regression-based):

| Metric | AI đề xuất | Chốt lại (bám ground truth) | Lý do |
|---|---|---|---|
| p95 latency | < 500ms | **cảnh báo nếu p95 > 25ms** (≈ 3–4× baseline 6–7ms) | 500ms lỏng tới mức vô nghĩa cho SUT này; ngưỡng tương đối bắt được regression thật. |
| p99 latency | (không nêu) | **< 30ms**; điều tra nếu max > 100ms lặp lại | Phân biệt tail-spike lẻ (GC/checkpoint) với suy giảm bền. |
| Error rate | < 5% | **< 0.5%** (baseline = 0%) | 5% che mất mọi lỗi thật; SUT hiện 0 lỗi nên ngưỡng phải sát 0. |
| Throughput | ≥ 100 req/s (chung chung) | **≥ 140 req/giây** ở 200 VU (regression nếu tụt > 20%) | Neo vào 151 req/s đã đo được, đặt sàn tương đối để bắt regression. |
| Breaking point | "đạt ở 200 VU" | **> 200 VU / > 151 req/s** (chưa gãy trong dải test) | Chưa có lỗi/latency leo → chưa chạm ngưỡng gãy. |

---

## 4. Judge optimizations — feasible vs hallucinated

Đối chiếu từng đề xuất với code thật (`backend/server.js`, `backend/database.js`; driver `sqlite3` async, **không phải** better-sqlite3):

| # | Đề xuất của AI | Phân loại | Lý do (đối chiếu code) |
|---|---|---|---|
| a | Index cho `products.name` để tăng tốc __search__ | __Hallucinated / vô hiệu__ | Query là `LIKE '%${q}%'` (`server.js:144`) — __leading wildcard__ khiến B-tree index __không dùng được__. Muốn tăng tốc phải dùng __FTS5__ hoặc bỏ wildcard đầu. Thêm index thường sẽ _không_ giúp gì. |
| b | Index cho `users.email` | __Feasible__ | Login chạy `SELECT * FROM users WHERE email = ?` (`server.js:35,70`), hiện __không có index__ trên `email` (chỉ PK trên `id`). Index này đúng hướng và sẽ scale khi user pool lớn (giờ chỉ 2 seed nên lợi ích thực đo ~0). |
| c | Bật __SQLite WAL__ | __Feasible__ | `database.js` __không set `journal_mode`__ → đang dùng rollback journal mặc định. `PRAGMA journal_mode=WAL` cho phép đọc song song lúc ghi → hợp với checkout (`INSERT orders`, endpoint nặng nhất). Đề xuất hợp lý, chi phí thấp. |
| d | Thêm __connection pool__ cho SQLite | __Hallucinated (cho SUT này)__ | `sqlite3` là DB __nhúng 1 file, 1 connection serialize__ — không phải mô hình client-server như Postgres/MySQL. Ghi luôn serialize ở tầng file; "pool" không áp dụng và không tăng throughput. AI bê pattern từ DB mạng sang. |
| e | __Redis cache__ cho categories/products | __Feasible nhưng thừa / ngoài scope__ | Về kỹ thuật khả thi, nhưng read hiện đã __~2ms__ (SQLite cache trong RAM, seed 5 dòng). Thêm Redis là tối ưu sớm, thêm hạ tầng ngoài SUT — không đáng ở tải này. Chỉ hợp khi bảng lớn + read-heavy thật. |
| f | __Node cluster / PM2__ đa nhân | __Feasible nhưng có bẫy__ | Máy 10 core, 1 process chỉ dùng ~1 core → về lý thuyết cluster tăng thông lượng. __Nhưng__ giỏ hàng lưu __in-memory__ (`userCarts`, BUG-5) không chia sẻ giữa worker → cluster sẽ __làm hỏng trạng thái giỏ__; SQLite ghi cũng tranh chấp file. Chỉ khả thi nếu chuyển cart sang store dùng chung trước. |
| g | Tăng __DB connection timeout__ để hết spike 51ms | __Hallucinated__ | 51ms là __max lẻ 1 sample__ (GC pause / SQLite checkpoint), __không phải timeout__ (0 lỗi, không có request bị hủy). Chỉnh timeout không liên quan nguyên nhân. Dựa trên M2 (đọc sai max lẻ) vốn đã bị hiểu nhầm. |

**Tổng kết phán xét:** 3 feasible thẳng (b, c) + 2 feasible-có-điều-kiện (e, f), **3 hallucinated** (a, d, g). Đáng chú ý: index `users.email` và WAL là hai đề xuất *đúng và rẻ*; còn index cho search, connection pool, và "tăng timeout" là AI áp mẫu sai ngữ cảnh SQLite/embedded.

---

## 5. Bài học

- AI mạnh ở **khung phân tích** (biết cần p95/throughput/error/bottleneck, biết tên các optimization) nhưng **yếu ở diễn giải con số**: nhầm p95 với mean (M1), đọc max lẻ thành xu hướng suy giảm (M2), suy sai bão hòa/bottleneck từ 42% CPU và code `LIKE` (M3, M4), nhầm baseline với capacity (M5); phần optimization thì **áp pattern DB mạng cho SQLite nhúng** (d, a).
- Nguồn gốc lỗi: AI suy diễn từ mẫu chung ("tải cao thì phải suy giảm", "search LIKE thì phải chậm") và đọc summary thiếu ngữ cảnh, thay vì đọc **số đo thô** và **code thật**.
- Nguyên tắc rút ra: luôn tự tính lại percentile từ `.jtl` thô làm ground truth; mọi con số AI nêu phải **trace ngược về log**; đề xuất tối ưu phải **đối chiếu driver/áp dụng thực tế** trước khi tin.
