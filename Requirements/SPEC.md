# SPEC — Mini Exercise: API Testing Pipeline (Generate → Audit → Extend → Execute → CI/CD)

> Tài liệu này là **đặc tả yêu cầu** để một coding agent (Codex) thực hiện bài Mini Exercise.
> Nguồn yêu cầu: `Mini_Exercise.pdf` (đề bài) + `postman-contract-test-prompt-guide.pdf` (guide viết prompt).
> Mọi mục đánh dấu `[TODO-USER]` **phải** được điền trước khi bắt đầu; agent KHÔNG được tự bịa.

---

## 0. Tham số đầu vào (điền trước khi chạy)

| Tham số      | Giá trị                 | Ghi chú                                                           |
| ------------ | ----------------------- | ----------------------------------------------------------------- |
| `MSSV`       | `23127207`              | Dùng cho `studentId`, tên nhánh, tên file zip                     |
| `API_CHOSEN` | `POST /api/products`    | 1 endpoint duy nhất từ bảng 21 API; không trùng với bạn cùng nhóm |
| `API_SLUG`   | `products`              | vd `login`, `cart`, `cancel-order` — dùng đặt tên file            |
| `BRANCH`     | `Khoa-MiniExercise-API` | Nhánh làm bài                                                     |
| `BASE_URL`   | `http://localhost:3000` | Biến `baseUrl` trong environment                                  |

**Khuyến nghị chọn API:** `PUT /api/orders/:id/cancel` (#19) — là endpoint duy nhất phủ đồng thời cả 4 nhóm test bắt buộc của Bước 1: domain partition (id), **state transition** (pending→canceled hợp lệ, delivered→canceled không hợp lệ), **security** (thiếu token / token hết hạn / IDOR hủy đơn người khác), và schema validation.
Phương án thay thế đơn giản hơn: `POST /api/login` (#9) — dễ làm nhưng **không có state transition**, phải bù bằng test case tự nghĩ.

---

## 1. Mục tiêu

Xây dựng trọn bộ artifact nộp bài cho **1 API duy nhất**, chạy được thật (Postman Runner + Newman + GitHub Actions), không phải tài liệu suông.

## 2. Phạm vi

**Trong phạm vi:** thiết kế test case, collection/environment/data file Postman, chạy Newman sinh report, workflow CI/CD với 2 commit minh họa pass/fail, tài liệu `test-design.md`.

**Ngoài phạm vi:** sửa code backend `eshop-sut`; test API khác ngoài `API_CHOSEN`; Pact contract test (guide có nêu nhưng đề bài Mini Exercise **không** yêu cầu — chỉ dùng phần Nhóm I của guide).

---

## 3. Deliverables (bắt buộc, đúng tên file)

| #   | File                                      | Yêu cầu chấp nhận                                                                                                  |
| --- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| D1  | `test-design.md`                          | Có đủ 5 phần: prompt đã dùng, AI output rút gọn (≥12 TC), bảng audit, test case extend (≥2), bảng Postman features |
| D2  | `mini-<API_SLUG>.data.json`               | ≥5 test case (đúng 5 iteration khi chạy), có cột `expected_status`, gồm cả positive + negative                     |
| D3  | `mini-<API_SLUG>.postman_collection.json` | Có pre-request script gắn header `X-Student-Id`, test script assert theo biến từ data file                         |
| D4  | `mini-local.postman_environment.json`     | Có `baseUrl` và `studentId=<MSSV>`                                                                                 |
| D5  | `mini-newman-report.json`                 | Sinh ra từ lần chạy Newman thật, 5 iteration, 0 assertion fail                                                     |
| D6  | `newman-api-test.yml`                     | Đặt tại `.github/workflows/`, tự start backend → cài newman → chạy collection → upload report                      |
| D7  | `ci-pass.png`, `ci-fail.png`              | Ảnh chụp GitHub Actions thật                                                                                       |
| D8  | `<MSSV>_Mini_API_Testing.zip`             | Đóng gói D1–D7                                                                                                     |

---

## 4. Yêu cầu chi tiết theo từng bước

### R1 — Bước 1: Generate with AI (≥12 test case)

- Prompt phải **mô tả API thật**: method, URL, headers, request body mẫu, response mẫu happy case **và** error case, status code có thể trả về. Không prompt kiểu "generate all tests".
- Prompt phải yêu cầu output dạng bảng với đúng các cột: `tc_id | input | expected_status | expected_fields | rationale`.
- Yêu cầu AI **liệt kê giả định** nếu thiếu thông tin thay vì tự bịa field.
- Coverage bắt buộc của 12+ TC:
  - **Domain partitions**: giá trị hợp lệ / không hợp lệ / biên cho từng tham số (email format, password complexity, `price > 0`, id tồn tại / không tồn tại).
  - **State transitions** (nếu API liên quan đơn hàng): `pending → confirmed → shipping → delivered`, nhánh `canceled`, và các chuyển trạng thái **không hợp lệ**.
  - **Security**: thiếu token (401), token hết hạn (401), token sai format, SQL injection, **IDOR**, role escalation (403 ≠ 401 — phải tách 2 case riêng).
  - **Schema validation**: response body đúng field + kiểu dữ liệu theo đặc tả.
- Đặt tên test theo tiền tố `Functional:` / `Contract:` (theo guide) để tách assertion nghiệp vụ khỏi assertion schema.
- Payload SQLi/XSS chỉ dùng dạng **benign** để kiểm tra hành vi sanitize; chỉ chạy trên môi trường local.
- **Lưu nguyên văn prompt + output** vào `test-design.md`.
- Nếu tạo Claude Code skill cho việc này (đề bài có gợi ý "tạo skill"): đặt tại `.claude/skills/api-testing/SKILL.md`.

### R2 — Bước 2: Audit (human review)

- Bảng 3 cột: `TC | Nhãn | Nhận xét hoặc chỉnh sửa`.
- **Mọi** TC phải có nhãn `VALID` / `INVALID` / `INCOMPLETE`, kèm lý do ≥1 câu.
- Phải sửa ≥1 case `INVALID`/`INCOMPLETE`. Nếu tất cả đều VALID → phải chỉ ra 1 giả định AI chưa nêu rõ và bổ sung.

### R3 — Bước 3: Extend (≥2 test case tự viết)

- Mỗi case kèm giải thích **vì sao AI bỏ sót** (prompt quality / model limitation / đặc thù API).
- Gợi ý hướng thường bị bỏ sót: `Content-Type: application/json`; response time dưới ngưỡng; edge case đầu vào (chuỗi rỗng, số âm, số rất lớn, ký tự đặc biệt); status không chuẩn REST (trả 200 thay vì 404).

### R4 — Bước 4: Execute

1. Start provider: `cd backend && npm run dev`; smoke check `curl http://localhost:3000/api/products/1` → 200, trả về "iPhone 15 Pro Max".
2. Chọn **5 test case** từ kết quả Bước 2+3 → viết vào `mini-<API_SLUG>.data.json`. Cấu trúc JSON phải khớp chính xác tên biến dùng trong collection.
3. Pre-request script (bắt buộc, đúng nội dung này):
   ```js
   pm.request.headers.upsert({
     key: "X-Student-Id",
     value: pm.environment.get("studentId"),
   });
   ```
4. Test script: assert dựa trên biến data file (`pm.iterationData.get("expected_status")`), **cộng thêm** ≥1 assertion tự viết về `Content-Type` hoặc response time, đặt tên có tiền tố `[MINI]`.
5. Chạy Newman:
   ```bash
   newman run mini-<API_SLUG>.postman_collection.json \
     --environment mini-local.postman_environment.json \
     --iteration-data mini-<API_SLUG>.data.json \
     --reporters cli,json \
     --reporter-json-export mini-newman-report.json
   ```

**Checkpoint R4:** đúng 5 iteration · 0 assertion fail · `mini-newman-report.json` tồn tại · log cho thấy header `X-Student-Id` = đúng MSSV.

### R5 — Bước 5: CI/CD

- `.github/workflows/newman-api-test.yml`: checkout → `actions/setup-node` (Node 18/20) → `npm ci` trong `backend` → start backend nền + wait-for-port 3000 → `npm i -g newman` → chạy lệnh ở R4.5 → `actions/upload-artifact` cho `mini-newman-report.json`.
- **C1 (pass):** push lên `feature/<MSSV>` → chụp `ci-pass.png`.
- **C2 (fail có chủ đích):** sửa `expected_status` từ `200` → `999` trong data file, push → chụp `ci-fail.png`.
- **C3 (khôi phục):** revert giá trị đúng, push. **Commit cuối trên nhánh bắt buộc phải pass.**

### R6 — Bước 6: Postman features

Bảng `Feature | Đã dùng? | Ghi chú` trong `test-design.md` với 10 dòng: Collections, Environment variables, Collection variables, Pre-request scripts, Test scripts, Data-driven runs, Newman CLI, Monitors, Mock servers, Workspaces.
**Bắt buộc ≥6 feature đánh "Có"**, mỗi cái ghi chú 1 câu. Đề xuất 6 cái dễ đạt: Collections, Environment variables, Collection variables, Pre-request scripts, Test scripts, Data-driven runs, Newman CLI (7).

---

## 5. Ràng buộc kỹ thuật

- Node.js 18 hoặc 20 LTS; Newman cài global; Postman Desktop cho phần export.
- Làm việc trên nhánh `feature/<MSSV>` của repo nhóm đã fork từ `eshop-sut`; tab Actions phải được "Enable".
- Không hard-code token/URL trong collection — dùng biến environment/collection.
- Không chạy payload phá hoại ngoài môi trường local.

## 6. Rủi ro & cách xử lý

| Rủi ro                                                                 | Xử lý                                                                                                  |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Data file không khớp tên biến trong collection → assertion sai âm thầm | Đặt tên biến 1 lần trong spec data schema, tham chiếu thống nhất                                       |
| Backend chưa sẵn sàng khi CI chạy newman                               | Thêm bước wait-for-port / retry curl trước khi chạy test                                               |
| Test phụ thuộc dữ liệu có sẵn (order id, token)                        | Tạo dữ liệu trong bước setup của collection (register → login → checkout) hoặc dùng seed data của repo |
| Gộp assert schema và assert nghiệp vụ vào 1 test                       | Tách theo tiền tố `Contract:` / `Functional:`                                                          |
| Nhầm 401 và 403                                                        | Luôn viết 2 test case riêng                                                                            |

## 7. Definition of Done

- [ ] Đủ 8 deliverable D1–D8, đúng tên file.
- [ ] `mini-newman-report.json` có `run.stats.assertions.failed == 0` và 5 iteration.
- [ ] ≥12 TC generate, 100% có nhãn audit, ≥2 TC extend.
- [ ] Pipeline: có bằng chứng 1 lần fail và commit cuối pass.
- [ ] ≥6 Postman feature được đánh dấu và ghi chú.

## 8. Thứ tự thực hiện cho Codex

1. Điền tham số mục 0 → xác nhận với người dùng.
2. Đọc code backend của `API_CHOSEN` trong repo để lấy **request/response thật** (không đoán).
3. R1 → R2 → R3, ghi dần vào `test-design.md`.
4. Sinh D2/D3/D4 → chạy R4 local → sửa tới khi 0 fail.
5. Sinh D6, push C1/C2/C3, thu thập D7.
6. Hoàn tất R6, đóng gói D8.
