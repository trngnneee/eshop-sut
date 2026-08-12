# 04 — JMX BUILD SPEC

> Đặc tả để sinh 4 file `.jmx` + 1 script k6. Tham số tải lấy từ `03_TEST_DESIGN.md` §3.
> **Trước khi bắt đầu: đọc lại `00_GROUP_SCOPE.md` §4.2.** Mỗi `.jmx` chỉ được có **đúng 5 HTTP Sampler**.

---

## 1. Khung chung của cả 4 test plan

Mọi `.jmx` dùng chung cấu trúc này; chỉ phần **Thread Group** và **Listener** khác nhau.

```
Test Plan  "23127207_<Scenario>_<YYYYMMDD>"
│   User Defined Variables:
│     BASE_HOST = localhost
│     BASE_PORT = 3000
│     PROTOCOL  = http
│
├── HTTP Request Defaults
│     Protocol: ${PROTOCOL}   Server: ${BASE_HOST}   Port: ${BASE_PORT}
│     Content encoding: UTF-8
│     Implementation: HttpClient4
│
├── HTTP Header Manager  (mức Test Plan)
│     Content-Type: application/json
│     Accept:       application/json
│
├── CSV Data Set Config  "khoa_users"
│     (thuộc tính bắt buộc — xem §2)
│
└── <THREAD GROUP(S)>            ← khác nhau theo scenario, xem §4
    │
    ├── HTTP Sampler  "01_Login"
    │     └── JSON Extractor  "extract_token"    $.token     → token
    │     └── JSON Extractor  "extract_userid"   $.user.id   → user_id
    │     └── Response Assertion  "assert_login_200"
    │     └── JSON Assertion     "assert_token_exists"
    │     └── Uniform Random Timer   offset 1000 / random 1000
    │
    ├── HTTP Sampler  "02_BrowseProducts"
    │     └── JSON Extractor  "extract_pid"      $..id  Match No. 0  → pid
    │     └── Response Assertion  "assert_browse_200"
    │     └── Response Assertion  "assert_is_array"
    │     └── Uniform Random Timer   offset 2000 / random 2000
    │
    ├── HTTP Sampler  "03_ProductDetail"
    │     └── Response Assertion  "assert_detail_200"
    │     └── JSON Assertion      "assert_has_name_price"
    │     └── Uniform Random Timer   offset 1000 / random 1000
    │
    ├── HTTP Sampler  "04_AddToCart"
    │     └── HTTP Header Manager   Authorization: Bearer ${token}
    │     └── Response Assertion  "assert_cart_200"
    │     └── Response Assertion  "assert_cart_message"
    │     └── Uniform Random Timer   offset 1000 / random 500
    │
    ├── HTTP Sampler  "05_Checkout"
    │     └── HTTP Header Manager   Authorization: Bearer ${token}
    │     └── JSON Extractor  "extract_orderid"  $.orderId → order_id
    │     └── Response Assertion  "assert_checkout_200"
    │     └── JSON Assertion      "assert_orderid_exists"
    │
    └── <LISTENER>                ← khác nhau theo scenario, xem §6
```

> **Timer đặt bên trong sampler** (làm con của sampler đó) chứ không đặt ở mức Thread Group. JMeter áp dụng timer **trước** khi chạy sampler chứa nó, nên đặt bên trong từng sampler mới kiểm soát được think time khác nhau cho từng bước.

---

## 2. CSV Data Set Config — thuộc tính bắt buộc

| Thuộc tính | Giá trị | Vì sao |
| :--- | :--- | :--- |
| Filename | `${__P(csvdir,)}/khoa_users.csv` | Đường dẫn truyền từ CLI bằng `-Jcsvdir=`, không hard-code path máy cá nhân |
| File encoding | `UTF-8` | `shipping_address` có tiếng Việt |
| Variable Names | *(để trống)* | Đọc tên biến từ dòng header của CSV |
| Ignore first line | `true` | Vì đang lấy tên biến từ header |
| Delimiter | `,` | |
| **Allow quoted data?** | **`true`** | `shipping_address` chứa dấu phẩy, được bọc `"` (RFC 4180) |
| **Recycle on EOF?** | **`true`** | Test chạy theo thời lượng, phải quay vòng khi hết 400 dòng |
| **Stop thread on EOF?** | **`false`** | Nếu `true`, thread sẽ chết khi hết file và tải sụt giữa chừng |
| **Sharing mode** | **`All threads`** | ⚠️ **Quan trọng nhất.** Mọi thread dùng chung một con trỏ đọc → mỗi thread nhận một dòng khác nhau. Nếu để `Current thread group` hoặc `Current thread`, mỗi thread đọc lại từ đầu file → **hàng trăm thread cùng đăng nhập bằng `khoa001@eshop.com`** → tranh chấp hàng `users` và lockout dây chuyền |

Biến sinh ra từ header: `email`, `password`, `product_id`, `quantity`, `price`, `total_amount`, `shipping_address`.

---

## 3. Chi tiết 5 HTTP Sampler

### 3.1 `01_Login`

| | |
| :--- | :--- |
| Method | `POST` |
| Path | `/api/login` |
| Body Data | `{"email":"${email}","password":"${password}"}` |

- JSON Extractor `extract_token`: JSON Path `$.token` → `token`, Default Value `TOKEN_NOT_FOUND`
- JSON Extractor `extract_userid`: JSON Path `$.user.id` → `user_id`, Default Value `-1`
- Response Assertion `assert_login_200`: Field = `Response Code`, Pattern Matching = `Equals`, Pattern = `200`
- JSON Assertion `assert_token_exists`: JSON Path `$.token`, tick *Assert JSON Path exists*, tick *Additionally assert value* với *Expect null* **tắt**

> Đặt `Default Value` cho extractor để khi login fail, biến `token` mang giá trị nhận biết được thay vì chuỗi rỗng — nhờ đó `04_AddToCart` fail với `401` rõ ràng, dễ truy nguyên hơn là fail mơ hồ.

### 3.2 `02_BrowseProducts`

| | |
| :--- | :--- |
| Method | `GET` |
| Path | `/api/products` |
| Parameters | **KHÔNG CÓ.** Không `search`, không `page`, không gì cả |

- JSON Extractor `extract_pid`: JSON Path `$..id`, **Match No. = `0`** (JMeter hiểu `0` là *chọn ngẫu nhiên một match*), → `pid`, Default Value `${product_id}` (rơi về giá trị từ CSV)
- Response Assertion `assert_browse_200`: Response Code Equals `200`
- Response Assertion `assert_is_array`: Field = `Text Response`, Pattern Matching = `Matches`, Pattern = `^\s*\[[\s\S]*\]\s*$`

> ⚠️ **Bẫy scope.** Nếu thấy bất kỳ chỗ nào trong `.jmx` có `search`, đó là lỗi — endpoint đó thuộc Trâm/Nguyên/Thịnh. Xem `00_GROUP_SCOPE.md` §4.2.

### 3.3 `03_ProductDetail`

| | |
| :--- | :--- |
| Method | `GET` |
| Path | `/api/products/${pid}` |

- Response Assertion `assert_detail_200`: Response Code Equals `200`
- JSON Assertion `assert_has_name_price`: JSON Path `$.name`, *Assert JSON Path exists*
- Thêm JSON Assertion thứ hai cho `$.price` (JSON Assertion chỉ nhận một path mỗi element)

> **Không** assert kiểu dữ liệu của `price`. Với `id` chẵn backend trả `price` dạng string (`server.js:162`) — nếu assert kiểu, test sẽ fail ~50% và làm hỏng số đo hiệu năng. Đây là **bug functional**, ghi nhận riêng vào bug report (`05_EXECUTION_RUNBOOK.md` §8), không trộn vào phép đo.

### 3.4 `04_AddToCart`

| | |
| :--- | :--- |
| Method | `POST` |
| Path | `/api/cart` |
| Header riêng | `Authorization: Bearer ${token}` |
| Body Data | xem dưới |

```json
{"product_id":${pid},"quantity":${quantity},"name":"PERF item ${pid}","price":${price}}
```

- Response Assertion `assert_cart_200`: Response Code Equals `200`
- Response Assertion `assert_cart_message`: Text Response, `Contains`, `Added to cart`

### 3.5 `05_Checkout`

| | |
| :--- | :--- |
| Method | `POST` |
| Path | `/api/checkout` |
| Header riêng | `Authorization: Bearer ${token}` |
| Body Data | `{"total_amount":${total_amount},"shipping_address":"${shipping_address}"}` |

- JSON Extractor `extract_orderid`: `$.orderId` → `order_id`, Default `-1`
- Response Assertion `assert_checkout_200`: Response Code Equals `200`
- JSON Assertion `assert_orderid_exists`: JSON Path `$.orderId`, *Assert JSON Path exists*

> `shipping_address` từ CSV có dấu phẩy nhưng **không** có dấu nháy kép bên trong (đã kiểm ở `02_DATA_SPEC.md` §3.3), nên nhúng thẳng vào JSON là an toàn. Nếu sau này dữ liệu có `"`, phải bọc qua `${__escapeXml()}` hoặc đổi cách sinh dữ liệu.

---

## 4. Thread Group theo từng kịch bản

### 4.1 Load — `23127207_Load_<YYYYMMDD>.jmx`

Một Thread Group duy nhất:

| Thuộc tính | Giá trị |
| :--- | :--- |
| Name | `TG_Load_50VU` |
| Number of Threads | `50` |
| Ramp-Up Period | `60` |
| Loop Count | `Infinite` ✓ |
| Specify Thread Lifetime | ✓ |
| Duration (seconds) | `300` |
| Startup delay | `0` |
| Action on sampler error | `Continue` |

### 4.2 Stress — `23127207_Stress_<YYYYMMDD>.jmx`

**Bốn** Thread Group song song, xếp bậc bằng `Startup delay`. Không dùng plugin `jpgc`.

| Thread Group | Threads | Ramp-Up | Startup delay | Duration | Cửa sổ hoạt động | VU đồng thời |
| :--- | :---: | :---: | :---: | :---: | :--- | :---: |
| `TG_Stress_Step1_25VU` | 25 | 30 | 0 | 480 | 0 → 480 s | |
| `TG_Stress_Step2_25VU` | 25 | 30 | 120 | 360 | 120 → 480 s | |
| `TG_Stress_Step3_50VU` | 50 | 30 | 240 | 240 | 240 → 480 s | |
| `TG_Stress_Step4_100VU` | 100 | 30 | 360 | 120 | 360 → 480 s | |

Tải **dồn** theo thời gian — đây chính là hiệu ứng bậc thang mong muốn:

| Phút | VU đồng thời | Bậc |
| :---: | :---: | :--- |
| 0–2 | 25 | Bậc 1 |
| 2–4 | 50 | Bậc 2 |
| 4–6 | 100 | Bậc 3 |
| 6–8 | **200** | Bậc 4 |

> **Điểm dễ sai:** `Duration` của mỗi nhóm phải khớp sao cho **tất cả cùng kết thúc ở giây 480**, nếu không các bậc sẽ tắt lệch nhau và biểu đồ tải thành hình răng cưa. Công thức: `Duration = 480 − Startup delay`.
>
> Vì tải là tổng dồn, khi báo cáo phải nói rõ "bậc 4 = 200 VU đồng thời", không phải "100 VU".

Cả 4 Thread Group **dùng chung một cây 5 sampler** — trong JMeter phải **sao chép** cây sampler vào từng Thread Group (JMeter không cho chia sẻ sampler giữa các Thread Group). Cách gọn hơn: đưa 5 sampler vào một **Module Controller** trỏ tới một **Test Fragment**, mỗi Thread Group chỉ chứa một Module Controller.

**Khuyến nghị: dùng Test Fragment + Module Controller** cho file Stress, để 5 sampler chỉ được định nghĩa một lần và không bị lệch giữa các bậc khi chỉnh sửa.

```
Test Plan
├── Test Fragment  "FRAG_BrowseToBuy"   (Enabled = false ở mức fragment là mặc định)
│     └── 01_Login … 05_Checkout        (đầy đủ extractor/assertion/timer)
├── TG_Stress_Step1_25VU   └── Module Controller → FRAG_BrowseToBuy
├── TG_Stress_Step2_25VU   └── Module Controller → FRAG_BrowseToBuy
├── TG_Stress_Step3_50VU   └── Module Controller → FRAG_BrowseToBuy
└── TG_Stress_Step4_100VU  └── Module Controller → FRAG_BrowseToBuy
```

### 4.3 Spike — `23127207_Spike_<YYYYMMDD>.jmx`

Ba Thread Group:

| Thread Group | Threads | Ramp-Up | Startup delay | Duration | Vai trò |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `TG_Spike_Baseline_10VU` | 10 | 30 | 0 | 360 | Nền tải liên tục, để đo phục hồi |
| `TG_Spike_Burst1_300VU` | 300 | **5** | 60 | 30 | Đợt sốc 1: giây 60 → 90 |
| `TG_Spike_Burst2_300VU` | 300 | **5** | 240 | 30 | Đợt sốc 2: giây 240 → 270 |

Dòng thời gian:

```
0s ────────── 60s ══════ 90s ────────── 240s ══════ 270s ────────── 360s
   baseline 10VU  ↑spike 310VU↑  hồi phục   ↑spike 310VU↑   hồi phục
```

- Khoảng 90 → 240 s (2,5 phút) là **cửa sổ đo phục hồi** sau đợt 1.
- Khoảng 270 → 360 s là cửa sổ phục hồi sau đợt 2.
- So sánh p95 của baseline ở ba giai đoạn (trước sốc / giữa hai sốc / sau sốc 2) để phát hiện suy giảm tích lũy.

> Cũng dùng Test Fragment + Module Controller như Stress.

### 4.4 Endurance — `23127207_Endurance_<YYYYMMDD>.jmx`

| Thuộc tính | Giá trị |
| :--- | :--- |
| Name | `TG_Endurance_30VU` |
| Number of Threads | `30` |
| Ramp-Up Period | `60` |
| Loop Count | `Infinite` ✓ |
| Duration (seconds) | **`720`** (12 phút) |
| Startup delay | `0` |

---

## 5. Cơ chế chọn `product_id` — hai tầng

| Tầng | Nguồn | Khi nào dùng |
| :---: | :--- | :--- |
| 1 | JSON Extractor `$..id` với `Match No. = 0` trên response của `02_BrowseProducts` | Mặc định. Mỗi VU lấy **ngẫu nhiên** một sản phẩm từ danh sách vừa duyệt — đúng hành vi "browse rồi chọn đại một cái" |
| 2 | Cột `product_id` trong CSV, gán làm `Default Value` của extractor | Dự phòng khi bước 2 lỗi hoặc trả mảng rỗng |

Cấu hình đúng của extractor `extract_pid`:

```
Names of created variables : pid
JSON Path expressions      : $..id
Match No. (0 for Random)   : 0
Default Values             : ${product_id}
```

> Đây cũng là điểm làm workflow **data-driven ở hai cấp** (đề §6): dữ liệu vừa đến từ CSV, vừa đến từ correlation động của response — nên nhấn mạnh trong `deliverables/01_test-design.md`.

---

## 6. Listener — ba loại khác nhau, không lặp

Đề §6: *"Across the three test plans, use three distinct listener / report types; do not repeat a type."*

| File `.jmx` | Listener | Cấu hình |
| :--- | :--- | :--- |
| **Load** | **Aggregate Report** | Filename để trống trong `.jmx` (đường dẫn `.jtl` truyền qua CLI `-l`) |
| **Stress** | **Summary Report** | như trên |
| **Spike** | **View Results Tree** | **Bắt buộc**: mở *Log/Display Only* → tick **`Errors`**. Không tick sẽ ghi toàn bộ request/response của 310 VU → file hàng GB và JMeter treo |
| **Endurance** | Aggregate Report | Dùng lại — hợp lệ, vì ràng buộc "3 view khác nhau" chỉ áp cho bộ Load/Stress/Spike |

> Khi chạy non-GUI, listener trong `.jmx` **không render UI** nhưng vẫn được ghi vào `.jmx` làm bằng chứng thiết kế, và TA mở GUI sẽ thấy đúng loại view. Số liệu thực tế đến từ file `.jtl` do tham số `-l` sinh ra.
>
> Để chụp ảnh màn hình listener cho báo cáo: sau khi chạy xong, mở JMeter GUI → mở đúng `.jmx` → nạp file `.jtl` vào listener (nút *Browse* trong listener) → chụp. Cách này cho ảnh listener thật mà không phải chạy lại ở chế độ GUI.

---

## 7. Cấu hình ghi `.jtl` — bắt buộc đủ trường

Đề §11: *"The raw `.jtl` log files, attached in full — not only the summary."*

Tạo `performance-testing/scripts/jmeter-user.properties`:

```properties
jmeter.save.saveservice.output_format=csv
jmeter.save.saveservice.timestamp_format=ms
jmeter.save.saveservice.print_field_names=true

jmeter.save.saveservice.time=true
jmeter.save.saveservice.label=true
jmeter.save.saveservice.response_code=true
jmeter.save.saveservice.response_message=true
jmeter.save.saveservice.successful=true
jmeter.save.saveservice.thread_name=true
jmeter.save.saveservice.thread_counts=true
jmeter.save.saveservice.bytes=true
jmeter.save.saveservice.sent_bytes=true
jmeter.save.saveservice.latency=true
jmeter.save.saveservice.connect_time=true
jmeter.save.saveservice.assertion_results_failure_message=true
jmeter.save.saveservice.idle_time=true

# Không lưu response body -> file .jtl không phình, vẫn đủ dữ liệu phân tích
jmeter.save.saveservice.response_data=false
jmeter.save.saveservice.samplerData=false
```

Header CSV kỳ vọng của `.jtl`:

```
timeStamp,elapsed,label,responseCode,responseMessage,threadName,dataType,success,failureMessage,bytes,sentBytes,grpThreads,allThreads,URL,Latency,IdleTime,Connect
```

`analyze_jtl.py` (`06_ANALYSIS_SPEC.md`) đọc đúng bộ cột này.

---

## 8. Đặc tả k6 (bonus) — `k6/23127207_Load_<YYYYMMDD>.js`

Chỉ làm bản tương đương **Load**. Không chặn deliverable chính.

| Mục | Yêu cầu |
| :--- | :--- |
| Workflow | Đúng 5 request như §3, cùng thứ tự, cùng tên nhóm (`group()` đặt tên `01_Login` … `05_Checkout`) |
| Dữ liệu | Đọc `data/khoa_users.csv` bằng `SharedArray` + `papaparse` (hoặc tự parse để tránh dependency ngoài) |
| Tải | `stages`: `{ duration: '60s', target: 50 }`, `{ duration: '300s', target: 50 }`, `{ duration: '30s', target: 0 }` |
| Think time | `sleep()` với cùng khoảng như §1: 1–2 / 2–4 / 1–2 / 1 s |
| Check | Tương đương assertion ở §3 (`check()` trên status và nội dung) |
| Thresholds | `http_req_duration: ['p(95)<800']`, `http_req_failed: ['rate<0.001']` |
| Output | `handleSummary()` ghi `results/k6/summary.json` **và** `results/k6/summary.html` |

Lệnh chạy:
```powershell
k6 run --out json="performance-testing\results\k6\raw.json" `
  "performance-testing\k6\23127207_Load_20260812.js"
```

Trong report ghi rõ: k6 là **phần bổ sung**, kết luận chính dựa trên JMeter.

---

## 9. Nghiệm thu `.jmx` — làm đủ trước khi commit

### 9.1 Kiểm tra scope (tự động)

```powershell
Select-String -Path "performance-testing\test-plans\*.jmx" `
  -Pattern "search=|apply-coupon|my-orders|/api/categories|/api/admin|/api/register|forgot-password"
```
→ **phải không có kết quả.**

### 9.2 Đếm sampler

```powershell
Get-ChildItem "performance-testing\test-plans\*.jmx" | ForEach-Object {
  $n = (Select-String -Path $_.FullName -Pattern 'HTTPSamplerProxy' -AllMatches).Matches.Count
  "$($_.Name): $n HTTPSamplerProxy tags"
}
```
→ Load/Endurance: `5` sampler (mỗi sampler xuất hiện 1 tag mở). Stress/Spike dùng Test Fragment nên cũng chỉ `5`.

### 9.3 Mở bằng GUI

```powershell
& ".tools\jmeter\bin\jmeter.bat" -t "performance-testing\test-plans\23127207_Load_20260812.jmx"
```
→ Không element nào bị đánh dấu đỏ / báo lỗi khi nạp.

### 9.4 Chạy thử 1 thread × 1 loop — **bắt buộc, không bỏ qua**

Tạm sửa Thread Group về `Threads=1`, `Loop=1`, bỏ tick Duration, chạy GUI, xem View Results Tree:

- [ ] `01_Login` → 200, `token` extract được (kiểm ở tab *Response Data*)
- [ ] `02_BrowseProducts` → 200, body là array 505 phần tử
- [ ] `03_ProductDetail` → 200, `pid` đã được thay bằng số thật (kiểm URL trong tab *Request*)
- [ ] `04_AddToCart` → 200, `Added to cart`, header `Authorization` có token thật
- [ ] `05_Checkout` → 200, có `orderId`

**Chỉ khi 5/5 xanh mới khôi phục tham số tải và chạy full.** Chạy full với `.jmx` chưa smoke sẽ tốn cả chục phút để rồi phát hiện `${token}` chưa bao giờ được thay.

---

## 10. Checklist

- [ ] 4 file `.jmx` đúng quy ước tên `23127207_{Scenario}_{YYYYMMDD}`
- [ ] Mỗi plan có **đúng 5** sampler, label `01_Login` … `05_Checkout`
- [ ] `Select-String` §9.1 không trả kết quả
- [ ] `CSV Data Set Config`: `Sharing mode = All threads`, `Recycle = true`, `Stop thread on EOF = false`, `Allow quoted data = true`
- [ ] Timer nằm **trong** từng sampler, không bước nào think time = 0
- [ ] Header `Authorization: Bearer ${token}` có ở bước 4 và 5
- [ ] Listener: Load = Aggregate, Stress = Summary, Spike = View Results Tree (**Errors only**)
- [ ] Stress: 4 Thread Group, `Duration = 480 − Startup delay`
- [ ] Spike: 3 Thread Group, ramp-up spike = 5 s
- [ ] `jmeter-user.properties` đã tạo, `response_data=false`
- [ ] Smoke 1×1 xanh 5/5 cho **cả 4** plan
- [ ] Commit tách riêng: Load → Stress → Spike+Endurance+k6 (xem `00_BUILD_SPEC.md` §4)
