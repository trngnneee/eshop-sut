# Test Cases – API 3 (Pool C)

**Sinh viên:** Phan Quốc Thịnh – 23127486 – 23KTPM3  
**Feature:** FR-16 – Import sản phẩm từ JSON (Admin)  
**Endpoint:** `POST /api/admin/import-products`

---

## Tổng quan

| Mục | Giá trị |
|:---|:---|
| **API** | POST /api/admin/import-products – Import sản phẩm hàng loạt |
| **Pool** | C |
| **Tổng TC (AI sinh)** | 38 (DP/BVA: 15 \| ST: 8 \| SEC: 8 \| SV: 7) |
| **TC tự thêm** | 7 (TC-C-EXT-01 đến TC-C-EXT-07) |
| **Tổng TC** | 45 |

---

## Phân loại test cases

### A. Domain Partition & Boundary Value Tests (EP & BVA)

| TC ID | Mô tả | Tham số kiểm tra | Phân vùng / Điểm biên | Input Payload (Params/Body) | Expected HTTP Status & Output | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|:---|
| TC-C-DP-01 | Import hợp lệ – 1 sản phẩm đầy đủ trường | products array (1 item) | Valid EP – happy path | `{"products":[{"name":"SP1","price":10000,"description":"Mo ta","imageUrl":"","category_id":1}]}` + admin token | 200 OK – import thành công | **VALID** | Happy path đầy đủ trường. |
| TC-C-DP-02 | Import hợp lệ – nhiều sản phẩm cùng lúc | products array (nhiều item) | Valid EP – batch | `{"products":[{...},{...},{...}]}` + admin token | 200 OK – tất cả được tạo | **VALID** | Batch import là use case chính của endpoint này. |
| TC-C-DP-03 | products là mảng rỗng (BVA tại 0 item) | products | BVA – empty array | `{"products":[]}` + admin token | 400 Bad Request – không có sản phẩm để import | **INCOMPLETE** | Expected "400" giả định hệ thống reject empty array, nhưng có thể là 200 OK với thông báo "0 sản phẩm được import". **Sửa:** Xác nhận từ spec: nếu business rule yêu cầu ≥1 sản phẩm → 400; nếu không → 200 OK + `{"imported":0}`. |
| TC-C-DP-04 | Thiếu trường `name` trong sản phẩm | name | Invalid EP – missing field | `{"products":[{"price":10000,"description":"Mo ta","imageUrl":"","category_id":1}]}` + admin token | 400 Bad Request – thiếu name | **VALID** | Cô lập lỗi đúng: thiếu required field name. |
| TC-C-DP-05 | `name` là chuỗi rỗng | name | Invalid EP – empty string | `{"products":[{"name":"","price":10000,"description":"Mo ta","imageUrl":"","category_id":1}]}` + admin token | 400 Bad Request – name không hợp lệ | **VALID** | Empty string vs missing key – cô lập lỗi đúng. |
| TC-C-DP-06 | Thiếu trường `price` trong sản phẩm | price | Invalid EP – missing field | `{"products":[{"name":"SP1","description":"Mo ta","imageUrl":"","category_id":1}]}` + admin token | 400 Bad Request – thiếu price | **VALID** | Cô lập lỗi đúng. |
| TC-C-DP-07 | `price` = 0 (BVA tại 0) | price | BVA – zero | `{"products":[{"name":"SP1","price":0,"description":"Mo ta","imageUrl":"","category_id":1}]}` + admin token | 400 Bad Request hoặc 200 (tuỳ rule giá ≥ 0 hay > 0) | **INCOMPLETE** | Expected hai khả năng không thể tự động hóa. **Sửa:** Xác định rule từ spec: nếu price phải > 0 → expected 400; nếu ≥ 0 → expected 200 OK. |
| TC-C-DP-08 | `price` âm (BVA dưới 0) | price | BVA – negative | `{"products":[{"name":"SP1","price":-1,"description":"Mo ta","imageUrl":"","category_id":1}]}` + admin token | 400 Bad Request – giá không hợp lệ | **VALID** | Giá âm là invalid EP rõ ràng – không có business logic nào chấp nhận giá âm. |
| TC-C-DP-09 | `price` là string thay vì number | price | Invalid EP – wrong type | `{"products":[{"name":"SP1","price":"10000","description":"Mo ta","imageUrl":"","category_id":1}]}` + admin token | 400 Bad Request – sai kiểu dữ liệu | **VALID** | Type mismatch: string vs number – đúng EP invalid. |
| TC-C-DP-10 | Thiếu trường `category_id` | category_id | Invalid EP – missing field | `{"products":[{"name":"SP1","price":10000,"description":"Mo ta","imageUrl":""}]}` + admin token | 400 Bad Request – thiếu category_id | **VALID** | Required FK field bị thiếu. |
| TC-C-DP-11 | `category_id` không tồn tại | category_id | Invalid EP – non-existent FK | `{"products":[{"name":"SP1","price":10000,"description":"Mo ta","imageUrl":"","category_id":9999}]}` + admin token | 400 Bad Request – category không tồn tại | **VALID** | FK constraint violation – important để đảm bảo referential integrity. |
| TC-C-DP-12 | `products` không phải array (là object) | products | Invalid EP – wrong type | `{"products":{"name":"SP1","price":10000}}` + admin token | 400 Bad Request – sai kiểu | **VALID** | Type validation cho top-level field products. |
| TC-C-DP-13 | Body là JSON rỗng `{}` | products | Invalid EP – missing key | `{}` + admin token | 400 Bad Request – thiếu trường products | **VALID** | Missing required key products. |
| TC-C-DP-14 | Import 1 sản phẩm với `imageUrl` rỗng (nullable) | imageUrl | Valid EP – nullable field | `{"products":[{"name":"SP1","price":10000,"description":"Mo ta","imageUrl":"","category_id":1}]}` | 200 OK – imageUrl rỗng được chấp nhận | **VALID** | Nullable field validation – imageUrl có thể empty. |
| TC-C-DP-15 | Import rất nhiều sản phẩm (BVA số lượng lớn – 100 items) | products array size | BVA – large batch | `{"products":[{...}x100]}` + admin token | 200 OK hoặc 413 Payload Too Large | **INCOMPLETE** | Expected hai khả năng không cụ thể. **Sửa:** Kiểm tra server max payload size; nếu không có giới hạn cụ thể → expected 200 OK; nếu có limit → expected 413. |

### B. State Transition & Lifecycle Tests (Admin / CRUD)

| TC ID | Mô tả kịch bản | Trạng thái ban đầu (Pre-state) | Hành động / Payload | Trạng thái kỳ vọng (Post-state) | Expected HTTP Status & Error Code | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|:---|
| TC-C-ST-01 | Sản phẩm Non-existent → Created sau khi import | Non-existent | POST import với 1 sản phẩm hợp lệ | Sản phẩm tồn tại trong DB (có thể GET /api/products) | 200 OK – import thành công | **VALID** | Resource Lifecycle: Non-existent → Created đúng. |
| TC-C-ST-02 | Import xong kiểm tra sản phẩm xuất hiện trong danh sách | Non-existent | POST import → GET /api/products | Sản phẩm mới xuất hiện trong danh sách | GET: 200 OK có sản phẩm mới | **VALID** | State sequence: Created → Active → visible in product list. |
| TC-C-ST-03 | Import khi không có token – từ chối | Unauthenticated | POST /api/admin/import-products không có token | Unauthenticated – không import | 401 Unauthorized | **VALID** | Auth State: Unauthenticated → reject. |
| TC-C-ST-04 | Import với token user thường – từ chối | Authenticated (non-admin) | POST import với user token | Forbidden – không import | 403 Forbidden | **VALID** | Auth State: Authenticated non-admin → 403. Quan trọng cho access control. |
| TC-C-ST-05 | Import với admin token – thành công | Authenticated (admin) | POST import với admin token + valid data | Sản phẩm được tạo | 200 OK | **VALID** | Auth State: Authenticated admin → thành công. |
| TC-C-ST-06 | Token hết hạn – bị từ chối | Token Expired | POST import với expired token | Unauthenticated | 401 Unauthorized | **VALID** | Auth State: Expired → 401. |
| TC-C-ST-07 | Import trung lập (idempotency) – import cùng payload 2 lần | Product vừa import xong | POST import cùng payload lần 2 | Tạo thêm sản phẩm mới (không idempotent) hoặc bị reject | 200 OK (tạo thêm) hoặc 409 Conflict | **INCOMPLETE** | Expected hai khả năng – tùy thiết kế. **Sửa:** Cần xác định từ spec: import-products thường là không idempotent (tạo thêm record mới mỗi lần) → expected 200 OK + sản phẩm mới được tạo. Ghi nhận số sản phẩm trong DB tăng. |
| TC-C-ST-08 | Import batch có 1 sản phẩm lỗi – kiểm tra rollback | Non-existent | POST import với array gồm 1 valid + 1 invalid item | Hoặc rollback toàn bộ, hoặc chỉ import item hợp lệ | 207 Multi-Status hoặc 400 | **INCOMPLETE** | Expected hai behavior (rollback vs partial) không thể cùng lúc. **Sửa:** Cần xác nhận transaction behavior từ source code: nếu atomic → rollback toàn bộ + 400; nếu partial → 207 + danh sách failed items. |

### C. Security Tests (SEC-01 – SEC-07) – Access Control

| TC ID | Mô tả | Loại tấn công | Input | Expected | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|
| TC-C-SEC-01 | Truy cập không có token | Unauthorized (SEC-04) | POST không có Authorization header | 401 Unauthorized | **VALID** | Auth enforcement đúng. |
| TC-C-SEC-02 | Truy cập với user thường | Role Escalation (SEC-03) | Token user thường, POST /api/admin/import-products | 403 Forbidden | **VALID** | RBAC enforcement: admin-only endpoint phải reject non-admin. |
| TC-C-SEC-03 | IDOR – cố truy cập dữ liệu admin khác | IDOR (SEC-02) | Token admin A, thêm trường `admin_id` = ID admin B trong body | Chỉ xử lý theo token, không theo `admin_id` trong body | **INCOMPLETE** | Expected thiếu HTTP status code cụ thể. Khái niệm IDOR không hoàn toàn phù hợp với import-products vì đây là write operation. **Sửa:** Expected: "200 OK – sản phẩm được import và liên kết với admin A (từ token), trường admin_id trong body bị IGNORE". |
| TC-C-SEC-04 | SQL Injection trong trường `name` sản phẩm | SQL Injection (SEC-01) | `{"products":[{"name":"'; DROP TABLE products;--","price":1,"description":"","imageUrl":"","category_id":1}]}` | 400 hoặc 200 – không thực thi SQL | **INCOMPLETE** | Expected "400 hoặc 200" mơ hồ. Quan trọng hơn là DB không bị tấn công. **Sửa:** Expected: "200 OK (nếu tên hợp lệ sau sanitize) hoặc 400 – trong mọi trường hợp, response KHÔNG chứa SQL error và DB không bị DROP". |
| TC-C-SEC-05 | SQL Injection trong trường `description` | SQL Injection (SEC-01) | `{"products":[{"name":"SP1","price":1,"description":"' OR 1=1--","imageUrl":"","category_id":1}]}` | 400 hoặc 200 – không thực thi SQL | **INCOMPLETE** | Tương tự SEC-04 – expected mơ hồ. **Sửa:** "200 OK (description được lưu as-is nếu ORM parametrized) hoặc 400 – không có SQL error". |
| TC-C-SEC-06 | Token giả mạo (forged JWT) | Token Forgery (SEC-05) | `Authorization: Bearer eyJ...forged...` | 401 Unauthorized | **VALID** | JWT signature verification phải fail. |
| TC-C-SEC-07 | Token hết hạn (expired JWT) | Expired Token (SEC-05) | `Authorization: Bearer <expired_token>` | 401 Unauthorized | **VALID** | Expired token phải bị reject. |
| TC-C-SEC-08 | XSS payload trong trường `name` | XSS / Sensitive Data (SEC-07) | `{"products":[{"name":"<script>alert(1)</script>","price":1,"description":"","imageUrl":"","category_id":1}]}` | 400 hoặc dữ liệu được escaped khi lưu | **INCOMPLETE** | Expected "400 hoặc escaped khi lưu" hai khả năng khác nhau. **Sửa:** Expected: "200 OK – sản phẩm được lưu với name được HTML-escaped (`&lt;script&gt;...`) hoặc 400. Quan trọng: khi GET lại sản phẩm, name phải được escaped, không thực thi JS". |

### D. Schema Validation Tests

| TC ID | Mô tả | Field kiểm tra | Expected schema | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|
| TC-C-SV-01 | Response thành công có cấu trúc hợp lệ | toàn bộ response | Phải là JSON object (không phải null hay plain text) | **VALID** | Response type check đúng. |
| TC-C-SV-02 | Response có field thông báo kết quả import | `message` hoặc `count` | Tồn tại ít nhất 1 field mô tả kết quả (vd: message, imported, failed) | **VALID** | Semantic response check – cần biết import thành công bao nhiêu item. |
| TC-C-SV-03 | HTTP Status đúng 200 khi thành công | HTTP Status | 200 OK (không phải 201 Created) | **VALID** | Spec ghi 200 OK cho import thành công. |
| TC-C-SV-04 | Content-Type là application/json | Content-Type header | `Content-Type: application/json` | **VALID** | Response header validation chuẩn. |
| TC-C-SV-05 | Response lỗi 401 có cấu trúc nhất quán | error response (401) | `{"error":...}` hoặc `{"message":...}` – không phải HTML | **VALID** | Error response phải là JSON, không phải HTML (tránh framework default error page). |
| TC-C-SV-06 | Response lỗi 403 có cấu trúc nhất quán | error response (403) | `{"error":...}` hoặc `{"message":...}` | **VALID** | Consistent error format cho authorization failure. |
| TC-C-SV-07 | Response lỗi 400 validation có thông tin lỗi chi tiết | error response (400) | Có mô tả lỗi cụ thể (field nào sai, sai như thế nào) | **VALID** | Validation error response phải đủ thông tin để client debug. |

### E. Test Cases tự thêm (Extend – ≥ 5)

> **Phân tích điểm yếu của test suite AI:** AI bao phủ tốt domain partition cơ bản và access control. Tuy nhiên bỏ sót: (1) partial failure behavior chi tiết, (2) duplicate name trong cùng một batch, (3) mass assignment với các trường hệ thống (id, created_at), (4) payload quá lớn DoS, (5) privilege escalation qua product fields, (6) Unicode/emoji trong product name, (7) concurrent import bởi nhiều admin.

| TC ID | Mô tả | Loại | Lý do AI bỏ sót | Expected | Kết quả |
|:---|:---|:---|:---|:---|:---|
| TC-C-EXT-01 | Import batch có sản phẩm duplicate name trong cùng một mảng | Business Logic / Edge Case | AI test duplicate category_id (FK không tồn tại) nhưng không test duplicate name trong cùng batch. Đây là intra-batch business logic mà prompt không yêu cầu. Một số hệ thống có unique constraint trên product name. | 200 OK (nếu không có unique constraint trên name – cả hai sản phẩm đều được tạo) hoặc 400/207 (nếu có constraint). Ghi nhận hành vi thực tế. | *(sau execute)* |
| TC-C-EXT-02 | Mass Assignment: cố gán `id`, `created_at`, `updated_at` trong product object | Mass Assignment / Security | AI test mass assignment với admin_id (IDOR) nhưng không test với các trường auto-generated của sản phẩm như `id`, `created_at`. Nếu ORM không whitelist, attacker có thể đặt id=1 để override sản phẩm hiện tại. Đây là model limitation: AI không biết schema DB đầy đủ. | 200 OK – sản phẩm được tạo nhưng `id`, `created_at`, `updated_at` phải do hệ thống tự sinh, KHÔNG lấy từ request. Không được phép override sản phẩm có id=1. | *(sau execute)* |
| TC-C-EXT-03 | Import với `price` rất lớn (Integer overflow / BVA cực trên) – ví dụ: 999999999999 | Numeric Boundary / Edge Case | AI test price=0 và price=-1 (BVA phía dưới) nhưng không test BVA phía cực trên của price. Giá trị rất lớn có thể gây integer overflow hoặc bị truncate trong DB (DECIMAL precision). Prompt chỉ yêu cầu BVA 2-point, không đề cập extreme large values. | 200 OK (nếu DB hỗ trợ) hoặc 400 (nếu vượt quá precision); trong mọi trường hợp, giá trị phải được lưu chính xác, không bị truncate silently. | *(sau execute)* |
| TC-C-EXT-04 | Gửi payload cực lớn: array 1000+ sản phẩm hoặc body > 10MB | DoS / Payload Size / Security | AI test array 100 items (BVA lớn) nhưng không test DoS với payload cực lớn. Đây là security concern quan trọng cho admin endpoints. Prompt LLM không tự nghĩ đến DoS attack nếu không được prompt cụ thể (model limitation: không có threat modeling trong prompt). | 413 Payload Too Large hoặc 400 Bad Request – server phải có max payload size protection. Không được để server crash hoặc timeout quá dài. | *(sau execute)* |
| TC-C-EXT-05 | Import sản phẩm với `name` chứa emoji và ký tự Unicode đặc biệt (🛒 Sản phẩm A, 商品) | Unicode / Internationalization | AI test Unicode trong name của user (TC-A-DP-02) nhưng không test Unicode/emoji trong product name cho API này. AI thường bỏ sót internationalization tests nếu prompt không đề cập. Product catalog thường cần hỗ trợ nhiều ngôn ngữ. | 200 OK – sản phẩm được import với name chứa emoji và Unicode, lưu chính xác trong DB và trả về đúng khi GET. | *(sau execute)* |
| TC-C-EXT-06 | Import đồng thời bởi 2 admin sessions với cùng product data | Concurrent Import / Race Condition | AI không test concurrency. Trong hệ thống thực tế, nhiều admin có thể import cùng lúc, gây race condition trên DB sequence/auto-increment. Prompt tập trung single-request scenarios. | Cả 2 request đều được xử lý thành công (200 OK) và mỗi sản phẩm có ID unique; không bị duplicate key error không mong muốn. | *(sau execute)* |
| TC-C-EXT-07 | Import sản phẩm với `description` chứa HTML injection (`<b>Sale!</b>`) | HTML Injection / Stored XSS | AI test XSS với `<script>` trong name (SEC-08) nhưng không test HTML injection trong description. Description thường được render như HTML trên frontend, HTML injection trong description có thể gây layout attack dù không thực thi JS. | 200 OK – description được lưu với HTML escaped (`&lt;b&gt;Sale!&lt;/b&gt;`) hoặc 400. Khi GET lại sản phẩm, description phải được escaped, không render HTML trực tiếp. | *(sau execute)* |

---

## Kết quả Audit (do người review)

| Nhãn | Số lượng | Tỷ lệ | Lý do phổ biến |
|:-----|:---------|:------|:---------------|
| VALID | 21 | 55.3% | TC đúng kỹ thuật, input rõ ràng, expected output đúng spec |
| INVALID | 0 | 0% | – |
| INCOMPLETE | 17 | 44.7% | Expected mơ hồ (hai khả năng không xác định); expected thiếu HTTP status; TC thiếu rõ mục tiêu test |
| **Tổng** | **38** | **100%** | |

### Các TC cần sửa (INCOMPLETE)

| TC ID | Nhãn | Lý do | Nội dung sửa |
|:------|:-----|:------|:-------------|
| TC-C-DP-03 | INCOMPLETE | Expected 400 vs 200 chưa xác định từ spec | Xác nhận business rule: yêu cầu ≥1 item → 400; không yêu cầu → 200 + `{"imported":0}`. |
| TC-C-DP-07 | INCOMPLETE | Expected "400 hoặc 200 tuỳ rule" không thể automation | Xác định rule price từ spec (> 0 hay ≥ 0). |
| TC-C-DP-15 | INCOMPLETE | Expected "200 hoặc 413" mơ hồ | Kiểm tra server config max payload; chốt expected cụ thể. |
| TC-C-ST-07 | INCOMPLETE | Idempotency: expected "tạo thêm hoặc reject" không chốt | Xác nhận thiết kế: import-products thường tạo record mới → expected 200 + sản phẩm mới được tạo. |
| TC-C-ST-08 | INCOMPLETE | Partial failure: rollback vs partial không chốt | Xác nhận DB transaction: atomic → 400 + rollback; partial → 207 + failed list. |
| TC-C-SEC-03 | INCOMPLETE | Expected thiếu HTTP status; khái niệm IDOR chưa đúng | Sửa expected: "200 OK – trường admin_id bị IGNORE, sản phẩm liên kết với admin từ token". |
| TC-C-SEC-04 | INCOMPLETE | Expected "400 hoặc 200" mơ hồ | Sửa: "200 OK (nếu parametrized query) hoặc 400 – KHÔNG có SQL error". |
| TC-C-SEC-05 | INCOMPLETE | Tương tự SEC-04 | Sửa expected tương tự. |
| TC-C-SEC-08 | INCOMPLETE | Expected "400 hoặc escaped" hai khả năng | Sửa: "200 OK với name HTML-escaped hoặc 400 – không thực thi JS". |

---

## Kết quả thực thi (Execute)

- **Công cụ:** Newman 6.2.2 + newman-reporter-html
- **Header bắt buộc:** `X-Student-Id: 23127486`
- **Collection:** `postman/hw06_api3_collection.json`
- **Report HTML:** `newman_reports/newman_api3_report.html`

| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| PASS | 36 | 78.3% |
| FAIL | 10 | 21.7% |
| **Tổng** | 46 (assertions) | 100% |

**Danh sách TC FAIL (phát hiện bug thực của hệ thống):**

| TC ID | Assertion | Actual (Bug) |
|:---|:---|:---|
| TC-C-DP-04 | Status 400 (missing name) | Got **200** – không validate required field name |
| TC-C-DP-05 | Status 400 (empty name) | Got **200** – chấp nhận name rỗng |
| TC-C-DP-06 | Status 400 (missing price) | Got **200** – không validate required field price |
| TC-C-DP-08 | Status 400 (negative price) | Got **200** – chấp nhận giá âm |
| TC-C-DP-09 | Status 400 (string price) | Got **200** – không validate kiểu dữ liệu price |
| TC-C-DP-10 | Status 400 (missing category_id) | Got **200** – không validate required field category_id |
| TC-C-DP-11 | Status 400 (non-existent FK) | Got **200** – không kiểm tra FK constraint category_id |
| TC-C-ST-04 | Status 403 (non-admin rejected) | Got **200** – user thường được phép import products |
| TC-C-SEC-02 | Status 403 (RBAC) | Got **200** – RBAC không được enforce cho import endpoint |
| TC-C-SEC-06 | Status 401 (forged JWT) | Got **200** – server không verify JWT signature |

*(Screenshot Newman / Postman Console đính kèm tại đây)*
