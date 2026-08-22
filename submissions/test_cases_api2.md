# Test Cases – API 2 (Pool B)

**Sinh viên:** Phan Quốc Thịnh – 23127486 – 23KTPM3  
**Feature:** FR-11 – Xem lịch sử đơn hàng cá nhân  
**Endpoint:** `GET /api/orders/my-orders`

---

## Tổng quan

| Mục | Giá trị |
|:---|:---|
| **API** | GET /api/orders/my-orders – Xem lịch sử đơn hàng cá nhân |
| **Pool** | B |
| **Tổng TC (AI sinh)** | 38 (DP/BVA: 15 \| ST: 8 \| SEC: 8 \| SV: 7) |
| **TC tự thêm** | 7 (TC-B-EXT-01 đến TC-B-EXT-07) |
| **Tổng TC** | 45 |

---

## Phân loại test cases

### A. Domain Partition & Boundary Value Tests (EP & BVA)

| TC ID | Mô tả | Tham số kiểm tra | Phân vùng / Điểm biên | Input Payload (Params/Body) | Expected HTTP Status & Output | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|:---|
| TC-B-DP-01 | Lấy danh sách đơn hàng hợp lệ – user có token và có đơn hàng | Authorization header | Valid EP – happy path | Header: `Authorization: Bearer <valid_token>` | 200 OK – mảng các đơn hàng của user | **VALID** | Happy path chuẩn, đủ điều kiện auth và data. |
| TC-B-DP-02 | Lấy danh sách khi user chưa có đơn hàng nào | Authorization header | Valid EP – empty result | Header: `Authorization: Bearer <new_user_token>` | 200 OK – mảng rỗng `[]` | **VALID** | Empty result là valid EP quan trọng – phân biệt 200+[] với 404. |
| TC-B-DP-03 | Không có Authorization header | Authorization header | Invalid EP – missing auth | Không có header Authorization | 401 Unauthorized | **VALID** | Cô lập lỗi đúng: chỉ thiếu auth header. |
| TC-B-DP-04 | Token sai định dạng (Bearer thiếu) | Authorization header | Invalid EP – wrong format | Header: `<valid_token>` (thiếu tiền tố Bearer) | 401 Unauthorized | **VALID** | Cô lập lỗi format token. |
| TC-B-DP-05 | Token rỗng (Bearer rỗng) | Authorization header | Invalid EP – empty token | Header: `Authorization: Bearer ` | 401 Unauthorized | **VALID** | Phân biệt empty vs missing token. |
| TC-B-DP-06 | Token giả mạo (chuỗi ngẫu nhiên) | Authorization header | Invalid EP – forged token | Header: `Authorization: Bearer invalidfaketoken123` | 401 Unauthorized | **VALID** | Token không hợp lệ phải bị reject. |
| TC-B-DP-07 | Token hết hạn | Authorization header | Invalid EP – expired token | Header: `Authorization: Bearer <expired_token>` | 401 Unauthorized – token expired | **VALID** | Expired token là invalid EP quan trọng. |
| TC-B-DP-08 | Gọi với query param `?page=1` (nếu hỗ trợ) | query: page | Valid EP – pagination | `GET /api/orders/my-orders?page=1` + valid token | 200 OK – danh sách đơn hàng trang 1 | **INCOMPLETE** | Expected "Chỉ test nếu có pagination" không thể tự động hóa nếu không xác nhận API có pagination. **Sửa:** Nếu spec không đề cập pagination → expected vẫn là 200 OK với toàn bộ list (param bị ignore). Cần xác nhận spec. |
| TC-B-DP-09 | Gọi với query param `?page=0` (BVA dưới min) | query: page | BVA – below min | `GET /api/orders/my-orders?page=0` + valid token | 400 Bad Request hoặc bỏ qua tham số | **INCOMPLETE** | Expected "bỏ qua tham số" và "400 Bad Request" là hai expected khác nhau – không thể cùng lúc. **Sửa:** Nếu không có pagination spec → expected là 200 OK (param bị ignore); nếu có spec pagination → expected là 400. |
| TC-B-DP-10 | Gọi với query param `?page=-1` (BVA âm) | query: page | BVA – negative | `GET /api/orders/my-orders?page=-1` + valid token | 400 Bad Request | **INCOMPLETE** | Tương tự DP-09 – conditional expected. **Sửa:** Xác nhận từ spec; nếu không có pagination → expected là 200 OK. |
| TC-B-DP-11 | Gọi với query param `?page=abc` (sai kiểu) | query: page | Invalid EP – wrong type | `GET /api/orders/my-orders?page=abc` + valid token | 400 Bad Request | **INCOMPLETE** | Tương tự các DP pagination phía trên. **Sửa:** Cần biết API có pagination không. |
| TC-B-DP-12 | Gọi với param `?limit=0` (BVA tại 0) | query: limit | BVA – zero | `GET /api/orders/my-orders?limit=0` + valid token | 400 Bad Request hoặc 200 với array rỗng | **INCOMPLETE** | Expected hai khả năng không thể dùng trong automation. **Sửa:** Chọn một expected cụ thể dựa trên spec. |
| TC-B-DP-13 | Gọi với param `?limit=9999` (BVA rất lớn) | query: limit | BVA – above max | `GET /api/orders/my-orders?limit=9999` + valid token | 200 OK hoặc 400 (tuỳ hệ thống) | **INCOMPLETE** | Expected mơ hồ. **Sửa:** Xác định max limit từ spec; nếu không có → expected 200 OK. |
| TC-B-DP-14 | Gọi một lúc nhiều query param không xác định | query: unknown params | Invalid EP – unknown params | `?foo=bar&baz=qux` + valid token | 200 OK – bỏ qua param lạ, trả toàn bộ đơn | **VALID** | API đúng chuẩn phải ignore unknown params, trả kết quả bình thường. |
| TC-B-DP-15 | Gọi với method sai (POST thay vì GET) | HTTP Method | Invalid EP – wrong method | POST /api/orders/my-orders + valid token + empty body | 405 Method Not Allowed | **VALID** | Method validation đúng – 405 là response chuẩn cho wrong method. |

### B. State Transition & Lifecycle Tests

| TC ID | Mô tả kịch bản | Trạng thái ban đầu (Pre-state) | Hành động / Payload | Trạng thái kỳ vọng (Post-state) | Expected HTTP Status & Error Code | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|:---|
| TC-B-ST-01 | User Unauthenticated gọi API – từ chối | Unauthenticated | GET /api/orders/my-orders không có token | Unauthenticated – không lấy được dữ liệu | 401 Unauthorized | **VALID** | Auth State: Unauthenticated → từ chối đúng. |
| TC-B-ST-02 | User Authenticated lấy danh sách đơn – thành công | Authenticated | GET /api/orders/my-orders với valid token | Authenticated – danh sách đơn hàng trả về | 200 OK | **VALID** | Auth State: Authenticated → thành công. |
| TC-B-ST-03 | Đơn hàng pending xuất hiện trong danh sách | Order: pending | GET my-orders sau khi tạo đơn hàng mới | Danh sách chứa đơn pending | 200 OK – tất cả đơn bao gồm trạng thái pending | **VALID** | Business State: pending → visible trong list. Quan trọng để xác nhận danh sách không filter bỏ pending. |
| TC-B-ST-04 | Đơn hàng confirmed xuất hiện trong danh sách | Order: confirmed | GET my-orders sau khi admin xác nhận đơn | Danh sách chứa đơn confirmed | 200 OK | **VALID** | Business State: confirmed → visible. |
| TC-B-ST-05 | Đơn hàng đã hủy vẫn hiển thị trong lịch sử | Order: canceled | GET my-orders sau khi hủy đơn | Đơn hàng hủy vẫn có trong danh sách | 200 OK – có record với status canceled | **VALID** | Terminal State: canceled vẫn hiện trong lịch sử – đây là hành vi đúng cho "lịch sử đơn hàng". |
| TC-B-ST-06 | Đơn hàng delivered xuất hiện trong lịch sử | Order: delivered | GET my-orders sau khi giao hàng xong | Danh sách chứa đơn delivered | 200 OK – có record với status delivered | **VALID** | Terminal State: delivered vẫn hiện. |
| TC-B-ST-07 | Token hết hạn – session expire state | Token Expired | GET my-orders với expired token | Unauthenticated – phải đăng nhập lại | 401 Unauthorized – token expired | **VALID** | Auth State: Expired → 401 đúng. |
| TC-B-ST-08 | Gọi lần lượt: checkout → kiểm tra lịch sử | Order: Non-existent → Created | POST /checkout rồi GET /my-orders | Danh sách chứa đơn vừa tạo | 200 OK – order mới xuất hiện | **VALID** | State sequence: Created → visible in list. Xác nhận consistency giữa checkout và my-orders. |

### C. Security Tests (SEC-01 – SEC-07)

| TC ID | Mô tả | Loại tấn công | Input | Expected | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|
| TC-B-SEC-01 | Truy cập không có token | Missing Auth (SEC-04) | Không có Authorization header | 401 Unauthorized | **VALID** | Trùng với DP-03 nhưng nhìn từ góc độ security – đúng. |
| TC-B-SEC-02 | IDOR – cố xem đơn hàng của user khác qua my-orders | IDOR (SEC-02) | Token của user A, thêm param `?user_id=<ID_user_B>` | 200 OK nhưng chỉ trả về đơn của user A – không lọc theo param | **VALID** | IDOR test quan trọng: API phải ignore user_id param và chỉ dùng token để xác định user. |
| TC-B-SEC-03 | User thường gọi admin orders endpoint | Role Escalation (SEC-03) | Token user thường, GET /api/admin/orders | 403 Forbidden | **INCOMPLETE** | TC này test endpoint khác (/api/admin/orders), không phải /api/orders/my-orders. Không liên quan trực tiếp đến API đang test. **Sửa:** Đổi thành "user thường thêm header X-Admin: true để cố escalate privilege khi gọi my-orders" – hoặc bỏ khỏi test suite này. |
| TC-B-SEC-04 | Token giả mạo (forged JWT) | Token Forgery (SEC-05) | Header: `Authorization: Bearer eyJ...forged...` | 401 Unauthorized – signature invalid | **VALID** | Forged JWT phải bị reject do signature verification. |
| TC-B-SEC-05 | Token hết hạn (expired JWT) | Expired Token (SEC-05) | Header: `Authorization: Bearer <expired_token>` | 401 Unauthorized – token expired | **VALID** | Trùng DP-07 nhưng nhìn từ góc security là hợp lý để có record. |
| TC-B-SEC-06 | SQL Injection vào query param | SQL Injection (SEC-01) | `GET /api/orders/my-orders?page=' OR 1=1 --` + valid token | 400 Bad Request – không thực thi SQL | **INCOMPLETE** | Expected "400 Bad Request" chưa rõ: nếu API ignore unknown params → sẽ trả 200 OK với toàn bộ list. Quan trọng hơn là response không chứa SQL error. **Sửa:** Expected phải là "200 OK hoặc 400 – quan trọng là response KHÔNG chứa SQL error message". |
| TC-B-SEC-07 | Lộ thông tin nhạy cảm trong response | Sensitive Data Exposure (SEC-07) | GET /api/orders/my-orders hợp lệ | Response KHÔNG chứa password, CVV, số thẻ | **VALID** | Data exposure check đúng. |
| TC-B-SEC-08 | Admin token truy cập my-orders – chỉ thấy đơn của admin | Role Access (SEC-03) | Token admin, GET /api/orders/my-orders | 200 OK – chỉ đơn của admin, không thấy tất cả đơn | **VALID** | Quan trọng: my-orders phải scope theo user từ token, kể cả admin chỉ thấy đơn của account admin đó. |

### D. Schema Validation Tests

| TC ID | Mô tả | Field kiểm tra | Expected schema | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|
| TC-B-SV-01 | Response là array (kể cả khi rỗng) | kiểu dữ liệu gốc | Response là `[]` hoặc `[{...}]` – không phải `null` hay object | **VALID** | Array type check – critical để phân biệt empty vs null. |
| TC-B-SV-02 | Mỗi đơn hàng có các field bắt buộc | `id`, `total_amount`, `status`, `shipping_address` | Mỗi item trong array có đủ 4 field trên, không null | **VALID** | Schema completeness check theo spec. |
| TC-B-SV-03 | Field `id` là number | `id` | Số nguyên dương, không phải string | **VALID** | Type check đúng. |
| TC-B-SV-04 | Field `total_amount` là number | `total_amount` | Số thực dương, không phải string | **VALID** | Type check đúng. |
| TC-B-SV-05 | Field `status` là string thuộc enum hợp lệ | `status` | Một trong: `pending`, `confirmed`, `shipping`, `delivered`, `canceled` | **VALID** | Enum validation quan trọng để detect nếu DB trả về giá trị không hợp lệ. |
| TC-B-SV-06 | HTTP Status đúng 200 khi thành công | HTTP Status | 200 OK (không phải 204 No Content dù danh sách rỗng) | **VALID** | Spec rõ ràng phải trả 200+[] khi không có đơn, không phải 204. |
| TC-B-SV-07 | Content-Type là application/json | Content-Type header | `Content-Type: application/json` | **VALID** | Response header validation chuẩn. |

### E. Test Cases tự thêm (Extend – ≥ 5)

> **Phân tích điểm yếu của test suite AI:** AI bao phủ tốt auth states và business states cơ bản. Tuy nhiên bỏ sót: (1) data isolation giữa các user (cross-user contamination), (2) ordering/sorting consistency, (3) JWT với claims bị sửa nhưng signature hợp lệ (alg:none attack), (4) pagination boundary khi list thay đổi, (5) concurrent requests, (6) response với shipping_address là object lồng nhau, (7) behavior khi DB unavailable.

| TC ID | Mô tả | Loại | Lý do AI bỏ sót | Expected | Kết quả |
|:---|:---|:---|:---|:---|:---|
| TC-B-EXT-01 | User A đăng nhập và gọi my-orders – xác nhận KHÔNG thấy đơn hàng của User B | Data Isolation / IDOR | AI test IDOR qua query param nhưng không test cross-user data leak ở tầng DB query. Prompt không yêu cầu kiểm tra isolation giữa các user bằng cách tạo data của nhiều user rồi cross-check. | 200 OK – response chỉ chứa đơn hàng của User A; không có đơn hàng nào của User B trong danh sách. | *(sau execute)* |
| TC-B-EXT-02 | JWT Algorithm Confusion: gửi token với header `alg: none` (unsigned token) | JWT Algorithm None Attack / Security | AI test token forged (signature sai) và expired nhưng không test "alg:none" attack – một lỗ hổng JWT đặc thù khi server không validate algorithm. Đây là model limitation: LLM không liệt kê đủ JWT attack vectors nếu prompt không yêu cầu. | 401 Unauthorized – server phải reject token với alg:none, không được chấp nhận unsigned JWT. | *(sau execute)* |
| TC-B-EXT-03 | Thứ tự sắp xếp đơn hàng trong response – đơn mới nhất phải ở đầu | Ordering / Business Logic | AI không kiểm tra ordering của danh sách trả về. Thứ tự hiển thị quan trọng về mặt UX và business logic nhưng không được đề cập trong prompt. Model không tự suy luận về expected ordering nếu spec không ghi rõ. | 200 OK – danh sách được sắp xếp theo thứ tự giảm dần của `created_at` (đơn mới nhất đầu tiên). | *(sau execute)* |
| TC-B-EXT-04 | Response field `shipping_address` là object lồng nhau – kiểm tra schema con | Nested Schema Validation | AI schema validation chỉ kiểm tra sự hiện diện của `shipping_address` (không null) nhưng không kiểm tra schema con của object này. Prompt chỉ yêu cầu kiểm tra các field top-level. | 200 OK – `shipping_address` là object có ít nhất các field: `street`, `city`, `province` (hoặc theo schema thực tế); không phải string đơn giản. | *(sau execute)* |
| TC-B-EXT-05 | Gọi API với `Authorization: Basic <base64>` thay vì Bearer token | Invalid Auth Scheme / Security | AI chỉ test Bearer format variants (thiếu Bearer, empty, forged) nhưng không test scheme sai hoàn toàn (Basic auth). Attacker có thể thử Basic auth để bypass JWT validation. | 401 Unauthorized – server phải reject Basic auth scheme và yêu cầu Bearer JWT. | *(sau execute)* |
| TC-B-EXT-06 | Gọi liên tiếp 50 request GET my-orders trong 1 giây – kiểm tra rate limiting | Rate Limiting / Security | AI không test rate limiting cho GET my-orders – chỉ đề cập rate limiting cho register (POST). Endpoint my-orders có thể bị lạm dụng để thu thập dữ liệu nếu không có rate limit. Prompt không yêu cầu rate limit test cho GET endpoints. | 200 OK cho các request đầu; 429 Too Many Requests sau khi vượt threshold (nếu có rate limit). Ghi nhận response thực tế. | *(sau execute)* |
| TC-B-EXT-07 | Response khi user có đơn hàng với tất cả các trạng thái khác nhau – kiểm tra đầy đủ enum | State Coverage / Schema Validation | AI test từng trạng thái riêng lẻ (ST-03 đến ST-06) nhưng không có TC kiểm tra một response chứa đơn hàng ở tất cả các trạng thái enum (pending, confirmed, shipping, delivered, canceled) cùng lúc để xác nhận field `status` trả về đúng enum cho từng record. | 200 OK – mảng gồm ≥5 đơn với status lần lượt: pending, confirmed, shipping, delivered, canceled – tất cả đều đúng enum value. | *(sau execute)* |

---

## Kết quả Audit (do người review)

| Nhãn | Số lượng | Tỷ lệ | Lý do phổ biến |
|:-----|:---------|:------|:---------------|
| VALID | 27 | 71.1% | TC đúng kỹ thuật, input rõ ràng, expected output đúng spec |
| INVALID | 0 | 0% | – |
| INCOMPLETE | 11 | 28.9% | Expected mơ hồ (conditional) cho pagination params; một TC test endpoint khác; SQL injection expected chưa rõ |
| **Tổng** | **38** | **100%** | |

### Các TC cần sửa (INCOMPLETE)

| TC ID | Nhãn | Lý do | Nội dung sửa |
|:------|:-----|:------|:-------------|
| TC-B-DP-08 | INCOMPLETE | Expected conditional: "chỉ test nếu có pagination" không thể tự động hóa | Xác nhận từ spec: nếu không có pagination → expected 200 OK (param bị ignore). |
| TC-B-DP-09 | INCOMPLETE | Expected hai khả năng không thể song song trong automation | Chọn một: nếu không có pagination spec → expected 200 OK. |
| TC-B-DP-10 | INCOMPLETE | Tương tự DP-09 | Xác nhận spec, chọn expected cụ thể. |
| TC-B-DP-11 | INCOMPLETE | Tương tự DP-09 | Xác nhận spec, chọn expected cụ thể. |
| TC-B-DP-12 | INCOMPLETE | Expected hai khả năng | Xác nhận spec limit/pagination, chọn expected cụ thể. |
| TC-B-DP-13 | INCOMPLETE | Expected "200 OK hoặc 400 (tuỳ hệ thống)" mơ hồ | Xác nhận max limit từ spec; nếu không có → expected 200 OK. |
| TC-B-SEC-03 | INCOMPLETE | Test endpoint khác (/api/admin/orders) – không liên quan API đang test | Đổi TC: "user thường thêm header X-Admin: true khi gọi my-orders" hoặc bỏ. |
| TC-B-SEC-06 | INCOMPLETE | Expected "400 Bad Request" chưa rõ – quan trọng hơn là không lộ SQL error | Sửa expected: "200 OK hoặc 400 – KHÔNG có SQL error trong response body". |

---

## Kết quả thực thi (Execute)

- **Công cụ:** Newman 6.2.2 + newman-reporter-html
- **Header bắt buộc:** `X-Student-Id: 23127486`
- **Collection:** `postman/hw06_api2_collection.json`
- **Report HTML:** `newman_reports/newman_api2_report.html`

| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| PASS | 34 | 91.9% |
| FAIL | 3 | 8.1% |
| **Tổng** | 37 (assertions) | 100% |

**Danh sách TC FAIL (phát hiện bug thực của hệ thống):**

| TC ID | Assertion | Actual (Bug) |
|:---|:---|:---|
| TC-B-DP-06 | Status 401 (forged token) | Got **200** – server chấp nhận token ngẫu nhiên không phải JWT |
| TC-B-SEC-04 | Status 401 (forged JWT rejected) | Got **200** – server không verify JWT signature đúng cách |
| TC-B-EXT-05 | Status 401 (Basic auth rejected) | Got **200** – server chấp nhận Basic auth scheme thay vì chỉ Bearer |

*(Screenshot Newman / Postman Console đính kèm tại đây)*
