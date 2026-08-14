# 02 — AI Generation Log: Step-by-Step Test Plan Design

> **Sinh viên:** Khoa (MSSV: **23127207**) · **Branch:** `HW5`  
> **Nhiệm vụ:** Dẫn dắt AI từng bước thiết kế bộ Test Plan theo đúng phương pháp luận kiểm thử hiệu năng.  
> **Công cụ AI sử dụng:** Gemini 3.7 Flash / Claude 3.5 Sonnet  
> **Thời gian thực hiện:** 2026-08-14 13:50–14:20 (+07:00)  

---

## 1. Tuyên bố và Nguyên tắc Dẫn dắt

Tuân thủ nghiêm ngặt yêu cầu §2 của đề bài (*"this does not mean issuing a single, generic prompt... Instead, you must guide the AI through every step of the technique as it was taught, using the AI as a disciplined assistant rather than a black box"*). Quá trình sinh test plan được chia thành 7 bước có thứ tự logic và có sự can thiệp, phản biện của người kỹ sư kiểm thử.

---

## 2. Nhật ký 7 Bước Tương tác Chi tiết

### Bước 1: Phân tích Endpoint và Chốt Workflow
- **Thời gian:** 2026-08-14 13:52 (+07:00)
- **Prompt:**
  ```text
  Tôi đang làm bài tập kiểm thử hiệu năng trên một hệ thống e-commerce demo tên EShop (Node.js + Express + SQLite, chạy ở http://localhost:3000).
  Ràng buộc quan trọng: nhóm tôi có 5 người, mỗi người phải chọn MỘT workflow end-to-end khác nhau, không được trùng. Workflow của tôi tên là "Browse-to-buy": người dùng đăng nhập, xem TOÀN BỘ danh sách sản phẩm (KHÔNG dùng chức năng tìm kiếm — endpoint search đã thuộc về bạn khác trong nhóm), xem chi tiết một sản phẩm, thêm vào giỏ, rồi thanh toán.
  Nhiệm vụ bước này: liệt kê chính xác các HTTP request tạo nên workflow đó, mỗi request ghi rõ method, path, header, body. Với mỗi request, phân loại nó thuộc nhóm nào trong ba nhóm mà đề bài yêu cầu: auth-heavy, read-heavy, transactional.
  Chưa cần viết file JMeter. Chỉ cần bảng phân tích.
  ```
- **Output của AI:**
  > Bảng phân tích 5 request:
  > 1. `POST /api/login` (Auth-heavy) — body: `{email, password}`
  > 2. `GET /api/products` (Read-heavy) — không query string
  > 3. `GET /api/products/:id` (Read-heavy) — lấy id từ catalog
  > 4. `POST /api/cart` (Transactional) — header: `Authorization: Bearer <token>`, body: `{product_id, quantity, name, price}`
  > 5. `POST /api/checkout` (Transactional) — header: `Authorization: Bearer <token>`, body: `{total_amount, shipping_address}`
- **Đánh giá & Can thiệp của Người:** AI xác định đúng 5 endpoint và phân loại chuẩn 3 nhóm. Người kỹ sư xác nhận không có endpoint `search`, `categories`, hay `apply-coupon` bị lẫn vào.

---

### Bước 2: Đọc Mã nguồn SUT Tìm Đặc thù Cài đặt
- **Thời gian:** 2026-08-14 13:57 (+07:00)
- **Prompt:**
  ```text
  Đây là mã nguồn xử lý của các endpoint trên (backend/server.js: login, products, cart, checkout, authenticateToken).
  Nhiệm vụ: đọc kỹ và chỉ ra những đặc điểm CÀI ĐẶT có thể ảnh hưởng tới thiết kế test hiệu năng hoặc tới việc đặt assertion. Tôi quan tâm đặc biệt tới:
  - cơ chế khóa tài khoản khi đăng nhập sai
  - endpoint nào có thể trả HTTP 200 nhưng thực chất không thành công
  - nơi lưu trạng thái giỏ hàng
  - điểm nào có thể trở thành nút thắt cổ chai khi nhiều luồng chạy đồng thời
  Với mỗi phát hiện, trích số dòng cụ thể.
  ```
- **Output của AI:**
  > 1. **Lockout:** `server.js:54` tăng `login_attempts += 2`, và `server.js:57` khóa 180,000ms (3 phút) nếu $\ge 3$. Tức 2 lần sai liên tiếp là khóa 3 phút (khác với spec FR-02 ghi 3 lần / 30s).
  > 2. **Trả 200 khi rỗng:** `server.js:161` nếu không tìm thấy product id thì trả `res.status(200).json({})`.
  > 3. **Ép kiểu string:** `server.js:162` nếu product id chẵn thì `row.price = row.price.toString()`.
  > 4. **Giỏ hàng in-memory:** `server.js:14` khai báo `userCarts = {}`, `server.js:293` `push` vào mảng, `server.js:297-309` checkout không xóa giỏ $\to$ Memory leak tích lũy trong Node heap.
  > 5. **Nút thắt SQLite:** `server.js:301` `INSERT INTO orders` chạy trên SQLite đơn luồng ghi, dễ gây `SQLITE_BUSY` ở concurrency cao.
- **Đánh giá & Can thiệp của Người:** Phát hiện rất chính xác các bug cố ý và cơ chế SUT. Người kỹ sư ghi chú: Assertion phải kiểm tra nội dung object thay vì chỉ kiểm tra status 200; và cần script reset lockout định kỳ giữa các run.

---

### Bước 3: Đề xuất Tham số Tải cho 4 Kịch bản
- **Thời gian:** 2026-08-14 14:02 (+07:00)
- **Prompt:**
  ```text
  Dựa trên workflow đã chốt ở bước 1 và các đặc thù cài đặt ở bước 2, hãy đề xuất tham số cho ba kịch bản Load, Stress, Spike, và một kịch bản Endurance/soak.
  Với mỗi kịch bản, cho tôi: số thread, ramp-up, thời lượng, và think time cho từng bước trong workflow.
  Ràng buộc:
  - SUT là tiến trình Node.js đơn luồng chạy CÙNG MÁY với JMeter (Intel Core i7-1260P, 16GB RAM). Tham số phải thực tế với phần cứng này.
  - Think time phải mô phỏng người dùng THẬT đang duyệt catalog, không được bằng 0.
  - Kịch bản Endurance phải kéo dài 10-15 phút theo yêu cầu đề bài.
  Giải thích lý do cho từng con số.
  ```
- **Output của AI:**
  > Ban đầu AI đề xuất Load 100 VU không có timer (think time = 0) và ramp-up 5s.
- **Đánh giá & Can thiệp của Người (Quan trọng):**
  - **Phản biện & Sửa lỗi:** Think time = 0 sẽ biến Load test thành DoS test và làm tê liệt JMeter trên máy chạy chung.
  - **Yêu cầu AI sửa:**
    - Load: 50 VU, ramp-up 60s, duration 300s (5 phút). Think time: 1-2s (login), 2-4s (browse catalog), 1-2s (detail), 1s (cart).
    - Stress: 4 bậc thang (25 $\to$ 50 $\to$ 100 $\to$ 200 VU), mỗi bậc 2 phút = 8 phút tổng.
    - Spike: Baseline 10 VU + 2 đợt sốc 300 VU (ramp 5s, giữ 30s tại phút thứ 1 và phút thứ 4).
    - Endurance: 30 VU $\times$ 12 phút (720s) để đo memory leak và trần bộ nhớ.

---

### Bước 4: Thiết kế Assertions & Correlation
- **Thời gian:** 2026-08-14 14:08 (+07:00)
- **Prompt:**
  ```text
  Với 5 request của workflow, hãy thiết kế:
  (a) các giá trị cần trích xuất từ response để dùng cho request sau (correlation)
  (b) các assertion cho từng request
  Lưu ý không được chỉ kiểm tra response code 200.
  ```
- **Output của AI:**
  > - `01_Login`: JSON Extractor `$.token` $\to$ `token`, `$.user.id` $\to$ `user_id`. Assert `$.token` exists.
  > - `02_BrowseProducts`: JSON Extractor `$..id` với Match No = 0 $\to$ `pid`. Assert Regex `^\[.*\]$`.
  > - `03_ProductDetail`: Assert Response code 200 kèm JSON Assertion `$.name` và `$.price`.
  > - `04_AddToCart`: Assert text contains `Added to cart`.
  > - `05_Checkout`: JSON Extractor `$.orderId` $\to$ `order_id`. Assert `$.orderId` exists.
- **Đánh giá & Can thiệp của Người:** Đồng ý thiết kế. Bổ sung giá trị mặc định cho `pid` là `${product_id}` từ CSV để có cơ chế fallback an toàn nếu bước 2 parse lỗi.

---

### Bước 5: Thiết kế Schema Dữ liệu CSV & Cấu hình CSV Data Set
- **Thời gian:** 2026-08-14 14:12 (+07:00)
- **Prompt:**
  ```text
  Workflow này phải data-driven bằng file CSV. Hãy thiết kế schema CSV: tên cột, kiểu dữ liệu, cột nào dùng ở request nào, và ví dụ 3 dòng.
  Ràng buộc:
  - Kịch bản Spike cần tới 310 luồng đồng thời.
  - Backend khóa tài khoản sau khi đăng nhập sai, nên nhiều luồng KHÔNG được dùng chung một tài khoản.
  - Địa chỉ giao hàng có chứa dấu phẩy.
  Cấu hình CSV Data Set Config trong JMeter cần đặt thế nào để mỗi luồng nhận một dòng khác nhau?
  ```
- **Output của AI:**
  > Schema: `email,password,product_id,quantity,price,total_amount,shipping_address`
  > Cấu hình JMeter:
  > - `Sharing mode`: **All threads** (để mỗi thread nhận 1 dòng độc lập).
  > - `Recycle on EOF`: `true`.
  > - `Stop thread on EOF`: `false`.
  > - `Allow quoted data`: `true` (xử lý dấu phẩy trong địa chỉ `"12 Nguyen Van Cu, Q5, TP.HCM"`).
- **Đánh giá & Can thiệp của Người:** Hoàn toàn chính xác. Yêu cầu tạo 400 user tương ứng trong database để phục vụ pool 310 VU của Spike.

---

### Bước 6: Sinh File `.jmx` Hoàn chỉnh
- **Thời gian:** 2026-08-14 14:15 (+07:00)
- **Prompt:**
  ```text
  Hãy thiết lập định dạng XML .jmx cho 4 file:
  1. 23127207_Load_20260814.jmx (Aggregate Report)
  2. 23127207_Stress_20260814.jmx (Summary Report, Test Fragment + 4 Module Controllers)
  3. 23127207_Spike_20260814.jmx (View Results Tree errors only, 3 Thread Groups)
  4. 23127207_Endurance_20260814.jmx (Aggregate Report, 720s)
  Chỉ dùng core element chuẩn của Apache JMeter 5.6.3.
  ```
- **Output của AI:**
  > Sinh cấu trúc cây Test Plan, HTTP Defaults, Header Manager, CSV Config, Thread Groups, và các Listener tương ứng.
- **Đánh giá & Can thiệp của Người:** Kiểm tra và đảm bảo không dùng bất kỳ third-party plugin nào (`jpgc`), đảm bảo file XML mở được 100% trên JMeter GUI của TA.

---

### Bước 7: Tự Rà soát và Liệt kê Giả định Rủi ro
- **Thời gian:** 2026-08-14 14:18 (+07:00)
- **Prompt:**
  ```text
  Hãy tự rà soát file .jmx vừa sinh và liệt kê những điểm bạn KHÔNG chắc chắn hoặc những giả định cần người kỹ sư tự kiểm chứng lại trước khi chạy tải thật.
  ```
- **Output của AI:**
  > 1. Giả định biến `${__P(csvdir)}` được truyền từ CLI. Nếu không truyền, đường dẫn CSV sẽ lỗi.
  > 2. Giả định cơ sở dữ liệu đã seed đủ 400 tài khoản `khoa001` .. `khoa400`. Nếu chạy trên DB mặc định (chỉ có 2 user), 100% thread sẽ fail login và dính lockout.
  > 3. Giả định máy đo có đủ RAM cấp heap cho JMeter (`-Xms1g -Xmx4g`).
- **Đánh giá & Can thiệp của Người:** Đây là các giả định hoàn toàn chuẩn xác. Người kỹ sư đã chuẩn bị script `seed_perf_data.js` và cấu hình `-Jcsvdir` trong script thực thi.

---

## 3. Tổng kết Hiệu quả Dẫn dắt AI
Quá trình 7 bước đã biến AI từ một công cụ sinh code chung chung thành một trợ lý đắc lực, bám sát từng đặc thù cài đặt của SUT và các ràng buộc học thuật của môn học. Mọi quyết định kỹ thuật cuối cùng đều do người kỹ sư kiểm định và làm chủ.
