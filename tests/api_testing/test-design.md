# Mini Exercise — API Testing: `POST /api/login`

- **MSSV:** 23127438
- **API đã chọn:** #9 — `POST /api/login` (Đăng nhập hệ thống)
- **SUT:** eshop-sut backend (`backend/server.js`), chạy tại `http://localhost:3000`

## Mô tả API

| Thuộc tính | Giá trị |
|---|---|
| Endpoint | `POST /api/login` |
| Request body | `{ "email": string, "password": string }` (JSON) |
| Response 200 | `{ "message": "Login successful", "token": <JWT>, "user": {...} }` |
| Response 401 | `{ "error": "Invalid email or password" }` (sai mật khẩu / email không tồn tại) |
| Response 403 | `{ "error": "Tài khoản đã bị khóa. Vui lòng thử lại sau." }` (tài khoản bị khóa) |
| Response 500 | `{ "error": <db error> }` |

Tài khoản seed sẵn: `test@eshop.com / Test1234!` (role `user`), `admin@eshop.com / Admin123!` (role `admin`).

**Hành vi đặc biệt (đọc từ source code):** mỗi lần sai mật khẩu với email tồn tại, `login_attempts` bị **cộng 2**; khi `login_attempts >= 3` tài khoản bị khóa **3 phút** (`locked_until`). Đăng nhập thành công reset `login_attempts = 0`. Điều này ảnh hưởng trực tiếp đến thứ tự chạy iteration (xem Bước 4).

---

## Bước 1 — Generate with AI

### Prompt đã dùng

> Tôi đang kiểm thử API `POST /api/login` của một backend Express + SQLite (eshop-sut).
>
> **Đặc tả:** request body JSON `{email, password}`. Đăng nhập thành công trả `200` với `{message: "Login successful", token: <JWT>, user: {id, name, email, role, ...}}`. Sai email hoặc sai mật khẩu trả `401` với `{error: "Invalid email or password"}`. Tài khoản bị khóa trả `403`. Tài khoản seed: `test@eshop.com / Test1234!` (user), `admin@eshop.com / Admin123!` (admin). Sai mật khẩu nhiều lần sẽ khóa tài khoản tạm thời.
>
> Hãy thiết kế test case **từng bước theo 4 nhóm sau, mỗi nhóm tối thiểu 2–4 case**, không gộp chung:
> 1. **Domain partitions:** giá trị hợp lệ / không hợp lệ / biên của `email` và `password` (email đúng-sai format, hoa-thường, thiếu field, body rỗng).
> 2. **State transitions:** hành vi khóa tài khoản sau nhiều lần đăng nhập sai, và reset khi đăng nhập thành công.
> 3. **Security:** SQL injection, XSS payload trong input, đăng nhập chéo tài khoản (dùng password của user khác).
> 4. **Schema validation:** response 200 phải chứa đúng các field `message`, `token` (JWT 3 phần), `user` với `id/name/email/role`; response lỗi phải chứa field `error`.
>
> Với **mỗi test case**, trả về bảng gồm đúng các cột: `tc_id`, `input` (request body cụ thể), `expected status`, `expected fields`, `rationale` (1–2 câu vì sao cần case này). Tổng cộng tối thiểu 12 case. Không tự ý giả định hành vi ngoài đặc tả — nếu phải giả định, ghi rõ ở cột rationale.

### AI output (rút gọn — 12 test case)

| tc_id | Input (request body) | Expected status | Expected fields | Rationale |
|---|---|---|---|---|
| AI-01 | `{"email":"test@eshop.com","password":"Test1234!"}` | 200 | `message`, `token`, `user` | Happy path — đăng nhập hợp lệ với role user. |
| AI-02 | `{"email":"admin@eshop.com","password":"Admin123!"}` | 200 | `message`, `token`, `user.role="admin"` | Đăng nhập hợp lệ với role admin, kiểm tra token chứa đúng role. |
| AI-03 | `{"email":"TEST@ESHOP.COM","password":"Test1234!"}` | 200 | `message`, `token`, `user` | Email thường không phân biệt hoa-thường theo RFC — giả định hệ thống chuẩn hóa email. |
| AI-04 | `{"email":"test@eshop.com","password":"WrongPass999!"}` | 401 | `error` | Partition mật khẩu sai với email tồn tại. |
| AI-05 | `{"email":"nonexistent@nowhere.test","password":"AnyPass123!"}` | 401 | `error` | Partition email không tồn tại; thông báo lỗi phải giống case sai mật khẩu (chống user enumeration). |
| AI-06 | `{"email":"test@eshop.com"}` (thiếu password) | 400 | `error` | Thiếu field bắt buộc — theo chuẩn REST nên trả 400 Bad Request. |
| AI-07 | `{"password":"Test1234!"}` (thiếu email) | 400 | `error` | Thiếu field bắt buộc — theo chuẩn REST nên trả 400 Bad Request. |
| AI-08 | `{}` (body rỗng) | 400 | `error` | Biên dưới của input — body không có field nào. |
| AI-09 | `{"email":"' OR '1'='1' --","password":"x"}` | 401 | `error` | Security — SQL injection cổ điển vào trường email không được bypass đăng nhập. |
| AI-10 | `{"email":"<script>alert(1)</script>@x.com","password":"x"}` | 401 | `error` | Security — payload XSS trong input phải bị từ chối như email không tồn tại. |
| AI-11 | Sai mật khẩu 3 lần liên tiếp với `test@eshop.com`, lần 4 dùng mật khẩu đúng | 403 (lần 4) | `error` | State transition — tài khoản phải bị khóa sau 3 lần sai (giả định mỗi lần sai +1 attempt). |
| AI-12 | `{"email":"test@eshop.com","password":"Test1234!"}` — kiểm schema sâu | 200 | `token` là JWT 3 phần; `user` có `id`, `name`, `email`, `role` | Schema validation — hợp đồng response phải đủ field cho client. |

---

## Bước 2 — Audit (human review)

| TC | Nhãn | Nhận xét hoặc chỉnh sửa |
|---|---|---|
| AI-01 | `VALID` | Khớp hành vi thực tế, đã verify bằng curl: 200 + đủ 3 field. Được chọn vào bộ chạy. |
| AI-02 | `VALID` | Đúng hành vi; không chọn vào bộ 5 iteration vì trùng partition "đăng nhập hợp lệ" với AI-01. |
| AI-03 | `INVALID` → **đã sửa** | AI giả định email không phân biệt hoa-thường, nhưng code dùng `WHERE email = ?` (SQLite `=` phân biệt hoa-thường) → thực tế trả **401**, không phải 200. Sửa expected status thành 401. Đây cũng là một usability issue đáng ghi nhận của SUT. |
| AI-04 | `VALID` | Đúng hành vi. **Bổ sung của người review:** case này có side effect `login_attempts +2`, phải đặt SAU case đăng nhập thành công và chỉ dùng tối đa 1 lần/lượt chạy để không khóa tài khoản seed. |
| AI-05 | `VALID` | Đúng hành vi, thông báo lỗi generic đúng như kỳ vọng chống user enumeration. |
| AI-06 | `INVALID` → **đã sửa** | API không có input validation — thiếu `password` vẫn đi vào so sánh và trả **401**, không phải 400. Sửa expected thành 401. Lưu ý thêm: case này vẫn tăng `login_attempts` của tài khoản thật (side effect nguy hiểm). |
| AI-07 | `INVALID` → **đã sửa** | Tương tự AI-06: thiếu `email` → query với `undefined` → không tìm thấy user → thực tế trả **401**. Sửa expected thành 401. |
| AI-08 | `INVALID` → **đã sửa** | Body rỗng thực tế trả **401** (không có user `undefined`), không phải 400. Đây là vi phạm chuẩn REST của SUT (đáng ra 400) — ghi nhận là observation, còn test case sửa theo hành vi thực tế. |
| AI-09 | `VALID` | Code dùng parameterized query nên SQLi không bypass được — expected 401 đúng. Được chọn vào bộ chạy. |
| AI-10 | `VALID` | Đúng hành vi (401); không chọn vào bộ 5 iteration vì cùng partition "email không tồn tại chứa ký tự đặc biệt" với AI-09. |
| AI-11 | `INCOMPLETE` | AI giả định mỗi lần sai +1 attempt, nhưng code **cộng 2** mỗi lần sai (`newAttempts = login_attempts + 2`) → chỉ cần **2 lần sai** là bị khóa. AI cũng không cảnh báo side effect: tài khoản seed bị khóa 3 phút sẽ làm fail các lần chạy CI kế tiếp. Vì vậy case này được giữ ở mức thiết kế/chạy tay, không đưa vào bộ data-driven. |
| AI-12 | `INCOMPLETE` | Danh sách field AI đưa ra đúng nhưng **thiếu quan sát quan trọng**: response 200 trả về **nguyên object `user` bao gồm cả `password` plaintext** — lỗ hổng lộ thông tin nhạy cảm. Bổ sung nhận xét này vào EX-03 bên dưới. Các assertion schema (JWT 3 phần, `user.email` khớp input) đã được gộp vào test script của collection. |

**Giả định AI chưa nêu rõ (bổ sung):** AI mặc định database luôn ở trạng thái seed sạch (`login_attempts = 0`, không bị khóa) khi bắt đầu chạy. Thực tế `database.sqlite` được commit kèm repo và bị thay đổi qua mỗi lần chạy, nên bộ test phải **tự bảo vệ**: iteration đăng nhập thành công chạy đầu tiên để reset `login_attempts` về 0.

---

## Bước 3 — Extend (test case AI bỏ sót)

| tc_id | Input | Expected status | Expected fields | Vì sao AI bỏ sót |
|---|---|---|---|---|
| EX-01 | Mọi response của `/api/login` (cả 200 lẫn 401) | — | Header `Content-Type` chứa `application/json`; response time < 2000ms | **Prompt quality:** prompt tập trung vào functional partition nên AI không sinh assertion phi chức năng ở tầng contract (header, latency). Được cài làm 2 assertion `[MINI]` chạy trong **mọi** iteration. |
| EX-02 | `{"email":"","password":""}` (chuỗi rỗng — khác với thiếu field) | 401 | `error` | **Model limitations:** AI sinh case "thiếu field" (AI-06/07/08) nhưng bỏ sót biên "field tồn tại nhưng là chuỗi rỗng" — hai partition khác nhau ở tầng parser/validation. Được chọn vào bộ chạy. |
| EX-03 | `{"email":"test@eshop.com","password":"Test1234!"}` — kiểm tra field **không được có** | 200 | `user` **không được** chứa `password` | **Đặc điểm API + prompt quality:** AI chỉ kiểm "field cần có" mà không kiểm "field cấm". Thực tế SUT trả về `password` plaintext trong `user` → **bug bảo mật thật** (đã confirm bằng curl). Không đưa assertion này vào bộ chạy CI vì sẽ fail do bug của SUT; ghi nhận làm bug report. |

---

## Bước 4 — Execute (Postman + Newman)

### 5 test case được chọn làm iteration data (`mini-login.data.json`)

Thứ tự có chủ đích: **AI-01 chạy đầu để reset `login_attempts`**, AI-04 (case duy nhất chạm `login_attempts`) chạy ngay sau, các case còn lại không có side effect.

| Iteration | tc_id | Mô tả | Expected status |
|---|---|---|---|
| 1 | AI-01 | Đăng nhập hợp lệ (user) | 200 |
| 2 | AI-04 | Sai mật khẩu, email tồn tại | 401 |
| 3 | AI-05 | Email không tồn tại | 401 |
| 4 | AI-09 | SQL injection vào email | 401 |
| 5 | EX-02 | Email + password chuỗi rỗng | 401 |

### Lệnh chạy

```bash
# Terminal 1
cd backend && npm run start

# Terminal 2
cd tests/api_testing
newman run mini-login.postman_collection.json \
  --environment mini-local.postman_environment.json \
  --iteration-data mini-login.data.json \
  --reporters cli,json \
  --reporter-json-export mini-newman-report.json
```

### Kết quả

- 5 iterations, 5 requests, **26 assertions, 0 failed** (xem `mini-newman-report.json`).
- Pre-request script upsert header `X-Student-Id = 23127438` và log ra console mỗi iteration để đối chiếu.
- Mỗi iteration chạy các assertion: status code theo `expected_status` từ data file, `Content-Type` là JSON, response time dưới ngưỡng (collection variable `maxResponseMs`), schema fields theo `expected_fields`, và assertion chuyên biệt cho positive case (JWT 3 phần, `user.email` khớp) / negative case (error message generic).

---

## Bước 5 — CI/CD

Workflow `newman-api-test.yml` (đặt tại `.github/workflows/`, bản copy nộp kèm trong thư mục này):

1. Checkout + setup Node 20.
2. `npm install` trong `backend/`, khởi động provider bằng `node server.js`, chờ tối đa 30s cho tới khi `GET /api/products/1` trả 200.
3. Cài Newman global, chạy collection với environment + iteration data.
4. Upload `mini-newman-report.json` làm artifact (kể cả khi fail, nhờ `if: always()`).

Quy trình pass/fail:

- **C1 (pass):** push bài làm lên nhánh `feature/23127438` → workflow "Newman API tests" xanh → chụp `ci-pass.png`.
- **C2 (fail có chủ đích):** đổi `expected_status` của AI-01 trong `mini-login.data.json` từ `200` thành `999` → push → workflow đỏ → chụp `ci-fail.png`.
- **C3 (khôi phục):** trả lại `200`, push lần cuối → pipeline xanh trở lại.

---

## Bước 6 — Postman features đã dùng

| Feature | Đã dùng? | Ghi chú |
|---|---|---|
| Collections | Có | Collection `Mini API Testing - POST /api/login (23127438)` chứa request data-driven duy nhất. |
| Environment variables | Có | `baseUrl`, `studentId` trong `mini-local.postman_environment.json`. |
| Collection variables | Có | `maxResponseMs = 2000` — ngưỡng response time dùng trong test script. |
| Pre-request scripts | Có | Upsert header `X-Student-Id` từ `studentId` và build request body động từ iteration data. |
| Test scripts (assertions) | Có | 5–6 assertion/iteration: status, Content-Type, response time, schema fields, JWT, error message. |
| Data-driven runs (Collection Runner + data file) | Có | 5 iteration từ `mini-login.data.json` với `expected_status`/`expected_fields` điều khiển assertion. |
| Newman CLI | Có | Chạy local và trong GitHub Actions với reporter `cli,json`. |
| Monitors | Không | Không cần lịch chạy định kỳ; CI đã đảm nhiệm việc chạy tự động khi push. |
| Mock servers | Không | SUT thật chạy local nên không cần mock. |
| Workspaces | Không | Bài làm cá nhân, dùng workspace mặc định. |

**Tổng: 7/10 feature** (đạt yêu cầu tối thiểu 6).

---

## Phát hiện đáng chú ý về SUT (bonus)

1. **Lộ mật khẩu plaintext:** `POST /api/login` (200) trả nguyên row `user` gồm `password`. Mật khẩu cũng được lưu plaintext trong DB (không hash).
2. **Sai bước nhảy lockout:** mỗi lần sai mật khẩu cộng 2 vào `login_attempts` (comment/hành vi mong đợi thường là +1), nên chỉ cần 2 lần sai là tài khoản bị khóa 3 phút.
3. **Vi phạm chuẩn REST:** thiếu field bắt buộc trả 401 thay vì 400 — không phân biệt được "request sai định dạng" với "sai thông tin đăng nhập".
4. **Thiếu field cũng tăng lockout counter:** request thiếu `password` với email tồn tại vẫn bị tính là một lần đăng nhập sai.
