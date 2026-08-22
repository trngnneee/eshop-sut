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
| TC-C-DP-03 | products là mảng rỗng (BVA tại 0 item) | products | BVA – empty array | `{"products":[]}` + admin token | 200 OK hoặc 400 Bad Request | **INCOMPLETE** | Expected 400 vs 200 chưa xác định từ spec: nếu không ràng buộc ≥1 item thì 200 OK. |
| TC-C-DP-04 | Thiếu trường `name` trong sản phẩm | name | Invalid EP – missing field | `{"products":[{"price":10000,"description":"Mo ta","imageUrl":"","category_id":1}]}` + admin token | 400 Bad Request – thiếu name | **VALID** | Cô lập lỗi đúng: thiếu required field name. |
| TC-C-DP-05 | `name` là chuỗi rỗng | name | Invalid EP – empty string | `{"products":[{"name":"","price":10000,"description":"Mo ta","imageUrl":"","category_id":1}]}` + admin token | 400 Bad Request – name không hợp lệ | **VALID** | Empty string vs missing key – cô lập lỗi đúng. |
| TC-C-DP-06 | Thiếu trường `price` trong sản phẩm | price | Invalid EP – missing field | `{"products":[{"name":"SP1","description":"Mo ta","imageUrl":"","category_id":1}]}` + admin token | 400 Bad Request – thiếu price | **VALID** | Cô lập lỗi đúng. |
| TC-C-DP-07 | `price` = 0 (BVA tại 0) | price | BVA – zero | `{"products":[{"name":"SP1","price":0,"description":"Mo ta","imageUrl":"","category_id":1}]}` + admin token | 200 OK hoặc 400 Bad Request | **INCOMPLETE** | Cần xác định rule price: nếu price ≥ 0 thì expected 200 OK. |
| TC-C-DP-08 | `price` âm (BVA dưới 0) | price | BVA – negative | `{"products":[{"name":"SP1","price":-1,"description":"Mo ta","imageUrl":"","category_id":1}]}` + admin token | 400 Bad Request – giá không hợp lệ | **VALID** | Giá âm là invalid EP rõ ràng. |
| TC-C-DP-09 | `price` là string thay vì number | price | Invalid EP – wrong type | `{"products":[{"name":"SP1","price":"10000","description":"Mo ta","imageUrl":"","category_id":1}]}` + admin token | 400 Bad Request – sai kiểu dữ liệu | **VALID** | Type mismatch: string vs number. |
| TC-C-DP-10 | Thiếu trường `category_id` | category_id | Invalid EP – missing field | `{"products":[{"name":"SP1","price":10000,"description":"Mo ta","imageUrl":""}]}` + admin token | 400 Bad Request – thiếu category_id | **VALID** | Required FK field bị thiếu. |
| TC-C-DP-11 | `category_id` không tồn tại | category_id | Invalid EP – non-existent FK | `{"products":[{"name":"SP1","price":10000,"description":"Mo ta","imageUrl":"","category_id":9999}]}` + admin token | 400 Bad Request – category không tồn tại | **VALID** | FK constraint violation. |
| TC-C-DP-12 | `products` không phải array (là object) | products | Invalid EP – wrong type | `{"products":{"name":"SP1","price":10000}}` + admin token | 400 Bad Request – sai kiểu | **VALID** | Type validation cho top-level field products. |
| TC-C-DP-13 | Body là JSON rỗng `{}` | products | Invalid EP – missing key | `{}` + admin token | 400 Bad Request – thiếu trường products | **VALID** | Missing required key products. |
| TC-C-DP-14 | Import 1 sản phẩm với `imageUrl` rỗng (nullable) | imageUrl | Valid EP – nullable field | `{"products":[{"name":"SP1","price":10000,"description":"Mo ta","imageUrl":"","category_id":1}]}` + admin token | 200 OK – imageUrl rỗng được chấp nhận | **VALID** | Nullable field validation. |
| TC-C-DP-15 | Import rất nhiều sản phẩm (BVA số lượng lớn) | products array size | BVA – large batch | `{"products":[{...}x50]}` + admin token | 200 OK hoặc 413 Payload Too Large | **INCOMPLETE** | Xác định max batch size từ cấu hình server. |

### B. State Transition & Lifecycle Tests (Admin / CRUD)

| TC ID | Mô tả kịch bản | Trạng thái ban đầu (Pre-state) | Hành động / Payload | Trạng thái kỳ vọng (Post-state) | Expected HTTP Status & Error Code | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|:---|
| TC-C-ST-01 | Sản phẩm Non-existent → Created sau khi import | Non-existent | POST import với 1 sản phẩm hợp lệ | Sản phẩm tồn tại trong DB (có thể GET /api/products) | 200 OK – import thành công | **VALID** | Resource Lifecycle: Non-existent → Created đúng. |
| TC-C-ST-02 | Import xong kiểm tra sản phẩm xuất hiện trong danh sách | Non-existent | POST import → GET /api/products | Sản phẩm mới xuất hiện trong danh sách | GET: 200 OK có sản phẩm mới | **VALID** | State sequence: Created → Active. |
| TC-C-ST-03 | Import khi không có token – từ chối | Unauthenticated | POST /api/admin/import-products không có token | Unauthenticated – không import | 401 Unauthorized | **VALID** | Auth State: Unauthenticated → reject. |
| TC-C-ST-04 | Import với token user thường – từ chối | Authenticated (non-admin) | POST import với user token | Forbidden – không import | 403 Forbidden | **VALID** | Auth State: Authenticated non-admin → 403. |
| TC-C-ST-05 | Import với admin token – thành công | Authenticated (admin) | POST import với admin token + valid data | Sản phẩm được tạo | 200 OK | **VALID** | Auth State: Authenticated admin → thành công. |
| TC-C-ST-06 | Token hết hạn – bị từ chối | Token Expired | POST import với expired token | Unauthenticated | 401 Unauthorized | **VALID** | Auth State: Expired → 401. |
| TC-C-ST-07 | Import lặp lại cùng payload | Product vừa import xong | POST import cùng payload lần 2 | Tạo thêm sản phẩm mới trong DB | 200 OK – tạo thêm sản phẩm | **INCOMPLETE** | Thiết kế import-products thường tạo record mới mỗi lần. |
| TC-C-ST-08 | Import batch có 1 sản phẩm lỗi – kiểm tra xử lý | Non-existent | POST import mảng có 1 item valid + 1 item invalid | Hệ thống xử lý atomic rollback hoặc partial | 400 Bad Request hoặc 200/207 | **INCOMPLETE** | Xác nhận transaction behavior từ DB. |

### C. Security Tests (SEC-01 – SEC-07) – Access Control

| TC ID | Mô tả | Loại tấn công | Input | Expected | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|
| TC-C-SEC-01 | Truy cập không có token | Unauthorized (SEC-04) | POST không có Authorization header | 401 Unauthorized | **VALID** | Auth enforcement đúng. |
| TC-C-SEC-02 | Truy cập với user thường | Role Escalation (SEC-03) | Token user thường, POST /api/admin/import-products | 403 Forbidden | **VALID** | RBAC enforcement: admin-only endpoint. |
| TC-C-SEC-03 | Cố gán admin_id trong body khi import | Mass Assignment (SEC-02) | Token admin A, thêm trường `admin_id` = 999 | 200 OK – trường admin_id bị IGNORE | **INCOMPLETE** | Mass assignment check: trường lạ bị bỏ qua. |
| TC-C-SEC-04 | SQL Injection trong trường `name` sản phẩm | SQL Injection (SEC-01) | `{"products":[{"name":"'; DROP TABLE products;--","price":1,"description":"","imageUrl":"","category_id":1}]}` | 200 OK hoặc 400 – KHÔNG có lỗi SQL | **INCOMPLETE** | DB không bị tấn công SQL injection. |
| TC-C-SEC-05 | SQL Injection trong trường `description` | SQL Injection (SEC-01) | `{"products":[{"name":"SP1","price":1,"description":"' OR 1=1--","imageUrl":"","category_id":1}]}` | 200 OK hoặc 400 – KHÔNG có lỗi SQL | **INCOMPLETE** | Parametrized query an toàn. |
| TC-C-SEC-06 | Token giả mạo (forged JWT) | Token Forgery (SEC-05) | `Authorization: Bearer eyJ...forged...` | 401 Unauthorized | **VALID** | JWT signature verification phải fail. |
| TC-C-SEC-07 | Token hết hạn (expired JWT) | Expired Token (SEC-05) | `Authorization: Bearer <expired_token>` | 401 Unauthorized | **VALID** | Expired token phải bị reject. |
| TC-C-SEC-08 | XSS payload trong trường `name` | XSS / Sensitive Data (SEC-07) | `{"products":[{"name":"<script>alert(1)</script>","price":1,"description":"","imageUrl":"","category_id":1}]}` | 200 OK hoặc 400 – không reflect script | **INCOMPLETE** | Dữ liệu được escape an toàn khi lưu/hiển thị. |

### D. Schema Validation Tests

| TC ID | Mô tả | Field kiểm tra | Expected schema | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|
| TC-C-SV-01 | Response thành công có cấu trúc hợp lệ | toàn bộ response | Phải là JSON object (không phải null hay plain text) | **VALID** | Response type check đúng. |
| TC-C-SV-02 | Response có field thông báo kết quả import | `message` hoặc `count` | Tồn tại ít nhất 1 field mô tả kết quả (vd: message, imported, count) | **VALID** | Semantic response check. |
| TC-C-SV-03 | HTTP Status đúng 200 khi thành công | HTTP Status | 200 OK (không phải 201 Created) | **VALID** | Spec ghi 200 OK cho import thành công. |
| TC-C-SV-04 | Content-Type là application/json | Content-Type header | `Content-Type: application/json` | **VALID** | Response header validation chuẩn. |
| TC-C-SV-05 | Response lỗi 401 có cấu trúc nhất quán | error response (401) | Content-Type là application/json | **VALID** | Error response phải là JSON. |
| TC-C-SV-06 | Response lỗi 403 có cấu trúc nhất quán | error response (403) | Content-Type là application/json | **VALID** | Consistent error format cho authorization failure. |
| TC-C-SV-07 | Response lỗi 400 validation có thông tin lỗi chi tiết | error response (400) | Có mô tả lỗi cụ thể | **VALID** | Validation error response. |

### E. Test Cases tự thêm (Extend – ≥ 5)

| TC ID | Mô tả | Loại | Lý do AI bỏ sót | Expected | Kết quả |
|:---|:---|:---|:---|:---|:---|
| TC-C-EXT-01 | Import batch có sản phẩm duplicate name trong cùng một mảng | Business Logic / Edge Case | AI test duplicate FK nhưng không test duplicate name trong cùng batch. | 200 OK hoặc 400 Bad Request. | PASS |
| TC-C-EXT-02 | Mass Assignment: cố gán `id`, `created_at` trong product object | Mass Assignment / Security | AI test admin_id nhưng không test auto-generated fields của sản phẩm (`id`, `created_at`). | 200 OK – `id`, `created_at` do hệ thống tự sinh, không bị override. | PASS |
| TC-C-EXT-03 | Import với `price` rất lớn (999999999999) – kiểm tra integer overflow / DB precision | Numeric Boundary / Edge Case | AI test BVA phía dưới nhưng không test BVA cực trên. | 200 OK hoặc 400 – giá trị được xử lý chính xác, không tràn số. | PASS |
| TC-C-EXT-04 | Mảng `products` chứa phần tử không phải object (`[123, "invalid_item"]`) | Array Element Type / Input Validation | AI test missing/empty array nhưng không test type mismatch của các phần tử bên trong array. | 400 Bad Request – phần tử trong products phải là object. | FAIL (Got 200) |
| TC-C-EXT-05 | Import sản phẩm với `name` chứa emoji và ký tự Unicode đặc biệt (🛒 Sản phẩm Unicode 特别商品) | Unicode / Internationalization | AI không test Unicode/emoji cho product catalog. | 200 OK – lưu chính xác emoji và Unicode trong DB. | PASS |
| TC-C-EXT-06 | Import sản phẩm với `price` là số thực dấu phẩy động (`19999.99`) | Numeric Type / Boundary | AI chỉ test số nguyên, không test số thực dấu phẩy động cho price. | 200 OK hoặc 400 – xử lý số thực chính xác. | PASS |
| TC-C-EXT-07 | Import sản phẩm với `description` chứa HTML injection (`<b>Sale!</b>`) | HTML Injection / Stored XSS | AI test script tag trong name nhưng không test HTML injection trong description. | 200 OK hoặc 400 – không render HTML trực tiếp. | PASS |

---

## Kết quả Audit (do người review)

| Nhãn | Số lượng | Tỷ lệ | Lý do phổ biến |
|:-----|:---------|:------|:---------------|
| VALID | 29 | 76.3% | TC đúng kỹ thuật, input rõ ràng, expected output đúng spec |
| INVALID | 0 | 0% | – |
| INCOMPLETE | 9 | 23.7% | Expected mơ hồ phụ thuộc transaction / business rules chưa làm rõ trong spec |
| **Tổng** | **38** | **100%** | |

### Các TC cần sửa (INCOMPLETE)

| TC ID | Nhãn | Lý do | Nội dung sửa |
|:------|:-----|:------|:-------------|
| TC-C-DP-03 | INCOMPLETE | Expected 400 vs 200 chưa xác định từ spec | Xác nhận rule: không bắt buộc ≥1 item → 200 OK. |
| TC-C-DP-07 | INCOMPLETE | Expected "400 hoặc 200 tuỳ rule" | Xác định rule price: nếu price ≥ 0 → expected 200 OK. |
| TC-C-DP-15 | INCOMPLETE | Expected 200 vs 413 | Kiểm tra server config max payload. |
| TC-C-ST-07 | INCOMPLETE | Idempotency: tạo thêm hay reject | Xác nhận thiết kế: tạo thêm record mới → expected 200 OK. |
| TC-C-ST-08 | INCOMPLETE | Partial failure: rollback vs partial | Xác nhận DB transaction atomic → 400 / 200 / 207. |
| TC-C-SEC-03 | INCOMPLETE | IDOR chưa chuẩn cho write operation | Sửa expected: 200 OK – admin_id bị ignore. |
| TC-C-SEC-04 | INCOMPLETE | Expected SQLi chưa rõ | Sửa: 200 OK hoặc 400 – KHÔNG có lỗi SQL lộ ra. |
| TC-C-SEC-05 | INCOMPLETE | Tương tự SEC-04 | Sửa: 200 OK hoặc 400 – KHÔNG có lỗi SQL. |
| TC-C-SEC-08 | INCOMPLETE | Expected XSS hai khả năng | Sửa: 200 OK hoặc 400 – không reflect script. |

---

## Kết quả thực thi (Execute)

- **Công cụ:** Newman 6.2.2 + newman-reporter-htmlextra
- **Header bắt buộc:** `X-Student-Id: 23127486`
- **Collection:** `postman/hw06_api3_collection.json` (47 requests gồm 2 setup login)
- **Report HTML:** `newman_reports/newman_api3_report.html`

| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| PASS | 40 | 75.5% |
| FAIL | 13 | 24.5% |
| **Tổng** | 53 (assertions) | 100% |

**Danh sách TC FAIL (phát hiện bug thực của hệ thống):**

| TC ID | Assertion | Actual (Bug) |
|:---|:---|:---|
| TC-C-DP-04 | Status 400 (missing name) | Got **200** – không validate required field name |
| TC-C-DP-05 | Status 400 (empty name) | Got **200** – chấp nhận name rỗng |
| TC-C-DP-06 | Status 400 (missing price) | Got **200** – không validate required field price |
| TC-C-DP-08 | Status 400 (negative price) | Got **200** – chấp nhận giá âm |
| TC-C-DP-09 | Status 400 (string price) | Got **200** – không validate kiểu dữ liệu price |
| TC-C-DP-10 | Status 400 (missing category_id) | Got **200** – không validate required field category_id |
| TC-C-DP-11 | Status 400 (non-existent category_id) | Got **200** – không kiểm tra FK constraint category_id |
| TC-C-ST-04 | Status 403 (non-admin regular user) | Got **200** – user thường được phép import products (RBAC bypass) |
| TC-C-ST-06 | Status 401 (expired token) | Got **403** – server trả 403 Forbidden thay vì 401 Unauthorized |
| TC-C-SEC-02 | Status 403 (role escalation) | Got **200** – RBAC không được enforce cho import endpoint |
| TC-C-SEC-06 | Status 401 (forged JWT) | Got **403** – server trả 403 Forbidden thay vì 401 Unauthorized |
| TC-C-SEC-07 | Status 401 (expired JWT) | Got **403** – server trả 403 Forbidden thay vì 401 Unauthorized |
| TC-C-EXT-04 | Status 400 (non-object in products) | Got **200** – không validate kiểu phần tử trong products array |

*(Screenshot Newman / Postman Console đính kèm tại đây)*
