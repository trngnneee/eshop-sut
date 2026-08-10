# PLAN — Codex thực hiện Mini Exercise (POST /api/products)

> Đầu vào: `Requirements/SPEC.md` (đã điền đủ tham số mục 0). Tài liệu này là **kế hoạch thi công**: thứ tự bước, nội dung cụ thể từng file, và tiêu chí kiểm tra.
> Nguyên tắc: **không sửa code backend**, không bịa hành vi API — mọi expected_status phải khớp hành vi thật đã verify bằng curl.

---

## 0. Tham số chốt

| Tham số      | Giá trị                 |
| ------------ | ----------------------- |
| `MSSV`       | `23127207`              |
| `API_CHOSEN` | `POST /api/products`    |
| `API_SLUG`   | `products`              |
| `BRANCH`     | `Khoa-MiniExercise-API` |
| `BASE_URL`   | `http://localhost:3000` |

Tên file dẫn xuất:
- `mini-products.data.json`
- `mini-products.postman_collection.json`
- `mini-local.postman_environment.json`
- `mini-newman-report.json`
- `.github/workflows/newman-api-test.yml`
- `23127207_Mini_API_Testing.zip`

Vị trí đặt artifact D1–D5: thư mục `mini-api-testing/` ở gốc repo (trừ D6 nằm ở `.github/workflows/`).

> **Đóng gói phẳng:** đề bài (trang 8) liệt kê nội dung zip **không có thư mục con**. Khi tạo `23127207_Mini_API_Testing.zip` phải flatten toàn bộ D1–D7 ra gốc zip, và lệnh newman ghi trong `test-design.md` phải khớp đường dẫn phẳng đó (không phải đường dẫn `mini-api-testing/...` dùng khi chạy trong repo).

> **Skill (đề bài gợi ý "tạo skill cho api testing"):** SPEC ghi `.claude/skills/api-testing/SKILL.md` nhưng repo đang dùng convention `.agents/skills/<name>/SKILL.md` (xem `.agents/skills/domain_and_boundary_testing/`). Đề bài không chỉ định path → **theo convention sẵn có của repo**: `.agents/skills/api_testing/SKILL.md`.

---

## 1. SỰ THẬT VỀ API (đã đọc code — dùng làm nguồn duy nhất)

`backend/server.js:167-177`:

```js
app.post("/api/products", (req, res) => {
  const { name, price, description, imageUrl, category_id } = req.body;
  db.run("INSERT INTO products (name, price, description, imageUrl, category_id) VALUES (?, ?, ?, ?, ?)",
    [name, price, description, imageUrl, category_id],
    function (err) {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ message: "Product created", id: this.lastID });
    });
});
```

Schema bảng (`backend/database.js:64-71`): `id INTEGER PK AUTOINCREMENT, name TEXT, price INTEGER, description TEXT, imageUrl TEXT, category_id INTEGER` — **không có NOT NULL, không có FK constraint, không CHECK**.

Hệ quả bắt buộc phải phản ánh trong test design:

| Thực tế                                                              | Ảnh hưởng                                                                |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Không có `authenticateToken` → không token vẫn tạo được sản phẩm    | **Đúng đặc tả đề bài**, xem OBS-01 bên dưới — KHÔNG gọi là bug          |
| Không validate `name`, `price` → thiếu field / `price` âm vẫn 200   | Test biên "expect 400" thực tế trả 200 → BUG                            |
| Dùng prepared statement (`?`) → SQLi payload bị lưu như string thường | Test SQLi kỳ vọng "không thực thi" → **PASS**, viết assert theo hướng này |
| Không escape HTML → payload XSS lưu nguyên văn                       | Test XSS: ghi nhận thiếu sanitize ở tầng API (OBS-02)                    |
| `category_id` không tồn tại vẫn insert được                          | BUG (thiếu FK)                                                           |
| Chỉ `err` mới ra 500; happy case trả **200**, KHÔNG phải 201          | Vi phạm REST → 1 trong ≥2 test case Extend                              |
| Response body chỉ có `{message, id}` — không trả object sản phẩm      | Contract assertion chỉ được assert 2 field này                           |

### OBS-01 — Vì sao "không auth" KHÔNG phải bug
Bảng 21 API trong `Mini_Exercise.pdf` (trang 2) mô tả #3 `POST /api/products` là *"Thêm mới sản phẩm. Yêu cầu JSON body đầy đủ thông tin"* — **cố ý không ghi "Yêu cầu Auth Token"**, trong khi #7 `POST /api/categories` thì có. Vậy endpoint là **public theo đặc tả**.

Hệ quả cho test design:
- KHÔNG viết "BUG-01: thiếu authentication". Thay bằng **OBS-01 (observation)**: *"Endpoint public đúng đặc tả; ghi nhận rủi ro thiếu phân quyền — bất kỳ ai cũng tạo được sản phẩm — như một khuyến nghị cải tiến, không phải defect."*
- Nhóm Security **chuyển trọng tâm** sang SQLi + XSS sanitization (vẫn đủ nhóm coverage bắt buộc).
- Vẫn giữ 1 TC "không token" để chứng minh endpoint public, nhưng nhãn audit là VALID-by-spec chứ không phải INVALID.
- **OBS-02**: API không escape HTML → payload XSS lưu literal; đây là rủi ro stored-XSS phụ thuộc tầng render, ghi nhận chứ không kết luận defect API.
- Giữ nguyên **BUG-02** (thiếu input validation) và **BUG-03** (trả 200 thay vì 201) — hai cái này là defect thật.

### Bước xác minh trước khi viết bất cứ test case nào
Chạy và **lưu output vào `test-design.md`** (mục "Evidence"):
```bash
cd backend && npm install && npm run dev   # nền
curl -s http://localhost:3000/api/products/1                                   # smoke: iPhone 15 Pro Max
curl -s -o- -w "\n%{http_code}\n" -X POST http://localhost:3000/api/products -H "Content-Type: application/json" -d '{"name":"T","price":100,"description":"d","imageUrl":"u","category_id":1}'
curl -s -o- -w "\n%{http_code}\n" -X POST http://localhost:3000/api/products -H "Content-Type: application/json" -d '{}'
curl -s -o- -w "\n%{http_code}\n" -X POST http://localhost:3000/api/products -H "Content-Type: application/json" -d '{"name":"X","price":-5,"category_id":1}'
curl -s -o- -w "\n%{http_code}\n" -X POST http://localhost:3000/api/products -d 'name=X&price=1'     # không JSON
curl -s -o- -w "\n%{http_code}\n" -X POST http://localhost:3000/api/products -H "Content-Type: application/json" -d '{"name":"A","price":{"a":1},"category_id":1}'  # kỳ vọng 500
curl -s -o- -w "\n%{http_code}\n" -X POST http://localhost:3000/api/products -H "Content-Type: application/json" -d '{"name":"<script>alert(1)</script>","price":100,"category_id":1}'   # XSS benign
# E2E chain: lấy id từ response POST rồi GET lại để xác minh đã lưu
curl -s http://localhost:3000/api/products/<id_vua_tao>
```
Nếu kết quả thật khác bảng trên → **lấy kết quả thật làm chuẩn**, sửa lại plan này rồi báo người dùng.

Backup DB trước khi test (POST ghi thật vào `backend/database.sqlite`):
`cp backend/database.sqlite backend/database.sqlite.bak` và restore sau khi xong, hoặc xoá file để seed lại.

---

## 2. Thứ tự thi công

### T1 — Chuẩn bị (30′)
1. `git checkout Khoa-MiniExercise-API`, `git pull`.
2. `mkdir mini-api-testing`.
3. Backup `database.sqlite`, start backend, chạy toàn bộ curl ở §1, lưu log thô vào `mini-api-testing/evidence-curl.txt`.

### T2 — R1 Generate (≥12 TC)
Viết **prompt nguyên văn** vào `test-design.md` §1. Prompt bắt buộc chứa:
- Method + URL + `Content-Type: application/json`
- Request body mẫu đầy đủ 5 field
- Response mẫu happy (`{"message":"Product created","id":11}`, HTTP 200) **và** error (`{"error":"..."}`, HTTP 500)
- Câu "liệt kê giả định nếu thiếu thông tin, không tự bịa field"
- Yêu cầu output bảng đúng 5 cột: `tc_id | input | expected_status | expected_fields | rationale`
- Yêu cầu đặt tên test theo tiền tố `Functional:` / `Contract:`

Ma trận coverage ≥12 TC (đây là nội dung tối thiểu — Codex bám theo):

| tc_id      | Nhóm             | Input                                           | expected_status (theo SPEC/REST) |
| ---------- | ---------------- | ----------------------------------------------- | -------------------------------- |
| TC-P-001   | Domain – valid  | đủ 5 field hợp lệ                              | 200/201                          |
| TC-P-002   | Domain – biên   | `price = 0`                                     | 400                              |
| TC-P-003   | Domain – invalid | `price = -1`                                    | 400                              |
| TC-P-004   | Domain – biên   | `price` rất lớn (2^53)                          | 400/200                          |
| TC-P-005   | Domain – invalid | thiếu `name`                                    | 400                              |
| TC-P-006   | Domain – invalid | `name` = chuỗi rỗng                             | 400                              |
| TC-P-007   | Domain – invalid | `price` là string `"abc"`                       | 400                              |
| TC-P-008   | Domain – invalid | `category_id` không tồn tại (`9999`)            | 400/404                          |
| TC-P-009   | Security         | **thiếu** Authorization header                  | 200 (public theo spec, OBS-01)   |
| TC-P-010   | Security         | token hết hạn / sai format                      | 401 nếu có auth — xem OBS-01     |
| TC-P-011   | Security         | token role `user` (không phải admin)            | 403 — case riêng, không gộp 401 |
| TC-P-012   | Security         | SQLi benign trong `name`: `A'); DROP TABLE x;--` | không thực thi, lưu literal      |
| TC-P-013   | Security         | XSS benign: `name = <script>alert(1)</script>`   | escape/sanitize hoặc 400         |
| TC-P-014   | Contract/Schema  | response khớp jsonSchema `{message, id}`        | 200                              |
| TC-P-015   | Error handling   | `price` là object → SQLite type error          | 500                              |
| TC-P-016   | E2E Workflow     | `POST` → `GET /:id` xác minh đã lưu đúng field | 200 + 200                        |

> `TC-P-010/011` giữ lại để thể hiện tư duy tách 401/403 theo yêu cầu đề bài, nhưng bảng audit phải ghi rõ chúng **không áp dụng** cho endpoint public này (OBS-01) → không đưa vào 5 iteration.

### T3 — R2 Audit
Bảng 3 cột `TC | Nhãn | Nhận xét hoặc chỉnh sửa`, **mọi TC đều có nhãn**, lý do ≥1 câu.

Dựa vào §1, hướng gán nhãn (Codex phải tự kiểm chứng lại bằng evidence, không copy mù):
- `TC-P-009` → **VALID**: endpoint public đúng đặc tả (OBS-01), sửa `expected_status` 401 → 200 và ghi observation về rủi ro phân quyền.
- `TC-P-010/011` → **INVALID**: AI giả định endpoint có auth trong khi bảng 21 API không yêu cầu token cho #3 → không áp dụng, loại khỏi bộ chạy. Đây chính là ≥1 case INVALID bắt buộc phải sửa.
- `TC-P-002..008` → **INCOMPLETE/INVALID**: SUT không validate → **BUG-02: thiếu input validation**. Tách `expected_status` (thật) và `spec_status` (đúng chuẩn).
- `TC-P-001` → **INCOMPLETE**: AI giả định 201 nhưng SUT trả 200, cũng không có header `Location` → **BUG-03**.
- `TC-P-012` → **VALID** (prepared statement đã chặn).
- `TC-P-013` → **INCOMPLETE**: AI chỉ nêu "kỳ vọng sanitize" mà không nói sanitize ở tầng nào → bổ sung: API lưu literal, phòng thủ nằm ở tầng render (OBS-02).
- `TC-P-015` → **VALID**, là con đường duy nhất chạm nhánh 500.
- `TC-P-016` → **VALID**.

Bắt buộc: sửa ít nhất 1 case INVALID/INCOMPLETE và **ghi rõ nội dung sửa**.

### T4 — R3 Extend (≥2 TC tự viết, kèm lý do AI bỏ sót)
1. **TC-EXT-001 — Content-Type sai**: gửi `application/x-www-form-urlencoded`. `express.json()` không parse → `req.body` rỗng → vẫn 200 nhưng bản ghi toàn NULL. *Lý do AI bỏ sót:* prompt tập trung body, model coi header là hiển nhiên (prompt quality).
2. **TC-EXT-002 — Response time < 1000ms** (ngưỡng theo guide mục 1; không dùng 500ms vì dễ flaky trên GitHub runner): yêu cầu phi chức năng, AI chỉ sinh test chức năng (model limitation).
3. **TC-EXT-003 — Status không chuẩn REST**: tạo tài nguyên trả 200 thay vì 201, và không có header `Location`. *Lý do:* AI suy theo chuẩn REST chứ không đọc code thật (đặc thù SUT).

### T5 — R4 Execute
**Data file `mini-products.data.json` — đúng 5 iteration.** Chọn 5 case sao cho khi chạy thật **0 assertion fail** → `expected_status` phải là **giá trị thật**, kèm cột ghi chú kỳ vọng theo spec:

```json
[
  { "tc_id": "TC-P-001", "case_name": "Happy path - full valid payload",
    "content_type": "application/json",
    "body": { "name": "Mini Test Product", "price": 1000, "description": "codex", "imageUrl": "http://x/i.png", "category_id": 1 },
    "expected_status": 200, "expect_id": true, "spec_status": 201, "note": "SUT tra 200 thay vi 201 - BUG-03" },

  { "tc_id": "TC-P-005", "case_name": "Missing name - no validation",
    "content_type": "application/json",
    "body": { "price": 1000, "category_id": 1 },
    "expected_status": 200, "expect_id": true, "spec_status": 400, "note": "BUG-02 thieu validation" },

  { "tc_id": "TC-P-013", "case_name": "Benign XSS payload in name",
    "content_type": "application/json",
    "body": { "name": "<script>alert(1)</script>", "price": 100, "category_id": 1 },
    "expected_status": 200, "expect_id": true, "spec_status": 400, "note": "OBS-02 khong sanitize o tang API" },

  { "tc_id": "TC-P-012", "case_name": "Benign SQLi payload in name",
    "content_type": "application/json",
    "body": { "name": "A'); DROP TABLE products;--", "price": 100, "category_id": 1 },
    "expected_status": 200, "expect_id": true, "spec_status": 200, "note": "Prepared statement chan SQLi" },

  { "tc_id": "TC-P-015", "case_name": "Invalid price type triggers DB error",
    "content_type": "application/json",
    "body": { "name": "Bad Price", "price": { "a": 1 }, "category_id": 1 },
    "expected_status": 500, "expect_id": false, "spec_status": 400, "note": "SQLite bind error" }
]
```
> Nếu curl ở §1 cho kết quả khác (đặc biệt case cuối), **sửa `expected_status` theo thực tế** rồi ghi lại lý do trong `test-design.md`.
>
> **Xung đột số dòng dữ liệu:** guide gợi ý ≥8 bộ dữ liệu, nhưng checkpoint đề bài yêu cầu **đúng 5 iteration**. → Theo đề bài (5), ghi 1 câu giải thích trong `test-design.md`. TC-P-009 bị loại khỏi bộ chạy vì mọi request trong collection vốn không gửi token nên đã trùng với happy path; TC-P-010/011 loại theo OBS-01.

**Collection `mini-products.postman_collection.json`** — 1 request `POST {{baseUrl}}/api/products`, body raw JSON `{{body}}`… lưu ý Postman không nội suy object vào raw body, nên dùng pre-request script build body:

Pre-request script (giữ nguyên đoạn bắt buộc của SPEC):
```js
pm.request.headers.upsert({ key: "X-Student-Id", value: pm.environment.get("studentId") });
pm.request.headers.upsert({ key: "Content-Type", value: pm.iterationData.get("content_type") || "application/json" });
pm.variables.set("bodyJson", JSON.stringify(pm.iterationData.get("body")));
```
→ Body raw = `{{bodyJson}}`.

Test script:
```js
const expected = Number(pm.iterationData.get("expected_status"));
const tc = pm.iterationData.get("tc_id");

pm.test(`Functional: ${tc} status = ${expected}`, () => pm.response.to.have.status(expected));

if (pm.iterationData.get("expect_id")) {
  // Guide muc 2: dung jsonSchema, KHONG check typeof thu cong,
  // va tach hoan toan khoi assertion nghiep vu o tren
  const schema = {
    type: "object",
    required: ["message", "id"],
    properties: {
      message: { type: "string" },
      id: { type: "number" },
    },
  };
  pm.test(`Contract: ${tc} response matches schema`, () =>
    pm.response.to.have.jsonSchema(schema));

  // Luu id cho folder E2E
  pm.collectionVariables.set("createdProductId", pm.response.json().id);
}

pm.test(`[MINI] ${tc} Content-Type is application/json`, () =>
  pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json"));

pm.test(`[MINI] ${tc} response time < 1000ms`, () => pm.expect(pm.response.responseTime).to.be.below(1000));
```

**Folder `E2E Workflow` trong collection** (guide trang 8 đánh "Bắt buộc" cho E2E; đề bài chính không bắt buộc nhưng đây là cách dùng *Collection variables* một cách thực chất):
- Request 2: `GET {{baseUrl}}{{apiPath}}/{{createdProductId}}` — assert 200, `name` khớp giá trị vừa POST, chứng minh dữ liệu đã lưu thật.
- Nếu muốn đủ chain CRUD: thêm `PUT /:id` → `DELETE /:id`, mỗi bước assert 200.
- Folder này chạy ngoài data-driven run (hoặc chỉ chạy ở iteration đầu) để **không phá checkpoint 5 iteration** — kiểm tra lại số assertion sau khi thêm.

**Environment `mini-local.postman_environment.json`**: `baseUrl=http://localhost:3000`, `studentId=23127207`.
**Collection variable** (để tick được feature R6): `apiPath=/api/products` — dùng trong URL `{{baseUrl}}{{apiPath}}`.

Chạy:
```bash
newman run mini-api-testing/mini-products.postman_collection.json \
  --environment mini-api-testing/mini-local.postman_environment.json \
  --iteration-data mini-api-testing/mini-products.data.json \
  --reporters cli,json \
  --reporter-json-export mini-api-testing/mini-newman-report.json
```
**Checkpoint:** 5 iteration · `run.stats.assertions.failed == 0` · report tồn tại · log có `X-Student-Id: 23127207`.

### T6 — R5 CI/CD
`.github/workflows/newman-api-test.yml`:
```yaml
name: Newman API Test
on: [push, workflow_dispatch]
jobs:
  api-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci || npm install
        working-directory: backend
      - run: npm run dev &
        working-directory: backend
      - name: Wait for backend
        run: npx wait-on http://localhost:3000/api/products --timeout 60000
      - run: npm i -g newman
      - run: |
          newman run mini-api-testing/mini-products.postman_collection.json \
            --environment mini-api-testing/mini-local.postman_environment.json \
            --iteration-data mini-api-testing/mini-products.data.json \
            --reporters cli,json \
            --reporter-json-export mini-newman-report.json
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: newman-report, path: mini-newman-report.json }
```
Lưu ý: `backend/database.sqlite` phải được commit hoặc seed tự động trên CI — kiểm tra `.gitignore` trước khi push.

Chuỗi commit trên `Khoa-MiniExercise-API`:
- **C1 pass** → chờ Actions xanh → `ci-pass.png`.
- **C2 fail chủ đích** → đổi `expected_status` của TC-P-001 từ `200` → `999`, push → đỏ → `ci-fail.png`.
- **C3 khôi phục** → revert về `200`, push → xanh. **Commit cuối phải pass.**

### T7 — R6 + đóng gói
Bảng 10 dòng `Feature | Đã dùng? | Ghi chú` trong `test-design.md`. Đánh **Có** cho 7: Collections, Environment variables, Collection variables, Pre-request scripts, Test scripts, Data-driven runs, Newman CLI. Đánh **Không** cho Monitors, Mock servers, Workspaces (ghi lý do 1 câu).

Zip: `23127207_Mini_API_Testing.zip` chứa D1–D7.

---

## 3. Cấu trúc `test-design.md`

```
# Mini Exercise — POST /api/products — 23127207
## 0. API under test (evidence: code + curl log)
## 1. Bước 1 — Prompt đã dùng (nguyên văn)
## 2. Bước 1 — AI output (bảng ≥12 TC, 5 cột)
## 3. Bước 2 — Audit table (TC | Nhãn | Nhận xét/chỉnh sửa) + danh sách BUG-02, BUG-03 + OBS-01, OBS-02
## 4. Bước 3 — Extend (≥2 TC + lý do AI bỏ sót)
## 5. Bước 4 — 5 case đã chọn, mapping data file ↔ collection variable
## 6. Bước 5 — CI/CD, 3 commit, 2 ảnh
## 7. Bước 6 — Postman features (10 dòng)
```

---

## 4. Definition of Done (checklist Codex tự verify)

- [ ] D1–D8 đủ, đúng tên file
- [ ] `mini-newman-report.json`: `run.stats.iterations.total == 5`, `run.stats.assertions.failed == 0`
- [ ] ≥12 TC generate, **100%** có nhãn audit, ≥2 TC extend có lý do
- [ ] Header `X-Student-Id: 23127207` xuất hiện trong log Newman
- [ ] Có `ci-fail.png` (1 lần fail) và commit cuối trên nhánh pass
- [ ] ≥6 Postman feature "Có" + ghi chú
- [ ] `backend/` không bị sửa (`git diff --stat backend/` rỗng, trừ `database.sqlite`)
- [ ] Payload SQLi chỉ chạy local

## 5. Điểm Codex PHẢI hỏi lại người dùng

1. Nếu curl §1 cho status khác bảng dự đoán → báo trước khi viết data file.
2. Nếu `backend/database.sqlite` nằm trong `.gitignore` → hỏi cách seed DB trên CI.
3. ~~Nhánh nộp~~ — **đã giải quyết**: `Mini_Exercise.pdf` trang 3 và 7 ghi `feature/<MSSV>` kèm chữ "ví dụ" → nhánh `Khoa-MiniExercise-API` hiện tại hợp lệ, không cần đổi. Yêu cầu cứng duy nhất: push lên repo nhóm đã fork từ `eshop-sut` và đã bấm "Enable" ở tab Actions.
