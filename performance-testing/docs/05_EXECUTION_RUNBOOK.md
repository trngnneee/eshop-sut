# 05 — EXECUTION RUNBOOK

> Chạy 4 kịch bản, thu bằng chứng, và chuẩn bị mọi thứ cho `deliverables/04_execution-report.md`.
> Đáp ứng đề §6 Task 1: *"Run as completely as possible, with evidence"* + §11 Anti-AI-Cheat.

---

## 1. `scripts/monitor_backend.ps1`

### 1.1 Vì sao cần

Đề yêu cầu *"a screenshot of the tool together with the backend process's resource usage"*. Screenshot Task Manager là bằng chứng **thị giác**, nhưng để viết được `05_endurance-threshold.md` với **số cụ thể** (trần RAM, tốc độ rò rỉ MB/phút) thì cần dữ liệu **định lượng theo thời gian**. Script này lo phần đó; screenshot lo phần kia. Cả hai đều bắt buộc.

### 1.2 Đặc tả

| Mục | Yêu cầu |
| :--- | :--- |
| Tham số | `-Scenario <string>` (bắt buộc), `-IntervalSec <int>` (mặc định `2`), `-OutFile <path>` (mặc định `results/<scenario>/resource-<scenario>.csv`) |
| Đối tượng | Tiến trình `node` đang chạy `server.js`. Tìm bằng `Get-CimInstance Win32_Process -Filter "Name='node.exe'"` rồi lọc `CommandLine -like '*server.js*'` |
| Chu kỳ | Mỗi `IntervalSec` giây ghi một dòng, tới khi bị dừng (`Ctrl+C` hoặc `Stop-Process` từ `run_scenario.ps1`) |
| Cột CSV | `timestamp,elapsed_sec,pid,cpu_percent,working_set_mb,private_mb,handles,threads` |
| `cpu_percent` | Tính **delta** `TotalProcessorTime` giữa 2 lần lấy mẫu, chia cho `IntervalSec × NumberOfLogicalProcessors × 1s`, nhân 100 |
| `working_set_mb` | `[math]::Round($p.WorkingSet64 / 1MB, 2)` |
| `private_mb` | `[math]::Round($p.PrivateMemorySize64 / 1MB, 2)` — **đây mới là con số dùng cho "memory ceiling"**, vì WorkingSet chịu ảnh hưởng của áp lực bộ nhớ toàn hệ thống |

> ⚠️ **Đừng dùng `$p.CPU`.** Thuộc tính đó là **tổng tích lũy** giây CPU từ lúc process khởi động, không phải phần trăm tức thời. Lấy nó rồi gọi là "CPU%" là một cách hiểu sai metric rất phổ biến — và cũng chính là loại lỗi mà Task 2 đi săn.

### 1.3 Verify

```powershell
# chạy thử 10 giây rồi Ctrl+C
.\performance-testing\scripts\monitor_backend.ps1 -Scenario smoke -IntervalSec 2
Get-Content "performance-testing\results\smoke\resource-smoke.csv" | Select-Object -First 5
```
Kỳ vọng: có header + ~5 dòng, `working_set_mb` là số dương hợp lý (vài chục tới vài trăm MB).

---

## 2. `scripts/run_scenario.ps1`

### 2.1 Đặc tả

```powershell
.\performance-testing\scripts\run_scenario.ps1 -Scenario Load
```

| Tham số | Giá trị hợp lệ |
| :--- | :--- |
| `-Scenario` | `Load` \| `Stress` \| `Spike` \| `Endurance` |
| `-RunDate` | `YYYYMMDD`, mặc định `Get-Date -Format yyyyMMdd` |
| `-SkipReset` | switch — bỏ qua reset lockout (chỉ dùng khi cố ý nối tiếp run) |

### 2.2 Trình tự bắt buộc

| # | Bước | Ghi chú |
| :---: | :--- | :--- |
| 1 | Kiểm tra backend sống: `Invoke-RestMethod http://localhost:3000/api/products` | Fail → dừng, không chạy tiếp |
| 2 | **Reset lockout**: `node scripts\reset_lockout.js`, **lưu timestamp** vào biến | Trừ khi `-SkipReset` |
| 3 | Tạo `results/<scenario>/` nếu chưa có | |
| 4 | Khởi động `monitor_backend.ps1` dạng background job, giữ lại object job | |
| 5 | Chạy JMeter **non-GUI** (lệnh đầy đủ §2.3) | |
| 6 | Dừng monitor: `Stop-Job` + `Remove-Job` | Luôn chạy, kể cả khi JMeter lỗi (`try/finally`) |
| 7 | Sinh HTML dashboard: `jmeter -g <jtl> -o <outdir>` | |
| 8 | Chạy `analyze_jtl.py` sinh `summary.json` + `summary.md` | |
| 9 | In tóm tắt ra console: thời gian bắt đầu/kết thúc, timestamp reset, đường dẫn artifact | Dán vào `04_execution-report.md` |

### 2.3 Lệnh JMeter non-GUI đầy đủ

```powershell
$root  = "C:\My Workspace\HCMUS\Test\Week 3\Hw2"
$pt    = "$root\performance-testing"
$scen  = "Load"
$date  = "20260812"
$name  = "23127207_${scen}_${date}"
$outdir = "$pt\results\$($scen.ToLower())"

& "$root\.tools\jmeter\bin\jmeter.bat" `
    -n `
    -t "$pt\test-plans\$name.jmx" `
    -l "$outdir\$name.jtl" `
    -j "$outdir\$name.jmeter.log" `
    -q "$pt\scripts\jmeter-user.properties" `
    -Jcsvdir="$pt\data" `
    -e -o "$outdir\html-report"
```

| Cờ | Ý nghĩa |
| :--- | :--- |
| `-n` | Non-GUI. **Bắt buộc** — chạy GUI ở 300 VU thì chính JMeter thành nút cổ chai |
| `-t` | File `.jmx` |
| `-l` | File `.jtl` raw — đây là thứ đề §11 yêu cầu nộp **đầy đủ** |
| `-j` | Log của JMeter (khác `.jtl`), giữ lại để truy lỗi |
| `-q` | Nạp `jmeter-user.properties` (cấu hình cột `.jtl`, xem `04_JMX_BUILD_SPEC.md` §7) |
| `-Jcsvdir` | Truyền thư mục CSV vào biến `${__P(csvdir)}` |
| `-e -o` | Sinh HTML dashboard ngay sau khi chạy |

> `-e -o` yêu cầu thư mục đích **rỗng hoặc chưa tồn tại**. Chạy lại lần 2 sẽ báo lỗi — xóa `html-report` trước, hoặc để script tự xóa.

### 2.4 Sinh HTML report từ `.jtl` đã có (khi cần làm lại)

```powershell
Remove-Item -Recurse -Force "$outdir\html-report" -ErrorAction SilentlyContinue
& "$root\.tools\jmeter\bin\jmeter.bat" -g "$outdir\$name.jtl" -o "$outdir\html-report"
```

---

## 3. Thứ tự chạy 4 kịch bản

| # | Kịch bản | Thời lượng | Nghỉ giữa các run | Vì sao nghỉ |
| :---: | :--- | :---: | :---: | :--- |
| 1 | **Load** | 5 phút | 3 phút | Chờ lockout tự hết hạn (180 s) + để CPU về nền |
| 2 | **Stress** | 8 phút | 3 phút | |
| 3 | **Spike** | 6 phút | 3 phút | |
| 4 | **Endurance** | 12 phút | — | Chạy cuối, vì làm phình `orders` nhiều nhất |

Tổng thời gian chạy ≈ **40 phút** kể cả nghỉ.

### 3.1 Có nên restart backend giữa các run không?

**Có — và phải ghi rõ.** `userCarts` là biến in-memory không bao giờ được giải phóng (`server.js:14,293`), nên nếu không restart, RSS của run sau sẽ mang theo rác của run trước và mọi so sánh bộ nhớ giữa các kịch bản trở nên vô nghĩa.

Quy ước: **restart backend trước mỗi kịch bản**, và ghi thời điểm restart vào `04_execution-report.md`.

**Ngoại lệ — Endurance:** kịch bản này *cần* quan sát tích lũy, nên khởi động backend sạch rồi chạy thẳng 12 phút, không can thiệp giữa chừng.

### 3.2 Có nên reset DB giữa các run không?

**Không**, trừ khi `orders` phình tới mức làm chậm rõ rệt. Lý do: workflow không đọc bảng `orders` (bước `my-orders` thuộc Bảo), nên số lượng đơn hàng gần như không ảnh hưởng đến 5 request đang đo. Nếu vẫn quyết định reset, phải **seed lại perf data** (`02_DATA_SPEC.md` §5) và ghi vào report.

---

## 4. Thủ tục reset lockout giữa các run — đề yêu cầu tường minh

> Đề §6: *"When Stress/Spike runs trigger the 3-fail login lockout, reset it between runs and document the steps."*

Chép nguyên các bước sau vào `deliverables/04_execution-report.md`, kèm ảnh chụp ở bước 2 và 4.

**Bước 1 — Phát hiện lockout.** Sau khi run kết thúc, đếm số `403` trong `.jtl`:
```powershell
$jtl = "performance-testing\results\stress\23127207_Stress_20260812.jtl"
Import-Csv $jtl | Where-Object { $_.label -eq '01_Login' } |
  Group-Object responseCode | Select-Object Name, Count
```
Có dòng `Name=403` → đã dính lockout.

**Bước 2 — Xác nhận nguyên nhân.** Xem một mẫu lỗi:
```powershell
Import-Csv $jtl | Where-Object { $_.responseCode -eq '403' } |
  Select-Object -First 3 timeStamp, label, responseMessage, failureMessage
```
📷 *Chụp màn hình bước này → `evidence/stress/lockout-detect.png`*

**Bước 3 — Reset.**
```powershell
node "performance-testing\scripts\reset_lockout.js"
```
Ghi lại timestamp script in ra.

**Bước 4 — Xác minh đã sạch.**
```powershell
node -e "const s=require('./backend/node_modules/sqlite3');const d=new s.Database('./backend/database.sqlite');d.get('SELECT COUNT(*) c FROM users WHERE locked_until IS NOT NULL',(e,r)=>console.log('locked users:',r.c));"
```
Phải in `locked users: 0`.
📷 *Chụp màn hình bước 3+4 → `evidence/stress/lockout-reset.png`*

**Bước 5 — Ghi vào report** theo bảng:

| Run | Thời điểm kết thúc | Số `403` ở `01_Login` | Thời điểm reset | Xác minh |
| :--- | :--- | :---: | :--- | :--- |
| Stress | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` | locked users = 0 |
| Spike | `<<FILL>>` | `<<FILL>>` | `<<FILL>>` | locked users = 0 |

---

## 5. Checklist bằng chứng cho MỖI run

| # | Bằng chứng | Đường dẫn | Ai làm |
| :---: | :--- | :--- | :--- |
| 1 | File `.jtl` raw đầy đủ | `results/<scen>/23127207_<Scen>_<date>.jtl` | script |
| 2 | Log JMeter | `results/<scen>/*.jmeter.log` | script |
| 3 | HTML dashboard | `results/<scen>/html-report/index.html` | script |
| 4 | CSV tài nguyên | `results/<scen>/resource-<scen>.csv` | script |
| 5 | `summary.json` + `summary.md` | `results/<scen>/` | script |
| 6 | 📷 **Ảnh JMeter + Task Manager cùng khung hình**, chụp **trong lúc** run đang chạy | `evidence/<scen>/jmeter+taskmgr-<scen>.png` | **NGƯỜI** |
| 7 | 📷 Ảnh listener (Aggregate/Summary/VRT) đã nạp `.jtl` | `evidence/<scen>/listener-<scen>.png` | **NGƯỜI** |
| 8 | 📷 Ảnh `dxdiag` (một lần cho cả bài) | `evidence/hardware/dxdiag.png` | **NGƯỜI** |
| 9 | Bảng spec phần cứng | `evidence/hardware/spec-table.md` | `01_ENVIRONMENT_SETUP.md` §8 |

### 5.1 Sanity check sau mỗi run

```powershell
$scen = "load"; $name = "23127207_Load_20260812"
$d = "performance-testing\results\$scen"

"jtl lines      : " + (Get-Content "$d\$name.jtl" | Measure-Object -Line).Lines
"html report    : " + (Test-Path "$d\html-report\index.html")
"resource rows  : " + (Get-Content "$d\resource-$scen.csv" | Measure-Object -Line).Lines
"error samples  : " + (Import-Csv "$d\$name.jtl" | Where-Object { $_.success -eq 'false' }).Count
```

| Kiểm tra | Ngưỡng chấp nhận |
| :--- | :--- |
| `jtl lines` | > 1000 với Load 5 phút. Nếu chỉ vài chục dòng → test chết sớm, điều tra `.jmeter.log` |
| `html report` | `True` |
| `resource rows` | ≈ thời lượng ÷ 2. Load 300 s → ~150 dòng |
| `error samples` | Với Load nên ≈ 0. Khác 0 thì **phải giải thích trong report**, không lờ đi |

---

## 6. Probe lockout — chạy RIÊNG, ngoài test hiệu năng

Mục đích: lấy bằng chứng cho bug FR-02 mà **không** đầu độc pool account của test hiệu năng. Chạy sau khi đã xong cả 4 kịch bản.

```powershell
$base = "http://localhost:3000"
$probe = "khoa400@eshop.com"   # dùng account cuối pool, sẽ reset ngay sau đó

function Try-Login($email, $pwd) {
  try {
    $r = Invoke-WebRequest -Uri "$base/api/login" -Method Post `
         -ContentType "application/json" `
         -Body (@{email=$email; password=$pwd} | ConvertTo-Json) -SkipHttpErrorCheck
    [pscustomobject]@{ Time=(Get-Date -Format "HH:mm:ss"); Status=$r.StatusCode; Body=$r.Content }
  } catch { [pscustomobject]@{ Time=(Get-Date -Format "HH:mm:ss"); Status='ERR'; Body=$_.Exception.Message } }
}

# Lần sai #1  -> spec FR-02 kỳ vọng login_attempts = 1, chưa khóa
Try-Login $probe "WrongPass1!"
# Lần sai #2  -> spec kỳ vọng = 2, chưa khóa. Thực tế: 2+2 = 4 >= 3 -> ĐÃ KHÓA
Try-Login $probe "WrongPass2!"
# Lần đúng    -> nếu trả 403 thì đã bị khóa sau ĐÚNG 2 lần sai, sai spec
Try-Login $probe "Test1234!"
```

**Kỳ vọng theo spec FR-02** (`README.md`): sau 2 lần sai, login đúng vẫn phải **thành công** (200).
**Kết quả thực tế dự đoán** (`server.js:54,57`): lần 3 trả **403** `"Tài khoản đã bị khóa"` → khóa sau **2** lần sai, và kéo dài **180 s** thay vì 30 s.

Đo thời gian khóa:
```powershell
$t0 = Get-Date
do { Start-Sleep -Seconds 10; $r = Try-Login $probe "Test1234!" ; $r }
while ($r.Status -ne 200)
"Lockout duration: $([int]((Get-Date) - $t0).TotalSeconds) giây"
```

📷 Chụp toàn bộ output → `evidence/issues/fr02-lockout-probe.png`

Sau khi probe xong: `node performance-testing\scripts\reset_lockout.js`

---

## 7. Kịch bản video demo (≥ 6 phút, tiếng Việt) — NGƯỜI thực hiện

> Đề §6 + §11: video **unlisted YouTube**, **≥ 6 phút tổng**, hiện **tool và resource monitor trong cùng một khung hình**, **giọng nói của chính sinh viên**, tiếng Việt.

### 7.1 Chuẩn bị khung hình

Chia màn hình: **trái** = cửa sổ terminal đang chạy JMeter non-GUI (hoặc JMeter GUI hiển thị listener), **phải** = Task Manager tab *Performance* + tab *Details* đã lọc `node.exe`. Cả hai phải thấy được trong **một** khung hình, không được cắt cảnh qua lại.

### 7.2 Clip 1 — Load (~2 phút 30)

| Thời điểm | Nội dung nói |
| :--- | :--- |
| 0:00–0:20 | "Chào thầy cô, em là <họ tên>, MSSV 23127207. Đây là bài HW05 Performance Testing trên hệ thống EShop. Workflow em nhận là **Browse-to-buy**, gồm 5 bước: đăng nhập, xem toàn bộ danh sách sản phẩm, xem chi tiết một sản phẩm, thêm vào giỏ, và thanh toán." |
| 0:20–0:45 | Mở `23127207_Load_20260812.jmx` trong GUI, rê chuột qua từng sampler: "Em dùng đúng 5 request, phủ 3 nhóm endpoint: auth-heavy là login, read-heavy là hai request products, transactional là cart và checkout. Em **không** dùng search vì bạn Trâm trong nhóm đã nhận endpoint đó." |
| 0:45–1:05 | Mở CSV Data Set Config: "Dữ liệu lấy từ file CSV 400 tài khoản. Em để **Sharing mode All threads** để mỗi thread nhận một dòng khác nhau, tránh việc hàng trăm thread cùng đăng nhập một tài khoản rồi bị khóa dây chuyền." |
| 1:05–1:20 | Chỉ vào Thread Group: "50 luồng, ramp-up 60 giây, chạy 5 phút." Chỉ vào Uniform Random Timer: "Think time 2 đến 4 giây ở bước duyệt danh sách, vì người dùng thật cần thời gian cuộn trang." |
| 1:20–1:35 | Chạy `run_scenario.ps1 -Scenario Load`, chỉ vào dòng reset lockout: "Trước mỗi run em reset trạng thái khóa tài khoản." |
| 1:35–2:20 | **Giữ khung hình có cả terminal và Task Manager.** "Đây là tiến trình node của backend. CPU đang ở khoảng <đọc số thật>, RAM <đọc số thật>." Đọc số liệu **thật đang hiện trên màn hình**. |
| 2:20–2:30 | Mở `html-report/index.html`, chỉ vào biểu đồ response time. |

### 7.3 Clip 2 — Stress (~2 phút)

| Thời điểm | Nội dung nói |
| :--- | :--- |
| 0:00–0:30 | Giải thích 4 Thread Group bậc thang: "25, rồi 50, rồi 100, rồi 200 luồng đồng thời. Em dùng 4 Thread Group xếp chồng bằng startup delay thay vì plugin, để file `.jmx` mở được trên máy khác mà không cần cài thêm gì." |
| 0:30–1:30 | Chạy, **giữ Task Manager trong khung**, mô tả CPU tăng theo từng bậc, đọc số thật. |
| 1:30–2:00 | Mở Summary Report đã nạp `.jtl`, đọc error% và p95 thật. Nếu có `SQLITE_BUSY` thì chỉ ra và nói: "Đây là lỗi thật của SUT khi nhiều luồng cùng ghi vào SQLite, em ghi nhận thành issue chứ không sửa backend." |

### 7.4 Clip 3 — Spike + Endurance (~2 phút)

| Thời điểm | Nội dung nói |
| :--- | :--- |
| 0:00–0:40 | Giải thích mô hình spike: baseline 10 luồng chạy suốt, 2 đợt sốc 300 luồng ramp-up 5 giây. "Em giữ baseline để đo được **thời gian phục hồi** sau cú sốc." |
| 0:40–1:20 | Chạy Spike, chỉ vào Task Manager lúc CPU dựng đứng, rồi lúc hạ xuống. |
| 1:20–2:00 | Chuyển sang Endurance: mở `resource-endurance.csv` hoặc biểu đồ RAM theo thời gian: "RAM của tiến trình node tăng đơn điệu từ <số> lên <số> MB sau 12 phút và **không giảm sau checkout**, vì giỏ hàng lưu in-memory và không bao giờ được xóa. Đây là memory leak thật của SUT." |

### 7.5 Quy tắc bắt buộc

- ❌ **Không** đọc số liệu không có trên màn hình.
- ❌ **Không** cắt cảnh để giấu lúc test fail — nếu fail, nói ra và giải thích.
- ✅ Nói **tiếng Việt**, giọng của chính mình, không dùng TTS.
- ✅ Tổng 3 clip **≥ 6 phút**.
- ✅ Upload **unlisted**, dán link vào `performance-testing/README.md`.

---

## 8. Bug report lên GitHub Issues — NGƯỜI thực hiện

> Đề §6: *"Log any genuine bugs or performance issues on your GitHub Issues page with screenshots."*

Repo: `https://github.com/trngnneee/eshop-sut/issues`. Dùng template `.github/ISSUE_TEMPLATE/bug_report.md`.

### Issue #1 — FR-02: bộ đếm login sai tăng 2 đơn vị và khóa 180 giây

| Mục | Nội dung |
| :--- | :--- |
| Title | `[FR-02] Login attempt counter increments by 2 and lockout lasts 180s instead of 30s` |
| Steps | Chạy probe ở §6 |
| Expected | Spec FR-02: mỗi lần sai `+1`; khóa khi `>= 3`; thời hạn **30 giây** |
| Actual | `server.js:54` `login_attempts + 2` → khóa sau **2** lần sai; `server.js:57` `Date.now() + 180000` → **180 giây** |
| Impact | Người dùng bị khóa sớm hơn mong đợi 33%; thời gian khóa gấp 6 lần spec. Trong test hiệu năng, một lỗi nhỏ có thể vô hiệu hóa cả pool tài khoản |
| Evidence | `evidence/issues/fr02-lockout-probe.png` |

### Issue #2 — FR-06: `GET /api/products/:id` trả 200 cho id không tồn tại

| Mục | Nội dung |
| :--- | :--- |
| Title | `[FR-06] GET /api/products/:id returns 200 with empty body for non-existent id` |
| Expected | `404 Not Found` |
| Actual | `server.js:161` `return res.status(200).json({})` |
| Impact | Client không phân biệt được "không có sản phẩm" với "sản phẩm rỗng"; test tự động dựa trên status code sẽ báo xanh sai |

### Issue #3 — FR-06: `price` trả về kiểu string khi `id` chẵn

| Mục | Nội dung |
| :--- | :--- |
| Title | `[FR-06] Product price returned as string for even product ids` |
| Actual | `server.js:162` `if (row.id % 2 === 0) row.price = row.price.toString()` |
| Impact | Client tính tổng tiền bằng phép cộng sẽ nối chuỗi thay vì cộng số |

### Issue #4 — Hiệu năng: giỏ hàng in-memory không bao giờ được giải phóng

| Mục | Nội dung |
| :--- | :--- |
| Title | `[PERF] In-memory cart (userCarts) grows unbounded — memory leak under sustained load` |
| Evidence | `results/endurance/resource-endurance.csv` + biểu đồ RSS |
| Actual | `server.js:14` khai báo `userCarts`; `:293` chỉ `push`; `:297-309` checkout **không** xóa giỏ |
| Số liệu | `<<FILL: RSS đầu run → RSS cuối run, MB/phút>>` |

### Issue #5 (nếu quan sát được) — `SQLITE_BUSY` ở tải cao

| Mục | Nội dung |
| :--- | :--- |
| Title | `[PERF] Checkout returns 500 SQLITE_BUSY at high concurrency` |
| Evidence | Trích dòng `.jtl` có `responseCode=500` và `failureMessage` chứa `SQLITE_BUSY` |
| Số liệu | `<<FILL: số lượng, xuất hiện từ bậc VU nào>>` |

📷 Sau khi tạo, chụp trang Issues → `evidence/issues/github-issues-list.png`

---

## 9. Khung `deliverables/04_execution-report.md`

```markdown
# Báo cáo Thực thi (Execution Report)

## 1. Môi trường
| Mục | Giá trị |
| Hostname | <<FILL>> |
| CPU / RAM / OS | <<FILL — lấy từ evidence/hardware/spec-table.md>> |
| JMeter | 5.6.3 (non-GUI) |
| Node.js | <<FILL>> |
| Dữ liệu | 400 user (khoa001–khoa400), 505 product (5 gốc + 500 PERF) |

## 2. Nhật ký chạy
| # | Kịch bản | Bắt đầu | Kết thúc | Thời lượng | Reset lockout lúc | Restart backend | Ghi chú |
|---|---|---|---|---|---|---|---|
| 1 | Load | <<FILL>> | <<FILL>> | 5' | <<FILL>> | có | |
| 2 | Stress | <<FILL>> | <<FILL>> | 8' | <<FILL>> | có | |
| 3 | Spike | <<FILL>> | <<FILL>> | 6' | <<FILL>> | có | |
| 4 | Endurance | <<FILL>> | <<FILL>> | 12' | <<FILL>> | có | không can thiệp giữa chừng |

## 3. Thủ tục reset lockout   (chép nguyên §4 của doc này + ảnh)

## 4. Kết quả tóm tắt mỗi run   (bảng từ results/<scen>/summary.md)

## 5. Sự cố gặp phải và cách xử lý
| Sự cố | Kịch bản | Nguyên nhân | Xử lý | Ảnh hưởng tới số liệu |

## 6. Bằng chứng đính kèm   (bảng §5 của doc này, tick đủ)

## 7. Giới hạn phương pháp   (chép từ 03_TEST_DESIGN.md §7)
```

---

## 10. Checklist

- [ ] `monitor_backend.ps1` chạy được, CSV có dữ liệu hợp lý, **không** dùng `$p.CPU` làm phần trăm
- [ ] `run_scenario.ps1` chạy một lệnh ra đủ 5 artifact
- [ ] Chạy đủ **4** kịch bản, mỗi kịch bản restart backend trước
- [ ] Sanity check §5.1 pass cho cả 4 run
- [ ] Thủ tục reset lockout §4 đã thực hiện và **chụp ảnh** ở bước 2, 3, 4
- [ ] Probe lockout §6 đã chạy, có ảnh
- [ ] 📷 Ảnh JMeter + Task Manager **cùng khung hình** cho cả 4 run
- [ ] 📷 Ảnh `dxdiag`, hostname khớp HW trước
- [ ] Video 3 clip, tổng ≥ 6 phút, tiếng Việt, upload unlisted
- [ ] Tạo ≥ 4 GitHub Issues, có ảnh
- [ ] `deliverables/04_execution-report.md` điền hết `<<FILL>>`
- [ ] Commit: `test(perf): execute all scenarios with raw jtl, html reports and resource logs`
