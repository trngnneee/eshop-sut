# Bước 4 — Case tự nghĩ mà AI sinh từ spec dễ bỏ sót

**Họ và tên:** Đặng Trường Nguyên

**MSSV:** 23127438

**Ngày:** 23/08/2026

Ý của bước này: liệt kê những case mà **một con AI chỉ đọc spec (README + OpenAPI) sẽ khó nghĩ ra** — phải đọc source `server.js`/`database.js` hoặc phải mở server probe cURL mới lòi ra. Với mỗi case em ghi rõ **vì sao AI dễ miss**, xếp vào 3 nhóm mà đề gợi ý:

- **[Prompt]** — *chất lượng prompt*: tại em chưa đưa source cho AI đọc / chưa bắt nó test theo luồng hoặc theo state.
- **[Model]** — *giới hạn model*: AI suy theo REST convention lý tưởng, không nghĩ tới việc code làm lệch spec (hoặc chỉ test tuần tự, không nghĩ tới đồng thời/kiểu dữ liệu lạ).
- **[API]** — *đặc tính API*: bug nằm ẩn trong code (parity `id%2`, secret hardcode, thiếu FK, thiếu middleware, `this.changes` không check) — không thể suy ra từ hộp đen.

Trong đây có **7 case hoàn toàn mới** em bổ sung ở bước này (TC-P1-084/085, TC-O2-058/059, TC-P3-074/075/076), tất cả đã probe cURL thật trên `localhost:3000` (backup + restore DB). Số còn lại là những case "đắt" nhất đã có sẵn từ Bước 2 — em gom lại đây kèm lý do bỏ-sót cho đủ ≥5/API.

---

## API-1 — `GET /api/products/:id` (+ `?search=`)

| TC-ID | Case | Actual (cURL) | Expected (contract) | Vì sao AI dễ miss |
|-------|------|---------------|---------------------|-------------------|
| **TC-P1-084**  | `GET /api/products/2.0` — id chẵn ở dạng không canonical | id coerce về `2`, **và** `price` trả về string `"28000000"` | `400` (DEC-01) hoặc ít nhất `price` number | **[API]** Hai bug chồng nhau: SQLite numeric affinity ép `"2.0"→2`, rồi nhánh `id%2===0` biến price thành string. Spec-only AI không biết cả hai. |
| **TC-P1-085**  | `GET /api/products?search=%` — ký tự `%` | Trả **cả 5** sản phẩm (bằng đúng `GET /api/products`) ⇒ filter bị **bypass hoàn toàn** | `200` + array **rỗng** (`%` phải là literal) | **[API]** Code nối chuỗi `'%${search}%'` → `'%%%'` = match tất cả. Nhìn spec, AI tưởng `%` là text thường nên đoán 0 kết quả. |
| TC-P1-004 / TC-P1-020 | Matrix id chẵn/lẻ, assert **kiểu** của `price` | id lẻ → number, id chẵn → **string** | `price` luôn number | **[API]** Logic `if (row.id % 2 === 0)` ẩn trong code (BUG-01). Không đọc source thì chỉ test 1 id mẫu là trượt. |
| TC-P1-013 | `GET /api/products/abc` | `200` + body `{}` | `400`/`404` | **[Model]** AI theo REST tưởng id phi số phải 400; không ngờ SUT nuốt hết trả `200 {}`. |
| TC-P1-050 | `?search='` (một nháy) gây lỗi SQL | `500` + **HTML** `<h1>Database Error</h1>` kèm message engine | `500` JSON chung chung / không leak | **[API]** Phải đọc `server.js:145-149` mới biết nhánh lỗi trả HTML thay vì JSON. |
| TC-P1-048 | `?search=%' UNION SELECT ... FROM users--` | Rút được email + **password plaintext** + role admin qua 1 GET không auth (BUG-20) | array rỗng, không lộ credential | **[API]** SQLi UNION chỉ nghĩ ra khi biết query nối chuỗi + biết schema bảng `users`. |

---

## API-2 — `PUT /api/orders/:id/cancel`

| TC-ID | Case | Actual (cURL) | Expected (contract) | Vì sao AI dễ miss |
|-------|------|---------------|---------------------|-------------------|
| __TC-O2-058__  | `GET /api/orders/:id` __không token__ đọc đơn người khác | `200` + lộ `user_id`, `total_amount`, __`shipping_address`__ của đơn bất kỳ | `401`/`403` (endpoint đơn hàng phải có auth) | __[Prompt]__ Em chỉ bảo AI test đúng endpoint `cancel`; nó không tự đi test endpoint __liền kề__ `GET /api/orders/:id`. Hoá ra route này quên `authenticateToken` ⇒ IDOR đọc mọi đơn. Luồng hủy không kín. |
| __TC-O2-059__  | Double-cancel __song song__ (2 request cùng lúc, đơn `pending`) | Probe (23/08): `200` + `400` — SUT __serialize đúng__ (event-loop Node + sqlite3). ⚠ Race __không tái hiện ổn định__ | 1 cái `200`, cái sau `400` | __[Model]__ AI test tuần tự (TC-O2-021) nhưng không nghĩ tới đồng thời. Cửa sổ race (read-check-write không atomic) tồn tại __về lý thuyết__ nhưng khó trigger trên SQLite ⇒ xếp __observation/nghi vấn__, không khẳng định bug. |
| TC-O2-018 / TC-O2-023 | `shipping → cancel` (user) | `200` + đơn đang giao bị chuyển `canceled` (BUG-05) | `400`, giữ `shipping` | __[API]+[Model]__ Code còn comment `// Lẽ ra phải là...`. AI đọc spec sinh được case này nhưng hay đặt nhầm expected `200` theo hành vi — em ép về `400` mới lộ bug. |
| TC-O2-032 | Forge token `{id: nạn nhân}` bằng secret lộ → hủy đơn người khác | `200` (BUG-13, escalation) | `401`/`403` | __[API]__ Chỉ nghĩ ra khi thấy secret hardcode ở `server.js:9`. |
| TC-O2-035 | User hủy đơn người khác | `404 "Order not found"` (không phải `403`) | 404 chấp nhận được (anti-enumeration) | __[Prompt]__ Đây là observation về trade-off 404-vs-403, phải test chéo ownership mới thấy — prompt spec thuần ít khi yêu cầu. |

---

## API-3 — `POST /api/products` + `PUT /api/products/:id`

| TC-ID | Case | Actual (cURL) | Expected (contract) | Vì sao AI dễ miss |
|-------|------|---------------|---------------------|-------------------|
| __TC-P3-074__  | `DELETE /api/products/99999` (không tồn tại) | `200 "Product deleted"` im lặng | `404` | __[API]__ Y hệt BUG-12 nhưng cho DELETE: code không kiểm `this.changes`. Spec chỉ nói "xoá sản phẩm", AI không nghĩ tới xoá thứ không tồn tại. |
| __TC-P3-075__  | Tạo __2 sản phẩm trùng tên__ | Cả 2 đều `200 created` (id 6, 7) | Tuỳ policy, nhưng nên có ràng buộc/ cảnh báo | __[API]+[Model]__ Bảng `products` không có `UNIQUE` trên `name` (đọc `database.js` mới rõ). AI mặc định trùng tên là "hợp lệ" nên không test. |
| __TC-P3-076__  | `POST` với `price: true` (boolean) | `200 created` | `400` (price phải là số > 0) | __[Model]__ AI test số/chuỗi/null/thiếu, hiếm khi thử __boolean__. SUT không validate kiểu nên nuốt luôn. |
| TC-P3-049 / 052 / 054 | `POST`/`PUT`/`DELETE` __không token__ | `200` — ẩn danh tạo/sửa/__xoá__ được (BUG-07) | `401`/`403` | __[Prompt]__ Spec ghi "Dành cho Admin" nên AI __giả định__ đã có auth, chỉ sinh happy-path. Route thật quên `authenticateToken` (đối chứng TC-P3-056: route import lại CÓ auth). |
| TC-P3-034 / 042 | `PUT /products/1 {"name":"x"}` (thiếu field) | `price/description/imageUrl/category_id` → __null__ (mất dữ liệu, BUG-11) | Chỉ đổi field gửi, hoặc `400` | __[Model]__ AI mặc định PUT semantics là "client gửi đủ field", không ngờ code `SET` cả 5 field ⇒ field thiếu bị null. |
| TC-P3-021 | `category_id: 9999` (không tồn tại) | `200 created` | `400` | __[API]__ Bảng `products` không khai báo FOREIGN KEY (`database.js`). Hộp đen không thấy được. |
