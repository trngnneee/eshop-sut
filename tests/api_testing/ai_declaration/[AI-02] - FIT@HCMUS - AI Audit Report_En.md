Faculty of Information Technology (FIT) – Ho Chi Minh City University of Science (HCMUS)

CS423 / CSC13003 – Software Testing (AI-augmented · 2026)

AI POLICY · TEMPLATES — 2026 v1.0

# AI Audit Report — HW06: API Testing (EShop)

Mandatory appendix for every AI-assisted homework (HW#01–HW#06, and Seminar).

Adapted from Med Kharbach, PhD (2026) — AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0. This adaptation is prepared for FIT@HCMUS – CS423 / CSC15003 Software Testing course.

## 1. Student Information

| Field | Value |
| --- | --- |
| Student name (printed): | DANG TRUONG NGUYEN |
| Student ID: | 23127438 |
| Class / Cohort: | 23KTPM3 |
| Assignment ID (e.g., HW#00, HW#02): | HW06 — API Testing |
| Assignment date: | 22/08/2026 |
| AI tool(s) used: | Claude Code (Claude Opus 5, 1M context) |
| AI tool(s) used: | [X] Yes  [ ] No |

## 2. Instructions (read before filling)

- Add one row per AI-generated artifact (test case, script, checklist, OpenAPI spec, JMeter plan, etc.).
- Paste the verbatim prompt — DO NOT paraphrase.
- Paste the verbatim AI output (or include a labelled screenshot in the report).
- Tag the verdict: VALID / INVALID / INCOMPLETE.
- Reasoning must cite a course slide, ISTQB section, or technical RFC.
- Show the corrected artifact with the change highlighted.
- Sample rows are in italic — replace them before submission.

## 3. Audit Table — one row per artifact

Scope of HW06 = 3 APIs: **API-1** `GET /api/products/:id` (+ list/search) — FR-05/06; **API-2** `PUT /api/orders/:id/cancel` — FR-10; **API-3** `POST /api/products` + `PUT /api/products/:id` — FR-15. All prompts below are verbatim as I typed them in Claude Code (Vietnamese, informal); `<<...>>` marks context the agent read from the repo itself at run time. The AI was driven step-by-step per technique (partition → boundary → security → schema → negative), never with a single "generate all test cases" prompt.

| (1) Prompt + Tool | (2) AI Output | (3) Verdict | (4) Reasoning (ISTQB / RFC) | (5) Student Fix |
| --- | --- | --- | --- | --- |
| __Tool:__ Claude Code (Claude Opus 5)<br>__Date:__ 22/08/2026<br>__Artifact:__ Bước 0 · Plan + scope 3 API<br>__Prompt (verbatim):__<br>hãy đọc đề bài, kết hợp source code của eshop và viết plan.md các bước thực hiện bài tập, plan này không nằm trong repo và sẽ ko push chung lên github<br>api giới hạn lại phạm vi này: FR-05 GET /api/products/:id) &#124; FR-10 PUT /api/orders/:id/cancel &#124; FR-15 POST /api/products[/:id] &#124; | `plan.md` (ngoài repo): pipeline 11 bước, timeline 10h, bảng bug §11 (BUG-01→13) đã probe live bằng cURL, checklist nộp bài. Chỉ ra nhãn FR lệch (GET /api/products/:id thực chất là FR-06, không phải FR-05). | INCOMPLETE | ISTQB FL – test planning & test basis: kế hoạch phải bám test basis thật (README FR + source), và scope phải khớp đặc tả. AI ánh xạ FR chưa chính xác vì đề và README dùng số FR khác nhau. | Tôi đối chiếu lại README của SUT, xác nhận FR-05 = list/search, FR-06 = detail; sửa các mismatch trong bố cục scope trước khi tiếp tục (tôi báo lại "t đã sửa các mismatch của m"). |
| __Tool:__ Claude Code (Claude Opus 5)<br>__Date:__ 22/08/2026<br>__Artifact:__ Bước 1 · OpenAPI spec<br>__Prompt (verbatim):__<br>t đã có api_specification, hãy convert ra openapi.yaml | `openapi.yaml` (OpenAPI 3.0.3) cho 3 API + fixtures; quy ước "Contract = spec (FR), hành vi sai của SUT ghi trong `x-sut-actual`"; nhúng `x-test-partitions`, `x-test-state-matrix`, `x-test-security-matrix`. Redocly lint: valid, 0 error. | INCOMPLETE | Contract testing: OpenAPI đóng vai test oracle, mọi field phải khớp test basis (`database.js` schema) và response thật. RFC 8259 (JSON) cho kiểu dữ liệu. | Tôi dựng SUT chạy live, đối chiếu từng field và viết `docs/openapi-audit.md` liệt kê 5 sai (M1–M5): rõ nhất là **M2** — AI ghi forged-token → `403`, nhưng thực tế chữ ký hợp lệ (secret lộ ở `server.js:9`) nên `jwt.verify` PASS ⇒ `200` (escalation thật). Tôi sửa lại toàn bộ 5 chỗ. |
| __Tool:__ Claude Code (Claude Opus 5)<br>__Date:__ 22/08/2026<br>__Artifact:__ API-1 · EP + BVA<br>__Prompt (verbatim):__<br>Ok làm API-1: GET /api/products/:id. Đi theo kỹ thuật phân hoạch tương đương + phân tích giá trị biên. Với mỗi tham số t muốn m tách hẳn 1 bảng partition rồi mới ra test case: Path param :id → id tồn tại (thử cả id LẺ và id CHẴN, t nghi có logic khác nhau), không tồn tại (99999), biên 1/0/-1, số cực lớn, 1.5, "abc", rỗng, có khoảng trắng, chuỗi cực dài. Query ?search= → rỗng, khớp 1, khớp nhiều, không khớp, ký tự % và _ (wildcard LIKE), unicode tiếng Việt có dấu, chuỗi rất dài. Nhớ: id không tồn tại theo FR-06 expected phải 404 — kể cả khi m đoán code trả khác. TC-ID TC-P1-001... | `API-1_TestCases.md`: 2 bảng partition (18 lớp cho `:id`, 19 lớp cho `?search=`) + 44 test case (TC-P1-001→044); probe live phát hiện 5 bug mới (BUG-14→18), gồm BUG-16 (tìm kiếm chữ HOA có dấu → 0 kết quả). | INCOMPLETE | ISTQB FL 4.2 – Black-box: Equivalence Partitioning + Boundary Value Analysis; expected result lấy từ test basis (spec), không lấy từ hành vi quan sát (SUT). | Bảng ban đầu để `1.0 → expected 200` (theo hành vi SUT) trong khi các dạng không canonical khác để 400 — mâu thuẫn nội bộ. Tôi yêu cầu chốt một quy ước thống nhất (dẫn tới DEC-01, hàng dưới). |
| __Tool:__ Claude Code (Claude Opus 5)<br>__Date:__ 22/08/2026<br>__Artifact:__ API-1 · bổ sung path list/search vào OpenAPI<br>__Prompt (verbatim):__<br>openapi.yaml thiếu path GET /api/products. File hiện chỉ có /api/products với method POST. Thiếu nó thì 19 case nhóm ?search= không có contract để đối chiếu, và generator ở Bước 9 không sinh được. thêm cái này | Thêm `operationId: listProducts` với 3 response (200 array / 400 param lặp / 500 leak lỗi), 19 lớp `x-test-partitions.search`, `x-cross-endpoint-check` (list vs detail cho BUG-01). Redocly valid. | VALID | Test basis completeness: mỗi test case phải map tới một mục đặc tả; thiếu path list thì 19 case search không có oracle. | Không cần sửa — tôi kiểm tra lại bằng Redocly (0 error) và xác nhận 19 lớp khớp 1:1 với bảng partition trong file test case. |
| __Tool:__ Claude Code (Claude Opus 5)<br>__Date:__ 22/08/2026<br>__Artifact:__ API-1 · DEC-01 chốt strict/lenient<br>__Prompt (verbatim):__<br>oke sửa lại Vấn đề 1.0 / " 1" / "+1" / "01" — strict (400) hay lenient (200) | Chốt **STRICT** (mọi chuỗi `:id` không canonical → 400); ghi `x-contract-decision` (ADR) trong OpenAPI; đồng bộ 5 test case + BUG-14 giữa hai file; đếm lại verdict (23 FAIL / 21 PASS). | VALID | Test oracle & spec ambiguity (ISTQB FL – expected results): khi spec mơ hồ, quyết định oracle phải nhất quán và ghi lại lý do; `type: integer, minimum: 1` đọc chặt ⇒ reject dạng không canonical. | Đây là quyết định của tôi; AI thực thi và cross-fix đúng cả hai file. Tôi xác nhận không còn ⚠ lẫn lộn strict/lenient trong suite. |
| __Tool:__ Claude Code (Claude Opus 5)<br>__Date:__ 22/08/2026<br>__Artifact:__ API-1 · Security (SEC-04/05)<br>__Prompt (verbatim):__<br>Vẫn API-1. Giờ sinh riêng nhóm test bảo mật, bám các mã SEC, đừng nói chung chung "kiểm tra bảo mật": SEC-05 SQL Injection ở ?search= — thử payload cụ thể ' OR '1'='1 , '; DROP TABLE products;-- , %' UNION SELECT ... — mỗi payload ghi rõ assertion (số record trả về, có lộ HTML lỗi/stacktrace không). SEC-04 XSS: nếu search echo lại từ khóa thì thử &lt;script&gt;alert(1)&lt;/script&gt;, assert có bị escape không. Rò rỉ thông tin: payload gây lỗi SQL trả HTML &lt;h1&gt;Database Error&lt;/h1&gt; kèm message → phá contract JSON. Mỗi case ghi payload thật + assertion thật. TC-P1-### | `API-1_Security_TestCases.md`: 14 case (TC-P1-045→058) đã probe live. Phát hiện **BUG-20** (UNION SELECT rút bảng users, lộ email + password plaintext + role của admin qua 1 GET không auth) và xác nhận BUG-04 (500 + HTML + `SQLITE_ERROR`). | VALID | SEC-05 (parameterized query) / SEC-04 (output encoding); ISTQB FL – security testing; OWASP A03 Injection. Đánh giá đúng: XSS ở tầng API không khai thác được vì API không echo từ khóa. | Không cần sửa nội dung; tôi tự probe bằng cURL (backup + restore DB), xác nhận payload DROP vô hại (SQLite `db.all` chỉ chạy statement đầu) và kiểm chứng credential leak thật trước khi ghi assertion. |
| __Tool:__ Claude Code (Claude Opus 5)<br>__Date:__ 22/08/2026<br>__Artifact:__ API-1 · Schema validation<br>__Prompt (verbatim):__<br>Vẫn API-1. Viết JSON Schema cho response detail rồi sinh test dùng pm.response.to.have.jsonSchema(...). Response đúng phải có ĐÚNG 6 field: id, name, price, description, imageUrl, category_id — không dư field lạ. Chú ý: price BẮT BUỘC là number (t nghi có id trả price ra string, nếu vậy là bug, cứ để expected = number). Cho t test cả: schema đúng, Content-Type: application/json, response time &lt; 2000ms. Ra JSON Schema trước, rồi bảng TC-P1-###. | `product.schema.json` + `product-list.schema.json` (draft-07, `additionalProperties:false`, `price:number`) + `API-1_Schema_TestCases.md` 16 case (TC-P1-059→074). Schema kiểm chứng bắt đúng BUG-01/02 + dư field. | VALID | Contract/schema validation; JSON Schema draft-07; RFC 8259 (JSON types). Một `jsonSchema()` bắt đồng thời sai kiểu + thiếu field + dư field. | Không cần sửa; tôi chạy `jsonschema` (Draft7Validator) trên 4 mẫu để xác minh schema PASS id lẻ, FAIL id chẵn (price string), FAIL `{}`, FAIL object dư field `role`. |
| __Tool:__ Claude Code (Claude Opus 5)<br>__Date:__ 22/08/2026<br>__Artifact:__ API-1 · Negative / Contract<br>__Prompt (verbatim):__<br>Chốt API-1 bằng nhóm negative/contract: Sai method: POST /api/products/1 (route này có tồn tại không?), DELETE lên detail. Header Accept: application/xml xem có đổi định dạng không. Thiếu header X-Student-Id. Bảng TC-P1-### | `API-1_Negative_Contract_TestCases.md`: 9 case (TC-P1-075→083) + bản đồ method đầy đủ. Xác nhận POST/PATCH → 404 HTML (BUG-15); DELETE /api/products/1 → xoá thật, không auth (BUG-07); Accept & X-Student-Id → SUT bỏ qua (PASS, không phóng đại thành bug). | INCOMPLETE | ISTQB FL – negative testing; RFC 9110 §15.5.6 (405 Method Not Allowed vs 404); content negotiation. | Probe lần đầu bị lỗi: `DELETE /api/products/1` xoá mất product 1 nên các GET Accept/X-Student-Id sau đó trả `{}` sai lệch. Tôi phát hiện, khôi phục DB, **probe lại theo đúng thứ tự (read trước, destructive sau)** để lấy số liệu đúng, và ghi rõ DELETE là destructive trong PRE-DESTRUCT. |

## 4. Summary of AI Accuracy

Aggregate the verdicts from Section 3 and complete the table below.

| Metric | Count | Percentage |
| --- | --- | --- |
| Total AI-generated artifacts audited | 8 | 100% |
| VALID (correct, accepted as-is) | 4 | 50% |
| INVALID (wrong; rejected) | 0 | 0% |
| INCOMPLETE (acceptable after edits) | 4 | 50% |

> Note: no artifact was wholesale INVALID, but two INCOMPLETE artifacts contained **factually wrong claims** that only live verification caught: the forged-token verdict in `openapi.yaml` (403 claimed vs 200 actual) and my own probing-order error in the Negative group (a destructive DELETE contaminated later reads). Both are logged above verbatim; neither was accepted before correction.

## 5. Conclusion — When should AI be used (or not)?

Write 80–150 words describing patterns you observed. Where did AI shine? Where did AI fail? What is your recommendation for using AI in this kind of work in the future?

AI was strong at the mechanical breadth of black-box design — enumerating equivalence classes and boundary values, drafting JSON Schemas, and structuring the OpenAPI contract — work that is tedious but rule-based. It was weak wherever the correct answer depended on the *implementation* rather than the spec: it assumed admin endpoints were authenticated (missing BUG-07), it could not imagine the `id % 2` price-coercion, and it predicted a forged token would be rejected when the leaked secret makes it succeed. Every one of those was caught only by running the SUT and probing with cURL, never by reasoning about the spec. My rule going forward: let AI generate the input space and the contract, but derive every *expected result* from the test basis and confirm every *actual result* by execution — the human owns the oracle, the AI owns the enumeration.

## 6. Mandatory Disclosure (paste verbatim)

For HW06, Claude Code drafted the implementation plan, the OpenAPI contract (`openapi.yaml`), the two reusable JSON Schemas, and the four API-1 test-case groups (Equivalence Partitioning + Boundary Value Analysis, Security, Schema validation, Negative/Contract — 83 test cases, TC-P1-001→083). I set the scope and technique for every step, drove the AI one technique at a time (never a single "generate all" prompt), and personally verified every result: I ran the SUT locally and probed all endpoints with cURL, corrected the OpenAPI mismatches (documented in `docs/openapi-audit.md`), decided the STRICT contract convention (DEC-01), and re-probed after a destructive test contaminated my data. All "actual" behaviour recorded in the test cases is from real execution on localhost:3000, with the seeded database backed up and restored. The detailed prompt log is Section 3 above. I confirm I did not use AI to generate any artifact in the prohibited category.

## Signature

| Student name (printed): | DANG TRUONG NGUYEN |
| --- | --- |
| Student ID: | 23127438 |
| Class / Cohort: | 23KTPM3 |
| Course: | CS423 / CSC13003 – Software Testing |
| Instructor: | Msc. Tran Thi Bich Hanh |
| Date: | 22/08/2026 |
| Signature: | ![signature](./signature.png) |

## References

- Kharbach, M. (2026). AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0.
- ISTQB Foundation Level Syllabus (latest version).
- Hardman, P. (2025). A Post-AI Learning Taxonomy.
- Fuster Rabella, M. (2025). OECD Education Working Paper No. 338.
- Perkins, M., Roe, J., & Furze, L. (2025). AI Assessment Scale.
- Anthropic (2025). Building reliable AI test agents — engineering blog.
- DeepEval & Promptfoo documentation — testing frameworks for LLM systems.
