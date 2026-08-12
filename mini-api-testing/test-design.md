# Mini Exercise — POST /api/products — 23127207

## 0. API under test (evidence: code + curl log)

### Scope and fixed parameters

| Parameter | Value |
| --- | --- |
| MSSV / student ID | 23127207 |
| API selected | POST /api/products |
| API slug | products |
| Branch | Khoa-MiniExercise-API |
| Base URL | http://localhost:3000 |

The selected endpoint is the product-creation endpoint in backend/server.js. The implementation destructures name, price, description, imageUrl, and category_id, then inserts them through a parameterized SQLite statement. A successful response is { "message": "Product created", "id": <number> } with HTTP 200; an SQLite/runtime error can produce HTTP 500.

The products table has the columns id, name, price, description, imageUrl, and category_id. It has no NOT NULL, foreign-key, or positive-price constraint. Therefore this test design distinguishes the status required by the product-management specification from the status actually returned by the SUT.

### Verification evidence

The backend was checked locally before the collection and data file were written. The smoke request returned the seeded product iPhone 15 Pro Max as required. The following is the relevant raw output from the verification run (the generated IDs are local database IDs and are intentionally not used as test data):

    === smoke GET /api/products/1 ===
    STATUS 200
    {"id":1,"name":"iPhone 15 Pro Max","price":30000000,"description":"Điện thoại cao cấp của Apple","imageUrl":"https://placehold.co/300x300/png?text=iPhone+15","category_id":1}

    === full valid JSON ===
    STATUS 200
    CONTENT_TYPE application/json; charset=utf-8
    BODY {"message":"Product created","id":6}

    === empty object ===
    STATUS 200
    CONTENT_TYPE application/json; charset=utf-8
    BODY {"message":"Product created","id":7}

    === negative price ===
    STATUS 200
    CONTENT_TYPE application/json; charset=utf-8
    BODY {"message":"Product created","id":8}

    === object price ===
    STATUS 200
    CONTENT_TYPE application/json; charset=utf-8
    BODY {"message":"Product created","id":9}

    === benign XSS ===
    STATUS 200
    CONTENT_TYPE application/json; charset=utf-8
    BODY {"message":"Product created","id":10}

    === benign SQLi ===
    STATUS 200
    CONTENT_TYPE application/json; charset=utf-8
    BODY {"message":"Product created","id":11}

    === non-JSON form ===
    STATUS 500
    CONTENT_TYPE text/html; charset=utf-8
    BODY [empty]

The follow-up GETs confirmed that the benign SQLi and XSS values were stored as literal strings. For the object-valued price, the follow-up GET returned "price":"[object Object]"; it did not trigger the 400 validation that the product specification would require. The SQLi test is safe and was run only against the local SUT.

backend/package.json exposes start but not dev. Local verification therefore used node server.js, and the workflow uses the existing npm start script without changing backend code.

## 1. Bước 1 — Prompt đã dùng (nguyên văn)

    You are designing contract and functional API tests for one real endpoint only.

    API: POST http://localhost:3000/api/products
    Headers: Content-Type: application/json. The endpoint may also receive the
    student header X-Student-Id. Do not invent an Authorization requirement.

    Request body (happy-case example):
    {
      "name": "Wireless Mouse",
      "price": 250000,
      "description": "Ergonomic mouse",
      "imageUrl": "http://example.test/mouse.png",
      "category_id": 1
    }

    Happy response example: HTTP 200 (or the REST-correct creation status if the
    implementation proves it), JSON {"message":"Product created","id":11}.
    Error response example: HTTP 500, JSON {"error":"..."}. Other statuses may
    be proposed only when the input or implementation justifies them.

    Generate at least 12 independent test cases using equivalence partitioning,
    boundary-value analysis, state/workflow reasoning where applicable, security,
    and response-schema validation. Cover valid and invalid name/price/category_id
    values, price boundaries (0, negative, very large), missing fields, an unknown
    category, a benign SQL-injection string, a benign XSS string, and the distinction
    between a missing token (401), an invalid/expired token (401), and an ordinary
    user attempting an admin-only operation (403). For this selected endpoint,
    explicitly verify from the specification whether authentication is required.
    Include a POST-to-GET persistence workflow if the endpoint supports it.

    Use test names with the prefix Functional: for business behavior and Contract:
    for response/schema assertions. For each case, output exactly this table shape:
    tc_id | input | expected_status | expected_fields | rationale

    Use the real response contract {message:string, id:number} for a successful
    creation. If information is missing, list your assumption explicitly instead
    of inventing a field, authentication rule, or database constraint. Separate
    the status expected by the product specification from the status the SUT may
    actually return when the implementation is available.

## 2. Bước 1 — AI output (rút gọn, 16 TC)

The output below preserves the requested five columns. The expected_status values in this table are the initial specification-oriented expectations; the audit in the next section corrects them where the SUT evidence disagrees.

| tc_id | input | expected_status | expected_fields | rationale |
| --- | --- | ---: | --- | --- |
| TC-P-001 | Full five-field valid JSON; test name Functional: create valid product | 201 | message:string, id:number | Valid nominal partition; REST creation normally returns 201. |
| TC-P-002 | price = 0; test name Functional: reject zero price | 400 | error:string | Zero is outside the positive-price domain. |
| TC-P-003 | price = -1; test name Functional: reject negative price | 400 | error:string | Negative values are an invalid numeric partition. |
| TC-P-004 | price = 9007199254740992 (2^53); test name Functional: handle very large price | 400 | error:string or safe numeric handling | Exercises overflow/precision boundary. |
| TC-P-005 | Omit name; test name Functional: reject missing name | 400 | error:string | Required product name is missing. |
| TC-P-006 | name = empty string; test name Functional: reject empty name | 400 | error:string | Empty string is the invalid boundary for a required name. |
| TC-P-007 | price = abc; test name Functional: reject nonnumeric price | 400 | error:string | Price has the wrong data type. |
| TC-P-008 | category_id = 9999; test name Functional: reject unknown category | 400 or 404 | error:string | A product should reference an existing category. |
| TC-P-009 | No Authorization header; test name Functional: allow public product creation | 200 | message, id | Authentication must be checked against the selected API's stated contract. |
| TC-P-010 | Expired or malformed bearer token; test name Functional: reject invalid token | 401 | error:string | 401 is distinct from a role/permission failure, if auth applies. |
| TC-P-011 | Valid ordinary-user token on an admin-only operation; test name Functional: forbid non-admin | 403 | error:string | 403 must remain separate from missing/invalid credentials. |
| TC-P-012 | name = A'); DROP TABLE products;--; test name Functional: preserve SQLi as data | 200 | message, id | A parameterized query must not execute the benign SQLi payload. |
| TC-P-013 | name = <script>alert(1)</script>; test name Functional: handle benign XSS | 400 or sanitized value | error:string or safe value | The API/rendering boundary must not turn input into executable HTML. |
| TC-P-014 | Validate response against message:string,id:number; test name Contract: creation schema | 200 | message:string, id:number | Separates schema assertions from functional status assertions. |
| TC-P-015 | price = {"a":1}; test name Functional: reject object price | 400 | error:string | Object is an invalid partition for an integer price. |
| TC-P-016 | POST a product, then GET /api/products/:id; test name Functional: persist created product | 200 + 200 | POST message,id; GET matching fields | Verifies the created ID is usable and data was persisted. |

Assumptions surfaced by the output: the product-management requirement expects a positive price, a required name/category, and a REST creation response; authentication is not inferred for this endpoint because the API list does not state it. The token cases are retained for security reasoning and explicitly audited as not applicable to this public endpoint.

## 3. Bước 2 — Audit table

Every generated case has a review label. VALID means the test expectation is usable as written; INCOMPLETE means the idea is useful but needs an implementation-specific assertion or clarification; INVALID means its initial expectation or applicability is wrong for this endpoint.

| TC | Nhãn | Nhận xét hoặc chỉnh sửa |
| --- | --- | --- |
| TC-P-001 | INCOMPLETE | The valid payload is correct, but the SUT returns 200 and no Location header rather than the initial 201 expectation; retain the case and set actual status to 200, while recording BUG-03. |
| TC-P-002 | INCOMPLETE | The specification says 400 for zero, but the implementation has no validation and is expected to insert it; separate spec_status=400 from expected_status=200 in any executable data. |
| TC-P-003 | INCOMPLETE | The negative-price partition is valid, but evidence shows no validation; correct the executable expectation to 200 and record BUG-02. |
| TC-P-004 | INCOMPLETE | The boundary is useful, but the initial output did not define whether a JavaScript-safe integer or SQLite storage rule controls it; keep it as an exploratory case and do not include it in the five deterministic iterations. |
| TC-P-005 | INCOMPLETE | Missing name is a valid negative test, but the SUT accepts it because the column is nullable; executable status is corrected from 400 to 200 and BUG-02 is recorded. |
| TC-P-006 | INCOMPLETE | Empty-name behavior was not verified with a separate response body; code inspection shows no name validation, so the expectation is corrected to actual 200 and the case remains a BUG-02 candidate. |
| TC-P-007 | INCOMPLETE | The type partition is useful, but SQLite coercion/error behavior must be measured rather than assumed; do not use a guessed 400 in the executable five-case set. |
| TC-P-008 | INCOMPLETE | The table has no foreign-key constraint, so 9999 is not rejected by this SUT; correct the expected status to 200 and record the missing-FK observation separately. |
| TC-P-009 | VALID | The endpoint is public in the selected API description, so no token is the correct scenario and 200 is the correct observed expectation. This is OBS-01 (a risk recommendation), not an authentication defect. |
| TC-P-010 | INVALID | The AI assumed authentication for an endpoint that does not require it; this 401 case is not applicable to POST /api/products and is excluded from the executable collection. |
| TC-P-011 | INVALID | The 403 role-escalation case belongs to an admin-protected endpoint, not this public endpoint; it remains as coverage reasoning but is excluded and is not merged with the 401 case. |
| TC-P-012 | VALID | The benign SQLi case matches the prepared statement in the implementation; a successful 200 plus literal persistence is the correct result. |
| TC-P-013 | INCOMPLETE | The initial output did not identify whether sanitization belongs in the API or renderer; the API stores the literal payload, so record OBS-02 and keep the executable assertion focused on non-execution/storage. |
| TC-P-014 | VALID | The successful response contains exactly the two documented contract fields needed here, and the collection uses a JSON Schema assertion rather than hand-written type checks. |
| TC-P-015 | INVALID | The initial 400 assumption is contradicted by evidence: the SUT returns 200 and SQLite stores the object as a string-like value ([object Object] on GET). Correct the actual expectation to 200 and record the validation defect. |
| TC-P-016 | VALID | The POST-to-GET workflow is a valid persistence check, but it is kept out of the data-driven five-iteration collection so the required iteration count stays exactly five. |

### Corrections made during audit

1. TC-P-009 was corrected from a presumed 401 to 200 because this endpoint is public by the selected API specification (OBS-01).
2. TC-P-001 was corrected from 201 to the verified 200 returned by the SUT (BUG-03).
3. TC-P-005 and TC-P-003 were corrected from 400 to the verified 200 because the implementation has no input validation (BUG-02).
4. TC-P-015 was corrected from 400 to the verified 200; this is why the final data file never asserts the unverified 500 assumption from the original plan.

### Findings

- BUG-02 — missing input validation: name, price, and other product fields are accepted when missing or invalid even though the product-management specification requires validation.
- BUG-03 — non-standard creation status: successful creation returns 200 rather than 201 and does not provide a Location header.
- OBS-01 — public endpoint: no token is required, consistent with the selected API description; this is a risk/improvement recommendation, not a defect for this exercise.
- OBS-02 — API-layer HTML handling: a benign XSS payload is stored literally. The API does not render it, so the renderer must escape it; the payload was limited to the local environment.

## 4. Bước 3 — Extend (test cases tự viết)

| TC | Test name | Input and expected result | Vì sao AI bỏ sót |
| --- | --- | --- | --- |
| TC-EXT-001 | Functional: reject or safely handle wrong Content-Type | Send the same JSON text with Content-Type application/x-www-form-urlencoded; the observed SUT result is HTTP 500 with text/html, while a robust API contract would return a deliberate 415/400 JSON error. | The prompt emphasized the JSON body and the model treated Content-Type as implicit (prompt-quality omission). |
| TC-EXT-002 | Contract: response time below 1000ms | Assert pm.response.responseTime < 1000 for each data-driven request. This threshold is chosen to avoid the 500ms flakiness risk on a GitHub-hosted runner. | The model focused on functional partitions and did not add a non-functional performance assertion (model limitation). |
| TC-EXT-003 | Contract: creation uses REST status and Location policy | A successful creation should be 201 with a Location header; the SUT is observed to return 200 without Location. | The model described the happy response but did not inspect the implementation's REST-status behavior (SUT-specific omission). |

TC-EXT-001 and TC-EXT-002 are represented in the collection: the fifth iteration exercises the wrong Content-Type and every iteration has the [MINI] response-time assertion. TC-EXT-003 is documented as a contract finding rather than asserted as 201, because the Newman run must have zero failures against the current SUT.

## 5. Bước 4 — 5 case đã chọn and mapping

The data file contains exactly five objects, so Newman must run exactly five iterations. The body and content_type columns are read in the pre-request script; expected_status drives the status assertion; expect_id controls the success JSON Schema assertion. spec_status is deliberately informational and is not used as the executable expectation.

| Iteration | tc_id | Case | Actual status used | Spec/reference status | Assertions |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | TC-P-001 | Full valid five-field payload | 200 | 201 | Functional status, Contract {message,id}, JSON Content-Type, response time |
| 2 | TC-P-005 | Missing name | 200 | 400 | Functional status, Contract {message,id}, JSON Content-Type, response time |
| 3 | TC-P-003 | Negative price | 200 | 400 | Functional status, Contract {message,id}, JSON Content-Type, response time |
| 4 | TC-P-012 | Benign SQLi string in name | 200 | 200 | Functional status, Contract {message,id}, JSON Content-Type, response time |
| 5 | TC-EXT-001 | JSON text sent as form-urlencoded | 500 | 415 | Functional status and response time; no JSON schema assertion is made for the observed HTML error response |

The plan/guide mentions larger data sets, but the exercise checkpoint requires exactly five iterations. This implementation follows the hard checkpoint and documents the additional generated cases in the design and audit tables.

### Collection mechanics

- The request URL is {{baseUrl}}/api/products, where baseUrl is an environment variable. The collection variable apiPath=/api/products is retained in the raw URL string for traceability, but the parsed url.path segments are stored as ["api","products"].
- Defect found in our own test asset (not in the SUT): storing url.path as ["{{apiPath}}"] made Newman resolve the request to http://localhost:3000//api/products (a doubled slash), which Express 5 answers with 404 HTML. All five iterations failed (14 assertions executed, 9 failed) until the path segments were split. Lesson: a collection variable that already contains a leading slash must not be reused as a single path segment.
- The pre-request script includes the required X-Student-Id upsert and builds bodyJson from the current iteration's body object.
- The test script reads pm.iterationData.get("expected_status"), uses Functional: for business/status assertions, Contract: for schema assertions, and [MINI] for response time and Content-Type checks.
- The exact local command that produced the committed report is:

    newman run mini-api-testing/mini-products.postman_collection.json \
      --environment mini-api-testing/mini-local.postman_environment.json \
      --iteration-data mini-api-testing/mini-products.data.json \
      --reporters cli,json \
      --reporter-json-export mini-api-testing/mini-newman-report.json \
      --verbose

For the flattened submission zip, the corresponding command uses the three JSON files at the zip root and exports mini-newman-report.json at that same root.

## 6. Bước 5 — CI/CD

.github/workflows/newman-api-test.yml performs checkout, Node 20 setup, npm ci with an npm install fallback in backend, starts the existing npm start script in the background, waits for /api/products/1, installs Newman globally, runs the five-iteration collection, and uploads mini-newman-report.json (plus the backend log on failure).

The three-commit evidence sequence was executed on branch Khoa-MiniExercise-API of https://github.com/trngnneee/eshop-sut:

| Commit | Message | Actions run | Result |
| --- | --- | --- | --- |
| 53f5827a | C1: Mini API testing - collection, data, newman report, CI workflow | #9 | Failure (infrastructure defect, see below) |
| 859a20d8 | C1 fix: tolerate out-of-sync backend lock file in CI | #10 | Success, newman-report artifact 5.32 kB |
| 08d9727c | C2: intentionally break expected_status to demonstrate CI failure | #11 | Failure, exit code 1 — captured as ci-fail.png |
| 9c447c76 | Revert "C2: ..." (C3 recovery) | #12 | Success — captured as ci-pass.png; final commit is green |

C2 changed only TC-P-001 expected_status from 200 to 999; C3 restored it with git revert so the history keeps both the break and the recovery explicit.

### Defect found by CI that local execution missed

Run #9 failed at the "Install backend dependencies" step:

    npm error `npm ci` can only install packages when your package.json and
    npm error package-lock.json ... are in sync.
    npm error Missing: picomatch@4.0.5 from lock file

The same npm ci command succeeds on the development machine, which runs npm 11.6.1; the GitHub-hosted runner uses the npm bundled with Node 20, which enforces lock-file consistency more strictly. This is exactly the class of defect a pipeline is supposed to surface: an environment-dependent failure invisible to local testing.

The fix was applied in the workflow (npm ci || npm install) rather than by regenerating backend/package-lock.json, because modifying the SUT is out of scope for this exercise and the lock file is shared with the rest of the group.

D5 status: mini-newman-report.json is genuine output of the official Newman JSON reporter (newman 6.2.2) against the local backend on 2026-08-10. Verified counts: 5 iterations (0 failed), 18 assertions (0 failed), every request resolved to http://localhost:3000/api/products, and the X-Student-Id: 23127207 header is present on all five executions.

D7 status: DONE. ci-pass.png is Actions run #12 (the final, reverted commit 9c447c7, Success) and ci-fail.png is run #11 (commit 08d9727, Failure). Both are screenshots of real runs on the group repository.

## 7. Bước 6 — Postman features

| Feature | Đã dùng? | Ghi chú |
| --- | --- | --- |
| Collections | Có | mini-products.postman_collection.json groups the selected API request and its scripts. |
| Environment variables | Có | baseUrl and studentId are stored in mini-local.postman_environment.json. |
| Collection variables | Có | apiPath is used in the request URL and createdProductId is available for future workflow extensions. |
| Pre-request scripts | Có | The script attaches X-Student-Id, selects the iteration Content-Type, and serializes the body. |
| Test scripts | Có | Functional, schema, response-time, and Content-Type assertions are defined in the collection. |
| Data-driven runs | Có | mini-products.data.json provides exactly five independent iterations. |
| Newman CLI | Có | The workflow and local command run the collection headlessly and export JSON. |
| Monitors | Không | A local submission exercise does not need a scheduled Postman monitor. |
| Mock servers | Không | The real local backend is the provider under test, so a mock would obscure SUT behavior. |
| Workspaces | Không | No shared Postman workspace is required for the repository artifact. |
