# API-1 — Nhóm test **Schema Validation** (Contract testing)

**API:** API-1 · **Endpoint:** `GET /api/products/:id` (detail) và `GET /api/products` (list)
**Kỹ thuật:** JSON Schema validation qua `pm.response.to.have.jsonSchema(...)` + kiểm Content-Type & response time
**Ngày lập:** 22/08/2026 · **Schema đã kiểm chứng bắt đúng BUG-01/02 bằng `jsonschema` (Draft-07)**

> TC-ID nối tiếp: nhóm này bắt đầu từ **TC-P1-059**.
> Schema tái sử dụng đặt tại `postman/schemas/product.schema.json` và `product-list.schema.json`
> (import vào collection dưới dạng biến để `pm.response.to.have.jsonSchema` dùng lại).

---

## 1. JSON Schema — response **detail** (`GET /api/products/:id`)

Contract theo **FR-06**: object có **đúng 6 field**, **không dư field lạ** (`additionalProperties: false`),
`price` **bắt buộc là number**.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "product.schema.json",
  "title": "Product (response của GET /api/products/:id)",
  "type": "object",
  "additionalProperties": false,
  "required": ["id", "name", "price", "description", "imageUrl", "category_id"],
  "properties": {
    "id":          { "type": "integer", "minimum": 1 },
    "name":        { "type": "string", "minLength": 1, "maxLength": 255 },
    "price":       { "type": "number", "minimum": 0 },
    "description": { "type": ["string", "null"] },
    "imageUrl":    { "type": ["string", "null"] },
    "category_id": { "type": ["integer", "null"], "minimum": 1 }
  }
}
```

**Hai chốt chặn quan trọng của schema này:**
- `"additionalProperties": false` → **fail nếu response dư bất kỳ field lạ** nào (vd lỡ trả `role`, `password` do lỗi UNION/join).
- `"price": { "type": "number" }` → **fail nếu `price` là string** — đây là cách bắt **BUG-01** một cách tự động, không phải so sánh giá trị thủ công.

> **Lưu ý draft:** Postman dùng **tv4** (JSON Schema draft-4) hoặc **Ajv** tùy phiên bản. `additionalProperties: false`
> và `type` mảng (`["string","null"]`) đều được cả hai hỗ trợ. Nếu collection cấu hình Ajv, khai báo
> `"$schema": "http://json-schema.org/draft-07/schema#"`; nếu tv4 thì bỏ dòng `$schema` cũng chạy.

### Kiểm chứng schema (đã chạy `jsonschema` Draft-07)

| Input | Kỳ vọng | Kết quả validate |
|-------|---------|------------------|
| `id=1` (price=`30000000` number) | PASS | ✅ PASS |
| `id=2` (price=`"28000000"` string) | FAIL | ❌ FAIL — `'28000000' is not of type 'number'` |
| `{}` (id không tồn tại) | FAIL | ❌ FAIL — thiếu cả 6 required field |
| object có thêm field `role` | FAIL | ❌ FAIL — `Additional properties are not allowed ('role' was unexpected)` |

⇒ Schema **phân biệt đúng** product hợp lệ với các dạng lỗi. Case FAIL trên SUT là bug thật, không phải schema sai.

---

## 2. JSON Schema — response **list** (`GET /api/products[?search=]`)

Contract theo **FR-05**: **mảng** các Product; mảng rỗng khi không khớp.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "product-list.schema.json",
  "type": "array",
  "items": { "$ref": "product.schema.json" }
}
```

> Trong Postman, vì `$ref` liên file khó dùng, dùng bản **inline** (nhúng `product` vào `items`):
> ```js
> const productSchema = pm.collectionVariables.get("productSchema");   // object đã lưu ở Setup
> const listSchema = { type: "array", items: JSON.parse(productSchema) };
> pm.test("List khớp schema", () => pm.response.to.have.jsonSchema(listSchema));
> ```

---

## 3. Đoạn script Postman dùng chung (đặt ở tab Tests)

```js
// --- Schema (nạp 1 lần ở request Setup, lưu vào collectionVariables) ---
const productSchema = JSON.parse(pm.collectionVariables.get("productSchema"));

// TC schema detail
pm.test("Content-Type là application/json", () =>
  pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json"));

pm.test("Response time < 2000ms", () =>
  pm.expect(pm.response.responseTime).to.be.below(2000));

pm.test("Body khớp JSON Schema Product (đúng 6 field, price là number, không dư)", () =>
  pm.response.to.have.jsonSchema(productSchema));

pm.test("price là number (chốt riêng cho BUG-01)", () => {
  const b = pm.response.json();
  pm.expect(b.price, "price phải là number").to.be.a("number");
});
```

---

## 4. Test cases

Header chung mọi case: `X-Student-Id: 23127438`. `GET` ⇒ `Body` rỗng.

### 4.1 Schema — detail (`:id`)

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-P1-059 | API-1 | FR-06 | Schema (happy, id lẻ) | PRE-1 | `GET /api/products/1` | — | — | `200` | `pm.response.to.have.jsonSchema(productSchema)` PASS; body đúng 6 field; `typeof price==="number"` | **P0** |
| TC-P1-060 | API-1 | FR-06 | Schema (id lẻ khác) | PRE-1 | `GET /api/products/3` | — | — | `200` | jsonSchema PASS; `price` number | P1 |
| TC-P1-061 | API-1 | FR-06 | Schema (id lẻ, biên max) | PRE-1 | `GET /api/products/5` | — | — | `200` | jsonSchema PASS; `price` number | P1 |
| TC-P1-062 | API-1 | FR-06 | **Schema (id CHẴN — bắt BUG-01)** | PRE-1 | `GET /api/products/2` | — | — | `200` | jsonSchema PASS; **`typeof price==="number"`**. Contract yêu cầu number; nếu SUT trả `"28000000"` (string) ⇒ **FAIL đúng chỗ** | **P0** |
| TC-P1-063 | API-1 | FR-06 | **Schema (id CHẴN khác)** | PRE-1 | `GET /api/products/4` | — | — | `200` | jsonSchema PASS; `price` number | **P0** |
| TC-P1-064 | API-1 | FR-06 | Schema — **no extra field** | PRE-1 | `GET /api/products/3` | — | — | `200` | `additionalProperties:false` PASS — body **không** chứa field ngoài 6 field contract (bắt lỗi dư `password/role` nếu có) | P1 |
| TC-P1-065 | API-1 | FR-06 | Schema — **required đầy đủ** | PRE-1 | `GET /api/products/99999` | — | — | `404` | Theo contract: `404` + `{error}`. **Assertion phụ:** body **không** phải object rỗng `{}` khớp Product (SUT trả `200 {}` ⇒ vừa sai status vừa fail schema Product ⇒ map BUG-02) | **P0** |
| TC-P1-066 | API-1 | FR-06 | Content-Type | PRE-1 | `GET /api/products/1` | — | — | `200` | `Content-Type` chứa `application/json; charset=utf-8` | P2 |
| TC-P1-067 | API-1 | FR-06 | Response time | PRE-1 | `GET /api/products/1` | — | — | `200` | `pm.response.responseTime < 2000` | P2 |
| TC-P1-068 | API-1 | FR-06 | Field type — `id` | PRE-1 | `GET /api/products/1` | — | — | `200` | `typeof body.id === "number"` và `Number.isInteger(body.id)` | P2 |
| TC-P1-069 | API-1 | FR-06 | Field type — `category_id` | PRE-1 | `GET /api/products/1` | — | — | `200` | `body.category_id` là integer ≥ 1 (hoặc null); không phải string | P2 |
| TC-P1-070 | API-1 | FR-06 | **Data-driven schema (matrix chẵn/lẻ)** | PRE-1 + `product-ids.csv` (id=1..5) | `GET /api/products/{{id}}` | — | — | `200` × 5 | **Cả 5 iteration** phải PASS `jsonSchema(productSchema)`. Kết quả: id lẻ PASS, **id chẵn FAIL** ⇒ 1 case tổng hợp chứng minh BUG-01 mang tính hệ thống | **P0** |

### 4.2 Schema — list (`?search=`)

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-P1-071 | API-1 | FR-05 | Schema list (đầy đủ) | PRE-1 | `GET /api/products` | — | — | `200` | `jsonSchema(listSchema)` PASS; `Array.isArray(body)`; đúng 5 phần tử | P1 |
| TC-P1-072 | API-1 | FR-05 | **Schema list — bắt BUG-01 diện rộng** | PRE-1 | `GET /api/products` | — | — | `200` | Mỗi phần tử `price` là number. **Đối chứng:** trong list, id chẵn `price` là number (SUT đúng ở list) — trái với detail ⇒ chứng minh lỗi ở handler detail. Xem TC-P1-021 | P1 |
| TC-P1-073 | API-1 | FR-05 | Schema list (empty) | PRE-1 | `GET /api/products?search=zzzzz` | — | — | `200` | `jsonSchema(listSchema)` PASS với mảng **rỗng** `[]`; không `null`, không object | P1 |
| TC-P1-074 | API-1 | FR-05 | Content-Type + time (list) | PRE-1 | `GET /api/products` | — | — | `200` | `Content-Type` application/json; `responseTime < 2000` | P2 |

**Tổng nhóm schema: 16 test case** (TC-P1-059 → 074).
API-1 tổng cộng: **44 (EP/BVA) + 14 (Security) + 16 (Schema) = 74 test case** — vượt xa mốc ≥35/API.

---

## Phụ lục — Hành vi SUT đã probe & verdict

> Đã đối chiếu với dữ liệu probe live (`localhost:3000`, DB seed) và kiểm chứng schema bằng `jsonschema` Draft-07.

| TC-ID | Input | Expected (contract) | **Actual (SUT)** | Verdict | Bug |
|-------|-------|---------------------|------------------|---------|-----|
| 059 | `id=1` | schema PASS, price number | `price=30000000` (number), 6 field | ✅ PASS | — |
| 060 | `id=3` | schema PASS | `price=45000000` (number) | ✅ PASS | — |
| 061 | `id=5` | schema PASS | `price=4000000` (number) | ✅ PASS | — |
| **062** | `id=2` | price **number** | `price="28000000"` (**string**) | ❌ **FAIL** | **BUG-01** |
| **063** | `id=4` | price **number** | `price="6000000"` (**string**) | ❌ **FAIL** | **BUG-01** |
| 064 | `id=3` no-extra | không dư field | đúng 6 field, không dư | ✅ PASS | — |
| **065** | `id=99999` | `404` + `{error}` | `200` + `{}` (fail cả status lẫn schema Product) | ❌ **FAIL** | **BUG-02** |
| 066 | `id=1` CT | application/json | `application/json; charset=utf-8` | ✅ PASS | — |
| 067 | `id=1` time | < 2000ms | ~0.9ms | ✅ PASS | — |
| 068 | `id=1` type id | integer | `1` (integer) | ✅ PASS | — |
| 069 | `id=1` type category_id | integer | `1` (integer) | ✅ PASS | — |
| **070** | matrix id 1–5 | 5× schema PASS | id lẻ PASS, id chẵn (2,4) FAIL | ❌ **FAIL** 2/5 | **BUG-01** |
| 071 | list | schema list PASS, 5 phần tử | 5 phần tử hợp lệ | ✅ PASS | — |
| 072 | list price type | mọi phần tử price number | tất cả number (kể cả id chẵn) | ✅ PASS | — |
| 073 | `search=zzzzz` | list rỗng | `[]` | ✅ PASS | — |
| 074 | list CT+time | json, <2000ms | json, ~1ms | ✅ PASS | — |

**Kết luận nhóm schema:** 16 case → **4 FAIL / 12 PASS**, ánh xạ **BUG-01** (id chẵn: 062/063/070) và **BUG-02** (065).
Điểm mạnh của cách tiếp cận schema: chỉ một `jsonSchema(productSchema)` bắt được **đồng thời** cả lỗi kiểu (`price` string), thiếu field (`{}`) và dư field lạ — thay vì viết rời từng assertion.

> **Đối chứng chốt hạ (list vs detail):** TC-P1-072 cho thấy trong **list**, `price` của id chẵn là **number**;
> nhưng TC-P1-062 cho thấy trong **detail**, cùng product đó `price` là **string**. Cùng một dữ liệu DB,
> hai endpoint khác kiểu ⇒ bằng chứng lỗi nằm ở **handler detail** (`server.js:161`
> `if (row.id % 2 === 0) row.price = row.price.toString()`), không phải ở tầng DB.
