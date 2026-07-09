# Ví Dụ Mẫu: Thiết Kế & Thực Thi Kiểm Thử Cho FR-07: Shopping Cart

Tài liệu này minh họa quá trình thực hiện kiểm thử end-to-end cho tính năng **FR-07: Shopping Cart** sử dụng kỹ năng `eshop-domain-bva-testing-skill`. Tất cả các nội dung dưới đây đều là mẫu minh họa dựa trên nghiệp vụ của EShop.

---

## 1. Feature Input Mẫu (Feature Specifications)

* **Feature ID:** FR-07
* **Feature Name:** Giỏ hàng (Shopping Cart)
* **Pool:** Pool B (Shopping Cart and Checkout)
* **Target Role:** Khách vãng lai và Thành viên đã đăng nhập
* **Description:** Cho phép người dùng thêm sản phẩm vào giỏ, cập nhật số lượng, áp dụng mã giảm giá và xem tổng tiền trước khi thanh toán.
* **Related UI Pages:** `/products/:id` (Trang chi tiết sản phẩm), `/cart` (Trang giỏ hàng)
* **Related API Endpoints:**
  - `POST /api/cart/add` (Thêm vào giỏ)
  - `PUT /api/cart/items/:id` (Cập nhật số lượng)
  - `DELETE /api/cart/items/:id` (Xóa sản phẩm)
  - `POST /api/cart/coupon` (Áp dụng coupon)
* **Preconditions:**
  - Sản phẩm tồn tại và còn hàng trong kho (`Stock > 0`).
  - Hệ thống đang chạy bình thường ở địa chỉ `http://localhost:3000`.
* **Business Rules & Constraints:**
  - Số lượng mua cho mỗi sản phẩm (`quantity`) phải từ `1` đến `100`.
  - Nếu sản phẩm đã có trong giỏ, việc thêm tiếp sẽ cộng dồn số lượng. Tổng số lượng cộng dồn không được vượt quá số lượng tồn kho của sản phẩm đó hoặc giới hạn tối đa `100`.
  - Mã giảm giá (`coupon_code`) là tùy chọn, nếu nhập phải có độ dài từ `5` đến `15` ký tự chữ và số, phải tồn tại trong cơ sở dữ liệu và còn hạn sử dụng.

---

## 2. Phân Tích Phân Vùng Tương Đương (Domain Partitions)

### Tham số đầu vào: `quantity` (Số lượng)
* **VC-quantity-01:** Số nguyên trong khoảng `[1, 100]` (Hợp lệ).
* **IC-quantity-01:** Số nguyên `<= 0` (Không hợp lệ).
* **IC-quantity-02:** Số nguyên `> 100` (Không hợp lệ).
* **IC-quantity-03:** Số lượng lớn hơn tồn kho thực tế (Không hợp lệ).
* **IC-quantity-04:** Dữ liệu không phải số nguyên (ký tự chữ, số thập phân) (Không hợp lệ).

### Tham số đầu vào: `coupon_code` (Mã giảm giá)
* **VC-coupon-01:** Mã giảm giá để trống (Hợp lệ).
* **VC-coupon-02:** Mã giảm giá hợp lệ, tồn tại và còn hạn (Hợp lệ).
* **IC-coupon-01:** Mã giảm giá không tồn tại trong hệ thống (Không hợp lệ).
* **IC-coupon-02:** Mã giảm giá đã hết hạn sử dụng (Không hợp lệ).
* **IC-coupon-03:** Mã giảm giá quá ngắn (`< 5` ký tự) hoặc quá dài (`> 15` ký tự) (Không hợp lệ).

### Bảng Mô Hình Miền (Domain Model Table)

| Tham Số (Parameter) | Phân Vùng Hợp Lệ (Valid) | Phân Vùng Không Hợp Lệ (Invalid) | Kết Quả Kỳ Vọng (Expected Outcome) |
| :--- | :--- | :--- | :--- |
| `quantity` | `1 <= Q <= 100` | `Q <= 0`, `Q > 100`, `Q > Stock`, `Q` không phải số nguyên | Chấp nhận thêm vào giỏ / Từ chối và hiển thị thông báo lỗi |
| `coupon_code` | Rỗng hoặc Trùng khớp mã hợp lệ | Không tồn tại, Hết hạn, Độ dài sai quy định | Áp dụng giảm giá thành công / Báo lỗi mã không hợp lệ |

---

## 3. Phân Tích Giá Trị Biên Mẫu (BVA Variables)

Áp dụng quy tắc 3-điểm-biên cho các tham số giới hạn.

### Biến: `quantity` (Giới hạn `[1, 100]`, Giả sử Tồn kho `Stock = 10`)
* **Biên dưới (Min = 1):**
  * `quantity = 0` (Min-1, Invalid)
  * `quantity = 1` (Min, Valid)
  * `quantity = 2` (Min+1, Valid)
* **Biên trên (Max = 100):**
  * `quantity = 99` (Max-1, Valid)
  * `quantity = 100` (Max, Valid)
  * `quantity = 101` (Max+1, Invalid)
* **Biên thực tế tồn kho (Stock = 10):**
  * `quantity = 10` (Stock, Valid)
  * `quantity = 11` (Stock+1, Invalid)

### Biến: Độ dài `coupon_code` (Giới hạn độ dài `[5, 15]` ký tự)
* **Biên dưới (Min = 5):**
  * Độ dài `4` ký tự (Min-1, Invalid)
  * Độ dài `5` ký tự (Min, Valid)
  * Độ dài `6` ký tự (Min+1, Valid)
* **Biên trên (Max = 15):**
  * Độ dài `14` ký tự (Max-1, Valid)
  * Độ dài `15` ký tự (Max, Valid)
  * Độ dài `16` ký tự (Max+1, Invalid)

---

## 4. Danh Sách 8 Domain Test Cases Mẫu

| Test Case ID | Type | Objective | Preconditions | Test Data | Steps | Expected Result | Actual Result | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-FR07-DT-001 | Positive | Kiểm tra thêm sản phẩm vào giỏ hàng thành công với số lượng hợp lệ | Người dùng ở trang chi tiết sản phẩm | `product_id = 1`, `quantity = 5` | 1. Nhập số lượng 5.<br>2. Nhấn nút "Thêm vào giỏ". | Sản phẩm được thêm thành công, số lượng giỏ hàng trên header hiển thị 5. | Giỏ hàng hiển thị 5 sản phẩm. | Passed | Thực tế chạy đạt |
| TC-FR07-DT-002 | Negative | Kiểm tra hệ thống từ chối khi nhập số lượng bằng 0 | Người dùng ở trang chi tiết sản phẩm | `product_id = 1`, `quantity = 0` | 1. Nhập số lượng 0.<br>2. Nhấn nút "Thêm vào giỏ". | Giao diện hiển thị thông báo lỗi "Số lượng phải lớn hơn 0", không thêm vào giỏ. | Hệ thống báo lỗi hợp lệ. | Passed |  |
| TC-FR07-DT-003 | Negative | Kiểm tra hệ thống từ chối khi nhập số lượng âm | Người dùng ở trang chi tiết sản phẩm | `product_id = 1`, `quantity = -5` | 1. Nhập số lượng -5.<br>2. Nhấn nút "Thêm vào giỏ". | Giao diện hiển thị thông báo lỗi "Số lượng không hợp lệ", nút thêm bị vô hiệu hóa. | (Xem BUG-FR07-B-01) Cho phép gửi API thành công. | Failed | Phát hiện BUG-FR07-B-01 |
| TC-FR07-DT-004 | Negative | Kiểm tra hệ thống từ chối khi số lượng vượt quá tồn kho | Sản phẩm tồn kho còn 10 | `product_id = 1`, `quantity = 15` | 1. Nhập số lượng 15.<br>2. Nhấn nút "Thêm vào giỏ". | Hiển thị thông báo lỗi "Vượt quá số lượng tồn kho (10 sản phẩm)". | Cho phép thêm 15 sản phẩm thành công. | Failed | Phát hiện BUG-FR07-B-02 |
| TC-FR07-DT-005 | Negative | Kiểm tra hệ thống từ chối khi số lượng không phải số nguyên | Người dùng ở trang chi tiết sản phẩm | `product_id = 1`, `quantity = 2.5` | 1. Nhập số lượng 2.5.<br>2. Nhấn nút "Thêm vào giỏ". | Giao diện tự động làm tròn hoặc hiển thị lỗi số lượng không hợp lệ. | Ô nhập tự động chuyển thành 2. | Passed | Tự động làm tròn về số nguyên gần nhất |
| TC-FR07-DT-006 | Positive | Kiểm tra áp dụng mã giảm giá hợp lệ thành công | Có sản phẩm trong giỏ, tổng tiền 100k | `coupon_code = "DISCOUNT10"` | 1. Vào trang giỏ hàng.<br>2. Nhập "DISCOUNT10".<br>3. Nhấn "Áp dụng". | Áp dụng thành công, tổng thanh toán giảm 10% (còn 90k). | Áp dụng thành công, trừ 10%. | Passed |  |
| TC-FR07-DT-007 | Negative | Kiểm tra áp dụng mã giảm giá không tồn tại | Có sản phẩm trong giỏ | `coupon_code = "NOSUCHCODE"` | 1. Vào trang giỏ hàng.<br>2. Nhập "NOSUCHCODE".<br>3. Nhấn "Áp dụng". | Hiển thị thông báo lỗi "Mã giảm giá không tồn tại". | Báo lỗi mã không hợp lệ. | Passed |  |
| TC-FR07-DT-008 | Negative | Kiểm tra áp dụng mã giảm giá đã hết hạn | Có sản phẩm trong giỏ | `coupon_code = "EXPIRED50"` | 1. Vào trang giỏ hàng.<br>2. Nhập "EXPIRED50".<br>3. Nhấn "Áp dụng". | Hiển thị lỗi "Mã giảm giá đã hết hạn sử dụng". | Áp dụng thành công mã hết hạn. | Failed | Phát hiện BUG-FR07-B-03 |

---

## 5. Danh Sách 8 BVA Test Cases Mẫu

| Test Case ID | Type | Objective | Preconditions | Test Data | Steps | Expected Result | Actual Result | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-FR07-BVA-001 | Edge | Kiểm tra số lượng tại biên dưới hợp lệ (Min = 1) | Giỏ hàng trống | `quantity = 1` | 1. Nhập số lượng 1.<br>2. Nhấn "Thêm vào giỏ". | Sản phẩm được thêm thành công với số lượng là 1. | Sản phẩm thêm thành công. | Passed |  |
| TC-FR07-BVA-002 | Edge | Kiểm tra số lượng ngay dưới biên dưới (Min-1 = 0) | Giỏ hàng trống | `quantity = 0` | 1. Nhập số lượng 0.<br>2. Nhấn "Thêm vào giỏ". | Báo lỗi "Số lượng phải lớn hơn hoặc bằng 1". | Hệ thống hiển thị lỗi. | Passed |  |
| TC-FR07-BVA-003 | Edge | Kiểm tra số lượng ngay trên biên dưới (Min+1 = 2) | Giỏ hàng trống | `quantity = 2` | 1. Nhập số lượng 2.<br>2. Nhấn "Thêm vào giỏ". | Sản phẩm được thêm thành công với số lượng là 2. | Sản phẩm thêm thành công. | Passed |  |
| TC-FR07-BVA-004 | Edge | Kiểm tra số lượng ngay dưới biên trên (Max-1 = 99) | Kho hàng có 200 sản phẩm | `quantity = 99` | 1. Nhập số lượng 99.<br>2. Nhấn "Thêm vào giỏ". | Sản phẩm được thêm thành công với số lượng là 99. | Sản phẩm thêm thành công. | Passed |  |
| TC-FR07-BVA-005 | Edge | Kiểm tra số lượng tại biên trên hợp lệ (Max = 100) | Kho hàng có 200 sản phẩm | `quantity = 100` | 1. Nhập số lượng 100.<br>2. Nhấn "Thêm vào giỏ". | Sản phẩm được thêm thành công với số lượng là 100. | Sản phẩm thêm thành công. | Passed |  |
| TC-FR07-BVA-006 | Edge | Kiểm tra số lượng ngay trên biên trên (Max+1 = 101) | Kho hàng có 200 sản phẩm | `quantity = 101` | 1. Nhập số lượng 101.<br>2. Nhấn "Thêm vào giỏ". | Hệ thống chặn từ chối và báo lỗi "Số lượng tối đa mỗi lần mua là 100". | Cho phép thêm 101 sản phẩm. | Failed | Phát hiện BUG-FR07-B-02 nâng cao |
| TC-FR07-BVA-007 | Edge | Kiểm tra độ dài mã giảm giá tại biên dưới (Min length = 5) | Có sản phẩm trong giỏ | `coupon_code = "SALE5"` | 1. Nhập mã "SALE5" (5 ký tự).<br>2. Nhấn "Áp dụng". | Hệ thống gửi request và phản hồi mã không tồn tại hoặc áp dụng thành công nếu có trong DB. | Gửi request thành công. | Passed |  |
| TC-FR07-BVA-008 | Edge | Kiểm tra độ dài mã giảm giá ngay dưới biên dưới (Min length - 1 = 4) | Có sản phẩm trong giỏ | `coupon_code = "GIFT"` | 1. Nhập mã "GIFT" (4 ký tự).<br>2. Nhấn "Áp dụng". | Chặn ở giao diện, hiển thị báo lỗi "Mã giảm giá phải từ 5-15 ký tự". | Áp dụng bình thường và báo không tồn tại. | Failed | Giao diện không validate độ dài trước khi gửi API |

---

## 6. Ba (3) Bug Reports Mẫu

### BUG 1: BUG-FR07-B-01
* **Title:** `[BUG][Shopping Cart] Số lượng sản phẩm có thể cập nhật thành số âm qua API`
* **Severity:** Major | **Priority:** High
* **Steps to Reproduce:**
  1. Thêm 1 sản phẩm vào giỏ hàng.
  2. Sử dụng Postman gửi request `PUT /api/cart/items/1` với payload `{"quantity": -5}`.
  3. Kiểm tra giỏ hàng trên giao diện Web.
* **Actual Result:** API trả về `200 OK`, số lượng sản phẩm trong giỏ hàng hiển thị là `-5`. Tổng tiền giỏ hàng bị trừ âm.
* **Expected Result:** API trả về lỗi `400 Bad Request`, thông báo số lượng không hợp lệ. Số lượng trong giỏ hàng không bị thay đổi.
* **Evidence:** ![Screenshot BUG 1](file:///tests/bug/evidence/BUG-FR07-B-01_screenshot.png)
* **Suggested Fix:** Thêm validation ở Backend controller: `if (quantity < 1) throw new BadRequestException("Quantity must be at least 1");`

### BUG 2: BUG-FR07-B-02
* **Title:** `[BUG][Shopping Cart] Cho phép tăng số lượng sản phẩm trong giỏ vượt quá tồn kho thực tế`
* **Severity:** Major | **Priority:** Medium
* **Steps to Reproduce:**
  1. Chọn sản phẩm A có số lượng tồn kho hiện tại là 3.
  2. Vào trang chi tiết, nhập số lượng là 10.
  3. Nhấn nút "Thêm vào giỏ".
* **Actual Result:** Sản phẩm được thêm thành công vào giỏ hàng với số lượng là 10.
* **Expected Result:** Hệ thống hiển thị thông báo lỗi "Sản phẩm chỉ còn lại 3 sản phẩm trong kho. Vui lòng giảm số lượng."
* **Evidence:** ![Screenshot BUG 2](file:///tests/bug/evidence/BUG-FR07-B-02_screenshot.png)
* **Suggested Fix:** Khi xử lý thêm vào giỏ ở Backend, cần truy vấn số lượng hàng tồn kho thực tế của sản phẩm từ DB và so sánh với số lượng yêu cầu của khách hàng trước khi lưu vào Session/Database.

### BUG 3: BUG-FR07-B-03
* **Title:** `[BUG][Shopping Cart] Áp dụng thành công mã giảm giá đã hết hạn sử dụng`
* **Severity:** Major | **Priority:** High
* **Steps to Reproduce:**
  1. Thêm sản phẩm trị giá 100,000 VND vào giỏ hàng.
  2. Tại ô mã giảm giá, nhập mã `EXPIRED50` (mã này có thời hạn sử dụng là ngày 2026-01-01, trong khi ngày hiện tại là 2026-06-28).
  3. Nhấn nút "Áp dụng".
* **Actual Result:** Mã giảm giá được áp dụng thành công, tổng tiền phải thanh toán giảm xuống còn 50,000 VND.
* **Expected Result:** Hệ thống từ chối mã và hiển thị thông báo lỗi: "Mã giảm giá này đã hết hạn sử dụng."
* **Evidence:** ![Screenshot BUG 3](file:///tests/bug/evidence/BUG-FR07-B-03_screenshot.png)
* **Suggested Fix:** Cập nhật điều kiện truy vấn mã giảm giá tại backend: `WHERE code = :code AND expiry_date >= NOW() AND is_active = true`.

---

## 7. AI Gap Analysis Mẫu

* **AI Generated (Ban đầu):** AI chỉ sinh ra các test case cơ bản liên quan đến kiểu dữ liệu của trường `quantity` và độ dài hợp lệ của chuỗi `coupon_code` dựa trên phân tích đặc tả lý thuyết.
* **AI Missed (Những gì AI bỏ sót):**
  1. **Các kịch bản thực tế:** AI không phát hiện ra việc thiếu kiểm tra logic số lượng vượt quá tồn kho (`quantity > Stock`).
  2. **Bugs thực tế:** AI không thể biết Backend của SUT thiếu validation đầu vào đối với method `PUT /api/cart/items/:id`, dẫn đến lỗi cập nhật số lượng âm qua Postman/API.
  3. **Lỗi logic thời gian:** AI bỏ sót điều kiện so sánh ngày hiện tại với thời hạn sử dụng của mã giảm giá trong database.
* **Why AI Missed:** Do AI chỉ thực hiện phân tích tĩnh (static analysis) dựa trên Requirements.pdf, không thể tương tác trực tiếp với API và Database của EShop để khám phá ra các lỗ hổng lập trình (implementation gaps).
* **Human Correction:** Tôi đã trực tiếp cài đặt Postman, gửi request API thử nghiệm và phát hiện ra backend không kiểm tra tính hợp lệ của số lượng âm. Tôi đã tự thiết kế bổ sung 3 test case API và 2 test case logic tồn kho.

---

## 8. AI Audit Entry Mẫu

* **Interaction ID:** `INT-001`
* **AI Tool Name:** Gemini 3.5 Flash (High)
* **Date & Time:** 2026-06-28 10:15
* **Task Purpose:** Thiết kế test case ban đầu cho FR-07.
* **Prompt Used:** *"Hãy giúp tôi phân tích phân vùng tương đương và giá trị biên cho trường quantity và coupon_code của tính năng giỏ hàng EShop."*
* **AI Output Summary:** Cung cấp danh sách các phân vùng cơ bản của `quantity` (1-100) và `coupon_code` (độ dài 5-15) cùng 10 test case mẫu.
* **Human Review & Correction:** Bổ sung thêm các kịch bản kiểm tra logic tồn kho thực tế của sản phẩm và kiểm tra API âm.

---

## 9. Test Summary Mẫu

* **Designed:** 16 test cases (8 Domain, 8 BVA).
* **Executed:** 16 test cases.
* **Passed:** 11.
* **Failed:** 5.
* **Blocked:** 0.
* **Bugs Found:** 3 bugs.
* **GitHub Issues Created:** Issue #25, #26, #27.

---

## 10. Gợi Ý Git Commit Messages

Nhằm đảm bảo lịch sử commit minh bạch và chuyên nghiệp, dưới đây là chuỗi commit đề xuất cho FR-07:
1. `feat(test): add test specification input for FR-07 shopping cart`
2. `test(fr07): design domain testing equivalence partitioning test cases`
3. `test(fr07): design boundary value analysis (BVA) test cases`
4. `test(fr07): update traceability matrix for designed test cases`
5. `test(fr07): execute test cases on localhost and record results`
6. `bug(fr07): create bug report BUG-FR07-B-01 for negative quantity issue`
7. `bug(fr07): create bug report BUG-FR07-B-02 for overselling inventory issue`
8. `bug(fr07): create bug report BUG-FR07-B-03 for expired coupon issue`
9. `docs(fr07): complete AI gap analysis and audit log for shopping cart`
