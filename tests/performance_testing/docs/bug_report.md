# Bug / Issue findings

- Họ và tên: Đặng Trường Nguyên
- MSSV: 23127438

## BUG-1 — Account lockout sai spec (severity: Medium, functional)

- **GitHub Issue:** [#402](https://github.com/trngnneee/eshop-sut/issues/402)
- **Spec FR-02:** sai ≥ 3 lần → khóa ~30 giây.
- __Thực tế (`server.js` dòng 54–57):__ mỗi lần sai `login_attempts += 2`, ngưỡng khóa `>= 3`, thời gian khóa `Date.now() + 180000` = __180 giây__.
- **Hệ quả:** chỉ cần **2 lần** nhập sai đã bị khóa (không phải 3), và khóa gấp 6 lần spec.
- __Evidence:__ `evidence/lockout_probe.md` (curl 2 lần sai → lần login đúng nhận HTTP 403).

## BUG-2 — Search endpoint dính SQL Injection (severity: High, security)

- **GitHub Issue:** [#403](https://github.com/trngnneee/eshop-sut/issues/403)
- **`server.js` dòng 144:** `SELECT * FROM products WHERE name LIKE '%${searchQuery}%'` — nối chuỗi trực tiếp query string vào SQL.
- **PoC an toàn:** `GET /api/products?search='` trả về `<h1>Database Error</h1>` lộ lỗi SQL; payload `%' OR '1'='1` trả toàn bộ bảng products.
- **Hệ quả:** rò rỉ dữ liệu, có thể khai thác sâu hơn. (Trong perf test tôi chỉ dùng keyword sạch để tránh nhiễu số liệu.)

## BUG-3 — `GET /api/products/:id` trả HTTP 200 cho id không tồn tại (severity: Low, correctness)

- **GitHub Issue:** [#404](https://github.com/trngnneee/eshop-sut/issues/404)
- **`server.js` dòng 161:** `if (!row) return res.status(200).json({});` — không tồn tại vẫn trả 200 với body rỗng thay vì 404.
- **Hệ quả:** client/monitor khó phát hiện lỗi; assertion chỉ dựa status code sẽ bỏ sót.

## BUG-4 — `GET /api/products/:id` trả `price` khác kiểu dữ liệu (severity: Low, correctness)

- **GitHub Issue:** [#405](https://github.com/trngnneee/eshop-sut/issues/405)
- **`server.js` dòng 162:** `if (row.id % 2 === 0) row.price = row.price.toString();` — sản phẩm id chẵn trả `price` dạng **string**, id lẻ dạng **number**.
- **Hệ quả:** client parse giá không nhất quán; dễ gây bug tính tiền.

## BUG-5 — Cart lưu in-memory, không phân tách và mất khi restart (severity: Medium, reliability)

- **GitHub Issue:** [#406](https://github.com/trngnneee/eshop-sut/issues/406)
- **`server.js` dòng 14, 290–295:** `userCarts` là object trong RAM, `push` nguyên `req.body` không validate.
- __Hệ quả:__ (a) restart server mất toàn bộ giỏ; (b) nhiều VU dùng chung user_id sẽ trộn giỏ; (c) rò rỉ bộ nhớ khi user tăng (không bao giờ giải phóng) — liên quan trực tiếp tới quan sát RAM trong soak test.

## BUG-6 — `database.js` DROP + reseed toàn bộ DB mỗi lần khởi động (severity: Medium, ops)

- **GitHub Issue:** [#407](https://github.com/trngnneee/eshop-sut/issues/407)
- **`database.js` dòng 15–20 + gọi `initDatabase()` ở cuối:** mỗi lần require/khởi động server → xóa sạch dữ liệu.
- **Hệ quả:** không thể restart để reset lockout mà không mất user pool + orders; nguy hiểm nếu vô tình chạy ở môi trường có dữ liệu thật.
