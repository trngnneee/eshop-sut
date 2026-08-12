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

| Bước | Kỳ vọng |
| :--- | :--- |
| Login OK | HTTP 200, JSON có `token` |
| Login fail / locked | 401 hoặc 403 (chỉ ghi nhận khi cố tình probe lockout) |
| Read APIs | HTTP 200, body là JSON array/object hợp lệ |
| Cart | HTTP 200, có message thành công |
| Checkout | HTTP 200, có `orderId` |

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

## 7. Tài khoản & dữ liệu seed gốc

Seed mặc định của SUT (`backend/database.js`):

- Admin: `admin@eshop.com` / `Admin123!`
- User: `test@eshop.com` / `Test1234!`
- Categories: `Điện thoại`, `Laptop`, `Phụ kiện`
- **Chỉ 5 sản phẩm** → quá ít để `GET /api/products` lộ chi phí thật (xem `02_DATA_SPEC.md` §3)

**Khuyến nghị nhóm:** mỗi người tự seed user pool riêng đủ cho số thread cao nhất của mình.

---

## 8. Checklist khóa scope

- [x] Đủ 5 tên + 5 workflow không trùng
- [x] Khoa = Browse-to-buy, MSSV `23127207` đã điền vào quy ước tên
- [ ] Chuẩn bị CSV + user pool riêng (`khoa001…khoa400`) — xem `02_DATA_SPEC.md`
- [ ] Thống nhất tool (JMeter chính, k6 phụ) và cách reset lockout
- [ ] Không đổi sang trùng chuỗi bước của người khác
- [ ] Chạy lệnh `Select-String` ở §4.2 trước mỗi lần commit `.jmx` — không được có kết quả
