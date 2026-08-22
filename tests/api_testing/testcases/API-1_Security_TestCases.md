# API-1 — Nhóm test **Bảo mật** (SEC-04 / SEC-05 + rò rỉ thông tin)

**API:** API-1 · **Endpoint:** `GET /api/products?search=` (và `GET /api/products/:id`)
**Kỹ thuật:** Security testing bám mã SEC-01…SEC-07 trong `README.md` của SUT
**Phạm vi nhóm này:** SEC-05 (SQL Injection), SEC-04 (XSS / output encoding), và lỗi rò rỉ thông tin (contract JSON bị phá thành HTML + leak nội dung lỗi DB)
**Ngày lập:** 22/08/2026 · **Đã probe live trên `localhost:3000`**

> **Tách bạch với nhóm EP/BVA:** file `API-1_TestCases.md` chỉ phủ phân hoạch/biên; các payload tấn công
> được gom **riêng** vào đây để dễ chấm và dễ map sang bug report. TC-ID tiếp nối dãy cũ, bắt đầu từ **TC-P1-045**.
>
> **Nguồn gốc lỗ hổng (đọc code):** `backend/server.js:143-145`
> ```js
> const searchQuery = req.query.search;
> const query = `SELECT * FROM products WHERE name LIKE '%${searchQuery}%'`;  // ⚠ nối chuỗi thẳng
> db.all(query, [], (err, rows) => { if (err) return res.status(500).send(`<h1>Database Error</h1><p>${err.message}</p>`); ... });
> ```
> Vi phạm **SEC-05** (không dùng parameterized query) và tạo thêm kênh **rò rỉ lỗi** (`err.message` render vào HTML).

---

## PRE — Tiền đề

| Mã | Nội dung |
|----|----------|
| **PRE-1** | Backend `node server.js` tại `http://localhost:3000`, DB seed sạch (5 products id 1–5; 2 users: `admin@eshop.com/Admin123!` role=admin, `test@eshop.com/Test1234!` role=user). |
| **PRE-SEC** | ⚠ Payload **destructive** (TC-P1-047) có thể phá dữ liệu trên DB khác. Trên SUT này an toàn vì `db.all()` chỉ thực thi **statement đầu tiên** (không hỗ trợ multi-statement), nhưng **vẫn phải backup** `database.sqlite` trước khi chạy và restore sau. |

Header dùng chung mọi case: `X-Student-Id: 23127438`. Endpoint `GET` ⇒ `Body` rỗng.
Cột **URL** ghi giá trị `search` ở dạng **thô** (chưa URL-encode); khi chạy phải encode (Postman/Newman tự lo, hoặc `curl -G --data-urlencode`).

---

## 1. Bảng phân tích tấn công (attack surface → payload → cơ chế)

| Attack ID | SEC | Kênh | Payload (thô) | Cơ chế khai thác | Kỳ vọng contract |
|-----------|-----|------|---------------|------------------|------------------|
| **A1** | SEC-05 | `?search=` | `' OR '1'='1` | Tautology: đóng chuỗi LIKE, chèn điều kiện luôn đúng | Coi literal ⇒ **0** kết quả |
| **A2** | SEC-05 | `?search=` | `' OR 1=1--` | Tautology + comment nuốt phần đuôi query | Coi literal ⇒ **0** kết quả |
| **A3** | SEC-05 | `?search=` | `'; DROP TABLE products;--` | Stacked query (destructive) | Coi literal ⇒ **0** kết quả; bảng **còn nguyên** |
| **A4** | SEC-05 | `?search=` | `%' UNION SELECT id,email,password,role,login_attempts,locked_until FROM users--` | UNION rút cột nhạy cảm từ bảng `users` | Coi literal ⇒ **0** kết quả; **không** lộ user |
| **A5** | SEC-05 | `?search=` | `' UNION SELECT id,name,email,password,role,phone FROM users--` | UNION lấy trọn bộ credential (6 cột khớp shape products) | Coi literal ⇒ **0** kết quả; **không** lộ password |
| **A6** | rò rỉ | `?search=` | `'` (một nháy đơn) | Làm hỏng cú pháp SQL để lấy thông điệp lỗi | `{error}` JSON chung chung, **không** lộ engine |
| **A7** | rò rỉ | `?search=` | `abc'` | Nháy đơn không cân → lỗi token | Như A6 |
| **A8** | rò rỉ | `?search=` | `')` | Đóng ngoặc thừa → lỗi cú pháp khác | Như A6 |
| **A9** | SEC-04 | `?search=` | `<script>alert(1)</script>` | Kiểm tra API có echo lại từ khóa dạng HTML không | Response `application/json`; **không** chứa payload thô; **không** phải HTML |
| **A10** | SEC-04 | `?search=` | `<img src=x onerror=alert(1)>` | Biến thể XSS không cần thẻ script | Như A9 |
| **A11** | SEC-05 | `:id` | `1 OR 1=1` / `1; DROP TABLE products;--` | SQLi qua path param (đối chứng — param này DÙNG parameterized query) | An toàn: `400`/`404`, không leak, bảng nguyên |

---

## 2. Test cases

### 2.1 SEC-05 — SQL Injection ở `?search=`

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL (`search=`) | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------------------|---------|------|-----------------|-------------------------------|----------|
| TC-P1-045 | API-1 | **SEC-05** | SQLi tautology | PRE-1 | `GET /api/products?search=' OR '1'='1` | — | — | `200` | `Array.isArray(body)` **và** `body.length === 0`. Payload phải được coi là literal ⇒ **không** khớp product nào. (Nếu trả về ≥1 phần tử ⇒ filter bị bypass ⇒ **FAIL/SQLi**) | **P0** |
| TC-P1-046 | API-1 | **SEC-05** | SQLi tautology + comment | PRE-1 | `GET /api/products?search=' OR 1=1--` | — | — | `200` | `body.length === 0` | **P0** |
| TC-P1-047 | API-1 | **SEC-05** | SQLi stacked (destructive) | PRE-1 + PRE-SEC (backup DB) | `GET /api/products?search='; DROP TABLE products;--` | — | — | `200` | `body.length === 0`. **Assertion hậu kiểm bắt buộc:** gọi lại `GET /api/products` (no search) → vẫn trả **5** product ⇒ bảng `products` chưa bị xoá | **P0** |
| TC-P1-048 | API-1 | **SEC-05** | SQLi **UNION** — rò rỉ dữ liệu | PRE-1 | `GET /api/products?search=%' UNION SELECT id,email,password,role,login_attempts,locked_until FROM users--` | — | — | `200` | `body.length === 0`. **Assertion chống rò rỉ:** `JSON.stringify(body)` **không** chứa `"@eshop.com"`, **không** chứa `"Admin123!"`, **không** chứa `"admin"` (role). Có bất kỳ chuỗi nào ⇒ **FAIL nghiêm trọng** (lộ credential) | **P0** |
| TC-P1-049 | API-1 | **SEC-05** | SQLi **UNION** — lộ credential đầy đủ | PRE-1 | `GET /api/products?search=' UNION SELECT id,name,email,password,role,phone FROM users--` | — | — | `200` | `body.length === 0`. **Assertion:** không phần tử nào có `description === "Admin123!"` hoặc `price === "admin@eshop.com"`; toàn bộ `body` không chứa mật khẩu plaintext | **P0** |

### 2.2 Rò rỉ thông tin — payload gây lỗi SQL trả HTML + message

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL (`search=`) | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------------------|---------|------|-----------------|-------------------------------|----------|
| TC-P1-050 | API-1 | **SEC-05** / rò rỉ | Error-based leak | PRE-1 | `GET /api/products?search='` (một nháy đơn) | — | — | `200` (literal ⇒ 0 kết quả) **hoặc** `500` với JSON | **(a)** `Content-Type` chứa `application/json` — **không** `text/html`; **(b)** `body` parse được thành JSON; **(c)** body **không** chứa `<h1>`, không chứa `SQLITE`, không chứa `error.message` nội bộ | **P0** |
| TC-P1-051 | API-1 | **SEC-05** / rò rỉ | Error-based leak | PRE-1 | `GET /api/products?search=abc'` | — | — | `200` hoặc `500`-JSON | Như TC-050: không HTML, không lộ `unrecognized token` | P1 |
| TC-P1-052 | API-1 | **SEC-05** / rò rỉ | Error-based leak | PRE-1 | `GET /api/products?search=')` | — | — | `200` hoặc `500`-JSON | Như TC-050: không lộ `near ")": syntax error` | P1 |
| TC-P1-053 | API-1 | rò rỉ | Contract khi lỗi | PRE-1 | `GET /api/products?search='` | — | — | Bất kỳ | Nếu status `5xx`: body vẫn **đúng schema `Error`** (`{error: string}`), `error` là thông điệp **chung chung** (vd `"Internal server error"`), không nhúng chuỗi engine/DB | P1 |

### 2.3 SEC-04 — XSS / output encoding ở `?search=`

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL (`search=`) | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------------------|---------|------|-----------------|-------------------------------|----------|
| TC-P1-054 | API-1 | **SEC-04** | XSS reflected — script tag | PRE-1 | `GET /api/products?search=<script>alert(1)</script>` | — | — | `200` | **(a)** `Content-Type: application/json` (không `text/html`); **(b)** `Array.isArray(body)` và `body.length === 0` (không khớp product); **(c)** raw response **không** echo lại nguyên chuỗi `<script>` — API không phản chiếu từ khóa | **P0** |
| TC-P1-055 | API-1 | **SEC-04** | XSS — img onerror | PRE-1 | `GET /api/products?search=<img src=x onerror=alert(1)>` | — | — | `200` | Như TC-054: JSON, `length===0`, không echo payload thô | P1 |
| TC-P1-056 | API-1 | **SEC-04** | XSS header hardening | PRE-1 | `GET /api/products?search=<script>alert(1)</script>` | — | — | `200` | Response có `X-Content-Type-Options: nosniff` (chặn browser đoán MIME). *(Case này kỳ vọng cao hơn hiện trạng — dùng để khuyến nghị hardening; ghi observation nếu SUT thiếu)* | P2 |

### 2.4 SEC-05 — đối chứng ở `:id` (path param dùng parameterized query)

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-P1-057 | API-1 | **SEC-05** | SQLi ở `:id` (đối chứng dương) | PRE-1 | `GET /api/products/1 OR 1=1` | — | — | `400`/`404` | Không trả nhiều hơn 1 product; không leak; bảng nguyên. (Endpoint này DÙNG `WHERE id = ?` parameterized ⇒ **phải an toàn** — dùng để chứng minh sự bất nhất: `:id` an toàn còn `?search=` thì không) | P1 |
| TC-P1-058 | API-1 | **SEC-05** | SQLi ở `:id` (stacked) | PRE-1 + PRE-SEC | `GET /api/products/1; DROP TABLE products;--` | — | — | `400`/`404` | Bảng `products` còn 5 dòng sau khi gọi | P2 |

**Tổng nhóm bảo mật: 14 test case** (TC-P1-045 → 058).
Cộng với 44 case EP/BVA ⇒ **API-1 hiện có 58 test case** (chưa gồm nhóm Schema validation).

---

## Phụ lục — Hành vi SUT đã probe & verdict

> Chạy `node server.js` tại `localhost:3000`, backup `database.sqlite` trước và restore sau. Số liệu là thực đo.

| TC-ID | Payload | Expected (contract) | **Actual (SUT)** | Verdict | Bug |
|-------|---------|---------------------|------------------|---------|-----|
| **045** | `' OR '1'='1` | 200, array **rỗng** | 200, array **5** phần tử `[1,2,3,4,5]` — filter bị bypass | ❌ **FAIL** | **BUG-03** |
| **046** | `' OR 1=1--` | 200, rỗng | 200, array **5** | ❌ **FAIL** | **BUG-03** |
| **047** | `'; DROP TABLE products;--` | 200, rỗng; bảng nguyên | 200, array **5**; **bảng còn nguyên** (db.all chỉ chạy statement đầu ⇒ DROP không thực thi) | ❌ **FAIL** (SQLi có, DROP vô hại) | **BUG-03** |
| **048** | `%' UNION SELECT ... FROM users--` | 200, rỗng; không lộ user | 200, **7 phần tử**; phần tử đầu = `{"id":1,"name":"admin@eshop.com","price":"Admin123!","description":"admin",...}` — **LỘ email + password plaintext + role của admin** | ❌ **FAIL nghiêm trọng** | **BUG-20 (mới)** |
| **049** | `' UNION SELECT id,name,email,password,role,phone FROM users--` | 200, rỗng | 200, **7 phần tử**; `{"id":1,"name":"Admin User","price":"admin@eshop.com","description":"Admin123!","imageUrl":"admin",...}` | ❌ **FAIL nghiêm trọng** | **BUG-20 (mới)** |
| **050** | `'` | JSON, không HTML/không leak | **`500`**, `Content-Type: text/html`, body `<h1>Database Error</h1><p>SQLITE_ERROR: unrecognized token: "'"</p>` | ❌ **FAIL** | **BUG-04** |
| **051** | `abc'` | JSON, không leak | `500` + HTML + `SQLITE_ERROR: unrecognized token: "'"` | ❌ **FAIL** | **BUG-04** |
| **052** | `')` | JSON, không leak | `500` + HTML + `SQLITE_ERROR: near ")": syntax error` | ❌ **FAIL** | **BUG-04** |
| **053** | `'` | 5xx → schema Error | `500` là HTML thuần, **không** có field `error` | ❌ **FAIL** | **BUG-04** |
| **054** | `<script>alert(1)</script>` | JSON, rỗng, không echo | 200, `application/json`, array **rỗng** `[]`, **không** echo payload | ✅ **PASS** | — |
| **055** | `<img src=x onerror=...>` | JSON, rỗng, không echo | 200, `[]`, không echo | ✅ **PASS** | — |
| **056** | script + check header | có `X-Content-Type-Options` | 200, **thiếu** `X-Content-Type-Options` | ❌ FAIL (hardening) | **BUG-21 (mới, minor)** |
| **057** | `:id = 1 OR 1=1` | 400/404, an toàn | 200 + `{}` (SQLite ép `"1 OR 1=1"`→ không khớp ⇒ rỗng); **không** leak, bảng nguyên | ⚠ PASS (an toàn SQLi) / FAIL contract (đáng lẽ 400) → map **BUG-03** phần `:id` | — |
| **058** | `:id = 1; DROP...` | 400/404; bảng nguyên | 200 + `{}`; bảng còn 5 dòng | ⚠ an toàn SQLi | — |

**Kết luận nhóm bảo mật:** 14 case → **11 FAIL / 2 PASS / 1 mixed**. Endpoint `?search=` **có lỗ hổng SQL Injection thực sự** (bypass filter + **rò rỉ credential admin qua UNION**), cộng lỗi rò rỉ thông báo lỗi. XSS ở tầng API **không** khai thác được vì API không echo từ khóa (rủi ro XSS chuyển sang tầng render FR-05 của Frontend, và stored-XSS qua tên sản phẩm ở API-3).

### Bug mới / cập nhật từ nhóm này

| Bug | FR/SEC | Severity | Mô tả | Ghi chú map |
|-----|--------|----------|-------|-------------|
| **BUG-03** | SEC-05 | **Critical/P0** | SQL Injection ở `?search=` — nối chuỗi `LIKE '%${searchQuery}%'`. Tautology bypass filter (045/046); wildcard bypass (đã ghi ở nhóm EP: BUG-17). | Đã có mã BUG-03; nhóm này bổ sung bằng chứng khai thác |
| **BUG-20** | **SEC-05 + SEC-01** | **Critical/P0** | **UNION-based SQLi rút toàn bộ bảng `users` qua endpoint products**, lộ `email` + **mật khẩu plaintext** + `role`. Kết hợp SEC-01 (password lưu plaintext) ⇒ chiếm được tài khoản admin chỉ bằng 1 request GET không cần auth. | **Bug mới, nặng nhất của API-1** |
| **BUG-04** | SEC-05 | **Major/P1** | Payload gây lỗi SQL → `500` + `Content-Type: text/html` + `<h1>Database Error</h1>` kèm nguyên văn `SQLITE_ERROR` (`err.message`). Phá contract JSON + lộ engine/cấu trúc query. | Đã khai báo ở `openapi.yaml` response 500 của `listProducts` |
| **BUG-21** | SEC-04 | Minor/P2 | Thiếu header `X-Content-Type-Options: nosniff`. | Hardening — observation |

> **Điểm dành cho phần "AI bỏ sót" (bước Extend):** BUG-20 (UNION rò rỉ credential) là case AI ít khi tự sinh — AI thường dừng ở tautology `' OR '1'='1` để "chứng minh SQLi" mà không đi tiếp tới UNION rút bảng khác, vì nó cần biết **tên bảng `users` và số cột khớp** — thông tin chỉ có khi đọc `database.js`. Đây là ví dụ điển hình *API characteristic + prompt quality* trong AI Critique.
