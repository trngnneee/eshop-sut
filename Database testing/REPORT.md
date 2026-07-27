# BÁO CÁO KIỂM THỬ – MINI LAB DATABASE TESTING & TEST DATA GENERATION FOR E-COMMERCE

---

## 1. THÔNG TIN CHUNG

- **Tên bài lab**: Mini Lab Database Testing & Test Data Generation for E-Commerce
- **Họ và tên / MSSV**: 23127207
- **Công nghệ sử dụng**:
  - Backend SUT: Node.js, Express.js
  - Database: SQLite (in-memory `:memory:`)
  - Test Framework: Jest, Supertest
  - Test Data Generation: `@faker-js/faker` combined with deterministic seeding
- **Ngày chạy test**: 2026-07-27
- **Lệnh chạy test**: 
  ```bash
  cd "Database testing"
  npm install
  npm test
  ```
  *(Hoặc: `node node_modules/jest/bin/jest.js --runInBand --verbose`)*

---

## 2. MÔ TẢ MÔI TRƯỜNG KIỂM THỬ

- **Hệ điều hành**: Windows 11 / Windows Server
- **Node.js runtime**: v24.10.0
- **Dependencies**:
  - `express`: `^4.19.2`
  - `sqlite3`: `^5.1.7`
  - `jest`: `^29.7.0`
  - `supertest`: `^7.0.0`
  - `@faker-js/faker`: `^8.4.1`
- **Cấu hình Jest**: `testEnvironment: "node"`, chạy `--runInBand` (đơn luồng) để bảo đảm tuần tự hóa việc tương tác với database in-memory và không gây tranh chấp tài nguyên.

---

## 3. PHẠM VI KIỂM THỬ

1. **Database Integrity Testing**:
   - Kiểm tra Ràng buộc Khóa ngoại (Referential Integrity / Foreign Key Constraints & Cascade Delete).
   - Kiểm tra Ràng buộc Duy nhất (Unique Constraint) trên mã Coupon.
   - Kiểm tra Tính nhất quán kiểu dữ liệu (Data Type Consistency) đối với trường `price` của sản phẩm.

2. **Integration Testing – Apply Coupon (`POST /api/apply-coupon`)**:
   - Áp dụng coupon phần trăm hợp lệ (`CP_PERCENT`).
   - Kiểm tra đơn hàng chưa đạt giá trị tối thiểu (`min_order_amount`).
   - Kiểm tra mã giảm giá đã hết hạn (`expired_at`).
   - Kiểm tra mã giảm giá đã đạt giới hạn sử dụng của người dùng (`max_uses_per_user`).
   - Kiểm tra mã giảm giá đang ở trạng thái không hoạt động (`is_active = 0`).
   - Áp dụng coupon số tiền cố định hợp lệ (`CP_FIXED`).

3. **Integration Testing – Order State Machine (`PUT /api/admin/orders/:id/status`)**:
   - Chuyển trạng thái theo chuỗi hợp lệ: `pending` → `confirmed` → `shipping` → `delivered`.
   - Chuyển trạng thái không hợp lệ từ trạng thái kết thúc: `canceled` → `delivered`.

---

## 4. THIẾT KẾ DỮ LIỆU KIỂM THỬ (TEST DATA DESIGN)

### 4.1. Chiến lược sinh dữ liệu (Data Generation Strategy)
- **Tái lập dữ liệu (Reproducibility)**: Gọi `faker.seed(23127207)` ở **đầu mỗi lần thực thi hàm `setupTestDB(db)`**. Điều này bảo đảm mọi lượt chạy test (dù chạy toàn bộ hay chạy đơn lẻ từng test case) đều có dữ liệu ngẫu nhiên giống hệt nhau.
- **Phân tách trách nhiệm**:
  - **Faker**: Dùng để sinh các trường dữ liệu mô tả không tham gia vào logic kiểm tra trực tiếp (như tên sản phẩm ngẫu nhiên, tên người dùng phụ, email phụ, số lượng tồn kho `stock`).
  - **Dữ liệu cố định (Deterministic Data)**: Các ID (1 đến 5), mã coupon (`CP_EXPIRED`, `CP_INACTIVE`, `CP_PERCENT`, `CP_FIXED`, `CP_MAX_REACHED`), giá niêm yết (100, 200, 300, 400, 500) và số tiền đơn hàng được ghi cứng để phục vụ các assertion chính xác.
- **Ngày tháng tương đối (Dynamic Relative Timestamps)**: Tránh ghi cứng năm 2025/2030. Thời điểm hết hạn được tính bằng `Date.now() - 24*60*60*1000` (hết hạn) và `Date.now() + 365*24*60*60*1000` (còn hạn).

### 4.2. Dataset chuẩn được nạp vào Database

| Bảng | Dữ liệu chính | Mục đích kiểm thử |
| :--- | :--- | :--- |
| **users** | `id: 1, email: 'test@example.com', name: 'Test User'`<br>`id: 2, email: faker, name: faker` | Dùng làm người dùng thực hiện giao dịch và xóa kiểm tra referential integrity. |
| **products** | `ID 1: price 100`<br>`ID 2: price 200` (ID chẵn)<br>`ID 3: price 300`<br>`ID 4: price 400` (ID chẵn)<br>`ID 5: price 500` | Kiểm tra Data Type Consistency (`price` phải luôn là `number`). ID 2 và 4 để kích hoạt bug ép kiểu string. |
| **coupons** | - `CP_EXPIRED`: `fixed`, `10`, hết hạn<br>- `CP_INACTIVE`: `fixed`, `10`, `is_active=0`<br>- `CP_PERCENT`: `percent`, `0.10` (10%), min `100`, max uses `5`<br>- `CP_FIXED`: `fixed`, `15`, min `0`, max uses `5`<br>- `CP_MAX_REACHED`: `fixed`, `10`, max uses `1` | Phục vụ 6 kịch bản áp dụng mã giảm giá. |
| **coupon_usage** | `id: 1, coupon_id: 5 (CP_MAX_REACHED), user_id: 1` | Đánh dấu User 1 đã dùng 1/1 lượt coupon `CP_MAX_REACHED`; đồng thời dùng để test xóa User 1 (Referential Integrity). |
| **orders** | - `Order 1`: `user_id: 1, total: 500, status: 'pending'`<br>- `Order 2`: `user_id: 1, total: 200, status: 'canceled'` | Order 1 test luồng chuyển trạng thái chuẩn. Order 2 test luồng chuyển trạng thái sai từ `canceled`. |

---

## 5. DANH SÁCH TEST CASE VÀ KẾT QUẢ THỰC TẾ

| Test Case ID | Nhóm kiểm thử | Mục tiêu kiểm thử | Preconditions / Input | Expected Result (Theo nghiệp vụ chuẩn) | Actual Result (Từ Jest output thực tế) | Status | Related Bug |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **TC-DB-001** | Database Integrity | Kiểm tra Ràng buộc Khóa ngoại (Referential Integrity) khi xóa User có record con trong `coupon_usage`. | User 1 có record con trong `coupon_usage`. Thực hiện `DELETE FROM users WHERE id = 1`. | Bảng `coupon_usage` không còn record của `user_id = 1` (rows = 0) hoặc DB chặn việc xóa. | Record `coupon_usage` của `user_id = 1` vẫn tồn tại (`rows = 1`). Assertion `expect(1).toBe(0)` thất bại. | **FAIL** *(Intentional)* | `BUG-DB-001` |
| **TC-DB-002** | Database Integrity | Kiểm tra Unique Constraint khi thêm mã Coupon bị trùng (`CP_FIXED`). | Mã coupon `CP_FIXED` đã tồn tại trong DB. Thực hiện `INSERT INTO coupons` mã `CP_FIXED`. | DB quăng lỗi `SQLITE_CONSTRAINT`, không thêm record mới vào bảng (`countAfter === countBefore`). | Nhận lỗi `SQLITE_CONSTRAINT: UNIQUE constraint failed: coupons.code`, số lượng record không đổi. | **PASS** | N/A |
| **TC-DB-003** | Database Integrity | Kiểm tra Tính nhất quán kiểu dữ liệu (`price` phải luôn là `number`) của tất cả sản phẩm. | Gọi `GET /api/products/:id` cho các ID từ 1 đến 5. | Tất cả 5 sản phẩm đều trả về HTTP 200 và kiểu dữ liệu của `price` là `number`. | Product 2 và Product 4 trả về `priceType: 'string'`. Filter thu được 2 sản phẩm lỗi (`invalidProducts.length = 2`). | **FAIL** *(Intentional)* | `BUG-API-002` |
| **TC-COUPON-001** | Apply Coupon | Kiểm tra tính tiền khi áp dụng Coupon phần trăm (`CP_PERCENT` giảm 10%). | `user_id: 1, coupon_code: 'CP_PERCENT', total_amount: 200`. | HTTP 200, `discount_amount: 20`, `final_amount: 180`. | HTTP 200 nhưng `discount_amount: 180`, `final_amount: 20` (Công thức SUT tính nhầm discount = 200 * (1 - 0.10)). | **FAIL** *(Intentional)* | `BUG-API-003` |
| **TC-COUPON-002** | Apply Coupon | Kiểm tra từ chối khi tổng đơn nhỏ hơn `min_order_amount`. | `user_id: 1, coupon_code: 'CP_PERCENT', total_amount: 50` (min requirement: 100). | HTTP 400 và trả về thông báo lỗi. | Trả về HTTP 400 với message `{ error: 'Minimum order amount not reached' }`. | **PASS** | N/A |
| **TC-COUPON-003** | Apply Coupon | Kiểm tra từ chối khi Coupon đã hết hạn (`CP_EXPIRED`). | `user_id: 1, coupon_code: 'CP_EXPIRED', total_amount: 100`. | HTTP 400 và trả về thông báo lỗi coupon hết hạn. | Trả về HTTP 400 với message `{ error: 'Coupon has expired' }`. | **PASS** | N/A |
| **TC-COUPON-004** | Apply Coupon | Kiểm tra từ chối khi người dùng đã dùng hết lượt (`CP_MAX_REACHED`). | User 1 đã có 1 record trong `coupon_usage` với `CP_MAX_REACHED` (max = 1). | HTTP 400 và trả về thông báo lỗi hết lượt sử dụng. | Trả về HTTP 400 với message `{ error: 'Coupon usage limit reached' }`. | **PASS** | N/A |
| **TC-COUPON-005** | Apply Coupon | Kiểm tra từ chối khi Coupon không hoạt động (`CP_INACTIVE`). | `user_id: 1, coupon_code: 'CP_INACTIVE', total_amount: 100` (`is_active = 0`). | HTTP 400 và trả về thông báo lỗi coupon inactive. | Trả về HTTP 400 với message `{ error: 'Coupon is inactive' }`. | **PASS** | N/A |
| **TC-COUPON-006** | Apply Coupon | Kiểm tra tính tiền khi áp dụng Coupon số tiền cố định (`CP_FIXED` giảm 15). | `user_id: 1, coupon_code: 'CP_FIXED', total_amount: 100`. | HTTP 200, `discount_amount: 15`, `final_amount: 85`. | Trả về HTTP 200, `discount_amount: 15`, `final_amount: 85`. | **PASS** | N/A |
| **TC-ORDER-001** | Order State Machine | Kiểm tra chuỗi chuyển trạng thái đơn hàng hợp lệ (`pending` → `confirmed` → `shipping` → `delivered`). | Order 1 đang ở trạng thái `pending`. Thực hiện 3 API PUT liên tiếp. | HTTP 200 cho từng bước, DB cập nhật `status = 'delivered'`. | Cả 3 bước đều đạt HTTP 200. Truy vấn DB xác nhận status cuối cùng của Order 1 là `delivered`. | **PASS** | N/A |
| **TC-ORDER-002** | Order State Machine | Kiểm tra từ chối chuyển trạng thái không hợp lệ từ `canceled` sang `delivered`. | Order 2 đang ở trạng thái `canceled`. Thực hiện `PUT /api/admin/orders/2/status` với `{ status: 'delivered' }`. | HTTP 400 và trạng thái đơn hàng trong DB giữ nguyên là `canceled`. | API trả về HTTP 200 và DB bị cập nhật sai thành `status = 'delivered'`. | **FAIL** *(Intentional)* | `BUG-API-004` |

---

## 6. TỔNG HỢP KẾT QUẢ KIỂM THỬ

| Chỉ số | Expected Baseline | Actual Jest Result | Ghi chú |
| :--- | :---: | :---: | :--- |
| **Tổng số test cases** | **11** | **11** | Đầy đủ 3 nhóm kiểm thử |
| **Số test case PASS** | **7** | **7** | Các tính năng hoạt động đúng nghiệp vụ |
| **Số test case FAIL** | **4** | **4** | **4 lỗi cố ý của hệ thống SUT được phát hiện thành công** |
| **Số test case BLOCKED** | **0** | **0** | Không có test case bị nghẽn |
| **Tỷ lệ Pass (Pass Rate)** | **63.64%** | **63.64%** | Khớp chính xác baseline kiểm thử |

> [!NOTE]
> Tiến trình Jest kết thúc với **exit code: 1** (Non-zero exit code). Đây là **hành vi hoàn toàn dự kiến** và là bằng chứng thực nghiệm khẳng định 4 lỗi ẩn của hệ thống SUT (System Under Test) đã được bộ test phát hiện chính xác, không phải do lỗi hạ tầng hay lỗi script test.

---

## 7. DANH SÁCH BUG PHÁT HIỆN

### BUG-DB-001: Orphan Record trong bảng `coupon_usage` khi xóa User do thiếu Foreign Key Constraint

- **Severity**: High
- **Component**: Database Schema – Table `coupon_usage`
- **Found by Test Case**: `TC-DB-001`
- **Preconditions**: User 1 tồn tại và có dữ liệu lịch sử sử dụng coupon trong bảng `coupon_usage`.
- **Steps to Reproduce**:
  1. Đã có record `user_id = 1` trong bảng `coupon_usage`.
  2. Thực hiện câu lệnh SQL: `DELETE FROM users WHERE id = 1;`
  3. Truy vấn bảng `coupon_usage`: `SELECT * FROM coupon_usage WHERE user_id = 1;`
- **Expected Result**: DB từ chối xóa user hoặc tự động xóa sạch dữ liệu liên quan trong `coupon_usage` (rows length = 0).
- **Actual Result**: User 1 bị xóa nhưng record trong `coupon_usage` vẫn tồn tại, trở thành dữ liệu mồ côi (orphan record).
- **Evidence**:
  ```text
  ● Database Integrity Testing › TC-DB-001: Referential Integrity – orphan record
    expect(received).toBe(expected) // Object.is equality
    Expected: 0
    Received: 1
  ```
- **Business Impact**: Gây rác dữ liệu database, vi phạm tính toàn vẹn dữ liệu (Referential Integrity), có thể gây lỗi hệ thống khi các báo cáo thống kê JOIN giữa `coupon_usage` và `users`.

---

### BUG-API-002: Trả về sai kiểu dữ liệu trường `price` (String thay vì Number) đối với sản phẩm có ID chẵn

- **Severity**: Medium
- **Component**: API `GET /api/products/:id`
- **Found by Test Case**: `TC-DB-003`
- **Preconditions**: Database có các sản phẩm ID 1, 2, 3, 4, 5 với giá `price` dạng `REAL/Number`.
- **Steps to Reproduce**:
  1. Gửi request `GET /api/products/2`.
  2. Gửi request `GET /api/products/4`.
  3. Kiểm tra kiểu dữ liệu của `res.body.price`.
- **Expected Result**: Trường `price` trong JSON response phải luôn là kiểu `number` đối với mọi sản phẩm (`typeof price === 'number'`).
- **Actual Result**: Với các sản phẩm có ID chẵn (ID 2 và ID 4), trường `price` bị chuyển thành kiểu string (`"200"`, `"400"`).
- **Evidence**:
  ```text
  ● Database Integrity Testing › TC-DB-003: Data Type Consistency
    Received: Array [
      Object { "id": 2, "price": "200", "priceType": "string", "statusCode": 200 },
      Object { "id": 4, "price": "400", "priceType": "string", "statusCode": 200 }
    ]
  ```
- **Business Impact**: Phá vỡ API Contract. Các ứng dụng Frontend hoặc Mobile App khi nhận dữ liệu string có thể thực hiện phép cộng chuỗi sai lệch (ví dụ: `"200" + 10 = "20010"` thay vì `210`) gây tính toán sai tổng tiền đơn hàng.

---

### BUG-API-003: Sai công thức tính toán số tiền giảm giá cho Coupon phần trăm (`POST /api/apply-coupon`)

- **Severity**: High
- **Component**: API `POST /api/apply-coupon`
- **Found by Test Case**: `TC-COUPON-001`
- **Preconditions**: Mã giảm giá `CP_PERCENT` có `discount_value = 0.10` (đại diện cho 10%).
- **Steps to Reproduce**:
  1. Gửi payload: `{ "user_id": 1, "coupon_code": "CP_PERCENT", "total_amount": 200 }`.
  2. Kiểm tra `discount_amount` và `final_amount` trong response.
- **Expected Result**:
  - `discount_amount` = $200 \times 0.10 = 20$
  - `final_amount` = $200 - 20 = 180$
- **Actual Result**: `discount_amount = 180`, `final_amount = 20`.
- **Evidence**:
  ```text
  ● Integration Testing – Apply Coupon › TC-COUPON-001: Coupon percent hợp lệ
    Object {
      "coupon_code": "CP_PERCENT",
    - "discount_amount": 20,
    - "final_amount": 180,
    + "discount_amount": 180,
    + "final_amount": 20,
      "total_amount": 200
    }
  ```
- **Business Impact**: Thiệt hại tài chính nghiêm trọng cho doanh nghiệp (đơn hàng $200 chỉ thu $20, giảm giá tới $180 thay vì giảm $20).

---

### BUG-API-004: Cho phép chuyển trạng thái đơn hàng không hợp lệ từ `canceled` sang `delivered`

- **Severity**: High
- **Component**: API `PUT /api/admin/orders/:id/status`
- **Found by Test Case**: `TC-ORDER-002`
- **Preconditions**: Order 2 đang có trạng thái `canceled` trong database.
- **Steps to Reproduce**:
  1. Gửi request `PUT /api/admin/orders/2/status` với body `{ "status": "delivered" }`.
  2. Truy vấn trực tiếp database để kiểm tra cột `status` của Order 2.
- **Expected Result**: API trả về HTTP 400 (`Invalid status transition`) và trạng thái đơn hàng trong DB phải giữ nguyên là `canceled`.
- **Actual Result**: API trả về HTTP 200 và trạng thái đơn hàng trong DB bị cập nhật thành `delivered`.
- **Evidence**:
  ```text
  ● Integration Testing – Order State Machine › TC-ORDER-002: Invalid canceled -> delivered
    Received: Object { "databaseStatus": "delivered", "statusCode": 200 }
    Expected: Object { "databaseStatus": "canceled", "statusCode": 400 }
  ```
- **Business Impact**: Sai lệch báo cáo doanh thu và giao vận; một đơn hàng đã hủy vẫn được đánh dấu là đã giao thành công, gây gian lận hoặc thất thoát hàng hóa.

---

## 8. PHÂN TÍCH NGUYÊN NHÂN NỀN TẢNG (ROOT CAUSE ANALYSIS) VÀ CODE FIX PATCHES

### 8.1. Root Cause & Patch cho BUG-DB-001
- **Root Cause**: Bảng `coupon_usage` được khởi tạo thiếu khai báo Khóa ngoại `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`. Đồng thời kết nối SQLite mặc định chưa bật pragma foreign keys.
- **Proposed Fix Patch**:
  ```sql
  PRAGMA foreign_keys = ON;

  CREATE TABLE IF NOT EXISTS coupon_usage (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      coupon_id INTEGER NOT NULL,
      user_id INTEGER NOT NULL,
      used_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (coupon_id) REFERENCES coupons(id) ON DELETE CASCADE,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
  );
  ```

---

### 8.2. Root Cause & Patch cho BUG-API-002
- **Root Cause**: Trong file `app.js` (dòng 62), mã nguồn cố tình ép giá trị `row.price` sang dạng chuỗi khi `row.id % 2 === 0`:
  ```javascript
  if (row.id % 2 === 0) {
      row.price = row.price.toString();
  }
  ```
- **Proposed Fix Patch**: Xóa hoàn toàn đoạn mã ép kiểu chẵn/lẻ, bảo đảm luôn giữ nguyên kiểu số hoặc cast về `Number`:
  ```javascript
  app.get('/api/products/:id', (req, res) => {
    const productId = req.params.id;
    db.get('SELECT * FROM products WHERE id = ?', [productId], (err, row) => {
      if (err) return res.status(500).json({ error: err.message });
      if (!row) return res.status(404).json({ error: 'Product not found' });
      
      // Fix: Luôn đảm bảo price là Number
      row.price = Number(row.price);
      return res.status(200).json(row);
    });
  });
  ```

---

### 8.3. Root Cause & Patch cho BUG-API-003
- **Root Cause**: Trong file `app.js` (dòng 106), thuật toán tính giá trị giảm cho coupon phần trăm bị viết ngược, lấy số tiền còn lại gán cho `discount_amount`:
  ```javascript
  discount_amount = total_amount * (1 - coupon.discount_value);
  ```
- **Lưu ý về Convention quy đổi dữ liệu**: Bảng `coupons` lưu `discount_value = 0.10` tương ứng 10%. Do đó, công thức đúng phải nhân trực tiếp `coupon.discount_value` mà **không chia 100**.
- **Proposed Fix Patch**:
  ```javascript
  if (coupon.discount_type === 'percent') {
    // Fix: Công thức giảm giá đúng cho convention 0.10
    discount_amount = total_amount * coupon.discount_value;
  } else if (coupon.discount_type === 'fixed') {
    discount_amount = coupon.discount_value;
  }
  discount_amount = Math.min(total_amount, Math.max(0, discount_amount));
  const final_amount = Math.max(0, total_amount - discount_amount);
  ```

---

### 8.4. Root Cause & Patch cho BUG-API-004
- **Root Cause**: Trong file `app.js` (dòng 155), tồn tại nhánh `if` cho phép chuyển trạng thái từ `canceled` sang `delivered`:
  ```javascript
  if (currentStatus === 'canceled' && status === 'delivered') {
      isValidTransition = true;
  }
  ```
- **Proposed Fix Patch**: Xóa bỏ câu điều kiện sai trên và tái cấu trúc bằng bảng chuyển trạng thái (State Transition Matrix):
  ```javascript
  const allowedTransitions = {
    pending: ['confirmed', 'canceled'],
    confirmed: ['shipping', 'canceled'],
    shipping: ['delivered'],
    delivered: [],
    canceled: []
  };

  const isValidTransition = allowedTransitions[currentStatus]?.includes(status) || false;
  ```

---

## 9. ĐÁNH GIÁ TEST ISOLATION VÀ ĐỘ TỰ CỦA BỘ TEST (RELIABILITY & ISOLATION)

1. **Khả năng tái lập (Determinism & Repeatability)**:
   - Đã thực hiện gọi `faker.seed(23127207)` ở đầu hàm `setupTestDB(db)`.
   - Kết quả test qua 2 lần chạy liên tiếp thu được chỉ số giống hệt nhau: **11 total, 7 pass, 4 fail (Time ~6.8s - 7.7s)**.

2. **Tính độc lập giữa các Test Cases (Test Isolation)**:
   - Thực thi riêng biệt các test case đơn lẻ qua cờ `-t` của Jest (ví dụ: `npx jest -t "TC-COUPON-001"` hay `npx jest -t "TC-ORDER-001"`).
   - Tất cả các test đều chạy thành công độc lập mà không hề bị phụ thuộc vào trạng thái dữ liệu còn thừa của các test chạy trước đó.

3. **Quản lý Tài nguyên Database (Resource Clean-up)**:
   - Quá trình khởi tạo schema được đồng bộ qua Promise `schemaReady`.
   - Sau khi hoàn tất test suite, hàm `afterAll` thực thi `teardownTestDB(db)` đóng kết nối SQLite in-memory một cách triệt để, bảo đảm không xảy ra tình trạng "database is closed" hay "open handle".

---

## 10. KẾT LUẬN

Bộ kiểm thử tự động **Mini Lab Database Testing** đã hoàn thành 100% các tiêu chí yêu cầu của bài lab:
- Xây dựng thành công bộ dữ liệu thử nghiệm chuẩn với `@faker-js/faker` kết hợp seeding cố định.
- Triển khai 11 test cases bao phủ trọn vẹn Database Integrity, Integration Testing Apply Coupon và Order State Machine.
- Đã chứng minh và trích xuất bằng chứng thực nghiệm cho **4 lỗi ẩn trọng yếu của hệ thống SUT**.
- Báo cáo đã cung cấp phân tích nguyên nhân gốc rễ (Root Cause Analysis) và đề xuất bản vá mã nguồn (Code Fix Patch) chi tiết, chuẩn xác theo quy ước dữ liệu của bài.
