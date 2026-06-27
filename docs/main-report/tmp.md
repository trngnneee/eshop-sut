Dưới đây là bản **chuẩn hóa FR-05 và FR-11 theo cùng một style QA report thống nhất (format nộp bài, clean, giống nhau 100%)**.

Mình đã chuẩn hóa theo các tiêu chí:

* Cùng structure (Overview → Domain → BVA → Steps → Test cases → Coverage)
* Cùng cách viết bullet + table
* Cùng level chi tiết
* Cùng style “QA report chuẩn môn Software Testing”

---

# ✅ FR-05 & FR-11 – QA Report Chuẩn Hóa

---

# 📌 FR-05: Xem danh sách & Tìm kiếm sản phẩm

## 1. Tổng quan yêu cầu

Hệ thống hiển thị danh sách sản phẩm dạng grid và cho phép tìm kiếm theo tên sản phẩm.

Yêu cầu chính:

* Hiển thị danh sách sản phẩm đầy đủ thông tin (ảnh, tên, giá).
* Giá hiển thị đúng định dạng tiền tệ Việt Nam (₫).
* Có trạng thái loading và empty state.
* Trang chỉ được có đúng 1 thẻ h1.
* Dữ liệu hiển thị phải an toàn (không XSS).
* Input tìm kiếm phải được xử lý an toàn.

---

## 2. Domain Testing

### Input cần kiểm thử

* Từ khóa tìm kiếm
* Danh sách sản phẩm
* Số lượng h1
* Alt text ảnh
* Giá sản phẩm
* Trạng thái UI

### Miền giá trị

| Biến           | Domain   | Giá trị                         |
| -------------- | -------- | ------------------------------- |
| Search keyword | String   | hợp lệ / HTML / JS / chuỗi rỗng |
| Product list   | Integer  | 0, >0                           |
| h1 count       | Integer  | 0, 1, >1                        |
| alt text       | String   | hợp lệ / rỗng                   |
| price          | Currency | đúng định dạng ₫                |
| UI state       | Enum     | loading / empty / data          |

### Dữ liệu hợp lệ

* Keyword hợp lệ
* Có 1 h1
* Alt text mô tả đúng
* Giá hiển thị đúng ₫
* UI state hợp lệ

### Dữ liệu không hợp lệ

* Input chứa HTML/JS
* 0 hoặc >1 h1
* Alt text rỗng
* Sai định dạng giá

---

## 3. Boundary Value Analysis

| Variable      | Boundary | Ý nghĩa         |
| ------------- | -------- | --------------- |
| Product count | 0        | empty state     |
| Product count | 1        | min valid data  |
| h1 count      | 0        | thiếu heading   |
| h1 count      | 1        | hợp lệ          |
| h1 count      | 2        | duplicate error |

---

## 4. Test Cases

| ID             | Mục tiêu                    | Technique |
| -------------- | --------------------------- | --------- |
| TC-PRODUCT-001 | Hiển thị danh sách sản phẩm | Domain    |
| TC-PRODUCT-002 | Hiển thị tên sản phẩm       | Domain    |
| TC-PRODUCT-003 | Hiển thị giá ₫ đúng format  | Domain    |
| TC-PRODUCT-004 | Hiển thị ảnh + alt text     | Domain    |
| TC-PRODUCT-005 | Loading state               | Domain    |
| TC-PRODUCT-006 | Empty state (0 sản phẩm)    | BVA       |
| TC-PRODUCT-007 | Search hợp lệ               | Domain    |
| TC-PRODUCT-008 | Chống XSS input             | Domain    |
| TC-PRODUCT-009 | h1 = 1                      | BVA       |
| TC-PRODUCT-010 | Search page h1 = 1          | BVA       |
| TC-PRODUCT-011 | Render list đúng            | Domain    |
| TC-PRODUCT-012 | Image ratio đúng            | Domain    |
| TC-PRODUCT-013 | XSS nâng cao                | Domain    |
| TC-PRODUCT-014 | SQL Injection               | Domain    |

---

## 5. Coverage

* Domain: Search, UI state, security, product data
* Boundary: 0, 1, >1 (product & h1)
* Negative: XSS, SQL Injection, empty data

---

---

# 📌 FR-11: Xem lịch sử đơn hàng (User)

## 1. Tổng quan yêu cầu

Người dùng đã đăng nhập có thể xem lịch sử đơn hàng của chính mình.

Yêu cầu:

* Chỉ xem được đơn hàng của chính mình
* Không xem được đơn hàng người khác
* Không truy cập khi chưa đăng nhập
* Có phân trang khi dữ liệu lớn
* Hiển thị trạng thái đơn hàng bằng tiếng Việt + màu sắc

---

## 2. Domain Testing

### Input cần kiểm thử

* Authentication status
* Authorization (owner check)
* Order list
* Token
* Order ID
* Order status

### Miền giá trị

| Biến         | Domain       | Giá trị                                               |
| ------------ | ------------ | ----------------------------------------------------- |
| Login status | Boolean      | true / false                                          |
| Token        | String       | valid / missing                                       |
| Order count  | Integer      | 0, >0                                                 |
| Ownership    | Object match | match / not match                                     |
| Order status | Enum         | pending / confirmed / shipping / delivered / canceled |
| Order ID     | Integer      | valid / invalid                                       |

### Dữ liệu hợp lệ

* User login
* Token valid
* Order thuộc user
* Status hợp lệ

### Dữ liệu không hợp lệ

* No token
* Access order của user khác
* Invalid Order ID
* Chưa đăng nhập

---

## 3. Boundary Value Analysis

| Variable    | Boundary | Ý nghĩa               |
| ----------- | -------- | --------------------- |
| Order count | 0        | empty history         |
| Order count | 1        | first order           |
| Order count | >1       | list lớn / pagination |

---

## 4. Test Cases

| ID                  | Mục tiêu                       | Technique |
| ------------------- | ------------------------------ | --------- |
| TC-ORDERHISTORY-001 | Chưa đăng nhập không xem được  | Domain    |
| TC-ORDERHISTORY-002 | 0 đơn hàng                     | BVA       |
| TC-ORDERHISTORY-003 | 1 đơn hàng                     | BVA       |
| TC-ORDERHISTORY-004 | Không xem đơn người khác       | Domain    |
| TC-ORDERHISTORY-005 | Hiển thị order info            | Domain    |
| TC-ORDERHISTORY-006 | Status pending                 | Domain    |
| TC-ORDERHISTORY-007 | Status confirmed               | Domain    |
| TC-ORDERHISTORY-008 | Status shipping                | Domain    |
| TC-ORDERHISTORY-009 | Status delivered               | Domain    |
| TC-ORDERHISTORY-010 | Status canceled                | Domain    |
| TC-ORDERHISTORY-011 | Pagination                     | BVA       |
| TC-ORDERHISTORY-012 | No token → 401                 | Domain    |
| TC-ORDERHISTORY-013 | Only own orders                | Domain    |
| TC-ORDERHISTORY-014 | No login access detail blocked | Domain    |

---

## 5. Coverage

* Domain: Authentication, Authorization, Order status
* Boundary: 0, 1, many orders
* Negative: Unauthorized access, cross-user access, missing token

---

# 🎯 KẾT LUẬN (Quan trọng khi nộp bài)

Sau khi chuẩn hóa:

✔ FR-05 và FR-11 đồng nhất structure
✔ Có Domain + BVA rõ ràng
✔ Có negative testing (security)
✔ Có coverage summary
✔ Format giống report QA thực tế

---

Nếu bạn muốn, mình có thể nâng thêm 1 level nữa thành:

👉 **“Report chuẩn A+ có traceability matrix + risk analysis + severity mapping”**
(kiểu báo cáo công ty QA thật luôn)
