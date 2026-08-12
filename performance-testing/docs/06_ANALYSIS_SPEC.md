# 06 — ANALYSIS SPEC (`analyze_jtl.py`)

> Script này là **nguồn sự thật** (ground truth) cho Task 2. Mọi con số dùng để phản biện AI trong
> `deliverables/06_ai-analysis-critique.md` phải đến từ đây, chứ không từ trí nhớ hay từ HTML dashboard đọc bằng mắt.

---

## 1. Vì sao cần script riêng khi JMeter đã có HTML dashboard

| Lý do | Giải thích |
| :--- | :--- |
| **Trích dẫn được** | Đề §6 Task 2 yêu cầu *"cite the correct value from your raw `.jtl` log"*. Cần con số kèm cách tính minh bạch, tái lập được |
| **Kiểm chứng chéo** | Nếu script và HTML dashboard cho cùng p95, ta biết cả hai đều đúng. Lệch nhau → phải truy nguyên trước khi viết báo cáo |
| **Cắt lát theo thời gian** | Dashboard cho toàn run; ta cần so p95 **2 phút đầu** với **2 phút cuối** (endurance), và p95 **từng bậc** (stress). Dashboard không làm được |
| **Máy đọc được** | `summary.json` đưa thẳng vào prompt cho AI ở Task 2 |

---

## 2. Đầu vào

File `.jtl` định dạng CSV, header do `jmeter-user.properties` quy định (`04_JMX_BUILD_SPEC.md` §7):

```
timeStamp,elapsed,label,responseCode,responseMessage,threadName,dataType,success,failureMessage,bytes,sentBytes,grpThreads,allThreads,URL,Latency,IdleTime,Connect
```

| Cột dùng | Ý nghĩa | Lưu ý |
| :--- | :--- | :--- |
| `timeStamp` | epoch **milliseconds** | Không phải giây. Nhầm đơn vị là lỗi kinh điển |
| `elapsed` | **Response time** đầy đủ (ms): từ lúc gửi byte đầu tới lúc nhận byte cuối | Đây mới là thứ gọi là "response time" |
| `Latency` | Thời gian tới **byte đầu tiên** của response (ms) | **Không phải** response time. Với payload lớn như `02_BrowseProducts`, `elapsed` lớn hơn `Latency` đáng kể |
| `Connect` | Thời gian bắt tay TCP (ms) | Là **một phần** của `Latency`, không cộng thêm |
| `label` | Tên sampler (`01_Login` …) | Khóa nhóm |
| `success` | `true` / `false` | JMeter tính theo assertion, **không chỉ** theo status code |
| `responseCode` | `200`, `401`, `403`, `500`, hoặc `Non HTTP response code:...` | |
| `allThreads` | Số thread đang hoạt động toàn test tại thời điểm mẫu | Dùng để cắt lát theo bậc ở Stress |
| `bytes` | Kích thước response | Dùng chứng minh `02_BrowseProducts` nặng payload |

---

## 3. Đầu ra

### 3.1 `summary.json`

```json
{
  "source_file": "results/load/23127207_Load_20260812.jtl",
  "generated_at": "2026-08-12T14:32:10",
  "run": {
    "start_ts": 1755000000000,
    "end_ts":   1755000300000,
    "duration_sec": 300.0,
    "total_samples": 12480,
    "total_errors": 3,
    "error_rate_pct": 0.024,
    "throughput_rps": 41.6,
    "max_concurrent_threads": 50
  },
  "labels": {
    "02_BrowseProducts": {
      "count": 2496,
      "errors": 0,
      "error_rate_pct": 0.0,
      "elapsed": { "min": 12, "avg": 187.4, "max": 1832,
                   "p50": 165, "p90": 342, "p95": 421, "p99": 903 },
      "latency": { "avg": 151.2, "p95": 380 },
      "bytes":   { "avg": 148332.0, "total": 370236672 },
      "throughput_rps": 8.32
    }
  },
  "errors_breakdown": { "500": 3 },
  "time_slices": [
    { "slice": "0-60s",    "samples": 1180, "p95": 388, "error_rate_pct": 0.0 },
    { "slice": "60-120s",  "samples": 2510, "p95": 415, "error_rate_pct": 0.0 }
  ]
}
```

### 3.2 `summary.md`

Bảng Markdown dán thẳng được vào báo cáo:

```markdown
### Load — 23127207_Load_20260812

**Tổng quan:** 12.480 mẫu · 300,0 s · 41,60 req/s · lỗi 0,024 % · tối đa 50 thread

| Label | Count | Err% | Min | Avg | p50 | p90 | **p95** | p99 | Max | RPS | Avg bytes |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 01_Login | 2496 | 0,00 | 3 | 18,2 | 15 | 31 | **42** | 88 | 210 | 8,32 | 412 |
| 02_BrowseProducts | 2496 | 0,00 | 12 | 187,4 | 165 | 342 | **421** | 903 | 1832 | 8,32 | 148332 |
| ... |
```

---

## 4. Định nghĩa percentile — nearest-rank, ghi rõ trong báo cáo

Có nhiều cách tính percentile cho ra kết quả **khác nhau**. Phải chốt một cách và công bố, nếu không việc "AI nói p95 = X, thực tế = Y" sẽ thành tranh cãi về phương pháp thay vì về sự thật.

**Chọn: nearest-rank (ISO 80000-2 / phương pháp JMeter dùng).**

```
Cho n giá trị elapsed đã sắp tăng dần: x[0] .. x[n-1]
rank = ceil(p / 100 × n)            # p = 95 -> p95
index = max(0, rank - 1)
percentile = x[index]
```

Ví dụ n = 100, p = 95 → rank = 95 → index 94 → giá trị lớn thứ 95.

Trong Python:
```python
import math
def percentile_nearest_rank(sorted_values, p):
    n = len(sorted_values)
    if n == 0:
        return None
    rank = math.ceil(p / 100.0 * n)
    return sorted_values[max(0, rank - 1)]
```

> ⚠️ **Không dùng `numpy.percentile` mặc định** — nó dùng nội suy tuyến tính, cho kết quả lệch vài ms so với JMeter. Chênh lệch nhỏ nhưng đủ để phá vỡ luận điểm "con số của AI sai, con số đúng là X".
>
> Ghi câu này vào báo cáo: *"Percentile được tính theo nearest-rank, cùng phương pháp JMeter, để đối chiếu được với HTML dashboard."*

---

## 5. Đặc tả CLI

```powershell
python performance-testing\scripts\analyze_jtl.py `
  --jtl "performance-testing\results\load\23127207_Load_20260812.jtl" `
  --out-dir "performance-testing\results\load" `
  --scenario Load `
  --slice-sec 60
```

| Tham số | Bắt buộc | Mặc định | Ý nghĩa |
| :--- | :---: | :--- | :--- |
| `--jtl` | ✔ | | Đường dẫn file `.jtl` |
| `--out-dir` | | thư mục chứa `.jtl` | Nơi ghi `summary.json` + `summary.md` |
| `--scenario` | | suy từ tên file | Nhãn hiển thị |
| `--slice-sec` | | `60` | Độ rộng lát cắt thời gian |
| `--resource-csv` | | | Nếu truyền, gộp thống kê RAM/CPU vào `summary.json` |

### 5.1 Yêu cầu triển khai

| Mục | Yêu cầu |
| :--- | :--- |
| Thư viện | **Chỉ dùng standard library** (`csv`, `json`, `math`, `argparse`, `statistics`, `datetime`). Không cần `pip install`, chạy được trên máy TA |
| Bộ nhớ | File `.jtl` của Spike có thể hàng trăm nghìn dòng → đọc bằng `csv.DictReader` theo dòng, chỉ giữ list `elapsed` theo label |
| Encoding | Mở với `encoding='utf-8'`; nếu lỗi thì fallback `utf-8-sig` (JMeter đôi khi ghi BOM) |
| Dòng hỏng | Bỏ qua dòng thiếu cột, **đếm và báo cáo** số dòng bỏ qua — không im lặng nuốt |
| Số học | Làm tròn 2 chữ số thập phân cho avg/rps/pct; percentile giữ **số nguyên** ms |

### 5.2 Cách tính từng metric

| Metric | Công thức | Bẫy phải tránh |
| :--- | :--- | :--- |
| `duration_sec` | `(max(timeStamp + elapsed) − min(timeStamp)) / 1000` | Không dùng `max(timeStamp) − min(timeStamp)`: bỏ sót thời gian chạy của request cuối |
| `throughput_rps` (toàn run) | `total_samples / duration_sec` | |
| `throughput_rps` (theo label) | `count_label / duration_sec` — dùng **duration toàn run**, không phải khoảng riêng của label | Nếu chia theo khoảng riêng, các label sẽ cho tổng RPS lớn hơn thực tế |
| `error_rate_pct` | `count(success == 'false') / count × 100` | Đếm theo cột `success`, **không** theo `responseCode != 200`. JMeter đánh `success=false` cả khi assertion fail dù status 200 |
| `p95` | nearest-rank trên list `elapsed` **đã sort** | Sort trước khi lấy, và sort riêng cho từng label |
| `max_concurrent_threads` | `max(allThreads)` | |

---

## 6. Cắt lát thời gian — bắt buộc cho Stress và Endurance

### 6.1 Stress: p95 theo từng bậc tải

Với `--slice-sec 120`, script cắt run 480 s thành 4 lát khớp 4 bậc ở `03_TEST_DESIGN.md` §4.2:

| Lát | Bậc | VU đồng thời kỳ vọng |
| :--- | :--- | :---: |
| 0–120 s | Bậc 1 | 25 |
| 120–240 s | Bậc 2 | 50 |
| 240–360 s | Bậc 3 | 100 |
| 360–480 s | Bậc 4 | 200 |

Mỗi lát báo cáo: `samples`, `p95`, `error_rate_pct`, `avg_allThreads`.

`avg_allThreads` là **kiểm chứng** rằng thiết kế bậc thang hoạt động đúng. Nếu lát 4 cho `avg_allThreads ≈ 100` thay vì ~200 thì cấu hình `Startup delay`/`Duration` sai — phải sửa `.jmx` và chạy lại, đừng báo cáo số sai.

**Điểm gãy (knee point)** = bậc đầu tiên mà p95 tăng **phi tuyến** so với bậc trước (ví dụ p95 tăng > 2× trong khi VU chỉ tăng 2×) hoặc `error_rate_pct` vượt 1 %.

### 6.2 Endurance: phát hiện trôi theo thời gian

Với `--slice-sec 120` trên run 720 s → 6 lát. Báo cáo:

| Chỉ số | Cách tính | Ý nghĩa |
| :--- | :--- | :--- |
| **Trôi p95** | `p95(lát cuối) − p95(lát đầu)` và tỉ lệ % | Tăng > 20 % ⇒ có suy giảm theo thời gian |
| **Ổn định throughput** | Độ lệch chuẩn RPS giữa các lát | |
| **Xu hướng RAM** | Hồi quy tuyến tính `private_mb` theo thời gian từ `--resource-csv` → **MB/phút** | Hệ số góc > 0 rõ rệt ⇒ memory leak |
| **Trần RAM** | `max(private_mb)` | Con số "memory ceiling" đề yêu cầu |

### 6.3 Spike: cửa sổ phục hồi

Cắt thủ công theo dòng thời gian ở `03_TEST_DESIGN.md` §4.3:

| Cửa sổ | Khoảng | Ý nghĩa |
| :--- | :--- | :--- |
| Trước sốc | 0–60 s | Baseline sạch |
| Sốc 1 | 60–90 s | Đỉnh tải |
| Phục hồi 1 | 90–240 s | So p95 với "trước sốc" |
| Sốc 2 | 240–270 s | |
| Phục hồi 2 | 270–360 s | So với "phục hồi 1" để tìm suy giảm tích lũy |

**Thời gian phục hồi** = số giây từ khi spike kết thúc tới khi p95 của baseline quay về trong phạm vi 110 % giá trị trước sốc.

---

## 7. Đối chiếu bắt buộc với HTML dashboard

Sau khi chạy script, mở `results/<scen>/html-report/index.html` → tab **Statistics** và so:

| Cột dashboard | Trường trong `summary.json` | Dung sai |
| :--- | :--- | :--- |
| `#Samples` | `labels.<label>.count` | phải **bằng chính xác** |
| `Error %` | `labels.<label>.error_rate_pct` | ≤ 0,01 điểm phần trăm |
| `Average` | `labels.<label>.elapsed.avg` | ≤ 1 ms |
| `95th pct` | `labels.<label>.elapsed.p95` | ≤ 1 ms |
| `Throughput` | `labels.<label>.throughput_rps` | ≤ 0,1 req/s |

**Lệch quá dung sai ⇒ dừng lại, truy nguyên.** Nguyên nhân hay gặp:

| Triệu chứng | Nguyên nhân |
| :--- | :--- |
| p95 lệch vài ms | Dùng nội suy thay vì nearest-rank (§4) |
| Error% lệch | Đếm theo `responseCode` thay vì cột `success` |
| Count lệch | Không bỏ qua dòng header, hoặc `.jtl` bị ghi nối từ run trước |
| Throughput lệch nhiều | Tính `duration` sai (§5.2) |

Ghi kết quả đối chiếu này vào báo cáo — nó chính là bằng chứng rằng "giá trị đúng" ở Task 2 thực sự đúng.

---

## 8. Chạy hàng loạt cho cả 4 kịch bản

```powershell
$pt = "C:\My Workspace\HCMUS\Test\Week 3\Hw2\performance-testing"
$date = "20260812"

@(
  @{ s='Load';      slice=60  },
  @{ s='Stress';    slice=120 },
  @{ s='Spike';     slice=30  },
  @{ s='Endurance'; slice=120 }
) | ForEach-Object {
  $lower = $_.s.ToLower()
  python "$pt\scripts\analyze_jtl.py" `
    --jtl "$pt\results\$lower\23127207_$($_.s)_$date.jtl" `
    --out-dir "$pt\results\$lower" `
    --scenario $_.s `
    --slice-sec $_.slice `
    --resource-csv "$pt\results\$lower\resource-$lower.csv"
}
```

> `--slice-sec` khác nhau theo kịch bản là có chủ ý: Spike dùng 30 s để nhìn được cú sốc kéo dài đúng 30 s; Stress dùng 120 s để khớp từng bậc.

---

## 9. Bảng tổng hợp cho báo cáo

Sau khi có 4 `summary.json`, gộp thành một bảng so sánh trong `deliverables/05_endurance-threshold.md`:

| Kịch bản | VU đỉnh | Samples | RPS | Err% | p95 `02_Browse` | p95 `05_Checkout` | RAM đỉnh (MB) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Load | 50 | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` |
| Stress | 200 | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` |
| Spike | 310 | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` |
| Endurance | 30 | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` |

Và kết luận ngưỡng chịu tải, dạng câu có số:

> *"Trên phần cứng `<<hostname>>` (`<<CPU>>`, `<<RAM>>` GB), SUT giữ được p95 dưới `<<X>>` ms với error rate dưới `<<Y>>` % ở mức tối đa `<<Z>>` VU đồng thời, tương đương `<<R>>` req/s. Vượt mức này, p95 tăng phi tuyến từ `<<A>>` ms lên `<<B>>` ms và error rate lên `<<C>>` %. Trần bộ nhớ quan sát được của tiến trình backend là `<<M>>` MB, tăng `<<G>>` MB/phút trong suốt 12 phút chạy bền và không giảm sau khi tải kết thúc."*

---

## 10. Checklist

- [ ] `analyze_jtl.py` chỉ dùng standard library
- [ ] Percentile theo **nearest-rank**, có ghi chú phương pháp trong output
- [ ] `error_rate` tính theo cột `success`, không theo `responseCode`
- [ ] Phân biệt đúng `elapsed` / `Latency` / `Connect`
- [ ] Sinh đủ `summary.json` + `summary.md` cho cả 4 kịch bản
- [ ] **Đã đối chiếu** với HTML dashboard, mọi sai lệch trong dung sai §7
- [ ] Có lát cắt thời gian cho Stress (4 bậc) và Endurance (6 lát)
- [ ] `avg_allThreads` từng bậc Stress khớp thiết kế (25/50/100/200)
- [ ] Đã tính xu hướng RAM (MB/phút) và trần RAM
