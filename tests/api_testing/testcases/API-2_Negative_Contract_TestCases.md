# API-2 — Nhóm test **Negative / Contract** (sai method · Content-Type · body · header)

**API:** API-2 · **Endpoint:** `PUT /api/orders/:id/cancel`
**Kỹ thuật:** Negative testing (HTTP method, Content-Type, body shape, header)
**Ngày lập:** 22/08/2026 · **Đã probe live trên `localhost:3000`, backup/restore DB**

> TC-ID nối tiếp: nhóm này **TC-O2-049 → 057**. Đây là nhóm **chốt cuối** của API-2.

---

## PRE — Tiền đề

| Mã | Nội dung |
|----|----------|
| **PRE-U** | Login `test@eshop.com` → `{{userToken}}` (id=2). |
| **PRE-ORD** | Mỗi case sai-method/malformed dùng **một đơn `pending` mới** (`POST /api/checkout`) để tránh nhiễu — vì có case cancel thành công sẽ đổi state. `orderId` lấy động. |

Header chung (trừ nhóm 3): `X-Student-Id: 23127438` + `Bearer {{userToken}}`.

> **Bản đồ method của `/api/orders/:id/cancel`:** chỉ **PUT** tồn tại. GET/POST/DELETE/PATCH đều `404`.

---

## 1. Test cases

### 1.1 Sai HTTP method

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-O2-049 | API-2 | FR-10 | Sai method — GET | PRE-ORD (pending) | `GET /api/orders/{{ordId}}/cancel` | `Bearer {{userToken}}` | — | `404`/`405` | Route chỉ nhận PUT. **Assertion contract:** body là **JSON** `{error}`, `Content-Type: application/json`. Đơn **không** bị hủy (GET không được đổi state — an toàn side-effect). SUT trả `404` **HTML** ⇒ FAIL contract (BUG-15) | P1 |
| TC-O2-050 | API-2 | FR-10 | Sai method — POST | PRE-ORD | `POST /api/orders/{{ordId}}/cancel` | `Bearer {{userToken}}` | `{}` | `404`/`405` | JSON `{error}`, không HTML; đơn không đổi | P2 |
| TC-O2-051 | API-2 | FR-10 | Sai method — DELETE | PRE-ORD | `DELETE /api/orders/{{ordId}}/cancel` | `Bearer {{userToken}}` | — | `404`/`405` | JSON `{error}`, không HTML | P2 |

### 1.2 Content-Type & body shape (PUT hợp lệ, biến thể payload)

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-O2-052 | API-2 | FR-10 | Content-Type `text/plain` | PRE-ORD (pending) | `PUT /api/orders/{{ordId}}/cancel` | `Content-Type: text/plain` | `hello` | `200` | Cancel **không cần body** ⇒ payload text bị bỏ qua, hủy thành công `{message}`; hậu kiểm `status==="canceled"` | P2 |
| TC-O2-053 | API-2 | FR-10 | **Malformed JSON** | PRE-ORD | `PUT /api/orders/{{ordId}}/cancel` | `Content-Type: application/json` | `{bad json` | `400` | **Assertion:** body-parser từ chối JSON hỏng ⇒ `400`. Contract yêu cầu body lỗi là **JSON** `{error}`. SUT trả `400` nhưng dạng **HTML** ⇒ FAIL contract (BUG-15). Đơn **không** bị hủy | P1 |
| TC-O2-054 | API-2 | FR-10 | Body rỗng | PRE-ORD | `PUT /api/orders/{{ordId}}/cancel` | *(không Content-Type)* | *(rỗng)* | `200` | Cancel không cần body ⇒ `200` `{message}`; `status==="canceled"` | P2 |
| TC-O2-055 | API-2 | FR-10 | Body là **array** | PRE-ORD | `PUT /api/orders/{{ordId}}/cancel` | `Content-Type: application/json` | `[1,2,3]` | `200` | Array bị bỏ qua (endpoint không đọc body) ⇒ hủy thành công; không crash, không set field từ array | P2 |

### 1.3 Header `X-Student-Id`

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-O2-056 | API-2 | FR-10 | Thiếu `X-Student-Id` | PRE-ORD (pending) | `PUT /api/orders/{{ordId}}/cancel` | `Bearer {{userToken}}` *(không X-Student-Id)* | — | `200` | SUT không yêu cầu header này ⇒ hủy bình thường. Bằng chứng anti-cheat nằm ở pre-request console log, không ở server | P3 |
| TC-O2-057 | API-2 | FR-10 | Có `X-Student-Id` (đối chứng) | PRE-ORD | `PUT /api/orders/{{ordId}}/cancel` | `Bearer {{userToken}}` + `X-Student-Id: 23127438` | — | `200` | Kết quả giống TC-056 ⇒ header không ảnh hưởng response server | P3 |

**Tổng nhóm negative/contract API-2: 9 test case** (TC-O2-049 → 057).

---

## 2. Tổng kết API-2 (đủ 4 nhóm)

| Nhóm | File | Số case | TC-ID |
|------|------|---------|-------|
| Phân hoạch `:id` + ownership | `API-2_TestCases.md` | 15 | 001–015 |
| State transition (FR-10) | `API-2_StateTransition_TestCases.md` | 9 | 016–024 |
| Security (auth/forge/IDOR) | `API-2_Security_TestCases.md` | 13 | 025–037 |
| Schema validation | `API-2_Schema_TestCases.md` | 11 | 038–048 |
| Negative / Contract | *(file này)* | 9 | 049–057 |
| **Tổng API-2** | | **57** | **TC-O2-001 → 057** |

---

## Phụ lục — Hành vi SUT đã probe & verdict

> Mỗi case dùng đơn `pending` mới; DB backup/restore. Các GET/POST/DELETE không đổi state (an toàn).

| TC-ID | Input | Expected (contract) | **Actual (SUT)** | Verdict | Bug |
|-------|-------|---------------------|------------------|---------|-----|
| **049** | GET /cancel | `404`/`405` + JSON | `404` + **HTML** `text/html` | ❌ **FAIL** | **BUG-15** |
| **050** | POST /cancel | `404`/`405` + JSON | `404` + **HTML** | ❌ **FAIL** | **BUG-15** |
| **051** | DELETE /cancel | `404`/`405` + JSON | `404` + **HTML** | ❌ **FAIL** | **BUG-15** |
| 052 | text/plain body | `200`, body bỏ qua | `200` `{"message":"Order canceled successfully"}` | ✅ PASS | — |
| **053** | malformed JSON | `400` + **JSON** `{error}` | `400` + **HTML** `text/html` | ❌ **FAIL** | **BUG-15** |
| 054 | body rỗng | `200` | `200` `{"message":...}` | ✅ PASS | — |
| 055 | body array `[1,2,3]` | `200`, bỏ qua | `200` `{"message":...}`, không crash | ✅ PASS | — |
| 056 | thiếu X-Student-Id | `200` | `200` `{"message":...}` | ✅ PASS | — |
| 057 | có X-Student-Id | `200`, giống 056 | `200` `{"message":...}` | ✅ PASS | — |

**Kết luận:** 9 case → **5 PASS / 4 FAIL**, cả 4 FAIL đều là **BUG-15** (lỗi trả **HTML** thay vì JSON).
- **FAIL (049/050/051):** sai method → `404` HTML.
- **FAIL (053):** malformed JSON → `400` **đúng status** nhưng body HTML (body-parser của Express trả trang lỗi mặc định, không qua JSON error-handler).
- **PASS:** endpoint cancel **không đọc body** nên mọi biến thể payload (text/plain, rỗng, array) đều bị bỏ qua an toàn — không crash, không mass-assign. `X-Student-Id` được bỏ qua đúng kỳ vọng.

> **Ghi chú `405` vs `404`:** giống API-1, URL tồn tại nhưng sai method đáng lẽ nên trả `405 Method Not Allowed`
> (RFC 9110 §15.5.6) kèm header `Allow`; Express trả `404`. Gộp chung vào BUG-15 (định dạng lỗi), không tách bug riêng.
> **Ghi chú malformed JSON:** đây là hành vi mặc định của `body-parser` khi `Content-Type: application/json` mà
> body không parse được — nó ném lỗi `400` **trước khi** vào route handler, nên trả trang HTML mặc định. Cần một
> error-handler tập trung để chuẩn hoá về JSON.
