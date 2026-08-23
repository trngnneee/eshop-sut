# API-3 — Quản lý sản phẩm · Test cases (Input Validation: Partition + BVA cho từng field)

**API:** API-3 · **FR:** FR-15 (Product CRUD) · **Endpoints:** `POST /api/products` (tạo) + `PUT /api/products/:id` (sửa)
**Kỹ thuật:** Equivalence Partitioning + Boundary Value Analysis, **tách riêng cho từng field**
**Auth (theo FR-12/SEC-02/03):** bắt buộc admin — *lưu ý: SUT hiện KHÔNG enforce (BUG-07), test auth ở nhóm Security riêng*
**Ngày lập:** 22/08/2026 · **Đã probe live trên `localhost:3000`, backup/restore DB**

> **Ràng buộc FR-15 (dùng làm Expected):** `name` bắt buộc, ≤255 ký tự · `price` bắt buộc, số **dương (>0)** ·
> `category_id` bắt buộc, phải **tồn tại** trong bảng `categories` (seed: 1,2,3) · khi **sửa**, chỉ đổi field được gửi,
> không null hóa field khác.
> **Nguyên tắc Expected:** input vi phạm FR-15 → **400**. SUT thực tế trả `200` (không validate gì) ⇒ giữ expected **400**
> và đánh dấu **bug** (theo đúng yêu cầu). TC-ID: **TC-P3-001 → 048**.

---

## PRE — Tiền đề

| Mã | Nội dung |
|----|----------|
| **PRE-1** | Backend chạy, DB seed sạch: categories id **1,2,3**; products id **1–5**. |
| **PRE-SEED-CAT** | Chỉ có 3 category (1,2,3). `category_id` ngoài tập này = "không tồn tại". |
| **PRE-DESTRUCT** | POST tạo record mới; PUT sửa/null-hóa record. **Backup `database.sqlite` trước, restore sau** hoặc chạy có teardown. |
| **PRE-VALID** | Payload hợp lệ mẫu: `{"name":"Sony WH-1000XM5","price":8500000,"description":"Chống ồn","imageUrl":"https://x/y.png","category_id":3}`. |

Header chung: `X-Student-Id: 23127438` (+ `Bearer {{adminToken}}` — dù SUT bỏ qua, vẫn gửi cho đúng thiết kế).
`price` mặc định number trong JSON trừ khi ghi rõ là chuỗi.

---

## 1. Bảng phân hoạch — field `name`

Contract: string, **bắt buộc**, độ dài **1..255**, không rỗng/không chỉ khoảng trắng.

| Class | Loại | Giá trị | Lý do | Expected |
|-------|------|---------|-------|----------|
| N-V1 | Valid | `"a"` (1 ký tự) | biên dưới độ dài | 200 |
| N-V2 | Valid | 255 ký tự | **biên trên** | 200 |
| N-V3 | Valid | `"Điện thoại Xịn"` unicode có dấu | ký tự hợp lệ tiếng Việt | 200 |
| N-I1 | Invalid | `""` (rỗng) | vi phạm bắt buộc | **400** |
| N-I2 | Invalid | thiếu hẳn field | bắt buộc | **400** |
| N-I3 | Invalid | 256 ký tự | **biên trên + 1** | **400** |
| N-I4 | Invalid | 300 ký tự | vượt xa giới hạn | **400** |
| N-I5 | Invalid | `"   "` toàn khoảng trắng | rỗng về mặt ngữ nghĩa | **400** |
| N-I6 | Invalid | `12345` (số, không phải string) | sai kiểu | **400** |

## 2. Bảng phân hoạch — field `price`

Contract: number **nguyên dương (>0)**, bắt buộc.

| Class | Loại | Giá trị | Lý do | Expected |
|-------|------|---------|-------|----------|
| P-V1 | Valid | `100000` | số dương hợp lệ | 200 |
| P-V2 | Valid | `1` | **biên dưới hợp lệ** (>0) | 200 |
| P-I1 | Invalid | `0` | **biên**: không dương | **400** |
| P-I2 | Invalid | `-1` | số âm | **400** |
| P-I3 | Invalid | `1.5` | số thực (không nguyên) | **400** |
| P-I4 | Invalid | `"1000"` (chuỗi) | sai kiểu | **400** |
| P-I5 | Invalid | `null` | rỗng | **400** |
| P-I6 | Invalid | thiếu field | bắt buộc | **400** |
| P-I7 | Invalid | `999999999999999` cực lớn | tràn/không hợp lý | 200 (hoặc 400) — xem note |
| P-I8 | Invalid | `1e5` (ký hiệu khoa học) | JSON parse thành `100000` | 200 nếu ≡ số dương; kiểm tra cách lưu |

## 3. Bảng phân hoạch — field `category_id`

Contract: integer, bắt buộc, **phải tồn tại** trong `categories` (1,2,3).

| Class | Loại | Giá trị | Lý do | Expected |
|-------|------|---------|-------|----------|
| C-V1 | Valid | `1` | tồn tại | 200 |
| C-V2 | Valid | `2` | tồn tại | 200 |
| C-V3 | Valid | `3` | tồn tại (biên trên tập seed) | 200 |
| C-I1 | Invalid | `9999` | **không tồn tại** (thiếu FK) | **400** |
| C-I2 | Invalid | `0` | biên/không tồn tại | **400** |
| C-I3 | Invalid | `-1` | âm | **400** |
| C-I4 | Invalid | `"abc"` | sai kiểu | **400** |
| C-I5 | Invalid | thiếu field | bắt buộc | **400** |

## 4. Bảng phân hoạch — `imageUrl` / `description` (optional)

Contract: FR-15 không bắt buộc; nếu có nên là string; `imageUrl` nên đúng dạng URL.

| Class | Field | Giá trị | Expected |
|-------|-------|---------|----------|
| IM-V1 | imageUrl | `""` rỗng | 200 (optional) |
| IM-V2 | imageUrl | `null` | 200 |
| IM-I1 | imageUrl | `"not a url"` | 200 hoặc 400 (spec không nói rõ ⇒ observation) |
| IM-I2 | imageUrl | chuỗi 5000 ký tự | 200 (hoặc 400 nếu có giới hạn) |
| DE-V1 | description | `""` / `null` | 200 |
| DE-I1 | description | chuỗi rất dài | 200 |

---

## 5. Test cases — `POST /api/products` (tạo)

Body luôn kèm các field hợp lệ khác (theo PRE-VALID), chỉ **biến thiên 1 field** mỗi case để cô lập.

### 5.1 name

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Body (field biến thiên) | Expected status | Expected / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|--------------------------|-----------------|--------------------------|----------|
| TC-P3-001 | API-3 | FR-15 | N-V1 | PRE-1 | `POST /api/products` | `name:"a"` | `200` | `{message,id}`; tạo thành công | P1 |
| TC-P3-002 | API-3 | FR-15 | N-V2 (biên 255) | PRE-1 | `POST /api/products` | `name`=255 ký tự | `200` | tạo thành công | P1 |
| TC-P3-003 | API-3 | FR-15 | N-V3 unicode | PRE-1 | `POST /api/products` | `name:"Điện thoại Xịn"` | `200` | lưu đúng unicode | P2 |
| TC-P3-004 | API-3 | FR-15 | N-I1 rỗng | PRE-1 | `POST /api/products` | `name:""` | **`400`** | Từ chối name rỗng. SUT `200` ⇒ **BUG-08** | **P0** |
| TC-P3-005 | API-3 | FR-15 | N-I2 thiếu | PRE-1 | `POST /api/products` | *(bỏ field name)* | **`400`** | Bắt buộc. SUT `200` ⇒ BUG-08 | **P0** |
| TC-P3-006 | API-3 | FR-15 | N-I3 (biên 256) | PRE-1 | `POST /api/products` | `name`=256 ký tự | **`400`** | Vượt 255. SUT `200` ⇒ **BUG-10** | P1 |
| TC-P3-007 | API-3 | FR-15 | N-I4 (300) | PRE-1 | `POST /api/products` | `name`=300 ký tự | **`400`** | SUT `200` ⇒ BUG-10 | P1 |
| TC-P3-008 | API-3 | FR-15 | N-I5 khoảng trắng | PRE-1 | `POST /api/products` | `name:"   "` | **`400`** | Rỗng ngữ nghĩa. SUT `200` ⇒ BUG-08 | P1 |
| TC-P3-009 | API-3 | FR-15 | N-I6 số | PRE-1 | `POST /api/products` | `name:12345` | **`400`** | Sai kiểu. SUT `200`, lưu `"12345"` (string do TEXT affinity) ⇒ BUG-08 | P2 |

### 5.2 price

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Body (field biến thiên) | Expected status | Expected / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|--------------------------|-----------------|--------------------------|----------|
| TC-P3-010 | API-3 | FR-15 | P-V2 (biên >0) | PRE-1 | `POST /api/products` | `price:1` | `200` | tạo thành công | P1 |
| TC-P3-011 | API-3 | FR-15 | P-I1 (0) | PRE-1 | `POST /api/products` | `price:0` | **`400`** | price phải >0. SUT `200` ⇒ **BUG-08** | **P0** |
| TC-P3-012 | API-3 | FR-15 | P-I2 (-1) | PRE-1 | `POST /api/products` | `price:-1` | **`400`** | Âm. SUT `200` ⇒ BUG-08 | **P0** |
| TC-P3-013 | API-3 | FR-15 | P-I3 (1.5) | PRE-1 | `POST /api/products` | `price:1.5` | **`400`** | Không nguyên. SUT `200` ⇒ BUG-08 | P1 |
| TC-P3-014 | API-3 | FR-15 | P-I4 chuỗi | PRE-1 | `POST /api/products` | `price:"1000"` | **`400`** | Sai kiểu. SUT `200`, lưu số 1000 (coerce) ⇒ BUG-08 | P1 |
| TC-P3-015 | API-3 | FR-15 | P-I5 null | PRE-1 | `POST /api/products` | `price:null` | **`400`** | Bắt buộc. SUT `200` ⇒ BUG-08/09 | P1 |
| TC-P3-016 | API-3 | FR-15 | P-I6 thiếu | PRE-1 | `POST /api/products` | *(bỏ price)* | **`400`** | Bắt buộc. SUT `200` ⇒ BUG-08 | **P0** |
| TC-P3-017 | API-3 | FR-15 | P-I7 cực lớn | PRE-1 | `POST /api/products` | `price:999999999999999` | `200` | **Observation:** FR-15 + cột `price INTEGER` không đặt trần ⇒ chấp nhận là đúng spec. Assert lưu đúng số (không tràn/không đổi) | P2 |
| TC-P3-018 | API-3 | FR-15 | P-I8 (1e5) | PRE-1 | `POST /api/products` | `price:1e5` | `200` | JSON parse `1e5`→`100000` (>0) ⇒ hợp lệ; assert lưu `100000` | P2 |

### 5.3 category_id

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Body (field biến thiên) | Expected status | Expected / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|--------------------------|-----------------|--------------------------|----------|
| TC-P3-019 | API-3 | FR-15 | C-V1 | PRE-1 | `POST /api/products` | `category_id:1` | `200` | tạo thành công | P1 |
| TC-P3-020 | API-3 | FR-15 | C-V3 (biên 3) | PRE-1 | `POST /api/products` | `category_id:3` | `200` | tạo thành công | P2 |
| TC-P3-021 | API-3 | FR-15 | C-I1 (9999) | PRE-SEED-CAT | `POST /api/products` | `category_id:9999` | **`400`** | Category không tồn tại (thiếu FK). SUT `200` ⇒ **BUG-08** (thiếu ràng buộc khoá ngoại) | **P0** |
| TC-P3-022 | API-3 | FR-15 | C-I2 (0) | PRE-1 | `POST /api/products` | `category_id:0` | **`400`** | Không tồn tại. SUT `200` ⇒ BUG-08 | P1 |
| TC-P3-023 | API-3 | FR-15 | C-I3 (-1) | PRE-1 | `POST /api/products` | `category_id:-1` | **`400`** | Âm. SUT `200` ⇒ BUG-08 | P2 |
| TC-P3-024 | API-3 | FR-15 | C-I4 ("abc") | PRE-1 | `POST /api/products` | `category_id:"abc"` | **`400`** | Sai kiểu. SUT `200` ⇒ BUG-08 | P1 |
| TC-P3-025 | API-3 | FR-15 | C-I5 thiếu | PRE-1 | `POST /api/products` | *(bỏ category_id)* | **`400`** | Bắt buộc. SUT `200` ⇒ BUG-08 | **P0** |

### 5.4 imageUrl / description + tổ hợp

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Body (field biến thiên) | Expected status | Expected / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|--------------------------|-----------------|--------------------------|----------|
| TC-P3-026 | API-3 | FR-15 | IM-V1/V2 | PRE-1 | `POST /api/products` | `imageUrl:""` / `null` | `200` | Optional ⇒ chấp nhận | P2 |
| TC-P3-027 | API-3 | FR-15 | IM-I1 bad url | PRE-1 | `POST /api/products` | `imageUrl:"not a url"` | `200` | **Observation:** FR-15 không ràng buộc định dạng URL ⇒ chấp nhận. Assert lưu **nguyên văn** chuỗi | P3 |
| TC-P3-028 | API-3 | FR-15 | IM-I2 dài | PRE-1 | `POST /api/products` | `imageUrl`=5000 ký tự | `200` | **Observation:** FR-15 không nêu ngưỡng độ dài cho imageUrl ⇒ khẳng định hành vi: `200` + assert lưu đủ 5000 ký tự. (Muốn test giới hạn thì phải chốt ngưỡng trước) | P3 |
| TC-P3-029 | API-3 | FR-15 | DE-V1 | PRE-1 | `POST /api/products` | `description:""`/`null` | `200` | Optional | P3 |
| TC-P3-030 | API-3 | FR-15 | **Tổ hợp nhiều lỗi** | PRE-1 | `POST /api/products` | `{"name":"","price":-500,"category_id":9999}` | **`400`** | Nhiều vi phạm cùng lúc. SUT `200` created (record rác) ⇒ **BUG-08** | **P0** |
| TC-P3-031 | API-3 | FR-15 | Body rỗng | PRE-1 | `POST /api/products` | `{}` | **`400`** | Thiếu mọi field bắt buộc. SUT `200`, record toàn null ⇒ **BUG-09** | **P0** |
| TC-P3-032 | API-3 | SEC-04 | Stored XSS vector | PRE-1 | `POST /api/products` | `name:"<script>alert(1)</script>"` | `200`/`400` | API lưu **nguyên văn** payload. **Assertion:** payload persisted verbatim → cờ **SEC-04**: nếu Frontend render `name` không escape ⇒ stored XSS. (Ở tầng API lưu raw là bình thường; rủi ro ở tầng render — kiểm chéo FR-05) | P1 |

## 6. Test cases — `PUT /api/products/:id` (sửa)

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Body | Expected status | Expected / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|------|-----------------|--------------------------|----------|
| TC-P3-033 | API-3 | FR-15 | Update hợp lệ | PRE-1, product id=3 tồn tại | `PUT /api/products/3` | đủ 5 field hợp lệ | `200` | `{message}`; đọc lại đúng giá trị mới | P1 |
| TC-P3-034 | API-3 | FR-15 | **PUT partial → null hóa** | PRE-1, product id=1 | `PUT /api/products/1` | `{"name":"Chỉ đổi tên"}` | **`400`** hoặc chỉ đổi `name` | **Assertion toàn vẹn:** đọc lại id=1 → `price/description/imageUrl/category_id` **giữ nguyên**. SUT set chúng = **null** (mất dữ liệu) ⇒ **BUG-11** | **P0** |
| TC-P3-035 | API-3 | FR-15 | **PUT id không tồn tại** | PRE-1 | `PUT /api/products/99999` | đủ 5 field | **`404`** | SUT `200 "Product updated"` (no-op im lặng) ⇒ **BUG-12** | P1 |
| TC-P3-036 | API-3 | FR-15 | PUT name rỗng | PRE-1, id=3 | `PUT /api/products/3` | `name:""`, các field khác hợp lệ | **`400`** | SUT `200`, ghi đè name rỗng ⇒ BUG-08 | P1 |
| TC-P3-037 | API-3 | FR-15 | PUT price ≤0 | PRE-1, id=3 | `PUT /api/products/3` | `price:-1` | **`400`** | SUT `200` ⇒ BUG-08 | P1 |
| TC-P3-038 | API-3 | FR-15 | PUT category không tồn tại | PRE-1, id=3 | `PUT /api/products/3` | `category_id:9999` | **`400`** | SUT `200` ⇒ BUG-08 | P1 |
| TC-P3-039 | API-3 | FR-15 | **PUT edit-isolation** | PRE-1 | `PUT /api/products/3` (đủ field) rồi `GET /api/products/2` | — | id=2 **không đổi** | **Assertion:** sửa id=3 không ảnh hưởng id=2. SUT PASS (WHERE id=? đúng) ⇒ khẳng định FR-15 phần isolation đạt | P1 |
| TC-P3-040 | API-3 | FR-15 | PUT id=0 | PRE-1 | `PUT /api/products/0` | đủ field | `400`/`404` | id không hợp lệ | P2 |
| TC-P3-041 | API-3 | FR-15 | PUT id=abc | PRE-1 | `PUT /api/products/abc` | đủ field | `400` | id phi số | P2 |
| TC-P3-042 | API-3 | FR-15 | PUT body rỗng | PRE-1, id=3 | `PUT /api/products/3` | `{}` | **`400`** | SUT `200`, null hóa TẤT CẢ field id=3 (mất dữ liệu toàn bộ) ⇒ **BUG-11** nặng | **P0** |

## 7. Route âm bản

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Body | Expected status | Expected / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|------|-----------------|--------------------------|----------|
| TC-P3-043 | API-3 | FR-15 | `POST /api/products/:id` không tồn tại | PRE-1 | `POST /api/products/1` | `{}` | `404`/`405` + JSON | Route tạo-theo-id không tồn tại; SUT trả `404` **HTML** ⇒ BUG-15 | P2 |
| TC-P3-044 | API-3 | FR-15 | `PATCH /api/products/:id` | PRE-1 | `PATCH /api/products/1` | `{}` | `404`/`405` + JSON | Không hỗ trợ PATCH; HTML ⇒ BUG-15 | P3 |
| TC-P3-045 | API-3 | FR-15 | malformed JSON | PRE-1 | `POST /api/products` | `{bad json` | `400` + JSON | Body-parser lỗi → `400`; SUT trả HTML ⇒ BUG-15 | P2 |
| TC-P3-046 | API-3 | FR-15 | Content-Type text/plain | PRE-1 | `POST /api/products` | `Content-Type: text/plain` + JSON string | `400`/`415` | Không parse JSON ⇒ body rỗng ⇒ tạo record null (BUG-09) hoặc từ chối | P3 |
| TC-P3-047 | API-3 | FR-15 | Content-Type + valid | PRE-1 | `POST /api/products` | `application/json` + PRE-VALID | `200` | Đối chứng dương: tạo thành công đúng contract | P2 |
| ~~TC-P3-048~~ | — | — | *(đã bỏ)* | — | — | — | — | **Gộp vào TC-P3-057** (nhóm Security) — trùng test mass-assign `id`/`role` trên POST; TC-057 bao rộng hơn (thêm `is_admin`). Xem `docs/ai-testcase-audit.md`. | — |

| TC-P3-073 | API-3 | FR-15 | Thiếu header `X-Student-Id` | PRE-1 | `POST /api/products` (body hợp lệ, **không** gửi `X-Student-Id`) | `200` | SUT **không** yêu cầu header này (yêu cầu của HW06, không phải SUT) ⇒ tạo product bình thường. Bằng chứng chấm bài nằm ở **console pre-request script**, không ở phía server. Đối chứng với API-1 TC-P1-082 / API-2 TC-O2-056 | P3 |

**Tổng nhóm validation API-3: 48 test case hiệu lực** (TC-P3-001 → 048, trong đó TC-P3-048 đã gộp vào TC-P3-057) **+ TC-P3-073** (bổ sung header) = **48 case**.
Nhóm **Security/Auth** (BUG-07 — thiếu middleware) và **Schema** sẽ là nhóm riêng kế tiếp.

---

## Phụ lục — Hành vi SUT đã probe & verdict

> POST/PUT là mutating ⇒ backup `database.sqlite` trước, restore sau. Giá trị "lưu thực tế" đọc lại qua `GET`.

| TC-ID | Input | Expected (FR-15) | **Actual (SUT)** | Verdict | Bug |
|-------|-------|------------------|------------------|---------|-----|
| 001–003 | name valid (1/255/unicode) | `200` | `200` created | ✅ PASS | — |
| **004** | name `""` | `400` | `200` created | ❌ FAIL | **BUG-08** |
| **005** | name thiếu | `400` | `200` created | ❌ FAIL | **BUG-08** |
| **006/007** | name 256/300 | `400` | `200` created | ❌ FAIL | **BUG-10** |
| **008** | name `"   "` | `400` | `200` created | ❌ FAIL | BUG-08 |
| **009** | name `12345` | `400` | `200`, lưu `"12345"` (string) | ❌ FAIL | BUG-08 |
| 010 | price `1` | `200` | `200` | ✅ PASS | — |
| **011** | price `0` | `400` | `200` created | ❌ FAIL | **BUG-08** |
| **012** | price `-1` | `400` | `200` created | ❌ FAIL | **BUG-08** |
| **013** | price `1.5` | `400` | `200` (lưu 1.5) | ❌ FAIL | BUG-08 |
| **014** | price `"1000"` | `400` | `200`, lưu số `1000` (coerce) | ❌ FAIL | BUG-08 |
| **015** | price `null` | `400` | `200` created | ❌ FAIL | BUG-08/09 |
| **016** | price thiếu | `400` | `200` created | ❌ FAIL | **BUG-08** |
| 017 | price cực lớn | `400`/`200` | `200` | ⚠ observation | — |
| 018 | price `1e5` | `200` | `200`, lưu `100000` | ✅ PASS | — |
| 019/020 | category 1/3 | `200` | `200` | ✅ PASS | — |
| **021** | category `9999` | `400` | `200` created (thiếu FK) | ❌ FAIL | **BUG-08** |
| **022** | category `0` | `400` | `200` | ❌ FAIL | BUG-08 |
| **023** | category `-1` | `400` | `200` | ❌ FAIL | BUG-08 |
| **024** | category `"abc"` | `400` | `200` | ❌ FAIL | BUG-08 |
| **025** | category thiếu | `400` | `200` | ❌ FAIL | **BUG-08** |
| 026/029 | imageUrl/description rỗng/null | `200` | `200` | ✅ PASS | — |
| 027/028 | imageUrl bad/dài | observation | `200`, lưu nguyên | ⚠ observation | — |
| **030** | tổ hợp `{name:"",price:-500,cat:9999}` | `400` | `200` created (record rác) | ❌ FAIL | **BUG-08** |
| **031** | body `{}` | `400` | `200`, record toàn null | ❌ FAIL | **BUG-09** |
| 032 | name `<script>` | `200`/`400` | `200`, lưu **nguyên văn** payload | ⚠ SEC-04 flag | stored-XSS vector |
| 033 | PUT hợp lệ | `200` | `200` | ✅ PASS | — |
| **034** | PUT `{name only}` | giữ field khác | id=1 → `price/desc/imageUrl/category_id` = **null** | ❌ FAIL | **BUG-11** |
| **035** | PUT id 99999 | `404` | `200 "Product updated"` (no-op) | ❌ FAIL | **BUG-12** |
| **036/037/038** | PUT name rỗng / price -1 / cat 9999 | `400` | `200`, ghi đè | ❌ FAIL | BUG-08 |
| 039 | PUT isolation (sửa 3, đọc 2) | id=2 không đổi | id=2 **không đổi** | ✅ PASS | — |
| **042** | PUT body `{}` | `400` | `200`, null hóa toàn bộ id=3 | ❌ FAIL | **BUG-11** |
| **043/044/045** | POST/:id · PATCH · malformed | JSON | `404`/`400` **HTML** | ❌ FAIL | **BUG-15** |
| 047 | POST valid | `200` | `200` created | ✅ PASS | — |
| 048 | mass-assign id/role | bỏ qua | `200`, id tự tăng (≠999), không có cột role | ✅ PASS | — |

**Kết luận nhóm validation:** ~48 case → **~26 FAIL / ~15 PASS / ~4 observation**.
- **BUG-08 (Critical):** POST/PUT **không validate gì** — name rỗng, price ≤0, category không tồn tại, sai kiểu... đều tạo/sửa thành công. Vi phạm toàn bộ ràng buộc FR-15.
- **BUG-09 (Major):** body `{}` tạo record toàn `null`.
- **BUG-10 (Major):** name >255 ký tự được chấp nhận.
- **BUG-11 (Critical):** PUT thiếu field → null hóa các field không gửi (mất dữ liệu); body `{}` xoá sạch mọi field của record.
- **BUG-12 (Major):** PUT id không tồn tại → `200` no-op thay vì `404`.
- **BUG-15:** route âm bản / malformed → HTML.
- **PASS quan trọng (FR-15 đạt):** **edit-isolation** — sửa 1 product không ảnh hưởng product khác (TC-039); mass-assign bị bỏ qua (TC-048); `1e5` xử lý đúng.
- **SEC-04 flag:** name lưu nguyên văn `<script>` — stored-XSS vector, rủi ro thực tế ở tầng render (kiểm chéo FR-05); ở tầng API lưu raw là bình thường nên không tính bug API riêng, nhưng ghi cờ.

> **Điểm nhấn:** đây là API có mật độ bug cao nhất — **một endpoint gần như không có tầng validation**. Nguyên nhân gốc:
> `server.js:167-177` (POST) và `:179-189` (PUT) đưa thẳng `req.body` vào câu SQL `INSERT/UPDATE`, không kiểm tra field nào.
