# 03 — Kế hoạch Thực thi HW06 (dành cho Codex)

> **Đọc trước khi bắt đầu:** [`01-requirements-analysis.md`](01-requirements-analysis.md) (yêu cầu R-01…R-16) và [`02-sut-defect-catalog.md`](02-sut-defect-catalog.md) (oracle của SUT).
>
> **Cách dùng:** thực hiện tuần tự theo Phase. Mỗi task có `ID`, `Owner`, `Input`, `Output`, `DoD` (Definition of Done) và `Commit`. **Không gộp task vào chung một commit** — yêu cầu R-13 chấm điểm dựa trên commit log.

---

## 0. Quy ước chung (bắt buộc tuân thủ)

| Quy ước | Giá trị |
| :--- | :--- |
| Branch làm việc | `HW6-Khoa` (đã checkout sẵn) |
| MSSV | `23127207` |
| Thư mục bài nộp | `hw06/` (ở gốc repo) |
| Thư mục tài liệu phân tích | `docs/hw06/` (chính là thư mục này) |
| Mã test case | `TC-API-LOGIN-###`, `TC-API-CHECKOUT-###`, `TC-API-ORDER-STATUS-###` |
| Mã bug | Dùng `D-*` của `02-sut-defect-catalog.md`, ánh xạ sang số issue GitHub khi tạo |
| Base URL | `http://localhost:3000` |
| Header bắt buộc | `X-Student-Id: 23127207` trên **mọi** request |
| Ngôn ngữ tài liệu | Tiếng Việt (thống nhất với artifact sẵn có trong repo) |

### 0.1 Ba luật cứng

1. **Không bịa bằng chứng.** Số liệu Newman, link CI, số issue GitHub, screenshot — chỉ được ghi sau khi **đã chạy/đã tạo thật**. Chỗ chưa có, để nguyên `<!-- TODO(HUMAN): ... -->` và ghi vào `04-deliverables-checklist.md`.
2. **Log AI ngay tại chỗ.** Sau **mỗi** lần dùng AI để sinh nội dung, append ngay một entry vào `hw06/report/ai-audit-report.md` theo template ở §10.2. Không ghi bù cuối buổi.
3. **Không đụng vào 3 hạng mục HUMAN-only** (R-14, R-15 screenshot, R-16 sơ đồ) — xem bảng ở `README.md` §3.

### 0.2 Ghi chú quan trọng về môi trường

- 🔴 **Backend reset DB mỗi lần khởi động** (`backend/database.js:117`). Mọi test phải **tự tạo tiền đề** (tự đăng ký user, tự tạo order) — **cấm** hard-code `orderId`/`userId`.
- Tài khoản seed: `admin@eshop.com` / `Admin123!` (role admin, id 1), `test@eshop.com` / `Test1234!` (role user, id 2).
- Giỏ hàng nằm trong RAM (`server.js:14`), mất khi restart.
- Khi test lockout (API-1) sẽ khoá tài khoản **180 giây** → **luôn dùng user dùng-một-lần** (`hw06_login_{{$timestamp}}@test.local`) cho nhóm test này, tuyệt đối không khoá `test@eshop.com` vì các phase sau còn cần.

---

## 1. Cấu trúc thư mục đích

```
hw06/
├── README.md                                  # bảng tự chấm + test summary (R: mục 14 đề bài)
├── api-01-login/
│   ├── 01-ai-generated.md                     # output thô của AI (R-01)
│   ├── 02-audit.md                            # bảng VALID/INVALID/INCOMPLETE (R-02)
│   ├── 03-extended.md                         # ≥5 case tự thêm + "vì sao AI bỏ sót" (R-03)
│   └── test-cases.md                          # bảng test case CHỐT (nguồn cho Postman + Excel)
├── api-02-checkout/                           # cùng 4 file như trên
├── api-03-admin-order-status/                 # cùng 4 file như trên
├── postman/
│   ├── EShop-HW06-23127207.postman_collection.json
│   ├── EShop-HW06-local.postman_environment.json
│   ├── data/
│   │   ├── login-partitions.data.json
│   │   ├── checkout-partitions.data.json
│   │   └── order-status-matrix.data.json      # 25 dòng ma trận 5×5
│   └── postman-features.md                    # R-06
├── newman/
│   ├── run-newman.sh                          # script chạy thật
│   ├── run-newman.ps1
│   └── reports/                               # HTML/JSON do Newman sinh ra (R-04)
├── test-generator/
│   ├── design.md                              # pseudocode + quyết định thiết kế (R-08, R-09)
│   ├── diagram.png                            # 🧑 HUMAN tự vẽ (R-09, R-16)
│   └── generator.py                           # hiện thực tham chiếu
├── excel/
│   ├── test-cases.csv                         # + .xlsx
│   └── test-summary.csv                       # + .xlsx
├── evidence/
│   └── screenshots/                           # 🧑 HUMAN chụp
├── openapi/
│   └── eshop.openapi.yaml                     # tuỳ chọn
└── report/
    ├── main-report.md                         # báo cáo chính (+ PDF)
    ├── bug-report.md                          # R-05
    ├── cicd-report.md                         # R-07
    ├── ai-audit-report.md                     # R-11
    ├── ai-critique.md                         # 🧑 HUMAN viết (R-12)
    └── git-commit-log.txt                     # R-13

.agents/skills/api_test_generator/             # Agent Skill (R-10)
├── SKILL.md
├── scripts/generate_api_tests.py
└── examples/login.endpoint.json

.github/workflows/hw06-newman-api-test.yml     # CI/CD (R-07)
```

Ngoài ra, đồng bộ với quy ước `Rule.pdf` (test case là file Markdown trong `tests/`):

```
tests/test-cases/api-login/TC-API-LOGIN-###.md
tests/test-cases/api-checkout/TC-API-CHECKOUT-###.md
tests/test-cases/api-order-status/TC-API-ORDER-STATUS-###.md
tests/test-runs/hw06-api-test-run.md
tests/test-summary/traceability-matrix.md      # CẬP NHẬT file sẵn có, không tạo mới
```

> **Quyết định thiết kế:** bảng test case đầy đủ nằm ở `hw06/api-0X-*/test-cases.md` (dạng bảng, tiện xuất Excel); `tests/test-cases/` chứa file `.md` riêng lẻ theo template `Rule.pdf` §H.5. Để tránh trùng lặp công sức, **chỉ sinh file `.md` riêng lẻ cho các test case đã FAIL (có bug)** cộng thêm 5 case đại diện mỗi API — và ghi rõ quy ước này trong `main-report.md`.

---

## 2. PHASE 0 — Chuẩn bị (T-0.x)

| ID | Owner | Việc | Output | DoD |
| :--- | :-: | :--- | :--- | :--- |
| **T-0.1** | 🤖 | Tạo cây thư mục `hw06/` như §1 (kèm `.gitkeep` cho thư mục rỗng) | Cây thư mục | `git status` thấy đủ thư mục |
| **T-0.2** | 🤖 | Cài dependency backend, khởi động server, kiểm tra health `GET /api/products` trả `200` + 5 sản phẩm | Server chạy ở `:3000` | `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/products` → `200` |
| **T-0.3** | 🤖 | Sửa `.github/ISSUE_TEMPLATE/bug_report.md` — file hiện **lặp nội dung 3 lần** và có 2 khối front-matter chồng nhau ⇒ GitHub không parse đúng. Giữ **đúng 1** khối front-matter + 1 thân template theo `Rule.pdf` §H.8 | File template sạch | Mở file thấy đúng 1 block `---…---` ở đầu |
| **T-0.4** | 🤖 | Quyết định về `.agents/skills/domain_and_boundary_testing/` — hiện đang bị **xoá ở working tree** nhưng vẫn còn trong index. Khôi phục bằng `git restore` (skill của HW trước, nên giữ làm tiền lệ) | Thư mục được khôi phục | `git status` không còn dòng ` D .agents/...` |
| **T-0.5** | 🤖 | Cài `newman` + `newman-reporter-htmlextra` ở phạm vi dự án: tạo `hw06/package.json` với devDependencies và script `test:api` | `hw06/package.json`, lockfile | `npx newman -v` chạy được |
| **T-0.6** | 🤖 | Tạo khung rỗng `hw06/report/ai-audit-report.md` với câu khai báo bắt buộc *"I use AI tools for the following tasks,"* + bảng công cụ đã dùng | File khung | Có đủ heading cho các entry sẽ append |

**Commit:** `chore(hw06): khởi tạo cấu trúc thư mục và môi trường cho HW06 API Testing`

---

## 3. PHASE 1 — API-1 · `POST /api/login` (T-1.x)

### 3.1 T-1.1 — Generate với AI (R-01) 🤖

**Bắt buộc dùng chuỗi 5 prompt tách bạch** (P-01 cấm 1 prompt tổng). Mỗi prompt là **một lần tương tác riêng**, log riêng vào AI Audit.

| Bước | Prompt (tóm tắt — nội dung đầy đủ xem §10.1) | Sản phẩm |
| :-: | :--- | :--- |
| P1 | Phân tích endpoint: liệt kê **mọi** tham số đầu vào (body, header), kiểu, ràng buộc theo `api_specification.md` + FR-02; liệt kê **trạng thái hệ thống** liên quan (`login_attempts`, `locked_until`) | Bảng tham số & trạng thái |
| P2 | Từ bảng P1, sinh test case **domain partition** cho từng tham số (valid/invalid partition + biên) | ~16 case |
| P3 | Từ mô hình trạng thái khoá tài khoản, sinh test case **state transition** (chưa khoá → đếm → khoá → hết hạn → reset) | ~8 case |
| P4 | Từ SEC-01…SEC-07, sinh test case **security** cho endpoint này | ~8 case |
| P5 | Từ hình dạng response trong `api_specification.md`, sinh test case **schema validation** | ~4 case |

- **Mục tiêu số lượng:** **≥ 36 test case**.
- **Output:** `hw06/api-01-login/01-ai-generated.md` — bảng gồm: `TC ID | Nhóm | Tiêu đề | Precondition | Test data | Expected result (theo đặc tả)`.
- ⚠️ Ghi **nguyên văn** output AI, **chưa sửa gì**. Bước sửa nằm ở T-1.2.

**DoD:** đếm được ≥ 36 dòng; đủ 4 nhóm; 5 entry đã có trong `ai-audit-report.md`.
**Commit:** `test(api-01): sinh 36 test case cho POST /api/login bằng chuỗi prompt 5 bước`

---

### 3.2 T-1.2 — Audit (R-02) 🤖 + 🧑

Đối chiếu **từng** case với `02-sut-defect-catalog.md` §1.

**Output:** `hw06/api-01-login/02-audit.md` — bảng `TC ID | Nhãn | Lý do | Hành động sửa`.

**Tiêu chí gán nhãn (áp dụng thống nhất cả 3 API):**

| Nhãn | Khi nào dùng |
| :--- | :--- |
| **VALID** | Precondition, test data và expected result đều đúng theo đặc tả; chạy được ngay |
| **INVALID** | Expected result **sai** (thường vì AI mô tả *hành vi hiện tại của SUT* thay vì *hành vi đúng theo đặc tả*, hoặc ngược lại — bịa ra ràng buộc mà đặc tả không có) |
| **INCOMPLETE** | Ý tưởng đúng nhưng thiếu precondition / thiếu test data cụ thể / expected result mơ hồ ("hệ thống báo lỗi" mà không nói mã lỗi, không nói response shape) |

**Lỗi AI thường mắc ở API này — soi kỹ:**

1. Viết expected result cho lockout là *"khoá sau 3 lần sai, 30 giây"* → **đúng theo đặc tả** ⇒ VALID (và test này sẽ **FAIL** khi chạy, đó chính là bug D-LOGIN-01/02 — **đừng sửa expected result cho khớp SUT**).
2. Viết case SQL injection với expected *"đăng nhập bị bypass"* → **INVALID**, vì `server.js:35` dùng parameterized query. Expected đúng là `401` + không bypass.
3. Bỏ sót hoàn toàn việc kiểm tra **response có chứa `password`** (D-LOGIN-03) → phần này thuộc T-1.3.
4. Bịa ràng buộc "mật khẩu tối thiểu 8 ký tự" cho endpoint **login** → INVALID (ràng buộc đó thuộc FR-01 register, login không validate độ mạnh).
5. Bịa mã lỗi `429 Too Many Requests` → INVALID, SUT dùng `403`.

**🧑 HUMAN checkpoint:** sinh viên phải đọc lại bảng audit và ký xác nhận ở cuối file (`Reviewed by: Khoa – <ngày>`). R-02 quy trách nhiệm cho **người**, không cho AI.

**DoD:** 100% case của T-1.1 có nhãn + lý do; mọi case INVALID/INCOMPLETE có cột "Hành động sửa" đã thực hiện.
**Commit:** `test(api-01): audit test case AI sinh cho login (VALID/INVALID/INCOMPLETE) và sửa lại`

---

### 3.3 T-1.3 — Extend (R-03) 🤖

Thêm **≥ 6 test case tự thiết kế** mà AI bỏ sót. Gợi ý bám sát `02-sut-defect-catalog.md` §1.2:

| TC | Nội dung | Bug nhắm tới | Vì sao AI bỏ sót (mẫu lập luận) |
| :--- | :--- | :--- | :--- |
| E-1 | Sai mật khẩu **đúng 2 lần** rồi thử đăng nhập **đúng** → phải vào được (spec: chỉ khoá từ lần 3) | D-LOGIN-01 | AI sinh case theo *mô tả* đặc tả ("khoá sau 3 lần") mà không thiết kế case **đo bước nhảy của bộ đếm**; nó không có mô hình về "counter increment" như một biến quan sát được |
| E-2 | Đo **thời lượng khoá thực tế**: chờ 35 s sau khi khoá rồi đăng nhập đúng → phải vào được | D-LOGIN-02 | Case phụ thuộc thời gian thực; AI hiếm khi sinh test case có yếu tố *đợi* vì không mô phỏng được trục thời gian |
| E-3 | Assert response **không** chứa các field nhạy cảm: `password`, `reset_token`, `login_attempts`, `locked_until` | D-LOGIN-03 | AI kiểm tra schema theo hướng *"có đủ field cần"* (positive) chứ không theo hướng *"không được thừa field cấm"* (negative schema) |
| E-4 | Giải mã JWT, assert payload **có `exp`** và `exp - iat ≤ 24h` | D-LOGIN-05 | `api_specification.md` chỉ nói "trả về chuỗi JWT token"; AI không tự mở token ra soi claim vì spec không mô tả cấu trúc payload |
| E-5 | Sau khi hết hạn khoá, sai **1 lần** → phải **không** bị khoá lại ngay | D-LOGIN-06 | Đây là lỗi ở **đường quay lui** của state machine; AI mô hình hoá state machine theo chiều tiến, bỏ qua trạng thái tồn dư (residual state) |
| E-6 | Tự ký JWT bằng secret hard-code trong `server.js:9` với payload `{id:1, role:"admin"}` → gọi API admin | D-LOGIN-05 | AI chỉ đọc `api_specification.md`, **không đọc mã nguồn**, nên không biết secret bị lộ — giới hạn về **phạm vi ngữ cảnh được cấp** |

**Output:** `hw06/api-01-login/03-extended.md` — bảng test case + cột **"Vì sao AI bỏ sót"** phân loại theo 3 nguyên nhân đề bài nêu: `chất lượng prompt` / `giới hạn model` / `đặc thù API`.

**DoD:** ≥ 6 case; mỗi case có lý do cụ thể (không được viết chung chung kiểu "AI không đủ thông minh").
**Commit:** `test(api-01): bổ sung 6 test case AI bỏ sót cho login kèm phân tích nguyên nhân`

---

### 3.4 T-1.4 — Chốt danh sách test case 🤖

Gộp T-1.1 (đã sửa) + T-1.3 → `hw06/api-01-login/test-cases.md`.

**Cột bắt buộc:** `TC ID | Requirement | Nhóm (Partition/State/Security/Schema) | Kỹ thuật (EP/BVA/State-transition/…) | Precondition | Method+Endpoint | Test data | Expected (status + body) | Nguồn (AI/Human) | Kỳ vọng chạy (PASS/FAIL) | Bug ID`

> Cột **"Kỳ vọng chạy"** là điểm mấu chốt: case assert đúng đặc tả nhưng SUT có bug ⇒ ghi `FAIL (D-LOGIN-01)`. Nhờ cột này mới cấu hình được chế độ `spec_strict` ở Phase 5 và giải thích được kết quả Newman.

**DoD:** tổng ≥ 42 case; cột "Kỳ vọng chạy" điền đủ.
**Commit:** `docs(api-01): chốt bảng 42 test case cho POST /api/login`

---

## 4. PHASE 2 — API-2 · `POST /api/checkout` (T-2.x)

Lặp lại đúng cấu trúc T-1.1 → T-1.4, thay nội dung theo `02-sut-defect-catalog.md` §2.

| ID | Việc | Output | Commit |
| :--- | :--- | :--- | :--- |
| **T-2.1** | Generate — chuỗi 5 prompt, ≥ 36 case. **Bối cảnh cần đưa vào prompt:** FR-08 (backend phải tự tính lại tổng tiền, phải xoá giỏ sau thanh toán), FR-10 (đơn mới = `pending`), luồng `POST /api/cart` → `POST /api/checkout` → `GET /api/orders/my-orders` | `api-02-checkout/01-ai-generated.md` | `test(api-02): sinh 36 test case cho POST /api/checkout bằng chuỗi prompt 5 bước` |
| **T-2.2** | Audit + 🧑 checkpoint | `api-02-checkout/02-audit.md` | `test(api-02): audit test case AI sinh cho checkout và sửa lại` |
| **T-2.3** | Extend ≥ 6 case | `api-02-checkout/03-extended.md` | `test(api-02): bổ sung 6 test case AI bỏ sót cho checkout kèm phân tích nguyên nhân` |
| **T-2.4** | Chốt bảng | `api-02-checkout/test-cases.md` | `docs(api-02): chốt bảng 42 test case cho POST /api/checkout` |

### Gợi ý phân vùng cho T-2.1 (dùng để kiểm tra AI có phủ đủ không)

- `total_amount`: hợp lệ · `0` · âm · chuỗi `"200000"` · `null` · thiếu trường · số thực · rất lớn (`9e18`) · ký hiệu khoa học · `NaN` · mảng/đối tượng.
- `shipping_address`: hợp lệ · rỗng · thiếu · rất dài (>1000 ký tự) · payload XSS · payload SQLi · ký tự Unicode/tiếng Việt có dấu.
- Xác thực: không token · token sai chữ ký · token hết hạn · header sai định dạng (`Bearer` thiếu) · token của user khác.
- Luồng/trạng thái: giỏ rỗng vẫn checkout được · giỏ không bị xoá sau checkout · đơn mới phải là `pending` · gửi 2 lần tạo 2 đơn.
- Schema: `orderId` phải là **số nguyên**; `message` là chuỗi; `Content-Type: application/json`; không thừa field.

### 6 case Extend gợi ý cho T-2.3

| TC | Nội dung | Bug | Vì sao AI bỏ sót |
| :--- | :--- | :--- | :--- |
| E-1 | Thêm sản phẩm 30 triệu vào giỏ, checkout với `total_amount: 1` → assert đơn tạo ra phải có tổng đúng **theo giỏ**, không theo body | D-CHK-01 | AI test **từng endpoint độc lập**, không dựng **bất biến xuyên endpoint** (giỏ ↔ đơn) |
| E-2 | Checkout `total_amount: -500000` → assert phải `400` | D-CHK-02 | Spec API không ghi ràng buộc dương cho `total_amount`; AI bám `api_specification.md` mà không suy ra từ FR-08 |
| E-3 | Checkout xong gọi `GET /api/cart` → assert giỏ **rỗng** | D-CHK-03 | Đây là **hậu điều kiện (post-condition)** ở endpoint **khác**; AI chỉ assert response của chính request đó |
| E-4 | Giỏ rỗng → checkout → assert `400` | D-CHK-04 | Không có mô tả tường minh trong spec API ⇒ cần suy luận nghiệp vụ |
| E-5 | User A checkout → user B (và cả **request không token**) gọi `GET /api/orders/:id` của A → assert `401/403` | D-CHK-07 | **IDOR ở endpoint kề bên** — ngoài phạm vi endpoint được hỏi trong prompt |
| E-6 | `shipping_address` = `<img src=x onerror=alert(1)>` → assert bị từ chối hoặc được escape khi đọc lại | D-CHK-05 | AI xếp XSS vào nhóm "lỗi frontend", ít khi assert ở tầng API |

---

## 5. PHASE 3 — API-3 · `PUT /api/admin/orders/:id/status` (T-3.x)

| ID | Việc | Output | Commit |
| :--- | :--- | :--- | :--- |
| **T-3.1** | Generate — chuỗi 5 prompt, ≥ 38 case. **Bắt buộc** yêu cầu AI sinh **đủ ma trận 5×5 = 25 case** chuyển trạng thái | `api-03-admin-order-status/01-ai-generated.md` | `test(api-03): sinh 38 test case cho PUT /api/admin/orders/:id/status bằng chuỗi prompt 5 bước` |
| **T-3.2** | Audit + 🧑 checkpoint | `.../02-audit.md` | `test(api-03): audit test case AI sinh cho admin order status và sửa lại` |
| **T-3.3** | Extend ≥ 6 case | `.../03-extended.md` | `test(api-03): bổ sung 6 test case AI bỏ sót cho admin order status kèm phân tích nguyên nhân` |
| **T-3.4** | Chốt bảng | `.../test-cases.md` | `docs(api-03): chốt bảng 44 test case cho PUT /api/admin/orders/:id/status` |

### Ma trận 25 case bắt buộc

Lấy nguyên bảng ở `02-sut-defect-catalog.md` §3.2. Mỗi ô = 1 test case:
`TC-API-ORDER-STATUS-001` … `-025`, đặt tên theo `<from>_to_<to>`.
Cột **Expected** lấy theo **cột "Đặc tả"**, cột **Kỳ vọng chạy** lấy theo chênh lệch với **cột "Hiện thực"**:

- 23/25 ô → `PASS`
- ô `shipping → canceled` → `FAIL (D-ADM-03)`
- ô `canceled → delivered` → `FAIL (D-ADM-02)`

### 6 case Extend gợi ý cho T-3.3

| TC | Nội dung | Bug | Vì sao AI bỏ sót |
| :--- | :--- | :--- | :--- |
| E-1 | Dùng token **user thường** gọi endpoint admin → assert `403` | D-ADM-01 | AI mặc định *"endpoint tên `/admin/` thì chắc chắn đã chặn role"* — **thiên lệch giả định** (assumption bias), nó test *chức năng* chứ không test *giả định về chức năng* |
| E-2 | User A đổi trạng thái đơn của **user B** → assert `403` | D-ADM-01 | Cần dựng **2 danh tính** trong 1 kịch bản; AI sinh case đơn danh tính |
| E-3 | `canceled → delivered` rồi kiểm tra **doanh thu Dashboard** (FR-13 chỉ tính `delivered`) tăng sai | D-ADM-02 | **Tác động dây chuyền sang FR khác**; AI không mô hình hoá liên đới giữa các FR |
| E-4 | Admin huỷ đơn ở `shipping` → assert phải thành công theo FR-10 | D-ADM-03 | Đặc tả diễn đạt gián tiếp ("chỉ Admin mới thao tác được") — cần **suy luận từ ngôn ngữ tự nhiên mơ hồ** |
| E-5 | User gọi `PUT /api/orders/:id/cancel` khi đơn ở `shipping` → assert `400` | D-ADM-08 | Endpoint **khác** cùng state machine — ngoài phạm vi prompt |
| E-6 | Gửi `status` là mảng `["delivered"]` / object / chuỗi rỗng / thiếu trường → assert `400` với thông báo *phân biệt được* "giá trị không hợp lệ" vs "chuyển trạng thái không hợp lệ" | D-ADM-06 | AI test giá trị enum sai dạng chuỗi, hiếm khi test **sai kiểu dữ liệu (type confusion)** |

---

## 6. PHASE 4 — Postman collection (T-4.x)

### 6.1 T-4.1 — Environment 🤖

`hw06/postman/EShop-HW06-local.postman_environment.json`

| Biến | Giá trị khởi tạo | Ghi chú |
| :--- | :--- | :--- |
| `base_url` | `http://localhost:3000` | R-15 |
| `student_id` | `23127207` | R-14 |
| `admin_email` / `admin_password` | `admin@eshop.com` / `Admin123!` | seed |
| `user_email` / `user_password` | `test@eshop.com` / `Test1234!` | seed |
| `userToken`, `adminToken`, `userId`, `orderId`, `lockUser` | *(rỗng — điền lúc chạy)* | biến động |
| `spec_strict` | `off` | `off` \| `canary` \| `full` — xem §7.2 |

### 6.2 T-4.2 — Pre-request script cấp Collection 🤖 ⚠️ (R-14)

Đặt ở **cấp collection**, tuyệt đối không đặt lẻ từng request:

```js
// Bắt buộc: gắn X-Student-Id cho MỌI request (Requirements mục 11)
const sid = pm.environment.get("student_id") || "23127207";
pm.request.headers.upsert({ key: "X-Student-Id", value: sid });

// Log ra Postman Console để chụp màn hình làm bằng chứng
console.log("[HW06] " + pm.info.requestName
          + " | X-Student-Id: " + sid
          + " | " + pm.request.method + " " + pm.request.url.toString());

// Helper dùng chung cho mọi test script
pm.collectionVariables.set("helpers", `
  const MODE = (pm.environment.get("spec_strict") || "off").toLowerCase();
  const CANARY = ["TC-API-LOGIN-013"];
  // specTest: chỉ chạy assertion phản ánh ĐÚNG ĐẶC TẢ (sẽ fail vì SUT có bug)
  function specTest(id, name, fn) {
    if (MODE === "full" || (MODE === "canary" && CANARY.indexOf(id) !== -1)) {
      pm.test("[SPEC] " + id + " - " + name, fn);
    }
  }
  function hasNoSecretFields(obj) {
    return ["password","reset_token","login_attempts","locked_until"]
      .every(k => !(k in (obj || {})));
  }
`);
```

Trong test script của mỗi request, dòng đầu tiên: `eval(pm.collectionVariables.get("helpers"));`

### 6.3 T-4.3 — Cấu trúc Collection 🤖

```
EShop HW06 - API Testing - 23127207
├── 00 - Setup
│   ├── Health check                        GET  /api/products
│   ├── Register disposable user            POST /api/register   → lockUser = hw06_{{$timestamp}}@test.local
│   ├── Login user                          POST /api/login      → userToken, userId
│   └── Login admin                         POST /api/login      → adminToken
├── API-1 · POST /api/login
│   ├── 1.1 Domain partitions  [DDT: login-partitions.data.json]
│   ├── 1.2 State transitions  (lockout: sai 1 → sai 2 → sai 3 → khoá → chờ → reset)
│   ├── 1.3 Security           (SQLi, no-enumeration, JWT claims, token tự ký, rò rỉ field)
│   └── 1.4 Schema validation
├── API-2 · POST /api/checkout
│   ├── 2.1 Domain partitions  [DDT: checkout-partitions.data.json]
│   ├── 2.2 Flow & post-conditions  (cart → checkout → cart rỗng?, đơn = pending)
│   ├── 2.3 Security           (auth ma trận, IDOR GET /api/orders/:id, XSS address)
│   └── 2.4 Schema validation
├── API-3 · PUT /api/admin/orders/:id/status
│   ├── 3.1 Transition matrix  [DDT: order-status-matrix.data.json — 25 dòng]
│   ├── 3.2 Domain partitions  (status enum, kiểu dữ liệu, :id không tồn tại/âm/chuỗi)
│   ├── 3.3 Security           (role escalation, cross-user, no token, token hỏng)
│   └── 3.4 Schema validation
└── 99 - Teardown  (ghi tổng kết ra console)
```

**Yêu cầu kỹ thuật:**

- Request trong folder DDT phải **tự bỏ qua** khi chạy không có data file:
  ```js
  // Pre-request của folder DDT
  if (!pm.iterationData.get("tc_id")) { pm.execution.skipRequest(); }
  ```
  *(Nếu phiên bản Newman không hỗ trợ `pm.execution.skipRequest`, thay bằng cách chỉ chạy folder DDT ở lần gọi Newman riêng — ghi rõ trong `cicd-report.md`.)*
- Mọi `pm.test` phải đặt tên bắt đầu bằng **mã test case**: `pm.test("TC-API-LOGIN-004 - Email sai định dạng trả 401", …)` → nhờ đó ánh xạ 1-1 từ Newman report về bảng test case.
- Test case phản ánh **đúng đặc tả nhưng SUT vi phạm** ⇒ dùng `specTest(id, name, fn)` thay cho `pm.test`.

**Commit:** `feat(postman): xây collection + environment cho 3 API kèm pre-request X-Student-Id`

### 6.4 T-4.4 — Data files 🤖

| File | Số dòng | Cột |
| :--- | :-: | :--- |
| `login-partitions.data.json` | ~16 | `tc_id, email, password, expected_status, expected_error, note` |
| `checkout-partitions.data.json` | ~18 | `tc_id, total_amount, shipping_address, token_kind, expected_status, note` |
| `order-status-matrix.data.json` | 25 | `tc_id, from_status, to_status, expected_allowed, expected_status, note` |

> Với `order-status-matrix.data.json`, mỗi iteration phải **tự dựng đơn hàng ở trạng thái `from_status`** (checkout tạo `pending`, rồi lần lượt chuyển tới `from_status` qua các bước hợp lệ) trước khi thử chuyển sang `to_status`. Viết logic dựng tiền đề này trong pre-request của request đó.

**Commit:** `feat(postman): thêm 3 data file cho data-driven run (16+18+25 bộ dữ liệu)`

### 6.5 T-4.5 — Danh sách tính năng Postman (R-06) 🤖 + 🧑

`hw06/postman/postman-features.md` — bảng `Tính năng | Đã dùng ở đâu | Bằng chứng`:

| Tính năng | Nơi dùng | Owner |
| :--- | :--- | :-: |
| Collection | `EShop-HW06-23127207.postman_collection.json` | 🤖 |
| Folders phân tầng | 4 folder/API theo nhóm test | 🤖 |
| Environment | `EShop-HW06-local.postman_environment.json` | 🤖 |
| Environment / Collection variables | `base_url`, `student_id`, `userToken`, `orderId`, `spec_strict` | 🤖 |
| Dynamic variables | `{{$timestamp}}`, `{{$randomEmail}}`, `{{$guid}}` | 🤖 |
| Pre-request scripts | cấp collection (X-Student-Id) + cấp folder (dựng tiền đề) | 🤖 |
| Test scripts + Chai assertions | mọi request | 🤖 |
| Data-driven (Collection Runner + data file) | 3 file DDT | 🤖 |
| Variable chaining giữa request | `userToken` → `orderId` → transition | 🤖 |
| `pm.response.to.have.jsonSchema` | folder Schema validation | 🤖 |
| Newman CLI + reporter `htmlextra` | `hw06/newman/` | 🤖 |
| Newman trong CI (GitHub Actions) | `.github/workflows/hw06-newman-api-test.yml` | 🤖 |
| **Workspace** | Tạo workspace *"HCMUS – HW06 API Testing"* trên Postman, import collection | 🧑 |
| **Mock server** | Tạo mock từ collection, chụp màn hình | 🧑 |
| **Monitor** | Tạo monitor chạy collection theo lịch, chụp màn hình | 🧑 |
| **Postman Console** | Screenshot chứng minh header `X-Student-Id` (R-14) | 🧑 |

**Commit:** `docs(postman): liệt kê các tính năng Postman đã sử dụng`

---

## 7. PHASE 5 — Thực thi Newman (T-5.x) — R-04

### 7.1 T-5.1 — Script chạy 🤖

`hw06/newman/run-newman.sh` (và bản `.ps1` tương đương) — nhận tham số chế độ:

```bash
#!/usr/bin/env bash
# Cách dùng: ./run-newman.sh [off|canary|full]
set -u
MODE="${1:-full}"
HERE="$(cd "$(dirname "$0")" && pwd)"
COL="$HERE/../postman/EShop-HW06-23127207.postman_collection.json"
ENV="$HERE/../postman/EShop-HW06-local.postman_environment.json"
DATA="$HERE/../postman/data"
OUT="$HERE/reports"
mkdir -p "$OUT"

run() { # run <tên> <tham số thêm...>
  local name="$1"; shift
  npx newman run "$COL" -e "$ENV" \
    --env-var "spec_strict=$MODE" \
    -r cli,htmlextra,json \
    --reporter-htmlextra-export "$OUT/$name.html" \
    --reporter-json-export      "$OUT/$name.json" \
    "$@"
}

run "00-full-suite"
run "01-ddt-login"        --folder "1.1 Domain partitions" -d "$DATA/login-partitions.data.json"
run "02-ddt-checkout"     --folder "2.1 Domain partitions" -d "$DATA/checkout-partitions.data.json"
run "03-ddt-order-status" --folder "3.1 Transition matrix" -d "$DATA/order-status-matrix.data.json"
```

> ⚠️ **Trước mỗi lần chạy phải restart backend** để DB về trạng thái sạch (xem §0.2). Ghi bước này vào đầu script.

### 7.2 Ba chế độ chạy — thiết kế then chốt cho R-07

| Chế độ | `spec_strict` | Assertion nào chạy | Dùng cho |
| :--- | :--- | :--- | :--- |
| `off` | `off` | Chỉ assertion mô tả hành vi **đã kiểm chứng là đúng** | **Commit CI xanh** (R-07 "all passing") |
| `canary` | `canary` | Như `off` **+ đúng 1** assertion `TC-API-LOGIN-013` (bug D-LOGIN-01) | **Commit CI đỏ** (R-07 "one test case failing") |
| `full` | `full` | Toàn bộ, gồm mọi assertion theo đặc tả | **Báo cáo bằng chứng bug** nộp bài (R-04, R-05) |

> Cách làm này **trung thực**: không có test nào bị chế ra để fail. Lần chạy đỏ fail vì một **bug thật** (bộ đếm tăng +2), và chính lần chạy đó là bằng chứng gắn vào issue GitHub của D-LOGIN-01.

### 7.3 T-5.2 — Chạy thật & lưu báo cáo 🤖

1. Restart backend → chạy `./run-newman.sh full` → lưu vào `hw06/newman/reports/`.
2. Trích số liệu từ file `.json` → điền bảng tổng kết ở `hw06/README.md` và `tests/test-runs/hw06-api-test-run.md` (định dạng theo `Rule.pdf` §H.6: `Test Case ID | Module | Tester | Result | Related Bug | Note`).
3. **Không sửa tay** file HTML/JSON do Newman sinh ra.

**DoD:** tồn tại ≥ 4 file HTML + 4 file JSON; hostname trong report là `localhost`; tổng số assertion khớp số test case đã chốt.
**Commit:** `test(newman): chạy toàn bộ test suite và lưu Newman HTML/JSON report`

### 7.4 T-5.3 — 🧑 HUMAN: screenshot bằng chứng

- Mở Postman → Runner → chạy collection → mở **Console** → chụp màn hình thấy rõ dòng `[HW06] … | X-Student-Id: 23127207` → lưu `hw06/evidence/screenshots/01-x-student-id-console.png` **(R-14 — bắt buộc)**.
- Chụp màn hình Newman CLI output → `02-newman-cli-run.png` **(R-15)**.
- Chụp Postman Workspace / Mock server / Monitor → `03-*.png` (R-06).

---

## 8. PHASE 6 — CI/CD (T-6.x) — R-07

### 8.1 T-6.1 — Workflow 🤖

`.github/workflows/hw06-newman-api-test.yml`:

```yaml
name: HW06 - Newman API Tests

on:
  push:
    branches: ['HW6-Khoa']
  pull_request:
    branches: ['main']
  workflow_dispatch:

env:
  SPEC_STRICT: 'off'          # ← commit đỏ đổi thành 'canary'

jobs:
  api-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }

      - name: Install backend deps & start server
        run: |
          cd backend && npm install
          node server.js &
          for i in $(seq 1 30); do
            curl -sf http://localhost:3000/api/products && break || sleep 1
          done

      - name: Install Newman
        run: npm install -g newman newman-reporter-htmlextra

      - name: Run API tests (X-Student-Id 23127207)
        run: |
          newman run hw06/postman/EShop-HW06-23127207.postman_collection.json \
            -e hw06/postman/EShop-HW06-local.postman_environment.json \
            --env-var "spec_strict=${{ env.SPEC_STRICT }}" \
            -r cli,htmlextra,json \
            --reporter-htmlextra-export newman-ci-report.html \
            --reporter-json-export      newman-ci-report.json

      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: newman-report-${{ github.sha }}
          path: newman-ci-*.
```

> Tham khảo workflow của nhóm ở `origin/HW6-Thinh:.github/workflows/newman-api-test.yml` để giữ phong cách nhất quán, nhưng **không sao chép nguyên văn** (R: mục 17 — cấm sao chép giữa sinh viên).

**Commit:** `ci(hw06): thêm GitHub Actions chạy Newman cho bộ test API`

### 8.2 T-6.2 — Hai commit mẫu 🤖 + 🧑

| Bước | Việc | Kết quả mong đợi |
| :-: | :--- | :--- |
| 1 | Push commit với `SPEC_STRICT: 'off'` | ✅ Pipeline **xanh** — toàn bộ test pass → **commit mẫu #1** |
| 2 | Sửa **đúng 1 dòng** `SPEC_STRICT: 'off'` → `'canary'`, commit riêng | ❌ Pipeline **đỏ** — đúng **1 test case fail** (`TC-API-LOGIN-013`) → **commit mẫu #2** |
| 3 | 🧑 Chụp màn hình 2 lần chạy ở tab Actions | `evidence/screenshots/04-ci-pass.png`, `05-ci-fail.png` |
| 4 | 🤖 Ghi 2 commit SHA + 2 link run vào `cicd-report.md` | — |

**Commit #1:** `ci(hw06): chạy pipeline ở chế độ off - toàn bộ test case pass`
**Commit #2:** `ci(hw06): bật chế độ canary - 1 test case fail do bug D-LOGIN-01 (bộ đếm tăng 2)`

### 8.3 T-6.3 — CI/CD report 🤖

`hw06/report/cicd-report.md` gồm: sơ đồ pipeline (mermaid) · giải thích từng step · giải thích thiết kế 3 chế độ `spec_strict` · bảng 2 lần chạy (SHA, link, kết quả, số test pass/fail, screenshot) · cách tải artifact.

**Commit:** `docs(hw06): viết CI/CD report cho 2 lần chạy pipeline`

---

## 9. PHASE 7 — Bug report & GitHub Issues (T-7.x) — R-05

| ID | Owner | Việc | DoD |
| :--- | :-: | :--- | :--- |
| **T-7.1** | 🤖 | Viết `hw06/report/bug-report.md` — mỗi bug theo template `Rule.pdf` §H.8, **bắt buộc** có `Found by Test Case: TC-…` và trích **response thật** từ Newman report làm Actual result | 15 bug (xem `02-sut-defect-catalog.md` §5), mỗi bug có đủ Expected / Actual / Evidence |
| **T-7.2** | 🤖 | Tạo issue trên GitHub bằng `gh issue create` (repo `trngnneee/eshop-sut`), gắn label theo `Rule.pdf` §H.7: `type: bug`, `module: api`, `severity: *`, `priority: *`, `found-by: test-case` | Mỗi bug 1 issue; ghi số issue ngược lại vào `bug-report.md` |
| **T-7.3** | 🧑 | Chụp màn hình **từng** issue → `hw06/evidence/screenshots/bug-##-issue.png`, đính vào issue tương ứng | **R-05 bắt buộc mỗi issue có screenshot** |
| **T-7.4** | 🤖 | Cập nhật `tests/test-summary/traceability-matrix.md` — thêm phần *"HW06 — API Testing"* với các dòng `Requirement | Test Case | Result | Bug Issue | Status` | Mọi test case FAIL đều có Bug Issue tương ứng (`Rule.pdf` §H.6) |

> ⚠️ Trước khi tạo issue hàng loạt, **hỏi xác nhận người dùng** — tạo 15 issue trên repo dùng chung của nhóm là hành động đối ngoại, không hoàn tác dễ dàng.

**Commit:** `docs(hw06): viết bug report cho 15 lỗi và cập nhật traceability matrix`

---

## 10. PHASE 8 — Agent Skill: AI-driven API Test Generator (T-8.x) — R-08…R-10

### 10.1 T-8.1 — 🧑 HUMAN: thiết kế + sơ đồ (R-09, R-16)

⚠️ **Codex không được làm task này.** Sinh viên tự ra quyết định thiết kế và tự vẽ sơ đồ (draw.io / Excalidraw / vẽ tay chụp lại) → lưu `hw06/test-generator/diagram.png`.

Sơ đồ nên thể hiện được các khối: `API Spec` → `Parser` → `Parameter & State Model` → `4 bộ sinh case (Partition / State / Security / Schema)` → `Test Case IR` → `Renderer (Markdown + Postman JSON)` → `Audit hook`.

### 10.2 T-8.2 — Pseudocode + tài liệu thiết kế 🤖 (theo sơ đồ của sinh viên)

`hw06/test-generator/design.md`: mô tả đầu vào/đầu ra, cấu trúc dữ liệu trung gian, chiến lược sinh case cho từng nhóm, cách nối vào bước audit, giới hạn đã biết. Kèm pseudocode.

### 10.3 T-8.3 — Hiện thực Agent Skill 🤖 (R-10)

`.agents/skills/api_test_generator/SKILL.md` — theo đúng phong cách skill sẵn có `.agents/skills/domain_and_boundary_testing/SKILL.md` (front-matter `name` + `description`, quy trình từng bước, template output, quy ước đặt mã).

Skill phải mô tả **quy trình 5 bước bắt buộc** (chính là chuỗi prompt P1–P5 ở §3.1) để lần sau tái sử dụng được cho API khác, **và** một bước phụ: tự động append entry vào AI Audit Report (đề bài mục 9 khuyến khích rõ điều này).

`.agents/skills/api_test_generator/scripts/generate_api_tests.py` — bản hiện thực chạy được: đọc file mô tả endpoint (JSON) → sinh bảng test case Markdown + skeleton Postman request.

**DoD:** chạy `python .agents/skills/api_test_generator/scripts/generate_api_tests.py examples/login.endpoint.json` sinh ra output hợp lệ.
**Commit:** `feat(skill): xây Agent Skill sinh test case API tự động từ đặc tả`

### 10.4 T-8.4 — 🧑 HUMAN: video demo (R-10, tuỳ chọn nhưng nên có)

Quay màn hình chạy skill sinh test cho **1 API** → upload YouTube (unlisted) → dán link vào `hw06/README.md` và `main-report.md`.

---

## 11. PHASE 9 — Báo cáo & đóng gói (T-9.x)

| ID | Owner | Output | Nội dung bắt buộc |
| :--- | :-: | :--- | :--- |
| **T-9.1** | 🤖 | `hw06/report/main-report.md` | Giới thiệu · SUT & môi trường · lý do chọn 3 API · **với từng API**: quy trình 5 bước, chuỗi prompt đã dùng, kết quả audit (thống kê VALID/INVALID/INCOMPLETE), case mở rộng, kết quả chạy, bug tìm được · danh sách tính năng Postman · CI/CD · thiết kế test generator · kết luận. **Nhúng link tới mọi artifact.** |
| **T-9.2** | 🤖 | `hw06/report/ai-audit-report.md` | Hoàn thiện: câu khai báo *"I use AI tools for the following tasks,"* + bảng công cụ + **toàn bộ** entry (tool / ngày giờ / prompt đầy đủ / output) — R-11 |
| **T-9.3** | 🧑 | `hw06/report/ai-critique.md` | **200–300 từ, sinh viên tự viết.** Codex chỉ chuẩn bị sẵn *phần dữ liệu đầu vào*: bảng thống kê "AI sai ở đâu" rút từ 3 file `02-audit.md` + 3 file `03-extended.md` — R-12 |
| **T-9.4** | 🤖 | `hw06/excel/test-cases.csv` + `test-summary.csv` (và `.xlsx`) | Xuất từ 3 file `test-cases.md`. Thử `pip install openpyxl` để sinh `.xlsx`; nếu không được, để CSV + ghi task chuyển đổi cho HUMAN |
| **T-9.5** | 🤖 | `hw06/report/git-commit-log.txt` | `git log --pretty=format:'%h %ad %an %s' --date=iso HW6-Khoa > hw06/report/git-commit-log.txt` — R-13 |
| **T-9.6** | 🤖 | `hw06/README.md` | Bảng tự chấm (mục 15 đề bài) + test summary: số API, số test case sinh / thêm / chạy / pass / fail, số bug + link repo công khai |
| **T-9.7** | 🤖 | `hw06/openapi/eshop.openapi.yaml` *(tuỳ chọn)* | Chuyển `api_specification.md` sang OpenAPI 3.0. ⚠️ Nếu do AI sinh thì **phải audit** và ghi kết quả audit — đề bài yêu cầu rõ |
| **T-9.8** | 🧑 | `<MSSV>_HW06_AI_API_<Grade>.zip` | Xuất PDF cho `main-report.md` + `ai-audit-report.md` + `ai-critique.md`, rồi đóng gói theo `04-deliverables-checklist.md` |

**Commit:** `docs(hw06): hoàn thiện báo cáo chính, AI audit, README tự chấm và git commit log`

---

## 12. Bảng tổng hợp task & commit

| # | Task | Owner | Commit message |
| :-: | :--- | :-: | :--- |
| 1 | T-0.1 … T-0.6 | 🤖 | `chore(hw06): khởi tạo cấu trúc thư mục và môi trường cho HW06 API Testing` |
| 2 | T-1.1 | 🤖 | `test(api-01): sinh 36 test case cho POST /api/login bằng chuỗi prompt 5 bước` |
| 3 | T-1.2 | 🤖🧑 | `test(api-01): audit test case AI sinh cho login (VALID/INVALID/INCOMPLETE) và sửa lại` |
| 4 | T-1.3 | 🤖 | `test(api-01): bổ sung 6 test case AI bỏ sót cho login kèm phân tích nguyên nhân` |
| 5 | T-1.4 | 🤖 | `docs(api-01): chốt bảng 42 test case cho POST /api/login` |
| 6 | T-2.1 | 🤖 | `test(api-02): sinh 36 test case cho POST /api/checkout bằng chuỗi prompt 5 bước` |
| 7 | T-2.2 | 🤖🧑 | `test(api-02): audit test case AI sinh cho checkout và sửa lại` |
| 8 | T-2.3 | 🤖 | `test(api-02): bổ sung 6 test case AI bỏ sót cho checkout kèm phân tích nguyên nhân` |
| 9 | T-2.4 | 🤖 | `docs(api-02): chốt bảng 42 test case cho POST /api/checkout` |
| 10 | T-3.1 | 🤖 | `test(api-03): sinh 38 test case cho PUT /api/admin/orders/:id/status bằng chuỗi prompt 5 bước` |
| 11 | T-3.2 | 🤖🧑 | `test(api-03): audit test case AI sinh cho admin order status và sửa lại` |
| 12 | T-3.3 | 🤖 | `test(api-03): bổ sung 6 test case AI bỏ sót cho admin order status kèm phân tích nguyên nhân` |
| 13 | T-3.4 | 🤖 | `docs(api-03): chốt bảng 44 test case cho PUT /api/admin/orders/:id/status` |
| 14 | T-4.1…T-4.3 | 🤖 | `feat(postman): xây collection + environment cho 3 API kèm pre-request X-Student-Id` |
| 15 | T-4.4 | 🤖 | `feat(postman): thêm 3 data file cho data-driven run (16+18+25 bộ dữ liệu)` |
| 16 | T-4.5 | 🤖🧑 | `docs(postman): liệt kê các tính năng Postman đã sử dụng` |
| 17 | T-5.1, T-5.2 | 🤖 | `test(newman): chạy toàn bộ test suite và lưu Newman HTML/JSON report` |
| 18 | T-6.1 | 🤖 | `ci(hw06): thêm GitHub Actions chạy Newman cho bộ test API` |
| 19 | T-6.2a | 🤖 | `ci(hw06): chạy pipeline ở chế độ off - toàn bộ test case pass` |
| 20 | T-6.2b | 🤖 | `ci(hw06): bật chế độ canary - 1 test case fail do bug D-LOGIN-01 (bộ đếm tăng 2)` |
| 21 | T-6.3 | 🤖 | `docs(hw06): viết CI/CD report cho 2 lần chạy pipeline` |
| 22 | T-7.1…T-7.4 | 🤖🧑 | `docs(hw06): viết bug report cho 15 lỗi và cập nhật traceability matrix` |
| 23 | T-8.2, T-8.3 | 🤖 | `feat(skill): xây Agent Skill sinh test case API tự động từ đặc tả` |
| 24 | T-9.1…T-9.7 | 🤖 | `docs(hw06): hoàn thiện báo cáo chính, AI audit, README tự chấm và git commit log` |

**Tổng: 24 commit** — thoả R-13 ("commit riêng cho từng bước của quy trình, cho từng API").

---

## 13. Phụ lục — Chuỗi prompt chuẩn (dùng cho T-1.1 / T-2.1 / T-3.1)

> Chép nguyên văn các prompt này (thay `<ENDPOINT>`, `<FR>`) vào AI Audit Report ở R-11. **Không** rút gọn thành một prompt duy nhất — vi phạm P-01.

**P1 — Phân tích tham số & trạng thái**

```
Đây là đặc tả API của hệ thống EShop (api_specification.md, phần <MỤC>) và đặc tả nghiệp vụ (README.md, <FR>).
CHƯA sinh test case. Ở bước này chỉ làm đúng 2 việc:
1. Liệt kê MỌI tham số đầu vào của <ENDPOINT>: tên, vị trí (body/path/query/header),
   kiểu dữ liệu, bắt buộc hay không, ràng buộc theo đặc tả.
2. Liệt kê MỌI trạng thái hệ thống ảnh hưởng tới kết quả gọi API này.
Trình bày dưới dạng 2 bảng Markdown.
```

**P2 — Domain partition**

```
Dựa trên bảng tham số ở bước 1, áp dụng Equivalence Partitioning + Boundary Value Analysis.
Với TỪNG tham số: liệt kê phân vùng hợp lệ, phân vùng không hợp lệ, và các giá trị biên.
Sau đó sinh test case, mỗi phân vùng không hợp lệ là MỘT test case riêng.
Định dạng bảng: TC ID | Nhóm=Partition | Tiêu đề | Precondition | Test data | Expected (HTTP status + body).
Expected result phải bám theo ĐẶC TẢ, không phải theo phỏng đoán về hiện thực.
```

**P3 — State transition**

```
Dựa trên bảng trạng thái ở bước 1, vẽ mô hình trạng thái của <ENDPOINT> dưới dạng bảng chuyển đổi.
Sinh test case phủ: mọi chuyển đổi HỢP LỆ, mọi chuyển đổi KHÔNG HỢP LỆ, và các trạng thái kết thúc.
Định dạng bảng như bước 2, cột Nhóm = State.
```
*(Với API-3, thêm: "Ma trận có 5 trạng thái nên phải sinh đủ 25 test case, không được bỏ ô nào.")*

**P4 — Security**

```
Đây là 7 yêu cầu bảo mật SEC-01..SEC-07 của hệ thống: <dán bảng từ README.md mục 9>.
Với <ENDPOINT>, sinh test case bảo mật cho từng yêu cầu áp dụng được, tối thiểu phủ:
SQL injection, thiếu/sai/hỏng JWT, IDOR, role escalation, rò rỉ dữ liệu nhạy cảm trong response.
Định dạng bảng như bước 2, cột Nhóm = Security, thêm cột SEC ID.
```

**P5 — Schema validation**

```
Đây là hình dạng response được đặc tả cho <ENDPOINT>: <dán từ api_specification.md>.
Sinh test case kiểm tra response khớp CHÍNH XÁC đặc tả: đúng tên field, đúng kiểu dữ liệu,
KHÔNG có field thừa (đặc biệt là field nhạy cảm), đúng Content-Type, đúng HTTP status cho từng nhánh.
Định dạng bảng như bước 2, cột Nhóm = Schema.
```

---

## 14. Thứ tự chạy khuyến nghị

```
Phase 0  ──►  Phase 1  ──►  Phase 2  ──►  Phase 3
(môi trường)   (API-1)      (API-2)      (API-3)
                                            │
                    ┌───────────────────────┘
                    ▼
Phase 4  ──►  Phase 5  ──►  Phase 6  ──►  Phase 7  ──►  Phase 8  ──►  Phase 9
(Postman)     (Newman)      (CI/CD)       (Bugs)       (Skill)      (Báo cáo)
```

**Các điểm dừng chờ HUMAN** (Codex phải dừng và báo, không tự đi tiếp):

1. Sau **T-1.2 / T-2.2 / T-3.2** — sinh viên duyệt bảng audit (R-02 quy trách nhiệm cho người).
2. Trước **T-7.2** — xác nhận trước khi tạo 15 issue trên repo dùng chung.
3. Tại **T-8.1** — sinh viên tự vẽ sơ đồ trước khi Codex viết `design.md`.
4. Tại **T-5.3, T-6.2 bước 3, T-7.3** — sinh viên chụp screenshot.
