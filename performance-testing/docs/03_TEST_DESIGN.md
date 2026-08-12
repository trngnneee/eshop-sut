# 03 — TEST DESIGN (Workflow + tham số tải)

> Đây là doc nền cho `deliverables/01_test-design.md` — phần chấm điểm chính của **Task 1** (60/100).
> Workflow: **Browse-to-buy** (MSSV 23127207). Ranh giới scope: `00_GROUP_SCOPE.md`.

---

## 1. Workflow end-to-end — 5 bước

Một iteration của một virtual user (VU):

| # | Label JMeter | Request | Nhóm endpoint | Think time sau bước |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `01_Login` | `POST /api/login` | **auth-heavy** | 1–2 s |
| 2 | `02_BrowseProducts` | `GET /api/products` *(không query string)* | **read-heavy** | **2–4 s** |
| 3 | `03_ProductDetail` | `GET /api/products/${product_id}` | **read-heavy** | 1–2 s |
| 4 | `04_AddToCart` | `POST /api/cart` + Bearer | **transactional** | 1 s |
| 5 | `05_Checkout` | `POST /api/checkout` + Bearer | **transactional** | — |

Dùng đúng các label này ở mọi `.jmx`, vì `analyze_jtl.py` và toàn bộ báo cáo trích dẫn theo tên label.

### 1.1 Luận cứ phủ đủ 3 nhóm endpoint (đề §5 + §6)

| Nhóm | Bước phủ | Vì sao đại diện được cho nhóm |
| :--- | :--- | :--- |
| **Auth-heavy** | 1 | `POST /api/login` là điểm vào duy nhất phát sinh JWT. Đây cũng là endpoint duy nhất có **trạng thái ghi ngược lại DB khi thất bại** (`login_attempts`, `locked_until` — `server.js:47-62`), nên nó vừa là auth vừa là ghi có tranh chấp |
| **Read-heavy** | 2 và 3 | Bước 2 là đọc **toàn bộ** catalog (`SELECT * FROM products` không WHERE — `server.js:153`); bước 3 là đọc **một** bản ghi theo khóa chính (`server.js:160`). Hai thái cực của chi phí đọc, đo được cả chi phí serialize lẫn chi phí truy vấn điểm |
| **Transactional** | 4 và 5 | Bước 4 ghi vào **bộ nhớ tiến trình** (`userCarts` — `server.js:293`); bước 5 ghi vào **SQLite** (`INSERT INTO orders` — `server.js:301`). Hai loại ghi khác hẳn nhau: một cái đo áp lực heap, một cái đo tranh chấp khóa file DB |

### 1.2 Vì sao think time như vậy

| Bước | Think time | Luận cứ |
| :--- | :--- | :--- |
| Sau 1 (login) | 1–2 s | Người dùng thật vừa đăng nhập xong, trang chủ tải và mắt lướt qua — khoảng dừng ngắn |
| Sau 2 (browse) | **2–4 s** | Đây là điểm khác biệt của Browse-to-buy so với Search-to-buy của Trâm: người **duyệt** catalog phải cuộn và đọc lưới sản phẩm, lâu hơn người đã biết rõ mình tìm gì rồi gõ từ khóa. Con số 2–4 s cũng làm giảm nhịp gọi lại endpoint nặng nhất, tránh biến Load test thành stress test ngoài ý muốn |
| Sau 3 (detail) | 1–2 s | Đọc mô tả + chọn số lượng |
| Sau 4 (cart) | 1 s | Thao tác cơ học, bấm sang trang thanh toán |
| Sau 5 | — | Kết thúc iteration |

Tổng think time ≈ **5–9 s/iteration** (trung bình ~7 s). Cộng thời gian phản hồi, mỗi VU sinh khoảng **6–8 iteration/phút** ở trạng thái nhàn.

Trong JMeter dùng **Uniform Random Timer**: `Constant Delay Offset` = cận dưới, `Random Delay Maximum` = độ rộng khoảng. Ví dụ 2–4 s → offset `2000`, max `2000`.

> **Không dùng think time = 0.** Đó là lỗi kinh điển của test plan do AI sinh: nó biến mọi kịch bản thành stress test và làm mất ý nghĩa của việc phân biệt Load / Stress / Spike. Xem `07_HUMAN_REVIEW_TEMPLATE.md` §mục 2.

---

## 2. Extract & assertion từng bước

| Bước | Extract | Assertion |
| :--- | :--- | :--- |
| 1 `01_Login` | JSON Extractor `$.token` → biến `token`<br>JSON Extractor `$.user.id` → biến `user_id` | • Response code `200`<br>• JSON Assertion: `$.token` tồn tại và khác rỗng |
| 2 `02_BrowseProducts` | JSON Extractor `$..id` → biến `pid`, `Match No. = 0` (random) | • Response code `200`<br>• Response Assertion (Contains, Regex): `^\[` — body phải là JSON **array** |
| 3 `03_ProductDetail` | — | • Response code `200`<br>• JSON Assertion: `$.name` tồn tại **và** `$.price` tồn tại |
| 4 `04_AddToCart` | — | • Response code `200`<br>• Response Assertion Contains: `Added to cart` |
| 5 `05_Checkout` | JSON Extractor `$.orderId` → biến `order_id` | • Response code `200`<br>• JSON Assertion: `$.orderId` tồn tại |

### 2.1 Vì sao assertion không được dừng ở "response code 200"

Hai bẫy đã xác nhận trong code:

- `server.js:161` — `GET /api/products/:id` với id không tồn tại trả **`200` kèm body `{}`**, không phải `404`. Nếu chỉ assert status thì test "xanh" trong khi thực chất chẳng lấy được sản phẩm nào.
- `server.js:162` — nếu `id` **chẵn**, `price` bị ép thành **string** (`row.price = row.price.toString()`). JSON Assertion trên `$.price` vẫn pass (trường tồn tại), nhưng đây là **bug functional cần log lên GitHub Issues** (đề §6 *"Report issues"*).

→ Bước 3 bắt buộc assert **nội dung**, và trong quá trình chạy phải quan sát xem `price` có lẫn kiểu string không, ghi vào bug report.

### 2.2 Xử lý lockout trong assertion

`POST /api/login` có 3 kết cục:

| Kết cục | Status | Body | Xử lý |
| :--- | :---: | :--- | :--- |
| Thành công | 200 | có `token` | pass |
| Sai mật khẩu | 401 | `Invalid email or password` | fail — điều tra ngay, CSV sai |
| **Bị khóa** | **403** | `Tài khoản đã bị khóa. Vui lòng thử lại sau.` | fail — **dấu hiệu chưa reset lockout**, dừng run và reset |

Trong Load/Stress/Spike **chỉ dùng credential đúng**, nên bất kỳ `401`/`403` nào cũng là tín hiệu bất thường phải giải thích trong `04_execution-report.md`, **không được im lặng bỏ qua**.

---

## 3. Ma trận tham số 4 kịch bản

Cả 4 kịch bản dùng **chung một workflow 5 bước** ở §1, chỉ khác mô hình tải — đúng yêu cầu đề: *"All three test plans must exercise the same end-to-end workflow."*

| | **Load** | **Stress** | **Spike** | **Endurance** |
| :--- | :--- | :--- | :--- | :--- |
| **Mục tiêu** | Đo hành vi ở tải kỳ vọng, ổn định | Tìm điểm gãy khi tải tăng dần | Đo khả năng chịu cú sốc và **phục hồi** | Tìm ngưỡng chịu tải bền của phần cứng |
| **Thread model** | 50 threads | 4 Thread Group xếp chồng: 25 → 50 → 100 → 200 | Baseline 10 threads chạy suốt + 2 đợt spike 300 threads | 30 threads |
| **Ramp-up** | 60 s | mỗi bậc 30 s | spike: **5 s** | 60 s |
| **Thời lượng** | 5 phút (scheduler) | 8 phút (4 bậc × 2 phút) | 6 phút | **12 phút** |
| **Think time** | 1–2 / 2–4 / 1–2 / 1 s | như Load | như Load | như Load |
| **Loop** | Infinite + scheduler | Infinite + scheduler | Infinite + scheduler | Infinite + scheduler |
| **Report view** | **Aggregate Report** | **Summary Report** | **View Results Tree** (Errors only) | Aggregate Report *(dùng lại — hợp lệ vì đề chỉ yêu cầu 3 view khác nhau trên bộ Load/Stress/Spike)* |
| **Tên file** | `23127207_Load_<YYYYMMDD>.jmx` | `23127207_Stress_<YYYYMMDD>.jmx` | `23127207_Spike_<YYYYMMDD>.jmx` | `23127207_Endurance_<YYYYMMDD>.jmx` |

> **Ba report view không lặp lại** (đề §6): Aggregate / Summary / View Results Tree. Endurance là kịch bản bổ sung ngoài bộ 3 bắt buộc nên được phép dùng lại view.

---

## 4. Luận cứ chọn tham số

### 4.1 Load — 50 threads, ramp 60 s, giữ 5 phút

- **50 VU**: SUT là demo Node.js đơn tiến trình, chạy cùng máy với JMeter. 50 VU với think time ~7 s cho **tải danh nghĩa ≈ 50 ÷ 7 ≈ 7 iteration/s ≈ 35 request/s** — nằm trong tầm phục vụ được của một tiến trình Node đơn luồng, đúng tinh thần Load test là "tải kỳ vọng", không phải tải phá.
- **Ramp-up 60 s** (≈ 0,8 VU/s): đủ chậm để tách bạch giai đoạn khởi động khỏi giai đoạn ổn định, nên p95 đo ở phần giữa mới phản ánh trạng thái steady-state. Ramp-up quá nhanh sẽ trộn chi phí khởi tạo thread của JMeter vào số đo.
- **Giữ 5 phút**: sau khi 50 VU đã vào hết (phút thứ 1), còn ~4 phút steady-state → đủ mẫu để percentile ổn định.

### 4.2 Stress — 25 → 50 → 100 → 200, mỗi bậc 2 phút

- **Bậc thang thay vì tăng liên tục**: mỗi bậc giữ 2 phút để hệ đạt trạng thái ổn định ở mức tải đó, nhờ vậy **so sánh p95 giữa các bậc mới có nghĩa**. Tăng liên tục cho đường cong đẹp nhưng không tách được "chậm vì tải" khỏi "chậm vì đang tăng tải".
- **Vì sao 4 Thread Group xếp chồng bằng `startup delay` mà không dùng Stepping/Concurrency Thread Group**: hai loại đó thuộc plugin `jpgc` phải tải thêm. Xếp chồng Thread Group là **cơ chế lõi của JMeter**, không phụ thuộc plugin → `.jmx` mở được trên máy TA mà không cần cài gì thêm. Đánh đổi: tải thực tế là **tổng dồn** của các nhóm đang chạy, nên phải cấu hình delay và duration khớp nhau (chi tiết ở `04_JMX_BUILD_SPEC.md` §4.2).
- **Trần 200 VU**: vượt xa mức Load 4 lần, đủ để chạm điểm gãy trên máy cá nhân mà chưa làm JMeter tự nghẽn (JMeter chạy chung máy nên vượt ~300 thread thì chính JMeter thành nút cổ chai, số đo mất giá trị).

### 4.3 Spike — baseline 10 + 2 đợt 300 VU ramp 5 s

- **Baseline 10 VU chạy suốt**: có nền tải liên tục thì mới đo được **thời gian phục hồi** sau spike — nếu spike xong không còn request nào, không biết hệ đã trở lại bình thường hay chưa.
- **300 VU trong 5 s** (60 VU/s): mô phỏng flash sale / thông báo đẩy. Ramp gần như tức thời chính là bản chất của Spike, khác hẳn Stress tăng có kiểm soát.
- **Hai đợt spike**: đợt 1 đo phản ứng lần đầu; đợt 2 (sau khi đã hồi) kiểm tra hệ có **suy giảm tích lũy** không — với `userCarts` rò rỉ bộ nhớ (`server.js:14,293`), giả thuyết là đợt 2 tệ hơn đợt 1. Đây là quan sát cần xác nhận bằng số, không kết luận trước.
- **300 VU cần ≥ 300 account**: pool 400 user ở `02_DATA_SPEC.md` được chọn chính vì con số này.

### 4.4 Endurance — 30 VU × 12 phút

- Đề yêu cầu soak **10–15 phút**; chọn **12 phút** ở giữa khoảng.
- **30 VU** (dưới mức Load 50) để hệ chắc chắn **không** bão hòa CPU — mục tiêu là tách riêng hiệu ứng **tích lũy theo thời gian** (rò rỉ bộ nhớ, DB phình) khỏi hiệu ứng **tải tức thời**. Nếu chạy soak ở mức bão hòa thì không phân biệt được hai nguyên nhân.
- Số cần thu ở kịch bản này (đề §6 *"reported with concrete numbers"*):
  - **Max stable RPS** — throughput trung bình ở khoảng steady-state
  - **Memory ceiling** — RSS đỉnh của tiến trình `node` (từ `resource-endurance.csv`)
  - **Xu hướng RSS** — có tăng đơn điệu không, tốc độ MB/phút
  - **Trôi p95** — p95 của 2 phút đầu so với 2 phút cuối

---

## 5. Xử lý account lockout theo từng kịch bản

| Kịch bản | Rủi ro lockout | Biện pháp |
| :--- | :--- | :--- |
| **Load** | Thấp — 50 VU trên 400 account, chỉ login đúng | Reset trước run cho sạch |
| **Stress** | **Cao** — 200 VU đồng thời, CSV recycle nhiều vòng | Reset **trước mỗi bậc**? Không — chỉ reset **trước run**, vì reset giữa chừng sẽ làm nhiễu số đo. Thay vào đó theo dõi tỉ lệ `403` và ghi lại |
| **Spike** | **Cao nhất** — 310 VU, CSV recycle rất nhanh | Reset trước run; nếu `403` > 1% thì nâng pool user lên 600 và chạy lại |
| **Endurance** | Trung bình — 30 VU nhưng chạy 12 phút, recycle nhiều vòng | Reset trước run |

**Nguyên tắc:** dùng **credential đúng 100%**. Không cố tình chèn login sai vào 3 kịch bản chính, vì lockout 3 phút (`server.js:57`) sẽ đầu độc pool account và làm hỏng số đo hiệu năng.

> Hành vi lockout **vẫn được kiểm chứng riêng**, bằng một probe thủ công ngoài test plan hiệu năng (xem `05_EXECUTION_RUNBOOK.md` §6). Kết quả probe là bằng chứng cho bug FR-02 (`+2` thay vì `+1`, 180 s thay vì 30 s) trong bug report.

---

## 6. Ngưỡng (SLO) đề xuất — đặt TRƯỚC khi chạy

Đặt ngưỡng trước để tránh thiên kiến "số đo ra sao thì ngưỡng thế đó". Đây là **giả định ban đầu**, sẽ được hiệu chỉnh trong `05_endurance-threshold.md` bằng số liệu thật.

| Metric | Ngưỡng đề xuất | Lý do |
| :--- | :--- | :--- |
| p95 `02_BrowseProducts` | ≤ 800 ms | Endpoint nặng nhất, người dùng chấp nhận < 1 s cho trang danh sách |
| p95 `03_ProductDetail` | ≤ 300 ms | Truy vấn theo khóa chính, phải nhanh |
| p95 `05_Checkout` | ≤ 1000 ms | Có ghi DB, chấp nhận chậm hơn |
| Error rate (Load) | ≤ 0,1 % | Ở tải kỳ vọng gần như không được lỗi |
| Error rate (Stress ở bậc ≤ 100 VU) | ≤ 1 % | |
| Throughput ổn định (Load) | ≥ 25 req/s | Ước lượng từ §4.1 |

> Ngưỡng cho Spike **không đặt trước**: mục tiêu của Spike là mô tả hành vi khi quá tải và đo thời gian phục hồi, không phải đạt/không đạt một con số.

---

## 7. Giới hạn phương pháp — bắt buộc ghi vào report

Nêu thẳng những giới hạn này là **điểm cộng** khi chấm phần phân tích, không phải điểm trừ:

1. **JMeter và SUT chạy cùng một máy.** JMeter tiêu thụ CPU/RAM đáng kể, nên ở tải cao một phần độ trễ đo được đến từ chính công cụ đo. Giảm thiểu bằng cách chạy **non-GUI**; nhưng không loại bỏ được hoàn toàn. Mọi kết luận về "điểm gãy" là điểm gãy của **hệ máy đo + máy bị đo**, không phải của riêng SUT.
2. **Không có network latency thật.** Mọi request đi qua loopback → số đo là cận dưới lý tưởng; môi trường thật sẽ chậm hơn.
3. **SQLite là file cục bộ.** Hành vi tranh chấp khóa khác hẳn DB client-server; kết luận không suy rộng sang PostgreSQL/MySQL được.
4. **DB đã seed thêm 500 sản phẩm** (`02_DATA_SPEC.md` §1) → số đo `02_BrowseProducts` không so trực tiếp được với thành viên chạy trên DB gốc 5 sản phẩm.
5. **Cart lưu trong RAM tiến trình** (`server.js:14`) → restart server là mất sạch giỏ hàng. Mọi so sánh giữa các run phải tính đến việc server có bị restart giữa chừng hay không.

---

## 8. Checklist

- [ ] Workflow đúng **5 bước**, không có `?search=` / `apply-coupon` / `my-orders` / `categories`
- [ ] Label khớp `01_Login` … `05_Checkout`
- [ ] Think time có luận cứ, không có bước nào = 0
- [ ] 4 kịch bản dùng chung workflow, chỉ khác mô hình tải
- [ ] 3 report view khác nhau trên bộ Load/Stress/Spike
- [ ] Assertion kiểm **nội dung**, không chỉ status code
- [ ] Đã ghi ngưỡng SLO **trước** khi chạy
- [ ] Đã ghi 5 giới hạn phương pháp ở §7
- [ ] Nội dung này được viết lại thành `deliverables/01_test-design.md`
- [ ] Commit: `docs(perf): add browse-to-buy test design and AI generation log`
