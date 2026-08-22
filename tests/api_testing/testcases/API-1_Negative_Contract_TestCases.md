# API-1 — Nhóm test **Negative / Contract** (sai method · content negotiation · header)

**API:** API-1 · **Endpoint:** `GET /api/products/:id` và `GET /api/products`
**Kỹ thuật:** Negative testing (HTTP method, header) + kiểm tra contract định dạng phản hồi
**Ngày lập:** 22/08/2026 · **Đã probe live trên `localhost:3000`, DB restore sau mỗi lần chạy**

> TC-ID nối tiếp: nhóm này bắt đầu từ **TC-P1-075**. Đây là nhóm **chốt** API-1.

---

## PRE — Tiền đề

| Mã | Nội dung |
|----|----------|
| **PRE-1** | Backend `node server.js` tại `http://localhost:3000`, DB seed sạch (5 products id 1–5). |
| **PRE-DESTRUCT** | ⚠ TC-P1-078 gửi `DELETE /api/products/1` — **route này CÓ tồn tại và thực sự XOÁ** product. Phải backup `database.sqlite` trước, restore sau; hoặc chạy ở cuối suite kèm teardown re-seed. **Không** để case này chạy lẫn trước các case đọc product 1. |

Header chung mọi case (trừ nhóm 3): `X-Student-Id: 23127438`.

---

## 1. Bản đồ method của các route sản phẩm (đã probe — trả lời câu "route có tồn tại không?")

| URL | Method | Route tồn tại? | HTTP thực tế | Ghi chú |
|-----|--------|----------------|--------------|---------|
| `/api/products/:id` | **GET** | ✅ (API-1) | `200` JSON | endpoint đang test |
| `/api/products/:id` | **PUT** | ✅ (API-3 update) | `200` JSON | cập nhật product |
| `/api/products/:id` | **DELETE** | ✅ (products delete) | `200` JSON — **XOÁ thật** | không auth (thuộc BUG-07) |
| `/api/products/:id` | **POST** | ❌ không có | `404` **HTML** | Express default handler |
| `/api/products/:id` | **PATCH** | ❌ không có | `404` **HTML** | Express default handler |
| `/api/products` | **GET** | ✅ (API-1 list) | `200` JSON array | — |
| `/api/products` | **POST** | ✅ (API-3 create) | `200` JSON | tạo product |
| `/api/products` | **PUT** | ❌ không có | `404` **HTML** | — |
| `/api/products` | **DELETE** | ❌ không có | `404` **HTML** | — |

> **Trả lời trực tiếp câu hỏi trong prompt:** `POST /api/products/1` **KHÔNG** tồn tại → `404` (HTML).
> Nhưng `DELETE /api/products/1` **CÓ** tồn tại và **destructive** — cần cẩn trọng khi test.

---

## 2. Test cases

### 2.1 Sai HTTP method

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-P1-075 | API-1 | FR-06 | Negative method — POST lên detail | PRE-1 | `POST /api/products/1` | `Content-Type: application/json` | `{}` | `404` **hoặc** `405` | Route không tồn tại. **Assertion contract:** body là **JSON** `{error:...}`, `Content-Type: application/json`. (SUT trả `404` **HTML** ⇒ FAIL contract) | P1 |
| TC-P1-076 | API-1 | FR-06 | Negative method — PATCH lên detail | PRE-1 | `PATCH /api/products/1` | `Content-Type: application/json` | `{}` | `404`/`405` | Như TC-075: JSON, không HTML | P2 |
| TC-P1-077 | API-1 | FR-05 | Negative method — PUT lên collection | PRE-1 | `PUT /api/products` | `Content-Type: application/json` | `{}` | `404`/`405` | JSON `{error}`, không HTML | P2 |
| TC-P1-078 | API-1 | FR-06 | Negative method — DELETE lên detail | PRE-1 + **PRE-DESTRUCT** | `DELETE /api/products/1` | — | — | `405` (theo contract API-1: detail chỉ đọc) **hoặc** `401/403` | ⚠ **Case đối chứng, chạy có kiểm soát.** Route DELETE tồn tại + **không auth** ⇒ xoá product không cần đăng nhập. **Assertion:** kỳ vọng bị chặn; SUT trả `200 {"message":"Product deleted"}` ⇒ **FAIL** (map **BUG-07**). Sau case: teardown re-seed / restore DB | P1 |

### 2.2 Content negotiation (`Accept`)

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-P1-079 | API-1 | FR-06 | Content negotiation — XML | PRE-1 | `GET /api/products/1` | `Accept: application/xml` | — | `200` (hoặc `406`) | API chỉ hỗ trợ JSON. **Assertion:** `Content-Type` là `application/json` và body vẫn là JSON hợp lệ — API **không** tự đổi sang XML. (Khẳng định hành vi, **không** phải bug) | P2 |
| TC-P1-080 | API-1 | FR-06 | Content negotiation — HTML | PRE-1 | `GET /api/products/1` | `Accept: text/html` | — | `200` | `Content-Type: application/json`; body JSON, không phải trang HTML | P2 |
| TC-P1-081 | API-1 | FR-06 | Content negotiation — text/plain | PRE-1 | `GET /api/products/1` | `Accept: text/plain` | — | `200` | `Content-Type: application/json`; body JSON | P3 |

### 2.3 Header `X-Student-Id`

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-P1-082 | API-1 | FR-06 | Thiếu `X-Student-Id` | PRE-1 | `GET /api/products/1` | *(cố tình KHÔNG gửi X-Student-Id)* | — | `200` | SUT **không** yêu cầu header này (đây là yêu cầu của HW06, không phải của SUT) ⇒ vẫn trả product bình thường. **Assertion:** `200` + schema Product. *(Case này chứng minh header không ảnh hưởng response; bằng chứng anti-cheat nằm ở pre-request script + console log, không phải ở phía server)* | P3 |
| TC-P1-083 | API-1 | FR-06 | Có `X-Student-Id` (đối chứng) | PRE-1 | `GET /api/products/1` | `X-Student-Id: 23127438` | — | `200` | Cùng kết quả TC-082 (response không đổi khi có/không header) ⇒ khẳng định SUT bỏ qua header, không rò rỉ hành vi theo StudentID | P3 |

**Tổng nhóm negative/contract: 9 test case** (TC-P1-075 → 083).

---

## 3. Tổng kết API-1 (đủ 4 nhóm)

| Nhóm | File | Số case | TC-ID |
|------|------|---------|-------|
| Equivalence Partitioning + BVA | `API-1_TestCases.md` | 44 | 001–044 |
| Security (SEC-04/05 + rò rỉ) | `API-1_Security_TestCases.md` | 14 | 045–058 |
| Schema validation | `API-1_Schema_TestCases.md` | 16 | 059–074 |
| Negative / Contract | *(file này)* | 9 | 075–083 |
| **Tổng API-1** | | **83** | **TC-P1-001 → 083** |

---

## Phụ lục — Hành vi SUT đã probe & verdict

> Đã chạy `node server.js` tại `localhost:3000`; `DELETE` chạy có backup/restore; các GET không làm bẩn dữ liệu.

| TC-ID | Input | Expected (contract) | **Actual (SUT)** | Verdict | Bug |
|-------|-------|---------------------|------------------|---------|-----|
| **075** | `POST /api/products/1` | `404`/`405` + JSON | `404` + **HTML** (`<!DOCTYPE html>...Cannot POST`), `text/html` | ❌ **FAIL** (route đúng là không tồn tại, nhưng lỗi phải là JSON) | **BUG-15** |
| **076** | `PATCH /api/products/1` | `404`/`405` + JSON | `404` + **HTML** | ❌ **FAIL** | **BUG-15** |
| **077** | `PUT /api/products` | `404`/`405` + JSON | `404` + **HTML** | ❌ **FAIL** | **BUG-15** |
| **078** | `DELETE /api/products/1` | `405`/`401`/`403` (bị chặn) | `200` + `{"message":"Product deleted"}` — **product bị xoá thật, không cần auth** | ❌ **FAIL nghiêm trọng** | **BUG-07** |
| 079 | `Accept: application/xml` | `200` JSON (không đổi định dạng) | `200` + `application/json`, body JSON | ✅ PASS | — |
| 080 | `Accept: text/html` | `200` JSON | `200` + `application/json` | ✅ PASS | — |
| 081 | `Accept: text/plain` | `200` JSON | `200` + `application/json` | ✅ PASS | — |
| 082 | thiếu `X-Student-Id` | `200` (SUT bỏ qua header) | `200` + product đầy đủ | ✅ PASS | — |
| 083 | có `X-Student-Id` | `200`, giống 082 | `200` + product đầy đủ, y hệt | ✅ PASS | — |

**Kết luận nhóm negative/contract:** 9 case → **4 FAIL / 5 PASS**.
- **FAIL** (075/076/077 → BUG-15): mọi lỗi 404 trả **HTML** thay vì JSON — phá contract "API luôn trả JSON".
- **FAIL nghiêm trọng** (078 → BUG-07): `DELETE /api/products/:id` xoá product **không cần xác thực** — đây là hệ quả của cùng lỗ hổng thiếu middleware ở nhóm route sản phẩm (POST/PUT/DELETE đều thiếu `authenticateToken`).
- **PASS**: content negotiation (SUT nhất quán trả JSON — hợp lý cho API JSON thuần) và `X-Student-Id` (SUT bỏ qua đúng như kỳ vọng — header là yêu cầu của HW06, bằng chứng anti-cheat lấy từ pre-request console log).

> **Ghi chú về `405` vs `404`:** Với URL **có tồn tại** nhưng method không hỗ trợ, chuẩn REST khuyến nghị
> `405 Method Not Allowed` kèm header `Allow`. Express mặc định trả `404` cho mọi route không khớp
> (không phân biệt "path sai" với "method sai"). Đây là **observation** về chất lượng contract, đã gộp
> chung vào BUG-15 (lỗi định dạng lỗi 404), không tách bug riêng để tránh phóng đại.
