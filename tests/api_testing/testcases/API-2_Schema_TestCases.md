# API-2 — Nhóm test **Schema Validation** (contract response + status theo transition)

**API:** API-2 · **Endpoint:** `PUT /api/orders/:id/cancel`
**Kỹ thuật:** JSON Schema validation (`pm.response.to.have.jsonSchema`) + assert status code theo từng transition + response time
**Ngày lập:** 22/08/2026 · **Schema kiểm chứng bằng `jsonschema` Draft-07**

> TC-ID nối tiếp: nhóm này **TC-O2-038 → 048**. Đây là nhóm **chốt** API-2 (đủ 4 nhóm: phân hoạch · state · security · schema).
> Schema tái dùng: `postman/schemas/message-response.schema.json`, `error-response.schema.json`.

---

## 1. JSON Schema

### 1.1 Success — `{message: string}`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "message-response.schema.json",
  "type": "object",
  "additionalProperties": false,
  "required": ["message"],
  "properties": { "message": { "type": "string", "minLength": 1 } }
}
```

### 1.2 Error — `{error: string}`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "error-response.schema.json",
  "type": "object",
  "additionalProperties": false,
  "required": ["error"],
  "properties": { "error": { "type": "string", "minLength": 1 } }
}
```

**Chốt chặn:** `additionalProperties:false` → fail nếu response lẫn cả `message` và `error`, hoặc dư field.
`required` + `minLength:1` → fail nếu thiếu field hoặc chuỗi rỗng.

### Kiểm chứng schema (đã chạy `jsonschema` Draft-07)

| Input | Schema | Kỳ vọng | Kết quả |
|-------|--------|---------|---------|
| `{"message":"Order canceled successfully"}` | message | PASS | ✅ PASS |
| `{"error":"x"}` | message | FAIL | ❌ `Additional properties ('error')` |
| `{"message":"ok","extra":1}` | message | FAIL | ❌ `Additional properties ('extra')` |
| `{"error":"Cannot cancel this order."}` | error | PASS | ✅ PASS |
| `{"error":"Order not found"}` | error | PASS | ✅ PASS |
| `{}` | error | FAIL | ❌ `'error' is a required property` |

---

## 2. Script Postman dùng chung

```js
const okSchema  = JSON.parse(pm.collectionVariables.get("messageSchema"));
const errSchema = JSON.parse(pm.collectionVariables.get("errorSchema"));

pm.test("Content-Type application/json", () =>
  pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json"));
pm.test("Response time < 2000ms", () =>
  pm.expect(pm.response.responseTime).to.be.below(2000));

// ví dụ cho transition pending→cancel (kỳ vọng 200 + message schema):
pm.test("status 200", () => pm.response.to.have.status(200));
pm.test("body khớp {message}", () => pm.response.to.have.jsonSchema(okSchema));

// ví dụ cho transition không hợp lệ (kỳ vọng 400 + error schema):
pm.test("status 400", () => pm.response.to.have.status(400));
pm.test("body khớp {error}", () => pm.response.to.have.jsonSchema(errSchema));
```

---

## 3. Test cases

Header chung: `X-Student-Id: 23127438` + `Bearer {{userToken}}`. Fixture state dựng như nhóm state-transition.

### 3.1 Schema success `{message}` (transition hợp lệ)

| TC-ID | API | FR/SEC | Technique | Precondition (state) | Method + URL | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|----------------------|--------------|-----------------|-------------------------------|----------|
| TC-O2-038 | API-2 | FR-10 | Schema success | pending (checkout) | `PUT /api/orders/{{ordPending}}/cancel` | `200` | `jsonSchema(messageSchema)` PASS; đúng 1 field `message` là string không rỗng; **không** có field `error` | **P0** |
| TC-O2-039 | API-2 | FR-10 | Schema success | confirmed (checkout → admin confirmed) | `PUT /api/orders/{{ordConfirmed}}/cancel` | `200` | `jsonSchema(messageSchema)` PASS; `message` string | P1 |
| TC-O2-040 | API-2 | FR-10 | Content-Type + time | pending | `PUT /api/orders/{{ordP2}}/cancel` | `200` | `Content-Type` chứa `application/json`; `responseTime < 2000` | P2 |

### 3.2 Schema error `{error}` (transition không hợp lệ, status theo spec)

| TC-ID | API | FR/SEC | Technique | Precondition (state) | Method + URL | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|----------------------|--------------|-----------------|-------------------------------|----------|
| TC-O2-041 | API-2 | FR-10 | Schema error + status | **shipping** (→confirmed→shipping) | `PUT /api/orders/{{ordShipping}}/cancel` | **`400`** (spec) | Assert **status 400** + `jsonSchema(errorSchema)`. SUT trả `200`+`{message}` ⇒ **cả 2 assert FAIL** = BUG-05 (status sai + schema sai loại) | **P0** |
| TC-O2-042 | API-2 | FR-10 | Schema error + status | delivered | `PUT /api/orders/{{ordDelivered}}/cancel` | `400` | status `400` + `jsonSchema(errorSchema)`; `error` = "Cannot cancel this order." | **P0** |
| TC-O2-043 | API-2 | FR-10 | Schema error + status | canceled | `PUT /api/orders/{{ordCanceled}}/cancel` | `400` | status `400` + `jsonSchema(errorSchema)` | P1 |
| TC-O2-044 | API-2 | FR-10 | Schema error — not found | id 99999 | `PUT /api/orders/99999/cancel` | `404` | status `404` + `jsonSchema(errorSchema)`; `error` = "Order not found" | P1 |
| TC-O2-045 | API-2 | SEC-02 | Schema error — auth | pending (đơn tồn tại) | `PUT /api/orders/{{ordAuth}}/cancel` *(không token)* | `401` | status `401` + `jsonSchema(errorSchema)`; `error` = "Unauthorized" | P1 |
| TC-O2-046 | API-2 | SEC-02 | Schema error — forbidden | đơn tồn tại | `PUT .../cancel` `Bearer garbage` | `403` | status `403` + `jsonSchema(errorSchema)`; `error` = "Forbidden" | P2 |

### 3.3 Contract âm bản — nơi schema JSON KHÔNG áp dụng được

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|-----------------|-------------------------------|----------|
| TC-O2-047 | API-2 | FR-10 | Contract khi lỗi định dạng | — | `PUT /api/orders//cancel` (id rỗng) | `404`/`405` + JSON | **Assertion:** `Content-Type` phải là `application/json` để `jsonSchema(errorSchema)` chạy được. SUT trả **HTML** ⇒ body không parse JSON ⇒ FAIL = BUG-15 | P2 |
| TC-O2-048 | API-2 | FR-10 | Mutual-exclusion | pending | `PUT /api/orders/{{ordX}}/cancel` | `200` | Response chứa **hoặc** `message` **hoặc** `error`, **không đồng thời cả hai** (assert bằng `additionalProperties:false` của messageSchema) | P2 |

**Tổng nhóm schema API-2: 11 test case** (TC-O2-038 → 048).
**API-2 tổng cộng: 15 + 9 + 13 + 11 = 48 test case** (TC-O2-001 → 048).

---

## Phụ lục — Hành vi SUT đã probe & verdict

> Số liệu response lấy từ các lần probe live ở 3 nhóm trước (cùng SUT, cùng DB seed). Schema đã kiểm chứng Draft-07.

| TC-ID | Transition/Input | Expected (spec) | **Actual (SUT)** | Verdict | Bug |
|-------|------------------|-----------------|------------------|---------|-----|
| 038 | pending→cancel | `200` + `{message}` | `200` `{"message":"Order canceled successfully"}` | ✅ PASS | — |
| 039 | confirmed→cancel | `200` + `{message}` | `200` `{"message":...}` | ✅ PASS | — |
| 040 | pending CT+time | json, <2000ms | `application/json`, ~1ms | ✅ PASS | — |
| **041** | shipping→cancel | **`400` + `{error}`** | `200` + `{message}` | ❌ **FAIL** | **BUG-05** |
| 042 | delivered→cancel | `400` + `{error}` | `400` `{"error":"Cannot cancel this order."}` | ✅ PASS | — |
| 043 | canceled→cancel | `400` + `{error}` | `400` `{"error":"Cannot cancel this order."}` | ✅ PASS | — |
| 044 | id 99999 | `404` + `{error}` | `404` `{"error":"Order not found"}` | ✅ PASS | — |
| 045 | không token | `401` + `{error}` | `401` `{"error":"Unauthorized"}` | ✅ PASS | — |
| 046 | token rác | `403` + `{error}` | `403` `{"error":"Forbidden"}` | ✅ PASS | — |
| **047** | id rỗng `//cancel` | `404`/`405` + JSON | `404` + **HTML** | ❌ **FAIL** | **BUG-15** |
| 048 | mutual-exclusion | chỉ 1 trong 2 field | các response đều đúng 1 field | ✅ PASS | — |

**Kết luận:** 11 case → **9 PASS / 2 FAIL** (BUG-05 ở 041, BUG-15 ở 047).
Response contract của API-2 **nhìn chung sạch**: mọi phản hồi JSON đều đúng dạng `{message}` hoặc `{error}`, đúng 1 field, không lẫn lộn. Hai chỗ hỏng là (a) transition `shipping→cancel` trả nhầm `{message}`+`200` thay vì `{error}`+`400` (BUG-05 — schema bắt được vì trả **sai loại** response), và (b) route id rỗng trả HTML (BUG-15).

> **Điểm mạnh của schema testing ở đây:** BUG-05 bị bắt **hai lần độc lập** — vừa sai **status** (200≠400), vừa sai **loại response** (`{message}` thay vì `{error}`). Một transition sai không chỉ trả nhầm mã mà còn nhầm cả hình dạng contract, nên assert schema là lớp phòng thủ thứ hai sau assert status.
