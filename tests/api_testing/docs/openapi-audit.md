# Audit OpenAPI — AI sinh vs Thực tế SUT

__Họ và tên:__ Đặng Trường Nguyên

__MSSV:__ 23127438

__File audit:__ `tests/api_testing/openapi.yaml`

__Ngày:__ 22/08/2026

---

## 1. Việc đã làm

Sau khi nhờ AI convert `api_specification.md` sang `openapi.yaml`, em không tin ngay mà tự dựng SUT lên chạy để kiểm chứng lại từng field. Cụ thể em:

- Chạy `node server.js` ở `localhost:3000` (backup `database.sqlite` trước, khôi phục lại sau khi dò xong để không làm bẩn data seed).
- Đối chiếu từng `type` / `enum` / `required` trong OpenAPI với `backend/database.js` (`price INTEGER`, `category_id INTEGER`, `orders.status TEXT`...).
- Gọi cURL thẳng vào 3 API trong scope + fixtures để so **response thật** với cái AI ghi.
- Chỗ nào AI đoán sai thì ghi lại vào bảng bên dưới, và em đã sửa luôn trong `openapi.yaml`.

Một điểm em muốn nói trước: bản `openapi.yaml` này theo quy ước **"Contract = spec (FR), còn hành vi sai của SUT ghi trong `x-sut-actual`"**. Nên chuyện file có `404` / `400` / `required` **không phải** là lỗi "AI tự bịa thêm" như em lo lúc đầu — đó là contract cố ý, mỗi chỗ đều có `x-sut-actual` đi kèm. Vì vậy em chỉ soi những chỗ **sai về sự thật** (mã lỗi thực tế, số dòng code, kiểu dữ liệu), chứ không bắt lỗi mấy chỗ contract cố tình khác implementation.

---

## 2. Các chỗ AI đoán sai (AI-claimed vs Reality)

| # | Chỗ trong `openapi.yaml` | AI ghi | Thực tế em verify | Mức | Đã sửa |
|---|--------------------------|--------|----------------------|-----|--------|
| M1 | `cancelOrder` › `x-test-security-matrix`, dòng *"Authorization rỗng / \"Bearer \""* | header rỗng ⇒ `401` | header **có mặt nhưng rỗng** ⇒ **`403`**; chỉ header **vắng hẳn** mới ra `401` | Trung bình | ✅ |
| M2 | `cancelOrder` › `x-test-security-matrix`, dòng *forged token* | forged token ⇒ `403` | chữ ký hợp lệ (secret lộ) ⇒ `jwt.verify` PASS ⇒ **`200`**, hủy đơn thành công (escalation thật) | Cao | ✅ |
| M3 | `getProductById` › `x-sut-actual` + `x-sut-code-ref` | BUG-01 `:161`, BUG-02 `:160`, code-ref `159-165` | thực tế `:162`, `:161`, `159-166` | Thấp | ✅ |
| M4 | `adminSetOrderStatus` › `x-sut-actual` | `canceled→delivered` ở `:548` | thực tế `:550` | Thấp | ✅ |
| M5 | `x-test-partitions` (id + ProductInput), cột `expect` | (dễ hiểu nhầm là actual) | `expect` là **contract**, SUT thật gần như luôn trả `200` | Thấp | ✅ |

Ngoài 5 chỗ trên, em không tìm thấy sai sót nào ở schema type, enum trạng thái, shape response fixture, hay các BUG-05/07/08/09/10/11/12 — tất cả đều khớp thực tế (xem mục 4).

---

## 3. Giải thích chi tiết

### M1 — Auth header rỗng: AI ghi `401`, thực tế `403`

Đoạn middleware `server.js:99-109`:

```js
const authHeader = req.headers["authorization"];
const token = authHeader && authHeader.split(" ")[1];
if (token == null) return res.status(401).json({ error: "Unauthorized" });
jwt.verify(token, SECRET_KEY, (err, user) => {
  if (err) return res.status(403).json({ error: "Forbidden" });
  ...
});
```

Chỗ này dùng `token == null` — chỉ true khi `token` là `undefined`/`null`. Nếu client gửi header **có mặt nhưng giá trị rỗng**, thì `token = ""`, mà `"" == null` là **false**, nên nó không dừng ở `401` mà chui vào `jwt.verify("")` → lỗi → **`403`**. AI gộp chung "vắng header" với "header rỗng" vào cùng một dòng `401` là sai.

em test lại:

```ini
PUT /api/orders/1/cancel  (không có header)                → 401  ✓ đúng
PUT /api/orders/1/cancel  -H "Authorization;" (rỗng)       → 403  ✗ AI ghi 401
PUT /api/orders/1/cancel  -H "Authorization: <raw token>"  → 401  ✓ (không có "Bearer")
PUT /api/orders/1/cancel  -H "Authorization: Bearer xxx"   → 403  ✓
```

**Đã sửa:** tách thành các dòng riêng — *vắng header* / *thiếu prefix Bearer* ⇒ `401`; *header rỗng* / *`Bearer ` + token rỗng* ⇒ `403`, kèm comment giải thích ngay trong YAML.

### M2 — Forged admin token: AI ghi `403`, thực tế `200`

Secret bị hardcode ở `server.js:9`. em tự ký một token `{id:2, role:"admin"}` bằng đúng secret đó, chữ ký hợp lệ nên `jwt.verify` pass luôn. Mà `cancelOrder` còn chẳng check `role`, chỉ so `id` với `user_id` của đơn:

```sh
FORGED=$(node -e "console.log(require('jsonwebtoken').sign({id:2,role:'admin'},'super_secret_key_that_should_not_be_here'))")
PUT /api/orders/1/cancel -H "Authorization: Bearer $FORGED"  → 200 {"message":"Order canceled successfully"}
```

Vấn đề là cột `expectedStatus` ở các dòng khác (`token rác → 403`, `IDOR → 404`) là **giá trị SUT trả thật** để em assert, riêng dòng forged token lại ghi `403` theo **contract mong muốn** trong khi thực tế là `200`. Trộn hai kiểu nghĩa vào một cột thì lúc generate test sẽ hiểu nhầm.

**Đã sửa:** giữ `expectedStatus: 403` là contract nhưng gắn thêm `x-sut-actual` (bugId `BUG-SEC-FORGE`, observed `200`), đánh dấu rõ đây là case **expected-FAIL** — SUT trả `200` chính là bằng chứng bug, giống cách file đã xử lý BUG-05.

### M3 / M4 — Số dòng code bị lệch

| AI ghi | Thực tế (`grep -n`) |
|--------|---------------------|
| BUG-01 parity `server.js:161` | dòng **162** |
| BUG-02 `!row` `server.js:160` | dòng **161** |
| code-ref `getProductById` `159-165` | route trải **159-166** |
| OUT-OF-SCOPE `canceled→delivered` `server.js:548` | dòng **550** |

Chỉ lệch 1-2 dòng (chắc AI đếm trên bản hơi khác), không ảnh hưởng test nhưng để reviewer trace đúng thì em sửa lại hết. Các trích dẫn còn lại thì đúng: `createProduct 167-177`, `updateProduct 179-189`, `cancelOrder 321-342` + comment `328-331`, secret `server.js:9`.

### M5 — Cột `expect` trong partition là contract chứ không phải actual

Trong `x-test-partitions`, mọi input sai đều ghi `expect: 400`. Cái này đúng theo quy ước file (contract = FR-15), nhưng đọc lướt dễ tưởng SUT trả 400, trong khi thực tế nó trả **`200`** gần hết (BUG-08/09/10). Không phải lỗi, nhưng để tránh nhầm khi làm generator, em thêm comment ở đầu mỗi block `x-test-partitions` nói rõ *`expect` = contract, actual xem `x-sut-actual`*.

---

## 4. Những chỗ AI làm đúng

Ở phần này em muốn ghi nhận là AI đã né được đúng mấy cái bẫy mà em lo:

- **Không bịa `201 Created`** cho `POST /api/products` — nó dùng `200` và ghi chú rõ 201 chỉ là convention REST, không tính là bug. 👍
- `404` / `400` / `required` đều có nhưng **cố ý làm contract**, mỗi chỗ kèm `x-sut-actual` mô tả SUT thật trả `200`/no-op ⇒ không phải lỗi.
- **Toàn bộ bug map khớp 100% với cURL** (em verify lại từng cái):

| Bug | AI ghi | cURL thực tế | Khớp |
|-----|--------|--------------|------|
| BUG-01 | id chẵn → `price` string | `GET /products/2` → `"price":"28000000"` | ✓ |
| BUG-02 | id không tồn tại → `200 {}` | `GET /products/99999` → `200 {}` | ✓ |
| BUG-03 | id phi số → `200 {}` | `GET /products/abc` → `200 {}` | ✓ |
| BUG-05 | user hủy đơn `shipping` → `200` | verified `200` | ✓ |
| BUG-07 | product write không auth → `200` | `POST/PUT` không token → `200` | ✓ |
| BUG-08 | name rỗng + price âm + category sai → `200` | verified `200 created` | ✓ |
| BUG-09 | body `{}` → `200` | verified `200 created` | ✓ |
| BUG-10 | name 300 ký tự → `200` | verified `200 created` | ✓ |
| BUG-11 | partial PUT → null hóa field | verified các field → `null` | ✓ |
| BUG-12 | PUT id không tồn tại → `200` | verified `200 "Product updated"` | ✓ |

- __Kiểu dữ liệu khớp `database.js`:__ `price` integer ✓, `category_id` integer ✓, `OrderStatus` enum `[pending, confirmed, shipping, delivered, canceled]` ✓.
- **SQLi khoanh vùng đúng:** ghi `GET /products/:id` dùng parameterized (`WHERE id = ?`) nên an toàn, không gán nhầm SQLi cho detail — lỗ hổng thật nằm ở `?search=` bên endpoint list. ✓
- __IDOR đúng:__ hủy đơn người khác → `404 "Order not found"` (do `WHERE id=? AND user_id=?`), verified. ✓
- **Fixture đúng shape:** `login → {message,token,user}`, `checkout → {message,orderId}`, `adminSetOrderStatus → {message}`. ✓
- **Mấy edge em test thêm:** `GET /products/` (id rỗng) → `200` trả list ✓; `GET /products/1.0` → product 1 ✓ (SQLite ép `1.0→1`); `GET /products/1.5` → `200 {}` ✓.

---

## 5. Kết luận

Bản `openapi.yaml` chất lượng khá tốt, phần lớn sai sót là mấy chi tiết nhỏ (số dòng) và 2 chỗ về mã lỗi auth (M1, M2) mà nếu không chạy thật thì không thể phát hiện. Sau khi em sửa cả 5 điểm trực tiếp trong file, `openapi.yaml` đã đủ chính xác để dùng làm **input chuẩn cho generator ở Bước 9**.

**Checklist đã sửa trong `openapi.yaml`:**

- [x] M1 — tách case auth: header rỗng ⇒ `403`, vắng header/thiếu Bearer ⇒ `401`
- [x] M2 — gắn `x-sut-actual` (`BUG-SEC-FORGE`, actual `200`) cho dòng forged token, đánh dấu expected-FAIL
- [x] M3 — sửa số dòng BUG-01 → `162`, BUG-02 → `161`, code-ref getProduct → `159-166`
- [x] M4 — sửa OUT-OF-SCOPE `canceled→delivered` → `550`
- [x] M5 — thêm comment `expect` = contract ở 2 block `x-test-partitions`
