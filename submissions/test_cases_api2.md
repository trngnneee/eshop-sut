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
| TC-B-DP-06 | Token giả mạo (chuỗi ngẫu nhiên) | Authorization header | Invalid EP – forged token | Header: `Authorization: Bearer invalidfaketoken123` | 401 Unauthorized | **VALID** | Token không hợp lệ phải bị reject (401). |
| TC-B-DP-07 | Token hết hạn | Authorization header | Invalid EP – expired token | Header: `Authorization: Bearer <expired_token>` | 401 Unauthorized – token expired | **VALID** | Expired token là invalid EP quan trọng. |
| TC-B-DP-08 | Gọi với query param `?page=1` | query: page | Valid EP – ignore param | `GET /api/orders/my-orders?page=1` + valid token | 200 OK – bỏ qua param page, trả toàn bộ đơn hàng | **VALID** | Spec không có pagination, API chuẩn bỏ qua param và trả 200 OK. |
| TC-B-DP-09 | Gọi với query param `?page=0` | query: page | Valid EP – ignore param | `GET /api/orders/my-orders?page=0` + valid token | 200 OK – bỏ qua param page, trả toàn bộ đơn hàng | **VALID** | Bỏ qua query param không xác định trong spec. |
| TC-B-DP-10 | Gọi với query param `?page=-1` | query: page | Valid EP – ignore param | `GET /api/orders/my-orders?page=-1` + valid token | 200 OK – bỏ qua param page, trả toàn bộ đơn hàng | **VALID** | Bỏ qua query param không xác định trong spec. |
| TC-B-DP-11 | Gọi với query param `?page=abc` | query: page | Valid EP – ignore param | `GET /api/orders/my-orders?page=abc` + valid token | 200 OK – bỏ qua param page, trả toàn bộ đơn hàng | **VALID** | Bỏ qua query param không xác định trong spec. |
| TC-B-DP-12 | Gọi với param `?limit=0` | query: limit | Valid EP – ignore param | `GET /api/orders/my-orders?limit=0` + valid token | 200 OK – bỏ qua param limit, trả toàn bộ đơn hàng | **VALID** | Bỏ qua query param không xác định trong spec. |
| TC-B-DP-13 | Gọi với param `?limit=9999` | query: limit | Valid EP – ignore param | `GET /api/orders/my-orders?limit=9999` + valid token | 200 OK – bỏ qua param limit, trả toàn bộ đơn hàng | **VALID** | Bỏ qua query param không xác định trong spec. |
| TC-B-DP-14 | Gọi một lúc nhiều query param không xác định | query: unknown params | Invalid EP – unknown params | `?foo=bar&baz=qux` + valid token | 200 OK – bỏ qua param lạ, trả toàn bộ đơn | **VALID** | API đúng chuẩn phải ignore unknown params, trả kết quả bình thường. |
| TC-B-DP-15 | Gọi với method sai (POST thay vì GET) | HTTP Method | Invalid EP – wrong method | POST /api/orders/my-orders + valid token + empty body | 405 Method Not Allowed hoặc 404 | **VALID** | Method validation đúng – 405/404 là response chuẩn cho wrong method. |

### B. State Transition & Lifecycle Tests

| TC ID | Mô tả kịch bản | Trạng thái ban đầu (Pre-state) | Hành động / Payload | Trạng thái kỳ vọng (Post-state) | Expected HTTP Status & Error Code | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|:---|
| TC-B-ST-01 | User Unauthenticated gọi API – từ chối | Unauthenticated | GET /api/orders/my-orders không có token | Unauthenticated – không lấy được dữ liệu | 401 Unauthorized | **VALID** | Auth State: Unauthenticated → từ chối đúng. |
| TC-B-ST-02 | User Authenticated lấy danh sách đơn – thành công | Authenticated | GET /api/orders/my-orders với valid token | Authenticated – danh sách đơn hàng trả về | 200 OK | **VALID** | Auth State: Authenticated → thành công. |
| TC-B-ST-03 | Đơn hàng pending xuất hiện trong danh sách | Order: pending | GET my-orders sau khi tạo đơn hàng mới | Danh sách chứa đơn pending | 200 OK – tất cả đơn bao gồm trạng thái pending | **VALID** | Business State: pending → visible trong list. |
| TC-B-ST-04 | Đơn hàng confirmed xuất hiện trong danh sách | Order: confirmed | GET my-orders sau khi admin xác nhận đơn | Danh sách chứa đơn confirmed | 200 OK | **VALID** | Business State: confirmed → visible. |
| TC-B-ST-05 | Đơn hàng đã hủy vẫn hiển thị trong lịch sử | Order: canceled | GET my-orders sau khi hủy đơn | Đơn hàng hủy vẫn có trong danh sách | 200 OK – có record với status canceled | **VALID** | Terminal State: canceled vẫn hiện trong lịch sử. |
| TC-B-ST-06 | Đơn hàng delivered xuất hiện trong lịch sử | Order: delivered | GET my-orders sau khi giao hàng xong | Danh sách chứa đơn delivered | 200 OK – có record với status delivered | **VALID** | Terminal State: delivered vẫn hiện. |
| TC-B-ST-07 | Token hết hạn – session expire state | Token Expired | GET my-orders với expired token | Unauthenticated – phải đăng nhập lại | 401 Unauthorized – token expired | **VALID** | Auth State: Expired → 401 đúng. |
| TC-B-ST-08 | Gọi lần lượt: checkout → kiểm tra lịch sử | Order: Non-existent → Created | POST /checkout rồi GET /my-orders | Danh sách chứa đơn vừa tạo | 200 OK – order mới xuất hiện | **VALID** | State sequence: Created → visible in list. |

### C. Security Tests (SEC-01 – SEC-07)

| TC ID | Mô tả | Loại tấn công | Input | Expected | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|
| TC-B-SEC-01 | Truy cập không có token | Missing Auth (SEC-04) | Không có Authorization header | 401 Unauthorized | **VALID** | Trùng với DP-03 nhưng nhìn từ góc độ security – đúng. |
| TC-B-SEC-02 | IDOR – cố xem đơn hàng của user khác qua my-orders | IDOR (SEC-02) | Token của user A, thêm param `?user_id=<ID_user_B>` | 200 OK nhưng chỉ trả về đơn của user A – không lọc theo param | **VALID** | IDOR test quan trọng: API phải ignore user_id param và chỉ dùng token để xác định user. |
| TC-B-SEC-03 | User gửi kèm header X-Admin: true (Role Escalation) | Role Escalation (SEC-03) | Token user thường, Header `X-Admin: true` | 200 OK – chỉ trả đơn của user, không escalate | **INCOMPLETE** | Cần làm rõ: header tùy biến không được gây phân quyền sai lệch. |
| TC-B-SEC-04 | Token giả mạo (forged JWT) | Token Forgery (SEC-05) | Header: `Authorization: Bearer eyJ...forged...` | 401 Unauthorized – signature invalid | **VALID** | Forged JWT phải bị reject do signature verification (401). |
| TC-B-SEC-05 | Token hết hạn (expired JWT) | Expired Token (SEC-05) | Header: `Authorization: Bearer <expired_token>` | 401 Unauthorized – token expired | **VALID** | Expired JWT phải bị reject (401). |
| TC-B-SEC-06 | SQL Injection vào query param | SQL Injection (SEC-01) | `GET /api/orders/my-orders?page=' OR 1=1 --` + valid token | 200 OK hoặc 400 – KHÔNG có lỗi SQL lộ ra | **INCOMPLETE** | Sửa expected: "200 OK hoặc 400 – quan trọng là response KHÔNG chứa SQL error message". |
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

| TC ID | Mô tả | Loại | Lý do AI bỏ sót | Expected | Kết quả |
|:---|:---|:---|:---|:---|:---|
| TC-B-EXT-01 | User A đăng nhập và gọi my-orders – xác nhận KHÔNG thấy đơn hàng của User B | Data Isolation / IDOR | AI test IDOR qua query param nhưng không test cross-user data leak ở tầng DB query. | 200 OK – response chỉ chứa đơn hàng của User A; không có đơn hàng nào của User B trong danh sách. | PASS |
| TC-B-EXT-02 | JWT Algorithm Confusion: gửi token với header `alg: none` (unsigned token) | JWT Algorithm None Attack / Security | AI test token forged và expired nhưng không test "alg:none" attack. | 401 Unauthorized – server phải reject token với alg:none. | FAIL (Got 403) |
| TC-B-EXT-03 | Thứ tự sắp xếp đơn hàng trong response – kiểm tra tính nhất quán | Ordering / Business Logic | AI không kiểm tra ordering của danh sách trả về. | 200 OK – danh sách đơn hàng được trả về nhất quán. | PASS |
| TC-B-EXT-04 | Response field `shipping_address` schema check | Nested Schema Validation | AI schema validation chỉ kiểm tra top-level field. | 200 OK – `shipping_address` hợp lệ. | PASS |
| TC-B-EXT-05 | Gọi API với `Authorization: Basic <base64>` thay vì Bearer token | Invalid Auth Scheme / Security | AI chỉ test Bearer format variants nhưng không test scheme sai hoàn toàn (Basic auth). | 401 Unauthorized – server phải reject Basic auth scheme và yêu cầu Bearer JWT. | FAIL (Got 403) |
| TC-B-EXT-06 | Header Authorization có keyword `bearer` viết thường (case insensitivity) | Auth Header Normalization / Security | AI không kiểm tra tính chuẩn hóa scheme theo RFC 6750. | 200 OK (chấp nhận bearer thường) hoặc 401 Unauthorized. | PASS |
| TC-B-EXT-07 | Response khi user có đơn hàng với các trạng thái enum khác nhau | State Coverage / Schema Validation | AI test từng trạng thái riêng lẻ nhưng không test bao phủ enum trong danh sách thực tế. | 200 OK – tất cả đơn hàng có field status thuộc enum hợp lệ. | PASS |

---

## Kết quả Audit (do người review)

| Nhãn | Số lượng | Tỷ lệ | Lý do phổ biến |
|:-----|:---------|:------|:---------------|
| VALID | 36 | 94.7% | TC đúng kỹ thuật, input rõ ràng, expected output đúng spec (đã chuẩn hóa 200 OK cho query params không có trong spec) |
| INVALID | 0 | 0% | – |
| INCOMPLETE | 2 | 5.3% | SQL injection và custom header privilege escalation cần làm rõ assertion không lộ SQL error |
| **Tổng** | **38** | **100%** | |

### Các TC cần sửa (INCOMPLETE)

| TC ID | Nhãn | Lý do | Nội dung sửa |
|:------|:-----|:------|:-------------|
| TC-B-SEC-03 | INCOMPLETE | Header X-Admin tùy biến chưa rõ ràng | Sửa expected: 200 OK chỉ trả đơn của user, header lạ bị ignore. |
| TC-B-SEC-06 | INCOMPLETE | Expected "400 Bad Request" chưa rõ ràng | Sửa expected: "200 OK hoặc 400 – KHÔNG có SQL error trong response body". |

---

## Kết quả thực thi (Execute)

- **Công cụ:** Newman 6.2.2 + newman-reporter-htmlextra
- **Header bắt buộc:** `X-Student-Id: 23127486`
- **Collection:** `postman/hw06_api2_collection.json` (47 requests gồm 2 setup login)
- **Report HTML:** `newman_reports/newman_api2_report.html`

| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| PASS | 58 | 89.2% |
| FAIL | 7 | 10.8% |
| **Tổng** | 65 (assertions) | 100% |

**Danh sách TC FAIL (phát hiện bug thực của hệ thống):**

| TC ID | Assertion | Actual (Bug) |
|:---|:---|:---|
| TC-B-DP-06 | Status 401 (forged token) | Got **403** – server trả 403 Forbidden thay vì 401 Unauthorized |
| TC-B-DP-07 | Status 401 (expired token) | Got **403** – server trả 403 Forbidden thay vì 401 Unauthorized |
| TC-B-ST-07 | Status 401 (session expired) | Got **403** – server trả 403 Forbidden thay vì 401 Unauthorized |
| TC-B-SEC-04 | Status 401 (forged JWT) | Got **403** – server trả 403 Forbidden thay vì 401 Unauthorized |
| TC-B-SEC-05 | Status 401 (expired JWT) | Got **403** – server trả 403 Forbidden thay vì 401 Unauthorized |
| TC-B-EXT-02 | Status 401 (alg: none rejected) | Got **403** – server trả 403 Forbidden thay vì 401 Unauthorized |
| TC-B-EXT-05 | Status 401 (Basic auth rejected) | Got **403** – server trả 403 Forbidden thay vì 401 Unauthorized |

*(Screenshot Newman / Postman Console đính kèm tại đây)*
