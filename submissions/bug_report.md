# Báo cáo Bug – HW06 API Testing

**Sinh viên:** Phan Quốc Thịnh – 23127486 – 23KTPM3  
**GitHub Issues:** *(link đến trang Issues của repo)*

---

## Tổng quan

| Mục | Giá trị |
|:---|:---|
| **Tổng số bug** | 19 |
| **API 1 bugs** | 10 |
| **API 2 bugs** | 3 |
| **API 3 bugs** | 6 |

---

## Danh sách Bug

### API 1 – Pool A: POST /api/register – Đăng ký tài khoản

| Bug ID | Tiêu đề | Mô tả | Steps to Reproduce | Expected | Actual | Severity | Link Issue | Screenshot |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| BUG-A-01 | Không validate input bắt buộc (name, email, password) | Server chấp nhận đăng ký với name/email/password rỗng hoặc thiếu | POST /api/register với body `{"name":"","email":"","password":""}` | 400 Bad Request | 200 OK – user được tạo | **Critical** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-02 | Không validate định dạng email | Server chấp nhận email không hợp lệ (thiếu @, thiếu domain) | POST với email=`invalidemail.com` | 400 Bad Request | 200 OK | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-03 | Không enforce password minimum length | Server chấp nhận password 1 ký tự và 7 ký tự | POST với `"password":"A"` | 400 Bad Request (min 8 ký tự) | 200 OK | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-04 | Không enforce giới hạn độ dài name (max 255) | Server chấp nhận name dài 256 ký tự vượt max | POST với `name` dài 256 ký tự | 400 Bad Request | 200 OK | **Medium** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-05 | Cho phép đăng ký email trùng (duplicate) | Server tạo user mới dù email đã tồn tại | Register cùng email 2 lần | 400/409 Conflict | 200 OK – user duplicate được tạo | **Critical** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-06 | Server crash (500) khi nhận body text/plain hoặc thiếu Content-Type | Server văng ngoại lệ TypeError khi req.body không được parse JSON | POST /api/register với Content-Type: text/plain | 400 Bad Request hoặc 415 | **500 Internal Server Error** | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-07 | Không sanitize SQL Injection trong email | Server chấp nhận payload SQLi `' OR 1=1 --` làm email hợp lệ | POST với email=`' OR 1=1 --` | 400 Bad Request | 200 OK | **Critical** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-08 | Chấp nhận JSON null cho name/email/password | Server coi null như giá trị hợp lệ cho tất cả required fields | POST với `{"name":null,"email":null,"password":null}` | 400 Bad Request | 200 OK | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-09 | Không validate email XSS payload | Email chứa `<script>alert(1)</script>@test.com` được chấp nhận | POST với email=`<script>alert(1)</script>@test.com` | 400 Bad Request | 200 OK | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-10 | Không validate email @domain.com (thiếu local-part) | Email bắt đầu bằng @ được chấp nhận | POST với email=`@domain.com` | 400 Bad Request | 200 OK | **Medium** | *(sinh viên tạo)* | *(sinh viên chụp)* |

### API 2 – Pool B: GET /api/orders/my-orders – Xem lịch sử đơn hàng

| Bug ID | Tiêu đề | Mô tả | Steps to Reproduce | Expected | Actual | Severity | Link Issue | Screenshot |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| BUG-B-01 | Trả mã lỗi 403 Forbidden thay vì 401 Unauthorized khi token invalid / forged / expired | Server xử lý sai chuẩn REST API: lỗi xác thực (Authentication) phải trả 401 | GET /api/orders/my-orders với token forged / expired | 401 Unauthorized | 403 Forbidden | **Medium** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-B-02 | Chấp nhận token không có chữ ký (alg: none) | Unsigned JWT token với header alg: none không bị reject đúng chuẩn 401 | GET với unsigned token | 401 Unauthorized | 403 Forbidden | **Medium** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-B-03 | Xử lý sai mã lỗi khi dùng Basic auth scheme | Server trả 403 thay vì 401 khi client gửi Basic auth thay vì Bearer | GET với `Authorization: Basic ...` | 401 Unauthorized | 403 Forbidden | **Low** | *(sinh viên tạo)* | *(sinh viên chụp)* |

### API 3 – Pool C: POST /api/admin/import-products – Import sản phẩm

| Bug ID | Tiêu đề | Mô tả | Steps to Reproduce | Expected | Actual | Severity | Link Issue | Screenshot |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| BUG-C-01 | Không validate required fields trong product | Import sản phẩm thiếu name/price/category_id hoặc rỗng vẫn thành công | POST với products thiếu name, hoặc price, hoặc category_id | 400 Bad Request | 200 OK – product được tạo với null fields | **Critical** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-C-02 | Chấp nhận giá âm và kiểu dữ liệu sai cho price | price=-1 và price="10000" (string) được chấp nhận | POST với `"price":-1` hoặc `"price":"10000"` | 400 Bad Request | 200 OK | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-C-03 | Không kiểm tra FK constraint category_id | category_id=9999 (không tồn tại) được import thành công | POST với `"category_id":9999` | 400 Bad Request (FK violation) | 200 OK | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-C-04 | RBAC không được áp dụng cho import endpoint | User thường (role=user) được phép import products như admin | POST /api/admin/import-products với token của user thường | 403 Forbidden | 200 OK – products được import | **Critical** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-C-05 | Xử lý sai mã lỗi (403 vs 401) khi admin token forged / expired | Server trả 403 thay vì 401 khi token admin không hợp lệ | POST với forged / expired token | 401 Unauthorized | 403 Forbidden | **Medium** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-C-06 | Chấp nhận mảng products chứa phần tử không phải object | Mảng chứa số hoặc chuỗi `products: [123, "invalid"]` được import | POST với `{"products": [123, "invalid"]}` | 400 Bad Request | 200 OK | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |

---

## Tóm tắt phân loại bug

| Loại bug | Số lượng |
|:---|:---|
| Security – RBAC / Access Control Bypass | 1 (BUG-C-04) |
| Security – SQL Injection | 1 (BUG-A-07) |
| Input Validation – Required fields | 4 (BUG-A-01, BUG-A-03, BUG-A-04, BUG-C-01) |
| Input Validation – Type / Format / Null | 6 (BUG-A-02, BUG-A-08, BUG-A-09, BUG-A-10, BUG-C-02, BUG-C-06) |
| Business Logic – Duplicate constraint | 1 (BUG-A-05) |
| Database Referential Integrity (FK constraint) | 1 (BUG-C-03) |
| HTTP Status Code Compliance (403 vs 401) | 3 (BUG-B-01, BUG-B-02, BUG-C-05) |
| Server Stability & Error Handling (500 crash) | 2 (BUG-A-06, BUG-B-03) |
| **Tổng unique bugs** | **19** |

---

> **Lưu ý:** Link GitHub Issue và screenshot phải do sinh viên tự tạo và đính kèm. AI đã xác nhận các bug bằng Newman execution thực tế trên server đang chạy tại `http://localhost:3000`.
