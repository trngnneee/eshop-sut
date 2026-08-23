Faculty of Information Technology (FIT) – Ho Chi Minh City University of Science (HCMUS)

CS423 / CSC13003 – Software Testing (AI-augmented · 2026)

AI POLICY · TEMPLATES — 2026 v1.0

# AI Use Disclosure Form

Attach to assignments where AI was used in any permitted capacity.

Adapted from Med Kharbach, PhD (2026) — AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0. This adaptation is prepared for FIT@HCMUS – CS423 / CSC15003 Software Testing course.

## 1. Course & Student Info

| Field | Value |
| --- | --- |
| Course: | CS423 / CSC13003 – Software Testing |
| Assignment ID: | HW06 — API Testing |
| Assignment Title: | API Testing on EShop (SUT) — 3 APIs: FR-05/06, FR-10, FR-15 |
| AI Use Category (1–5): | Category |
| Date: | 22/08/2026 |
| Student name: | Dang Truong Nguyen |
| Student ID: | 23127438 |

## 2. Disclosure Questions

### 1. AI tool(s) used:

- Claude Code (Claude Opus 5, 1M context)

### 2. Stage(s) of the assignment where AI was used:

Tick all that apply: [x] brainstorming  [x] outlining  [x] drafting  [x] feedback  [x] revision  [x] coding  [x] data analysis  [ ] visual design  [ ] other (specify).

AI drafted the implementation plan, converted the API specification to OpenAPI (`openapi.yaml`), wrote four reusable JSON Schemas, and generated the API-1 and API-2 test-case groups (partitioning, boundary, state-transition, security, schema, negative/contract). I set the scope and the technique for each step, drove the AI one technique at a time, ran the SUT locally and probed every endpoint with cURL to establish the real "actual" behaviour myself, decided the STRICT contract convention (DEC-01), and made every expected-result and severity decision. The self-drawn AI-test-generator diagram (Agent Skill, Step 9) is designed by me, not AI-generated.

### 3. Main prompts or tasks given to the AI:

Paste the 2–3 most impactful prompts verbatim. For the full transcript, attach Appendix A (the AI Audit Report Section 3).

The full prompt set is in the AI Audit Report (Section 3), pasted verbatim. The 3 most impactful:

1. **Prompt — EP + BVA for API-1**

   Ok làm API-1: GET /api/products/:id. Đi theo kỹ thuật phân hoạch tương đương + phân tích giá trị biên. Với mỗi tham số t muốn m tách hẳn 1 bảng partition rồi mới ra test case: Path param :id → id tồn tại (thử cả id LẺ và id CHẴN, t nghi có logic khác nhau), không tồn tại (99999), biên 1/0/-1, số cực lớn, 1.5, "abc", rỗng, có khoảng trắng, chuỗi cực dài. Query ?search= → rỗng, khớp 1, khớp nhiều, không khớp, ký tự % và _ (wildcard LIKE), unicode tiếng Việt có dấu, chuỗi rất dài. Nhớ: id không tồn tại theo FR-06 expected phải 404 — kể cả khi m đoán code trả khác. TC-ID TC-P1-001...

2. **Prompt — Security (SEC-04/05)**

   Vẫn API-1. Giờ sinh riêng nhóm test bảo mật, bám các mã SEC, đừng nói chung chung "kiểm tra bảo mật": SEC-05 SQL Injection ở ?search= — thử payload cụ thể ' OR '1'='1 , '; DROP TABLE products;-- , %' UNION SELECT ... — mỗi payload ghi rõ assertion (số record trả về, có lộ HTML lỗi/stacktrace không). SEC-04 XSS: nếu search echo lại từ khóa thì thử <script>alert(1)</script>, assert có bị escape không. Rò rỉ thông tin: payload gây lỗi SQL trả HTML <h1>Database Error</h1> kèm message → phá contract JSON. Mỗi case ghi payload thật + assertion thật. TC-P1-###

3. **Prompt — Schema validation**

   Vẫn API-1. Viết JSON Schema cho response detail rồi sinh test dùng pm.response.to.have.jsonSchema(...). Response đúng phải có ĐÚNG 6 field: id, name, price, description, imageUrl, category_id — không dư field lạ. Chú ý: price BẮT BUỘC là number (t nghi có id trả price ra string, nếu vậy là bug, cứ để expected = number). Cho t test cả: schema đúng, Content-Type: application/json, response time < 2000ms.

### 4. Specific parts of the work AI contributed to:

Be specific. Example: 'AI generated TC01–TC15 in Section 3.2; I rewrote TC04 and TC11; AI did NOT contribute to Sections 1, 2, 4, or the AI Critique.'

Claude Code generated `plan.md`, `openapi.yaml`, the four reusable JSON Schemas under `postman/schemas/` (product, product-list, message-response, error-response), the four **API-1** files (TC-P1-001→083), the five **API-2** files (TC-O2-001→057), and the three **API-3** files (TC-P3-001→072: input-validation, security, schema), and the consolidated `testcases/00-TestCases-Summary.md` — **219 test cases** total after my Step-3 audit (de-duplication) and Step-4 extend passes. I decided the scope (3 APIs), the technique sequence, and DEC-01 (STRICT id validation); I ran the SUT and produced all cURL evidence for the "actual" columns (including forging JWTs with the leaked secret and probing all 5 order states); I wrote `docs/openapi-audit.md` correcting 5 AI mismatches. AI did NOT contribute to: the scope/technique decisions, the expected-result oracle, the self-drawn generator diagram, or the AI Critique. All three in-scope APIs are covered; remaining HW06 steps (Postman collection assembly, Newman run, CI/CD, agent-skill generator) are pending.

### 5. How I reviewed, revised, or verified the AI output:

Describe your verification method (ran the test, checked the spec, asked the TA, looked up RFC, cross-checked with the ISTQB syllabus, etc.).

- I stood up the SUT (`node server.js`, localhost:3000) and probed every endpoint with cURL, backing up `database.sqlite` before destructive tests and restoring it after. This caught claims the AI could not derive from the spec: BUG-07 (admin product routes have no auth), BUG-01 (`id % 2` coerces price to string), BUG-20 (UNION SQLi leaks admin credentials), and the forged-token verdict error in `openapi.yaml` (AI said 403; actual is 200).
- I validated `openapi.yaml` with Redocly (0 errors) and validated both JSON Schemas with Python `jsonschema` (Draft7Validator) against known-good and known-bad samples to prove they catch BUG-01/02 and extra fields.
- For API-2 I forged JWTs with the leaked secret (`server.js:9`) using `jsonwebtoken` and drove the full order state machine (checkout → admin status updates) to reach each of the 5 states, confirming BUG-05 (user cancels a shipping order) and BUG-13 (forged-id token cancels another user's order).
- I cross-checked expected results against the README FR spec and cited ISTQB / RFC 9110 / RFC 8259 / RFC 7519 in the audit reasoning column.

### 6. Citation (if required by course style guide):

Software Testing uses the IEEE style. Example: Anthropic. (2026). AI Tool (e.g., ChatGPT, Claude, Gemini) [Large language model]. https://claude.ai

1. Anthropic. (2026). Claude (Claude Opus 5) [Large language model]. https://claude.ai

## 3. Statement of Honesty

By signing below, I confirm that the disclosure above is accurate and complete. I understand that undisclosed or false disclosure of AI use is treated as academic misconduct and may result in a 0 grade for the assignment and disciplinary referral.

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
