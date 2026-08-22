# API Specification — EShop (Scope: FR-05, FR-10, FR-15)

> **Phạm vi:** Tài liệu này chỉ đặc tả **3 API trong scope** của HW06:
> | # | FR | Endpoint | Nguồn code |
> |---|----|----------|-----------|
> | API-1 | FR-05 / FR-06 | `GET /api/products/:id` | `eshop-sut/backend/server.js:160-166` |
> | API-2 | FR-10 | `PUT /api/orders/:id/cancel` | `eshop-sut/backend/server.js:320-343` |
> | API-3 | FR-15 | `POST /api/products` + `PUT /api/products/:id` | `eshop-sut/backend/server.js:168-197` |
>
> **Base URL:** `http://localhost:3000`
> **Content-Type:** `application/json`
> **Header bắt buộc cho bài nộp:** mọi request kèm `X-Student-Id: <MSSV>` (yêu cầu HW06, không phải yêu cầu của SUT).
>
> **Quan trọng — tài liệu này ghi HAI cột hành vi:**
> - **Spec (FR)** = hành vi *đúng theo* `README.md` của SUT (dùng làm **Expected** khi viết test case).
> - **Thực tế (SUT)** = hành vi *quan sát được* khi chạy live (`node server.js`), dùng làm **Actual**.
> - Chỗ hai cột **lệch nhau** = **BUG** đã được kiểm chứng bằng cURL (xem bảng cuối mỗi mục).

---

## Tài khoản seed (để lấy token / dựng tiền đề)

| Vai trò | Email | Password |
|---------|-------|----------|
| Admin | `admin@eshop.com` | `Admin123!` |
| User | `test@eshop.com` | `Test1234!` |

Lấy token:
```bash
curl -s -X POST localhost:3000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@eshop.com","password":"Test1234!"}'
# -> { "message":"Login successful", "token":"<JWT>", "user":{...} }
```

Bảng `products` seed sẵn 5 sản phẩm (id 1–5). Schema (từ `database.js`):
```
products( id INTEGER PK, name TEXT, price INTEGER,
          description TEXT, imageUrl TEXT, category_id INTEGER )
```
> Lưu ý: **không** có ràng buộc `NOT NULL`, không `CHECK`, không FK trên `category_id` ⇒ DB chấp nhận rỗng/âm/không tồn tại.

---

## API-1 — `GET /api/products/:id` (FR-05 / FR-06 · Xem chi tiết sản phẩm)

### Mô tả
Trả về chi tiết một sản phẩm theo `id`. **Không yêu cầu** xác thực.

### Request
- **Method / Path:** `GET /api/products/:id`
- **Path param:** `id` — định danh sản phẩm.
- **Auth:** không.
- **Body:** không.

### Response — hành vi THỰC TẾ của SUT
| Trường hợp | HTTP thực tế | Body thực tế |
|---|---|---|
| `id` tồn tại, **id lẻ** | `200` | Object đầy đủ, `price` kiểu **number**: `{"id":1,"name":"iPhone 15 Pro Max","price":30000000,...}` |
| `id` tồn tại, **id chẵn** | `200` | Object đầy đủ nhưng `price` bị ép thành **string**: `{"id":2,...,"price":"28000000",...}` |
| `id` không tồn tại (vd `99999`) | `200` | `{}` (object rỗng) |
| `id` phi số (vd `abc`) | `200` | `{}` |
| `id` = `0`, `-1` | `200` | `{}` |
| `id` = `1.0` | `200` | Trả về sản phẩm id 1 (SQLite ép `1.0`→`1`) |

Ví dụ response id lẻ (id=1):
```json
{
  "id": 1,
  "name": "iPhone 15 Pro Max",
  "price": 30000000,
  "description": "Điện thoại cao cấp của Apple",
  "imageUrl": "https://placehold.co/300x300/png?text=iPhone+15",
  "category_id": 1
}
```

### Bug đã kiểm chứng (Expected theo FR vs Actual)
| Bug | Điều kiện | Expected (FR-06) | Actual (SUT) | Ghi chú |
|-----|-----------|------------------|--------------|---------|
| **BUG-01** | `GET /api/products/2` (id chẵn) | `price` là **number** (nhất quán với id lẻ và schema `INTEGER`) | `price` là **string** `"28000000"` | `server.js:163` `if (row.id % 2 === 0) row.price = row.price.toString()` — lỗi kiểu dữ liệu, phá vỡ contract. |
| **BUG-02** | `GET /api/products/99999` (không tồn tại) | `404 Not Found` | `200` với body `{}` | `server.js:161` trả `res.status(200).json({})`. Client không phân biệt được "không có" với "có". |
| **BUG-03** | `GET /api/products/abc` (id phi số) | `400 Bad Request` (id không hợp lệ) | `200 {}` | Không validate kiểu param. |

> **Test hint:** dùng phân hoạch tương đương (id hợp lệ lẻ/chẵn, id không tồn tại, id phi số, biên `0`/`-1`) + assert **kiểu** của `price` (không chỉ giá trị) để bắt BUG-01.

---

## API-2 — `PUT /api/orders/:id/cancel` (FR-10 · Hủy đơn hàng)

### Mô tả
User tự hủy đơn hàng **của chính mình**. Theo FR-10, chỉ được hủy khi đơn ở trạng thái `pending` hoặc `confirmed`.

### Request
- **Method / Path:** `PUT /api/orders/:id/cancel`
- **Auth:** **bắt buộc** — `Authorization: Bearer <token>`.
- **Body:** không.

### State machine (FR-10)
```
pending    ──(User/Admin hủy)──► canceled     ✔ cho phép
confirmed  ──(User/Admin hủy)──► canceled     ✔ cho phép
shipping   ──(chỉ ADMIN)───────► canceled     ✘ USER KHÔNG được hủy
delivered  = trạng thái kết thúc               ✘ không được hủy
canceled   = trạng thái kết thúc               ✘ không được hủy
```

### Response — hành vi THỰC TẾ (đã kiểm chứng live)
| Trạng thái đơn trước khi gọi | HTTP thực tế | Body thực tế |
|---|---|---|
| `pending` | `200` | `{"message":"Order canceled successfully"}` |
| `confirmed` | `200` | `{"message":"Order canceled successfully"}` |
| `shipping` | `200` ⚠️ | `{"message":"Order canceled successfully"}` |
| `delivered` | `400` | `{"error":"Cannot cancel this order."}` |
| `canceled` (hủy lại) | `400` | `{"error":"Cannot cancel this order."}` |
| Đơn không tồn tại / không thuộc về user | `404` | `{"error":"Order not found"}` |
| Thiếu token | `401` | `{"error":"Unauthorized"}` |
| Token sai / hết hạn | `403` | `{"error":"Forbidden"}` |

### Bug đã kiểm chứng
| Bug | Điều kiện | Expected (FR-10) | Actual (SUT) | Ghi chú |
|-----|-----------|------------------|--------------|---------|
| **BUG-05** (bug cắm sẵn) | Đơn ở `shipping`, user gọi cancel | `400` — user không được hủy khi đang giao | `200 "Order canceled successfully"` | `server.js:327-331`: guard chỉ chặn `delivered`/`canceled`; còn comment thừa nhận `// Lẽ ra phải là: if (status !== 'pending' && status !== 'confirmed')`. **Critical/P0.** |

> **Test hint:** đây là state-transition testing. Với mỗi trạng thái nguồn, dựng tiền đề bằng: `POST /api/checkout` → `PUT /api/admin/orders/:id/status` (token admin) để đẩy trạng thái, rồi gọi cancel. **Nhớ đặt Expected của case `shipping` = 400** (đừng để AI tự đặt 200 theo hành vi thực tế).

---

## API-3 — Quản lý sản phẩm (FR-15 · Product CRUD)

Gồm 2 endpoint trong scope: **tạo** và **sửa theo id**.

### Ràng buộc đầu vào theo FR-15 (dùng làm Expected)
- `name`: **bắt buộc**, tối đa **255** ký tự.
- `price`: **bắt buộc**, phải là số **dương (> 0)**.
- `category_id`: **bắt buộc**, phải tồn tại trong bảng `categories`.
- Khi **sửa**: chỉ sản phẩm đó thay đổi; các sản phẩm khác giữ nguyên; **không** được null hóa field không gửi.

### A. `POST /api/products` — Tạo sản phẩm
- **Auth:** ⚠️ **KHÔNG** yêu cầu (route không gắn `authenticateToken`).
- **Body:**
  ```json
  { "name": "Tên SP", "price": 100000, "description": "Mô tả", "imageUrl": "http://...", "category_id": 1 }
  ```
- **Response thực tế:** luôn `200` `{"message":"Product created","id":<lastID>}` — **không validate gì**.

### B. `PUT /api/products/:id` — Sửa sản phẩm
- **Auth:** ⚠️ **KHÔNG** yêu cầu.
- **Body:** kỳ vọng đủ 5 field (`name, price, description, imageUrl, category_id`).
- **Response thực tế:** luôn `200` `{"message":"Product updated"}` — kể cả khi `id` không tồn tại (no-op im lặng).
- **Cơ chế:** câu lệnh là `UPDATE products SET name=?, price=?, ... WHERE id=?` với **tất cả** field ⇒ field nào không gửi sẽ bị set **NULL** (destructive full-replace).

### Bug đã kiểm chứng
| Bug | Request | Expected (FR-15) | Actual (SUT) | Ghi chú |
|-----|---------|------------------|--------------|---------|
| **BUG-08** | `POST` `{"name":"","price":-500,"category_id":9999}` | `400` — name bắt buộc, price>0, category phải tồn tại | `200` Product created | Không validate. `server.js:168-179`. **Critical/P0.** |
| **BUG-09** | `POST` `{}` (body rỗng) | `400` | `200` created (record toàn `null`) | Major/P1. |
| **BUG-10** | `POST` với `name` dài 300 ký tự | `400` — tối đa 255 | `200` created | Major/P1. |
| **BUG-11** | `PUT /api/products/1 -d '{"name":"x"}'` rồi `GET /api/products/1` | Chỉ đổi `name`; các field khác giữ nguyên | `price/description/imageUrl/category_id` bị set **null** → **mất dữ liệu** | `server.js:186-193`. **Critical/P0.** |
| **BUG-12** | `PUT /api/products/99999` (không tồn tại) | `404` | `200 "Product updated"` (no-op) | Major/P1. |
| **SEC/AUTH** | `POST`/`PUT`/`DELETE` **không kèm token** | `401`/`403` (chỉ admin — FR-15) | `200` thành công | Thiếu auth & phân quyền hoàn toàn. |

### Ghi chú route âm bản
- `POST /api/products/:id` **không tồn tại** ⇒ trả `404` HTML mặc định của Express (`Cannot POST /api/products/1`), **không phải** JSON. Có thể đưa 1 test case negative để chứng minh.

> **Test hint:** kết hợp phân hoạch/biên trên `name` (rỗng, 255, 256, 300), `price` (âm, 0, dương, phi số), `category_id` (tồn tại, không tồn tại). Với BUG-11 dùng **side-effect isolation**: snapshot `GET /api/products` trước/sau `PUT` để chứng minh dữ liệu bị null hóa và/hoặc sản phẩm khác có bị ảnh hưởng không.

---

## Phụ lục — Lệnh cURL tái lập nhanh

```bash
cd eshop-sut/backend && npm install && node server.js   # dựng SUT (mỗi lần chạy sẽ DROP + reseed DB)

# API-1: kiểu price lệch giữa id lẻ/chẵn
curl -s localhost:3000/api/products/1   # price: number
curl -s localhost:3000/api/products/2   # price: "string"
curl -s localhost:3000/api/products/99999   # {} + HTTP 200

# API-3: tạo không validate + partial PUT null hóa
curl -s -X POST localhost:3000/api/products -H "Content-Type: application/json" -d '{}'
curl -s -X PUT  localhost:3000/api/products/1 -H "Content-Type: application/json" -d '{"name":"x"}'
curl -s localhost:3000/api/products/1   # các field khác -> null

# API-2: user hủy đơn shipping (BUG-05)
UT=$(curl -s -X POST localhost:3000/api/login -H 'Content-Type: application/json' -d '{"email":"test@eshop.com","password":"Test1234!"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["token"])')
AT=$(curl -s -X POST localhost:3000/api/login -H 'Content-Type: application/json' -d '{"email":"admin@eshop.com","password":"Admin123!"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["token"])')
OID=$(curl -s -X POST localhost:3000/api/checkout -H "Authorization: Bearer $UT" -H 'Content-Type: application/json' -d '{"total_amount":200000,"shipping_address":"HCM"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["orderId"])')
curl -s -X PUT localhost:3000/api/admin/orders/$OID/status -H "Authorization: Bearer $AT" -H 'Content-Type: application/json' -d '{"status":"confirmed"}'
curl -s -X PUT localhost:3000/api/admin/orders/$OID/status -H "Authorization: Bearer $AT" -H 'Content-Type: application/json' -d '{"status":"shipping"}'
curl -s -X PUT localhost:3000/api/orders/$OID/cancel -H "Authorization: Bearer $UT"   # -> 200 (đáng lẽ 400)
```

> Tất cả hành vi "Thực tế" trong tài liệu này đã được chạy trực tiếp trên bản local `node server.js` ngày lập tài liệu; DB được khôi phục nguyên trạng sau khi dò.
