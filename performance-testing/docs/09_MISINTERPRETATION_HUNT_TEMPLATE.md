# 09 — MISINTERPRETATION HUNT (Task 2)

> Khung cho `deliverables/06_ai-analysis-critique.md`. **10 điểm.**
> Đề §6 Task 2: *"identify where it misinterprets or misreads the metrics. For each misinterpretation, cite the **correct value from your raw `.jtl` log** and explain the error."* + *"classify each as **feasible or hallucinated**, with reasoning."*

---

## 1. Cấu trúc bắt buộc của `06_ai-analysis-critique.md`

| Phần | Nội dung | Nguồn |
| :--- | :--- | :--- |
| **§1 — Output thô của AI** | Dán **nguyên văn** kết quả 3 prompt A/B/C. Không sửa, không rút gọn, không tô đẹp | `08_AI_ANALYSIS_PROMPTS.md` §3 |
| **§2 — Săn lỗi diễn giải** | Bảng đối chiếu từng nhận định sai với giá trị đúng từ `.jtl` | §2 dưới đây |
| **§3 — Phán quyết đề xuất tối ưu** | Bảng feasible / hallucinated kèm lý do | §3 dưới đây |
| **§4 — Kết luận** | Mẫu sai của AI, và cách mình dùng AI khác đi ở lần sau | §4 dưới đây |

---

## 2. §2 — Bảng săn lỗi diễn giải

### 2.1 Định dạng bảng

| # | Nhận định của AI (trích nguyên văn) | Giá trị AI nói | **Giá trị đúng** | Nguồn xác minh | Loại lỗi | Giải thích |
| :--: | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | | | | `summary.json` → `labels.XX.elapsed.p95` | | |

Cột **Nguồn xác minh** phải trỏ tới vị trí cụ thể trong `.jtl` hoặc `summary.json`, kèm lệnh tái lập được. Ví dụ:

```powershell
# Xác minh p95 của 02_BrowseProducts trong run Load
python performance-testing\scripts\analyze_jtl.py `
  --jtl "performance-testing\results\load\23127207_Load_20260812.jtl" --scenario Load
# -> labels["02_BrowseProducts"]["elapsed"]["p95"]
```

### 2.2 Cần bao nhiêu mục

**Tối thiểu 3 lỗi diễn giải thật.** Chất lượng hơn số lượng: một lỗi được truy tới tận nguồn và giải thích rõ cơ chế còn giá trị hơn năm lỗi hời hợt.

Nếu AI phân tích quá tốt và không đủ 3 lỗi: **đừng bịa**. Thay vào đó ghi rõ *"AI phân tích chính xác ở N/M nhận định"*, liệt kê những chỗ nó đúng, rồi phân tích **những chỗ nó nói mơ hồ hoặc thiếu điều kiện** — mơ hồ cũng là một dạng khiếm khuyết đáng phân tích.

### 2.3 Sáu loại lỗi diễn giải hay gặp — đối chiếu output thật

Đây là **danh sách cần kiểm tra**, không phải danh sách để chép. Đọc output AI rồi soi xem có mắc cái nào không.

#### Loại A — Nhầm `Latency` với response time

| | |
| :--- | :--- |
| **Dấu hiệu** | AI nói "thời gian phản hồi trung bình là X ms" nhưng X khớp cột `Latency`, không khớp `elapsed` |
| **Vì sao là lỗi** | `Latency` là thời gian tới **byte đầu tiên**; `elapsed` là thời gian tới **byte cuối cùng**. Với `02_BrowseProducts` trả về ~150 KB JSON của 505 sản phẩm, khoảng cách giữa hai con số là đáng kể — đó chính là chi phí truyền và serialize payload lớn, phần quan trọng nhất của endpoint này |
| **Xác minh** | So `labels["02_BrowseProducts"].elapsed.avg` với `.latency.avg` trong `summary.json` |
| **Ghi vào báo cáo** | *"AI báo response time trung bình `<<X>>` ms. Giá trị đúng từ `.jtl` là `<<Y>>` ms (cột `elapsed`); `<<X>>` là giá trị của cột `Latency`. Chênh lệch `<<Y−X>>` ms chính là thời gian truyền `<<bytes>>` byte payload — phần chi phí đặc trưng nhất của endpoint trả toàn bộ catalog, và cũng là phần AI đã bỏ qua."* |

#### Loại B — Nhầm tổng giây CPU với phần trăm CPU

| | |
| :--- | :--- |
| **Dấu hiệu** | AI đọc `resource-*.csv` và nói "CPU đạt 240 %" hoặc "CPU tăng liên tục suốt run" |
| **Vì sao là lỗi** | Nếu cột đó là `TotalProcessorTime` tích lũy thì nó **luôn tăng đơn điệu** theo định nghĩa, kể cả khi hệ nhàn rỗi. Diễn giải thành "CPU tăng liên tục ⇒ hệ đang quá tải" là sai về bản chất metric |
| **Xác minh** | Xem đặc tả cột ở `05_EXECUTION_RUNBOOK.md` §1.2 — `cpu_percent` được tính bằng **delta** chia cho khoảng lấy mẫu |
| **Ghi vào báo cáo** | Nêu rõ metric tích lũy khác metric tức thời như thế nào |

#### Loại C — Nhầm error rate vì đếm sai cột

| | |
| :--- | :--- |
| **Dấu hiệu** | AI nói "tỉ lệ lỗi 0 %" trong khi `summary.json` cho `error_rate_pct > 0`, hoặc ngược lại |
| **Vì sao là lỗi** | JMeter đánh `success = false` khi **assertion fail**, kể cả khi `responseCode = 200`. Đếm theo `responseCode != 200` sẽ bỏ sót nhóm lỗi này. Trên SUT này chuyện đó có thật: `GET /api/products/:id` trả `200` với body rỗng (`server.js:161`) |
| **Xác minh** | ```powershell<br>$j = Import-Csv "<jtl>"<br>"success=false : " + ($j \| Where-Object success -eq 'false').Count<br>"code<>200     : " + ($j \| Where-Object responseCode -ne '200').Count<br>``` Hai số này **khác nhau** là bằng chứng |

#### Loại D — Nhầm thread count của Stress

| | |
| :--- | :--- |
| **Dấu hiệu** | AI nói "bậc cuối chạy 100 luồng" |
| **Vì sao là lỗi** | Thiết kế Stress dùng **4 Thread Group xếp chồng** (`03_TEST_DESIGN.md` §4.2). Ở bậc 4, cả bốn nhóm cùng hoạt động → `25 + 25 + 50 + 100 = 200` luồng đồng thời. Con số 100 chỉ là **kích thước của nhóm thứ tư** |
| **Xác minh** | `max(allThreads)` trong `.jtl`, hoặc `time_slices[3].avg_allThreads` trong `summary.json` |
| **Vì sao AI sai** | Nó suy từ mô tả cấu hình chứ không đọc cột `allThreads` trong dữ liệu thật. Đây là ví dụ đắt giá cho *"AI suy luận từ mô tả, không kiểm chứng bằng dữ liệu"* |

#### Loại E — Trung bình che giấu đuôi phân phối

| | |
| :--- | :--- |
| **Dấu hiệu** | AI kết luận "hiệu năng tốt, trung bình chỉ `<<X>>` ms" mà không nhắc p95/p99 |
| **Vì sao là lỗi** | Với phân phối lệch phải điển hình của web, trung bình bị kéo xuống bởi khối request nhanh. `p99` có thể gấp 10–20 lần trung bình. Kết luận dựa trên trung bình bỏ qua đúng nhóm người dùng chịu trải nghiệm tệ nhất |
| **Xác minh** | So `elapsed.avg` với `elapsed.p99` trong `summary.json` — ghi cả tỉ số `p99/avg` |

#### Loại F — Quy nhân quả sai cho nút thắt cổ chai

| | |
| :--- | :--- |
| **Dấu hiệu** | AI nói "`02_BrowseProducts` chậm vì truy vấn cơ sở dữ liệu chậm" |
| **Vì sao có thể sai** | Chưa chắc. Cần tách bạch: `Latency` cao ⇒ chậm ở phía server xử lý; `elapsed − Latency` lớn ⇒ chậm ở khâu truyền payload. Với 505 bản ghi, phần lớn chi phí có thể nằm ở `JSON.stringify` và truyền dữ liệu chứ không phải ở SQLite |
| **Xác minh** | So `latency.avg` với `elapsed.avg`, và đối chiếu `bytes.avg`. Nếu `elapsed − Latency` chiếm phần lớn thì nguyên nhân là payload, không phải truy vấn |
| **Vì sao quan trọng** | Chẩn đoán sai nguyên nhân dẫn thẳng tới đề xuất sai ở §3 (thêm index) |

---

## 3. §3 — Phán quyết đề xuất tối ưu

### 3.1 Thang phân loại

| Nhãn | Nghĩa |
| :--- | :--- |
| **Feasible & effective** | Làm được, và số liệu ủng hộ việc nó sẽ cải thiện đúng nút thắt đã đo |
| **Feasible but ineffective** | Làm được về mặt kỹ thuật, nhưng **không chạm** vào nút thắt thật. Đây là loại nguy hiểm nhất vì nghe rất hợp lý |
| **Hallucinated** | Không áp dụng được với ngăn xếp công nghệ này — AI đề xuất theo phản xạ từ ngữ cảnh khác |
| **Out of scope** | Đúng nhưng vượt xa quy mô bài toán |

### 3.2 Bảng phán quyết — luận cứ đã chuẩn bị sẵn

Điền cột "Số liệu chứng minh" sau khi có kết quả thật.

| # | Đề xuất của AI | Phán quyết | Lý do | Số liệu chứng minh |
| :--: | :--- | :--- | :--- | :--- |
| 1 | Thêm index cho `products.name` (hoặc "đánh index bảng products") | **Feasible but ineffective** | Đường nóng của workflow này là `GET /api/products` **không tham số**, chạy `SELECT * FROM products` **không có mệnh đề WHERE** (`backend/server.js:153`). Truy vấn không lọc thì bộ tối ưu SQLite luôn quét toàn bảng — **không index nào được dùng tới**. Chi phí thật nằm ở việc đọc 505 hàng rồi `JSON.stringify` thành ~150 KB, không nằm ở khâu tìm kiếm.<br><br>*Ghi chú:* trên nhánh có `?search=` (`server.js:144`, `LIKE '%kw%'`) index cũng vô dụng, vì wildcard đứng đầu làm B-tree không dùng được — nhưng nhánh đó **ngoài scope workflow này** | `elapsed − Latency` của `02_BrowseProducts` = `<<FILL>>` ms, chiếm `<<FILL>>` % tổng thời gian ⇒ chi phí ở truyền/serialize, không ở truy vấn |
| 2 | Bật SQLite **WAL** (`PRAGMA journal_mode=WAL`) | **Feasible & effective** | `POST /api/checkout` chạy `INSERT INTO orders` (`server.js:301`). Ở chế độ journal mặc định (`DELETE`), mỗi ghi phải giữ khóa độc quyền toàn cơ sở dữ liệu. WAL cho phép đọc song song với ghi và giảm rõ rệt tranh chấp — đúng loại tải mà `05_Checkout` tạo ra ở bậc VU cao | Số `SQLITE_BUSY` quan sát được: `<<FILL>>`; p95 của `05_Checkout` ở bậc 200 VU = `<<FILL>>` ms so với bậc 25 VU = `<<FILL>>` ms |
| 3 | Dùng **connection pool** cho cơ sở dữ liệu | **Hallucinated** (trong ngữ cảnh này) | Connection pool là khái niệm của cơ sở dữ liệu client-server (PostgreSQL, MySQL), nơi mỗi kết nối là một socket tốn kém. SQLite là **thư viện nhúng thao tác trên file cục bộ**; driver `sqlite3` của Node mở một handle file và tuần tự hóa lệnh nội bộ. Không có "kết nối" để gom vào pool. Đề xuất này là phản xạ từ ngữ cảnh backend thông thường, không phải suy luận từ ngăn xếp đã mô tả trong prompt | Không cần số liệu — sai về mặt kiến trúc |
| 4 | Sửa rò rỉ bộ nhớ ở giỏ hàng | **Feasible & effective** — và là **root cause thật** | `server.js:14` khai báo `const userCarts = {}`; `:293` chỉ `push`; `:297-309` checkout **không** xóa giỏ. Mỗi iteration của mỗi VU thêm vĩnh viễn một phần tử vào heap tiến trình | RSS tăng từ `<<FILL>>` MB lên `<<FILL>>` MB sau 12 phút, tốc độ `<<FILL>>` MB/phút, **không giảm** sau khi tải kết thúc |
| 5 | Phân trang `GET /api/products` | **Feasible & effective** — hiệu quả cao nhất cho workflow này | Cắt thẳng vào chi phí đã đo được: giảm số hàng phải serialize và số byte phải truyền.<br>**Đánh đổi:** thay đổi hợp đồng API, frontend phải sửa theo. Cần bàn với bên phát triển, không phải tối ưu "âm thầm" như WAL | `bytes.avg` của `02_BrowseProducts` = `<<FILL>>` byte/request × `<<FILL>>` request = `<<FILL>>` MB truyền trong một run |
| 6 | Thêm tầng cache Redis | **Out of scope** | Đúng về nguyên tắc với dữ liệu catalog ít thay đổi, nhưng thêm một dịch vụ ngoài vào một ứng dụng demo chạy trên máy cá nhân là chi phí vận hành lớn hơn nhiều so với lợi ích. Cache trong tiến trình (`Map` + TTL) đạt phần lớn lợi ích với chi phí gần bằng không | — |
| 7 | *(nếu AI đề xuất thêm)* | | | |

> **Đừng chép nguyên bảng này.** Chỉ giữ những dòng tương ứng với đề xuất AI **thực sự** đưa ra. Nếu AI không nhắc tới WAL thì không được có dòng WAL — báo cáo phải phản ánh phiên làm việc thật.
>
> Nếu AI đề xuất thứ không có trong bảng, tự phân loại theo thang §3.1 và viết luận cứ tương tự.

### 3.3 Vì sao mục 1 và 3 là điểm sáng của bài này

Cả hai đều là đề xuất **nghe rất chuyên nghiệp**. "Thêm index" và "dùng connection pool" là lời khuyên đúng trong 90 % hệ thống backend. Chúng sai ở đây vì hai chi tiết cụ thể của ngăn xếp: truy vấn không có `WHERE`, và cơ sở dữ liệu là thư viện nhúng.

Đây chính là điều đề bài muốn sinh viên chứng minh: **AI đưa ra lời khuyên đúng-thống-kê nhưng sai-ngữ-cảnh, và chỉ người đã đọc mã nguồn mới bác được.**

---

## 4. §4 — Kết luận

Trả lời ba câu, mỗi câu 2–4 câu văn:

1. **Mẫu sai của AI là gì?** Nó sai ngẫu nhiên hay sai có hệ thống? (Gợi ý từ §2 và §3: các lỗi có xu hướng đến từ việc **suy luận theo mẫu phổ biến thay vì kiểm chứng bằng dữ liệu/mã nguồn cụ thể**.)
2. **Điều gì khiến nó không tự phát hiện?** (AI không có quyền truy cập file `.jtl` gốc mà chỉ nhận bản tóm tắt; nó không chạy được truy vấn để tự kiểm chứng; và nó không có phản hồi từ hệ thống thật.)
3. **Lần sau mình sẽ dùng AI khác đi thế nào?** Nêu một quy tắc **cụ thể và kiểm chứng được**, không nói chung chung "cần review kỹ hơn".
   Ví dụ: *"Với mọi nhận định định lượng của AI, tôi sẽ yêu cầu nó nêu rõ tên cột dữ liệu mà nó dùng để rút ra con số đó. Nhận định nào không chỉ được cột nguồn thì tôi coi là chưa được kiểm chứng và tự tính lại."*

---

## 5. Checklist

- [ ] §1 dán output AI **nguyên văn**, cả 3 prompt A/B/C
- [ ] §2 có **≥ 3** lỗi diễn giải thật, mỗi lỗi có **giá trị đúng trích từ `.jtl`**
- [ ] Mỗi lỗi kèm **lệnh tái lập được** để xác minh
- [ ] §3 phân loại **mọi** đề xuất AI đưa ra, không bỏ sót cái nào
- [ ] Có ít nhất một **"feasible but ineffective"** và một **"hallucinated"**, kèm luận cứ từ mã nguồn
- [ ] Mọi `<<FILL>>` đã điền bằng số thật
- [ ] §4 có quy tắc cụ thể, kiểm chứng được — không phải "cần cẩn thận hơn"
- [ ] Không chép nguyên các dòng mẫu ở §3.2 mà AI không thực sự đề xuất
