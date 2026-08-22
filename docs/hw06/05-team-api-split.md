# 05 — Phân chia API cho nhóm 5 người (HW06)

> **Ràng buộc từ đề (Requirements.pdf §5):** mỗi thành viên chọn **3 API**, mỗi API thuộc **một pool khác nhau** (A / B / C — Pool D mobile không dùng). **Không hai thành viên nào được trùng bộ 3.** HW06 là **bài cá nhân**: chia API chỉ để tránh trùng, mỗi người tự làm trọn pipeline R-01→R-05 + Agent Skill trên repo/branch của mình.
>
> Bảng dưới chia **không giao nhau một endpoint chính nào** (mạnh hơn mức đề yêu cầu) và đã kiểm tra từng endpoint có bug thật trong `backend/server.js` để ai cũng có nguyên liệu viết bug report.

## Bảng chia

| TV | Pool A | Pool B | Pool C |
| :--- | :--- | :--- | :--- |
| **1 — 23127207 (đã làm)** | FR-02 `POST /api/login` | FR-08 `POST /api/checkout` | FR-18 `PUT /api/admin/orders/:id/status` |
| **2** | FR-03 `POST /api/forgot-password` | FR-09 `POST /api/apply-coupon` | FR-17 `POST` + `/api/admin/coupons[/:id]` |
| **3** | FR-05  `GET /api/products/:id`) | FR-10 `PUT /api/orders/:id/cancel` | FR-15 `POST /api/products[/:id]` |
| **4** | FR-04 `PUT /api/users/me`  | FR-07 `POST /api/cart` | FR-19 `DELETE /api/admin/users/:id` |
| **5** | FR-01 `POST /api/register` | FR-11 `GET /api/orders/my-orders` | FR-16 `POST /api/admin/import-products` |

Với 5 người, **Pool B đã dùng hết 5/5 feature** (FR-07…FR-11) — người thứ 6 (nếu có) buộc phải dùng lại một FR của Pool B với endpoint khác.

**Dự phòng (chưa ai lấy):** FR-06 `GET /api/products/:id` tách riêng khỏi TV3 (Pool A) · FR-14 categories CRUD, FR-12/FR-13 access control & dashboard (Pool C).

---

## Vì sao chia như vậy — mạch bug của từng người

Đề chấm theo **4 trục bắt buộc**: domain partition · state transition · security (SEC-01→07) · schema validation. Mỗi bộ 3 dưới đây đủ cả 4 trục.

### Thành viên 2 — "trục coupon + khôi phục mật khẩu"
- **A · forgot/reset password** (`server.js:68-111`): `resetToken` **trả thẳng trong response** (lộ OTP); token chỉ **4 chữ số**, không hạn dùng, không giới hạn số lần thử → brute-force; email không tồn tại trả `404 "User not found"` → **user enumeration**; reset xong **không** clear `login_attempts` / `locked_until`; `newPassword` không kiểm độ mạnh, lưu plaintext. State machine 2 bước: *chưa có token → có token → token đã dùng/không hợp lệ*.
- **B · apply-coupon** (`server.js:363-443`): **không có `authenticateToken`**, `user_id` lấy từ **body** → bỏ trường `user_id` là **né được giới hạn `max_uses_per_user`**; công thức percent sai `total*(1-discount_value)` → giảm giá **âm**, `final_amount` phình to; điều kiện `total_amount > min_order_amount` sai biên (đúng phải `>=`); check hết hạn nằm **bên trong** nhánh đủ min → mã hết hạn mà đơn nhỏ thì báo sai lỗi.
- **C · admin coupons** (`server.js:457-493`): chỉ `authenticateToken`, **không kiểm role admin** → user thường tạo/xoá được mã; không validate `type`, `discount_value` âm, `expired_at` quá khứ; lỗi DB trả nguyên `err.message`.

### Thành viên 3 — "trục sản phẩm + huỷ đơn"
- **A · product search** (`server.js:141-166`): **SQL Injection thật** — chuỗi nối `LIKE '%${searchQuery}%'` (SEC-05); lỗi DB trả về **HTML** kèm thông điệp nội bộ; `GET /api/products/:id` với id không tồn tại trả **`200 {}`** thay vì `404`, và **id chẵn thì `price` bị ép thành string** → miếng ngon cho *schema validation*.
- **B · order cancel** (`server.js:321-343`): cho huỷ đơn đang **`shipping`** (FR-10 cấm — trong code còn có comment thừa nhận), `delivered`/`canceled` chặn đúng → ma trận chuyển trạng thái 5 ô rõ ràng; đơn người khác trả `404` (chỗ này **đúng**, phải viết expected là "bị từ chối").
- **C · product CRUD** (`server.js:167-198`): `POST` / `PUT` / `DELETE /api/products` **hoàn toàn không có auth** → khách vãng lai xoá sạch sản phẩm (broken access control, Critical); `price` âm/0/string vẫn nhận; xoá id không tồn tại vẫn `200`.

### Thành viên 4 — "trục người dùng + giỏ hàng"
- **A · profile update** (`server.js:118-140`): body có `role` là **update thẳng cột role** → **privilege escalation**, user tự nâng mình thành admin (SEC-03); thiếu field thì ghi đè `NULL`; `phone` không validate; `GET /api/users/me` `SELECT *` → **trả cả `password`, `reset_token`** (SEC-01).
- **B · cart** (`server.js:284-296`): `userCarts[userId].push(req.body)` — **push nguyên body**, không kiểm sản phẩm tồn tại, `quantity` âm/0/chuỗi, **`price` do client tự khai** (giá 100.000 khai thành 1), thêm 2 lần không gộp dòng; giỏ nằm **trong RAM** → mất khi restart.
- **C · admin users** (`server.js:494-509`): cả hai endpoint **chỉ có `authenticateToken`, không kiểm role** → user thường xem được **toàn bộ danh sách user** (kèm `login_attempts`, `locked_until`) và **xoá được cả tài khoản admin**; xoá không cascade `orders` → đơn mồ côi; xoá id không tồn tại vẫn `200`.

### Thành viên 5 — "trục vòng đời dữ liệu: tạo user → xem đơn → nạp hàng loạt"
- **A · register** (`server.js:20-29`): **không validate gì cả** so với FR-01 — email sai định dạng, mật khẩu yếu (FR-01 đòi ≥8 ký tự, có hoa/thường/số/ký tự đặc biệt), **thiếu hẳn trường xác nhận mật khẩu**, thiếu field thì tạo user với cột `NULL`; email trùng → **`500` kèm nguyên `err.message`** (`UNIQUE constraint failed: users.email`) ⇒ lộ schema DB **và** cho phép user enumeration; mật khẩu lưu **plaintext** (SEC-01); `id` trả về tăng tuần tự → đếm được số user. Lưu ý audit: `role` **không** lấy từ body, nên case "đăng ký kèm `role: admin`" phải có expected là **"role vẫn là user"** — AI hay viết ngược.
- **B · order history** (`server.js:311-319`): FR-11 nói "chỉ xem được đơn của chính mình"; code lọc `user_id` từ token là **đúng**, nên trục security phải đánh chỗ khác: JWT ký bằng **secret hard-code** (`server.js:9`, không `expiresIn`) → **tự ký token với `id` bất kỳ là đọc được lịch sử đơn người khác**; `SELECT *` trả nguyên `shipping_address` chưa escape (payload XSS nhét vào lúc checkout vẫn nằm đó); `err` bị bỏ qua ⇒ lỗi DB thành `200` body rỗng thay vì `500`; không phân trang, không giới hạn; đơn **mồ côi** sau khi admin xoá user vẫn tồn tại. Schema: `total_amount` INTEGER, `status` thuộc enum 5 giá trị, `created_at` dạng `YYYY-MM-DD HH:MM:SS`.
- **C · import products** (`server.js:199-241`): chỉ `authenticateToken`, **không kiểm role admin** → user thường import hàng loạt (FR-12); **race condition thật** — `stmt.finalize()` trả response trước khi các callback của `stmt.run` chạy xong ⇒ `inserted` đếm thiếu và mảng `errors` rỗng dù có dòng lỗi; `row.price` không validate (âm / chuỗi / `null` vẫn vào DB); `row.category_id || 1` ⇒ `category_id: 0` bị **âm thầm đổi thành 1**, FK không tồn tại vẫn nhận; chỉ chặn `!row.name` nên `name: "   "` vẫn qua; mảng rỗng / không phải mảng trả `400` (chỗ này **đúng**). Partition rất đẹp: partial success (5 dòng = 3 hợp lệ + 2 lỗi).

> ⚠️ **Điểm chồng lấn duy nhất, cần thống nhất trước:** endpoint kề `GET /api/orders/:id` (`server.js:344`) **không có auth → IDOR**. TV1 đã dùng nó làm *extend case* của checkout, TV5 cũng dễ chạm vào khi test FR-11. Đề chỉ cấm trùng **bộ 3 API chính** nên không phạm quy, nhưng hai bạn nên thống nhất: hoặc chỉ TV1 mở Issue cho bug này, hoặc TV5 mở Issue trên repo mình và ghi rõ API chính vẫn là `my-orders`.

---

## Lưu ý chung cho cả 5 người

1. **DB reset mỗi lần khởi động** (`database.js:117` gọi `initDatabase()` với `DROP TABLE`). Test **phải tự dựng tiền đề** (tự đăng ký user, tự tạo đơn), không hard-code ID.
2. Tài khoản seed: admin `admin@eshop.com` / `Admin123!`, user `test@eshop.com` / `Test1234!`; 3 category, 5 product (id 1–5), 4 coupon.
3. Mỗi request phải gắn header `X-Student-Id: {MSSV của chính mình}` (pre-request script) — TA đối chiếu screenshot Console.
4. Bug **có sẵn trong SUT là bug thật** → mở GitHub Issue trên repo của **chính mình**, kèm screenshot; không dùng chung issue với bạn khác.
5. Case AI hay sinh sai expected: SQLi ở `/api/login` **không** có lỗ hổng (parameterized) — expected đúng là "bị từ chối, 401"; huỷ đơn của người khác trả `404` là **đúng**; đăng ký kèm `role: admin` **không** nâng quyền. Nếu AI viết expected là "thành công" ⇒ audit gán **INVALID**.
