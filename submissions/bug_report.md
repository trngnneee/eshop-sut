# Báo cáo Bug – HW06 API Testing

**Sinh viên:** Phan Quốc Thịnh – 23127486 – 23KTPM3  
**GitHub Issues:** *(link đến trang Issues của repo)*

---

## Tổng quan

| Mục | Giá trị |
|:---|:---|
| **Tổng số bug** | 17 |
| **API 1 bugs** | 9 |
| **API 2 bugs** | 3 |
| **API 3 bugs** | 5 |

---

## Danh sách Bug

### API 1 – Pool A: POST /api/register – Đăng ký tài khoản

| Bug ID | Tiêu đề | Mô tả | Steps to Reproduce | Expected | Actual | Severity | Link Issue | Screenshot |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| BUG-A-01 | Không validate input bắt buộc (name, email, password) | Server chấp nhận đăng ký với name/email/password rỗng hoặc thiếu | POST /api/register với body `{"name":"","email":"","password":""}` | 400 Bad Request | 200 OK – user được tạo | **Critical** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-02 | Không validate định dạng email | Server chấp nhận email không hợp lệ (thiếu @, thiếu domain, chỉ có @domain.com) | POST với email=`invalidemail.com` | 400 Bad Request | 200 OK | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-03 | Không enforce password minimum length | Server chấp nhận password 1 ký tự và 7 ký tự | POST với `"password":"A"` | 400 Bad Request (min 8 ký tự) | 200 OK | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-04 | Cho phép đăng ký email trùng (duplicate) | Server tạo user mới dù email đã tồn tại | Register cùng email 2 lần | 400/409 Conflict | 200 OK – user duplicate được tạo | **Critical** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-05 | Server crash (500) khi nhận body text/plain | Khi gửi body không phải JSON, server trả 500 thay vì 400/415 | POST /api/register với Content-Type: text/plain | 400 Bad Request hoặc 415 | **500 Internal Server Error** | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-06 | Không sanitize SQL Injection trong email | Server chấp nhận payload SQLi `' OR 1=1 --` làm email hợp lệ | POST với email=`' OR 1=1 --` | 400 Bad Request | 200 OK | **Critical** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-07 | Chấp nhận JSON null cho name/email/password | Server coi null như giá trị hợp lệ cho tất cả required fields | POST với `{"name":null,"email":null,"password":null}` | 400 Bad Request | 200 OK | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-08 | Không validate email XSS payload | Email chứa `<script>alert(1)</script>@test.com` được chấp nhận | POST với email=`<script>alert(1)</script>@test.com` | 400 Bad Request | 200 OK | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-A-09 | Không validate email @domain.com (thiếu local-part) | Email bắt đầu bằng @ được chấp nhận | POST với email=`@domain.com` | 400 Bad Request | 200 OK | **Medium** | *(sinh viên tạo)* | *(sinh viên chụp)* |

### API 2 – Pool B: GET /api/orders/my-orders – Xem lịch sử đơn hàng

| Bug ID | Tiêu đề | Mô tả | Steps to Reproduce | Expected | Actual | Severity | Link Issue | Screenshot |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| BUG-B-01 | Chấp nhận token ngẫu nhiên (không phải JWT) | Server không kiểm tra cấu trúc JWT, chấp nhận chuỗi ngẫu nhiên | GET /api/orders/my-orders với header `Authorization: Bearer invalidfaketoken123xyz` | 401 Unauthorized | 200 OK | **Critical** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-B-02 | Không verify chữ ký JWT | JWT forged (signature sai) được chấp nhận | GET với forged JWT (valid header.payload + invalid signature) | 401 Unauthorized | 200 OK | **Critical** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-B-03 | Chấp nhận Basic auth scheme | Server không giới hạn scheme auth, chấp nhận Basic thay vì chỉ Bearer | GET với `Authorization: Basic dGVzdHVzZXI6cGFzc3dvcmQ=` | 401 Unauthorized | 200 OK | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |

### API 3 – Pool C: POST /api/admin/import-products – Import sản phẩm

| Bug ID | Tiêu đề | Mô tả | Steps to Reproduce | Expected | Actual | Severity | Link Issue | Screenshot |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| BUG-C-01 | Không validate required fields trong product | Import sản phẩm thiếu name/price/category_id vẫn thành công | POST với products thiếu name, hoặc price, hoặc category_id | 400 Bad Request | 200 OK – product được tạo với null fields | **Critical** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-C-02 | Chấp nhận giá âm và kiểu dữ liệu sai cho price | price=-1 và price="10000" (string) được chấp nhận | POST với `"price":-1` hoặc `"price":"10000"` | 400 Bad Request | 200 OK | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-C-03 | Không kiểm tra FK constraint category_id | category_id=9999 (không tồn tại) được import thành công | POST với `"category_id":9999` | 400 Bad Request (FK violation) | 200 OK | **High** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-C-04 | RBAC không được enforce cho import endpoint | User thường (role=user) được phép import products | POST /api/admin/import-products với token của user thường | 403 Forbidden | 200 OK – products được import | **Critical** | *(sinh viên tạo)* | *(sinh viên chụp)* |
| BUG-C-05 | JWT forgery không bị phát hiện | Forged JWT được chấp nhận cho admin endpoint | POST với forged JWT mang role=admin | 401 Unauthorized | 200 OK | **Critical** | *(sinh viên tạo)* | *(sinh viên chụp)* |

---

## Tóm tắt phân loại bug

| Loại bug | Số lượng |
|:---|:---|
| Security – JWT/Auth bypass | 5 (BUG-A-06, BUG-B-01, BUG-B-02, BUG-B-03, BUG-C-05) |
| Security – RBAC / Access Control | 2 (BUG-C-04, BUG-C-05 overlap) |
| Input Validation – Required fields | 4 (BUG-A-01, BUG-A-03, BUG-A-04, BUG-C-01) |
| Input Validation – Type/Format | 4 (BUG-A-02, BUG-A-07, BUG-A-08, BUG-C-02) |
| Business Logic | 1 (BUG-A-04 – duplicate email) |
| FK Constraint / Referential Integrity | 1 (BUG-C-03) |
| Server Error (500) | 1 (BUG-A-05) |
| **Tổng unique bugs** | **17** |

---

> **Lưu ý:** Link GitHub Issue và screenshot phải do sinh viên tự tạo và đính kèm. AI đã xác nhận các bug bằng Newman execution thực tế trên server đang chạy tại `http://localhost:3000`.


**Sinh viên:** Phan Quốc Thịnh – 23127486 – 23KTPM3  
**GitHub Issues:** *(link đến trang Issues của repo)*


