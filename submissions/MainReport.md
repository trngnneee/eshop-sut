# HW06 – Báo cáo Kiểm thử API

**Khoa Công nghệ Thông tin (FIT) – Trường Đại học Khoa học Tự nhiên TP.HCM (HCMUS)**  
**CS423 / CSC13003 – Kiểm thử Phần mềm (AI-augmented · 2026)**

---

## Thông tin sinh viên

| Trường | Giá trị |
|:---|:---|
| **Họ và tên:** | Phan Quốc Thịnh |
| **MSSV:** | 23127486 |
| **Lớp:** | 23KTPM3 |
| **Ngày:** | *(cập nhật khi nộp)* |

---

## 1. Giới thiệu

*(Mô tả ngắn về bài tập, hệ thống SUT EShop, và 3 API được chọn.)*

### 1.1. Hệ thống cần kiểm thử (SUT)

- **Tên:** EShop – Ứng dụng thương mại điện tử demo
- **Repository:** https://github.com/ttbhanh/eshop-sut

### 1.2. Các API được chọn

| Pool | Feature | Endpoint | Mô tả |
|:---|:---|:---|:---|
| Pool A | FR-01 – Đăng ký tài khoản | `POST /api/register` | Đăng ký tài khoản người dùng mới |
| Pool B | FR-11 – Xem lịch sử đơn hàng | `GET /api/orders/my-orders` | Lấy danh sách đơn hàng cá nhân của user hiện tại |
| Pool C | FR-16 – Import sản phẩm (Admin) | `POST /api/admin/import-products` | Admin import hàng loạt sản phẩm từ JSON Array |

### 1.3. Công cụ sử dụng

- *(Tên AI tool, Postman, Newman, ...)*

---

## 2. API 1 – Pool A: Đăng ký tài khoản (FR-01)

> **Endpoint:** `POST /api/register`  
> **Feature:** FR-01 – Đăng ký tài khoản

### 2.1. Bước 1: Sinh test cases bằng AI (Generate)

**Prompt 1 – Domain Testing (EP & BVA):**
```
Dựa trên API spec của endpoint POST /api/register, hãy áp dụng kỹ thuật Domain Testing
(Equivalence Partitioning & Boundary Value Analysis) để thiết kế test cases theo các quy tắc sau:

1. Phân tích biến: Liệt kê tất cả tham số đầu vào/ra, xác định các lớp tương đương Hợp lệ (Valid EP),
   Không hợp lệ (Invalid EP: sai kiểu, chuỗi rỗng, vượt ngưỡng, ký tự đặc biệt,...) và các giá trị
   biên (BVA 2-point/3-point).
2. Nguyên tắc tạo Test Case:
   * Valid Cases: Kết hợp tối đa các lớp hợp lệ vào cùng 1 test case.
   * Invalid / Boundary Cases (Cô lập lỗi): Mỗi test case chỉ chứa DUY NHẤT 1 giá trị không hợp lệ
     hoặc 1 giá trị biên lỗi; toàn bộ các tham số còn lại bắt buộc phải dùng giá trị đại diện hợp lệ.
   * Đảm bảo phủ hết tất cả các EP và BVA đã xác định.

Xuất kết quả theo định dạng bảng:
| TC ID | Mô tả | Tham số kiểm tra | Phân vùng / Điểm biên | Input Payload (Params/Body) | Expected HTTP Status & Output |

API Spec:
- Endpoint: POST /api/register
- Body (JSON): {"name": "Nguyen Van A", "email": "test@domain.com", "password": "Password123!"}
- Response thành công (200 OK): {"message": "User registered successfully", "id": 1}
- Tất cả 3 trường đều bắt buộc, không yêu cầu auth
```

*Output AI 1 (tóm tắt):* (Chi tiết xem file AI_Audit.md)
AI sinh ra 20 test cases Domain EP & BVA, bao gồm: 3 valid case (happy path, Unicode name, sub-domain email),
17 invalid/boundary cases cô lập lỗi từng trường (name rỗng, email sai định dạng, password BVA ngắn/dài,
email duplicate, body rỗng, wrong content-type, v.v.)

**Prompt 2 – State Transition & Lifecycle:**
```
Dựa trên API spec của endpoint POST /api/register, hãy áp dụng kỹ thuật State Transition Testing
để thiết kế test cases theo các yêu cầu sau:

1. Xác định mô hình trạng thái: Nhận diện thực thể User (Resource Lifecycle) và Auth State,
   liệt kê tất cả State và Event/Action (được kích hoạt bởi endpoint này).
2. Xây dựng kịch bản chuyển đổi:
   * Chuyển đổi hợp lệ (Valid Transition): Gọi endpoint khi thực thỉ ở đúng trạng thái cho phép.
   * Chuyển đổi không hợp lệ (Invalid Transition): Gọi endpoint khi đã tồn tại (duplicate).
   * Kịch bản chuỗi (State Sequence): Kiểm tra tính toàn vẹn sau khi chuyển trạng thái.

Xuất kết quả theo định dạng bảng:
| TC ID | Mô tả kịch bản | Trạng thái ban đầu (Pre-state) | Hành động / Payload | Trạng thái kỳ vọng (Post-state) | Expected HTTP Status & Error Code |

API Spec: POST /api/register – public endpoint, tạo user mới, trả về {message, id}.
Trạng thái: Non-existent → Created (Active) | Duplicate → reject | Unauthenticated → được phép gọi.
```

*Output AI 2 (tóm tắt):*
AI sinh ra 5 test cases State Transition: Resource Lifecycle (Non-existent → Created), Duplicate rejection,
State Sequence (Register → Login), Idempotency check, Auth State (public endpoint không cần token).

**Prompt 3 – Security Tests (SEC-01 – SEC-07):**
```
Đối với endpoint POST /api/register, hãy sinh test cases bảo mật cho từng loại sau:
SQL Injection (vào từng field: name, email, password), XSS payload trong name,
IDOR (gửi kèm token của user khác), Role Escalation (gán role=admin trong body),
Rate Limiting (brute force), Sensitive Data Exposure (response lộ password hash).

Với mỗi loại, cung cấp:
[TC ID | Mô tả | Loại tấn công | Input | Expected Response]
```

*Output AI 3 (tóm tắt):*
AI sinh ra 9 test cases security: 3 SQL Injection (email/name/password), 1 XSS, 1 IDOR, 1 Role Escalation,
1 Rate Limiting, 1 Sensitive Data Exposure, 1 Missing Content-Type.

**Prompt 4 – Schema Validation:**
```
Dựa vào response schema của POST /api/register trong API spec, hãy sinh test cases
Schema Validation để kiểm tra:
- Response có đủ các field theo spec: message (string), id (number)
- Kiểu dữ liệu chính xác (id phải là number, không phải string)
- Response KHÔNG chứa thông tin nhạy cảm (password, hash)
- HTTP status code đúng (200 OK)
- Content-Type: application/json
- Response lỗi có cấu trúc nhất quán

Bảng: [TC ID | Mô tả | Field kiểm tra | Expected schema]
```

*Output AI 4 (tóm tắt):*
AI sinh ra 8 test cases Schema Validation: kiểm tra shape (message+id), nội dung message, kiểu id,
vắng mặt password field, HTTP 200, error shape 400, type check id, Content-Type.

**Số test cases AI sinh ra:** 42 (DP/BVA: 20 | ST: 5 | SEC: 9 | SV: 8).

### 2.2. Bước 2: Kiểm tra (Audit)

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




| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| VALID | 31 | 73.8% |
| INVALID | 0 | 0% |
| INCOMPLETE | 11 | 26.2% |
| **Tổng** | **42** | **100%** |

**Nhận xét tổng quan về chất lượng output AI:**
AI sinh ra 42 TC có cấu trúc tốt, bao phủ đầy đủ các kỹ thuật EP/BVA, State Transition, Security và Schema Validation. Ưu điểm: cô lập lỗi tốt trong EP/BVA, xác định đúng happy path và invalid EP cho 3 field bắt buộc. Sau khi xác nhận spec (min password = 8), các TC DP-12/13/14 được sửa lại và nâng lên VALID. Vẫn còn 11 TC INCOMPLETE do expected output phụ thuộc vào rule chưa xác nhận trong spec (name max-length, password complexity) hoặc test sai khái niệm (TC-A-SEC-05 IDOR trên public endpoint), hoặc trùng ý (SV-07 vs SV-03).

### 2.3. Bước 3: Bổ sung (Extend)

**Phân tích điểm yếu:** AI bỏ sót race condition, email normalization, HTTP verb tampering, mass assignment extended fields, plus-addressing email, timing attack, và null-type edge case.

| TC ID | Mô tả | Lý do AI bỏ sót |
|:---|:---|:---|
| TC-A-EXT-01 | Đăng ký đồng thời 2 request với cùng email mới (race condition) | AI không mô hình hóa concurrent state; prompt tập trung single-request scenarios |
| TC-A-EXT-02 | Email chữ hoa (TEST@DOMAIN.COM) sau khi đã đăng ký email thường | AI không kiểm tra email case-insensitivity / normalization policy |
| TC-A-EXT-03 | HTTP Verb Tampering: PUT /api/register thay vì POST | AI không test method ngoài GET/POST; prompt không yêu cầu method tampering |
| TC-A-EXT-04 | Mass Assignment extended: cố gán `is_verified: true`, `created_at` trong body | AI chỉ test role=admin; không biết toàn bộ schema DB (model limitation) |
| TC-A-EXT-05 | Email plus-addressing hợp lệ: `user+tag@domain.com` | AI không đề cập plus addressing; prompt chỉ đề cập sub-domain email |
| TC-A-EXT-06 | Timing Attack: so sánh response time email tồn tại vs không tồn tại | Security nâng cao mà LLM không biết nếu không được prompt cụ thể |
| TC-A-EXT-07 | Body với `email` là `null` (JSON null, khác `""` và missing key) | AI test empty string và missing nhưng không test JSON null type |
| TC-A-EXT-08 | Body với `name` là `null` – có thể bị cast sai thành string `"null"` | AI chỉ test empty string và missing key cho name, không test null type; AI không phân biệt 3 dạng khác nhau của "không có giá trị" |
| TC-A-EXT-09 | Body với `password` là `null` – nguy hiểm nếu server tạo account với password null | AI test empty string và missing key cho password nhưng không test null; null password có thể gây bypass auth |
| TC-A-EXT-10 | `name` dài 256 ký tự (BVA trên max) – làm rõ TC-A-DP-15 bị INCOMPLETE | TC-A-DP-15 (AI sinh) có expected mơ hồ vì chưa xác nhận max-length; kiểm tra source code xác nhận VARCHAR(255) → extend với expected rõ ràng: 400 Bad Request |
| TC-A-EXT-11 | Email thiếu local-part: `@domain.com` (có `@` nhưng không có phần trước `@`) | AI test thiếu `@` (DP-06) và thiếu domain sau `@` (DP-07) nhưng bỏ sót trường hợp ngược lại – đây là invalid EP đối xứng cần có |
| TC-A-EXT-12 | XSS payload trong trường `email`: `<script>alert(1)</script>@test.com` | AI chỉ test XSS trong `name`, bỏ sót `email` – Stored XSS trong email có thể bị khai thác trong trang admin/profile |
| TC-A-EXT-13 | XSS payload trong trường `password`: `<script>alert(1)</script>` | AI chỉ test XSS trong `name`, bỏ sót `password` – cần đảm bảo server không reflect XSS trong error response |

### 2.4. Bước 4: Thực thi (Execute)

- **Công cụ:** Newman 6.2.2 + newman-reporter-html
- **Collection:** `postman/hw06_api1_collection.json`
- **Report HTML:** `newman_reports/newman_api1_report.html`
- **Header bắt buộc:** `X-Student-Id: 23127486`

| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| PASS | **32** | 60.4% |
| FAIL | **21** | 39.6% |
| **Tổng assertions** | **53** | 100% |
| **Tổng requests** | **39** | - |

> Newman HTML report: `newman_reports/newman_api1_report.html`

### 2.5. Bước 5: Báo cáo Bug

*(Các bug phát hiện được bằng Newman execution – chi tiết xem `bug_report.md`)*

| Bug ID | Mô tả | Severity | Link Issue |
|:---|:---|:---|:---|
| BUG-A-01 | Không validate required fields (name/email/password) | Critical | *(sinh viên tạo)* |
| BUG-A-02 | Không validate định dạng email | High | *(sinh viên tạo)* |
| BUG-A-03 | Không enforce password minimum length | High | *(sinh viên tạo)* |
| BUG-A-04 | Cho phép đăng ký email trùng (duplicate) | Critical | *(sinh viên tạo)* |
| BUG-A-05 | Server crash 500 khi nhận Content-Type: text/plain | High | *(sinh viên tạo)* |
| BUG-A-06 | SQL Injection trong email không bị chặn | Critical | *(sinh viên tạo)* |
| BUG-A-07 | Chấp nhận JSON null cho name/email/password | High | *(sinh viên tạo)* |
| BUG-A-08 | XSS trong email không bị reject | High | *(sinh viên tạo)* |
| BUG-A-09 | Email @domain.com (thiếu local-part) được chấp nhận | Medium | *(sinh viên tạo)* |

---

## 3. API 2 – Pool B: Xem lịch sử đơn hàng cá nhân (FR-11)

> **Endpoint:** `GET /api/orders/my-orders`  
> **Feature:** FR-11 – Xem lịch sử đơn hàng cá nhân

### 3.1. Bước 1: Sinh test cases bằng AI (Generate)

**Prompt 1 – Domain Testing (EP & BVA):**
```
Dựa trên API spec của endpoint GET /api/orders/my-orders, hãy áp dụng kỹ thuật Domain Testing
(Equivalence Partitioning & Boundary Value Analysis) để thiết kế test cases theo các quy tắc sau:

1. Phân tích biến: Liệt kê tất cả tham số đầu vào (Authorization header, query params tùy chọn),
   xác định các lớp tương đương và giá trị biên.
2. Nguyên tắc:
   * Valid Cases: Kết hợp token hợp lệ với các tham số hợp lệ.
   * Invalid Cases (cô lập lỗi): Mỗi TC chỉ sai 1 giá trị (thiếu token, sai định dạng, token giả, ...).
   * BVA: Giá trị biên của query params (page=0, page=-1, limit=0, limit=9999, ...).

Xuất kết quả theo định dạng bảng:
| TC ID | Mô tả | Tham số kiểm tra | Phân vùng / Điểm biên | Input Payload (Params/Body) | Expected HTTP Status & Output |

API Spec:
- Endpoint: GET /api/orders/my-orders
- Header bắt buộc: Authorization: Bearer <token>
- Response: mảng các đơn hàng của user hiện tại (chỉ của user đó, không phải toàn bộ)
```

*Output AI 1 (tóm tắt):*
AI sinh ra 15 test cases Domain EP & BVA: 2 valid (có đơn/không có đơn), 5 invalid auth (missing/wrong/empty/forged/expired token),
5 BVA query params (page=0/âm/abc, limit=0/9999), 2 edge (unknown params, wrong HTTP method) và 1 method sai.

**Prompt 2 – State Transition & Lifecycle:**
```
Dựa trên API spec của endpoint GET /api/orders/my-orders, hãy áp dụng kỹ thuật State Transition Testing:

1. Xác định mô hình trạng thái:
   - Session/Auth State: Unauthenticated → Authenticated → Token Expired
   - Business State của đơn hàng: pending/confirmed/shipping/delivered/canceled
2. Kịch bản chuyển trạng thái:
   * Vào API khi ở trạng thái auth khác nhau
   * Đơn hàng ở các trạng thái khác nhau có xuất hiện trong danh sách không?
   * State sequence: Checkout → kiểm tra my-orders

Xuất kết quả theo định dạng bảng:
| TC ID | Mô tả kịch bản | Trạng thái ban đầu | Hành động | Trạng thái kỳ vọng | Expected HTTP Status |

API Spec: GET /api/orders/my-orders, yêu cầu Bearer token, trả về mảng đơn của user.
```

*Output AI 2 (tóm tắt):*
AI sinh ra 8 test cases State Transition: 2 auth state (Unauthenticated/Authenticated),
4 business state (đơn pending/confirmed/canceled/delivered trong list), 1 expired token, 1 state sequence (checkout → my-orders).

**Prompt 3 – Security Tests (SEC-01 – SEC-07):**
```
Đối với endpoint GET /api/orders/my-orders, hãy sinh test cases bảo mật cho từng loại:
Missing Auth, IDOR (cố xem đơn user khác qua query param), Role Escalation
(user thường gọi admin endpoint), Token Forgery, Expired Token, SQL Injection (query param),
Sensitive Data Exposure, Admin access only returns own orders.

Với mỗi loại:
[TC ID | Mô tả | Loại tấn công | Input | Expected Response]
```

*Output AI 3 (tóm tắt):*
AI sinh ra 8 test cases security: Missing Auth, IDOR (user_id param), Role Escalation, Token Forgery,
Expired Token, SQL Injection query param, Sensitive Data Exposure, Admin scope isolation.

**Prompt 4 – Schema Validation:**
```
Dựa vào response schema của GET /api/orders/my-orders trong API spec, hãy sinh test cases
Schema Validation để kiểm tra:
- Response là array (kể cả khi rỗng phải trả [] không phải null)
- Mỗi item có các field: id (number), total_amount (number), status (string enum), shipping_address
- Field status thuộc enum: pending/confirmed/shipping/delivered/canceled
- HTTP Status đúng 200 OK
- Content-Type: application/json

Bảng: [TC ID | Mô tả | Field kiểm tra | Expected schema]
```

*Output AI 4 (tóm tắt):*
AI sinh ra 7 test cases Schema Validation: array type, field bắt buộc, kiểu id/total_amount, status enum,
HTTP 200, Content-Type.

**Số test cases AI sinh ra:** 38 (DP/BVA: 15 | ST: 8 | SEC: 8 | SV: 7)

### 3.2. Bước 2: Kiểm tra (Audit)

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




| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| VALID | 27 | 71.1% |
| INVALID | 0 | 0% |
| INCOMPLETE | 11 | 28.9% |
| **Tổng** | **38** | **100%** |

**Nhận xét tổng quan về chất lượng output AI:**
AI sinh ra 38 TC với tỷ lệ VALID cao hơn API 1 (71.1%). Ưu điểm: auth state transitions đầy đủ, IDOR qua query param, data exposure check, business states (pending/confirmed/canceled/delivered) trong list. Nhược điểm: 11/38 TC INCOMPLETE chủ yếu do các TC pagination (DP-08 đến DP-13) có expected conditional vì API spec không đề cập rõ pagination – AI suy luận có pagination nhưng không chắc chắn. Ngoài ra, TC-B-SEC-03 test endpoint khác (/api/admin/orders) không phải endpoint đang test. TC-B-SEC-06 SQL injection expected chưa rõ về behavior thực tế.

### 3.3. Bước 3: Bổ sung (Extend)

**Phân tích điểm yếu:** AI bỏ sót cross-user data isolation test, JWT alg:none attack, ordering/sorting, nested schema validation, Basic auth scheme, rate limiting cho GET, và state coverage đồng thời.

| TC ID | Mô tả | Lý do AI bỏ sót |
|:---|:---|:---|
| TC-B-EXT-01 | User A gọi my-orders – xác nhận KHÔNG thấy đơn của User B (data isolation) | AI test IDOR qua query param nhưng không test cross-user DB query isolation trực tiếp |
| TC-B-EXT-02 | JWT Algorithm Confusion: gửi token với header `alg: none` | AI test token forged/expired nhưng không test alg:none attack – model limitation về JWT vulnerabilities |
| TC-B-EXT-03 | Thứ tự sắp xếp đơn hàng – đơn mới nhất phải ở đầu | AI không kiểm tra ordering; prompt không đề cập expected ordering behavior |
| TC-B-EXT-04 | Response field `shipping_address` là nested object – kiểm tra schema con | AI chỉ check shipping_address không null, không kiểm tra schema con. Prompt chỉ yêu cầu top-level fields |
| TC-B-EXT-05 | `Authorization: Basic <base64>` thay vì Bearer token | AI chỉ test Bearer format variants, không test wrong auth scheme |
| TC-B-EXT-06 | 50 request liên tiếp GET my-orders – kiểm tra rate limiting | AI không đề cập rate limit cho GET endpoints; prompt không yêu cầu |
| TC-B-EXT-07 | Response chứa đơn hàng ở tất cả 5 trạng thái enum cùng lúc | AI test từng trạng thái riêng lẻ nhưng không test full-coverage trong 1 response |

### 3.4. Bước 4: Thực thi (Execute)

- **Công cụ:** Newman 6.2.2 + newman-reporter-html
- **Collection:** `postman/hw06_api2_collection.json`
- **Report HTML:** `newman_reports/newman_api2_report.html`
- **Header bắt buộc:** `X-Student-Id: 23127486`

| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| PASS | **34** | 91.9% |
| FAIL | **3** | 8.1% |
| **Tổng assertions** | **37** | 100% |
| **Tổng requests** | **23** | - |

> Newman HTML report: `newman_reports/newman_api2_report.html`

### 3.5. Bước 5: Báo cáo Bug

*(Chi tiết xem `bug_report.md`)*

| Bug ID | Mô tả | Severity | Link Issue |
|:---|:---|:---|:---|
| BUG-B-01 | Server chấp nhận token ngẫu nhiên (không phải JWT) | Critical | *(sinh viên tạo)* |
| BUG-B-02 | JWT forged signature không bị verify | Critical | *(sinh viên tạo)* |
| BUG-B-03 | Basic auth scheme được chấp nhận thay vì reject | High | *(sinh viên tạo)* |

---

## 4. API 3 – Pool C: Import sản phẩm (Admin) (FR-16)

> **Endpoint:** `POST /api/admin/import-products`  
> **Feature:** FR-16 – Import sản phẩm từ JSON (Admin)

### 4.1. Bước 1: Sinh test cases bằng AI (Generate)

**Prompt 1 – Domain Testing (EP & BVA):**
```
Dựa trên API spec của endpoint POST /api/admin/import-products, hãy áp dụng kỹ thuật
Domain Testing (Equivalence Partitioning & Boundary Value Analysis) theo các quy tắc sau:

1. Phân tích biến: Liệt kê tất cả tham số trong mảng products[] (name, price, description,
   imageUrl, category_id) và tham số mảng products tổng thể (size = 0/1/nhiều/rất nhiều).
2. Nguyên tắc:
   * Valid Cases: Kết hợp các trường hợp lệ, bao gồm nullable field (imageUrl = "").
   * Invalid Cases (cô lập lỗi): Mỗi TC chỉ sai 1 trường (thiếu name, price=âm, category_id không tồn, ...).
   * BVA: price=0, price=-1, array rỗng, array 100 items.

Xuất kết quả theo định dạng bảng:
| TC ID | Mô tả | Tham số kiểm tra | Phân vùng / Điểm biên | Input Payload | Expected HTTP Status & Output |

API Spec:
- Endpoint: POST /api/admin/import-products
- Header bắt buộc: Authorization: Bearer <admin_token>
- Body: {"products": [{"name":"...","price":10000,"description":"...","imageUrl":"","category_id":1}]}
- Response: 200 OK khi thành công
- Chỉ admin mới được gọi
```

*Output AI 1 (tóm tắt):*
AI sinh ra 15 test cases Domain EP & BVA: 2 valid (1 item/batch), 1 empty array BVA, 5 invalid cô lập
(name rỗng/missing, price missing), 4 BVA price (0/âm/string), 3 FK/type issues và nullable imageUrl.

**Prompt 2 – State Transition & Lifecycle:**
```
Dựa trên API spec của POST /api/admin/import-products, hãy áp dụng kỹ thuật State Transition Testing:

1. Xác định mô hình trạng thái:
   - Auth State: Unauthenticated / Authenticated (non-admin) / Authenticated (admin) / Token Expired
   - Resource Lifecycle (sản phẩm): Non-existent → Created (Active)
2. Kịch bản:
   * Gọi API khi ở từng auth state khác nhau
   * State sequence: Import → kiểm tra sản phẩm xuất hiện trong GET /api/products
   * Idempotency: import cùng payload 2 lần
   * Partial failure: 1 item hợp lệ + 1 item lỗi

Xuất kết quả:
| TC ID | Mô tả kịch bản | Trạng thái ban đầu | Hành động | Trạng thái kỳ vọng | Expected HTTP Status |

API Spec: POST /api/admin/import-products – admin only, tạo sản phẩm hàng loạt.
```

*Output AI 2 (tóm tắt):*
AI sinh ra 8 test cases State Transition: 4 auth state (Unauthenticated/non-admin/admin/expired),
2 lifecycle (Non-existent → Created, state sequence), 1 idempotency, 1 partial failure.

**Prompt 3 – Security Tests (SEC-01 – SEC-07):**
```
Đối với endpoint POST /api/admin/import-products, hãy sinh test cases bảo mật cho từng loại:
Missing Auth (401), Role Escalation – user thường gọi admin endpoint (403),
IDOR – cố gán admin_id trong body, SQL Injection vào name/description,
Token Forgery, Expired Token, XSS payload trong các trường văn bản.

Với mỗi loại:
[TC ID | Mô tả | Loại tấn công | Input | Expected Response]
```

*Output AI 3 (tóm tắt):*
AI sinh ra 8 test cases security: Missing Auth, Role Escalation, IDOR (admin_id body),
2 SQL Injection (name/description), Token Forgery, Expired Token, XSS (name field).

**Prompt 4 – Schema Validation:**
```
Dựa vào response của POST /api/admin/import-products trong API spec, hãy sinh test cases
Schema Validation để kiểm tra:
- Response thành công là JSON object (không phải null)
- Có field thông báo kết quả (message hoặc imported count)
- HTTP Status đúng 200 OK
- Content-Type: application/json
- Response lỗi 401/403/400 có cấu trúc JSON nhất quán (không trả HTML)
- Response 400 có thông tin lỗi chi tiết

Bảng: [TC ID | Mô tả | Field kiểm tra | Expected schema]
```

*Output AI 4 (tóm tắt):*
AI sinh ra 7 test cases Schema Validation: response shape, result field, HTTP 200,
Content-Type, error 401/403/400 structure và error detail.

**Số test cases AI sinh ra:** 38 (DP/BVA: 15 | ST: 8 | SEC: 8 | SV: 7)

### 4.2. Bước 2: Kiểm tra (Audit)

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




| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| VALID | 21 | 55.3% |
| INVALID | 0 | 0% |
| INCOMPLETE | 17 | 44.7% |
| **Tổng** | **38** | **100%** |

**Nhận xét tổng quan về chất lượng output AI:**
API 3 có tỷ lệ INCOMPLETE cao nhất (44.7%) trong 3 API. Nguyên nhân: (1) Nhiều TC có expected output với hai khả năng không xác định ("400 hoặc 200 tuỳ rule", "rollback hoặc partial") vì spec import-products không chi tiết về transaction behavior và business rules (price=0, empty array, max batch size); (2) Một số SEC TC có expected mơ hồ (SQL injection và XSS không chốt rõ outcome); (3) TC-C-SEC-03 IDOR concept không chính xác cho write endpoint. AI thiếu context về DB transaction design và spec chi tiết của import endpoint, dẫn đến expected output không cụ thể.

### 4.3. Bước 3: Bổ sung (Extend)

**Phân tích điểm yếu:** AI bỏ sót duplicate name trong batch, mass assignment với auto-generated fields, integer overflow price, DoS payload, Unicode/emoji product name, concurrent import, và HTML injection trong description.

| TC ID | Mô tả | Lý do AI bỏ sót |
|:---|:---|:---|
| TC-C-EXT-01 | Import batch có sản phẩm duplicate name trong cùng mảng | AI test FK constraint nhưng không test intra-batch duplicate; prompt không yêu cầu |
| TC-C-EXT-02 | Mass Assignment: cố gán `id`, `created_at` trong product object | AI test admin_id IDOR nhưng không test auto-generated fields – không biết schema DB đầy đủ |
| TC-C-EXT-03 | `price` rất lớn (999999999999) – kiểm tra integer overflow / DB precision | AI test BVA phía dưới (0, -1) nhưng không test BVA cực trên; prompt chỉ yêu cầu 2-point BVA |
| TC-C-EXT-04 | Payload cực lớn: array 1000+ sản phẩm hoặc body > 10MB (DoS test) | AI test 100 items nhưng không test DoS-level payload; prompt không đề cập threat modeling |
| TC-C-EXT-05 | Import sản phẩm với name chứa emoji và Unicode đặc biệt (🛒, 商品) | AI không test i18n cho product; prompt không đề cập internationalization |
| TC-C-EXT-06 | Import đồng thời bởi 2 admin sessions với cùng product data | AI không test concurrency; prompt tập trung single-request scenarios |
| TC-C-EXT-07 | `description` chứa HTML injection (`<b>Sale!</b>`) – Stored XSS variant | AI test XSS với script tag trong name nhưng không test HTML injection trong description |

### 4.4. Bước 4: Thực thi (Execute)

- **Công cụ:** Newman 6.2.2 + newman-reporter-html
- **Collection:** `postman/hw06_api3_collection.json`
- **Report HTML:** `newman_reports/newman_api3_report.html`
- **Header bắt buộc:** `X-Student-Id: 23127486`

| Nhãn | Số lượng | Tỷ lệ |
|:---|:---|:---|
| PASS | **36** | 78.3% |
| FAIL | **10** | 21.7% |
| **Tổng assertions** | **46** | 100% |
| **Tổng requests** | **31** | - |

> Newman HTML report: `newman_reports/newman_api3_report.html`

### 4.5. Bước 5: Báo cáo Bug

*(Chi tiết xem `bug_report.md`)*

| Bug ID | Mô tả | Severity | Link Issue |
|:---|:---|:---|:---|
| BUG-C-01 | Không validate required fields (name/price/category_id) | Critical | *(sinh viên tạo)* |
| BUG-C-02 | Chấp nhận giá âm và string type cho price | High | *(sinh viên tạo)* |
| BUG-C-03 | Không kiểm tra FK constraint category_id | High | *(sinh viên tạo)* |
| BUG-C-04 | RBAC không enforce – user thường import được products | Critical | *(sinh viên tạo)* |
| BUG-C-05 | Forged JWT không bị detect cho admin endpoint | Critical | *(sinh viên tạo)* |

---

## 5. Các tính năng Postman đã sử dụng

| Tính năng | Mô tả sử dụng |
|:---|:---|
| **Workspaces** | Tạo workspace chuyên biệt `HW06 – EShop API Testing` để quản lý các collections và môi trường của bài tập. |
| **Collections** | Tổ chức 3 collections riêng biệt theo từng API: `HW06 – API 1 (POST /api/register)`, `HW06 – API 2 (GET /api/orders/my-orders)`, `HW06 – API 3 (POST /api/admin/import-products)`. |
| **Variables** | Sử dụng biến đa tầng (Collection/Environment variables): `baseUrl`, `studentId`, `token`, `adminToken` để tái sử dụng linh hoạt giữa các requests. |
| **Environments** | Thiết lập môi trường `HW06-Local` (`postman/hw06_environment.json`) với target `http://localhost:3000` và cấu hình token động. |
| **Pre-request Scripts** | Tự động tạo timestamp `Date.now()` cho unique email và cấu hình header sinh viên `X-Student-Id` trước khi gửi request. |
| **Test Scripts** | Viết các Chai Assertion (`pm.test`, `pm.expect`) kiểm tra HTTP status code, JSON response schema, kiểm tra kiểu dữ liệu, xác thực quyền truy cập và phát hiện lộ lọt dữ liệu nhạy cảm. |
| **Collection Runner / Newman** | Tự động hóa thực thi toàn bộ test suite thông qua Newman CLI (`npx newman run`) và xuất báo cáo trực quan với `newman-reporter-htmlextra`. |

---

## 6. Tích hợp CI/CD

*(Tóm tắt ngắn – chi tiết trong `cicd_report.md`)*

- **Pipeline:** GitHub Actions
- **Run 1 (all PASS):** *(link)*
- **Run 2 (có test FAIL):** *(link)*

---

## 7. Agent Skill – AI-driven Test Generator

*(Tóm tắt – chi tiết trong `agent_skill.md`)*

---

## 8. Phụ lục

- **Phụ lục A – AI Audit Report:** xem `AI_Audit.md`
- **Phụ lục B – AI Critique:** xem `AI_Critique.md`
- **Phụ lục C – Bug Report:** xem `bug_report.md`
- **Phụ lục D – CI/CD Report:** xem `cicd_report.md`
- **Phụ lục E – Git Commit Log:** xem `git_commit_log.txt`
