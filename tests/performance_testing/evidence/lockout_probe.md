# Lockout probe & reset procedure — 23127438

Thời điểm: 2026-08-15 14:03:24

## 1. Probe: cố tình login sai trên user hy sinh nguyen_probe@eshop.com

```
$ login sai lần 1 (attempts 0→2):
{"error":"Invalid email or password"}
$ login sai lần 2 (attempts 2→4 ≥ 3 → locked_until = now + 180s):
{"error":"Invalid email or password"}
$ login ĐÚNG mật khẩu nhưng đã bị khóa → 403:
{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."} [HTTP 403]
$ trạng thái DB:
nguyen_probe@eshop.com|4|2026-08-15T07:06:24.474Z
```

**Quan sát:** chỉ cần **2 lần sai** là khóa (mỗi lần sai +2 attempts, ngưỡng ≥3), khóa **180 giây** — khác spec FR-02 (3 lần sai, khóa ~30s).

## 2. Reset lockout (dùng giữa các run Stress/Spike)

Cách A — SQL reset (dùng trong bài, không mất data):
```
$ sqlite3 database.sqlite "UPDATE users SET login_attempts=0, locked_until=NULL WHERE locked_until IS NOT NULL;"
$ login lại sau reset → 200:
{"message":"Login successful","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJp ..."
```

Cách B — đợi hết 180s `locked_until` (chậm).
Cách C — restart server: **KHÔNG dùng** vì `database.js` DROP toàn bộ bảng và reseed → mất 60 user pool + toàn bộ orders.

## 3. Nhật ký reset trong bộ chạy nộp bài (2026-08-15)

- Reset SQL (Cách A) được chạy **tự động trước mỗi run** và **thủ công giữa Stress (19:19–19:26) → Spike (19:28–19:33)** lúc 19:28:02.
- Toàn bộ trình tự probe → 403 → xem DB → reset → verify 0 user khóa → login lại 200 được chụp trong `screenshots/lockout_reset_steps.png`.
- Sau Spike, chạy reset lần cuối; xác nhận `SELECT COUNT(*) FROM users WHERE locked_until IS NOT NULL` = 0.
