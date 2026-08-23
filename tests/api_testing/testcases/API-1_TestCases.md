# API-1 — `GET /api/products/:id` · Test cases (Phân hoạch tương đương + Phân tích giá trị biên)

**API:** API-1 · **FR:** FR-05 (danh sách & tìm kiếm) / FR-06 (chi tiết sản phẩm)
**Kỹ thuật:** Equivalence Partitioning (EP) + Boundary Value Analysis (BVA)
**Endpoint chính:** `GET /api/products/:id` — **kèm** endpoint liền kề `GET /api/products?search=` để phủ đủ FR-05
**Auth:** không yêu cầu
**Ngày lập:** 22/08/2026

> **Nguyên tắc đặt Expected:** Expected lấy từ **contract** (`openapi.yaml` + FR trong `README.md` của SUT),
> **không** lấy từ hành vi quan sát được của SUT. Ví dụ: `id` không tồn tại → Expected = **404**,
> kể cả khi SUT thật trả `200 {}`. Chỗ lệch = bug (xem Phụ lục B).

---

## PRE — Tiền đề dùng chung

| Mã | Nội dung |
|----|----------|
| **PRE-1** | Backend chạy `node server.js` tại `http://localhost:3000`. DB vừa được reseed tự động: **3 categories (id 1–3)**, **5 products (id 1–5)**, bảng `orders` rỗng. |
| **PRE-2** | Không có test nào tạo/xoá product chạy trước (giữ nguyên tập seed id 1–5). Nếu chạy chung suite với API-3, phải chạy folder API-1 **trước**, hoặc restart server giữa 2 folder. |

Bảng seed dùng để đối chiếu:

| id | name | price | category_id |
|----|------|-------|-------------|
| 1 | iPhone 15 Pro Max | 30000000 | 1 |
| 2 | Samsung Galaxy S24 Ultra | 28000000 | 1 |
| 3 | MacBook Pro M3 | 45000000 | 2 |
| 4 | Tai nghe AirPods Pro 2 | 6000000 | 3 |
| 5 | Bàn phím cơ Keychron Q1 | 4000000 | 3 |

---

## 1. Bảng phân hoạch — Path param `:id`

Miền hợp lệ theo contract: **integer ≥ 1**, tồn tại trong bảng `products`.

| Class ID | Loại | Lớp tương đương / Giá trị biên | Đại diện | Lý do tách lớp | Expected (contract) |
|----------|------|-------------------------------|----------|----------------|---------------------|
| **V1** | Valid | id tồn tại, **số LẺ** | 1, 3, 5 | Nghi vấn có nhánh xử lý theo tính chẵn/lẻ ⇒ phải tách riêng khỏi V2 | `200` + object `Product`, `price` là **number** |
| **V2** | Valid | id tồn tại, **số CHẴN** | 2, 4 | Cùng lý do V1 — đây là lớp phát hiện lỗi kiểu dữ liệu | `200` + object `Product`, `price` là **number** |
| **B1** | Boundary | **biên dưới** của miền hợp lệ | 1 | min hợp lệ = 1 (AUTOINCREMENT bắt đầu từ 1) | `200` |
| **B2** | Boundary | **biên trên** tập dữ liệu tồn tại | 5 | id lớn nhất đang tồn tại | `200` |
| **B3** | Boundary | **biên trên + 1** | 6 | Ngay ngoài tập tồn tại — nhạy hơn 99999 | `404` |
| **B4** | Boundary | **biên dưới − 1** (zero) | 0 | 0 không thuộc miền `≥ 1` | `400` |
| **I1** | Invalid | id đúng kiểu nhưng **không tồn tại** | 99999 | Phân biệt "sai kiểu" vs "đúng kiểu nhưng không có" | `404` |
| **I2** | Invalid | số **âm** | -1 | Vi phạm `minimum: 1` | `400` |
| **I3** | Invalid | số **cực lớn** (vượt int64) | 9999999999999999999 | Tràn số / vượt `format: int64` | `400` |
| **I4** | Invalid | **số thực không nguyên** | 1.5 | Vi phạm `type: integer` | `400` |
| **I5** | Invalid | **số thực có phần thập phân = 0** | 1.0 | Lớp riêng: nhìn như số nguyên nhưng chuỗi không canonical ⇒ dễ bị ép kiểu ngầm | `400` (DEC-01: strict) |
| **I6** | Invalid | **chuỗi phi số** | abc | Sai kiểu hoàn toàn | `400` |
| **I7** | Invalid | **rỗng** (`/api/products/`) | *(trailing slash)* | Không còn là endpoint detail — Express khớp về route list | `200` + **array** (không phải object) |
| **I8** | Invalid | có **khoảng trắng đầu** | `%201` (`" 1"`) | Chuỗi không canonical, kiểm tra ép kiểu ngầm | `400` (DEC-01: strict) |
| **I9** | Invalid | có **khoảng trắng cuối** | `1%20` (`"1 "`) | Tách riêng khỏi I8 (leading vs trailing) | `400` (DEC-01: strict) |
| **I10** | Invalid | **dấu cộng phía trước** | `%2B1` (`"+1"`) | Dấu tường minh — không canonical | `400` (DEC-01: strict) |
| **I11** | Invalid | **zero đứng đầu** | `01` | Không canonical | `400` (DEC-01: strict) |
| **I12** | Invalid | **chuỗi cực dài** | 1000 ký tự `a` | Kiểm tra giới hạn độ dài / DoS nhẹ | `400` |

> **Ghi chú A — DEC-01: đã chốt STRICT** (22/08/2026 — ghi trong `openapi.yaml` › `getProductById` › `x-contract-decision`).
>
> Năm lớp **I5, I8, I9, I10, I11** đều là *"biểu diễn chuỗi không canonical của một số nguyên"*
> (`1.0`, `" 1"`, `"1 "`, `"+1"`, `"01"`). Hai cách đọc contract:
>
> | | Expected | Hệ quả |
> |---|---|---|
> | **STRICT** ✅ *(đã chọn)* | `400` cho cả 5 lớp | 5 case FAIL trên SUT ⇒ ánh xạ **BUG-14** |
> | Lenient | `200` + product 1 | 5 case PASS, BUG-14 không tồn tại |
>
> **Lý do chọn STRICT:**
> 1. **Nhất quán** — nếu nhận `1.0` thì buộc phải nhận cả `" 1"`, `"+1"`, `"01"`; không thể nhận cái này mà từ chối cái kia.
> 2. Việc ép kiểu là **hành vi rò rỉ từ tầng DB** lên tầng API (SQLite numeric affinity tự strip khoảng
>    trắng, bỏ dấu `+`, bỏ zero đứng đầu) — không phải quyết định thiết kế của API. Contract không nên
>    hợp thức hoá nó.
> 3. `type: integer` + `minimum: 1` đọc chặt ⇒ validator chuẩn (Postman `jsonSchema`,
>    `express-openapi-validator`) đều reject các dạng này.
>
> **Nếu sau này đổi sang lenient:** phải đổi **đồng thời** cả 5 case TC-P1-012/015/016/017/018 sang `200`
> **và** xoá BUG-14 khỏi `openapi.yaml` + bảng bug. Không được sửa lẻ.

---

## 2. Bảng phân hoạch — Query param `?search=` (`GET /api/products`)

Contract theo FR-05: *"Thanh tìm kiếm tìm theo **tên** sản phẩm"* ⇒ so khớp **substring trên `name`**, xử lý ký tự người dùng nhập như **văn bản thuần** (literal), không phải cú pháp truy vấn.

| Class ID | Loại | Lớp tương đương | Đại diện | Lý do tách lớp | Expected (contract) |
|----------|------|-----------------|----------|----------------|---------------------|
| **SV1** | Valid | **không truyền** param | *(no param)* | Đường cơ sở — trả toàn bộ | `200` + array 5 phần tử |
| **SV2** | Valid | param **rỗng** | `search=` | Rỗng ≠ không truyền: cần khẳng định 2 nhánh cho cùng kết quả | `200` + array 5 phần tử |
| **SV3** | Valid | khớp **đúng 1** | `iPhone` | Nhánh 1 kết quả | `200` + array 1 (id=1) |
| **SV4** | Valid | khớp **nhiều** | `Pro` | Nhánh nhiều kết quả | `200` + array 3 (id 1,3,4) |
| **SV5** | Valid | **không khớp** | `zzzzz` | Empty state (FR-05) | `200` + array **rỗng** |
| **SV6** | Valid | khớp **toàn bộ tên** | `Keychron Q1` | Biên: chuỗi tìm = 1 phần tên đầy đủ | `200` + array 1 (id=5) |
| **SB1** | Boundary | **1 ký tự** | `i` | Biên dưới độ dài chuỗi tìm | `200` + array (khớp mọi tên chứa `i`) |
| **SB2** | Boundary | **chuỗi cực dài** (1000 ký tự) | `aaa…a` | Biên trên độ dài | `200` + array rỗng |
| **SC1** | Valid | **case-insensitive, ASCII** | `iphone` | Tìm kiếm phải không phân biệt hoa/thường | `200` + array 1 (id=1) |
| **SC2** | Valid | **case-insensitive, ASCII hoa** | `IPHONE` | Đối xứng với SC1 | `200` + array 1 (id=1) |
| **SU1** | Valid | **unicode có dấu, đúng case** | `Bàn phím` | Tên sản phẩm tiếng Việt | `200` + array 1 (id=5) |
| **SU2** | Valid | **unicode có dấu, chữ thường** | `bàn phím` | Case-fold trên ký tự ASCII trong chuỗi unicode | `200` + array 1 (id=5) |
| **SU3** | Valid | **unicode có dấu, CHỮ HOA** | `BÀN PHÍM` | **Lớp then chốt**: nếu SC1/SC2 không phân biệt hoa/thường thì unicode phải nhất quán | `200` + array 1 (id=5) |
| **SU4** | Valid | **unicode bỏ dấu** | `Ban phim` | FR-05 không yêu cầu tìm bỏ dấu ⇒ khẳng định hành vi, không phải bug | `200` + array rỗng |
| **SI1** | Invalid | **wildcard `%`** của LIKE | `%` | Ký tự đặc biệt của SQL LIKE phải được xử lý **literal** | `200` + array rỗng |
| **SI2** | Invalid | **wildcard `_`** của LIKE | `_` | Cùng lý do SI1, ký tự khác | `200` + array rỗng |
| **SI3** | Invalid | **nhiều wildcard** | `%%` | Tổ hợp — kiểm tra escape có triệt để | `200` + array rỗng |
| **SI4** | Invalid | **chỉ khoảng trắng** | `%20` (`" "`) | Spec không quy định trim ⇒ chỉ assert schema | `200` + array (không assert số lượng) |
| **SI5** | Invalid | **param lặp** | `search=Pro&search=Mac` | Express parse thành mảng ⇒ nguy cơ nối chuỗi sai | `200` + array 3 (dùng giá trị đầu) **hoặc** `400` |

> **Ngoài phạm vi bảng này:** payload SQL Injection (`' OR '1'='1`) và XSS trên `?search=` thuộc
> nhóm **Security (SEC-04/SEC-05)** — sẽ sinh ở bước Security, không trộn vào bảng EP/BVA.

---

## 3. Test cases

Header dùng chung cho **mọi** case: `X-Student-Id: 23127438` (inject bằng pre-request script ở cấp collection).
Cột `Headers` chỉ ghi phần **thêm vào**. Endpoint là `GET` nên `Body` luôn rỗng.

### 3.1 Nhóm `:id` — Valid & Boundary

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / schema | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|------------------------|----------|
| TC-P1-001 | API-1 | FR-06 | EP-V1 + BVA-B1 | PRE-1 | `GET /api/products/1` | — | — | `200` | Object khớp schema `Product`, đủ 6 field; `id=1`; `name="iPhone 15 Pro Max"`; **`typeof price === "number"`**; `price=30000000` | P1 |
| TC-P1-002 | API-1 | FR-06 | EP-V1 | PRE-1 | `GET /api/products/3` | — | — | `200` | `id=3`; `typeof price === "number"`; `price=45000000` | P2 |
| TC-P1-003 | API-1 | FR-06 | EP-V1 + BVA-B2 | PRE-1 | `GET /api/products/5` | — | — | `200` | `id=5`; `typeof price === "number"`; `price=4000000` | P1 |
| TC-P1-004 | API-1 | FR-06 | **EP-V2** | PRE-1 | `GET /api/products/2` | — | — | `200` | `id=2`; **`typeof price === "number"`** (⚠ case bắt BUG-01); `price=28000000` | **P0** |
| TC-P1-005 | API-1 | FR-06 | **EP-V2** | PRE-1 | `GET /api/products/4` | — | — | `200` | `id=4`; **`typeof price === "number"`**; `price=6000000` | **P0** |
| TC-P1-006 | API-1 | FR-06 | BVA-B3 | PRE-1 | `GET /api/products/6` | — | — | `404` | `{ "error": <string> }` — **không** phải `{}` | P1 |

### 3.2 Nhóm `:id` — Invalid

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / schema | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|------------------------|----------|
| TC-P1-007 | API-1 | FR-06 | EP-I1 | PRE-1 | `GET /api/products/99999` | — | — | `404` | `{ "error": <string> }`. Assert **`pm.response.code === 404`**, không assert `{}` | **P0** |
| TC-P1-008 | API-1 | FR-06 | BVA-B4 | PRE-1 | `GET /api/products/0` | — | — | `400` | `{ "error": <string> }` | P1 |
| TC-P1-009 | API-1 | FR-06 | EP-I2 | PRE-1 | `GET /api/products/-1` | — | — | `400` | `{ "error": <string> }` | P1 |
| TC-P1-010 | API-1 | FR-06 | EP-I3 | PRE-1 | `GET /api/products/9999999999999999999` | — | — | `400` | `{ "error": <string> }`; không `500`, không leak stack trace | P1 |
| TC-P1-011 | API-1 | FR-06 | EP-I4 | PRE-1 | `GET /api/products/1.5` | — | — | `400` | `{ "error": <string> }` | P2 |
| TC-P1-012 | API-1 | FR-06 | EP-I5 | PRE-1 | `GET /api/products/1.0` | — | — | `400` | `{ "error": <string> }`. Theo **DEC-01 (strict)**: `1.0` không phải dạng canonical của integer | P2 |
| TC-P1-013 | API-1 | FR-06 | EP-I6 | PRE-1 | `GET /api/products/abc` | — | — | `400` | `{ "error": <string> }` | P1 |
| TC-P1-014 | API-1 | FR-05 | EP-I7 | PRE-1 | `GET /api/products/` | — | — | `200` | **Array** 5 phần tử (Express khớp về route list, không phải detail). Assert `Array.isArray(body) === true` | P2 |
| TC-P1-015 | API-1 | FR-06 | EP-I8 | PRE-1 | `GET /api/products/%201` | — | — | `400` | `{ "error": <string> }`. Theo **DEC-01 (strict)** | P2 |
| TC-P1-016 | API-1 | FR-06 | EP-I9 | PRE-1 | `GET /api/products/1%20` | — | — | `400` | `{ "error": <string> }`. Theo **DEC-01 (strict)** | P2 |
| TC-P1-017 | API-1 | FR-06 | EP-I10 | PRE-1 | `GET /api/products/%2B1` | — | — | `400` | `{ "error": <string> }`. Theo **DEC-01 (strict)** | P2 |
| TC-P1-018 | API-1 | FR-06 | EP-I11 | PRE-1 | `GET /api/products/01` | — | — | `400` | `{ "error": <string> }`. Theo **DEC-01 (strict)** | P2 |
| TC-P1-019 | API-1 | FR-06 | EP-I12 + BVA | PRE-1 | `GET /api/products/aaa…a` (1000 ký tự) | — | — | `400` | `{ "error": <string> }`; response time < 2000ms (không treo) | P2 |

### 3.3 Nhóm `:id` — Contract & nhất quán (cross-cutting)

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / schema | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|------------------------|----------|
| TC-P1-020 | API-1 | FR-06 | EP-V1+V2 (data-driven) | PRE-1 + data file `product-ids.csv` = 1,2,3,4,5 | `GET /api/products/{{id}}` | — | — | `200` × 5 | **Với cả 5 iteration**: `typeof price === "number"`. Case tổng hợp bắt BUG-01 trên toàn matrix chẵn/lẻ | **P0** |
| TC-P1-021 | API-1 | FR-06 | Cross-endpoint consistency | PRE-1 | `GET /api/products` **rồi** `GET /api/products/2` | — | — | `200` cả hai | `price` của product id=2 phải **cùng kiểu** ở list và ở detail. (Case này chứng minh lỗi nằm ở handler detail, không phải ở DB) | **P0** |
| TC-P1-022 | API-1 | FR-06 | Contract | PRE-1 | `GET /api/products/1` | — | — | `200` | Header `Content-Type` chứa `application/json` | P2 |
| TC-P1-023 | API-1 | FR-06 | Contract | PRE-1 | `GET /api/products/1` | — | — | `200` | Response time < 2000ms | P2 |
| TC-P1-024 | API-1 | FR-06 | Schema (strict) | PRE-1 | `GET /api/products/3` | — | — | `200` | Body có **đúng 6 field** `id,name,price,description,imageUrl,category_id` — không thiếu, **không thừa** (`additionalProperties: false`) | P1 |
| TC-P1-025 | API-1 | FR-06 | Negative route | PRE-1 | `POST /api/products/1` | `Content-Type: application/json` | `{}` | `404` | Body là **JSON** `{ "error": <string> }`, `Content-Type: application/json`. (Route không tồn tại nhưng lỗi vẫn phải đúng contract, không trả HTML) | P2 |

### 3.4 Nhóm `?search=` (FR-05)

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / schema | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|------------------------|----------|
| TC-P1-026 | API-1 | FR-05 | EP-SV1 | PRE-1 | `GET /api/products` | — | — | `200` | Array **5** phần tử; mỗi phần tử khớp schema `Product` | P1 |
| TC-P1-027 | API-1 | FR-05 | EP-SV2 | PRE-1 | `GET /api/products?search=` | — | — | `200` | Array **5** phần tử (rỗng ≡ không truyền) | P2 |
| TC-P1-028 | API-1 | FR-05 | EP-SV3 | PRE-1 | `GET /api/products?search=iPhone` | — | — | `200` | Array **1**; `[0].id === 1` | P1 |
| TC-P1-029 | API-1 | FR-05 | EP-SV4 | PRE-1 | `GET /api/products?search=Pro` | — | — | `200` | Array **3**; tập id = `{1,3,4}` | P1 |
| TC-P1-030 | API-1 | FR-05 | EP-SV5 | PRE-1 | `GET /api/products?search=zzzzz` | — | — | `200` | Array **rỗng** `[]` (empty state), không phải `404`, không phải `null` | P1 |
| TC-P1-031 | API-1 | FR-05 | EP-SV6 | PRE-1 | `GET /api/products?search=Keychron Q1` | — | — | `200` | Array **1**; `[0].id === 5` | P2 |
| TC-P1-032 | API-1 | FR-05 | BVA-SB1 | PRE-1 | `GET /api/products?search=i` | — | — | `200` | Array; mọi phần tử có `name` chứa `i`/`I` | P2 |
| TC-P1-033 | API-1 | FR-05 | BVA-SB2 | PRE-1 | `GET /api/products?search=aaa…a` (1000 ký tự) | — | — | `200` | Array **rỗng**; response time < 2000ms | P2 |
| TC-P1-034 | API-1 | FR-05 | EP-SC1 | PRE-1 | `GET /api/products?search=iphone` | — | — | `200` | Array **1**; `[0].id === 1` (không phân biệt hoa/thường) | P1 |
| TC-P1-035 | API-1 | FR-05 | EP-SC2 | PRE-1 | `GET /api/products?search=IPHONE` | — | — | `200` | Array **1**; `[0].id === 1` | P2 |
| TC-P1-036 | API-1 | FR-05 | EP-SU1 | PRE-1 | `GET /api/products?search=Bàn phím` | — | — | `200` | Array **1**; `[0].id === 5` | P1 |
| TC-P1-037 | API-1 | FR-05 | EP-SU2 | PRE-1 | `GET /api/products?search=bàn phím` | — | — | `200` | Array **1**; `[0].id === 5` | P2 |
| TC-P1-038 | API-1 | FR-05 | **EP-SU3** | PRE-1 | `GET /api/products?search=BÀN PHÍM` | — | — | `200` | Array **1**; `[0].id === 5`. ⚠ Case bắt lỗi tìm kiếm không nhất quán với unicode | **P1** |
| TC-P1-039 | API-1 | FR-05 | EP-SU4 | PRE-1 | `GET /api/products?search=Ban phim` | — | — | `200` | Array **rỗng** (FR-05 không yêu cầu tìm bỏ dấu — khẳng định hành vi) | P2 |
| TC-P1-040 | API-1 | FR-05 | **EP-SI1** | PRE-1 | `GET /api/products?search=%25` | — | — | `200` | Array **rỗng** — `%` phải được xử lý **literal**, không phải wildcard SQL | **P0** |
| TC-P1-041 | API-1 | FR-05 | **EP-SI2** | PRE-1 | `GET /api/products?search=_` | — | — | `200` | Array **rỗng** — `_` phải literal | **P0** |
| TC-P1-042 | API-1 | FR-05 | EP-SI3 | PRE-1 | `GET /api/products?search=%25%25` | — | — | `200` | Array **rỗng** | P1 |
| TC-P1-043 | API-1 | FR-05 | EP-SI4 | PRE-1 | `GET /api/products?search=%20` | — | — | `200` | Array khớp schema. **Không assert số lượng** — spec không quy định trim (spec gap, ghi observation) | P2 |
| TC-P1-044 | API-1 | FR-05 | EP-SI5 | PRE-1 | `GET /api/products?search=Pro&search=Mac` | — | — | `200` | Array **rỗng** `[]`. Express gom `search` lặp thành mảng `['Pro','Mac']` → nội suy thành `LIKE '%Pro,Mac%'` → **0 kết quả** (thất bại im lặng). Đây là **BUG-18**, không phải "lấy giá trị đầu" | P2 |

**Tổng: 44 test case** (25 cho `:id`, 19 cho `?search=`) — đã vượt mốc ≥35/API chỉ bằng EP + BVA.
Các nhóm **Security (SEC-01…07)** và **Schema validation** sẽ bổ sung thêm ở bước sau.

---

## Phụ lục A — Ma trận phủ lớp tương đương

| Param | Số lớp | Lớp đã phủ | Test case |
|-------|--------|-----------|-----------|
| `:id` | 18 (V1,V2 · B1–B4 · I1–I12) | 18/18 ✅ | TC-P1-001 → 019 |
| `?search=` | 19 (SV1–SV6,SB1–SB2,SC1–SC2,SU1–SU4,SI1–SI5) | 19/19 ✅ | TC-P1-026 → 044 |
| Contract/nhất quán | — | — | TC-P1-020 → 025 |

Mỗi lớp có **≥1** đại diện; V1/V2 và các lớp P0 có **≥2** đại diện.

---

## Phụ lục B — Hành vi SUT đã probe & verdict dự kiến

> Đã chạy `node server.js` tại `localhost:3000` trên DB seed sạch; toàn bộ request là `GET` nên không làm bẩn dữ liệu.
> Bảng này dùng cho bước **Audit** và bước **Bug report** — **không** dùng để sửa cột Expected ở trên.

| TC-ID | Input | Expected (contract) | **Actual (SUT)** | Verdict dự kiến | Bug |
|-------|-------|---------------------|------------------|-----------------|-----|
| 001 | `id=1` | `200`, price number | `200`, `price=30000000` (number) | ✅ PASS | — |
| 002 | `id=3` | `200`, price number | `200`, `price=45000000` (number) | ✅ PASS | — |
| 003 | `id=5` | `200`, price number | `200`, `price=4000000` (number) | ✅ PASS | — |
| **004** | `id=2` | `200`, price **number** | `200`, `price="28000000"` (**string**) | ❌ **FAIL** | **BUG-01** |
| **005** | `id=4` | `200`, price **number** | `200`, `price="6000000"` (**string**) | ❌ **FAIL** | **BUG-01** |
| **006** | `id=6` | `404` | `200` + `{}` | ❌ **FAIL** | **BUG-02** |
| **007** | `id=99999` | `404` | `200` + `{}` | ❌ **FAIL** | **BUG-02** |
| **008** | `id=0` | `400` | `200` + `{}` | ❌ **FAIL** | **BUG-03** |
| **009** | `id=-1` | `400` | `200` + `{}` | ❌ **FAIL** | **BUG-03** |
| **010** | `id=9999999999999999999` | `400` | `200` + `{}` | ❌ **FAIL** | BUG-03 |
| **011** | `id=1.5` | `400` | `200` + `{}` | ❌ **FAIL** | BUG-03 |
| **012** | `id=1.0` | `400` | `200` + product **id=1** | ❌ **FAIL** | **BUG-14** |
| **013** | `id=abc` | `400` | `200` + `{}` | ❌ **FAIL** | **BUG-03** |
| 014 | `id` rỗng | `200` + array 5 | `200` + array 5 `[1,2,3,4,5]` | ✅ PASS | — |
| **015** | `id=" 1"` | `400` | `200` + product **id=1** | ❌ **FAIL** | **BUG-14** |
| **016** | `id="1 "` | `400` | `200` + product **id=1** | ❌ **FAIL** | **BUG-14** |
| **017** | `id="+1"` | `400` | `200` + product **id=1** | ❌ **FAIL** | **BUG-14** |
| **018** | `id="01"` | `400` | `200` + product **id=1** | ❌ **FAIL** | **BUG-14** |
| **019** | `id=` 1000 ký tự | `400` | `200` + `{}` | ❌ **FAIL** | BUG-03 |
| **020** | matrix id 1–5 | 5×price number | id chẵn → string, id lẻ → number | ❌ **FAIL** 2/5 | **BUG-01** |
| **021** | list vs detail, id=2 | cùng kiểu | list → **number**, detail → **string** | ❌ **FAIL** | **BUG-01** |
| 022 | header | `application/json` | `application/json; charset=utf-8` | ✅ PASS | — |
| 023 | response time | < 2000ms | ~0.9ms | ✅ PASS | — |
| 024 | schema strict | đúng 6 field | đúng 6 field | ✅ PASS | — |
| **025** | `POST /api/products/1` | `404` + JSON | `404` + **HTML** `text/html` | ❌ **FAIL** | **BUG-15** |
| 026 | no param | array 5 | array 5 | ✅ PASS | — |
| 027 | `search=` | array 5 | array 5 | ✅ PASS | — |
| 028 | `search=iPhone` | array 1 | array 1 `[1]` | ✅ PASS | — |
| 029 | `search=Pro` | array 3 `{1,3,4}` | array 3 `[1,3,4]` | ✅ PASS | — |
| 030 | `search=zzzzz` | array rỗng | array rỗng | ✅ PASS | — |
| 031 | `search=Keychron Q1` | array 1 `[5]` | array 1 `[5]` | ✅ PASS | — |
| 032 | `search=i` | array | array | ✅ PASS | — |
| 033 | `search=` 1000 ký tự | array rỗng | array rỗng | ✅ PASS | — |
| 034 | `search=iphone` | array 1 `[1]` | array 1 `[1]` | ✅ PASS | — |
| 035 | `search=IPHONE` | array 1 `[1]` | array 1 `[1]` | ✅ PASS | — |
| 036 | `search=Bàn phím` | array 1 `[5]` | array 1 `[5]` | ✅ PASS | — |
| 037 | `search=bàn phím` | array 1 `[5]` | array 1 `[5]` | ✅ PASS | — |
| **038** | `search=BÀN PHÍM` | array 1 `[5]` | array **rỗng** | ❌ **FAIL** | **BUG-16** |
| 039 | `search=Ban phim` | array rỗng | array rỗng | ✅ PASS | — |
| **040** | `search=%` | array rỗng | array **5** (toàn bộ) | ❌ **FAIL** | **BUG-17** |
| **041** | `search=_` | array rỗng | array **5** | ❌ **FAIL** | **BUG-17** |
| **042** | `search=%%` | array rỗng | array **5** | ❌ **FAIL** | **BUG-17** |
| 043 | `search=" "` | array (no count assert) | array 5 | ✅ PASS | — |
| **044** | `search=Pro&search=Mac` | array 3 hoặc `400` | array **rỗng** (nối thành `"Pro,Mac"`) | ❌ **FAIL** | **BUG-18** |

**Tổng kết dự kiến:** 44 case → **23 FAIL / 21 PASS**, ánh xạ tới **3 bug đã biết** (BUG-01/02/03) và **5 bug mới phát hiện** ở bước này (BUG-14 → BUG-18).

Phân bố bug trên các case FAIL: `BUG-01` × 4 · `BUG-02` × 2 · `BUG-03` × 6 · `BUG-14` × 5 · `BUG-15` × 1 · `BUG-16` × 1 · `BUG-17` × 3 · `BUG-18` × 1.

### Bug mới phát hiện (chưa có trong `openapi.yaml`)

| Bug | FR/SEC | Severity | Mô tả | Nguyên nhân gốc |
|-----|--------|----------|-------|-----------------|
| **BUG-14** | FR-06 | Minor/P2 | `:id` nhận mọi dạng chuỗi số **không canonical** (`1.0`, `" 1"`, `"1 "`, `"+1"`, `"01"`) và vẫn trả product id=1 với `200` | Route không validate param; SQLite **numeric affinity** tự strip khoảng trắng, bỏ dấu `+`, bỏ zero đứng đầu, ép `1.0`→`1` khi so với cột `id INTEGER`. Thuộc lớp lỗi *validation bị bỏ qua, DB tự cứu* — response trông hợp lệ nên rất dễ bỏ sót |
| **BUG-15** | FR-06 | Minor/P2 | Route không tồn tại trả `404` dạng **HTML** `text/html`, không phải JSON | Không có error-handler 404 tập trung ⇒ dùng handler mặc định của Express |
| **BUG-16** | FR-05 | **Major/P1** | Tìm kiếm **CHỮ HOA có dấu** không ra kết quả: `BÀN PHÍM` → 0, `bàn phím` → 1 | `LIKE` của SQLite chỉ case-fold **ASCII**, không fold Unicode ⇒ tìm kiếm tiếng Việt không nhất quán. Đây là lỗi trực tiếp với người dùng VN |
| **BUG-17** | FR-05 / SEC-05 | **Major/P1** | `search=%` hoặc `search=_` trả **toàn bộ** sản phẩm — bypass hoàn toàn bộ lọc | `server.js:144` nối chuỗi `LIKE '%${searchQuery}%'`, không escape wildcard. Cùng gốc với lỗ hổng SQLi (sẽ khai thác sâu ở bước Security) |
| **BUG-18** | FR-05 | Minor/P2 | Param `search` lặp → Express parse thành array → nối thành `"Pro,Mac"` → 0 kết quả, im lặng | Không validate `typeof req.query.search === 'string'` |

---

## Phụ lục C — Ghi chú cho bước tiếp theo

1. ✅ **XONG** — đã thêm `GET /api/products` (`operationId: listProducts`) vào `openapi.yaml`, kèm 3 response (`200`/`400`/`500`) và đủ 19 lớp `x-test-partitions.search`.
2. ✅ **XONG** — đã chốt **DEC-01 = STRICT**: sửa `{ value: '1.0' }` từ `expect: 200` → `expect: 400`, bổ sung 4 lớp I8–I11 (`" 1"`, `"1 "`, `"+1"`, `"01"`) vào `x-test-partitions.id` (nay đủ **18 lớp / 19 entry**), và ghi quyết định + lý do vào `x-contract-decision`.
3. ✅ **XONG** — BUG-14 → BUG-18 đã vào `openapi.yaml`: BUG-14 ở `getProductById.x-sut-actual-summary`, BUG-15 ở `createProduct.x-negative-route-note`, BUG-16/17 ở `listProducts.x-sut-actual-summary`, BUG-18 ở response `400`, BUG-04 ở response `500`. **Còn lại:** bổ sung 5 bug này vào bảng bug tổng `plan.md` §11.
4. **Data file cho Collection Runner:** `postman/data/product-ids.csv` với cột `id,expectedPriceType` = `1,number` … `5,number` (dùng cho TC-P1-020).
5. **Thứ tự chạy:** folder API-1 phải chạy **trước** API-3, hoặc restart server ở giữa — vì API-3 tạo/sửa product làm lệch tập seed id 1–5 (PRE-2).
