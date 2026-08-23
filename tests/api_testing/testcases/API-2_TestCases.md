# API-2 — `PUT /api/orders/:id/cancel` · Test cases (Phân hoạch `:id` + Ownership)

**API:** API-2 · **FR:** FR-10 (Order State Machine) · **Endpoint:** `PUT /api/orders/:id/cancel`
**Kỹ thuật:** Equivalence Partitioning trên path param `:id`, trục **ownership** (đơn của ai) và **định dạng id**
**Auth:** **bắt buộc** `Authorization: Bearer <token>` (token **user**)
**Ngày lập:** 22/08/2026 · **Đã probe live trên `localhost:3000`, backup/restore DB**

> **Phạm vi nhóm này:** chỉ phân hoạch theo `:id` (ownership + định dạng), **giữ cố định state = `pending`**
> để cô lập biến `:id`. Trục **state transition** (pending/confirmed/shipping/delivered/canceled) là nhóm **riêng kế tiếp**
> (theo đúng FR-10). TC-ID nhóm này: **TC-O2-001 → 015**.

---

## PRE — Tiền đề & dữ liệu dựng sẵn

Bảng `orders` seed **rỗng** ⇒ phải tự tạo đơn bằng `POST /api/checkout`. Hai tài khoản seed:

| Vai trò | Email | Password | user id (trong JWT) |
|---------|-------|----------|---------------------|
| User | `test@eshop.com` | `Test1234!` | **2** |
| Admin | `admin@eshop.com` | `Admin123!` | **1** |

| Mã | Nội dung tiền đề |
|----|------------------|
| **PRE-U** | Đăng nhập `test@eshop.com` → lấy `{{userToken}}` (id=2, role=user). |
| **PRE-A** | Đăng nhập `admin@eshop.com` → lấy `{{adminToken}}` (id=1). Dùng để tạo "đơn của người khác". |
| **PRE-OWN** | `POST /api/checkout` bằng `{{userToken}}` → đơn **của user (id=2)**, state `pending` → lưu `{{ownOrderId}}`. |
| **PRE-OTHER** | `POST /api/checkout` bằng `{{adminToken}}` → đơn **của admin (id=1)**, state `pending` → lưu `{{otherOrderId}}`. |
| **PRE-CANCELED** | Tạo thêm 1 đơn của user rồi cancel trước → state `canceled` → lưu `{{canceledOrderId}}` (cho case double-cancel). |

> ⚠ **Không hard-code order id.** Bảng `orders` re-seed rỗng mỗi lần khởi động server; `orderId` phải lấy động
> từ response của `checkout`. Chạy các case cancel **theo đúng thứ tự tạo đơn**.

Header chung mọi case: `X-Student-Id: 23127438` + `Authorization: Bearer {{userToken}}` (trừ case auth âm bản).

---

## 1. Bảng phân hoạch — Path param `:id`

Miền hợp lệ theo contract: **integer ≥ 1**, trỏ tới đơn **tồn tại** và **thuộc về user đang gọi**.
Hai trục độc lập: **(A) định dạng/khoảng giá trị của id**, **(B) quyền sở hữu**.

| Class ID | Trục | Lớp tương đương | Đại diện | Precondition (state · owner) | Expected (contract) |
|----------|------|-----------------|----------|------------------------------|---------------------|
| **V1** | ownership | id hợp lệ, **đơn của chính user**, đang `pending` | `{{ownOrderId}}` | pending · user(2) | `200` — hủy thành công |
| **O1** | ownership | id hợp lệ, **đơn của người khác** | `{{otherOrderId}}` | pending · admin(1) | `404` — không lộ tồn tại (anti-enumeration) |
| **I1** | tồn tại | id đúng kiểu, **không tồn tại** | 99999 | — | `404` |
| **B1** | biên | **biên dưới − 1** (zero) | 0 | — | `400` (id không hợp lệ, theo DEC-01 strict) |
| **I2** | định dạng | **số âm** | -1 | — | `400` |
| **I3** | định dạng | **chuỗi phi số** | abc | — | `400` |
| **I4** | định dạng | **số thực** | 1.5 | — | `400` |
| **I5** | định dạng | **rỗng** (`/orders//cancel`) | *(empty)* | — | `404`/`405` + JSON (route không khớp) |

> **Ghi chú ownership (quan trọng):** SUT truy vấn `WHERE id = ? AND user_id = ?` (`server.js:322-323`).
> Vì vậy "đơn của người khác" và "đơn không tồn tại" **cùng** trả `404 "Order not found"`.
> Đây là hành vi **anti-enumeration hợp lý** (không tiết lộ đơn có tồn tại hay không) ⇒ **PASS, không phải bug**.
> Nếu SUT trả `403` cho đơn người khác thì mới là lộ thông tin. Ta khẳng định điều này bằng O1.

> **Ghi chú DEC-01 (nhất quán với API-1):** với id **sai định dạng** (`abc`, `1.5`) và **ngoài miền** (`0`, `-1`),
> contract strict kỳ vọng `400`. SUT trả `404` (query parameterized nên id sai chỉ đơn giản không khớp dòng nào).
> Đây là **validation gap mức thấp** — **không** có rủi ro bảo mật (khác hẳn SQLi ở API-1), nên ghi **observation**,
> không nâng thành bug nặng.

---

## 2. Test cases

Cột `Precondition` ghi rõ **state của đơn** và **đơn thuộc user nào**. `PUT` cancel ⇒ `Body` rỗng.

### 2.1 Ownership (đơn của mình / của người khác / không tồn tại)

| TC-ID | API | FR/SEC | Technique | Precondition (state · owner) | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|------------------------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-O2-001 | API-2 | FR-10 | EP-V1 (happy) | PRE-OWN: đơn **pending**, **của user(2)** | `PUT /api/orders/{{ownOrderId}}/cancel` | `Bearer {{userToken}}` | — | `200` | `{ "message": "Order canceled successfully" }`. Hậu kiểm: `GET /api/orders/{{ownOrderId}}` → `status === "canceled"` | **P0** |
| TC-O2-002 | API-2 | FR-10 / SEC-02 | EP-O1 (IDOR) | PRE-OTHER: đơn **pending**, **của admin(1)** | `PUT /api/orders/{{otherOrderId}}/cancel` | `Bearer {{userToken}}` | — | `404` | `{ "error": "Order not found" }`. **Assertion IDOR:** user KHÔNG hủy được đơn người khác; status **không** phải `200`; đơn admin vẫn `pending` (kiểm bằng adminToken) | **P0** |
| TC-O2-003 | API-2 | FR-10 | EP-I1 | Không có đơn id=99999 | `PUT /api/orders/99999/cancel` | `Bearer {{userToken}}` | — | `404` | `{ "error": "Order not found" }` | P1 |
| TC-O2-004 | API-2 | FR-10 / SEC-02 | Anti-enumeration | So sánh TC-002 vs TC-003 | *(phân tích)* | — | — | `404` cả hai | Response của "đơn người khác" và "đơn không tồn tại" **giống hệt nhau** (`404` + cùng message) ⇒ không rò rỉ sự tồn tại của đơn. Khẳng định hành vi đúng | P1 |

### 2.2 Định dạng / khoảng giá trị của `:id`

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-O2-005 | API-2 | FR-10 | BVA-B1 | — | `PUT /api/orders/0/cancel` | `Bearer {{userToken}}` | — | `400` (strict) | `{error}` JSON. Theo DEC-01: id=0 ngoài miền `≥1`. SUT trả `404` ⇒ validation gap (observation) | P2 |
| TC-O2-006 | API-2 | FR-10 | EP-I2 | — | `PUT /api/orders/-1/cancel` | `Bearer {{userToken}}` | — | `400` (strict) | `{error}` JSON. id âm không hợp lệ | P2 |
| TC-O2-007 | API-2 | FR-10 | EP-I3 | — | `PUT /api/orders/abc/cancel` | `Bearer {{userToken}}` | — | `400` (strict) | `{error}` JSON. id phi số | P1 |
| TC-O2-008 | API-2 | FR-10 | EP-I4 | — | `PUT /api/orders/1.5/cancel` | `Bearer {{userToken}}` | — | `400` (strict) | `{error}` JSON. id số thực | P2 |
| TC-O2-009 | API-2 | FR-10 | EP-I5 | — | `PUT /api/orders//cancel` | `Bearer {{userToken}}` | — | `404`/`405` | Route không khớp. **Assertion contract:** body phải là **JSON** `{error}`, `Content-Type: application/json` (SUT trả HTML ⇒ FAIL, map BUG-15) | P2 |

### 2.3 Auth trên endpoint cancel (path :id giữ hợp lệ)

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-O2-010 | API-2 | **SEC-02** | Auth — thiếu token | PRE-OTHER (đơn tồn tại) | `PUT /api/orders/{{otherOrderId}}/cancel` | *(không Authorization)* | — | `401` | `{ "error": "Unauthorized" }`. Không hủy được | **P0** |
| TC-O2-011 | API-2 | **SEC-02** | Auth — token rác | PRE-OTHER | `PUT /api/orders/{{otherOrderId}}/cancel` | `Authorization: Bearer xxx.yyy.zzz` | — | `403` | `{ "error": "Forbidden" }` | P1 |
| TC-O2-012 | API-2 | SEC-02 | Auth — thiếu prefix Bearer | PRE-OWN | `PUT /api/orders/{{ownOrderId}}/cancel` | `Authorization: {{userToken}}` (không "Bearer ") | — | `401` | Token không parse được ⇒ coi như thiếu | P2 |

### 2.4 Đối chứng trạng thái kết thúc (bắc cầu sang nhóm state-transition)

| TC-ID | API | FR/SEC | Technique | Precondition | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-O2-013 | API-2 | FR-10 | Double-cancel (idempotency) | PRE-CANCELED: đơn **canceled**, của user | `PUT /api/orders/{{canceledOrderId}}/cancel` | `Bearer {{userToken}}` | — | `400` | `{ "error": "Cannot cancel this order." }`. Không hủy lại đơn đã hủy | P1 |
| TC-O2-014 | API-2 | FR-10 | Ownership + đã canceled | Đơn canceled của **admin** | `PUT /api/orders/{{otherCanceledId}}/cancel` | `Bearer {{userToken}}` | — | `404` | Ownership check **ưu tiên trước** state check ⇒ `404` (không lộ đơn đang ở state nào) | P2 |
| TC-O2-015 | API-2 | FR-10 | Body thừa field lạ (khác `status`) | PRE-OWN | `PUT /api/orders/{{ownOrderId}}/cancel` | `Bearer {{userToken}}` | `{"user_id":1,"total_amount":0,"foo":"bar"}` | `200` | Body bị **bỏ qua** hoàn toàn — hủy thành công, `user_id`/`total_amount` của đơn **không đổi** (hậu kiểm bằng `GET`). *(Vector `{"status":"delivered"}` tách riêng ở nhóm Security TC-O2-036 để không trùng)* | P2 |

**Tổng nhóm phân hoạch `:id`: 15 test case** (TC-O2-001 → 015).
Nhóm **state-transition** (5 state × cancel + fixtures qua admin) sẽ nối tiếp từ **TC-O2-016**.

---

## Phụ lục — Hành vi SUT đã probe & verdict

> Đã login user(id=2) + admin(id=1), tạo đơn cho từng bên, probe live; DB backup trước và restore sau.

| TC-ID | Input (id · owner) | Expected (contract) | **Actual (SUT)** | Verdict | Bug |
|-------|--------------------|---------------------|------------------|---------|-----|
| 001 | own · pending | `200` canceled | `200` `{"message":"Order canceled successfully"}`; sau đó `status=canceled` | ✅ PASS | — |
| 002 | other (admin) · pending | `404` (IDOR chặn) | `404` `{"error":"Order not found"}` | ✅ PASS | — |
| 003 | 99999 | `404` | `404` `{"error":"Order not found"}` | ✅ PASS | — |
| 004 | so sánh 002 vs 003 | giống hệt | cùng `404` + cùng message | ✅ PASS | — |
| 005 | 0 | `400` (strict) | `404` `{"error":"Order not found"}` | ⚠ observation | validation gap (thấp) |
| 006 | -1 | `400` (strict) | `404` | ⚠ observation | validation gap (thấp) |
| 007 | abc | `400` (strict) | `404` | ⚠ observation | validation gap (thấp) |
| 008 | 1.5 | `400` (strict) | `404` | ⚠ observation | validation gap (thấp) |
| **009** | `//cancel` (rỗng) | `404`/`405` + **JSON** | `404` + **HTML** `<!DOCTYPE html>...Cannot PUT` | ❌ **FAIL** | **BUG-15** |
| 010 | other · thiếu token | `401` | `401` `{"error":"Unauthorized"}` | ✅ PASS | — |
| 011 | other · token rác | `403` | `403` `{"error":"Forbidden"}` | ✅ PASS | — |
| 012 | own · thiếu "Bearer " | `401` | `401` (token null sau split) | ✅ PASS | — |
| 013 | canceled (own) | `400` | `400` `{"error":"Cannot cancel this order."}` | ✅ PASS | — |
| 014 | canceled (other) | `404` (ownership trước) | `404` | ✅ PASS | — |
| 015 | own · body `{status:delivered}` | `200` canceled (bỏ qua body) | `200`; status = `canceled` | ✅ PASS | — |

**Kết luận nhóm phân hoạch `:id`:** 15 case → **10 PASS / 1 FAIL / 4 observation**.
- **PASS quan trọng:** ownership được enforce đúng — user **không** hủy được đơn người khác (TC-002), và SUT dùng `404` thay vì `403` nên **không rò rỉ** sự tồn tại của đơn (TC-004). Đây là điểm SUT làm **đúng**.
- **FAIL (009 → BUG-15):** id rỗng → route trả HTML thay vì JSON (cùng lỗi định dạng lỗi như API-1).
- **Observation (005–008):** id sai định dạng trả `404` thay vì `400` — validation gap mức thấp, **không** rủi ro bảo mật vì query đã parameterized (`WHERE id=? AND user_id=?`); ghi nhận theo DEC-01 nhưng không nâng thành bug.

> **Lưu ý cho nhóm state-transition kế tiếp:** bug nghiêm trọng của API-2 (BUG-05: user hủy được đơn `shipping`)
> **không** lộ ra ở nhóm này vì ta giữ state = `pending`. Nó chỉ xuất hiện khi test đủ 5 state — sẽ làm ở TC-O2-016+.
