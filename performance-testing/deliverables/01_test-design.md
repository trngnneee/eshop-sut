# 01 — Test Design: Browse-to-buy Workflow

> **Học phần:** Kiểm thử Phần mềm (HW05 – Performance Testing)  
> **Hệ thống kiểm thử (SUT):** EShop (Node.js Express + SQLite)  
> **Sinh viên thực hiện:** Khoa (MSSV: **23127207**) · **Branch:** `HW5`  
> **Workflow:** **Browse-to-buy**  

---

## 1. Phân định Scope và Ranh giới Kiểm thử Nhóm

Theo yêu cầu mục §5 của đề bài (*"ensure that your selection is not duplicated among the members of your group: no two members may test the same workflow"*), nhóm 5 thành viên đã phân chia ma trận workflow độc lập.

### 1.1 Ranh giới của Workflow Browse-to-buy (MSSV 23127207)
Workflow bao gồm **đúng 5 HTTP request**, phủ trọn vẹn 3 nhóm endpoint bắt buộc:

| # | Bước | Endpoint | Phương thức | Nhóm Endpoint | Mục đích kỹ thuật |
|:---:|:---|:---|:---:|:---|:---|
| 1 | `01_Login` | `/api/login` | `POST` | **Auth-heavy** | Xác thực người dùng, nhận JWT token, kiểm tra áp lực xác thực và cơ chế ghi `login_attempts` |
| 2 | `02_BrowseProducts` | `/api/products` | `GET` | **Read-heavy** | Duyệt toàn bộ danh mục sản phẩm (*không dùng search query*), đo chi phí quét bảng và serialize JSON toàn bộ catalog |
| 3 | `03_ProductDetail` | `/api/products/${pid}` | `GET` | **Read-heavy** | Truy vấn chi tiết một sản phẩm theo khóa chính được chọn ngẫu nhiên từ catalog |
| 4 | `04_AddToCart` | `/api/cart` | `POST` | **Transactional** | Ghi thông tin sản phẩm vào giỏ hàng in-memory của tiến trình (`userCarts`), tạo tải bộ nhớ RAM (heap) |
| 5 | `05_Checkout` | `/api/checkout` | `POST` | **Transactional** | Thanh toán đơn hàng, ghi nhận đơn vào SQLite (`orders`), tạo tranh chấp khóa file cơ sở dữ liệu |

### 1.2 Các Endpoint Tuyệt đối NẰM NGOÀI Scope (Excluded Endpoints)
Để đảm bảo không trùng lặp với các thành viên khác, các endpoint sau **không bao giờ xuất hiện** trong bất kỳ kịch bản nào của bài thi này:
- `GET /api/products?search=` (Thuộc Trâm, Nguyên, Thịnh)
- `GET /api/categories` (Thuộc Nguyên)
- `POST /api/apply-coupon` (Thuộc Thịnh)
- `GET /api/orders/my-orders` (Thuộc Bảo)
- Mọi endpoint `/api/admin/*`, `/api/register`, `/api/forgot-password`.

---

## 2. Thiết kế Từng Bước Workflow Chi tiết

### 2.1 Luận cứ Think Time Thực tế
Không áp dụng `think_time = 0` vì sẽ biến mọi kịch bản thành stress test phi thực tế và làm nghẽn máy đo JMeter. Hệ thống áp dụng **Uniform Random Timer** mô phỏng hành vi duyệt web tự nhiên:

- **Sau Bước 1 (`01_Login`):** `1–2 s` (Offset 1000ms, Random 1000ms) — người dùng vừa đăng nhập, chờ giao diện trang chính hiển thị và định hình hành động tiếp theo.
- **Sau Bước 2 (`02_BrowseProducts`):** `2–4 s` (Offset 2000ms, Random 2000ms) — điểm khác biệt then chốt của Browse-to-buy so với Search-to-buy: người dùng duyệt lướt danh mục sản phẩm cần thời gian cuộn trang và xem ảnh trước khi chọn một món đồ. Khoảng dừng này cũng giảm nhịp gọi dồn dập vào endpoint nặng nhất của hệ thống.
- **Sau Bước 3 (`03_ProductDetail`):** `1–2 s` (Offset 1000ms, Random 1000ms) — đọc thông tin mô tả chi tiết, kiểm tra giá và chọn số lượng.
- **Sau Bước 4 (`04_AddToCart`):** `1–1.5 s` (Offset 1000ms, Random 500ms) — thao tác chuyển từ giỏ hàng sang màn hình xác nhận thanh toán.
- **Sau Bước 5 (`05_Checkout`):** `0 s` — hoàn tất 1 vòng lặp (iteration).

Tổng think time trung bình ~`5–9.5 s` mỗi iteration. Ở trạng thái nhàn, mỗi Virtual User sinh ra khoảng `6–8 iteration/phút`.

### 2.2 Cơ chế Correlation & Data-Driven 2 Cấp
Workflow được tham số hóa linh hoạt và chống gãy bằng cơ chế 2 cấp:
1. **Cấp 1 — Dữ liệu tĩnh từ CSV (`khoa_users.csv`):** Cung cấp tài khoản độc lập (`email`, `password`), số lượng (`quantity`), giá tham chiếu (`price`), tổng tiền (`total_amount`), và địa chỉ giao hàng (`shipping_address`).
2. **Cấp 2 — Trích xuất động từ Response:** Bước 2 dùng **JSON Extractor** với JSONPath `$..id` và `Match No. = 0` (chọn ngẫu nhiên 1 ID sản phẩm từ danh sách 505 sản phẩm vừa duyệt). Nếu bước 2 gặp sự cố, fallback dự phòng sẽ lấy `${product_id}` từ CSV để bước 3 và 4 vẫn có dữ liệu hợp lệ.

### 2.3 Thiết kế Assertion Kiểm soát Lỗi Ngầm
Do SUT có các lỗi cố ý trong mã nguồn, assertion không được dừng ở `Response Code 200`:
- **`01_Login`:** Kiểm tra Response Code `200` và JSON Assertion trường `$.token` tồn tại khác rỗng.
- **`02_BrowseProducts`:** Kiểm tra Response Code `200` và Response Assertion Regex `^\s*\[[\s\S]*\]\s*$` xác nhận payload trả về là JSON Array hợp lệ.
- **`03_ProductDetail`:** Kiểm tra Response Code `200` kèm JSON Assertion trường `$.name` và `$.price` phải tồn tại. *(Tránh bẫy `server.js:161` trả 200 kèm `{}` khi id không tồn tại).*
- **`04_AddToCart`:** Kiểm tra Response Code `200` và Body chứa chuỗi `Added to cart`.
- **`05_Checkout`:** Kiểm tra Response Code `200` và JSON Assertion trường `$.orderId` phải tồn tại dạng số.

---

## 3. Ma trận 4 Kịch bản Tải (Load Profiles)

Cả 4 kịch bản đều thực thi **cùng một workflow 5 bước**, chỉ khác cấu hình tải và Listener:

| Kịch bản | Mục tiêu chính | Cấu hình Virtual Users (VU) | Ramp-up | Thời lượng | Listener & Report View |
|:---|:---|:---|:---:|:---:|:---|
| **Load** | Đo đạc hiệu năng ở mức tải kỳ vọng chuẩn | 50 VU | 60 s | 300 s (5 phút) | **Aggregate Report** |
| **Stress** | Xác định điểm gãy (knee point) và giới hạn bão hòa | 4 Thread Group xếp bậc: 25 $\to$ 50 $\to$ 100 $\to$ 200 VU | mỗi bậc 30 s | 480 s (8 phút, 4 bậc $\times$ 2 phút) | **Summary Report** |
| **Spike** | Đo khả năng chịu xung tải đột biến và năng lực phục hồi | Baseline 10 VU (360 s) + 2 đợt sốc 300 VU (delay 60s & 240s, dur 30s) | 5 s | 360 s (6 phút) | **View Results Tree** (*Errors only*) |
| **Endurance** | Đo mức độ ổn định dài hạn và tìm memory leak | 30 VU | 60 s | 720 s (12 phút) | **Aggregate Report** |

---

## 4. Ngưỡng Chất lượng Kỳ vọng (SLO Baseline)
*Thiết lập trước khi chạy tải thực tế để đánh giá khách quan:*

1. **p95 `02_BrowseProducts`:** $\le 800\text{ ms}$ (endpoint nặng nhất do payload catalog).
2. **p95 `03_ProductDetail`:** $\le 300\text{ ms}$ (truy vấn điểm theo khóa chính).
3. **p95 `05_Checkout`:** $\le 1000\text{ ms}$ (ghi I/O đĩa SQLite).
4. **Error Rate (Load test):** $\le 0.1\%$.
5. **Throughput trung bình (Load test):** $\ge 25\text{ req/s}$.

---

## 5. Giới hạn Phương pháp Luận (Methodological Limitations)

Khi đánh giá kết quả, các yếu tố kỹ thuật sau cần được công nhận minh bạch:
1. **Chạy cùng máy vật lý (Co-located SUT & JMeter):** JMeter và Node.js server chạy chung trên cùng một máy, do đó ở tải cực cao (Spike 310 VU, Stress 200 VU) tải CPU của JMeter sẽ cạnh tranh với backend. Việc chạy chế độ Non-GUI (`jmeter -n`) là bắt buộc để giảm thiểu tối đa hiện tượng này.
2. **Độ trễ mạng Loopback (No Network Latency):** Tất cả request đi qua `localhost` nên thời gian bắt tay TCP và truyền tải mạng là cận dưới lý tưởng; môi trường production thực tế sẽ có latency mạng cao hơn.
3. **Đặc tính Khóa File của SQLite:** SQLite tuần tự hóa các lệnh ghi (`exclusive lock` khi checkout). Kết quả phản ánh bản chất của SQLite, không suy rộng cho MySQL/PostgreSQL.
4. **Quy mô Catalog Đã Seed Thêm 500 Sản phẩm:** Bộ dữ liệu gồm 505 sản phẩm (~150KB JSON mỗi lần browse) làm tăng đáng kể chi phí serialize so với DB mặc định (5 sản phẩm).
5. **Giỏ hàng In-Memory không giải phóng:** Biến `userCarts` trong `server.js` không có cơ chế TTL hay cleanup sau checkout, dẫn đến heap memory tăng liên tục theo thời gian.
