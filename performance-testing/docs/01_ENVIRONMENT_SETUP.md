# 01 — ENVIRONMENT SETUP

> Mọi lệnh trong file này là **PowerShell trên Windows**, chạy từ **thư mục gốc repo**:
> `C:\My Workspace\HCMUS\Test\Week 3\Hw2`
>
> Trạng thái đã khảo sát: Java ✅ (`Eclipse Adoptium JDK 25`), Python ✅ (`C:\Python314\python.exe`), JMeter ❌, k6 ❌.

---

## 1. Xác nhận điều kiện tiên quyết

```powershell
java -version          # cần >= 8; máy này có JDK 25
node -v                # cần >= 18
python --version       # cần >= 3.8
git rev-parse --abbrev-ref HEAD    # phải in ra: HW5
```

Nếu không ở branch `HW5`:
```powershell
git checkout HW5
```

---

## 2. Cài Apache JMeter 5.6.3

JMeter là **công cụ chính** (đề §8: *"JMeter (default) or k6 (bonus)"*). Cài vào `.tools/` trong repo để mọi đường dẫn trong script là tương đối.

```powershell
$root = "C:\My Workspace\HCMUS\Test\Week 3\Hw2"
New-Item -ItemType Directory -Force "$root\.tools" | Out-Null

$url = "https://dlcdn.apache.org/jmeter/binaries/apache-jmeter-5.6.3.zip"
$zip = "$root\.tools\apache-jmeter-5.6.3.zip"

Invoke-WebRequest -Uri $url -OutFile $zip
Expand-Archive -Path $zip -DestinationPath "$root\.tools" -Force
Rename-Item "$root\.tools\apache-jmeter-5.6.3" "$root\.tools\jmeter"
Remove-Item $zip
```

> Nếu `dlcdn.apache.org` trả 404 (bản mới hơn đã thay thế), dùng mirror lưu trữ vĩnh viễn:
> `https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.6.3.zip`

**Verify — bắt buộc, không bỏ qua:**
```powershell
& "$root\.tools\jmeter\bin\jmeter.bat" -v
```
Phải in ra banner có dòng `5.6.3`.

> JDK 25 mới hơn nhiều so với bản JMeter build cho JDK 8, nên khi khởi động có thể in cảnh báo kiểu
> `WARNING: A restricted method in java.lang.System has been called`.
> Đây là **cảnh báo, không phải lỗi** — JMeter vẫn chạy. Nếu gặp lỗi thật sự chặn khởi động, cài thêm JDK 17 LTS và trỏ `JAVA_HOME` sang nó chỉ cho phiên chạy JMeter.

---

## 3. Cài k6 (bonus — không chặn deliverable chính)

```powershell
winget install --id Grafana.k6 -e --accept-source-agreements --accept-package-agreements
k6 version
```

Nếu `winget` không dùng được: tải `k6-vX.Y.Z-windows-amd64.zip` từ `https://github.com/grafana/k6/releases`, giải nén vào `.tools\k6\`, rồi gọi bằng đường dẫn đầy đủ.

> **Nếu k6 không cài được: bỏ qua và đi tiếp.** k6 chỉ là phần bonus; bộ deliverable chấm điểm là JMeter. Ghi lại việc bỏ qua trong `deliverables/04_execution-report.md`.

---

## 4. Loại binary khỏi Git

`.tools/` chứa hàng nghìn file binary, **không được commit**.

Mở `.gitignore` ở gốc repo, thêm (nếu chưa có):

```gitignore
# Performance testing toolchain (binaries, do not commit)
.tools/

# JMeter local artifacts
*.jmeter.log
jmeter.log
```

**Verify:**
```powershell
git check-ignore -v .tools\jmeter\bin\jmeter.bat
```
Phải in ra dòng khớp rule `.tools/`.

> Lưu ý: repo đã có sẵn `.tools/models/` (whisper model từ bài trước). Rule `.tools/` phủ luôn cả thư mục đó — đúng ý, vì đó cũng là binary.
>
> Ngược lại, `performance-testing/results/` **PHẢI được commit** (đề §14 yêu cầu nộp raw `.jtl` + HTML report). Đừng vô tình ignore nhầm.

---

## 5. Khởi động SUT

### 5.1 Cài dependency backend (chỉ lần đầu)

```powershell
cd "C:\My Workspace\HCMUS\Test\Week 3\Hw2\backend"
npm install
```

### 5.2 Reset database về trạng thái sạch

```powershell
node "C:\My Workspace\HCMUS\Test\Week 3\Hw2\backend\database.js"
```
Phải in: `Database initialized and seeded (Phase 2).`

> Lệnh này **DROP toàn bộ bảng** rồi seed lại (`backend/database.js:15-20`). Chạy trước mỗi đợt test lớn để số liệu có baseline sạch — nhưng **chạy trước bước seed perf data**, không phải sau, nếu không sẽ xóa mất 400 user vừa tạo.

### 5.3 Chạy server

```powershell
node "C:\My Workspace\HCMUS\Test\Week 3\Hw2\backend\server.js"
```
Phải in: `Server is running on http://localhost:3000`

**Để terminal này chạy suốt quá trình test.** Mở terminal mới cho các lệnh còn lại.

Chạy nền (tiện cho script tự động):
```powershell
$sut = Start-Process -FilePath "node" `
  -ArgumentList "`"C:\My Workspace\HCMUS\Test\Week 3\Hw2\backend\server.js`"" `
  -PassThru -WindowStyle Minimized
$sut.Id    # ghi lại PID để monitor_backend.ps1 bám vào
```

---

## 6. Smoke test — đúng 5 endpoint trong scope

Chạy **trước khi** đụng tới `.jmx`. Nếu bước nào fail, dừng lại xử lý ngay; đừng đi tiếp.

```powershell
$base = "http://localhost:3000"

# [1/5] auth-heavy — login (dùng account seed gốc để smoke, chưa cần perf pool)
$login = Invoke-RestMethod -Uri "$base/api/login" -Method Post `
  -ContentType "application/json" `
  -Body '{"email":"test@eshop.com","password":"Test1234!"}'
$token = $login.token
"[1/5] login  -> token length = $($token.Length)"

# [2/5] read-heavy — FULL LIST, KHÔNG có ?search=
$products = Invoke-RestMethod -Uri "$base/api/products" -Method Get
"[2/5] products -> count = $($products.Count)"

# [3/5] read-heavy — product detail
$pid0 = $products[0].id
$detail = Invoke-RestMethod -Uri "$base/api/products/$pid0" -Method Get
"[3/5] detail -> id=$($detail.id) name=$($detail.name) price=$($detail.price)"

# [4/5] transactional — add to cart
$hdr = @{ Authorization = "Bearer $token" }
$cart = Invoke-RestMethod -Uri "$base/api/cart" -Method Post -Headers $hdr `
  -ContentType "application/json" `
  -Body (@{ product_id=$pid0; quantity=1; name=$detail.name; price=100000 } | ConvertTo-Json)
"[4/5] cart -> $($cart.message)"

# [5/5] transactional — checkout
$order = Invoke-RestMethod -Uri "$base/api/checkout" -Method Post -Headers $hdr `
  -ContentType "application/json" `
  -Body '{"total_amount":100000,"shipping_address":"1 Ly Thuong Kiet, Q10"}'
"[5/5] checkout -> orderId = $($order.orderId)"
```

**Kỳ vọng:** cả 5 dòng in ra không lỗi, `token` có độ dài > 0, `orderId` là số.

> Chạy smoke test xong nhớ **reset DB** trước khi chạy test thật, để order rác không lẫn vào số liệu:
> `node backend\database.js` rồi seed lại perf data theo `02_DATA_SPEC.md`.

---

## 7. Bảng xử lý sự cố

| Triệu chứng | Nguyên nhân | Cách xử lý |
| :--- | :--- | :--- |
| `Error: listen EADDRINUSE :::3000` | Đã có process chiếm cổng 3000 | `Get-NetTCPConnection -LocalPort 3000 \| Select-Object OwningProcess` rồi `Stop-Process -Id <pid>` |
| `jmeter.bat` báo `JAVA_HOME not set` | Java có trong PATH nhưng thiếu biến môi trường | `$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-25.0.2.10-hotspot"` |
| JMeter khởi động rồi thoát ngay | Không đủ heap | Sửa `.tools\jmeter\bin\jmeter.bat`: `set HEAP=-Xms1g -Xmx4g` |
| `Cannot find module 'sqlite3'` | Chưa `npm install` trong `backend/` | `cd backend; npm install` |
| `SQLITE_BUSY: database is locked` | Nhiều thread ghi đồng thời vào SQLite | **Không phải lỗi cấu hình — đây là kết quả test thật.** Ghi nhận thành finding (xem `00_BUILD_SPEC.md` §1.3) |
| Login trả `403` `"Tài khoản đã bị khóa"` | Account dính lockout từ run trước | `node performance-testing\scripts\reset_lockout.js` (xem `02_DATA_SPEC.md` §4) |
| `Invoke-WebRequest` tải JMeter rất chậm / timeout | Mirror xa | Đổi sang `archive.apache.org` hoặc tải tay bằng trình duyệt rồi `Expand-Archive` |
| HTML report rỗng, JMeter báo `results file is empty` | Chạy `-g` trỏ sai file `.jtl` | Kiểm tra `.jtl` có > 1 dòng (dòng đầu là header CSV) |
| `Expand-Archive` báo path quá dài | Windows MAX_PATH | Bật long path: `git config --system core.longpaths true`, hoặc giải nén vào `C:\jmeter` |

---

## 8. Ghi nhận thông số phần cứng (cho đề §6 và §11)

Đề yêu cầu **hardware report** với hostname khớp các bài trước.

```powershell
# Ảnh chụp dxdiag — NGƯỜI tự chụp, đây chỉ là lệnh mở
dxdiag

# Bảng spec dạng text, đưa vào evidence/hardware/spec-table.md
$sys = Get-CimInstance Win32_ComputerSystem
$cpu = Get-CimInstance Win32_Processor
$os  = Get-CimInstance Win32_OperatingSystem
$dsk = Get-CimInstance Win32_DiskDrive | Select-Object -First 1

[pscustomobject]@{
  Hostname      = $env:COMPUTERNAME
  OS            = "$($os.Caption) $($os.Version)"
  CPU           = $cpu.Name
  Cores_Threads = "$($cpu.NumberOfCores) cores / $($cpu.NumberOfLogicalProcessors) threads"
  RAM_GB        = [math]::Round($sys.TotalPhysicalMemory / 1GB, 2)
  Disk          = "$($dsk.Model) ($([math]::Round($dsk.Size/1GB,0)) GB)"
  Java          = (java -version 2>&1)[0]
  Node          = (node -v)
  JMeter        = "5.6.3"
} | Format-List
```

Dán kết quả vào `performance-testing/evidence/hardware/spec-table.md`.

> ⚠️ **Hostname phải trùng** với các HW trước (đề §11). Nếu đổi máy giữa chừng, phải giải thích trong report.

---

## 9. Checklist hoàn tất Phase này

- [ ] `java -version`, `node -v`, `python --version` đều OK
- [ ] Đang ở branch `HW5`
- [ ] `.tools\jmeter\bin\jmeter.bat -v` in ra `5.6.3`
- [ ] `.tools/` đã nằm trong `.gitignore` và `git check-ignore` xác nhận
- [ ] k6 cài được (hoặc đã ghi nhận việc bỏ qua)
- [ ] `node backend\server.js` chạy được, in `Server is running on http://localhost:3000`
- [ ] Smoke test §6 chạy hết 5/5 bước không lỗi
- [ ] `evidence/hardware/spec-table.md` đã có nội dung, hostname đã đối chiếu
- [ ] Commit: `chore(perf): setup jmeter/k6 toolchain and gitignore`
