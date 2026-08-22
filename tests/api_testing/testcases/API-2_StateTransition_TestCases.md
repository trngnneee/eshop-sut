# API-2 — `PUT /api/orders/:id/cancel` · **State-Transition Testing** (FR-10)

**API:** API-2 · **FR:** FR-10 (Order State Machine) · **Event dưới test:** *user gọi cancel*
**Kỹ thuật:** State Transition Testing — 0-switch coverage (mỗi state nguồn × sự kiện `cancel`)
**Auth:** `Authorization: Bearer {{userToken}}` (token **user**, id=2)
**Ngày lập:** 22/08/2026 · **Đã probe live đầy đủ 5 state trên `localhost:3000`, backup/restore DB**

> Đây là **phần lõi của API-2**. TC-ID nối tiếp nhóm phân hoạch: **TC-O2-016 → 024**.
> **Expected LẤY THEO SPEC (FR-10), không lấy theo hành vi SUT.** Đặc biệt case `shipping → cancel`:
> expected = **400** (user không được hủy khi đang giao); SUT trả `200` ⇒ đó **chính là bug cần bắt** (BUG-05).

---

## 0. Sơ đồ trạng thái (FR-10) — trích context

```
                 [Admin xác nhận]        [Admin giao hàng]      [Admin hoàn tất]
   pending ───────────────────► confirmed ─────────────► shipping ───────────► delivered   (final)
      │                             │
      │ [User/Admin hủy]            │ [User/Admin hủy]
      ▼                             ▼
   canceled  (final)            canceled  (final)

Ràng buộc:
- delivered, canceled = FINAL STATE → mọi chuyển đổi tiếp theo bị chặn.
- Khi đơn ở shipping: CHỈ Admin được hủy; USER KHÔNG được tự hủy.
- Mọi chuyển đổi không hợp lệ → trả lỗi phù hợp.
```

**Sự kiện dưới test = "user gọi `PUT /api/orders/:id/cancel`".** Từ góc nhìn **user**, chỉ `pending` và
`confirmed` là hủy được; `shipping` (chỉ admin), `delivered`, `canceled` đều phải bị từ chối.

---

## 1. Bảng chuyển trạng thái đầy đủ (State-Transition Table, 0-switch)

| # | State nguồn | Sự kiện | Guard (FR-10) | Expected state đích | **Expected HTTP (SPEC)** | Fixture để dựng state nguồn |
|---|-------------|---------|---------------|---------------------|--------------------------|------------------------------|
| T1 | `pending` | user cancel | user/admin được hủy | `canceled` | **200** | `POST /api/checkout` (đơn tạo ra là `pending`) |
| T2 | `confirmed` | user cancel | user/admin được hủy | `canceled` | **200** | checkout → admin `{confirmed}` |
| T3 | `shipping` | user cancel | **chỉ admin** — user **KHÔNG** | *(giữ nguyên `shipping`)* | **400** ⚠ | checkout → admin `{confirmed}` → admin `{shipping}` |
| T4 | `delivered` | user cancel | final state | *(giữ nguyên `delivered`)* | **400** | checkout → `{confirmed}` → `{shipping}` → `{delivered}` |
| T5 | `canceled` | user cancel | final state | *(giữ nguyên `canceled`)* | **400** | checkout → user cancel (về `canceled`) |

**Transition hợp lệ (từ góc nhìn user):** T1, T2 → `canceled`.
**Transition không hợp lệ phải bị chặn:** T3 (đặc quyền admin), T4, T5 (final state).

> Chuỗi fixture dùng token **admin** cho `PUT /api/admin/orders/:id/status`; mỗi bước đẩy đúng 1 nấc theo
> sơ đồ. Không nhảy cóc (vd `pending → shipping`) vì admin state machine cũng chặn.

---

## 2. Test cases

Header chung: `X-Student-Id: 23127438`. Cột **Precondition** ghi **cả chuỗi setup** để dựng state nguồn.
`orderId` lấy động từ response `checkout` — **không** hard-code.

### 2.1 Ma trận 5 state (mỗi state một đơn riêng)

| TC-ID | API | FR/SEC | Transition | Precondition (chuỗi fixture → state nguồn) | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|-----------|--------------------------------------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-O2-016 | API-2 | FR-10 | **T1** pending→cancel | `POST /api/checkout` (userToken) → đơn `pending` → `{{ordPending}}` | `PUT /api/orders/{{ordPending}}/cancel` | `Bearer {{userToken}}` | — | **200** | `{"message":"Order canceled successfully"}`; hậu kiểm `GET /api/orders/{{ordPending}}` → `status==="canceled"` | **P0** |
| TC-O2-017 | API-2 | FR-10 | **T2** confirmed→cancel | checkout → `PUT /api/admin/orders/{{ordConfirmed}}/status {status:"confirmed"}` (adminToken) → `confirmed` | `PUT /api/orders/{{ordConfirmed}}/cancel` | `Bearer {{userToken}}` | — | **200** | `{"message":"Order canceled successfully"}`; hậu kiểm `status==="canceled"` | **P0** |
| TC-O2-018 | API-2 | **FR-10** | **T3** shipping→cancel | checkout → admin `{confirmed}` → admin `{shipping}` → state `shipping` → `{{ordShipping}}` | `PUT /api/orders/{{ordShipping}}/cancel` | `Bearer {{userToken}}` | — | **400** ⚠ | `{"error": <string>}`. **ĐẶT EXPECTED = 400** (FR-10: user không được hủy khi shipping). **Assertion kép:** (a) status `400`; (b) hậu kiểm `GET` → `status` vẫn `"shipping"` (đơn KHÔNG bị hủy). SUT trả `200` + chuyển sang `canceled` ⇒ **FAIL = BUG-05** | **P0** |
| TC-O2-019 | API-2 | FR-10 | **T4** delivered→cancel | checkout → `{confirmed}` → `{shipping}` → `{delivered}` → state `delivered` → `{{ordDelivered}}` | `PUT /api/orders/{{ordDelivered}}/cancel` | `Bearer {{userToken}}` | — | **400** | `{"error":"Cannot cancel this order."}`; hậu kiểm `status` vẫn `"delivered"` (final state bất biến) | **P0** |
| TC-O2-020 | API-2 | FR-10 | **T5** canceled→cancel | checkout → user cancel → state `canceled` → `{{ordCanceled}}` | `PUT /api/orders/{{ordCanceled}}/cancel` | `Bearer {{userToken}}` | — | **400** | `{"error":"Cannot cancel this order."}`; hậu kiểm `status` vẫn `"canceled"` | **P0** |

### 2.2 Case bổ sung (idempotency & sequence)

| TC-ID | API | FR/SEC | Kịch bản | Precondition (chuỗi fixture) | Method + URL | Headers | Body | Expected status | Expected body / **assertion** | Priority |
|-------|-----|--------|----------|------------------------------|--------------|---------|------|-----------------|-------------------------------|----------|
| TC-O2-021 | API-2 | FR-10 | **Double-cancel liên tiếp** (idempotency) | checkout → đơn `pending` → `{{ordDbl}}` | `PUT /api/orders/{{ordDbl}}/cancel` **rồi gọi lại lần 2 ngay** | `Bearer {{userToken}}` | — | Lần 1: **200** · Lần 2: **400** | Lần 1 `canceled`; lần 2 `{"error":"Cannot cancel this order."}`. Hủy không idempotent kiểu "200 mỗi lần" — lần 2 phải bị chặn; đơn không bị đổi gì thêm | P1 |
| TC-O2-022 | API-2 | FR-10 | **Cancel ngay sau khi admin set delivered** | checkout → `{confirmed}` → `{shipping}` → admin `{delivered}` **vừa xong** → user cancel ngay | `PUT /api/orders/{{ordJustDelivered}}/cancel` | `Bearer {{userToken}}` | — | **400** | `{"error":"Cannot cancel this order."}`; `status` vẫn `"delivered"`. Không có "cửa sổ thời gian" cho phép hủy sau khi vừa giao | P1 |
| TC-O2-023 | API-2 | FR-10 | **Toàn vẹn dữ liệu sau BUG-05** | Như TC-018 (đơn `shipping`) | `PUT /api/orders/{{ordShipping2}}/cancel` rồi `GET /api/orders/{{ordShipping2}}` | `Bearer {{userToken}}` | — | Theo spec: `400`, state `shipping` | **Assertion hậu quả:** nếu cancel trả `200` thì đơn đang giao bị chuyển `canceled` ⇒ chứng minh **thiệt hại dữ liệu** của BUG-05 (đơn hàng đang vận chuyển bị hủy sai) | **P0** |
| TC-O2-024 | API-2 | FR-10 | **Mass-assign qua body** ở state shipping | đơn `shipping` → `{{ordShip3}}` | `PUT /api/orders/{{ordShip3}}/cancel` | `Bearer {{userToken}}` | `{"status":"delivered"}` | **400** (theo spec) | Body phải bị bỏ qua; kể cả có bug BUG-05, endpoint chỉ set `canceled`, không set theo `status` client gửi | P2 |

**Tổng nhóm state-transition: 9 test case** (TC-O2-016 → 024).
**API-2 tổng cộng: 15 (phân hoạch :id) + 9 (state-transition) = 24 test case** (TC-O2-001 → 024).

---

## Phụ lục — Hành vi SUT đã probe & verdict

> Mỗi state dựng bằng **một đơn riêng** (tránh nhiễu). Chuỗi: `checkout` (user) → `admin/orders/:id/status` (admin) từng nấc → `orders/:id/cancel` (user). DB backup trước, restore sau.

| TC-ID | Transition | Expected (SPEC) | **Actual (SUT)** | State sau khi gọi | Verdict | Bug |
|-------|-----------|-----------------|------------------|-------------------|---------|-----|
| 016 | pending → cancel | `200` → canceled | `200` `{"message":"Order canceled successfully"}` | `canceled` | ✅ PASS | — |
| 017 | confirmed → cancel | `200` → canceled | `200` `{"message":"Order canceled successfully"}` | `canceled` | ✅ PASS | — |
| **018** | **shipping → cancel** | **`400`** (giữ shipping) | **`200`** `{"message":"Order canceled successfully"}` | **`canceled`** ⚠ | ❌ **FAIL** | **BUG-05** |
| 019 | delivered → cancel | `400` (giữ delivered) | `400` `{"error":"Cannot cancel this order."}` | `delivered` | ✅ PASS | — |
| 020 | canceled → cancel | `400` (giữ canceled) | `400` `{"error":"Cannot cancel this order."}` | `canceled` | ✅ PASS | — |
| 021 | double-cancel | `200` rồi `400` | lần 1 `200` · lần 2 `400` | `canceled` | ✅ PASS | — |
| 022 | cancel sau delivered | `400` | `400` `{"error":"Cannot cancel this order."}` | `delivered` | ✅ PASS | — |
| **023** | data integrity (shipping) | `400`, giữ `shipping` | cancel `200` → đơn `shipping` chuyển `canceled` | **`canceled`** | ❌ **FAIL** | **BUG-05** |
| 024 | mass-assign body (shipping) | `400` | `200`; set `canceled` (không set `delivered` theo body) | `canceled` | ❌ FAIL (do BUG-05) / body bị bỏ qua đúng | **BUG-05** |

**Kết luận:** 9 case → **6 PASS / 3 FAIL**, cả 3 FAIL đều là **BUG-05**.

### BUG-05 (bug cắm sẵn) — hồ sơ đầy đủ

| Trường | Nội dung |
|--------|----------|
| **Severity / Priority** | **Critical / P0** |
| **FR** | FR-10 — "Khi đơn ở `shipping`, User không được phép tự hủy — chỉ Admin mới thao tác được" |
| **Steps** | (1) user checkout → đơn `pending`; (2) admin `PUT /admin/orders/:id/status {confirmed}` → `{shipping}`; (3) user `PUT /api/orders/:id/cancel` |
| **Expected** | `400` + đơn giữ nguyên `shipping` |
| **Actual** | `200` `{"message":"Order canceled successfully"}` + đơn chuyển sang `canceled` |
| **Root cause** | `server.js:328-331` — guard chỉ chặn `delivered`/`canceled`: `if (order.status === "delivered" \|\| order.status === "canceled")`. Thiếu chặn `shipping`. Trong code còn comment thừa nhận: `// Lẽ ra phải là: if (order.status !== 'pending' && order.status !== 'confirmed')` |
| **Impact** | Người dùng tự hủy được đơn **đang vận chuyển** → sai nghiệp vụ giao hàng, mất toàn vẹn trạng thái đơn (TC-023) |
| **Fix gợi ý** | Đổi guard thành whitelist: `if (order.status !== 'pending' && order.status !== 'confirmed') return 400;` |

> **Điểm nhấn phương pháp:** đây là lý do đề bài nhấn mạnh *"đừng để expected = 200 kể cả nếu code cho 200"*.
> Nếu lấy expected theo hành vi quan sát (`200`) thì test **xanh** và **giấu mất bug**. Chỉ khi expected bám
> **spec** (`400`) thì test mới **đỏ đúng chỗ** và lộ ra BUG-05. Đây là bản chất của state-transition testing:
> oracle đến từ mô hình trạng thái, không từ implementation.
