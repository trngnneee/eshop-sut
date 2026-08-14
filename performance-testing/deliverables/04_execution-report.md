# 04 — Performance Test Execution Report (Task 1)

> **Học phần:** Kiểm thử Phần mềm (HW05)  
> **Sinh viên:** Khoa (MSSV: **23127207**) · **SUT:** EShop  
> **Kịch bản thực thi:** **Browse-to-buy** (`POST /api/login` $\to$ `GET /api/products` $\to$ `GET /api/products/{id}` $\to$ `POST /api/cart` $\to$ `POST /api/checkout`)  
> **Thời điểm chạy:** `2026-08-14` / `2026-08-15` · **Công cụ:** Apache JMeter 5.6.3 (Non-GUI)  

---

## 1. Điều Kiện Ban Đầu và Quản Lý Trạng Thái SUT

Để đảm bảo tính nhất quán và loại bỏ nhiễu do rò rỉ bộ nhớ tích lũy giữa các kịch bản, mỗi bài kiểm thử đều được khởi động từ một tiến trình Node.js mới tinh (`private_mb` < 100 MB), dữ liệu database được re-seed 400 user + 505 product và reset cờ khóa tài khoản:

| Kịch bản | RAM Khởi đầu (`private_mb`) | RAM Kết thúc (`private_mb`) | Trần RAM (`private_mb`) | Trạng thái Tiến trình Backend |
|:---|---:|---:|---:|:---|
| **Load Test** | **83.67 MB** | 140.97 MB | 173.31 MB | Hoạt động bình thường suốt 300s |
| **Stress Test** | **59.74 MB** | 157.07 MB | 178.08 MB | Hoạt động bình thường suốt 480s |
| **Spike Test** | **59.77 MB** | 143.85 MB | 175.17 MB | Hoạt động bình thường suốt 360s |
| **Endurance Test** | **60.30 MB** | 137.39 MB | 172.49 MB | Hoạt động bình thường suốt 720s |

---

## 2. Bảng Tóm Tắt Kết Quả 4 Kịch Bản Tải Thực Tế (Ground-Truth)

| Kịch bản | Số VU | Thời lượng | Tổng số mẫu | Thông lượng (RPS) | Tỉ lệ lỗi | **p95 Tổng thể (Dashboard Total)** | Đánh giá Kỹ thuật |
|:---|---:|---:|---:|---:|---:|---:|:---|
| **Load Test** | 50 VU | 300 s (5 min) | 9,173 | 30.79 req/s | 0.00% | **25.0 ms** | ✅ **PASS SLO** (p95 < 800ms, Error < 0.1%) |
| **Stress Test** | 25 $\to$ 200 VU | 480 s (8 min) | 26,939 | 56.23 req/s | 0.00% | **586.0 ms** | ⚠️ **Knee point tại 100 $\to$ 200 VU** (p95 tăng từ 26ms lên 761ms) |
| **Spike Test** | 10 VU $\to$ 300 VU | 360 s (6 min) | 11,794 | 32.96 req/s | 0.00% | **1,016.0 ms** | ✅ **Đàn hồi tốt**: p95 đỉnh 1,302ms, phục hồi về 25ms ở 10 VU |
| **Endurance Test**| 30 VU | 720 s (12 min) | 13,355 | 18.62 req/s | 0.00% | **382.0 ms** | ⚠️ **Suy thoái do Heap Leak**: p95 tăng từ 47ms lên 2,112ms |

---

## 3. Chi Tiết Từng Kịch Bản Thực Thi

### 3.1 Kịch bản 1: Load Test (50 VU — 5 Phút)
- **File log gốc:** `results/load/23127207_Load_20260814.jtl`
- **Lệnh kiểm chứng:** `python performance-testing/scripts/analyze_jtl.py --jtl performance-testing/results/load/23127207_Load_20260814.jtl`

| Label | Samples | Err% | Min (ms) | Avg (ms) | p50 (ms) | p90 (ms) | **p95 (ms)** | p99 (ms) | Max (ms) | RPS | Avg Payload |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `01_Login` | 1,861 | 0.00% | 1 | 5.9 | 3 | 8 | **14** | 77 | 214 | 6.25 | 685.6 B |
| `02_BrowseProducts` | 1,835 | 0.00% | 3 | 13.1 | 10 | 19 | **31** | 74 | 280 | 6.16 | 154,044.0 B |
| `03_ProductDetail` | 1,831 | 0.00% | 1 | 6.4 | 3 | 9 | **14** | 136 | 350 | 6.15 | 573.8 B |
| `04_AddToCart` | 1,823 | 0.00% | 0 | 2.2 | 2 | 3 | **4** | 7 | 87 | 6.12 | 294.0 B |
| `05_Checkout` | 1,823 | 0.00% | 9 | 21.9 | 16 | 27 | **38** | 189 | 359 | 6.12 | 314.6 B |
| **TOTAL (Overall)** | **9,173** | **0.00%** | **0** | **9.9** | **3** | **18** | **25** | **104** | **359** | **30.79** | — |

- **Phân tích lát cắt thời gian:** `0-60s`: p95 = 23ms; `60-120s`: 26ms; `120-180s`: 30ms; `180-240s`: 22ms; `240-300s`: 22ms.

---

### 3.2 Kịch bản 2: Stress Test (25 $\to$ 50 $\to$ 100 $\to$ 200 VU — 8 Phút)
- **File log gốc:** `results/stress/23127207_Stress_20260814.jtl`

| Label | Samples | Err% | Min (ms) | Avg (ms) | p50 (ms) | p90 (ms) | **p95 (ms)** | p99 (ms) | Max (ms) | RPS |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `01_Login` | 5,496 | 0.00% | 1 | 112.3 | 8 | 423 | **667** | 1241 | 2121 | 11.47 |
| `02_BrowseProducts` | 5,430 | 0.00% | 4 | 124.7 | 14 | 397 | **696** | 1777 | 2241 | 11.33 |
| `03_ProductDetail` | 5,361 | 0.00% | 1 | 112.0 | 7 | 378 | **671** | 1616 | 2054 | 11.19 |
| `04_AddToCart` | 5,327 | 0.00% | 0 | 41.2 | 3 | 108 | **283** | 609 | 1302 | 11.12 |
| `05_Checkout` | 5,325 | 0.00% | 9 | 107.0 | 25 | 318 | **576** | 1324 | 1966 | 11.11 |
| **TOTAL (Overall)** | **26,939** | **0.00%** | **0** | **99.7** | **8** | **341** | **586** | **1498** | **2241** | **56.23** |

- **Phân bố p95 theo từng Bậc thang Tải (Step Analysis):**
  - **Step 1 (0-120s — 25 VU):** 1,820 samples $\to$ p95 = **26 ms**
  - **Step 2 (120-240s — 50 VU):** 3,886 samples $\to$ p95 = **27 ms**
  - **Step 3 (240-360s — 100 VU):** 7,439 samples $\to$ p95 = **361 ms** (Bắt đầu nghẽn)
  - **Step 4 (360-480s — 200 VU):** 13,794 samples $\to$ p95 = **761 ms** (Tăng x29 lần so với baseline!)
- **Điểm bẻ cong (Knee point):** Hệ thống bắt đầu suy thoái rõ rệt từ mốc **100 VU** trở lên do hàng đợi sự kiện của Node.js bị dồn ứ.

---

### 3.3 Kịch bản 3: Spike Test (10 VU $\to$ 2 đợt Đột biến 300 VU — 6 Phút)
- **File log gốc:** `results/spike/23127207_Spike_20260814.jtl`

| Label | Samples | Err% | Min (ms) | Avg (ms) | p50 (ms) | p90 (ms) | **p95 (ms)** | p99 (ms) | Max (ms) | RPS |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `01_Login` | 2,673 | 0.00% | 1 | 192.3 | 11 | 710 | **1,117** | 2293 | 2598 | 7.47 |
| `02_BrowseProducts` | 2,406 | 0.00% | 4 | 211.0 | 23 | 802 | **1,180** | 1793 | 2467 | 6.72 |
| `03_ProductDetail` | 2,306 | 0.00% | 0 | 163.9 | 18 | 478 | **962** | 2084 | 2566 | 6.44 |
| `04_AddToCart` | 2,211 | 0.00% | 0 | 91.8 | 6 | 207 | **652** | 1304 | 1590 | 6.18 |
| `05_Checkout` | 2,198 | 0.00% | 9 | 193.9 | 33 | 681 | **969** | 2214 | 2460 | 6.14 |
| **TOTAL (Overall)** | **11,794** | **0.00%** | **0** | **172.5** | **16** | **617** | **1,016** | **2119** | **2598** | **32.96** |

- **Phân tích Khả năng Phục hồi (Resilience & Recovery Analysis):**
  - `0-60s (Baseline 10 VU)`: 352 mẫu $\to$ p95 = **27 ms**, 0% lỗi.
  - `60-120s (Burst 1 — 300 VU)`: 5,320 mẫu $\to$ p95 tăng vọt lên **852 ms** (Max 1,489ms), không có lỗi.
  - `120-180s (Phục hồi sau Burst 1 — 10 VU)`: 400 mẫu $\to$ p95 lập tức giảm về **26 ms**!
  - `180-240s (Ổn định nền — 10 VU)`: 417 mẫu $\to$ p95 duy trì **28 ms**.
  - `240-300s (Burst 2 — 300 VU)`: 4,907 mẫu $\to$ p95 tăng lên **1,302 ms** (Max 2,598ms).
  - `300-360s (Phục hồi sau Burst 2 — 10 VU)`: 398 mẫu $\to$ p95 quay về **25 ms**!
- **Kết luận:** Hệ thống có khả năng tự phục hồi tức thời (trong vòng vài giây) ngay khi xung tải đột biến chấm dứt.

---

### 3.4 Kịch bản 4: Endurance Test (30 VU — 12 Phút)
- **File log gốc:** `results/endurance/23127207_Endurance_20260814.jtl`

| Label | Samples | Err% | Min (ms) | Avg (ms) | p50 (ms) | p90 (ms) | **p95 (ms)** | p99 (ms) | Max (ms) | RPS |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `01_Login` | 2,688 | 0.00% | 1 | 86.4 | 4 | 146 | **507** | 1984 | 3622 | 3.75 |
| `02_BrowseProducts` | 2,674 | 0.00% | 3 | 113.0 | 16 | 195 | **459** | 2495 | 3627 | 3.73 |
| `03_ProductDetail` | 2,667 | 0.00% | 0 | 88.4 | 3 | 161 | **475** | 1987 | 3785 | 3.72 |
| `04_AddToCart` | 2,663 | 0.00% | 1 | 36.6 | 2 | 58 | **170** | 765 | 1889 | 3.71 |
| `05_Checkout` | 2,663 | 0.00% | 8 | 92.7 | 23 | 153 | **365** | 1470 | 3049 | 3.71 |
| **TOTAL (Overall)** | **13,355** | **0.00%** | **0** | **83.6** | **5** | **156** | **382** | **1841** | **3785** | **18.62** |

- **Xu hướng suy thoái p95 theo thời gian (Latency Degradation Trend):**
  - `0-120s`: 1,853 mẫu $\to$ p95 = **47 ms**
  - `120-240s`: 2,443 mẫu $\to$ p95 = **46 ms**
  - `240-360s`: 2,428 mẫu $\to$ p95 = **111 ms** (Tăng x2.4)
  - `360-480s`: 2,300 mẫu $\to$ p95 = **525 ms** (Tăng x11.4)
  - `480-600s`: 2,341 mẫu $\to$ p95 = **419 ms**
  - `600-720s`: 1,990 mẫu $\to$ p95 = **2,112 ms** (**Tăng gấp 45 lần so với ban đầu!**)
- **Biến động Bộ nhớ V8 Heap:**
  - RAM Private bắt đầu: **60.30 MB**
  - RAM Private kết thúc: **137.39 MB** (Trần bộ nhớ đạt **172.49 MB**)
  - Tốc độ tăng trưởng bộ nhớ: **`6.45 MB / phút`**
- **Nguyên nhân cốt lõi:** Lỗi rò rỉ bộ nhớ in-memory `userCarts[userId].push(req.body)` tại `backend/server.js:14,293`. Càng nhiều đơn hàng được tạo, mảng giỏ hàng càng phình to mà không có cơ chế giải phóng hay giới hạn kích thước, khiến Garbage Collector của V8 phải tạm dừng (GC Pauses) thường xuyên hơn, đẩy p95 lên trên 2 giây.
