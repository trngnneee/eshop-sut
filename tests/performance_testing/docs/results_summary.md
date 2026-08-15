# Kết quả Performance Test

- Họ và tên: Đặng Trường Nguyên
- MSSV: 23127438

**Máy test:** Apple M4, 10 cores, 16GB RAM, macOS 15.5 — hostname `192.168.2.5`

**SUT:** EShop backend (Node.js + Express + SQLite), 1 process, `node server.js`

**Công cụ:** JMeter 5.6.3 (non-GUI), think-time mô phỏng người dùng thật.

__Thời điểm chạy (bộ kết quả nộp):__ 2026-08-15, 19:13–19:48 ICT — bằng chứng chụp màn hình trong `screenshots/run_*.png` (JMeter + htop bám process `node server.js`), reset lockout giữa Stress→Spike trong `screenshots/lockout_reset_steps.png`.

## Bảng tổng hợp

| Kịch bản | VU đỉnh | Samples | Error % | Throughput | p95 (ms) | p99 (ms) | max (ms) | node CPU đỉnh | node RSS đỉnh |
|---|---|---|---|---|---|---|---|---|---|
| **Load** | 20 | 3,833 | 0.00% | 12.84 req/s | 7 | 8 | 27 | 5.5% | 47 MB |
| **Stress** | 200 | 63,398 | 0.00% | 151.20 req/s | 7 | 11 | 51 | 41.6% | 102 MB |
| **Spike** | 160 | 22,080 | 0.00% | 73.71 req/s | 6 | 10 | 33 | 41.5% | 70 MB |
| **Soak** | 30 | 14,719 | 0.00% | 20.50 req/s | 6 | 7 | 23 | 6.7% | 42 MB |

## Nhận xét chính

### Load (baseline)

- 20 VU với think-time thực tế → ~12.8 req/s, p95 = 7ms, 0 lỗi. Đây là baseline "ngày thường": hệ nhàn rỗi (CPU ~5%).

### Stress (tìm breaking point)

- Bậc thang tới 200 VU → 151 req/s, vẫn **0 lỗi**, p95 chỉ 7ms — ngang baseline Load dù tải gấp ~12 lần (request rất nhẹ, event-loop chưa bão hòa).
- Node CPU đỉnh 41.6% trên 1 core-equivalent, RSS 102MB. **Chưa chạm breaking point ở 200 VU** — trên phần cứng M4, SUT (Node + SQLite in-process) không phải nút cổ chai ở mức tải này.
- **Kết luận threshold:** ngưỡng gãy nằm **> 200 VU / > 151 req/s**; giới hạn thực tế ở đây là think-time và số VU của JMeter, không phải CPU/RAM của SUT.

### Endpoint nào nặng nhất?

- `POST /api/checkout` luôn có mean/p95 cao nhất (~4–5ms) vì là request **ghi đĩa** (`INSERT INTO orders`, SQLite fsync). Các read (`categories`, `search`) nhẹ nhất (~1.5–2ms) do dữ liệu seed nhỏ, SQLite cache trong RAM.
- Dù `search` chạy `LIKE '%q%'` full-scan, bảng products chỉ 5 dòng nên không tốn — nếu bảng lớn hơn đây sẽ là điểm nóng đầu tiên.

### Spike (tải đột biến)

- Nền 10 VU chạy êm, tại t=90s bơm thêm +150 VU trong 10s (tăng ~16×). Kết quả: **0 lỗi**, p95 vẫn 6ms, chỉ `max` nhảy lên 33ms đúng lúc spike — tức có độ trễ đuôi ngắn nhưng không có request nào fail và hệ **hồi phục ngay** sau khi spike rút (throughput tức thời đạt ~222 req/s trong cửa sổ spike). Node CPU đỉnh 41.5%, RSS 70MB.
- Đây là bằng chứng event-loop của Node + SQLite in-process xử lý burst rất tốt khi payload nhẹ.

### Soak / Endurance (12 phút liên tục)

- 30 VU giữ đều 12 phút → 14,719 request, **0 lỗi**, throughput ổn định **20.5 req/s**, p95 = 6ms xuyên suốt (không drift tăng theo thời gian).
- **Memory:** node RSS dao động ~30–42MB và hạ về ~31MB khi kết thúc, **không có xu hướng leo dốc** → không phát hiện memory leak ở mức tải này. Cart in-memory (BUG-5) chưa gây rò rỉ đáng kể vì GC của V8 thu hồi kịp và mỗi object giỏ nhỏ; leak chỉ đáng lo khi số user đồng thời rất lớn và giỏ nhiều item.
- `max` latency 23ms xuất hiện lẻ tẻ ở `login`/`checkout` — khớp với các đợt GC pause / SQLite checkpoint ghi đĩa, không phải suy giảm bền.

## Endurance threshold (kết luận với số cụ thể)

Trên phần cứng **Apple M4 / 16GB**:

- **RPS ổn định bền vững:** ~20.5 req/s ở 30 VU (soak 12 phút, 0 lỗi) — và cao hơn nhiều: Stress đạt **151 req/s ở 200 VU vẫn 0 lỗi**.
- **Ngưỡng gãy (breaking point):** **chưa đạt tới trong dải test** — SUT không lỗi tới 200 VU. Ngưỡng thực nằm **> 200 VU / > 151 req/s**.
- **Trần CPU:** node process đỉnh ~42% (một core-equivalent) ở 200 VU → còn dư địa lớn (máy 10 core).
- **Trần RAM:** ~102MB ở 200 VU, ổn định ~30–47MB khi tải vừa → **không phải nút cổ chai**.
- **Nút cổ chai thực tế:** không phải SUT, mà là (a) think-time mô phỏng người dùng và (b) khả năng sinh thread của JMeter trên cùng 1 máy. Để tìm điểm gãy thật cần bỏ think-time và/hoặc chạy JMeter phân tán — ghi nhận là giới hạn của thiết lập test 1 máy.
