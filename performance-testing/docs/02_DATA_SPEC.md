# 02 — DATA SPEC (Seed data + CSV)

> Đáp ứng đề §6 Task 1: *"Make the workflow data-driven. Use CSV input data in the end-to-end workflow to parameterize requests."*

---

## 1. Vì sao phải seed thêm dữ liệu

Seed gốc (`backend/database.js:90-103`) chỉ có:

| Bảng | Số bản ghi seed gốc | Vấn đề khi test hiệu năng |
| :--- | :---: | :--- |
| `users` | **2** (`admin@eshop.com`, `test@eshop.com`) | Chạy 300 thread trên 1 account → mọi thread tranh nhau cùng một hàng `users`, và chỉ cần vài lần sai là **khóa toàn bộ test** |
| `products` | **5** | `GET /api/products` trả về ~1 KB → **không đo được gì**. Điểm nhấn của workflow Browse-to-buy là chi phí đọc toàn bộ catalog, mà 5 sản phẩm thì chi phí ≈ 0 |

Vì vậy phải seed:
- **400 user** với tiền tố `khoa` (đủ cho thread cao nhất là 310 ở Spike)
- **+500 product** (giữ nguyên 5 sản phẩm gốc)

> ⚠️ **Bắt buộc khai báo trong báo cáo.** Việc seed thêm 500 sản phẩm làm số đo của bài này **không so trực tiếp được** với thành viên chạy trên DB gốc. Ghi rõ điều kiện dữ liệu trong `deliverables/01_test-design.md` §Test data và trong main report.

---

## 2. `scripts/seed_perf_data.js`

### 2.1 Yêu cầu

| Mục | Giá trị |
| :--- | :--- |
| Ngôn ngữ | Node.js (CommonJS, khớp phong cách `backend/database.js`) |
| Dependency | `sqlite3` — **đã có sẵn** trong `backend/node_modules`, `require` bằng đường dẫn tương đối |
| DB đích | `backend/database.sqlite` (dùng `path.resolve(__dirname, '../../backend/database.sqlite')`) |
| Idempotent | Chạy nhiều lần không nhân đôi dữ liệu — xóa dữ liệu perf cũ trước khi insert |
| Output phụ | Ghi luôn `performance-testing/data/khoa_users.csv` |

### 2.2 Dữ liệu user

| Trường | Quy tắc |
| :--- | :--- |
| `name` | `Khoa Perf User 001` … `Khoa Perf User 400` |
| `email` | `khoa001@eshop.com` … `khoa400@eshop.com` (số 3 chữ số, pad `0`) |
| `password` | `Test1234!` — **plaintext**, vì SUT lưu plaintext (`server.js:46` so sánh trực tiếp `user.password === password`) |
| `role` | `user` |
| `login_attempts` | `0` |
| `locked_until` | `NULL` |
| `shipping_address` | `<số> <tên đường>, Q<1-12>, TP.HCM` — sinh xoay vòng |
| `phone` | `09` + 8 chữ số |

SQL dọn dẹp trước khi insert:
```sql
DELETE FROM users WHERE email LIKE 'khoa%@eshop.com';
```

### 2.3 Dữ liệu product

| Trường | Quy tắc |
| :--- | :--- |
| Số lượng | **500** bản ghi mới |
| `name` | `PERF <Dòng sản phẩm> <số thứ tự>` — ví dụ `PERF Laptop Gaming 042`. Tiền tố `PERF ` giúp phân biệt và xóa lại được |
| `price` | Số nguyên ngẫu nhiên trong `[100000, 50000000]`, làm tròn tới nghìn |
| `description` | Chuỗi ~120–200 ký tự (để payload full-list đủ nặng, giống dữ liệu thật) |
| `imageUrl` | `https://placehold.co/300x300/png?text=PERF+<n>` |
| `category_id` | Xoay vòng `1, 2, 3` (khớp 3 category seed gốc) |

SQL dọn dẹp trước khi insert:
```sql
DELETE FROM products WHERE name LIKE 'PERF %';
```

> **Giữ nguyên 5 sản phẩm gốc** (id 1–5). CSV của Trâm và Nguyên tham chiếu `product_id` 1 và 2; xóa chúng sẽ làm hỏng bài của thành viên khác nếu dùng chung DB.

### 2.4 Hiệu năng insert

Bọc trong transaction, nếu không 900 lần `INSERT` riêng lẻ sẽ rất chậm và dễ `SQLITE_BUSY`:

```js
db.serialize(() => {
  db.run('BEGIN TRANSACTION');
  // ... prepare + run vòng lặp ...
  db.run('COMMIT');
});
```

### 2.5 Output console kỳ vọng

```
[seed] Removed 0 old perf users, 0 old perf products
[seed] Inserted 400 users (khoa001..khoa400)
[seed] Inserted 500 products (PERF ...)
[seed] Wrote performance-testing/data/khoa_users.csv (400 rows + header)
[seed] Done.
```

### 2.6 Verify

```powershell
$db = "C:\My Workspace\HCMUS\Test\Week 3\Hw2\backend\database.sqlite"
node -e "const s=require('C:/My Workspace/HCMUS/Test/Week 3/Hw2/backend/node_modules/sqlite3');const d=new s.Database('$($db -replace '\\','/')');d.get(`"SELECT (SELECT COUNT(*) FROM users WHERE email LIKE 'khoa%') u,(SELECT COUNT(*) FROM products) p`",(e,r)=>console.log(r));"
```
Kỳ vọng: `{ u: 400, p: 505 }`

---

## 3. `data/khoa_users.csv`

### 3.1 Schema — đúng theo quy ước nhóm cho workflow Browse-to-buy

```
email,password,product_id,quantity,price,total_amount,shipping_address
```

| Cột | Dùng ở bước | Ghi chú |
| :--- | :--- | :--- |
| `email` | 1 — login | `khoa001@eshop.com` … `khoa400@eshop.com` |
| `password` | 1 — login | luôn `Test1234!` |
| `product_id` | 3 — detail (fallback) | **Fallback** khi JSON Extractor ở bước 2 không lấy được id. Xem `04_JMX_BUILD_SPEC.md` §5 |
| `quantity` | 4 — cart | `1`–`3` |
| `price` | 4 — cart | Đơn giá, khớp `product_id` tương ứng trong DB |
| `total_amount` | 5 — checkout | `price × quantity` |
| `shipping_address` | 5 — checkout | Có dấu phẩy → **bắt buộc bọc dấu nháy kép** |

### 3.2 Ví dụ (3 dòng đầu)

```csv
email,password,product_id,quantity,price,total_amount,shipping_address
khoa001@eshop.com,Test1234!,7,1,15420000,15420000,"12 Nguyen Van Cu, Q5, TP.HCM"
khoa002@eshop.com,Test1234!,143,2,3180000,6360000,"88 Cach Mang Thang 8, Q3, TP.HCM"
khoa003@eshop.com,Test1234!,266,1,27900000,27900000,"5 Ly Thuong Kiet, Q10, TP.HCM"
```

### 3.3 Ràng buộc bắt buộc

1. **400 dòng dữ liệu + 1 dòng header**, không dòng trống cuối file (JMeter đọc dòng trống thành record rỗng).
2. Encoding **UTF-8 không BOM**. BOM sẽ dính vào cột đầu tiên làm email bước 1 sai → 401 hàng loạt.
   ```js
   fs.writeFileSync(csvPath, content, { encoding: 'utf8' }); // Node mặc định không BOM
   ```
3. `shipping_address` chứa dấu phẩy → phải bọc `"` (RFC 4180). Trong JMeter đặt `Allow quoted data = true`.
4. Mọi `product_id` phải **tồn tại thật** trong `products`. Sinh bằng cách query lại DB sau khi insert, không hard-code.
5. `price` phải khớp `products.price` của `product_id` đó — nếu lệch thì dữ liệu đơn hàng vô nghĩa (dù backend không kiểm, xem `server.js:297`).

### 3.4 Vì sao gộp 1 file thay vì nhiều file

Đề cho phép *"one or more CSV files"*. Gộp một file vì mọi tham số đều gắn với **một virtual user cụ thể** — tách file sẽ khiến JMeter ghép chéo user A với địa chỉ của user B, tạo dữ liệu vô nghĩa.

> Nếu muốn thể hiện kỹ thuật multi-CSV, phương án thay thế: tách `khoa_credentials.csv` (`email,password`) và `khoa_orders.csv` (`product_id,quantity,price,total_amount,shipping_address`), dùng 2 `CSV Data Set Config`. **Phải ghi rõ trong report rằng việc ghép là ngẫu nhiên và chấp nhận được vì backend không ràng buộc chéo.**

---

## 4. `scripts/reset_lockout.js`

### 4.1 Vì sao cần

`backend/server.js:54,57`:
```js
const newAttempts = user.login_attempts + 2;      // spec FR-02 nói +1
if (newAttempts >= 3) {
  lockedUntil = new Date(Date.now() + 180000).toISOString();   // spec nói 30s
}
```

→ **2 lần login sai liên tiếp là khóa 3 phút.** Ở Stress/Spike với 200–300 thread, chỉ cần vài request lỗi là account dính khóa và mọi số đo sau đó vô nghĩa.

Đề §6 yêu cầu tường minh: *"When Stress/Spike runs trigger the 3-fail login lockout, reset it between runs and document the steps."*

### 4.2 Yêu cầu script

```sql
UPDATE users SET login_attempts = 0, locked_until = NULL;
```

Output console:
```
[reset-lockout] Cleared lockout on <N> users at <ISO timestamp>
```

In cả **timestamp** để dán vào `deliverables/04_execution-report.md` làm bằng chứng thời điểm reset.

### 4.3 Verify

```powershell
node "C:\My Workspace\HCMUS\Test\Week 3\Hw2\performance-testing\scripts\reset_lockout.js"
```
Chạy xong, `SELECT COUNT(*) FROM users WHERE locked_until IS NOT NULL` phải = `0`.

### 4.4 Ba cách reset — ghi cả ba vào báo cáo

| Cách | Lệnh / thao tác | Khi nào dùng |
| :--- | :--- | :--- |
| **A. Script (khuyến nghị)** | `node performance-testing\scripts\reset_lockout.js` | Mặc định, giữa mỗi run |
| **B. Chờ hết hạn** | Đợi ≥ 180 giây | Khi muốn chứng minh cơ chế tự mở khóa hoạt động |
| **C. Reset toàn bộ DB** | `node backend\database.js` rồi seed lại | Khi dữ liệu `orders` phình quá to giữa các run |

> Đề chấm cả **"document the steps"** — nên `04_execution-report.md` phải có ảnh chụp terminal lúc chạy reset, kèm timestamp khớp với thời gian bắt đầu run kế tiếp.

---

## 5. Thứ tự chạy — sai thứ tự là mất dữ liệu

```powershell
$root = "C:\My Workspace\HCMUS\Test\Week 3\Hw2"

# 1) Reset DB về seed gốc  (DROP mọi bảng — làm TRƯỚC)
node "$root\backend\database.js"

# 2) Seed dữ liệu perf     (thêm 400 user + 500 product, sinh CSV)
node "$root\performance-testing\scripts\seed_perf_data.js"

# 3) Khởi động server
node "$root\backend\server.js"
```

> ⚠️ Chạy `backend\database.js` **sau** `seed_perf_data.js` sẽ **xóa sạch** 400 user và 500 product vừa tạo.

---

## 6. Ảnh hưởng của dữ liệu tới kết quả — ghi vào report

| Quan sát dự kiến | Cơ chế |
| :--- | :--- |
| `GET /api/products` chậm hơn hẳn `GET /api/products/{id}` | Full list serialize 505 bản ghi; detail chỉ 1 (`server.js:153` vs `:160`) |
| Latency `GET /api/products` gần như phẳng theo số thread cho tới điểm bão hòa CPU | Node.js đơn luồng — request xếp hàng ở event loop, không phải ở DB |
| RSS của process `node` **tăng đơn điệu**, không giảm sau checkout | `userCarts` (`server.js:14`) chỉ `push` (`:293`), checkout không xóa giỏ (`:297-309`) → memory leak thật, là cơ sở cho "memory ceiling" ở `05_endurance-threshold.md` |
| `SQLITE_BUSY` xuất hiện ở bậc thread cao của Stress | `/api/checkout` `INSERT` đồng thời vào SQLite không bật WAL (`server.js:301`) |

Bốn quan sát này là **giả thuyết**, phải được xác nhận hoặc bác bỏ bằng số liệu thật trong `deliverables/05_endurance-threshold.md`. Không ghi thành kết luận trước khi chạy.

---

## 7. Checklist

- [ ] `scripts/seed_perf_data.js` chạy sạch, output đúng §2.5
- [ ] `SELECT COUNT(*) FROM users WHERE email LIKE 'khoa%'` = 400
- [ ] `SELECT COUNT(*) FROM products` = 505
- [ ] `data/khoa_users.csv` có 401 dòng, UTF-8 không BOM, `shipping_address` được bọc `"`
- [ ] Mọi `product_id` trong CSV tồn tại trong DB, `price` khớp
- [ ] `scripts/reset_lockout.js` chạy được, in timestamp
- [ ] Đã ghi "điều kiện dữ liệu +500 product" vào ghi chú cho `deliverables/01_test-design.md`
- [ ] Commit: `feat(perf): add seed data script and CSV dataset for browse-to-buy`
