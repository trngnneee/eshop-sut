# API-3 — Nhóm test **Schema Validation** (contract response tạo/sửa)

**API:** API-3 · **Endpoints:** `POST /api/products` (tạo), `PUT /api/products/:id` (sửa)
**Kỹ thuật:** JSON Schema validation (`pm.response.to.have.jsonSchema`) + assert status + response time
**Ngày lập:** 22/08/2026 · **Schema kiểm chứng bằng `jsonschema` Draft-07**

> TC-ID nối tiếp: nhóm này **TC-P3-062 → 072**. Nhóm **chốt** API-3 (đủ 4 nhóm: validation · security · schema · negative).
> Schema tái dùng: `postman/schemas/created-response.schema.json` (tạo), `message-response.schema.json` (sửa), `error-response.schema.json` (lỗi).

---

## 1. JSON Schema

### 1.1 Create success — `{message: string, id: number}`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "created-response.schema.json",
  "type": "object",
  "additionalProperties": false,
  "required": ["message", "id"],
  "properties": {
    "message": { "type": "string", "minLength": 1 },
    "id": { "type": "integer", "minimum": 1 }
  }
}
```

### 1.2 Update success — `{message: string}` (PUT chỉ trả message, KHÔNG có id)

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

**Chốt chặn:** `additionalProperties:false` + `id:integer`. Create phải có `id` **kiểu số**; PUT **không được** dư `id`.

### Kiểm chứng schema (đã chạy `jsonschema` Draft-07)

| Input | Schema | Kỳ vọng | Kết quả |
|-------|--------|---------|---------|
| `{"message":"Product created","id":6}` | created | PASS | ✅ PASS |
| `{"message":"Product created"}` | created | FAIL | ❌ `'id' is a required property` |
| `{"message":"x","id":"6"}` | created | FAIL | ❌ `'6' is not of type 'integer'` |
| `{"message":"x","id":6,"extra":1}` | created | FAIL | ❌ `Additional properties ('extra')` |
| `{"message":"Product updated"}` | message | PASS | ✅ PASS |
| `{"message":"Product updated","id":1}` | message | FAIL | ❌ `Additional properties ('id')` |

---

## 2. Script Postman dùng chung

```js
const createdSchema = JSON.parse(pm.collectionVariables.get("createdSchema")); // {message,id}
const msgSchema     = JSON.parse(pm.collectionVariables.get("messageSchema")); // {message}

pm.test("Content-Type application/json", () =>
  pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json"));
pm.test("Response time < 2000ms", () =>
  pm.expect(pm.response.responseTime).to.be.below(2000));

// POST create:
pm.test("status 200", () => pm.response.to.have.status(200));
pm.test("body khớp {message,id}", () => pm.response.to.have.jsonSchema(createdSchema));
pm.test("id là số dùng được", () => {
  pm.expect(pm.response.json().id).to.be.a("number");
  pm.collectionVariables.set("lastProductId", pm.response.json().id); // chain sang GET/PUT/DELETE
});
```

---

## 3. Test cases

Header chung: `X-Student-Id: 23127438` (+ `Bearer {{adminToken}}`). Payload hợp lệ theo PRE-VALID (API-3 validation file).

### 3.1 Schema create `{message,id}`

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Expected status | Expected / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|-----------------|--------------------------|----------|
| TC-P3-062 | API-3 | FR-15 | Schema create | PRE-1 | `POST /api/products` (body hợp lệ) | `200` | `jsonSchema(createdSchema)` PASS; đúng 2 field `message`+`id`; `typeof id==="number"`; `id≥1` | **P0** |
| TC-P3-063 | API-3 | FR-15 | id dùng được (chain) | PRE-1 | `POST /api/products` rồi `GET /api/products/{{id}}` | `200` cả hai | `id` trả về **trỏ tới record vừa tạo**: GET theo id đó trả đúng product | P1 |
| TC-P3-064 | API-3 | FR-15 | Content-Type + time (create) | PRE-1 | `POST /api/products` | `200` | `Content-Type` chứa `application/json`; `responseTime < 2000` | P2 |
| TC-P3-065 | API-3 | FR-15 | Create — không dư field | PRE-1 | `POST /api/products` | `200` | Response **chỉ** `message`+`id`, không dư (`additionalProperties:false`) | P2 |

### 3.2 Schema update `{message}`

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Expected status | Expected / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|-----------------|--------------------------|----------|
| TC-P3-066 | API-3 | FR-15 | Schema update | PRE-1, id=3 | `PUT /api/products/3` (body hợp lệ) | `200` | `jsonSchema(messageSchema)` PASS; đúng 1 field `message`; **không** có `id` | P1 |
| TC-P3-067 | API-3 | FR-15 | Content-Type + time (update) | PRE-1, id=3 | `PUT /api/products/3` | `200` | `application/json`; `responseTime < 2000` | P2 |

### 3.3 Schema error `{error}` (đối chiếu — khi validation đúng, lỗi phải theo schema error)

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Expected status | Expected / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|-----------------|--------------------------|----------|
| TC-P3-068 | API-3 | FR-15 | Error schema — input vi phạm | PRE-1 | `POST /api/products` `{"name":"","price":-1}` | **`400`** + `jsonSchema(errorSchema)` | Theo spec, input rác → `400` + `{error}`. SUT trả `200`+`{message,id}` ⇒ **FAIL** (BUG-08): sai cả status lẫn loại response | **P0** |
| TC-P3-069 | API-3 | FR-15 | Error schema — PUT not found | PRE-1 | `PUT /api/products/99999` | **`404`** + `jsonSchema(errorSchema)` | SUT trả `200`+`{message}` ⇒ FAIL (BUG-12): sai status + sai loại | P1 |
| TC-P3-070 | API-3 | SEC-02 | Error schema — auth | PRE-1 | `POST /api/products` *(không token)* | **`401`** + `jsonSchema(errorSchema)` | SUT trả `200`+`{message,id}` ⇒ FAIL (BUG-07) | **P0** |

### 3.4 Contract âm bản

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Expected status | Expected / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|-----------------|--------------------------|----------|
| TC-P3-071 | API-3 | FR-15 | Mutual-exclusion | PRE-1 | `POST /api/products` (hợp lệ) | `200` | Response là `{message,id}` **hoặc** `{error}`, không lẫn; assert bằng `additionalProperties:false` | P2 |
| TC-P3-072 | API-3 | FR-15 | Create response `id` khớp DB | PRE-1 | `POST` rồi `GET /api/products` (list) | `200` | `id` trả về = `id` của phần tử mới trong list (không lệch, không trùng) | P2 |

**Tổng nhóm schema API-3: 11 test case** (TC-P3-062 → 072).

---

## 4. Tổng kết API-3 (đủ 4 nhóm — chưa gồm Negative gộp)

| Nhóm | File | Số case | TC-ID |
|------|------|---------|-------|
| Input validation (Partition+BVA) | `API-3_TestCases.md` | 48 | 001–048 |
| Security (auth/role/forge/XSS) | `API-3_Security_TestCases.md` | 13 | 049–061 |
| Schema validation | *(file này)* | 11 | 062–072 |
| **Tổng API-3** | | **72** | **TC-P3-001 → 072** |

*(Nhóm Negative/Contract của API-3 phần lớn đã nằm trong validation file — TC-P3-043→046: route âm bản, malformed JSON, Content-Type. Có thể gộp hoặc tách nếu cần.)*

---

## Phụ lục — Hành vi SUT đã probe & verdict

> Response create/update lấy từ probe live nhóm validation (cùng SUT). Schema kiểm chứng Draft-07.

| TC-ID | Input | Expected (spec) | **Actual (SUT)** | Verdict | Bug |
|-------|-------|-----------------|------------------|---------|-----|
| 062 | POST hợp lệ | `200` + `{message,id}` | `200` `{"message":"Product created","id":N}` | ✅ PASS | — |
| 063 | id chain → GET | id trỏ record mới | GET theo id trả đúng product | ✅ PASS | — |
| 064 | CT + time | json, <2000ms | `application/json`, ~1ms | ✅ PASS | — |
| 065 | create no-extra | đúng 2 field | `{message,id}` không dư | ✅ PASS | — |
| 066 | PUT hợp lệ | `200` + `{message}` | `200` `{"message":"Product updated"}` (không id) | ✅ PASS | — |
| 067 | PUT CT+time | json, <2000ms | `application/json`, ~1ms | ✅ PASS | — |
| **068** | POST input rác | `400` + `{error}` | `200` + `{message,id}` (tạo record rác) | ❌ **FAIL** | **BUG-08** |
| **069** | PUT 99999 | `404` + `{error}` | `200` + `{message}` (no-op) | ❌ **FAIL** | **BUG-12** |
| **070** | POST không token | `401` + `{error}` | `200` + `{message,id}` | ❌ **FAIL** | **BUG-07** |
| 071 | mutual-exclusion | 1 loại response | các response đều đúng 1 loại | ✅ PASS | — |
| 072 | id khớp DB | id = phần tử mới | id khớp | ✅ PASS | — |

**Kết luận nhóm schema:** 11 case → **8 PASS / 3 FAIL**.
- **Contract response "đường hạnh phúc" SẠCH:** create trả đúng `{message,id}` (id number), update trả đúng `{message}` (không dư id) — **PASS**. SUT làm đúng shape response khi thành công.
- **3 FAIL** đều ở nhánh đáng-lẽ-lỗi: input rác (068/BUG-08), not-found (069/BUG-12), thiếu auth (070/BUG-07) — SUT trả `200`+response success thay vì `4xx`+`{error}`. Schema bắt được vì response **sai loại** (success thay vì error).

> **Điểm mạnh:** ở API-3, schema không bắt được bug ở nhánh success (vì shape đúng), nhưng bắt "gián tiếp" ở chỗ:
> đáng lẽ phải trả `{error}` thì SUT trả `{message,id}`. Assert schema-của-loại-đúng theo status kỳ vọng ⇒ lộ ra
> mọi bug validation/auth/not-found mà chỉ assert status có thể bỏ sót.
