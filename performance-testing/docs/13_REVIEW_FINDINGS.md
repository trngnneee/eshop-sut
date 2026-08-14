# 13 — REVIEW FINDINGS: Kiểm định kết quả Antigravity đã thực thi

> **Người review:** Claude (đọc trực tiếp `.jtl`, `resource-*.csv`, `html-report`, `.jmx`, script — không đọc qua báo cáo)
> **Ngày review:** 2026-08-14
> **Đối tượng:** toàn bộ `performance-testing/**` + `.agents/skills/performance_testing/**` + `.github/workflows/`
> **Mục đích:** danh sách lỗi có bằng chứng + hướng sửa chính xác, để agent tiếp theo (Gemini/Antigravity) sửa được mà không phải điều tra lại.

---

## 0. Tóm tắt điều hành

**Phần hạ tầng làm rất tốt.** 4 kịch bản đã chạy thật, `.jtl` là log gốc hợp lệ, HTML dashboard sinh đúng, scope nhóm sạch tuyệt đối, `analyze_jtl.py` tính percentile **khớp 100%** với JMeter dashboard khi tôi tính lại độc lập.

**Nhưng phần diễn giải có một lỗi bịa nguyên nhân xuyên suốt toàn bộ báo cáo**, cộng với một tài liệu bị làm giả và hai script của Agent Skill không chạy được. Ba nhóm lỗi P0 dưới đây, nếu không sửa, làm mất điểm ở **Spike (20đ)**, **AI analysis (10đ)**, **Agent Skill (10đ)** và có nguy cơ bị quy vào mục 17 (liêm chính học thuật).

| # | Mức | Vấn đề | Ảnh hưởng |
|:--|:--|:--|:--|
| P0-1 | 🔴 Nghiêm trọng | Nguyên nhân lỗi Spike bị bịa: báo cáo nói "lockout 403", dữ liệu thật là **backend chết** | Task Spike 20đ + toàn bộ Task 2 |
| P0-2 | 🔴 Nghiêm trọng | `git-commit-log.txt` là **log giả**, không có commit thật nào | Mục 12 + rủi ro mục 17 |
| P0-3 | 🔴 Nghiêm trọng | `generate_jmx.py` **crash ngay dòng import** — Agent Skill không chạy được | Task 4 (10đ) |
| P1-4 | 🟠 Cao | `baseline/baseline.json` chứa số **bịa** (browse p95 450ms) trong khi số thật là 31ms | Task 3 + nguyên tắc cấm bịa số |
| P1-5 | 🟠 Cao | Backend **không được restart** giữa Load → Stress (RAM đầu run: 83MB vs 532MB) | Tính hợp lệ số Stress |
| P1-6 | 🟠 Cao | `compare_runs.py` crash `UnicodeEncodeError` trên Windows | Task 3/4 |
| P2-7 | 🟡 Vừa | Không có screenshot / video / GitHub Issue nào | Mục 11 + 14 (thiếu tài liệu bắt buộc ⇒ 0đ hạng mục) |
| P2-8 | 🟡 Vừa | `AI_AUDIT_REPORT.md` thiếu tên tool AI + timestamp + prompt/output thô | Mục AI Audit |
| P2-9 | 🟡 Vừa | Số "p95 24.2ms / 174.4ms / 395.2ms" không tra được về nguồn nào | Truy vết số liệu |
| P3-10 | ⚪ Nhỏ | Sai lệch trích dẫn dòng code (`server.js:283` vs `:293`), tên Thread Group Stress gây hiểu nhầm | Chỉn chu |

---

## 1. P0-1 — Nguyên nhân lỗi Spike Test bị bịa hoàn toàn

### 1.1 Báo cáo đang khẳng định gì

- `23127207_HW05_Report.md:43` — *"❌ **Bão hòa logic Lockout** do bug `login_attempts += 2` tại `server.js:54`"*
- `deliverables/04_execution-report.md:75` — *"Latency của các request thành công trở về mức 4 ms, **chứng minh engine Node.js không bị crash**. Tuy nhiên, các user bị khóa vẫn tiếp tục nhận **HTTP 403** do thời gian khóa kéo dài 180 giây."*
- `deliverables/06_ai-analysis-critique.md:19,29` và `AI_AUDIT_REPORT.md` §3.2 — toàn bộ Task 2 xây trên tiền đề "lỗi 403 trong Spike".

### 1.2 Dữ liệu thật nói gì

Phân bố `responseCode` trong `results/spike/23127207_Spike_20260814.jtl`:

| responseCode | Số mẫu | Ghi chú |
|:--|--:|:--|
| `Non HTTP response code: org.apache.http.conn.HttpHostConnectException` | **7,184** | Connection refused — **không có gì lắng nghe ở cổng 3000** |
| `404` | **5,408** | body **9,782 bytes HTML** "Not Found" — không phải Express API |
| `200` | 251 | |
| `Non HTTP response code: java.net.SocketException` | 20 | |
| **`403`** | **0** | ⚠️ **KHÔNG TỒN TẠI MỘT MẪU 403 NÀO** |

Và `results/spike/resource-spike.csv` — cột `pid`:

```
elapsed_sec=0      pid=2332   private_mb=59.59
elapsed_sec=55.9   pid=-1     private_mb=0.0    <-- tiến trình node BIẾN MẤT
... 151/175 mẫu còn lại đều pid=-1 cho tới hết run
```

Lỗi theo bucket 30s:

```
t=  0s  total= 116   err=    0     <- baseline sạch
t= 30s  total= 225   err=   90
t= 60s  total=5,408  err=5,408     <- BURST 1: 100% lỗi
t= 90s  total= 201   err=  201     <- "giai đoạn hồi phục": vẫn 100% lỗi
t=120s ... t=210s    err=100% suốt
t=240s  total=5,483  err=5,483     <- BURST 2 đánh vào server đã chết
t=270s ... t=330s    err=100%
```

### 1.3 Kết luận đúng

**Backend Node.js đã chết ở giây ~56 của Spike run (đúng lúc burst 1 đổ vào) và không bao giờ sống lại trong 5 phút còn lại.** Không hề có lockout, không hề có 403, và câu "chứng minh engine Node.js không bị crash" là **ngược 180° với bằng chứng của chính mình**. Con số "p95 = 11.8ms" của Spike được tính chủ yếu trên các mẫu *connection-refused fail nhanh*, nên vô nghĩa.

Đáng chú ý: 5,408 mẫu `404` trả về **HTML 9.7KB** — tức là sau khi backend chết, **một tiến trình khác** (nhiều khả năng dev-server của frontend) đã chiếm cổng 3000 và trả lời thay. Nghĩa là gần một nửa số mẫu Spike **không đo SUT**.

### 1.4 Phải sửa như thế nào

> ⚠️ **Không được "sửa cho đẹp".** SUT crash dưới 300 VU là một phát hiện **tốt hơn nhiều** so với câu chuyện lockout bịa ra. Chỉ cần kể đúng.

1. **Chạy lại Spike test** với quy trình sạch:
   - Tắt mọi tiến trình khác đang chiếm cổng 3000 (`Get-NetTCPConnection -LocalPort 3000`) — ghi lại bằng chứng cổng sạch trước khi chạy.
   - Chạy `node backend/server.js` **và redirect stderr ra file**: `node backend/server.js 2> results/spike/backend-stderr.log`. Đây là bằng chứng quyết định về nguyên nhân chết (OOM? uncaught exception? EMFILE?).
   - Giữ `monitor_backend.ps1` chạy suốt — cột `pid` chính là bằng chứng sống/chết.
2. Nếu backend **vẫn chết**: giữ nguyên kết quả, và viết lại mục Spike theo hướng:
   - Ghi rõ mốc thời gian chết (`elapsed_sec` đầu tiên có `pid=-1`).
   - Trích stack trace từ `backend-stderr.log` → đây là root cause thật.
   - Nêu rõ: **không đo được khả năng phục hồi (recovery)** vì SUT không phục hồi — đó chính là kết luận của bài Spike.
   - Mở 1 GitHub Issue: *"SUT crashes and does not recover under 300 VU spike"*.
3. Nếu backend **sống**: lúc đó mới có dữ liệu 403/lockout thật để nói về lockout.
4. **Xóa sạch** mọi câu về "403", "lockout", "engine không bị crash" ở: `23127207_HW05_Report.md:43,68`, `04_execution-report.md:75`, `06_ai-analysis-critique.md:19,29`, `AI_AUDIT_REPORT.md` §3.2 — trừ khi có mẫu 403 thật trong `.jtl` mới.
5. Mọi kết luận về Spike phải kèm **1 dòng lệnh kiểm chứng được** (ví dụ: `cut -d, -f4 <jtl> | sort | uniq -c`).

### 1.5 Điều này đồng thời phá hỏng Task 2

Task 2 hiện đang "vạch trần AI nói sai về nguyên nhân 403" — nhưng **cả AI lẫn phần phản biện đều đang nói về một loại lỗi không tồn tại**. Sau khi chạy lại Spike, phải làm lại chuỗi hội thoại Task 2 với dữ liệu thật. Ba luận điểm phản biện còn lại **vẫn đúng và giữ được**:
- Index trên `products` vô dụng vì `server.js:153` là `SELECT * FROM products` không WHERE ✅
- SQLite không có connection pool ✅
- Memory leak nằm ở `userCarts` (`server.js:14,293`) chứ không phải connection leak ✅

---

## 2. P0-2 — `git-commit-log.txt` là tài liệu giả

`deliverables/git-commit-log.txt` chứa 11 "commit" với author `Dang Dang Khoa <23127207@student.hcmus.edu.vn>`, ngày giờ `Fri Aug 14 07:00:00 2026 +0700`… **nhưng không có commit hash, và không phải output của `git log`.** Nó được viết tay.

Đối chiếu thực tế:

```
$ git status --short
?? performance-testing/23127207_HW05_Report.md
?? performance-testing/data/
?? performance-testing/results/
?? performance-testing/scripts/
?? performance-testing/test-plans/
...          <-- TOÀN BỘ công việc chưa được commit lần nào
```

`git log` trên branch `HW5` chỉ có 2 commit về HW05, cả hai đều là commit tài liệu do phiên trước tạo.

**Đây là rủi ro nặng nhất của cả bài** — mục 12 yêu cầu commit riêng từng bước, và một file log commit dựng sẵn có thể bị đọc là gian lận.

### Cách sửa

1. **Xóa** `deliverables/git-commit-log.txt` ngay.
2. Commit thật, theo từng bước, đúng bảng 11 commit message trong `docs/00_BUILD_SPEC.md` §6. Ví dụ:
   ```powershell
   git add .gitignore performance-testing/scripts/
   git commit -m "chore(perf): setup toolchain and directory structure"
   git add performance-testing/scripts/seed_perf_data.js performance-testing/data/
   git commit -m "feat(perf): add seed script and khoa_users.csv dataset"
   # ... tiếp tục từng bước
   ```
3. Sau khi commit xong mới sinh lại file log **bằng lệnh thật**:
   ```powershell
   git log --oneline --decorate > performance-testing/deliverables/git-commit-log.txt
   ```
4. Không bao giờ tự soạn nội dung cho file này.

---

## 3. P0-3 — Agent Skill không chạy được

```
$ python .agents/skills/performance_testing/scripts/generate_jmx.py --help
  File ".agents/skills/performance_testing/scripts/generate_jmx.py", line 11
    from xml.dom import minidmin
ImportError: cannot import name 'minidmin' from 'xml.dom'
```

Lỗi chính tả `minidmin` → `minidom`, ở **dòng import**, nghĩa là script **chưa từng chạy một lần nào**. Suy ra: 4 file `.jmx` trong `test-plans/` **không phải do script này sinh ra**, nên tuyên bố "tự động sinh `.jmx` từ config JSON, không hard-code" ở `23127207_HW05_Report.md:88` hiện là **không có bằng chứng**. Đây là hạng mục 10 điểm và tiêu chí chấm chính là *"reusable on additional endpoints"*.

### Cách sửa

1. Sửa `minidmin` → `minidom`.
2. **Bắt buộc chạy thật** cả hai config và lưu bằng chứng:
   ```powershell
   python .agents/skills/performance_testing/scripts/generate_jmx.py --config .agents/skills/performance_testing/examples/browse_to_buy_config.json --scenario Load --output performance-testing/test-plans/generated_browse_Load.jmx
   python .agents/skills/performance_testing/scripts/generate_jmx.py --config .agents/skills/performance_testing/examples/coupon_checkout_config.json --scenario Load --output performance-testing/evidence/skill-demo/generated_coupon_Load.jmx
   ```
   File thứ hai (workflow của thành viên khác) chính là **bằng chứng tái sử dụng** — đó là thứ ăn điểm.
3. Mở file sinh ra bằng JMeter GUI, xác nhận không element đỏ, chạy 1 thread × 1 loop.
4. Lưu output console vào `evidence/skill-demo/generate_jmx-console.txt`.
5. Kiểm tra `analyze_jtl.py` bản trong skill có **khác** bản trong `performance-testing/scripts/` (`diff` báo khác nhau) — phải đồng bộ 2 bản hoặc nêu rõ lý do khác.

---

## 4. P1-4 — `baseline/baseline.json` chứa số bịa

```json
"runner": "github-actions-ubuntu-latest",
"02_BrowseProducts": { "p95_ms": 450, "samples": 1200 }
```

Chưa có CI run nào từng chạy (`.github/workflows/perf-regression.yml` mới chỉ có `workflow_dispatch`). Số p95 = **450ms** cho `02_BrowseProducts` trong khi Load run thật đo được **31ms**. Toàn bộ `samples: 1200` cũng là số tròn tự nghĩ. Vi phạm trực tiếp nguyên tắc "cấm bịa số" ở `docs/00_BUILD_SPEC.md` §1.1.

### Cách sửa

Sinh baseline **từ Load run thật**:

```json
{
  "updated_at": "<lấy từ summary.json generated_at>",
  "commit": "<git rev-parse --short HEAD>",
  "runner": "local-windows-<CPU/RAM từ evidence/hardware/spec-table.md>",
  "source_run": "performance-testing/results/load/summary.json",
  "labels": {
    "01_Login":          { "p95_ms": 14, "samples": 1861 },
    "02_BrowseProducts": { "p95_ms": 31, "samples": 1835 },
    "03_ProductDetail":  { "p95_ms": 14, "samples": 1831 },
    "04_AddToCart":      { "p95_ms": 4,  "samples": 1823 },
    "05_Checkout":       { "p95_ms": 38, "samples": 1823 }
  }
}
```

(Số trên tôi đã đối chiếu khớp `results/load/summary.json` và HTML dashboard.) Thêm 1 câu trong `07_continuous-performance-testing.md`: baseline lấy từ máy local nên chỉ dùng để minh hoạ cơ chế; baseline dùng thật trong CI phải sinh trên runner.

---

## 5. P1-5 — Backend không được restart giữa các run

Cột `private_mb` đầu mỗi run trong `resource-*.csv`:

| Run | RAM đầu run | RAM cuối run | Đỉnh |
|:--|--:|--:|--:|
| Load | 83.67 MB | 140.97 MB | 173.31 MB |
| **Stress** | **532.82 MB** | **417.45 MB** | 578.45 MB |
| Spike | 59.59 MB | (chết) | 65.29 MB |
| Endurance | 60.30 MB | 137.39 MB | 172.49 MB |

Stress khởi động từ **532 MB** — tức backend đã tích luỹ rác từ các lần chạy trước và **không được restart**, trong khi Spike/Endurance bắt đầu từ ~60 MB (fresh). Hai hệ quả:

1. Số Stress không so được với các run khác (khác điều kiện ban đầu).
2. RAM trong Stress **giảm** 532 → 417 MB (GC dọn), điều này *mâu thuẫn* với câu chuyện "leak đơn điệu" ở `05_endurance-threshold.md` nếu ai đó đối chiếu chéo.

Ngoài ra `summary.json` của **Load** cũng ghi `memory_leak_mb_per_min: 11.54` — cao gần gấp đôi con số 6.45 của Endurance mà báo cáo dùng. Báo cáo phải giải thích vì sao chọn số của Endurance (đúng: vì Endurance mới là run đủ dài và bắt đầu từ trạng thái sạch).

### Cách sửa

1. Bổ sung vào `05_EXECUTION_RUNBOOK.md` và `run_scenario.ps1`: **bắt buộc restart backend + chờ 30s + xác nhận `private_mb` < 100 MB trước mỗi run**, ghi giá trị đó vào log run.
2. Chạy lại **Stress** từ trạng thái sạch (bắt buộc, vì knee-point 100→200 VU là kết luận trung tâm của bài Stress mà lại đo trên server đã ngập RAM).
3. Thêm mục "Điều kiện ban đầu mỗi run" vào `04_execution-report.md` với bảng RAM đầu run như trên.

---

## 6. P1-6 — `compare_runs.py` crash trên Windows

```
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f389'
  File "compare_runs.py", line 64, in compare_runs
```

Console Windows mặc định cp1252 không in được emoji 🎉.

### Cách sửa
Thêm ngay đầu file:
```python
import sys
sys.stdout.reconfigure(encoding="utf-8")
```
Hoặc bỏ emoji khỏi chuỗi output. Sau đó chạy thật và lưu output vào `evidence/skill-demo/compare_runs-console.txt` — Task 3 cần bằng chứng cơ chế so sánh chạy được.

---

## 7. P2-7 — Thiếu toàn bộ bằng chứng thủ công

`evidence/` hiện chỉ có đúng 1 file: `hardware/spec-table.md`. Grep toàn bộ `deliverables/` + báo cáo: **0 lần** nhắc tới screenshot, video, `.png`, `.mp4`.

Theo mục 11 và 14 của đề, thiếu **tài liệu bắt buộc** ⇒ mất trọn hạng mục. Cần:

| Cần có | Đường dẫn đề xuất | Ghi chú |
|:--|:--|:--|
| Screenshot JMeter đang chạy + Task Manager **cùng khung hình** × 4 run | `evidence/screenshots/<scenario>-run.png` | Bắt buộc cùng khung hình |
| Screenshot HTML dashboard × 4 | `evidence/screenshots/<scenario>-dashboard.png` | |
| Screenshot thủ tục reset lockout (5 bước) | `evidence/screenshots/lockout-reset-*.png` | Đề yêu cầu tường minh |
| Video ≥ 6 phút (3 clip) | link trong `README.md` | Kịch bản lời thoại có sẵn ở `docs/05_EXECUTION_RUNBOOK.md` |
| GitHub Issues cho bug tìm được | link trong `04_execution-report.md` | Draft có sẵn ở `docs/05_EXECUTION_RUNBOOK.md` |

Đồng thời `README.md` hiện **thiếu bảng self-assessment theo barem mục 15** — đây là mục `docs/12_REPORT_OUTLINE.md` §2 đã đặc tả nhưng chưa làm.

---

## 8. P2-8 — `AI_AUDIT_REPORT.md` không đủ tiêu chuẩn audit

Hiện chỉ có bảng % đóng góp AI/người. Thiếu 4 trường bắt buộc theo `docs/12_REPORT_OUTLINE.md`:

- **Tên tool AI cụ thể** (Antigravity? Gemini bản nào? ChatGPT?) — hiện chỉ ghi chung chung "AI"
- **Timestamp** từng tương tác
- **Prompt nguyên văn**
- **Output thô nguyên văn, chưa chỉnh sửa**

Đồng thời `06_ai-analysis-critique.md` §1 đang trình bày cả prompt và "AI trả lời" ở dạng đã được biên tập gọn gàng, không có dấu hiệu là output thô. Nếu phần này **không phải** hội thoại thật với một AI tool thì phải làm lại thật — đây chính là nội dung được chấm của Task 2, và mục 17 xử rất nặng.

`AI_CRITIQUE.md` đạt 278 từ ✅ (yêu cầu 200–300).

---

## 9. P2-9 — Số p95 trong báo cáo không tra được nguồn

Báo cáo ghi Load p95 = **24.2 ms**, Stress = **174.4 ms**, Endurance = **395.2 ms**. Nhưng:
- `summary.json` **không có** trường p95 tổng thể (chỉ có p95 **theo label**).
- HTML dashboard hàng `Total`: Load p95 = **25.0**, Spike p95 = **11.0** (báo cáo ghi 11.8).

Nghĩa là các số này là trung bình có trọng số tự tính ở đâu đó, không tái lập được.

### Cách sửa
Chọn **một** định nghĩa và dùng nhất quán, tôi đề xuất dùng p95 tổng thể của dashboard (đó là số TA sẽ mở ra đối chiếu):

| Run | p95 Total (dashboard, đã verify) |
|:--|--:|
| Load | 25 ms |
| Stress | 169 ms |
| Spike | 11 ms *(vô nghĩa — xem P0-1)* |
| Endurance | 382 ms |

Đồng thời bổ sung trường `overall` (p50/p90/p95/p99) vào output của `analyze_jtl.py` để số trong báo cáo luôn có nguồn máy sinh.

---

## 10. P3-10 — Lỗi nhỏ

- `06_ai-analysis-critique.md:31` ghi `server.js:14,283` — đúng phải là **`:293`** (`userCarts[userId].push(req.body)`).
- Thread Group Stress đặt tên `TG_Stress_Step4_100VU` nhưng đây là bậc **cộng dồn 200 VU** (25+25+50+100). Tên gây hiểu nhầm khi TA mở `.jmx`. Đổi thành `TG_Stress_Step4_+100VU_total200`.
- Load/Endurance `.jmx` không dùng Test Fragment + Module Controller (chỉ Spike có `FRAG_BrowseToBuy`). Không sai, nhưng nên thống nhất.
- `README.md` §1 liệt kê cây thư mục thiếu `docs/` — thư mục 14 file đặc tả.

---

## 11. Những thứ ĐÃ ĐÚNG — không được đụng vào

Ghi lại để agent sau không "sửa" hỏng phần đang tốt:

| Hạng mục | Trạng thái | Bằng chứng |
|:--|:--|:--|
| **Scope nhóm** | ✅ Sạch tuyệt đối | grep `search=`/`apply-coupon`/`my-orders`/`categories` trên toàn bộ `.jmx` + `.js`: **0 kết quả** |
| **5 label đúng workflow** | ✅ | `01_Login → 02_BrowseProducts → 03_ProductDetail → 04_AddToCart → 05_Checkout` trong cả 4 `.jtl` |
| **Độ chính xác `analyze_jtl.py`** | ✅ Khớp 100% | Tôi tính lại độc lập bằng nearest-rank: Load 9,173 mẫu / 0 lỗi / avg 9.91 / p90 18 / p95 25 / p99 104 — **trùng khít** dashboard và `summary.json` cả 4 run |
| **3 loại listener khác nhau** | ✅ | Load+Endurance = `StatVisualizer` (Aggregate), Stress = `SummaryReport`, Spike = `ViewResultsFullVisualizer` |
| **Stress xếp chồng đúng** | ✅ | delay 0/120/240/360, threads 25/25/50/100 ⇒ cộng dồn 25→50→100→200, `max_concurrent_threads: 200` trong `.jtl` |
| **CSV Data Set Config** | ✅ | `quotedData=true`, `recycle=true`, `shareMode.all`, `stopThread=false` — đúng đặc tả `04_JMX_BUILD_SPEC.md` |
| **Assertion kiểm nội dung** | ✅ | có `assert_has_name`, `assert_has_price`, `assert_is_array`, `assert_orderid_exists` — không chỉ check status code |
| **Load / Stress / Endurance là dữ liệu thật, dùng được** | ✅ | 0% lỗi, timestamp liên tục, thread ramp hợp lý |
| **Kết luận memory leak `userCarts`** | ✅ Đúng root cause | Endurance 60.30 → 137.39 MB trong 11.95 phút, `server.js:14,293` |
| **Task 3 CPT** | ✅ Thiết kế tốt | 4 tầng, 3-run median, ngưỡng 10%/20%, chỉ cần thay baseline thật |

---

## 12. Thứ tự thi công đề nghị

1. **Xóa** `git-commit-log.txt` (P0-2) — làm trước tiên, đây là rủi ro liêm chính.
2. Sửa `minidmin` → `minidom` + `sys.stdout.reconfigure` (P0-3, P1-6), chạy thật cả 2 config, lưu console log.
3. Sửa `baseline.json` bằng số thật từ `results/load/summary.json` (P1-4).
4. Restart backend sạch → **chạy lại Stress** → **chạy lại Spike** (có `backend-stderr.log`, có kiểm tra cổng 3000 sạch) (P0-1, P1-5).
5. Chạy lại `analyze_jtl.py` cho 2 run mới, thêm trường `overall` percentile (P2-9).
6. **Viết lại** mục Spike ở `04_execution-report.md` + báo cáo chính theo dữ liệu mới, xoá mọi câu về 403/lockout nếu không có mẫu 403 thật (P0-1).
7. Làm lại chuỗi hội thoại Task 2 với một AI tool có tên cụ thể, dán output thô, ghi timestamp (P0-1 §1.5, P2-8).
8. Chụp screenshot, quay video, mở GitHub Issues (P2-7) — **việc của người, agent không được bịa**.
9. Bổ sung bảng self-assessment vào `README.md` (P2-7).
10. Sửa các lỗi nhỏ P3-10.
11. Commit thật theo từng bước, rồi `git log > git-commit-log.txt`.

---

## 13. Nguyên tắc cho agent sửa bài này

1. **Mọi con số trong báo cáo phải kèm được một lệnh tái lập.** Nếu không tra được về `.jtl` / `summary.json` / dashboard thì xoá số đó đi.
2. **Không suy diễn nguyên nhân.** `responseCode` và cột `pid` trong `resource-*.csv` nói gì thì viết đúng như vậy. "Server chết" là kết quả tốt để báo cáo; "server bị lockout" khi không có mẫu 403 nào là bịa.
3. **Không sửa `backend/`** để số đẹp hơn.
4. **Không tự soạn nội dung cho file vốn phải do công cụ sinh ra** (`git-commit-log.txt`, `baseline.json`, `summary.json`).
5. Trước khi tuyên bố một script "hoạt động", **chạy nó** và lưu output.
