# Test Cases – API 1 (Pool A)

**Sinh viên:** Phan Quốc Thịnh – 23127486 – 23KTPM3  
**Feature:** FR-01 – Đăng ký tài khoản  
**Endpoint:** `POST /api/register`

---

## Tổng quan

| Mục | Giá trị |
|:---|:---|
| **API** | POST /api/register – Đăng ký tài khoản |
| **Pool** | A |
| **Tổng TC (AI sinh)** | 42 (DP/BVA: 20 \| ST: 5 \| SEC: 9 \| SV: 8) |
| **TC tự thêm** | 13 (TC-A-EXT-01 đến TC-A-EXT-13) |
| **Tổng TC** | 55 |

---

## Phân loại test cases

### A. Domain Partition & Boundary Value Tests (EP & BVA)

| TC ID | Mô tả | Tham số kiểm tra | Phân vùng / Điểm biên | Input Payload (Params/Body) | Expected HTTP Status & Output | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|:---|
| TC-A-DP-01 | Đăng ký hợp lệ – tất cả trường đúng chuẩn | name, email, password | Valid EP – happy path | `{"name":"Nguyen Van A","email":"test@domain.com","password":"Password123!"}` | 200 OK – `{"message":"User registered successfully","id":...}` | **VALID** | Happy path đủ 3 trường hợp lệ, expected output đúng spec. |
| TC-A-DP-02 | Đăng ký hợp lệ – name chứa ký tự Unicode (tiếng Việt) | name | Valid EP | `{"name":"Nguyễn Văn Ánh","email":"unicode@test.com","password":"Pass123!"}` | 200 OK – đăng ký thành công | **VALID** | Kiểm thử name Unicode là edge case quan trọng, đúng EP hợp lệ. |
| TC-A-DP-03 | Đăng ký hợp lệ – email dạng sub-domain | email | Valid EP | `{"name":"User A","email":"user@mail.sub.com","password":"Pass123!"}` | 200 OK – đăng ký thành công | **VALID** | Sub-domain email là định dạng hợp lệ theo RFC 5321. |
| TC-A-DP-04 | name là chuỗi rỗng | name | Invalid EP – required field | `{"name":"","email":"a@test.com","password":"Pass123!"}` | 400 Bad Request – lỗi validation name | **VALID** | Cô lập lỗi đúng: chỉ name rỗng, các trường khác hợp lệ. |
| TC-A-DP-05 | name thiếu hoàn toàn (không có key) | name | Invalid EP – missing field | `{"email":"a@test.com","password":"Pass123!"}` | 400 Bad Request – thiếu trường name | **VALID** | Phân biệt missing field vs empty string – đúng nguyên tắc EP. |
| TC-A-DP-06 | email sai định dạng – thiếu @ | email | Invalid EP – format | `{"name":"User A","email":"invalidemail.com","password":"Pass123!"}` | 400 Bad Request – email không hợp lệ | **VALID** | Thiếu @ là một trong các invalid EP định dạng email. |
| TC-A-DP-07 | email sai định dạng – thiếu domain | email | Invalid EP – format | `{"name":"User A","email":"user@","password":"Pass123!"}` | 400 Bad Request – email không hợp lệ | **VALID** | Thiếu domain sau @ là invalid EP khác. |
| TC-A-DP-08 | email là chuỗi rỗng | email | Invalid EP – required field | `{"name":"User A","email":"","password":"Pass123!"}` | 400 Bad Request – lỗi validation email | **VALID** | Phân biệt empty vs missing. Cô lập lỗi đúng chuẩn. |
| TC-A-DP-09 | email thiếu hoàn toàn (không có key) | email | Invalid EP – missing field | `{"name":"User A","password":"Pass123!"}` | 400 Bad Request – thiếu trường email | **VALID** | Đúng nguyên tắc cô lập lỗi từng field. |
| TC-A-DP-10 | password là chuỗi rỗng | password | Invalid EP – required field | `{"name":"User A","email":"a@test.com","password":""}` | 400 Bad Request – lỗi validation password | **VALID** | Cô lập lỗi đúng. |
| TC-A-DP-11 | password thiếu hoàn toàn (không có key) | password | Invalid EP – missing field | `{"name":"User A","email":"a@test.com"}` | 400 Bad Request – thiếu trường password | **VALID** | Cô lập lỗi đúng. |
| TC-A-DP-12 | password quá ngắn – 1 ký tự (BVA dưới min) | password | BVA – below min | `{"name":"User A","email":"a@test.com","password":"A"}` | 400 Bad Request – password quá ngắn (min = 8) | **VALID** | Spec xác định min password = 8 ký tự; 1 ký tự là BVA dưới min, phải bị reject. |
| TC-A-DP-13 | password đúng độ dài tối thiểu – 8 ký tự (BVA tại min) | password | BVA – at min | `{"name":"User A","email":"a@test.com","password":"Aa1!xxYZ"}` | 200 OK – đăng ký thành công | **VALID** | Spec min = 8; đúng tại ngưỡng tối thiểu → phải được chấp nhận. |
| TC-A-DP-14 | password 7 ký tự (BVA dưới min – 1) | password | BVA – below min (min−1) | `{"name":"User A","email":"a@test.com","password":"Aa1!xxY"}` | 400 Bad Request – password quá ngắn (cần đủ 8 ký tự) | **VALID** | 7 ký tự = min−1 – điểm biên ngay dưới ngưỡng tối thiểu, phải bị reject. |
| TC-A-DP-15 | name rất dài – 256 ký tự (BVA vượt max) | name | BVA – above max | `{"name":"AAAAAA...(256 chars)","email":"a@test.com","password":"Pass123!"}` | 400 Bad Request – name quá dài | **INCOMPLETE** | Spec không định nghĩa max-length name. Nếu hệ thống không giới hạn độ dài, expected có thể là 200 OK. **Sửa:** Kiểm tra DB schema/spec trước. Nếu VARCHAR(255) → expected 400. Nếu TEXT → expected 200 OK. |
| TC-A-DP-16 | name đúng giới hạn tối đa – 255 ký tự (BVA tại max) | name | BVA – at max | `{"name":"AAAA...(255 chars)","email":"a@test.com","password":"Pass123!"}` | 200 OK – đăng ký thành công | **INCOMPLETE** | Giống DP-15: cần xác nhận giới hạn từ spec/DB schema. Chỉ hợp lệ khi tồn tại rule max=255. |
| TC-A-DP-17 | email đã tồn tại trong hệ thống | email | Invalid EP – duplicate | `{"name":"User A","email":"existing@domain.com","password":"Pass123!"}` | 400/409 Conflict – email đã được đăng ký | **VALID** | Duplicate email là invalid EP quan trọng. Expected 400 hoặc 409 – cả hai đều hợp lý; cần xác nhận status code từ API thực tế. |
| TC-A-DP-18 | Toàn bộ body là JSON rỗng `{}` | name, email, password | Invalid EP – empty body | `{}` | 400 Bad Request – thiếu tất cả trường | **VALID** | Kiểm thử đồng thời missing tất cả fields là hợp lý cho case body rỗng. |
| TC-A-DP-19 | Body không phải JSON (plain text) | Content-Type | Invalid EP – wrong content type | Body: `name=User&email=a@b.com` không có header JSON | 400 Bad Request hoặc 415 Unsupported Media Type | **VALID** | Kiểm tra content negotiation đúng spec REST. |
| TC-A-DP-20 | password chỉ có ký tự số (không có chữ hoa/ký tự đặc biệt) | password | Invalid EP – weak password policy | `{"name":"User A","email":"a@test.com","password":"12345678"}` | 400 Bad Request – password yếu (nếu có rule) | **INCOMPLETE** | Expected "nếu có rule" không thể tự động hóa. **Sửa:** Kiểm tra spec: nếu không có password complexity rule → expected là 200 OK; nếu có rule yêu cầu uppercase/special char → expected là 400. |

### B. State Transition & Lifecycle Tests

| TC ID | Mô tả kịch bản | Trạng thái ban đầu (Pre-state) | Hành động / Payload | Trạng thái kỳ vọng (Post-state) | Expected HTTP Status & Error Code | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|:---|
| TC-A-ST-01 | Đăng ký email mới lần đầu – User chuyển sang Active | Non-existent (email chưa có) | POST /api/register với email mới hợp lệ | User Created / Active (có thể đăng nhập) | 200 OK – `{message, id}` | **VALID** | Resource Lifecycle Non-existent → Created đúng theo State Transition Testing (ISTQB §4.4). |
| TC-A-ST-02 | Đăng ký lại email đã tồn tại – hệ thống từ chối | User Active (email đã register) | POST /api/register với cùng email | Trạng thái không đổi – không tạo user mới | 400/409 Conflict | **VALID** | Invalid transition đúng – system giữ state, từ chối duplicate. |
| TC-A-ST-03 | Đăng ký thành công → Đăng nhập ngay (State sequence) | Non-existent | Register → Login liền với thông tin vừa tạo | User Authenticated (có JWT token hợp lệ) | Register: 200 OK, Login: 200 OK với token | **VALID** | State sequence Created → Authenticated quan trọng để xác nhận tài khoản được tạo đúng. |
| TC-A-ST-04 | Gửi lại cùng request register sau khi đã register thành công | User Active | POST lặp lại payload cũ | Vẫn từ chối – không tạo duplicate | 400/409 Conflict | **VALID** | Idempotency check hợp lệ, trùng với ST-02 về mặt logic nhưng từ góc độ idempotency là khác biệt. |
| TC-A-ST-05 | Đăng ký khi chưa có session/token (Public endpoint) | Unauthenticated | POST /api/register không có Authorization header | User Created (endpoint là public, không cần auth) | 200 OK – đăng ký thành công | **VALID** | Xác nhận đúng rằng /api/register là public endpoint, không yêu cầu auth. |

### C. Security Tests (SEC-01 – SEC-07)

| TC ID | Mô tả | Loại tấn công | Input | Expected | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|:---|
| TC-A-SEC-01 | SQL Injection vào trường email | SQL Injection (SEC-01) | `{"name":"User","email":"' OR 1=1 --","password":"Pass123!"}` | 400 Bad Request – bị block, KHÔNG có lỗi SQL lộ ra | **VALID** | Input SQLi điển hình vào email field, expected output đúng: reject và không lộ SQL error. |
| TC-A-SEC-02 | SQL Injection vào trường name | SQL Injection (SEC-01) | `{"name":"'; DROP TABLE users;--","email":"a@test.com","password":"Pass123!"}` | 400 Bad Request – không thực thi SQL | **VALID** | Drop table payload – kiểm tra xem DB có bị tấn công không. Expected đúng. |
| TC-A-SEC-03 | SQL Injection vào trường password | SQL Injection (SEC-01) | `{"name":"User","email":"b@test.com","password":"' OR '1'='1"}` | 400 Bad Request – không bypass | **INCOMPLETE** | Logic injection vào password khi register thường không có tác dụng vì password được hash, nhưng vẫn nên test để đảm bảo không lộ lỗi SQL. **Sửa:** Expected nên là "200 OK hoặc 400 – quan trọng là response KHÔNG chứa SQL error message". Cần rõ ràng hơn về mục tiêu test. |
| TC-A-SEC-04 | XSS payload trong trường name | Sensitive Data / XSS (SEC-07) | `{"name":"<script>alert(1)</script>","email":"c@test.com","password":"Pass123!"}` | 400 hoặc response trả về escaped string – không thực thi script | **VALID** | XSS trong stored field name là nguy hiểm nếu hiển thị lại mà không escape. Expected hợp lý. |
| TC-A-SEC-05 | Gọi register với Authorization header của user khác | IDOR (SEC-02) | Header: `Authorization: Bearer <valid_token>`, body: email mới | Chỉ tạo user với email mới, không ảnh hưởng tài khoản token | **INCOMPLETE** | TC này test sai khái niệm IDOR. Register là public endpoint, gửi kèm token không gây IDOR. Mục tiêu test không rõ ràng. **Sửa:** Bỏ hoặc thay bằng test "cố gắng register với token của admin để được quyền admin tự động" – Mass Assignment security check. |
| TC-A-SEC-06 | Cố gán role=admin trong body khi đăng ký | Role Escalation (SEC-03) | `{"name":"Hacker","email":"hack@test.com","password":"Pass123!","role":"admin"}` | 200 OK nhưng role PHẢI là user thường, không phải admin | **VALID** | Mass Assignment / Role Escalation test quan trọng. Expected đúng: hệ thống phải ignore trường role từ client. |
| TC-A-SEC-07 | Brute force: gửi nhiều request register liên tục | Rate Limiting (SEC-06) | 100+ requests/giây với email khác nhau | 429 Too Many Requests | **INCOMPLETE** | Expected 429 là đúng nếu có rate limiting, nhưng nhiều API đăng ký không có rate limit. **Sửa:** Cần xác nhận rate limit policy trong spec. Nếu không có policy → expected có thể là 200 OK cho mỗi request. Ghi chú: "Kỳ vọng 429 nếu hệ thống có rate limiting; ghi lại response thực tế nếu không có". |
| TC-A-SEC-08 | Response thành công lộ thông tin nhạy cảm | Sensitive Data Exposure (SEC-07) | POST /api/register hợp lệ | Response KHÔNG chứa password hoặc password hash | **VALID** | Kiểm tra data exposure đúng – password không bao giờ được trả về trong response. |
| TC-A-SEC-09 | Missing Content-Type header | Missing/Invalid Header (SEC-04) | Request không có `Content-Type: application/json` | 400 Bad Request hoặc 415 – không xử lý sai | **VALID** | Content-Type validation quan trọng để đảm bảo API không chấp nhận payload không rõ định dạng. |

### D. Schema Validation Tests

| TC ID | Mô tả | Field kiểm tra | Expected schema | Audit | Ghi chú |
|:---|:---|:---|:---|:---|:---|
| TC-A-SV-01 | Response thành công có đúng các field theo spec | `message`, `id` | `{"message": string, "id": number}` – không thêm/thiếu field | **VALID** | Kiểm tra shape đúng spec. |
| TC-A-SV-02 | Field `message` là string đúng nội dung theo spec | `message` | `"User registered successfully"` (string, không null) | **VALID** | Kiểm tra exact string match theo spec. |
| TC-A-SV-03 | Field `id` là number dương (integer) | `id` | Số nguyên dương > 0, không phải null hay string | **VALID** | Type + value range check. |
| TC-A-SV-04 | Response KHÔNG chứa field `password` hoặc `password_hash` | `password` (phải vắng mặt) | Response body không có key `password`, `hash`, `salt` | **VALID** | Security & Schema – quan trọng để đảm bảo không lộ sensitive data. |
| TC-A-SV-05 | HTTP Status code đúng 200 khi thành công | HTTP Status | Status code = 200 OK (spec ghi 200, không phải 201 Created) | **VALID** | Spec đặc tả 200 OK thay vì 201 Created – cần kiểm tra đúng. |
| TC-A-SV-06 | Response lỗi (400) có cấu trúc nhất quán | error response shape | Phải có field thông báo lỗi (vd: `{"error":...}` hoặc `{"message":...}`) | **VALID** | Error response schema nhất quán quan trọng cho client handling. |
| TC-A-SV-07 | Kiểu dữ liệu field `id` không phải string | `id` | `id` phải là number, KHÔNG phải `"1"` (string) | **INCOMPLETE** | TC này trùng ý với SV-03 (đã kiểm tra id là number dương). **Sửa:** Gộp vào SV-03 hoặc tách thành test case độc lập với input đặc thù để phân biệt. Nếu giữ riêng: xác nhận rõ assertion "typeof id === 'number'" là đủ. |
| TC-A-SV-08 | Response Content-Type header là application/json | Content-Type header | `Content-Type: application/json` hoặc `application/json; charset=utf-8` | **VALID** | Content-Type response header validation – chuẩn REST API. |

### E. Test Cases tự thêm (Extend – ≥ 5)

> **Phân tích điểm yếu của test suite AI:** AI đã bao phủ tốt các EP/BVA cơ bản và security patterns phổ biến (SQLi, XSS, Role Escalation). Tuy nhiên, AI bỏ sót các kịch bản: (1) race condition / concurrent registration, (2) email normalization / case sensitivity, (3) HTTP verb tampering, (4) mass assignment với các trường ẩn khác, (5) Unicode trong email, (6) timing attack trên email existence check, (7) CORS behavior, **(8) JSON null value cho name và password** – AI test empty string và missing key nhưng không phân biệt null type cho cả 3 field bắt buộc.

| TC ID | Mô tả | Loại | Lý do AI bỏ sót | Expected | Kết quả |
|:---|:---|:---|:---|:---|:---|
| TC-A-EXT-01 | Đăng ký đồng thời (concurrent) 2 request với cùng email mới | Race Condition / Business Logic | AI không mô hình hóa concurrent state – prompt tập trung vào single-request scenarios. Race condition đòi hỏi hiểu biết về DB-level locking mà LLM không tự suy luận. | Chỉ 1 trong 2 request được tạo thành công (200 OK), request còn lại trả về 400/409 Conflict – không được tạo duplicate user. | *(sau execute)* |
| TC-A-EXT-02 | Email với chữ hoa (TEST@DOMAIN.COM) đăng ký sau email thường (test@domain.com) | Email Case Normalization / Business Logic | AI không kiểm tra email case-insensitivity. RFC 5321 cho phép local-part case-sensitive nhưng thực tiễn hầu hết hệ thống normalize email thành lowercase. Prompt không đề cập normalization policy. | 400/409 Conflict – hệ thống phải treat email là case-insensitive (TEST@ == test@). Hoặc 200 OK nếu hệ thống case-sensitive (cần ghi nhận hành vi thực tế). | *(sau execute)* |
| TC-A-EXT-03 | HTTP Verb Tampering: gửi PUT /api/register thay vì POST | HTTP Verb Tampering / Security | AI không test HTTP method ngoài GET/POST. Prompt không yêu cầu test method tampering ngoài wrong method. PUT có thể bị server xử lý khác hoặc bypass một số middleware. | 404 Not Found hoặc 405 Method Not Allowed – server không cho phép PUT /api/register. | *(sau execute)* |
| TC-A-EXT-04 | Cố gán thêm field `is_verified: true` hoặc `created_at: "2000-01-01"` trong body | Mass Assignment (Extended) / Security | AI chỉ test role=admin trong mass assignment. Các trường nhạy cảm khác (is_verified, created_at, updated_at, balance) thường cũng bị lộ qua mass assignment nếu ORM không được cấu hình đúng. Đây là model limitation: AI không biết toàn bộ schema DB. | 200 OK nhưng các trường is_verified, created_at phải bị IGNORE – không ảnh hưởng đến giá trị thực trong DB. | *(sau execute)* |
| TC-A-EXT-05 | Email chứa ký tự đặc biệt hợp lệ theo RFC 5321: `user+tag@domain.com` (plus addressing) | Edge Case – Email Format / EP | AI sinh 2 valid email case (sub-domain, Unicode name) nhưng bỏ sót plus addressing và quoted strings. Prompt chỉ đề cập sub-domain email. Plus addressing phổ biến trong Gmail và cần được chấp nhận. | 200 OK – email `user+tag@domain.com` là hợp lệ và phải được chấp nhận. | *(sau execute)* |
| TC-A-EXT-06 | Timing Attack: so sánh response time giữa email tồn tại vs không tồn tại | Timing Attack / Security | AI không kiểm tra timing side-channel trong authentication/registration. Đây là security concern nâng cao mà model LLM thường không biết nếu không được prompt cụ thể. Nếu response time khác nhau đáng kể, attacker có thể enumerate valid emails. | Response time cho cả hai trường hợp phải xấp xỉ nhau (< 200ms difference) – không lộ thông tin qua timing. | *(sau execute)* |
| TC-A-EXT-07 | Body với trường `email` là `null` (JSON null, không phải chuỗi) | Edge Case – Null Type / EP | AI test empty string và missing field nhưng không test JSON null value. `null` là giá trị JSON hợp lệ nhưng khác với `""` và missing key – cần xử lý riêng. | 400 Bad Request – email là null không phải giá trị hợp lệ. | *(sau execute)* |
| TC-A-EXT-08 | Body với trường `name` là `null` (JSON null) – `{"name":null,"email":"a@test.com","password":"Pass123!"}` | Edge Case – Null Type / EP | Tương tự EXT-07: AI chỉ test empty string (`""`) và missing key cho name, không test giá trị JSON null. `null` là kiểu dữ liệu khác hoàn toàn với chuỗi rỗng và cần được validate riêng. Nếu server không xử lý đúng, null có thể bị cast thành string `"null"` và chấp nhận sai. | 400 Bad Request – name là null không phải giá trị hợp lệ; server không được chấp nhận hoặc cast `null` thành string. | *(sau execute)* |
| TC-A-EXT-09 | Body với trường `password` là `null` (JSON null) – `{"name":"User A","email":"a@test.com","password":null}` | Edge Case – Null Type / EP | Tương tự EXT-07 và EXT-08: AI test empty string và missing key cho password nhưng không test JSON null. Đặc biệt nguy hiểm: nếu server không validate null cho password, user có thể được tạo với password null/empty trong DB, dẫn đến account không thể đăng nhập hoặc có thể bị bypass auth. | 400 Bad Request – password là null không phải giá trị hợp lệ; tuyệt đối không được tạo account với password null. | *(sau execute)* |
| TC-A-EXT-10 | `name` dài 256 ký tự (BVA trên max) – `{"name":"A" × 256, "email":"a@test.com","password":"Pass123!"}` | BVA – Above Max / EP | TC-A-DP-15 trong phần AI đã test name 256 ký tự nhưng bị đánh INCOMPLETE vì expected output chưa được xác nhận (giả định max=255 nhưng không có trong spec). TC này làm rõ lại: kiểm tra source code xác nhận DB column `name VARCHAR(255)` – do đó 256 ký tự là BVA trên max và phải bị reject. AI đã sinh TC này nhưng expected mơ hồ; extend để có TC đầy đủ với input cụ thể và expected xác nhận rõ. | 400 Bad Request – name vượt 255 ký tự (giới hạn VARCHAR(255) trong DB); response phải chứa thông báo lỗi validation rõ ràng, không bị truncate thầm lặng. | *(sau execute)* |
| TC-A-EXT-11 | email thiếu local-part (chỉ có domain): `@domain.com` | Edge Case – Email Format / EP | AI test email thiếu `@` (DP-06) và thiếu domain sau `@` (DP-07), nhưng không test trường hợp ngược lại: có `@` nhưng thiếu phần trước `@` (local-part). Đây là invalid EP đối xứng cần có để phủ đủ các dạng sai định dạng email. Prompt chỉ yêu cầu 2 dạng sai email phổ biến. | 400 Bad Request – email `@domain.com` không hợp lệ (thiếu local-part theo RFC 5321). | *(sau execute)* |
| TC-A-EXT-12 | XSS payload trong trường `email`: `{"name":"User A","email":"<script>alert(1)</script>@test.com","password":"Pass123!"}` | XSS / Stored XSS (SEC-07) | AI chỉ test XSS trong trường `name` (TC-A-SEC-04) nhưng không test XSS trong `email`. Nếu email được hiển thị lại trên UI mà không escape, stored XSS trong email có thể bị khai thác trong trang admin hoặc profile. Prompt chỉ yêu cầu XSS trong name. | 400 Bad Request – email có ký tự `<>` không hợp lệ; hoặc nếu chấp nhận thì dữ liệu được lưu phải được HTML-escaped khi hiển thị – không thực thi JS. | *(sau execute)* |
| TC-A-EXT-13 | XSS payload trong trường `password`: `{"name":"User A","email":"a@test.com","password":"<script>alert(1)</script>"}` | XSS / Input Validation (SEC-07) | AI chỉ test XSS trong `name` (TC-A-SEC-04), không test XSS trong `password`. Dù password được hash nên không thể stored XSS, nhưng: (1) cần đảm bảo server không reflect payload trong response error message; (2) một số hệ thống log password trước khi hash (lỗi lập trình) dận đến XSS trong log viewer. | 200 OK hoặc 400 – response không reflect XSS payload; error message (nếu có) phải được sanitize, không thực thi script. | *(sau execute)* |

---

## Kết quả Audit (do người review)

| Nhãn | Số lượng | Tỷ lệ | Lý do phổ biến |
|:-----|:---------|:------|:---------------|
| VALID | 31 | 73.8% | TC đúng kỹ thuật EP/BVA/ST/SEC/SV, input rõ ràng, expected output đúng spec |
| INVALID | 0 | 0% | – |
| INCOMPLETE | 11 | 26.2% | Expected output mơ hồ ("tuỳ rule"), không xác định rule từ spec; một số TC trùng ý; một số TC test sai khái niệm |
| **Tổng** | **42** | **100%** | |

### Các TC cần sửa (INCOMPLETE)

| TC ID | Nhãn | Lý do | Nội dung sửa |
|:------|:-----|:------|:-------------|
| TC-A-DP-15 | INCOMPLETE | Expected "400 – name quá dài" giả định max=255 chưa xác nhận | Kiểm tra DB schema (VARCHAR(255)?) rồi điều chỉnh expected (đã làm rõ ở TC-A-EXT-10). |
| TC-A-DP-16 | INCOMPLETE | Tương tự DP-15 – BVA tại max chỉ valid khi tồn tại giới hạn | Xác nhận max-length từ spec/DB trước. |
| TC-A-DP-20 | INCOMPLETE | Expected "400 nếu có rule" không thể tự động hóa | Kiểm tra password complexity policy trong spec/source code. |
| TC-A-SEC-03 | INCOMPLETE | Injection vào password khi register ít nguy hiểm (hashed), mục tiêu test chưa rõ | Đổi expected: "Response 200 OK và KHÔNG chứa SQL error message trong body". |
| TC-A-SEC-05 | INCOMPLETE | IDOR test không áp dụng đúng cho public endpoint register | Thay bằng TC-A-EXT-04 (Mass Assignment với is_verified). |
| TC-A-SEC-07 | INCOMPLETE | Kỳ vọng 429 nhưng không xác nhận rate limit policy | Ghi chú: "Expected 429 nếu có rate limit; ghi nhận response thực tế nếu không có". |
| TC-A-SV-07 | INCOMPLETE | Trùng ý với SV-03 – có thể gộp | Giữ nhưng thêm assertion rõ ràng: `typeof response.id === 'number'`. |

---

## Kết quả thực thi (Execute)

- **Công cụ:** Newman 6.2.2 + newman-reporter-html
- **Header bắt buộc:** `X-Student-Id: 23127486`
- **Collection:** `postman/hw06_api1_collection.json`
- **Report HTML:** `newman_reports/newman_api1_report.html`

| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| PASS | 32 | 60.4% |
| FAIL | 21 | 39.6% |
| **Tổng** | 53 (assertions) | 100% |

**Danh sách TC FAIL (phát hiện bug thực của hệ thống):**

| TC ID | Assertion | Actual (Bug) |
|:---|:---|:---|
| TC-A-DP-04 | Status 400 (empty name) | Got **200** – server chấp nhận name rỗng |
| TC-A-DP-05 | Status 400 (missing name) | Got **200** – server chấp nhận thiếu name |
| TC-A-DP-06 | Status 400 (email no @) | Got **200** – server không validate email format |
| TC-A-DP-07 | Status 400 (email no domain) | Got **200** – server không validate email format |
| TC-A-DP-08 | Status 400 (empty email) | Got **200** – server chấp nhận email rỗng |
| TC-A-DP-09 | Status 400 (missing email) | Got **200** – server chấp nhận thiếu email |
| TC-A-DP-10 | Status 400 (empty password) | Got **200** – server chấp nhận password rỗng |
| TC-A-DP-11 | Status 400 (missing password) | Got **200** – server chấp nhận thiếu password |
| TC-A-DP-12 | Status 400 (password too short) | Got **200** – không enforce min length |
| TC-A-DP-14 | Status 400 (password 7 chars) | Got **200** – không enforce min length |
| TC-A-DP-17 | Status 400/409 (duplicate email) | Got **200** – cho phép đăng ký email trùng |
| TC-A-DP-18 | Status 400 (empty JSON body) | Got **200** – không validate required fields |
| TC-A-DP-19 | Status 400/415 (wrong content-type) | Got **500** – server crash thay vì trả lỗi |
| TC-A-ST-02 | Status 400/409 (duplicate) | Got **200** – cùng bug với DP-17 |
| TC-A-SEC-01 | Status 400 (SQLi blocked) | Got **200** – không sanitize email input |
| TC-A-SV-06 | Status 400 (empty body error) | Got **200** – cùng bug với DP-18 |
| TC-A-EXT-07 | Status 400 (null email) | Got **200** – null email được chấp nhận |
| TC-A-EXT-08 | Status 400 (null name) | Got **200** – null name được chấp nhận |
| TC-A-EXT-09 | Status 400 (null password) | Got **200** – null password được chấp nhận |
| TC-A-EXT-11 | Status 400 (email no local-part) | Got **200** – @domain.com được chấp nhận |
| TC-A-EXT-12 | Status 400 (XSS in email) | Got **200** – XSS trong email không bị reject |

*(Screenshot Newman / Postman Console đính kèm tại đây)*
