# 00 — GROUP SCOPE (Chốt phạm vi nhóm)

> **Mục đích:** Chứng minh yêu cầu §5 của đề — *"ensure that your selection is not duplicated among the members of your group: no two members may test the same workflow."*
> **Đồng thời là hàng rào chống lệch scope cho người/agent thi công.**

---

## 1. Quy tắc chung của đề

| Nhóm endpoint | Ý nghĩa (theo đề §5) |
| :--- | :--- |
| **Auth-heavy** | Login, có tính đến hành vi account lockout |
| **Read-heavy** | Product listing / search / detail |
| **Transactional** | Add-to-cart → checkout / order |

Mỗi thành viên chọn **một** end-to-end workflow phủ đủ 3 nhóm, rồi chạy **cùng workflow đó** cho cả 3 kịch bản **Load / Stress / Spike** — chỉ đổi tham số tải (threads, ramp-up, think-time).

Tên test plan: `{MSSV}_{Load|Stress|Spike}_{YYYYMMDD}`.

---

## 2. Phân công 5 thành viên

| # | Thành viên | Workflow | Điểm khác biệt chính |
| :---: | :--- | :--- | :--- |
| 1 | Võ Ngọc Bích Trâm (23127271) | **Search-to-buy** | Search → detail → cart → checkout |
| 2 | **Khoa (23127207)** ← *bài này* | **Browse-to-buy** | **List all products** → detail → cart → checkout |
| 3 | Nguyên | **Category-guided buy** | Categories → search → cart → checkout |
| 4 | Thịnh | **Coupon checkout** | Search → detail → cart → **apply-coupon** → checkout |
| 5 | Bảo | **Buy-then-history** | List → detail → cart → checkout → **my-orders** |

---

## 3. Ma trận endpoint × thành viên

| Endpoint | Trâm | **Khoa** | Nguyên | Thịnh | Bảo |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `POST /api/login` | ✓ | **✓** | ✓ | ✓ | ✓ |
| `GET /api/products` (full list) | | **✓** | | | ✓ |
| `GET /api/products?search=` | ✓ | | ✓ | ✓ | |
| `GET /api/products/{id}` | ✓ | **✓** | | ✓ | ✓ |
| `GET /api/categories` | | | ✓ | | |
| `POST /api/cart` | ✓ | **✓** | ✓ | ✓ | ✓ |
| `POST /api/apply-coupon` | | | | ✓ | |
| `POST /api/checkout` | ✓ | **✓** | ✓ | ✓ | ✓ |
| `GET /api/orders/my-orders` | | | | | ✓ |

**Kết luận:** chuỗi bước của 5 workflow khác nhau → thỏa *"no two members may test the same workflow"*.

Cặp gần nhau nhất là **Khoa** và **Bảo** (cùng dùng `GET /api/products` full list). Phân biệt:
- **Khoa** dừng ở `checkout`, trọng tâm là **chi phí đọc toàn bộ catalog** dưới tải cao.
- **Bảo** có thêm bước `GET /api/orders/my-orders` sau checkout, trọng tâm là **đọc-sau-ghi** khi bảng `orders` phình.

---

## 4. SCOPE CỦA KHOA (23127207) — Browse-to-buy

### 4.1 TRONG scope — đúng 5 request, không hơn không kém

| # | Request | Nhóm endpoint |
| :---: | :--- | :--- |
| 1 | `POST /api/login` | **auth-heavy** |
| 2 | `GET /api/products` *(không query string)* | **read-heavy** |
| 3 | `GET /api/products/{id}` | **read-heavy** |
| 4 | `POST /api/cart` | **transactional** |
| 5 | `POST /api/checkout` | **transactional** |

### 4.2 NGOÀI scope — TUYỆT ĐỐI KHÔNG đưa vào `.jmx`

| Endpoint | Thuộc về | Ghi chú |
| :--- | :--- | :--- |
| `GET /api/products?search=` | Trâm, Nguyên, Thịnh | ⚠️ **Bẫy phổ biến nhất.** AI/agent rất hay tự thêm `?search=` vì đó là mẫu quen thuộc. Bước 2 phải là `GET /api/products` **trần** |
| `GET /api/categories` | Nguyên | |
| `POST /api/apply-coupon` | Thịnh | |
| `GET /api/orders/my-orders` | Bảo | |
| `POST /api/register` | — | Ngoài scope HW05 của Khoa |
| `POST /api/forgot-password`, `POST /api/reset-password` | — | |
| `GET/PUT /api/users/me` | — | |
| `PUT /api/orders/{id}/cancel`, `GET /api/orders/{id}` | — | |
| Mọi `/api/admin/*` | — | |
| Mọi `POST/PUT/DELETE /api/products`, `/api/categories`, `/api/coupons` | — | |

> **Kiểm tra tự động trước khi commit `.jmx`:**
> ```powershell
> Select-String -Path "performance-testing\test-plans\*.jmx" `
>   -Pattern "search=|apply-coupon|my-orders|/api/categories|/api/admin|/api/register"
> ```
> Lệnh này **phải không trả về kết quả nào**.

### 4.3 Điểm nhấn báo cáo của Khoa

`GET /api/products` không có query → backend chạy `SELECT * FROM products` **không WHERE** (`backend/server.js:153`), tức là:
- Luôn full table scan, không index nào giúp được.
- Serialize **toàn bộ** catalog thành JSON ở mỗi request → payload và CPU tăng tuyến tính theo số sản phẩm.

Đây là khác biệt cốt lõi so với nhánh search của Trâm (trả về tập con). Báo cáo phải khai thác điểm này khi phân tích threshold và khi phản biện đề xuất "thêm index" của AI.

### 4.4 Cột CSV — hai phương án chọn sản phẩm

Bản phân công nhóm ghi cột của Khoa là `product_index_or_id`, tức cho phép hai cách:

| Phương án | Cột CSV | Cách hoạt động | Đánh giá |
| :--- | :--- | :--- | :--- |
| **A — `product_id` cố định** *(đang dùng)* | `product_id` | Lấy thẳng id từ CSV | Đơn giản, tái lập được. Nhưng nếu chỉ dùng cách này thì bước 2 chỉ là "gọi cho có", response không được dùng |
| **B — `product_index` động** | `product_index` | Trích phần tử thứ N từ response của bước 2 | **Data-driven hơn**: buộc phải thực sự đọc kết quả duyệt catalog |

**Quyết định:** dùng **cả hai theo hai tầng** — JSON Extractor `$..id` với `Match No. = 0` (chọn ngẫu nhiên từ response bước 2) làm tầng chính, `${product_id}` từ CSV làm `Default Value` dự phòng. Chi tiết ở `04_JMX_BUILD_SPEC.md` §5.

Cách này đạt mục tiêu "data-driven hơn" của phương án B mà vẫn không gãy khi bước 2 lỗi. Trong báo cáo nêu rõ workflow được tham số hóa ở **hai cấp**: dữ liệu tĩnh từ CSV và correlation động từ response.

---

## 5. Quy ước chung cả nhóm (áp dụng cho Khoa)

### 5.1 Auth & lockout

- Happy path: `POST /api/login` với email/password đúng → lấy `token`.
- Các request sau login gắn header `Authorization: Bearer ${token}`.
- **Spec FR-02** (`README.md`): sai ≥ 3 lần → khóa ~30 giây.
- **Implementation thật** (`backend/server.js:54,57`): mỗi lần sai `login_attempts += 2`, khóa ~**180 giây**.
  → Tức là **2 lần sai liên tiếp đã bị khóa 3 phút**. Thiết kế Stress/Spike phải theo **hành vi thật**, không theo spec.
- Giữa các lần chạy Stress/Spike: **reset lockout** (chờ hết `locked_until`, hoặc chạy `scripts/reset_lockout.js`) và **ghi lại bước reset trong báo cáo** (đề §6 yêu cầu tường minh).
- **Mỗi người dùng bộ user CSV riêng.** Khoa dùng tiền tố `khoa` (`khoa001@eshop.com` … `khoa400@eshop.com`), **không** dùng chung `test@eshop.com`.

### 5.2 Assertion tối thiểu

| Bước | Kỳ vọng | Ai dùng |
| :--- | :--- | :--- |
| Login OK | HTTP 200, JSON có `token` | cả 5 |
| Login fail / locked | 401 hoặc 403 (chỉ ghi nhận khi cố tình probe lockout) | cả 5 |
| Read APIs | HTTP 200, body là JSON array/object hợp lệ | cả 5 |
| Cart | HTTP 200, có message thành công | cả 5 |
| Checkout | HTTP 200, có `orderId` | cả 5 |
| Coupon | HTTP 200, `success: true`, có `final_amount` | Thịnh |
| My-orders | HTTP 200, array; sau checkout phải thấy order mới | Bảo |

### 5.3 CSV & evidence

- Data-driven bằng CSV (1 hoặc nhiều file).
- **Ba loại listener/report khác nhau** trên bộ 3 plan Load/Stress/Spike — không lặp loại.
- Soak ~10–15 phút.
- Chụp tool + Task Manager + hardware; video demo ≥ 6 phút tiếng Việt.

---

## 6. Payload tham chiếu backend (đã đối chiếu `backend/server.js`)

### `POST /api/login`
```http
POST /api/login
Content-Type: application/json

{ "email": "khoa001@eshop.com", "password": "Test1234!" }
```
Response 200: `{ "message": "Login successful", "token": "...", "user": { "id": 3, ... } }`

### `GET /api/products`
```http
GET /api/products
```
Response 200: JSON array **toàn bộ** sản phẩm. Không truyền `search`.

### `GET /api/products/{id}`
```http
GET /api/products/7
```
Response 200: object sản phẩm.
⚠️ Hai bẫy đã xác nhận trong code:
- `server.js:161` — id không tồn tại vẫn trả **`200` với body `{}`**, không phải 404.
- `server.js:162` — nếu `id` **chẵn**, trường `price` bị ép thành **string**.
→ Assertion không được chỉ kiểm `response code`.

### `POST /api/cart`
```http
POST /api/cart
Authorization: Bearer <token>
Content-Type: application/json

{ "product_id": 7, "quantity": 1, "name": "...", "price": 100000 }
```
*(Backend `push` nguyên `req.body` vào giỏ in-memory — `server.js:293` — nên field linh hoạt; giữ ổn định theo CSV.)*

### `POST /api/checkout`
```http
POST /api/checkout
Authorization: Bearer <token>
Content-Type: application/json

{ "total_amount": 100000, "shipping_address": "..." }
```
Response 200: `{ "message": "Checkout successful", "orderId": 12 }`

---

## 7. Chi tiết workflow từng thành viên

> Chép từ bản phân công nhóm, đã đối chiếu lại với `backend/server.js`.
> Mục đích: chứng minh 5 chuỗi bước khác nhau, và làm tài liệu tham chiếu chung khi nhóm rà soát chéo.
> **Khoa chỉ thi công mục 7.2.** Bốn mục còn lại là ngữ cảnh, không phải việc phải làm.

### 7.1 Trâm (23127271) — Search-to-buy

Mô phỏng user đã có tài khoản: đăng nhập → tìm sản phẩm → xem chi tiết → thêm giỏ → thanh toán.

| Nhóm | Endpoint |
| :--- | :--- |
| Auth-heavy | `POST /api/login` |
| Read-heavy | `GET /api/products?search={q}` → `GET /api/products/{id}` |
| Transactional | `POST /api/cart` → `POST /api/checkout` |

```
1. POST /api/login                 extract: token, user.id      think: 1–2s
2. GET  /api/products?search=${search}
                                   extract: product id (JSONPath) HOẶC từ CSV
                                                                think: 1–3s
3. GET  /api/products/${product_id}   assert: 200, có name/price think: 1–2s
4. POST /api/cart      (+ Bearer)  body: product_id, quantity, name, price
                                                                think: 1s
5. POST /api/checkout  (+ Bearer)  assert: 200 + orderId
```

**CSV:** `email,password,search,product_id,quantity,price,total_amount,shipping_address`

```csv
email,password,search,product_id,quantity,price,total_amount,shipping_address
tram01@eshop.com,Test1234!,Laptop,2,1,15000000,15000000,"123 Nguyen Hue, Q1"
tram02@eshop.com,Test1234!,iPhone,1,1,20000000,20000000,"45 Le Loi, Q3"
```

**Lockout:** Load chỉ login đúng. Stress/Spike nếu có bước fail login có chủ đích thì dùng user riêng và reset giữa run. Không tái dùng một user cho hàng trăm thread khi pool credential chưa đủ lớn.

**Ngoài scope:** register, forgot-password, categories, coupon, admin, my-orders.
**Tên plan:** `23127271_{Load|Stress|Spike}_YYYYMMDD`

---

### 7.2 Khoa (23127207) — Browse-to-buy ← **BÀI NÀY**

Chi tiết đầy đủ ở §4 và `03_TEST_DESIGN.md`. Tóm tắt để so sánh:

```
1. POST /api/login                 extract: token             think: 1–2s
2. GET  /api/products              (KHÔNG query search)
                                   extract: 1 id từ danh sách  think: 2–4s
3. GET  /api/products/${product_id}   assert: 200             think: 1–2s
4. POST /api/cart      (+ Bearer)                             think: 1s
5. POST /api/checkout  (+ Bearer)
```

Think time bước 2 là **2–4s** — dài hơn nhánh search (1–3s) vì duyệt catalog cần cuộn và đọc lưới sản phẩm, còn người đã biết mình tìm gì thì gõ từ khóa rồi quét kết quả nhanh hơn.

**Ngoài scope:** search query, categories, coupon, my-orders.
**Tên plan:** `23127207_{Load|Stress|Spike}_YYYYMMDD`

---

### 7.3 Nguyên — Category-guided buy

Login → xem danh mục → search theo từ khóa gắn category → add cart → checkout. **Không** gọi product detail.

| Nhóm | Endpoint |
| :--- | :--- |
| Auth-heavy | `POST /api/login` |
| Read-heavy | `GET /api/categories` → `GET /api/products?search={q}` |
| Transactional | `POST /api/cart` → `POST /api/checkout` |

```
1. POST /api/login                 extract: token             think: 1–2s
2. GET  /api/categories            assert: 200, array
                                   (seed: Điện thoại, Laptop, Phụ kiện)
                                   extract (tùy chọn): category name → search term
                                                                think: 1–2s
3. GET  /api/products?search=${search}
                                   extract: product_id (first match) HOẶC từ CSV
                                                                think: 1–3s
4. POST /api/cart      (+ Bearer)  body: product_id, quantity, price, name
5. POST /api/checkout  (+ Bearer)
```

**CSV:** `email,password,category_hint,search,product_id,quantity,price,total_amount,shipping_address`

```csv
email,password,category_hint,search,product_id,quantity,price,total_amount,shipping_address
nguyen01@eshop.com,Test1234!,Laptop,Laptop,2,1,15000000,15000000,"12 Tran Hung Dao"
nguyen02@eshop.com,Test1234!,Điện thoại,iPhone,1,1,20000000,20000000,"88 Hai Ba Trung"
```

**Lưu ý SUT (đã đối chiếu code):**
- `GET /api/categories` (`server.js:243`) chỉ trả list danh mục. Endpoint products công khai **không** filter theo `category_id` → "guided" ở đây nghĩa là *categories + search keyword liên quan*, không phải lọc thật.
- Search dùng `LIKE '%${searchQuery}%'` nối chuỗi trực tiếp (`server.js:144`) — có lỗ hổng SQL injection cố ý. Giữ keyword sạch trong CSV để không lẫn lỗi injection vào số đo hiệu năng.

**Ngoài scope:** product detail, coupon, my-orders, admin category CRUD.

---

### 7.4 Thịnh — Coupon checkout

Login → search + detail → cart → **áp mã giảm giá** → checkout với `total_amount` sau giảm.

| Nhóm | Endpoint |
| :--- | :--- |
| Auth-heavy | `POST /api/login` |
| Read-heavy | `GET /api/products?search=` → `GET /api/products/{id}` |
| Transactional | `POST /api/cart` → `POST /api/apply-coupon` → `POST /api/checkout` |

```
1. POST /api/login                 extract: token, user_id    think: 1–2s
2. GET  /api/products?search=${search}
3. GET  /api/products/${product_id}                           think: 1–2s
4. POST /api/cart      (+ Bearer)
5. POST /api/apply-coupon
      body: { "code": "${coupon_code}",
              "total_amount": ${total_before},
              "user_id": ${user_id} }
      # endpoint này KHÔNG yêu cầu JWT (server.js:363 không có authenticateToken)
      extract: final_amount, coupon_id, discount_amount
      assert: 200, success == true                            think: 1s
6. POST /api/checkout  (+ Bearer)
      body: { "total_amount": ${final_amount},   # số SAU giảm
              "shipping_address": "..." }
```

**CSV:** `email,password,search,product_id,quantity,price,total_before,coupon_code,shipping_address`

**Coupon seed** (`database.js:107-110`):

| Mã | Loại | Giá trị | Min order | Số lần/user | Ghi chú |
| :--- | :--- | ---: | ---: | :---: | :--- |
| `SAVE10` | percent | 10 % | 300.000 | 1 | |
| `BIGBUY` | fixed | 50.000 | 500.000 | 1 | |
| `VIP100` | fixed | 100.000 | 300.000 | 2 | Phù hợp nhất cho tải cao |
| `EXPIRED` | percent | 20 % | 100.000 | 1 | **Không dùng** cho happy path |

**Bốn đặc thù đã xác minh trong code — Thịnh cần đọc kỹ:**

| # | Phát hiện | Vị trí | Hệ quả |
| :---: | :--- | :--- | :--- |
| 1 | Ngưỡng dùng `>` **nghiêm ngặt**, spec FR-09 nói `>=` | `server.js:379` | Đơn đúng bằng `min_order_amount` sẽ **bị từ chối**. Đặt `total_before` **lớn hơn hẳn** ngưỡng |
| 2 | Công thức percent là `total × (1 − discount_value)`, spec là `total × discount_value / 100` | `server.js:399-401` | Với `SAVE10` (`discount_value = 10`): `discount_amount = total × (1−10) = −9 × total` → **âm**, và `final_amount = total − (−9×total) = 10 × total`. Mã percent làm đơn hàng **đắt gấp 10 lần**. Đây là **bug chắc chắn**, không phải "có thể lệch" — nên dùng mã `fixed` (`VIP100`/`BIGBUY`) cho happy path và log mã `percent` thành bug report |
| 3 | Giới hạn lượt dùng **chỉ được kiểm khi có `user_id`** | `server.js:386` vs `:416` | Bỏ `user_id` khỏi payload là bỏ qua hoàn toàn ràng buộc `max_uses_per_user` |
| 4 | `POST /api/coupon-usage` là endpoint **riêng**, phải gọi thủ công sau checkout | `server.js:444` | Nếu không gọi, `usage_count` không tăng → mã 1-lần/user dùng được vô hạn. Với test tải, **không gọi** là lựa chọn hợp lý (tránh cạn lượt), nhưng phải ghi rõ trong báo cáo |

**Ngoài scope:** categories, my-orders, admin coupon CRUD.

---

### 7.5 Bảo — Buy-then-history

Login → browse list + detail → mua xong → **đọc lịch sử đơn** để xác nhận order vừa tạo (đọc-sau-ghi).

| Nhóm | Endpoint |
| :--- | :--- |
| Auth-heavy | `POST /api/login` |
| Read-heavy | `GET /api/products` → `GET /api/products/{id}` |
| Transactional | `POST /api/cart` → `POST /api/checkout` → `GET /api/orders/my-orders` |

> `my-orders` đặt sau checkout nên vẫn thuộc nhánh transactional/order; read-heavy chính vẫn là products.

```
1. POST /api/login                 extract: token             think: 1–2s
2. GET  /api/products
3. GET  /api/products/${product_id}                           think: 1–2s
4. POST /api/cart      (+ Bearer)
5. POST /api/checkout  (+ Bearer)  extract: orderId · assert: 200
6. GET  /api/orders/my-orders (+ Bearer)
      assert: 200, array không rỗng
      assert (mạnh): tồn tại phần tử có id == orderId vừa tạo  think: 1s
```

**CSV:** `email,password,product_id,quantity,price,total_amount,shipping_address`

**Điểm nhấn báo cáo:** đo latency/error của `my-orders` khi số order mỗi user tăng dần sau Stress (bảng `orders` phình). So với Khoa: cùng browse-to-buy nhưng Bảo có thêm bước đọc-sau-ghi.

**Ngoài scope:** search, categories, coupon, admin order APIs, cancel order.

---

## 8. Tài khoản & dữ liệu seed

Seed mặc định của SUT (`backend/database.js:92-93`):

| Vai trò | Email | Mật khẩu |
| :--- | :--- | :--- |
| Admin | `admin@eshop.com` | `Admin123!` |
| User | `test@eshop.com` | `Test1234!` |

Categories seed: `Điện thoại`, `Laptop`, `Phụ kiện`.

**Quy ước nhóm:** mỗi người tự tạo user pool riêng đủ cho số thread cao nhất của mình, bằng `POST /api/register` hoặc script seed, với tiền tố riêng:

| Thành viên | Tiền tố | Ghi chú |
| :--- | :--- | :--- |
| Trâm | `tram01…` | |
| **Khoa** | **`khoa001…khoa400`** | 400 tài khoản, đủ cho spike 310 VU — xem `02_DATA_SPEC.md` §2.2 |
| Nguyên | `nguyen01…` | |
| Thịnh | `thinh01…` | Cần pool lớn hơn nếu dùng mã giới hạn 1 lượt/user |
| Bảo | `bao01…` | |

> Khoa dùng 3 chữ số (`khoa001`) thay vì 2 (`khoa01`) vì pool tới 400 tài khoản; sắp xếp theo chuỗi vẫn đúng thứ tự.

**Dữ liệu sản phẩm:** seed gốc chỉ có **5 sản phẩm** (`database.js:98-102`) — quá ít để `GET /api/products` lộ chi phí thật. Khoa seed thêm 500 sản phẩm; xem `02_DATA_SPEC.md` §1 và phần khai báo điều kiện dữ liệu trong báo cáo.

---

## 9. Checklist khóa scope

- [x] Đủ 5 tên + 5 workflow không trùng
- [x] Khoa = Browse-to-buy, MSSV `23127207` đã điền vào quy ước tên
- [ ] Mỗi người điền MSSV vào tên file plan
- [ ] Mỗi người chuẩn bị CSV + user pool riêng (Khoa: `khoa001…khoa400` — `02_DATA_SPEC.md`)
- [ ] Thống nhất tool (JMeter chính, k6 phụ) và cách reset lockout
- [ ] Không ai đổi sang trùng chuỗi bước của người khác
- [ ] Chạy lệnh `Select-String` ở §4.2 trước mỗi lần commit `.jmx` — không được có kết quả
