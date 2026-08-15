# Thiết kế test — Category-guided buy

- Họ và tên: Đặng Trường Nguyên
- MSSV: 23127438

## 1. Workflow và mapping 3 nhóm endpoint

Mỗi virtual user (VU) trong 1 iteration thực hiện đúng hành trình người mua "được dẫn hướng bởi danh mục":

| # | Request | Nhóm endpoint | Vai trò trong hành trình |
|---|---------|---------------|--------------------------|
| 1 | `POST /api/login` | **Auth-heavy** | Đăng nhập, lấy JWT `token`. Chịu ảnh hưởng account lockout (sai 2 lần → khóa 180s theo implementation thật) |
| 2 | `GET /api/categories` | **Read-heavy** | Người dùng mở trang danh mục (Điện thoại / Laptop / Phụ kiện) |
| 3 | `GET /api/products?search={q}` | **Read-heavy** | Tìm sản phẩm theo keyword gắn với category vừa xem. Backend chạy SQL `LIKE '%q%'` full-scan — điểm nóng hiệu năng |
| 4 | `POST /api/cart` (+ Bearer) | **Transactional** | Thêm giỏ — ghi vào in-memory store `userCarts` |
| 5 | `POST /api/checkout` (+ Bearer) | **Transactional** | Tạo đơn — `INSERT INTO orders` (SQLite, ghi đĩa) |

**Đủ 3 nhóm theo yêu cầu đề:** auth-heavy (bước 1), read-heavy (bước 2–3), transactional (bước 4–5). Cả 3 kịch bản Load/Stress/Spike dùng **cùng workflow này**, chỉ đổi tham số tải.

## 2. Data-driven

- `nguyen_users.csv` — 60 dòng, 10 cột: `email,password,category_hint,search,product_id,product_name,quantity,price,total_amount,shipping_address`.
- 60 user riêng (`nguyen01..nguyen60@eshop.com`) đăng ký qua `POST /api/register` — không dùng chung `test@eshop.com` với thành viên khác.
- CSV Data Set Config: `shareMode.all`, `recycle=true` → 200 VU của Stress vẫn luân phiên qua 60 bộ dữ liệu.
- Keyword search lấy từ tên sản phẩm thật trong seed: `iPhone`, `Samsung`, `MacBook`, `Tai nghe`, `Keychron` (xem AI Audit Report — Finding #1 trong `docs/ai_declaration/[AI-02] ... AI Audit Report_En.md` — vì sao __không__ dùng keyword `Laptop` như README nhóm gợi ý).

## 3. Tham số từng kịch bản và lý do

| Kịch bản | Cấu hình VU | Ramp-up | Thời lượng | Think-time | Lý do chọn |
|---|---|---|---|---|---|
| **Load** | 20 VU cố định | 60s | 5 phút | login/categories 1–2s, search 1–3s, cart/checkout 1s (theo quy ước nhóm) | Tải "ngày thường": mục tiêu lấy baseline p90/p95 khi hệ chưa nghẽn. 20 VU × ~5 req/8–10s ≈ 10–12 RPS — vừa sức 1 process Node + SQLite |
| **Stress** | Bậc thang 50 → 100 → 200 VU (3 thread group, delay 0/120/240s) | 60s mỗi bậc | 7 phút | đồng loạt 0.5–1s (dồn tải) | Tăng từng bậc để **định vị breaking point**: so sánh p95/error-rate giữa 3 mức tải trên cùng 1 run. 200 VU là ~10× Load |
| **Spike** | Nền 10 VU suốt 5 phút + **+150 VU bùng nổ tại t=90s trong 60s** (ramp 10s) | 10s | 5 phút | 0.3–0.7s | Mô phỏng flash-sale: hệ đang chạy êm thì tải tăng ~16× trong 10 giây. Quan sát: độ trễ đỉnh, error burst, và **thời gian hồi phục** sau khi spike rút |
| **Soak** | 30 VU giữ nguyên | 60s | 12 phút | như Load | Endurance: tìm RPS ổn định dài hạn + RAM ceiling của node process (bảng `orders` phình dần, cart in-memory không bao giờ giải phóng) |

## 4. Assertions (mỗi request đều có)

| Request | Assertions |
|---|---|
| Login | HTTP 200 (equals) + JSONPath `$.token` tồn tại |
| Categories | HTTP 200 + JSONPath `$[0].name` (array không rỗng) |
| Search | HTTP 200 + JSONPath `$[0].id` (có kết quả — keyword đảm bảo match seed) |
| Cart | HTTP 200 + body chứa `Added to cart` |
| Checkout | HTTP 200 + JSONPath `$.orderId` tồn tại (extract `orderId` để đối chiếu) |

## 5. Ba report view khác nhau (yêu cầu đề)

| Plan | Listener |
|---|---|
| `23127438_Load_20260815` | __Summary Report__ |
| `23127438_Stress_20260815` | __Aggregate Report__ |
| `23127438_Spike_20260815` | __View Results Tree__ |
| `23127438_Soak_20260815` (bổ sung) | Graph Results |

Mọi run đều xuất thêm raw `.jtl` (qua `-l`) và HTML dashboard (qua `-e -o`).

## 6. Xử lý account lockout

- Cả 4 plan chỉ login **đúng** mật khẩu → không tự gây lockout.
- Hành vi lockout được xác nhận bằng probe riêng trên user hy sinh (`evidence/lockout_probe.md`): sai 2 lần → khóa 180s (impl `+2 attempts/lần`, ngưỡng ≥3) — __khác spec FR-02__.
- Quy trình reset giữa các run: SQL `UPDATE users SET login_attempts=0, locked_until=NULL` — __không restart server__ vì `database.js` DROP + reseed toàn bộ DB khi khởi động (mất user pool và orders).
- Trong bộ chạy nộp bài (2026-08-15): reset được chạy **trước mỗi run** và chụp bằng chứng đầy đủ trình tự probe → 403 → reset → verify → login 200 giữa Stress→Spike lúc 19:28 (`screenshots/lockout_reset_steps.png`).

## 7. Cách chạy

```bash
cd tests/performance_testing
./scripts/monitor.sh results/load/resource_load.csv 340 &   # log CPU/RAM node mỗi 5s, chạy nền
jmeter -n -t testplans/23127438_Load_20260815.jmx \
  -l results/load/23127438_Load_20260815.jtl \
  -e -o results/load/html_report
python3 scripts/analyze_jtl.py results/load/23127438_Load_20260815.jtl  # percentile ground-truth
```

(Tương tự cho stress/spike/soak với duration monitor 460/340/760s; reset lockout trước mỗi run.)

## 8. Kết quả thực thi

Bộ kết quả nộp bài chạy **2026-08-15, 19:13–19:48 ICT**, cả 4 kịch bản **0% lỗi** — số liệu chi tiết: `docs/results_summary.md`; actual result từng testcase: `testcases/PERF-*.md`; ảnh bằng chứng (JMeter + htop tại đỉnh tải, hardware, lockout reset, HTML dashboard): `screenshots/`.
