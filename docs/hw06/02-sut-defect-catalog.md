# 02 — Phân tích SUT & Danh mục Lỗi (Defect Catalog)

> **Vai trò của tài liệu này:** đây là **oracle** — nguồn sự thật để (a) audit test case do AI sinh ra ở bước R-02, (b) biết trước bug nào là thật để viết bug report ở bước R-05, (c) quyết định assertion nào sẽ pass / fail khi chạy Newman.
>
> **Nguồn đối chiếu:**
> - **Đặc tả nghiệp vụ đúng** → `README.md` (System Requirements Specification v2.0)
> - **Đặc tả API** → `api_specification.md`
> - **Hiện thực thực tế** → `backend/server.js`, `backend/database.js`
>
> ⚠️ SUT là ứng dụng **cố tình cài lỗi** để phục vụ học kiểm thử. Khoảng cách giữa `README.md` và `server.js` chính là đề bài.

---

## 0. Thông tin nền tảng cần biết trước khi thiết kế test

| Mục | Giá trị | Ảnh hưởng tới thiết kế test |
| :--- | :--- | :--- |
| Base URL | `http://localhost:3000` | Thoả R-15 (hostname `localhost`) |
| Stack | Node.js + Express 5 + SQLite (`sqlite3`) | — |
| Tài khoản admin | `admin@eshop.com` / `Admin123!` | Dùng cho API-3 |
| Tài khoản user | `test@eshop.com` / `Test1234!` | Dùng cho API-1, API-2 |
| JWT secret | Hard-code trong `server.js:9` | Cho phép tự ký token giả → test role escalation |
| **DB reset mỗi lần khởi động** | `database.js:117` gọi `initDatabase()` ngay khi `require`, mà hàm này `DROP TABLE IF EXISTS` toàn bộ bảng (`database.js:15-21`) | 🔴 **Cực kỳ quan trọng:** cứ restart backend là **mất sạch dữ liệu** và ID tự tăng về đầu. ⇒ Test phải **tự tạo tiền đề** (tự đăng ký user, tự tạo đơn) chứ không được phụ thuộc ID cứng. Đổi lại, CI có môi trường sạch và **tất định** mỗi lần chạy. |
| Seed sẵn | 3 category, 2 user, 5 product (id 1–5), 4 coupon | `products.id` 1..5; user id 1 = admin, id 2 = test user |
| Giỏ hàng | Lưu **trong RAM** (`server.js:14` — biến `userCarts`) | Giỏ hàng không nằm trong DB, mất khi restart |

---

## 1. API-1 — `POST /api/login` (Pool A · FR-02)

**Mã nguồn:** `backend/server.js:32-67`

### 1.1 Đặc tả yêu cầu (FR-02 + SEC)

- Người dùng nhập Email và Mật khẩu.
- Sau mỗi lần đăng nhập sai, hệ thống tăng bộ đếm lên **đúng 1 đơn vị**.
- Sai **từ 3 lần trở lên** liên tiếp ⇒ khoá tạm **30 giây**; trả thông báo lỗi phù hợp, **không để lộ chi tiết nguyên nhân**.
- Đăng nhập thành công trả JWT Token, gửi kèm mọi request qua `Authorization: Bearer <token>`.
- SEC-01: mật khẩu **không** được lưu plaintext. SEC-02: API bảo mật phải yêu cầu JWT hợp lệ. SEC-05: truy vấn phải dùng Parameterized Query.

### 1.2 Danh mục lỗi

| ID | Mức độ | Yêu cầu vi phạm | Mô tả lỗi | Vị trí | Biểu hiện quan sát được |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **D-LOGIN-01** | Major | FR-02 | Bộ đếm sai tăng **+2** thay vì **+1** | `server.js:54` | Sai 1 lần → `login_attempts = 2`; sai **2 lần** → `= 4 ≥ 3` ⇒ **khoá sớm ở lần thứ 2** thay vì lần thứ 3 |
| **D-LOGIN-02** | Major | FR-02 | Thời gian khoá **180 000 ms = 180 giây** thay vì **30 giây** | `server.js:57` | Sau khi bị khoá, đăng nhập đúng mật khẩu vẫn `403` suốt 3 phút |
| **D-LOGIN-03** | **Critical** | SEC-01 | Response trả về **nguyên bản ghi user**, gồm cả `password` plaintext, `reset_token`, `login_attempts`, `locked_until` | `server.js:52` | `POST /api/login` (200) → body chứa `user.password = "Test1234!"` |
| **D-LOGIN-04** | **Critical** | SEC-01 | Mật khẩu **lưu plaintext** trong DB và so sánh bằng `===` | `server.js:46`, `database.js:91-93` | Không hash, không salt |
| **D-LOGIN-05** | Major | SEC-02 | JWT ký bằng secret hard-code trong mã nguồn và **không có `expiresIn`** | `server.js:9`, `server.js:51` | Token **không bao giờ hết hạn**; ai đọc được repo là tự ký được token admin |
| **D-LOGIN-06** | Major | FR-02 | Bộ đếm **không được reset khi hết hạn khoá** | `server.js:54` | Hết 180 s, chỉ cần sai **1 lần** là `attempts = 6 ≥ 3` ⇒ bị khoá lại ngay lập tức |
| **D-LOGIN-07** | Minor | FR-02 | Thông báo khi bị khoá **lộ nguyên nhân** ("Tài khoản đã bị khóa…") và dùng mã `403` khác với `401` của sai mật khẩu | `server.js:41-43` | Kẻ tấn công phân biệt được email nào tồn tại/đang bị khoá ⇒ user enumeration |
| **D-LOGIN-08** | Minor | — | Không validate body: thiếu `email`/`password`, sai kiểu dữ liệu đều **không** trả `400` | `server.js:33` | `{}` → `401` thay vì `400` |
| **D-LOGIN-09** | Minor | FR-02 | Không có rate-limit ở tầng IP; cơ chế khoá gắn theo tài khoản nên vẫn quét được nhiều email song song | `server.js:32` | — |

### 1.3 Hành vi **đúng** — dùng để viết test case pass (rất quan trọng khi audit)

| Điểm | Kết luận | Ghi chú cho bước Audit |
| :--- | :--- | :--- |
| SQL Injection ở `/api/login` | ✅ **KHÔNG có lỗi** — dùng parameterized query `db.get("… WHERE email = ?", [email])` (`server.js:35`) | AI gần như chắc chắn sẽ sinh case *"SQLi trên login"*. Case đó **VALID** nhưng **expected result phải là "bị từ chối an toàn, trả 401"**, không phải "đăng nhập được". Nếu AI viết expected là "bypass thành công" ⇒ gán **INVALID**. |
| Email không tồn tại | ✅ Trả `401 {"error":"Invalid email or password"}` — không lộ email có tồn tại hay không | Đúng chuẩn |
| Đăng nhập thành công | ✅ Reset `login_attempts = 0`, xoá `locked_until` (`server.js:47-50`) | Đúng chuẩn |

---

## 2. API-2 — `POST /api/checkout` (Pool B · FR-08, FR-10)

**Mã nguồn:** `backend/server.js:297-309`

### 2.1 Đặc tả yêu cầu (FR-08)

- Chỉ người dùng **đã đăng nhập** mới thanh toán được.
- Tổng tiền tính **tự động từ giỏ hàng**, người dùng **không được chỉnh sửa trực tiếp**.
- **Backend phải tự tính lại tổng tiền; không chấp nhận `total_amount` do client gửi lên.**
- Sau thanh toán thành công, **giỏ hàng được xoá**.
- Đơn mới tạo ở trạng thái `pending` (FR-10).

### 2.2 Danh mục lỗi

| ID | Mức độ | Yêu cầu vi phạm | Mô tả lỗi | Vị trí | Biểu hiện quan sát được |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **D-CHK-01** | **Critical** | FR-08 | Backend **tin tuyệt đối `total_amount` từ client**, không hề đọc giỏ hàng để tính lại | `server.js:299-303` | Giỏ 30 triệu nhưng gửi `total_amount: 1` → đơn hàng được tạo với giá 1 ₫ |
| **D-CHK-02** | Major | FR-08 | Không validate `total_amount`: chấp nhận **số âm**, `0`, chuỗi, `null`, thiếu hẳn trường | `server.js:299` | `total_amount: -500000` → tạo đơn thành công, `200` |
| **D-CHK-03** | Major | FR-08 | **Giỏ hàng không được xoá** sau checkout | `server.js:297-309` | `GET /api/cart` sau checkout vẫn trả nguyên nội dung cũ |
| **D-CHK-04** | Major | FR-08 | Checkout thành công **với giỏ hàng rỗng** | `server.js:297` | Không đăng gì vào giỏ vẫn tạo được đơn |
| **D-CHK-05** | Major | SEC-04 / FR-18 | `shipping_address` không validate, không escape — lưu nguyên payload | `server.js:299-303` | Gửi `<img src=x onerror=alert(1)>` → lưu nguyên vào DB, hiển thị lại ở màn Admin (FR-18 yêu cầu hiển thị an toàn) |
| **D-CHK-06** | Minor | — | Giỏ hàng lưu **trong RAM**, không đồng bộ DB, mất khi restart | `server.js:14, 284-295` | Ảnh hưởng tính đúng đắn khi scale/restart |
| **D-CHK-07** | Major | SEC-02 | `GET /api/orders/:id` **thiếu hoàn toàn `authenticateToken`** ⇒ **IDOR**: bất kỳ ai (kể cả chưa đăng nhập) đọc được đơn hàng của bất kỳ ai | `server.js:344` | So sánh trực tiếp với `GET /api/orders/my-orders` (`server.js:311`) *có* auth |
| **D-CHK-08** | Minor | — | Không idempotent: gửi lại request y hệt tạo thêm đơn trùng | `server.js:297` | Double-submit → 2 đơn |

> 💡 **D-CHK-07 là "viên ngọc" cho bước R-03 (Extend).** AI thường chỉ sinh test cho **đúng endpoint được hỏi** (`POST /api/checkout`) nên rất hay bỏ sót lỗ hổng ở **endpoint kề bên trong cùng luồng nghiệp vụ** (đọc lại đơn vừa tạo). Đây là ví dụ hoàn hảo để giải thích *"vì sao AI bỏ sót"* = **giới hạn phạm vi ngữ cảnh của prompt**.

### 2.3 Hành vi **đúng**

| Điểm | Kết luận |
| :--- | :--- |
| Yêu cầu JWT | ✅ Có `authenticateToken` — không token → `401`, token sai → `403` |
| Trạng thái đơn khởi tạo | ✅ Luôn là `pending` (`server.js:303`) — đúng FR-10 |
| `user_id` lấy từ token | ✅ `req.user.id`, **không** lấy từ body ⇒ không giả mạo được chủ đơn |
| Câu lệnh SQL | ✅ Parameterized |

---

## 3. API-3 — `PUT /api/admin/orders/:id/status` (Pool C · FR-10, FR-12, FR-18)

**Mã nguồn:** `backend/server.js:525-568`

### 3.1 Đặc tả yêu cầu

**FR-10 — State machine:**

```
pending ──[admin xác nhận]──► confirmed ──[admin giao]──► shipping ──[admin hoàn tất]──► delivered
   │                              │
   └──[user/admin huỷ]──► canceled ◄──[user/admin huỷ]──┘
```

- `delivered` và `canceled` là **trạng thái kết thúc** — không được chuyển sang bất kỳ trạng thái nào khác.
- Khi đơn ở `shipping`, **user không được tự huỷ** — **chỉ Admin mới thao tác được**.
- Mọi chuyển đổi không hợp lệ phải trả lỗi kèm thông báo phù hợp.

**FR-12 / SEC-03:** mọi API `/api/admin/*` phải yêu cầu ① JWT hợp lệ **và** ② `role = 'admin'` trong token — *"không chỉ kiểm tra sự tồn tại của Token"*.

### 3.2 Ma trận chuyển trạng thái: Đặc tả ⟷ Hiện thực

Bảng này sinh trực tiếp **25 test case** cho API-3.

| Từ \ Sang | `pending` | `confirmed` | `shipping` | `delivered` | `canceled` |
| :--- | :-: | :-: | :-: | :-: | :-: |
| **`pending`** | ✅❌ / ✅❌ | ✅✅ / ✅✅ | ❌ / ❌ | ❌ / ❌ | ✅✅ / ✅✅ |
| **`confirmed`** | ❌ / ❌ | ❌ / ❌ | ✅✅ / ✅✅ | ❌ / ❌ | ✅✅ / ✅✅ |
| **`shipping`** | ❌ / ❌ | ❌ / ❌ | ❌ / ❌ | ✅✅ / ✅✅ | **✅ / ❌ ⚠️ D-ADM-03** |
| **`delivered`** | ❌ / ❌ | ❌ / ❌ | ❌ / ❌ | ❌ / ❌ | ❌ / ❌ |
| **`canceled`** | ❌ / ❌ | ❌ / ❌ | ❌ / ❌ | **❌ / ✅ 🔴 D-ADM-02** | ❌ / ❌ |

*Ký hiệu ô: `Đặc tả / Hiện thực` — ✅ = cho phép, ❌ = phải từ chối (400).*
*Đối chiếu mã: whitelist transition ở `server.js:537-551`.*

### 3.3 Danh mục lỗi

| ID | Mức độ | Yêu cầu vi phạm | Mô tả lỗi | Vị trí | Biểu hiện quan sát được |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **D-ADM-01** | 🔴 **Critical** | FR-12, SEC-03 | Endpoint chỉ gọi `authenticateToken`, **hoàn toàn không kiểm tra `role === 'admin'`** | `server.js:525` | **Role escalation:** token của `test@eshop.com` (role `user`) đổi được trạng thái đơn của **bất kỳ** ai |
| **D-ADM-02** | 🔴 **Critical** | FR-10 | Cho phép chuyển **`canceled → delivered`** | `server.js:550-551` | Đơn đã huỷ "sống lại" thành đã giao ⇒ sai doanh thu ở Dashboard FR-13 (chỉ tính `delivered`) |
| **D-ADM-03** | Major | FR-10 | **Thiếu** transition `shipping → canceled` cho Admin, dù đặc tả nói *"khi ở shipping chỉ Admin mới thao tác được"* | `server.js:547-548` | Admin không huỷ được đơn đang giao ⇒ trả `400` |
| **D-ADM-04** | Major | — | Callback `db.run` **bỏ qua biến `err`** ⇒ luôn trả `200 "Order status updated"` kể cả khi UPDATE thất bại | `server.js:562-566` | False positive: client tưởng thành công |
| **D-ADM-05** | Minor | — | Response chỉ có `{message}`, **không trả trạng thái mới** | `server.js:565` | Phải gọi thêm request khác để verify ⇒ khó viết assertion; schema nghèo nàn |
| **D-ADM-06** | Minor | — | Không validate `status` thuộc enum 5 giá trị một cách tường minh (may mắn được whitelist transition chặn gián tiếp) | `server.js:526` | `status: "DELIVERED"` (hoa) → `400` "Invalid state transition" thay vì "giá trị không hợp lệ" |
| **D-ADM-07** | Minor | — | Không ghi audit log ai đổi trạng thái, lúc nào | `server.js:525` | Không truy vết được |

### 3.4 Lỗi liên quan cùng state machine (dùng cho bước Extend R-03)

| ID | Mức độ | Yêu cầu vi phạm | Mô tả | Vị trí |
| :--- | :--- | :--- | :--- | :--- |
| **D-ADM-08** | Major | FR-10 | `PUT /api/orders/:id/cancel` (endpoint của **user**) cho phép huỷ khi đơn đang ở **`shipping`** — đặc tả cấm user tự huỷ ở trạng thái này. Điều kiện chặn chỉ là `delivered`/`canceled` | `server.js:326-329` — **trong mã nguồn có sẵn comment thú nhận:** `// Lẽ ra phải là: if (order.status !== 'pending' && order.status !== 'confirmed')` |
| **D-ADM-09** | Major | FR-12, SEC-03 | Lỗi thiếu `role='admin'` mang tính **hệ thống**, lặp lại ở `GET /api/admin/users`, `DELETE /api/admin/users/:id`, `GET /api/admin/orders`, `POST /api/admin/coupons`, `POST /api/admin/import-products` | `server.js:494, 504, 510, 457, 199` |

### 3.5 Hành vi **đúng**

| Điểm | Kết luận |
| :--- | :--- |
| Order không tồn tại | ✅ Trả `404 {"error":"Order not found"}` (`server.js:532`) |
| `delivered` là trạng thái kết thúc | ✅ Không có transition nào ra khỏi `delivered` |
| Câu lệnh SQL | ✅ Parameterized ⇒ SQLi qua `:id` bị chặn |
| Không có token | ✅ `401`; token sai chữ ký ✅ `403` |

---

## 4. Lỗi ngoài phạm vi 3 API đã chọn (tham khảo — **không** đưa vào bug report của HW06)

Ghi lại để (a) tránh nhầm khi audit, (b) làm nguyên liệu cho phần AI Critique.

| Endpoint | Lỗi | Vị trí |
| :--- | :--- | :--- |
| `GET /api/products?search=` | **SQL Injection thật** — nối chuỗi trực tiếp `WHERE name LIKE '%${searchQuery}%'`, vi phạm SEC-05; lỗi DB còn trả về **HTML** | `server.js:144-150` |
| `GET /api/products/:id` | `price` trả về **kiểu string** khi `id` chẵn ⇒ sai schema; id không tồn tại trả `200 {}` thay vì `404` | `server.js:159-165` |
| `POST/PUT/DELETE /api/products` | **Không có xác thực nào cả** — ai cũng thêm/sửa/xoá sản phẩm được | `server.js:167, 179, 191` |
| `PUT /api/users/me` | Cho phép client **tự đổi `role`** ⇒ tự nâng quyền lên admin, vi phạm SEC-06 | `server.js:118-131` |
| `GET /api/users/me` | Trả nguyên bản ghi gồm `password` | `server.js:112-116` |
| `POST /api/forgot-password` | OTP chỉ **4 chữ số** (`1000 + random*9000`) thay vì 6, **không có hạn dùng** ⇒ vi phạm SEC-07 | `server.js:72` |
| `POST /api/register` | Không validate gì: email sai định dạng, mật khẩu yếu, email trùng, thiếu xác nhận mật khẩu — đều tạo tài khoản thành công | `server.js:20-30` |
| `POST /api/apply-coupon` | Công thức percent sai dấu: `discount = total × (1 − discount_value)`; với `SAVE10` (value = 10) → `discount = −9 × total` ⇒ `final_amount = 10 × total`. Ngoài ra C3 dùng `>` thay vì `>=`, và **không kiểm tra JWT** (C4) | `server.js:379, 399-400, 419-420` |
| `POST /api/admin/import-products` | **Không rollback** khi có dòng lỗi (FR-16 yêu cầu all-or-nothing); không kiểm tra `price > 0` | `server.js:199-241` |

---

## 5. Bảng tổng hợp bug dự kiến đưa vào GitHub Issues

Đây là danh sách **tối thiểu** cần mở issue (bước R-05). Mỗi issue phải có `Found by Test Case: TC-…` theo `Rule.pdf` §H.1.

| # | Bug ID | API | Tiêu đề issue dự kiến | Severity / Priority | Requirement |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | D-LOGIN-01 | API-1 | `[BUG][API-Login] Bộ đếm đăng nhập sai tăng 2 đơn vị, tài khoản bị khoá ngay ở lần sai thứ 2` | Major / P1 | FR-02 |
| 2 | D-LOGIN-02 | API-1 | `[BUG][API-Login] Thời gian khoá tài khoản là 180 giây thay vì 30 giây theo đặc tả` | Major / P1 | FR-02 |
| 3 | D-LOGIN-03 | API-1 | `[BUG][API-Login] Response đăng nhập trả về mật khẩu plaintext của người dùng` | Critical / P0 | SEC-01 |
| 4 | D-LOGIN-05 | API-1 | `[BUG][API-Login] JWT không có thời hạn hết hạn và ký bằng secret hard-code` | Major / P1 | SEC-02 |
| 5 | D-LOGIN-06 | API-1 | `[BUG][API-Login] Bộ đếm sai không được reset sau khi hết hạn khoá, gây khoá lại tức thì` | Major / P1 | FR-02 |
| 6 | D-CHK-01 | API-2 | `[BUG][API-Checkout] Backend chấp nhận total_amount do client gửi, không tính lại từ giỏ hàng` | Critical / P0 | FR-08 |
| 7 | D-CHK-02 | API-2 | `[BUG][API-Checkout] Tạo được đơn hàng với total_amount âm hoặc bằng 0` | Major / P1 | FR-08 |
| 8 | D-CHK-03 | API-2 | `[BUG][API-Checkout] Giỏ hàng không được xoá sau khi thanh toán thành công` | Major / P1 | FR-08 |
| 9 | D-CHK-04 | API-2 | `[BUG][API-Checkout] Thanh toán thành công với giỏ hàng rỗng` | Major / P2 | FR-08 |
| 10 | D-CHK-07 | API-2 | `[BUG][API-Order] IDOR — GET /api/orders/:id không yêu cầu xác thực, lộ đơn hàng người khác` | Critical / P0 | SEC-02 |
| 11 | D-ADM-01 | API-3 | `[BUG][API-Admin] Role escalation — user thường đổi được trạng thái đơn hàng qua API admin` | Critical / P0 | FR-12, SEC-03 |
| 12 | D-ADM-02 | API-3 | `[BUG][API-Admin] Cho phép chuyển trạng thái canceled → delivered, vi phạm trạng thái kết thúc` | Critical / P0 | FR-10 |
| 13 | D-ADM-03 | API-3 | `[BUG][API-Admin] Admin không huỷ được đơn ở trạng thái shipping` | Major / P2 | FR-10 |
| 14 | D-ADM-04 | API-3 | `[BUG][API-Admin] Luôn trả 200 kể cả khi lệnh UPDATE thất bại (bỏ qua err)` | Major / P2 | — |
| 15 | D-ADM-08 | API-3 | `[BUG][API-Order] User tự huỷ được đơn đang ở trạng thái shipping` | Major / P1 | FR-10 |

> **Ghi chú cho bước Audit:** con số 15 bug này là **kỳ vọng**, không phải hạn mức. Nếu khi chạy thật phát hiện thêm/bớt, cập nhật lại bảng và ghi rõ trong `bug-report.md`. **Tuyệt đối không mở issue cho bug chưa tái hiện được bằng một test case cụ thể** — vi phạm nguyên tắc *"Bug phải truy ngược được test case nào đã phát hiện"* của `Rule.pdf`.
