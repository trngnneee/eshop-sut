# API-3 — Nhóm test **Bảo mật** (SEC-02/03 auth & phân quyền · forge · mass-assign · SEC-04)

**API:** API-3 · **Endpoints:** `POST /api/products`, `PUT /api/products/:id`, `DELETE /api/products/:id`
**Kỹ thuật:** Access control testing (FR-12: "CRUD sản phẩm dành cho Admin") + JWT forge + mass-assignment + stored XSS
**Ngày lập:** 22/08/2026 · **Đã probe live trên `localhost:3000`, forge token thật, backup/restore DB**

> TC-ID nối tiếp: nhóm này **TC-P3-049 → 061**.
> **FR-12 / SEC-02 / SEC-03:** mọi API có tính ảnh hưởng dữ liệu (`POST/PUT/DELETE /api/products`) **phải** yêu cầu
> (1) JWT hợp lệ, (2) `role = 'admin'`. **Expected LẤY THEO SPEC:** gọi không token → `401`, role=user → `403`.
> Nếu SUT cho `200` (nghi thiếu middleware) thì **giữ expected 401/403 và đánh dấu bug** (đúng yêu cầu).

---

## 0. Lỗ hổng nền (đọc source)

`backend/server.js` — so sánh middleware giữa các route:
```js
app.post("/api/products",       (req, res) => { ... });        // :167  ⚠ KHÔNG có authenticateToken
app.put ("/api/products/:id",   (req, res) => { ... });        // :179  ⚠ KHÔNG có
app.delete("/api/products/:id", (req, res) => { ... });        // :191  ⚠ KHÔNG có
app.post("/api/admin/import-products", authenticateToken, ...) // :199  ✓ CÓ (đối chứng)
```
⇒ Ba route CRUD sản phẩm **quên gắn `authenticateToken`** và **không hề kiểm `role`** ⇒ **ẩn danh** cũng tạo/sửa/xoá được.
Đây là vi phạm nặng nhất của API-3 (**BUG-07**). Forged token (secret lộ ở `server.js:9`) cũng vào được, nhưng trên
endpoint này là **thừa** vì không có cổng auth nào để vượt.

### Cách tạo forged admin token
```js
// trong backend/: node -e 'console.log(require("jsonwebtoken").sign({id:2,role:"admin"},"super_secret_key_that_should_not_be_here"))'
```

---

## PRE — Tiền đề

| Mã | Nội dung |
|----|----------|
| **PRE-U** | Login `test@eshop.com` → `{{userToken}}` (role=**user**). |
| **PRE-FORGE** | Forge `{{forgedAdmin}}` = `sign({id:2, role:"admin"}, leakedSecret)`. |
| **PRE-DESTRUCT** | POST/PUT/DELETE mutating ⇒ **backup DB trước, restore sau**. DELETE xoá product thật. |

Header chung: `X-Student-Id: 23127438`. Payload hợp lệ: `{"name":"SecTest","price":1000,"category_id":1}`.

---

## 1. Test cases

### 1.1 SEC-02/03 — Auth & phân quyền trên POST (tạo)

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|--------------------------|----------|
| TC-P3-049 | API-3 | **SEC-02** | POST **không token** | PRE-1 | `POST /api/products` | *(không Authorization)* | hợp lệ | **`401`** | Theo FR-12 phải chặn. SUT `200` created ⇒ **ẩn danh tạo được sản phẩm** = **BUG-07 (Critical)** | **P0** |
| TC-P3-050 | API-3 | **SEC-03** | POST **token role=user** | PRE-U | `POST /api/products` | `Bearer {{userToken}}` | hợp lệ | **`403`** | role=user không đủ quyền. SUT `200` ⇒ **BUG-07** (không kiểm role) | **P0** |
| TC-P3-051 | API-3 | SEC-03 | POST **forged admin** | PRE-FORGE | `POST /api/products` | `Bearer {{forgedAdmin}}` | hợp lệ | **`403`** (token giả) | Token ký bằng secret lộ ⇒ được chấp nhận `200`. **Nhận xét:** trên endpoint này forge là **thừa** (đã không có auth); chỉ chứng minh secret lộ (BUG-13). Escalation thực sự của forge nằm ở `/api/admin/*` | P1 |

### 1.2 SEC-02/03 — Auth trên PUT (sửa) & DELETE (xoá)

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|--------------------------|----------|
| TC-P3-052 | API-3 | **SEC-02** | PUT **không token** | PRE-1, id=3 | `PUT /api/products/3` | *(không Authorization)* | hợp lệ | **`401`** | SUT `200` updated ⇒ ẩn danh sửa được = **BUG-07** | **P0** |
| TC-P3-053 | API-3 | **SEC-03** | PUT **role=user** | PRE-U, id=3 | `PUT /api/products/3` | `Bearer {{userToken}}` | hợp lệ | **`403`** | SUT `200` ⇒ BUG-07 | **P0** |
| TC-P3-054 | API-3 | **SEC-02** | DELETE **không token** | PRE-1 + PRE-DESTRUCT, id=5 | `DELETE /api/products/5` | *(không Authorization)* | — | **`401`** | SUT `200` deleted ⇒ **ẩn danh XOÁ được sản phẩm** = **BUG-07 (nặng nhất)**. Hậu kiểm: `GET /api/products/5` → không còn | **P0** |
| TC-P3-055 | API-3 | **SEC-03** | DELETE **role=user** | PRE-U + PRE-DESTRUCT, id=4 | `DELETE /api/products/4` | `Bearer {{userToken}}` | — | **`403`** | SUT `200` ⇒ BUG-07 | **P0** |
| TC-P3-056 | API-3 | SEC-02 | Đối chứng: route CÓ auth | PRE-1 | `POST /api/admin/import-products` | *(không token)* | `{"products":[]}` | `401` | Route import **có** `authenticateToken` ⇒ trả `401`. **Chứng minh** middleware tồn tại nhưng bị **quên** ở 3 route CRUD (TC-049/052/054) | P1 |

### 1.3 Mass assignment

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|--------------------------|----------|
| TC-P3-057 | API-3 | **SEC-06** | Mass-assign `id`/`role`/`is_admin` | PRE-1 | `POST /api/products` | — | `{...hợp lệ, "id":999, "role":"admin", "is_admin":true}` | `200` | Field lạ bị **bỏ qua**: id trả về là auto-increment (**≠ 999**); record chỉ có 6 cột chuẩn (không có `role`/`is_admin`). **PASS** — INSERT chỉ map 5 field cố định | P1 |
| TC-P3-058 | API-3 | SEC-06 | Mass-assign qua PUT | PRE-1, id=3 | `PUT /api/products/3` | — | `{...hợp lệ, "id":1, "created_at":"hacked"}` | `200` | `id` của record không đổi (WHERE id=3); cột `created_at` không bị ghi. Hậu kiểm bằng `GET` | P2 |

### 1.4 SEC-04 — Stored XSS

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|--------------------------|----------|
| TC-P3-059 | API-3 | **SEC-04** | Stored XSS — POST name `<script>` rồi GET | PRE-1 | `POST /api/products` `{"name":"<script>alert(1)</script>",...}` rồi `GET /api/products/{{xid}}` | — | — | `200` | **Assertion tầng API:** (a) `Content-Type: application/json` (không `text/html`) ⇒ payload trả về như **dữ liệu**, trình duyệt không thực thi trong ngữ cảnh JSON; (b) API lưu **nguyên văn** không sanitize. **Cờ SEC-04:** nếu Frontend render `name` bằng `innerHTML` không escape ⇒ **stored XSS** (kiểm chéo FR-05/SEC-04 tầng UI) | **P0** |
| TC-P3-060 | API-3 | SEC-04 | Stored XSS — img onerror | PRE-1 | `POST /api/products` `{"name":"<img src=x onerror=alert(1)>",...}` | — | — | `200` | Như TC-059: lưu nguyên văn; assert JSON, không escape phía API | P1 |
| TC-P3-061 | API-3 | SEC-04 | Stored XSS qua `description` | PRE-1 | `POST /api/products` `{"description":"<svg onload=alert(1)>",...}` | — | — | `200` | Field `description` cũng là vector; lưu nguyên văn | P2 |

**Tổng nhóm bảo mật API-3: 13 test case** (TC-P3-049 → 061).
**API-3 hiện có: 48 (validation) + 13 (security) = 61 test case** (TC-P3-001 → 061). Nhóm Schema + Negative sẽ nối tiếp.

---

## Phụ lục — Hành vi SUT đã probe & verdict

> Forge token thật bằng `jsonwebtoken` + secret lộ; DELETE có backup/restore; hậu kiểm bằng `GET`.

| TC-ID | Input | Expected (spec) | **Actual (SUT)** | Verdict | Bug |
|-------|-------|-----------------|------------------|---------|-----|
| **049** | POST không token | `401` | `200` `{"message":"Product created","id":..}` | ❌ **FAIL** | **BUG-07** |
| **050** | POST role=user | `403` | `200` created | ❌ **FAIL** | **BUG-07** |
| **051** | POST forged admin | `403` | `200` created | ❌ FAIL | BUG-13 (thừa ở đây) |
| **052** | PUT không token | `401` | `200` `{"message":"Product updated"}` | ❌ **FAIL** | **BUG-07** |
| **053** | PUT role=user | `403` | `200` updated | ❌ **FAIL** | **BUG-07** |
| **054** | DELETE không token | `401` | `200` `{"message":"Product deleted"}` — **xoá thật** | ❌ **FAIL** | **BUG-07** |
| **055** | DELETE role=user | `403` | `200` deleted | ❌ **FAIL** | **BUG-07** |
| 056 | POST import không token (đối chứng) | `401` | `401` `{"error":"Unauthorized"}` | ✅ PASS | — |
| 057 | mass-assign id/role/is_admin | bỏ qua | `200`; id auto-increment (≠999); không có cột role/is_admin | ✅ PASS | — |
| 058 | mass-assign qua PUT | bỏ qua | `200`; id không đổi | ✅ PASS | — |
| 059 | stored XSS name `<script>` | lưu như data, JSON | `200`; lưu **nguyên văn**; GET trả `application/json` + `"<script>alert(1)</script>"` | ⚠ SEC-04 flag | stored-XSS vector |
| 060 | stored XSS img onerror | như 059 | lưu nguyên văn | ⚠ SEC-04 flag | stored-XSS vector |
| 061 | stored XSS description | như 059 | lưu nguyên văn | ⚠ SEC-04 flag | stored-XSS vector |

**Kết luận:** 13 case → **7 FAIL / 3 PASS / 3 SEC-04 flag**.
- **BUG-07 (Critical/P0) — bug nặng nhất của API-3:** cả 3 route CRUD (`POST/PUT/DELETE /api/products`) **không có** `authenticateToken` và **không kiểm role** ⇒ **ẩn danh** tạo/sửa/**xoá** sản phẩm. TC-056 (route import có auth, trả 401) chứng minh middleware tồn tại nhưng **bị quên** ở 3 route này.
- **Mass-assign: PASS** — INSERT/UPDATE chỉ map 5 field cố định nên field lạ bị bỏ qua (không có lỗ hổng mass-assign).
- **SEC-04: flag** — payload lưu nguyên văn; ở tầng API trả JSON nên không thực thi, nhưng là **stored-XSS vector** nếu FE render không escape. Không tính bug API riêng, ghi cờ để kiểm chéo tầng UI.

### BUG-07 — hồ sơ

| Trường | Nội dung |
|--------|----------|
| **Severity / Priority** | **Critical / P0** |
| **FR/SEC** | FR-12 (CRUD chỉ Admin) + SEC-02 (JWT) + SEC-03 (kiểm role) |
| **Steps** | `curl -X DELETE localhost:3000/api/products/5` (không kèm token) → `200 {"message":"Product deleted"}`; `GET /api/products/5` → không còn |
| **Expected** | `401` khi thiếu token, `403` khi role≠admin |
| **Actual** | `200` — ẩn danh tạo/sửa/xoá toàn bộ sản phẩm |
| **Root cause** | `server.js:167/179/191` — 3 route CRUD **thiếu** middleware `authenticateToken` (so với `:199` import product có gắn) và không có tầng kiểm `role==='admin'` |
| **Impact** | Bất kỳ ai trên mạng cũng phá được toàn bộ catalog sản phẩm — xoá, đổi giá, chèn hàng giả. Kết hợp thiếu validation (BUG-08) ⇒ phá hoại hoàn toàn |
| **Fix gợi ý** | Gắn `authenticateToken` + middleware `requireAdmin` (kiểm `req.user.role==='admin'`) cho cả 3 route |
