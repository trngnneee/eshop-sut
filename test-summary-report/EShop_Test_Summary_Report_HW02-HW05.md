# TEST SUMMARY REPORT — HỆ THỐNG ESHOP

**Tổng hợp chương trình kiểm thử HW02 → HW05 (nhóm 2 thành viên)**

---

## THÔNG TIN TÀI LIỆU (Document Control)

| Mục | Nội dung |
|---|---|
| **Tên dự án** | EShop — Phiên bản dành cho Kiểm thử Phần mềm |
| **Hệ thống được kiểm thử (SUT)** | EShop (Backend API + Frontend Web + Web Admin + Mobile App) |
| **Repository** | https://github.com/trngnneee/eshop-sut |
| **Học phần** | Kiểm thử Phần mềm (Software Testing) — CS423 / CSC13003, FIT@HCMUS |
| **Thành viên 1** | Đặng Đăng Khoa — MSSV **23127207** |
| **Thành viên 2** | Đặng Trường Nguyên — MSSV **23127438** |
| **Phạm vi báo cáo** | 4 bài tập lớn: HW02 (Domain & BVA), HW03 (GUI / Usability / Cross-platform), HW04 (Automation), HW05 (Performance) |
| **Ngày phát hành** | 2026-08-17 |
| **Phiên bản** | 1.0 |
| **Trạng thái** | Final — tổng hợp từ các báo cáo gốc đã nộp |
| **Branch chứa tài liệu này** | `test-summary-report-Khoa` |

### Branch nguồn dữ liệu

| Bài tập | Thành viên 23127207 (Khoa) | Thành viên 23127438 (Nguyên) |
|---|---|---|
| HW02 | `HW2-Khoa` | `HW2-Nguyen` |
| HW03 | `HW3-Khoa` | `HW3-Nguyen` |
| HW04 | `HW4-Khoa` | `HW04-Nguyen` |
| HW05 | `HW5` | `feat/HW05-Nguyen` |

> **Nguyên tắc biên soạn:** mọi con số trong tài liệu này đều được trích trực tiếp từ báo cáo gốc trên
> các branch nêu trên. Tài liệu **không tính lại, không ước lượng và không hòa giải** các số liệu mâu
> thuẫn giữa các nguồn — mọi mâu thuẫn đều được nêu công khai tại mục 4.5.

---

## 1. MỤC ĐÍCH TÀI LIỆU (Purpose of the Document)

Tài liệu này tổng kết toàn bộ hoạt động kiểm thử đã thực hiện trên hệ thống EShop trong 4 bài tập lớn
HW02 → HW05 của hai thành viên, gộp thành một bản duy nhất nhằm:

1. **Cung cấp bức tranh tổng thể**: 8 branch riêng lẻ với 8 định dạng báo cáo khác nhau được quy về một
   khung báo cáo chuẩn duy nhất, giúp người đọc (giảng viên, thành viên nhóm, người tiếp nhận bàn giao)
   nắm được toàn bộ phạm vi, số liệu và kết luận mà không phải mở lần lượt từng branch.
2. **Đánh giá mức độ sẵn sàng của SUT**: tập hợp toàn bộ defect đã phát hiện, phân bố theo module và
   mức độ nghiêm trọng, để đưa ra kết luận Go / No-Go có căn cứ.
3. **Ghi nhận độ phủ và các khoảng trống**: nêu rõ những gì đã kiểm thử, những gì cố ý loại khỏi phạm vi,
   và những gì **chưa** kiểm thử được — kèm lý do.
4. **Rút bài học cho các đợt kiểm thử sau**: đặc biệt là các bài học về giới hạn của AI khi hỗ trợ thiết
   kế và phân tích kết quả kiểm thử.

**Đối tượng đọc:** giảng viên chấm bài, thành viên nhóm, và bất kỳ ai cần tiếp nhận lại công việc kiểm
thử trên hệ thống EShop.

---

## 2. TỔNG QUAN ỨNG DỤNG (Application Overview)

EShop là một nền tảng thương mại điện tử được xây dựng **có chủ đích cài lỗi** để phục vụ mục đích học
kiểm thử. Sinh viên dùng tài liệu đặc tả (`README.md` ở gốc repo) làm cơ sở thiết kế test case, sau đó
kiểm thử hệ thống thực để tìm các điểm triển khai không tuân thủ đặc tả.

### 2.1 Kiến trúc — 4 thành phần

| Thành phần | Công nghệ | URL mặc định | Vai trò |
|---|---|---|---|
| **Backend API** | Node.js + Express + SQLite | `http://localhost:3000` | Toàn bộ nghiệp vụ: xác thực, sản phẩm, giỏ hàng, coupon, đơn hàng, quản trị |
| **Frontend Web** | React + Vite + Tailwind CSS | `http://localhost:5173` | Giao diện khách hàng: đăng ký/đăng nhập, duyệt sản phẩm, giỏ hàng, thanh toán, hồ sơ |
| **Web Admin** | React + Vite + Tailwind CSS | `http://localhost:5174` | Giao diện quản trị: dashboard, danh mục, sản phẩm, đơn hàng, người dùng |
| **Mobile App** | React Native + Expo | IP LAN của máy chủ | Ứng dụng di động: danh sách sản phẩm, giỏ hàng, thanh toán, lịch sử đơn |

### 2.2 Module nghiệp vụ chính

- **Quản lý tài khoản**: đăng ký (FR-01), đăng nhập & khóa tài khoản (FR-02), quên mật khẩu 2 bước (FR-03),
  quản lý hồ sơ (FR-04).
- **Mua hàng**: danh sách & tìm kiếm sản phẩm (FR-20), giỏ hàng (FR-07), mã giảm giá (FR-09),
  thanh toán & vòng đời đơn hàng (FR-10), giỏ hàng & thanh toán trên mobile (FR-21).
- **Quản trị**: đăng nhập admin (FR-12), dashboard doanh thu (FR-13), quản lý danh mục (FR-14),
  quản lý đơn hàng (FR-18).

### 2.3 Tài khoản mặc định

- Admin: `admin@eshop.com` / `Admin123!`
- User test: `test@eshop.com` / `Test1234!`

---

## 3. PHẠM VI KIỂM THỬ (Testing Scope)

### 3.1 Trong phạm vi (In Scope)

Hai thành viên chia phạm vi để **không trùng feature và không trùng workflow hiệu năng**.

| Bài tập | 23127207 — Khoa | 23127438 — Nguyên |
|---|---|---|
| **HW02** | FR-02 Đăng nhập & khóa TK · FR-07 Giỏ hàng · FR-13 Dashboard · FR-21 Mobile Cart & Checkout | FR-04 Hồ sơ · FR-09 Mã giảm giá · FR-10 Vòng đời đơn hàng · FR-18 Quản lý đơn hàng admin · FR-20 Danh sách & tìm kiếm mobile |
| **HW03** | 5 màn hình: Web Login, Web Register, Admin Login, Admin Category, Mobile Login (qua Expo Web) | 8 màn hình web: Trang chủ, Chi tiết SP, Đăng nhập, Đăng ký, Quên MK, Giỏ hàng, Thanh toán, Hồ sơ/Lịch sử ĐH |
| **HW04** | FR-02 Login · FR-07 Cart · FR-13 Dashboard (UI + API) | FR-02 Login · FR-09 Coupon · FR-14 Category CRUD (UI + API) |
| **HW05** | Workflow **Browse-to-buy**: `POST /api/login` → `GET /api/products` → `GET /api/products/{id}` → `POST /api/cart` → `POST /api/checkout` | Workflow **Category-guided buy**: `POST /api/login` → `GET /api/categories` → `GET /api/products?search=` → `POST /api/cart` → `POST /api/checkout` |

Ngoài ra, thành viên 23127207 còn thực hiện 2 mini-lab bổ trợ trên branch `HW4-Khoa`:
**Database Testing** (toàn vẹn dữ liệu + integration coupon/order state machine, Jest + Supertest) và
**GUI Automation** cho màn hình danh sách sản phẩm (Playwright).

### 3.2 Ngoài phạm vi (Out of Scope)

- **Kiểm thử xâm nhập (penetration testing)** đầy đủ. Các lỗ hổng bảo mật được ghi nhận là **hệ quả** của
  kiểm thử chức năng/hiệu năng, không phải kết quả của một đợt pentest có phương pháp.
- **Triển khai và kiểm thử trên môi trường production**. Toàn bộ công việc chạy trên máy cá nhân
  (`localhost`), không có hạ tầng staging/production.
- **Kiểm thử tải hạ tầng ngoài SUT** (CDN, load balancer, reverse proxy) — hệ thống chỉ có 1 process Node.
- **Các endpoint bị loại khỏi workflow hiệu năng** để tránh trùng lặp giữa hai thành viên:
  - Khoa loại trừ: `/api/products?search=`, `/api/categories`, `/api/apply-coupon`,
    `/api/orders/my-orders`, `/api/admin/**`.
  - Nguyên loại trừ: `GET /api/products/{id}` (thuộc phạm vi thành viên khác).
- **Kiểm thử khả năng tương thích ngược của cơ sở dữ liệu / migration** — `database.js` xóa và seed lại
  toàn bộ DB mỗi lần khởi động nên không có kịch bản migration để kiểm thử.

### 3.3 Các hạng mục chưa kiểm thử được (Items Not Tested)

Mục này liệt kê **trung thực** những gì nằm trong phạm vi nhưng không hoàn thành được, kèm lý do.

| Hạng mục | Thuộc về | Số lượng / mức độ | Lý do |
|---|---|---|---|
| 89 test case HW02 chưa thực thi | Khoa | FR-02: 50 TC · FR-21: 39 TC | Hết thời lượng bài tập; FR-21 cần thiết bị/emulator mobile ổn định |
| Bàn phím mềm (soft keyboard) native Android | Khoa (HW03) | 1 item checklist | Chỉ chạy được qua Expo Web trên trình duyệt desktop — không phải thiết bị thật |
| Safari thật trên macOS/iOS | Cả hai (HW03) | 1/3 platform | Playwright cung cấp bản build **WebKit**, cùng engine `AppleWebKit/605.1.15` nhưng **không phải** `Safari.app` |
| Thiết bị Android vật lý | Cả hai (HW03) | — | Chỉ có Pixel emulation / Expo Web; đã khai báo rõ, không nhận là "kiểm thử trên Android thật" |
| Pilot session + phản hồi post-session probe | Khoa (HW03 Task 2) | 1 pilot + 7 bộ probe | Không thu thập được từ người tham gia |
| Kiểm thử usability có người dùng thật | Nguyên (HW03) | — | Phần HW03 của Nguyên tập trung vào GUI checklist và cross-platform; không có dữ liệu phiên usability |
| Điểm gãy thật của SUT | Nguyên (HW05) | > 200 VU | Nút cổ chai là think-time và khả năng sinh thread của JMeter trên 1 máy, không phải SUT — cần JMeter phân tán |

---

## 4. SỐ LIỆU KIỂM THỬ (Metrics)

### 4.1 Test case đã lập kế hoạch so với đã thực thi (Planned vs Executed)

| Bài tập / Hạng mục | Khoa — Planned | Khoa — Executed | Khoa — % | Nguyên — Planned | Nguyên — Executed | Nguyên — % |
|---|---:|---:|---:|---:|---:|---:|
| HW02 — Test case thiết kế | 259 | 170 | **65.6%** | 150 | 150 | **100%** |
| HW03 — GUI checklist item | 58 | 58 | 100% | 66 | 66 | 100% |
| HW03 — Phiên usability | 7 | 7 | 100% | — | — | — |
| HW03 — Lượt cross-platform | 232 *(58 × 4 môi trường)* | 232 | 100% | 198 *(66 × 3 platform)* | 198 | 100% |
| HW04 — Test case automation | 400 | 400 | 100% | 40 | 40 | 100% |
| HW04 — Lượt chạy trên browser | 1,200 *(400 × 3)* | 1,200 | 100% | 120 *(40 × 3)* | 120 | 100% |
| HW05 — Kịch bản tải | 4 | 4 | 100% | 4 | 4 | 100% |
| HW05 — Tổng số mẫu (samples) | — | **61,261** | — | — | **104,030** | — |

**Tổng hợp cấp nhóm:**

| Chỉ số | Giá trị |
|---|---:|
| Test case thủ công HW02 đã thiết kế | **409** (259 + 150) |
| Test case thủ công HW02 đã thực thi | **320** (170 + 150) — đạt **78.2%** |
| GUI checklist item | **124** (58 + 66) |
| Lượt thực thi cross-platform HW03 | **430** (232 + 198) |
| Test case automation HW04 | **440** (400 + 40) |
| Lượt chạy automation trên browser | **1,320** (1,200 + 120) |
| Kịch bản hiệu năng HW05 | **8** (4 + 4) |
| Tổng mẫu HTTP trong kiểm thử hiệu năng | **165,291** (61,261 + 104,030) |

### 4.2 Kết quả Pass / Fail / Blocked / Not executed

#### 4.2.1 HW02 — Kiểm thử miền & giá trị biên

**Khoa (23127207) — theo feature:**

| Feature | Tổng TC | Executed | Passed | Failed | Blocked | Not Executed |
|---|---:|---:|---:|---:|---:|---:|
| FR-02 Đăng nhập & Khóa tài khoản | 80 | 30 | 11 | 19 | 0 | 50 |
| FR-07 Giỏ hàng | 90 | 90 | 35 | 55 | 0 | 0 |
| FR-13 Dashboard | 46 | 46 | 36 | 10 | 0 | 0 |
| FR-21 Mobile Cart & Checkout | 43 | 4 | 2 | 2 | 0 | 39 |
| **Tổng** | **259** | **170** | **84** | **86** | **0** | **89** |

Tỉ lệ pass trên số đã thực thi: **49.4%** (84/170).

**Nguyên (23127438) — theo bộ kỹ thuật kiểm thử:**

| Test suite | Phạm vi | Designed | Executed | Passed | Failed | Bugs |
|---|---|---:|---:|---:|---:|---:|
| Domain / BVA Testing | FR-04, FR-10, FR-18, FR-20 | 100 | 100 | 79 | 21 | 10 |
| Decision Table Testing | FR-09 | 10 | 10 | 6 | 4 | 3 |
| State Transition Testing | FR-10 | 20 | 20 | 18 | 2 | 2 |
| Use Case Testing | FR-10 | 20 | 20 | 15 | 5 | 5 |
| **Tổng** | | **150** | **150** | **118** | **32** | **20** |

Tỉ lệ pass: **78.7%** (118/150). Chi tiết Domain/BVA theo feature: FR-04 `32/20/12`, FR-10 `23/21/2`,
FR-18 `27/21/6`, FR-20 `18/17/1` (Designed/Passed/Failed). Phân bổ kỹ thuật trong 100 TC Domain/BVA:
**69 EP + 31 BVA**.

#### 4.2.2 HW03 — GUI, Usability, Cross-platform

**Khoa (23127207):**

| Task | Đơn vị đo | Passed | Failed | Blocked / Khác |
|---|---|---:|---:|---|
| Task 1 — GUI checklist | 58 item | 37 | 20 | 1 Blocked |
| Task 2 — Usability | 7 người tham gia | **0/7** hoàn thành đủ SC1–SC5 | — | Phễu sụp tại bước cập nhật hồ sơ |
| Task 3 — Cross-platform | 58 item × 4 môi trường = 232 lượt | 37 | 20 | 1 Not-Observable / mỗi môi trường |

- SUS trung bình: **76.79** (70 câu trả lời từ 7 người tham gia).
- Trung vị thời gian hoàn thành tác vụ (tính được): **80 giây**.
- Nguồn gốc checklist: 48 item `AI_INITIAL` + 10 item `HUMAN_ADDED`.
- Chỉ **2/3** platform đủ điều kiện: WebKit trên Windows không phải Safari; Pixel emulation không phải Android thật.

**Nguyên (23127438):**

| Task | Đơn vị đo | Passed | Failed | Ghi chú |
|---|---|---:|---:|---|
| Task 1 — GUI checklist | 66 item | 9 | 57 | 62 item từ AI (sau dedup) + 4 item bổ sung thủ công |
| Task 3 — P1 Chromium 151 | 66 item | 7 | 59 | 0 Blocked |
| Task 3 — P2 Firefox 153 | 66 item | 6 | 60 | 0 Blocked |
| Task 3 — P3 WebKit 26.5 | 66 item | 6 | 60 | 0 Blocked |

Phân bổ 66 item theo Interface Aspect: IA-01 General UI **17** (3 Pass / 14 Fail) · IA-02 Forms **15**
(2/13) · IA-03 Navigation **15** (3/12) · IA-04 Feedback & State **19** (1/18).

Kết quả cross-platform: **179 ảnh viewport** cho mọi item Fail trên mọi platform + **18 ảnh cửa sổ thật**.
Khác biệt giữa các platform: **1** item đổi hẳn Pass/Fail (XP-01), **28** item cùng kết quả nhưng giá trị
hiển thị khác nhau, **4** item cho kết luận khác với chấm tay ở Task 1.

#### 4.2.3 HW04 — Automation

**Khoa (23127207)** — Playwright + TypeScript, mỗi feature chạy trên 3 browser và cho **kết quả pass/fail
giống hệt nhau** trên cả 3:

| Feature | Test case | Lượt chạy (×3 browser) | Passed | Failed | Bug đã biết tái hiện | Bug mới |
|---|---:|---:|---:|---:|---:|---:|
| FR-02 Login | 137 | 411 | 106 | 31 | 13 | 8 |
| FR-07 Cart | 142 | 426 | 66 | 76 | 15 | 7 |
| FR-13 Dashboard | 121 | 363 | 50 | 71 | 3 | 4 |
| **Tổng** | **400** | **1,200** | **222** | **178** | **31** | **19** |

**Nguyên (23127438)** — Playwright + TypeScript, data-driven + Page Object Model:

| Feature | Test case | Lượt chạy (×3 browser) | Passed | Failed | Bug phát hiện |
|---|---:|---:|---:|---:|---:|
| FR-02 Đăng nhập & Khóa TK | 15 | 45 | 27 | 18 *(= 6 TC × 3)* | 5 |
| FR-09 Mã giảm giá | 13 | 39 | 24 | 15 *(= 5 TC × 3)* | 3 |
| FR-14 Danh mục CRUD | 12 | 36 | 30 | 6 *(= 2 TC × 3)* | 1 |
| **Tổng** | **40** | **120** | **81** | **39** | **9** |

100% test fail là **fail đúng kỳ vọng**: assertion viết theo đặc tả, SUT triển khai sai đặc tả.
13 test case fail giống hệt nhau trên cả Chromium, Firefox và WebKit → chứng minh lỗi thuộc phía
server/ứng dụng chứ không phải test flaky.

**Mini-lab bổ trợ (Khoa, branch `HW4-Khoa`):**

| Mini-lab | Công cụ | Tổng TC | Passed | Failed | Pass rate |
|---|---|---:|---:|---:|---:|
| Database Testing | Jest 29 + Supertest 7 + faker (seed `23127207`) | 11 | 7 | 4 | 63.64% |
| GUI Automation — Product List | Playwright 1.61.1 (Chromium) | 20 | 13 | 7 | 65% |

#### 4.2.4 HW05 — Kiểm thử hiệu năng

**Khoa (23127207)** — Apache JMeter 5.6.3 non-GUI, workflow Browse-to-buy, máy Windows 11:

| Kịch bản | Cấu hình VU | Thời lượng | Samples | RPS | Error % | p95 tổng thể | Kết luận |
|---|---|---|---:|---:|---:|---:|---|
| Load | 50 VU | 5 phút | 9,173 | 30.79 | 0.00% | **25.0 ms** | ✅ Đạt SLO (`p95 < 800 ms`, `Error < 0.1%`) |
| Stress | 25 → 200 VU | 8 phút | 26,939 | 56.23 | 0.00% | **586.0 ms** | ⚠️ Knee point tại 100 → 200 VU (p95 tăng 26 ms → 761 ms) |
| Spike | 10 → 300 VU | 6 phút | 11,794 | 32.96 | 0.00% | **1,016.0 ms** | ✅ Đàn hồi tốt: đỉnh 1,302 ms, phục hồi về 25 ms |
| Endurance | 30 VU | 12 phút | 13,355 | 18.62 | 0.00% | **382.0 ms** | ⚠️ Rò rỉ bộ nhớ 6.45 MB/phút (p95 thoái hóa 47 ms → 2,112 ms) |
| **Tổng** | | **31 phút** | **61,261** | | **0.00%** | | |

Phát hiện quan trọng — **rò rỉ bộ nhớ**: RAM private tăng từ 60.30 MB lên 137.39 MB (đỉnh 172.49 MB) trong
12 phút → **6.45 MB/phút ≈ 387 MB/giờ**. Dự báo thời điểm cạn bộ nhớ (Time to OOM): container 512 MB sập
sau **70 phút**; cloud instance 1024 MB sau **149 phút**; Node.js heap 2048 MB sau **308 phút**.
Nguyên nhân gốc: đối tượng toàn cục `userCarts` tại `backend/server.js:14,293` liên tục `push()` mà không
bao giờ giải phóng sau khi thanh toán.

**Nguyên (23127438)** — Apache JMeter 5.6.3 non-GUI, workflow Category-guided buy, máy Apple M4 / 16 GB:

| Kịch bản | VU đỉnh | Thời lượng | Samples | Throughput | Error % | p95 | p99 | max | CPU đỉnh | RSS đỉnh |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Load | 20 | 5 phút | 3,833 | 12.84 req/s | 0.00% | 7 ms | 8 ms | 27 ms | 5.5% | 47 MB |
| Stress | 200 | ~7 phút | 63,398 | 151.20 req/s | 0.00% | 7 ms | 11 ms | 51 ms | 41.6% | 102 MB |
| Spike | 160 | 5 phút | 22,080 | 73.71 req/s | 0.00% | 6 ms | 10 ms | 33 ms | 41.5% | 70 MB |
| Soak | 30 | 12 phút | 14,719 | 20.50 req/s | 0.00% | 6 ms | 7 ms | 23 ms | 6.7% | 42 MB |
| **Tổng** | | **~29 phút** | **104,030** | | **0.00%** | | | | | |

Kết luận ngưỡng: **chưa chạm điểm gãy trong dải test** — SUT không lỗi tới 200 VU / 151 req/s. RAM node
dao động 30–42 MB và hạ về ~31 MB khi kết thúc soak → **không phát hiện rò rỉ bộ nhớ ở mức tải này**.
Endpoint nặng nhất luôn là `POST /api/checkout` (~4–5 ms, do `INSERT INTO orders` + fsync).

> **⚠️ Không so sánh trực tiếp p95 giữa hai thành viên.** Hai bộ số chạy trên hai cấu hình phần cứng và
> hai workflow khác nhau (Windows 11 vs Apple M4 10-core; Browse-to-buy có payload danh mục ~154 KB và
> 505 sản phẩm vs Category-guided buy trên bảng products 5 dòng). Chênh lệch p95 (25 ms vs 7 ms ở kịch bản
> Load) phản ánh khác biệt môi trường và dữ liệu, **không** phản ánh chất lượng phép đo.

> **⚠️ Kết luận về rò rỉ bộ nhớ khác nhau giữa hai bộ đo — và cả hai đều đúng trong bối cảnh của mình.**
> Khoa đo được 6.45 MB/phút với 30 VU trên workflow đẩy giỏ hàng liên tục và danh mục 505 sản phẩm;
> Nguyên không thấy leak ở 30 VU trên bảng products 5 dòng vì mỗi object giỏ rất nhỏ và GC của V8 thu hồi
> kịp. Cả hai cùng chỉ đúng một nguyên nhân gốc: giỏ hàng lưu in-memory (`userCarts`). Kết luận an toàn:
> **leak là có thật và phụ thuộc kích thước payload giỏ hàng cùng số user đồng thời.**

### 4.3 Tổng số defect theo trạng thái và mức độ nghiêm trọng

#### 4.3.1 Khoa (23127207)

| Bài tập | Sổ đăng ký defect | Số lượng | Phân bổ mức độ | GitHub Issue |
|---|---|---:|---|---|
| HW02 | `bug_report.md` | **48** | High 29 · Medium 13 · Low 6 | #31 – #166 (rải rác) |
| HW03 | `Bug_Report.md` | *(xem ghi chú)* | — | 18 issue duy nhất cho Task 1 |
| HW04 | `bug-report-*.md` | **50** | 1 Critical · 5 High (bảo mật) · còn lại Major/Medium/Minor | #318 – #329, #333 – #339 (19 bug mới) |
| HW05 | `deliverables/` + GitHub | **3** | 1 Major (memory leak) · 2 Medium (knee point, spike degradation) | 3 issue đã lập |

HW02 theo feature: FR-02 **19** bug · FR-07 **18** · FR-13 **5** · FR-21 **6** = 48.

HW04 gồm **31 bug đã biết từ HW02 được tái hiện lại** + **19 bug mới**, trong đó:
- **1 CRITICAL**: `PUT /api/users/me` cho phép người dùng bất kỳ tự đặt `role = "admin"` (privilege escalation).
- **5 HIGH (bảo mật)**: rò rỉ mật khẩu dạng plaintext qua API login; tài khoản "ma" do trùng email;
  chấp nhận mật khẩu rỗng; token đặt lại mật khẩu có thể brute-force; xem đơn hàng không cần xác thực (IDOR).

> **Ghi chú HW03 — không có một con số tổng duy nhất.** Báo cáo gốc cố ý giữ ba đơn vị đếm khác nhau và
> **không** cộng gộp: 20 **failed checklist assertion** (ánh xạ tới 18 GitHub issue) · 3 **software bug**
> (issue #55, #37, #118) · 4 **usability issue** · 9 **nhóm systemic finding** cross-platform. Một lỗi tái
> hiện trên môi trường khác **không** được tính là bug mới. Báo cáo này giữ nguyên cách đếm đó.

#### 4.3.2 Nguyên (23127438)

| Bài tập | Sổ đăng ký defect | Số lượng | Phân bổ mức độ | GitHub Issue |
|---|---|---:|---|---|
| HW02 | `TEST_CASE_SUMMARY.md` | **20** | High 17 · Medium 2 · Low 1 | — |
| HW03 Task 1 | `bug-report.md` | **48** (gộp từ 57 item Failed) | Blocker 2 · Major 20 · Minor 26 | #194 – #241 |
| HW03 Task 3 | `report.md` §3–5 | **7** phát hiện cross-platform | XP-01 … XP-07 | XP-01 → #242 |
| HW04 | `REPORT.md` | **9** | BUG-01 … BUG-09 | đã lập issue + ảnh chứng cứ |
| HW05 | `docs/bug_report.md` | **6** | 1 Critical · 3 Major · 2 Minor | #402 – #407 |

Chi tiết 6 bug HW05 của Nguyên:

| Issue | Bug | Mức độ |
|---|---|---|
| #402 | Account lockout sai đặc tả (2 lần sai đã khóa, khóa 180 s) | Major |
| #403 | **SQL Injection** ở `GET /api/products?search` | **Critical** |
| #404 | `GET /api/products/:id` trả HTTP 200 + `{}` cho id không tồn tại | Minor |
| #405 | Trường `price` khác kiểu dữ liệu giữa id chẵn và id lẻ | Minor |
| #406 | Giỏ hàng in-memory: mất khi restart, trộn giỏ giữa user, rò rỉ RAM | Major |
| #407 | `database.js` DROP + reseed toàn bộ DB mỗi lần khởi động | Major |

#### 4.3.3 Defect được cả hai thành viên phát hiện độc lập

Các lỗi dưới đây xuất hiện trong sổ đăng ký của **cả hai** thành viên. Khi tính tổng cấp nhóm, **chúng chỉ
được đếm một lần**; ngược lại, việc hai người phát hiện độc lập cùng một lỗi là bằng chứng mạnh cho tính
tái lập của lỗi đó.

| Lỗi | Khoa ghi nhận tại | Nguyên ghi nhận tại | Mức độ đồng thuận |
|---|---|---|---|
| Bộ đếm đăng nhập sai tăng **+2** thay vì +1, và khóa **180 s** thay vì 30 s | HW02 `BUG-FR02-A-01` (#31), `BUG-FR02-A-02` (#32) | HW04 `BUG-04`, `BUG-05`; HW05 issue #402 | Cao — cả hai đọc trực tiếp `server.js` |
| Ô mật khẩu trang `/login` dùng `type="text"` (không che ký tự) | HW02 `BUG-FR02-A-07` (#37) | HW03 `BUG-03` (#196); HW04 `BUG-03` | Cao |
| Heading trang `/login` hiển thị sai thành "Đăng Ký" | HW02 `BUG-FR02-A-04` (#34) | HW03 `BUG-06` (#199); HW04 `BUG-01` | Cao |
| Trường Email dùng `type="text"` thay vì `type="email"` | HW03 Task 1 (failed assertion) | HW03 `BUG-10` (#203); HW04 `BUG-02` | Cao |
| Giỏ hàng lưu in-memory → mất khi restart / rò rỉ RAM | HW05 (memory leak `userCarts`) | HW05 issue #406 | Cao — cùng chỉ ra `userCarts` |

**Ước tính tổng defect duy nhất cấp nhóm:** khoảng **170 – 180** defect, sau khi trừ khoảng 5–10 lỗi trùng
lặp nêu trên và các lỗi tái hiện giữa HW02 → HW04 của Khoa (31 lỗi). Con số này được trình bày là **ước
tính có khoảng**, không phải phép cộng chính xác, vì bốn bài tập dùng bốn đơn vị đếm khác nhau
(test case fail / checklist assertion / bug gộp theo nguyên nhân gốc / GitHub issue).

### 4.4 Phân bố defect theo module

Bảng đếm theo **sổ đăng ký gốc của từng bài tập**; ô trống nghĩa là module đó không nằm trong phạm vi
của thành viên/bài tập đó.

| Module | Khoa HW02 | Khoa HW04 | Nguyên HW02 | Nguyên HW03 | Nguyên HW04 | Nguyên HW05 |
|---|---:|---:|---:|---:|---:|---:|
| Xác thực & Khóa tài khoản (FR-01/02/03/12) | 19 | 21 | — | ~12 | 5 | 1 |
| Hồ sơ người dùng (FR-04) | — | — | 4 | ~3 | — | — |
| Giỏ hàng · Thanh toán · Coupon (FR-07/09/21) | 24 | 22 | 3 | ~20 | 3 | 1 |
| Vòng đời & quản lý đơn hàng (FR-10/18) | — | — | 12 | ~4 | — | — |
| Dashboard & Danh mục admin (FR-13/14) | 5 | 7 | — | — | 1 | — |
| Danh sách & tìm kiếm sản phẩm (FR-20) | — | — | 1 | ~9 | — | 2 |
| Backend / Hạ tầng / Hiệu năng | — | — | — | — | — | 2 |
| **Tổng theo sổ gốc** | **48** | **50** | **20** | **48** | **9** | **6** |

*Các số có dấu `~` ở cột Nguyên HW03 là phân bổ theo màn hình bị ảnh hưởng; một bug gộp theo nguyên nhân
gốc có thể chạm nhiều màn hình nên tổng cột được lấy từ sổ đăng ký (48), không phải từ phép cộng hàng.*

**Nhận xét:** hai module tập trung nhiều defect nhất trên toàn bộ chương trình kiểm thử là
**Xác thực & Khóa tài khoản** và **Giỏ hàng / Thanh toán / Coupon** — đúng hai module chứa toàn bộ lỗi
mức Critical và Blocker đã phát hiện.

### 4.5 Mâu thuẫn số liệu giữa các nguồn (khai báo bắt buộc)

Ba mâu thuẫn dưới đây tồn tại trong tài liệu gốc. Báo cáo này **nêu nguyên trạng, không tự hòa giải**.

1. **Khoa — HW02 dùng hai thang mức độ khác nhau.** `main-report.md` phân loại theo
   Critical / Major / Minor / Cosmetic, trong khi `bug_report.md` phân loại theo High / Medium / Low.
   Hai thang này **không quy đổi được cho nhau** và **không được cộng gộp**. Báo cáo này lấy
   `bug_report.md` (48 bug — High 29 / Medium 13 / Low 6) làm sổ đăng ký chuẩn.

2. **Nguyên — HW03 có hai cách trình bày phân bổ IA.** Phần đầu `checklist-final.md` ghi
   "IA-01: 16 · IA-02: 14 · IA-03: 15 · IA-04: 17 · GAP: 4", còn bảng tổng kết cuối file và
   `cross_platform_testing/report.md` ghi "IA-01 17 · IA-02 15 · IA-03 15 · IA-04 19". Đây **không phải
   sai số**: cách thứ nhất tách riêng 4 item GAP bổ sung thủ công, cách thứ hai đã phân bổ 4 item đó vào
   đúng IA tương ứng. Cả hai đều cho tổng **66**. Báo cáo này dùng cách thứ hai (17/15/15/19).

3. **Nguyên — Task 1 và Task 3 cho kết quả Pass/Fail lệch nhau.** Task 1 (chấm tay) ghi
   **9 Pass / 57 Fail**; Task 3 (harness tự động, cùng bộ 66 item, trên Chromium) đo được
   **7 Pass / 59 Fail**. Chênh lệch đến từ **4 item bị lật kết quả**: 3 item Task 1 chấm Pass thực ra Fail
   (chỉ lộ ra khi stub dữ liệu lỗi hoặc đo bằng script thay vì bằng mắt), và 1 item Task 1 chấm Fail nhưng
   Pass trên Chromium (thông báo `required` phụ thuộc trình duyệt). Đây được ghi nhận là **một phát hiện
   có giá trị về giới hạn của việc tự chấm tay**, không phải lỗi số liệu cần sửa.

---

## 5. CÁC LOẠI KIỂM THỬ ĐÃ THỰC HIỆN (Types of Testing Performed)

| # | Loại kiểm thử | Thực hiện bởi | Bài tập | Kết quả cốt lõi |
|---|---|---|---|---|
| 1 | **Domain / Equivalence Partitioning** | Cả hai | HW02 | Khoa: phân vùng hợp lệ/không hợp lệ cho 4 feature. Nguyên: 69 TC EP trong bộ Domain/BVA |
| 2 | **Boundary Value Analysis** | Cả hai | HW02 | Khoa: 19 TC BVA cho FR-02 phát hiện lockout bị đặt cứng 180 s. Nguyên: 31 TC BVA |
| 3 | **Decision Table / Pairwise** | Nguyên | HW02 | 10 TC cho FR-09 coupon (5 điều kiện C1–C5), 6 Pass / 4 Fail, 3 bug |
| 4 | **State Transition Testing** | Nguyên | HW02 | 20 TC cho máy trạng thái đơn hàng FR-10; phát hiện chuyển được từ trạng thái kết thúc `canceled` → `delivered` |
| 5 | **Use Case Testing** | Nguyên | HW02 | 20 TC theo luồng chính / thay thế / ngoại lệ cho FR-10; 15 Pass / 5 Fail |
| 6 | **GUI Checklist Testing** | Cả hai | HW03 | 124 item tổng cộng; Khoa 37/58 Pass, Nguyên 9/66 Pass |
| 7 | **Usability Testing (SUS)** | Khoa | HW03 | 7 phiên có người dùng thật; 0/7 hoàn thành đủ SC1–SC5; SUS trung bình 76.79 |
| 8 | **Cross-browser / Cross-platform** | Cả hai | HW03 | 430 lượt thực thi; phát hiện 1 item đổi hẳn kết quả theo engine + 28 khác biệt giá trị hiển thị |
| 9 | **Automation UI (Playwright)** | Cả hai | HW04 | 440 test case × 3 browser = 1,320 lượt chạy; kết quả nhất quán tuyệt đối giữa 3 engine |
| 10 | **Automation API** | Cả hai | HW04 | Kiểm tra trực tiếp mã trạng thái và payload; đây là con đường phát hiện lỗi privilege escalation và rò rỉ mật khẩu |
| 11 | **Database Integrity & Integration Testing** | Khoa | Mini-lab | 11 TC (Jest + Supertest, SQLite `:memory:`); 7 Pass / 4 Fail; phát hiện thiếu foreign key constraint |
| 12 | **Performance — Load** | Cả hai | HW05 | Khoa 50 VU/5 phút (p95 25 ms). Nguyên 20 VU/5 phút (p95 7 ms). Cả hai 0.00% lỗi |
| 13 | **Performance — Stress** | Cả hai | HW05 | Khoa tìm được knee point tại 100 → 200 VU. Nguyên chưa chạm điểm gãy ở 200 VU / 151 req/s |
| 14 | **Performance — Spike** | Cả hai | HW05 | Cả hai xác nhận hệ thống đàn hồi tốt, phục hồi ngay sau khi tải đột biến rút |
| 15 | **Performance — Endurance / Soak** | Cả hai | HW05 | Khoa phát hiện rò rỉ 6.45 MB/phút. Nguyên không thấy leak ở workload nhẹ hơn |
| 16 | **Continuous Performance Testing (đề xuất)** | Cả hai | HW05 | Khoa: GitHub Actions `perf-regression.yml` + `baseline.json` + ngưỡng PASS/WARN/FAIL. Nguyên: pipeline lọc theo diff `backend/**`, 3-run median, ngưỡng +20% |
| 17 | **AI Critique / Misinterpretation Hunt** | Cả hai | HW05 | Mỗi người bắt được **5 lỗi diễn giải** của AI khi phân tích kết quả hiệu năng |

---

## 6. MÔI TRƯỜNG VÀ CÔNG CỤ KIỂM THỬ (Test Environment & Tools)

### 6.1 Môi trường hệ thống

| Hạng mục | Khoa (23127207) | Nguyên (23127438) |
|---|---|---|
| Hệ điều hành | Windows 11 Home 10.0.26200 | macOS 15.5 (24F74) |
| Phần cứng | Máy cá nhân Windows | MacBook Air — Apple M4, 10 cores (4P + 6E), 16 GB RAM |
| Node.js runtime | v24.10.0 | v26.4.0 |
| Backend API | `http://localhost:3000` | `http://localhost:3000` |
| Frontend Web | `http://localhost:5173` | `http://localhost:5173` |
| Web Admin | `http://localhost:5174` | — |
| Cơ sở dữ liệu | SQLite (file + `:memory:` cho mini-lab) | SQLite (in-process) |
| Mobile | React Native + Expo (Expo Web trên desktop) | — |

### 6.2 Công cụ

| Nhóm | Khoa (23127207) | Nguyên (23127438) |
|---|---|---|
| Automation UI/API | Playwright **1.61.1** (TypeScript) | Playwright **1.62.1** (TypeScript) |
| Unit / Integration DB | Jest **29.7** + Supertest **7.0** + `@faker-js/faker` **8.4.1** (seed cố định `23127207`) | — |
| Hiệu năng | Apache JMeter **5.6.3** (non-GUI) + **k6** | Apache JMeter **5.6.3** (non-GUI) |
| Giám sát tài nguyên | Windows Task Manager (chụp cùng khung hình với JMeter) | `htop` bám process `node server.js` |
| CI / CPT | GitHub Actions — `.github/workflows/perf-regression.yml` + `baseline/baseline.json` | Đề xuất pipeline trong `docs/ci_proposal.md` |
| Agent Skill | `.agents/skills/performance_testing/` (`generate_jmx.py`, `analyze_jtl.py`, `compare_runs.py`) | `skill/perf-jmeter/` (`gen_plan.py`, `analyze.py`) |
| Quản lý defect | GitHub Issues trên `trngnneee/eshop-sut` (qua `gh` CLI) | GitHub Issues trên `trngnneee/eshop-sut` |
| Trình duyệt kiểm thử | Chromium, Firefox, WebKit (Playwright) | Chrome for Testing 151 (Blink), Firefox 153 (Gecko), WebKit 26.5 |

### 6.3 Dữ liệu kiểm thử

| Hạng mục | Khoa | Nguyên |
|---|---|---|
| Pool tài khoản hiệu năng | 400 user `khoa001@eshop.com` … `khoa400@eshop.com` | 60 user `nguyen01@eshop.com` … `nguyen60@eshop.com` |
| File dữ liệu | `performance-testing/data/khoa_users.csv` (400 dòng, chuẩn RFC 4180) | `testplans/nguyen_users.csv` (60 user, recycle) |
| Dữ liệu sản phẩm | Seed thêm 500 sản phẩm (tổng danh mục 505) | Dữ liệu seed mặc định (5 sản phẩm), keyword search khớp seed thật |
| Chiến lược sinh dữ liệu | `faker.seed(23127207)` để tái lập chính xác giữa các lần chạy | Đăng ký user qua `POST /api/register`, token động `{{UNIQUE}}`, `{{LONG255}}` |

> **Cả hai thành viên đều tạo pool tài khoản riêng thay vì dùng chung `test@eshop.com`.** Đây là quyết
> định bắt buộc: cơ chế khóa tài khoản của SUT khóa **180 giây** sau 2 lần đăng nhập sai, nên dùng chung
> tài khoản giữa các kịch bản/browser sẽ tạo ra kết quả fail giả.

---

## 7. BÀI HỌC KINH NGHIỆM (Lessons Learned)

### 7.1 AI hỗ trợ tốt việc sinh khối lượng, nhưng sai một cách tự tin ở phần suy luận

Đây là bài học lặp lại nhất quán trên cả 4 bài tập và ở cả hai thành viên.

**Khoa — HW05 (5 lỗi diễn giải của AI, đối chiếu với ground-truth tính lại từ log thô):**

| # | AI khẳng định | Thực tế |
|---|---|---|
| 1 | Rò rỉ bộ nhớ do "kết nối SQLite không đóng" | Do mảng in-memory `userCarts` trong heap V8 (`server.js:14,293`) |
| 2 | Nên đánh index trên bảng `products` | Câu truy vấn là `SELECT * FROM products` quét toàn bảng, không có WHERE → index vô nghĩa |
| 3 | Nên cấu hình connection pool | SQLite là CSDL nhúng đơn tệp, không có khái niệm connection pool như RDBMS |
| 4 | Hệ thống sập do cạn kiệt CPU | CPU chỉ đạt đỉnh 5.33%; độ trễ tăng do hàng đợi sự kiện Node.js và GC pause |
| 5 | Dùng công thức percentile nội suy | JMeter dùng nearest-rank theo ISO 80000-2 → sai lệch con số p95 |

**Nguyên — HW05 (5 lỗi diễn giải + phán xét 7 đề xuất tối ưu):**

| # | AI khẳng định | Thực tế |
|---|---|---|
| 1 | Gọi p95 là "giá trị trung bình" | p95 là bách phân vị, không phải mean |
| 2 | Đọc một `max` lẻ thành "suy giảm hệ thống" | 1 sample đơn lẻ, khớp GC pause / SQLite checkpoint |
| 3 | CPU 42% một core là "bão hòa / breaking point" | Máy 10 core → còn dư địa rất lớn |
| 4 | Bottleneck là endpoint `search` | Thực tế là `POST /api/checkout` (ghi đĩa + fsync) |
| 5 | Baseline có think-time = công suất tối đa | Think-time làm giảm throughput có chủ đích, không phải giới hạn hệ thống |

Trong 7 đề xuất tối ưu mà AI đưa ra: **3 là hallucination** (index cho `LIKE '%q%'` vô hiệu, connection pool
cho SQLite nhúng, tăng timeout), 2 khả thi (index `users.email`, bật WAL), 2 có điều kiện (Redis, cluster).

**Khoa — HW02:** AI bỏ sót việc phân vùng kiểm thử độ nhạy chữ hoa/thường của email, bỏ sót tab navigation
accessibility, và không phát hiện được race condition do truy vấn CSDL bất đồng bộ — những lỗi chỉ lộ ra
khi con người thao tác thủ công trên nhiều tab đồng thời.

> **Kết luận:** AI hữu ích để sinh khối lượng test case và bản nháp checklist, nhưng **mọi kết luận suy
> luận của AI đều phải được đối chiếu với dữ liệu thô hoặc mã nguồn trước khi đưa vào báo cáo.**

### 7.2 Cô lập trạng thái test quan trọng ngang với chính test đó

Trong HW04, `TC-LOGIN-001` của Khoa fail một cách không tái lập. Truy vết cho thấy nguyên nhân không phải
lỗi sản phẩm: tài khoản seed dùng chung `test@eshop.com` vẫn đang bị khóa từ lần chạy trước trong cửa sổ
180 giây thật của SUT. Sửa bằng một `test.beforeAll` mở khóa tài khoản trước khi chạy khối describe.
Điều tra sự cố này còn phát hiện thêm một khoảng trống tài liệu thật: `BUG-FR02-A-13` đã được
`TC-JWT-001` tái hiện suốt nhưng chưa bao giờ được ghi vào bảng bug.

Nguyên xử lý cùng vấn đề theo hướng phòng ngừa: đăng ký user mới qua API cho từng test lockout/coupon,
snapshot bảng danh mục trước mỗi test và dọn sạch trong `afterEach`, đặt `workers: 1`, và reseed DB trước
mỗi platform trong Task 3.

### 7.3 Tự chấm bằng mắt trên chính checklist mình viết là không đáng tin

Task 3 của Nguyên chạy lại **cùng bộ 66 item** bằng harness tự động và **lật ngược 4 kết luận** của Task 1
chấm tay. Ba trong số đó là item được chấm Pass nhưng thực ra Fail — chỉ lộ ra khi stub API trả dữ liệu
lỗi (`price: "ba mươi triệu"` → màn hình hiện `NaN ₫`) hoặc khi đo bằng script thay vì ước lượng bằng mắt
(grid 3 cột tại đúng breakpoint 768 px). Hợp đồng của harness cấm hard-code kết quả Task 1, và chính 4 item
lệch này là bằng chứng điều cấm đó có hiệu lực.

### 7.4 Đọc mã nguồn backend là con đường tìm ra các lỗi nghiêm trọng nhất

Hai lỗi nặng nhất trong toàn bộ chương trình kiểm thử đều được tìm ra bằng cách chủ động đọc mã nguồn
backend để tìm code path chưa có test case nào chạm tới, chứ không phải bằng cách mở rộng test case theo
đặc tả:

- **Privilege escalation** (`PUT /api/users/me` cho phép tự đặt `role = "admin"`) — Khoa, HW04.
- **SQL Injection** tại `GET /api/products?search` — Nguyên, HW05.

### 7.5 Nhãn platform phải được khai báo trung thực

Cả hai thành viên đều gặp cùng một giới hạn: Playwright cung cấp bản build **WebKit**, không phải
`Safari.app`. Cùng engine `AppleWebKit/605.1.15` nên cùng lớp render/JS/CSS/validation, nhưng vỏ ứng dụng
khác — trong ảnh chứng cứ, menu bar macOS hiện tên "Playwright" chứ không phải "Safari". Việc khai báo rõ
điều này (thay vì để nhãn "Safari" trôi qua) là lý do bộ chứng cứ vẫn dùng được: người đọc biết chính xác
mình đang nhìn cái gì.

---

## 8. KHUYẾN NGHỊ (Recommendations)

### 8.1 Với đội phát triển SUT — ưu tiên theo mức độ

| Ưu tiên | Khuyến nghị | Căn cứ |
|---|---|---|
| **P0 — Chặn go-live** | Chặn mass-assignment ở `PUT /api/users/me`: không cho phép client gửi trường `role` | Privilege escalation, Khoa HW04 (CRITICAL) |
| **P0** | Tham số hóa truy vấn ở `GET /api/products?search` | SQL Injection, Nguyên HW05 #403 (CRITICAL) |
| **P0** | Escape đầu ra thay vì `dangerouslySetInnerHTML` cho từ khóa tìm kiếm và tên người dùng | XSS, Nguyên HW03 BUG-01 (Blocker) |
| **P0** | Không nhận tổng tiền do client gửi lên ở `/api/checkout`; tính lại phía server | Nguyên HW03 BUG-02 (Blocker) — ô tổng tiền là input sửa được |
| **P1** | Giải phóng `userCarts[userId]` sau khi thanh toán (`backend/server.js:14,293`) | Rò rỉ 6.45 MB/phút; container 512 MB sập sau 70 phút |
| **P1** | Không log/trả về mật khẩu dạng plaintext qua API login | Khoa HW04 (HIGH) |
| **P1** | Thêm claim `exp` vào JWT và cơ chế rate limiting cho `/api/login` | Khoa HW02 `BUG-FR02-A-13`, `BUG-FR02-A-10` |
| **P1** | Sửa cơ chế khóa tài khoản: tăng bộ đếm **+1** (hiện +2), thời gian khóa **30 s** (hiện 180 s) | Cả hai thành viên phát hiện độc lập |
| **P2** | Thêm ràng buộc khóa ngoại cho `coupon_usage` (hiện để lại orphan record khi xóa user) | Khoa, mini-lab Database Testing `BUG-DB-001` |
| **P2** | Sửa công thức tính coupon phần trăm (hiện tính `discount = total × (1 − rate)` thay vì `total × rate`) | Khoa `BUG-API-003`; Nguyên HW04 `BUG-06` |
| **P2** | Chặn chuyển trạng thái từ trạng thái kết thúc (`canceled` → `delivered` hiện trả HTTP 200) | Khoa `BUG-API-004`; Nguyên HW02 State Transition |
| **P2** | `database.js` không nên DROP + reseed toàn bộ DB mỗi lần khởi động | Nguyên HW05 #407 |
| **P3** | Thống nhất `type="email"` / `type="password"`, dấu `*` cho trường bắt buộc, `lang="vi"`, `htmlFor` cho label | Cụm lỗi GUI/accessibility, cả hai thành viên |

### 8.2 Với hoạt động kiểm thử — các đợt sau

1. **Chạy nốt 89 test case còn tồn của HW02** (FR-02: 50, FR-21: 39) — đây là khoảng trống độ phủ lớn nhất
   còn lại của nhóm.
2. **Bổ sung thiết bị thật**: một máy macOS/iOS cho Safari và một thiết bị Android vật lý sẽ nâng số
   platform đủ điều kiện từ 2/3 lên 3/3 và mở khóa các item soft-keyboard hiện đang không quan sát được.
3. **Đưa cổng CPT vào CI cho mọi pull request** chạm `backend/**`, dùng ngưỡng tương đối so với
   `baseline.json` (PASS ≤ +10% Δp95 · WARN +10…20% · FAIL > +20% hoặc error > 1.0%) và median của 3 lần
   lặp để chống nhiễu.
4. **Chạy lại kịch bản endurance với payload giỏ hàng lớn trên cả hai môi trường** để định lượng chính xác
   ngưỡng mà rò rỉ `userCarts` trở nên nguy hiểm — hiện hai bộ đo cho kết luận khác nhau vì workload khác nhau.
5. **Bỏ think-time và/hoặc chạy JMeter phân tán** để tìm điểm gãy thật của SUT trên phần cứng Apple M4 —
   hiện giới hạn đo là công cụ, không phải hệ thống.
6. **Hợp nhất sổ đăng ký defect của hai thành viên** thành một register duy nhất có ID toàn cục, để loại
   bỏ hẳn nhu cầu ước lượng khoảng ở mục 4.3.3.

---

## 9. THỰC HÀNH TỐT ĐÃ ÁP DỤNG (Best Practices)

| # | Thực hành | Lợi ích thực tế đã đo được |
|---|---|---|
| 1 | **Data-driven test + Page Object Model** — toàn bộ test case nằm trong `data/*.json`, spec chỉ là vòng lặp dispatch | Nguyên mở rộng bộ test mà không viết thêm code spec; Khoa thêm 63 test case boundary/robustness với **zero** code spec mới |
| 2 | **Ma trận 3 browser cho mọi feature** | Kết quả pass/fail giống hệt nhau trên 3 engine là bằng chứng lỗi thuộc phía server, không phải flaky test — tách bạch được ngay hai loại nguyên nhân |
| 3 | **Pool tài khoản riêng cho từng thành viên** (`khoa001…400`, `nguyen01…60`) | Loại bỏ hoàn toàn fail giả do tranh chấp cửa sổ khóa tài khoản 180 s giữa các kịch bản |
| 4 | **Seed dữ liệu xác định** (`faker.seed(23127207)` gọi ở đầu mỗi `setupTestDB`) | Mọi lượt chạy — dù chạy toàn bộ hay chạy đơn lẻ — đều có dữ liệu giống hệt nhau |
| 5 | **Percentile theo nearest-rank ISO 80000-2** | Con số p95 trong báo cáo khớp chính xác với JMeter dashboard, không lệch do công thức nội suy |
| 6 | **Median của 3 lần lặp trong CPT** | Chống nhiễu phần cứng đám mây, giảm false alarm khi so với baseline |
| 7 | **Assertion kiểm nội dung, không chỉ status code** | Nguyên: login → `$.token`, categories → array, cart → "Added to cart", checkout → `$.orderId`. Nhiều lỗi trả HTTP 200 kèm body sai sẽ lọt nếu chỉ kiểm status |
| 8 | **Chụp JMeter + monitor tài nguyên trong cùng một khung hình** | Bằng chứng CPU/RAM gắn được với đúng thời điểm chạy, không thể ghép từ hai lần chạy khác nhau |
| 9 | **Overlay MSSV + timestamp + version trình duyệt lên mọi ảnh chứng cứ** | Mỗi ảnh tự chứng minh được nguồn gốc; HTML report hiển thị "Run by: {MSSV}" |
| 10 | **Phân biệt rõ `NOT_RECORDED` / `NOT_OBSERVABLE` / `NOT_REACHED`** | Dữ liệu thiếu không bao giờ bị quy về 0 — giữ được tính trung thực của thống kê |
| 11 | **Đóng gói tri thức thành Agent Skill tái sử dụng** | Cả hai đều tạo skill sinh test plan từ file config JSON, chứng minh khả năng tái dùng cho workflow khác |
| 12 | **Tách rõ "failed assertion" khỏi "bug"** | Nhiều assertion fail có thể chung một nguyên nhân gốc; Nguyên gộp 57 item Failed thành 48 bug theo root cause |

---

## 10. TIÊU CHÍ KẾT THÚC (Exit Criteria)

| # | Tiêu chí | Trạng thái | Ghi chú |
|---|---|:---:|---|
| 1 | Toàn bộ test case đã thiết kế được thực thi | **Partial** | 320/409 TC thủ công HW02 (78.2%). Còn 89 TC của Khoa chưa chạy (FR-02: 50, FR-21: 39) |
| 2 | Toàn bộ GUI checklist item được thực thi | **Yes** | 124/124 item (58 + 66) |
| 3 | Toàn bộ test case automation chạy trên ≥ 3 browser | **Yes** | 1,320 lượt chạy, kết quả nhất quán trên Chromium / Firefox / WebKit |
| 4 | Đủ 4 kịch bản hiệu năng cho mỗi thành viên | **Yes** | 8 kịch bản, 165,291 mẫu, 0.00% lỗi trên toàn bộ |
| 5 | Mọi defect phát hiện đều được ghi nhận có chứng cứ | **Yes** | Ảnh chứng cứ cho từng bug ở cả hai thành viên |
| 6 | Defect được lập GitHub Issue | **Partial** | Đã lập: Khoa #31–#166, #318–#339, 3 issue HW05; Nguyên #194–#242, #402–#407. **Chưa lập**: 13 bug đã biết của FR-02 trong HW04 của Khoa và 20 bug HW02 của Nguyên |
| 7 | Kiểm thử trên tối thiểu 3 platform đủ điều kiện | **No** | 2/3 — WebKit không phải Safari; Pixel emulation / Expo Web không phải Android thật |
| 8 | Dữ liệu usability đầy đủ (pilot + probe) | **No** | Khoa: thiếu pilot session và phản hồi post-session probe. Nguyên: không có phần usability |
| 9 | Xác định được điểm gãy (breaking point) của SUT | **Partial** | Khoa xác định knee point tại 100→200 VU. Nguyên chưa chạm điểm gãy ở 200 VU (giới hạn công cụ, không phải SUT) |
| 10 | Có đề xuất Continuous Performance Testing | **Yes** | Khoa: workflow GitHub Actions đã hiện thực hóa. Nguyên: pipeline đề xuất kèm flow chart và phân tích trade-off |
| 11 | Có Agent Skill đóng gói tái sử dụng | **Yes** | `.agents/skills/performance_testing/` và `skill/perf-jmeter/`, cả hai đã validate end-to-end |
| 12 | Có video demo | **Yes** | Khoa: 4 video (HW04 ×2, HW05 ×2). Nguyên: thư mục Drive cho HW05 |
| 13 | Có báo cáo AI Audit / AI Critique / Disclosure | **Yes** | Cả hai đều nộp đủ bộ khai báo AI theo mẫu FIT@HCMUS |
| 14 | Không còn defect Critical/Blocker mở | **No** | Còn tối thiểu 4 lỗi P0 chưa vá (privilege escalation, SQL Injection, XSS, tổng tiền client-side) |

**Kết luận tiêu chí kết thúc: 7 Yes · 4 Partial · 3 No.**

---

## 11. KẾT LUẬN VÀ KÝ DUYỆT (Conclusion / Sign Off)

### 11.1 Kết luận về hệ thống — quyết định Go / No-Go

> ### 🚫 **NO-GO** — Hệ thống EShop **không** đạt điều kiện đưa vào vận hành.

Căn cứ:

1. **Bốn lỗ hổng mức chặn (P0) vẫn đang mở**, mỗi lỗi đều đủ để chặn go-live một cách độc lập:
   - Privilege escalation: bất kỳ người dùng đã đăng nhập nào cũng có thể tự nâng quyền thành admin bằng
     **một lời gọi API duy nhất**.
   - SQL Injection tại endpoint tìm kiếm sản phẩm.
   - XSS qua `dangerouslySetInnerHTML` ở từ khóa tìm kiếm và tên người dùng.
   - Tổng tiền thanh toán là input do client sửa được và được gửi thẳng lên API.
2. **Rò rỉ bộ nhớ đã được định lượng**: 6.45 MB/phút ở 30 VU. Trên container 512 MB, hệ thống sẽ hết bộ
   nhớ sau **70 phút** vận hành liên tục — tức là không thể chạy qua một ca làm việc.
3. **Tỉ lệ pass của kiểm thử chức năng thấp**: 49.4% (Khoa HW02, trên số đã thực thi) và
   13.6% (Nguyên HW03 GUI checklist: 9/66). Đây là hệ thống được cài lỗi có chủ đích cho mục đích học,
   nên con số này phản ánh **hiệu quả phát hiện lỗi của bộ test**, không phải chất lượng của một sản phẩm
   thương mại — nhưng vẫn là căn cứ hợp lệ cho quyết định No-Go.
4. **Độ phủ chưa đầy đủ**: 89 test case chưa thực thi và chỉ 2/3 platform đủ điều kiện, nên không có cơ sở
   khẳng định các module còn lại là sạch lỗi.

**Về mặt hiệu năng thuần túy**, hệ thống cho kết quả tốt trong dải tải đã kiểm thử: 0.00% lỗi trên toàn bộ
165,291 mẫu, đàn hồi tốt trước tải đột biến, và trên phần cứng Apple M4 chưa chạm điểm gãy ở 200 VU.
Rào cản go-live là **bảo mật và quản lý bộ nhớ**, không phải throughput.

### 11.2 Kết luận về bộ tài liệu kiểm thử

> ### ✅ **ĐẠT** — Bộ tài liệu kiểm thử đủ điều kiện bàn giao / nộp bài.

Toàn bộ 8 gói bài tập đã hoàn thành với chứng cứ thực thi thật, số liệu truy vết được tới file nguồn, các
mâu thuẫn số liệu được khai báo công khai thay vì che giấu, và các hạng mục không hoàn thành được nêu rõ
kèm lý do (mục 3.3 và mục 10). Không có số liệu nào được tổng hợp lại hoặc suy diễn để biến một tiêu chí
không đạt thành đạt.

### 11.3 Bảng ký duyệt

| Vai trò | Họ và tên | MSSV | Chữ ký | Ngày |
|---|---|---|---|---|
| Người lập báo cáo | Đặng Đăng Khoa | 23127207 | | 2026-08-17 |
| Người rà soát | Đặng Trường Nguyên | 23127438 | | |
| Giảng viên duyệt | | | | |

---

## 12. ĐỊNH NGHĨA, TỪ VIẾT TẮT (Definitions, Acronyms, Abbreviations)

| Thuật ngữ | Nghĩa đầy đủ | Giải thích trong ngữ cảnh tài liệu này |
|---|---|---|
| **SUT** | System Under Test | Hệ thống EShop được kiểm thử |
| **FR** | Functional Requirement | Yêu cầu chức năng, đánh số FR-01 … FR-22 trong `README.md` gốc |
| **TC** | Test Case | Một trường hợp kiểm thử |
| **EP** | Equivalence Partitioning | Kỹ thuật chia miền dữ liệu thành các lớp tương đương |
| **BVA** | Boundary Value Analysis | Kỹ thuật kiểm thử giá trị biên |
| **POM** | Page Object Model | Mẫu thiết kế đóng gói thao tác UI vào lớp riêng theo từng trang |
| **IA-01…IA-04** | Interface Aspect | 4 nhóm phân loại checklist GUI: General UI · Forms · Navigation · Feedback & State |
| **SC1–SC5** | Success Criteria | 5 tiêu chí hoàn thành phiên usability (HW03 Task 2 của Khoa) |
| **T0–T11** | Time-coding schema | Lược đồ mã hóa mốc thời gian khi phân tích bản ghi phiên usability |
| **XP-01…XP-07** | Cross-Platform finding | Mã phát hiện khác biệt giữa các nền tảng (HW03 Task 3 của Nguyên) |
| **SUS** | System Usability Scale | Thang đo khả dụng 10 câu, quy về điểm 0–100 |
| **VU** | Virtual User | Người dùng ảo do JMeter/k6 mô phỏng |
| **RPS / Throughput** | Requests Per Second | Số yêu cầu hệ thống xử lý mỗi giây |
| **p95 / p99** | 95th / 99th Percentile | 95% (hoặc 99%) số yêu cầu có thời gian phản hồi nhỏ hơn giá trị này |
| **Nearest-rank** | ISO 80000-2 | Phương pháp tính bách phân vị mà JMeter sử dụng (không nội suy) |
| **SLO** | Service Level Objective | Mục tiêu mức dịch vụ, ở đây: `p95 < 800 ms` và `Error < 0.1%` |
| **Knee point** | Điểm gãy đường cong | Mức tải mà tại đó thời gian phản hồi bắt đầu tăng phi tuyến |
| **Breaking point** | Điểm gãy | Mức tải mà tại đó hệ thống bắt đầu trả lỗi |
| **OOM** | Out Of Memory | Sự cố hệ thống dừng do cạn kiệt bộ nhớ |
| **RSS** | Resident Set Size | Lượng RAM vật lý mà tiến trình đang chiếm |
| **GC** | Garbage Collection | Cơ chế thu hồi bộ nhớ tự động của V8 |
| **CPT** | Continuous Performance Testing | Kiểm thử hiệu năng liên tục, tích hợp vào CI/CD |
| **JMX** | JMeter Test Plan | File XML định nghĩa kế hoạch kiểm thử của JMeter |
| **JTL** | JMeter Test Log | File log thô ghi từng mẫu request của JMeter |
| **JWT** | JSON Web Token | Token xác thực trả về sau khi đăng nhập thành công |
| **IDOR** | Insecure Direct Object Reference | Lỗ hổng truy cập tài nguyên của người khác qua ID trực tiếp |
| **XSS** | Cross-Site Scripting | Lỗ hổng cho phép chèn và thực thi mã script trong trang |
| **Mass assignment** | — | Lỗ hổng cho phép client gán giá trị cho trường lẽ ra chỉ server được đặt (ở đây: `role`) |
| **WAL** | Write-Ahead Logging | Chế độ ghi của SQLite giúp tăng khả năng ghi đồng thời |
| **Think-time** | — | Thời gian chờ mô phỏng hành vi suy nghĩ của người dùng thật giữa hai thao tác |

---

## PHỤ LỤC — CHỈ MỤC TÀI LIỆU NGUỒN

Mọi số liệu trong báo cáo này đều truy vết được tới một trong các file dưới đây.

### Thành viên 23127207 — Đặng Đăng Khoa

| Bài tập | Tài liệu nguồn |
|---|---|
| HW02 | [`main-report.md`](https://github.com/trngnneee/eshop-sut/blob/HW2-Khoa/main-report.md) · [`bug_report.md`](https://github.com/trngnneee/eshop-sut/blob/HW2-Khoa/bug_report.md) |
| HW03 | [`final-submission/Main_Report.md`](https://github.com/trngnneee/eshop-sut/blob/HW3-Khoa/final-submission/Main_Report.md) · [`final-submission/Bug_Report.md`](https://github.com/trngnneee/eshop-sut/blob/HW3-Khoa/final-submission/Bug_Report.md) |
| HW04 | [`HW4/README.md`](https://github.com/trngnneee/eshop-sut/blob/HW4-Khoa/HW4/README.md) · `HW4/docs/bug-report-{login,cart,dashboard}.md` |
| HW04 mini-lab | [`Database testing/REPORT.md`](https://github.com/trngnneee/eshop-sut/blob/HW4-Khoa/Database%20testing/REPORT.md) · `GUI testing/automation/AUTOMATION_TEST_RESULT.md` |
| HW05 | [`performance-testing/23127207_HW05_Report.md`](https://github.com/trngnneee/eshop-sut/blob/HW5/performance-testing/23127207_HW05_Report.md) · `performance-testing/deliverables/` |

### Thành viên 23127438 — Đặng Trường Nguyên

| Bài tập | Tài liệu nguồn |
|---|---|
| HW02 | [`TEST_CASE_SUMMARY.md`](https://github.com/trngnneee/eshop-sut/blob/HW2-Nguyen/TEST_CASE_SUMMARY.md) |
| HW03 Task 1 | [`tests/gui_and_usability_testing/checklist-final.md`](https://github.com/trngnneee/eshop-sut/blob/HW3-Nguyen/tests/gui_and_usability_testing/checklist-final.md) · [`bug-report.md`](https://github.com/trngnneee/eshop-sut/blob/HW3-Nguyen/tests/gui_and_usability_testing/bug-report.md) |
| HW03 Task 3 | [`tests/cross_platform_testing/report.md`](https://github.com/trngnneee/eshop-sut/blob/HW3-Nguyen/tests/cross_platform_testing/report.md) · `results-matrix.md` · `divergences.md` |
| HW04 | [`tests/automation_testing/REPORT.md`](https://github.com/trngnneee/eshop-sut/blob/HW04-Nguyen/tests/automation_testing/REPORT.md) |
| HW05 | [`tests/performance_testing/23127438_HW05_Report.md`](https://github.com/trngnneee/eshop-sut/blob/feat/HW05-Nguyen/tests/performance_testing/23127438_HW05_Report.md) · [`docs/results_summary.md`](https://github.com/trngnneee/eshop-sut/blob/feat/HW05-Nguyen/tests/performance_testing/docs/results_summary.md) |

### Tài liệu chung

| Tài liệu | Đường dẫn |
|---|---|
| Đặc tả yêu cầu hệ thống (SRS) | [`README.md`](https://github.com/trngnneee/eshop-sut/blob/main/README.md) |
| Đặc tả API | [`api_specification.md`](https://github.com/trngnneee/eshop-sut/blob/main/api_specification.md) |
| Hướng dẫn cài đặt | [`setup_guide.md`](https://github.com/trngnneee/eshop-sut/blob/main/setup_guide.md) |
| Danh sách GitHub Issues | https://github.com/trngnneee/eshop-sut/issues |

---

*Kết thúc Test Summary Report — phiên bản 1.0, ngày 2026-08-17.*
