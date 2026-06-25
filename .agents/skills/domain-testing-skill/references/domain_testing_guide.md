# Hướng dẫn chi tiết Quy trình Kiểm thử miền và Quản lý trên GitHub

Tài liệu này tổng hợp toàn bộ các kỹ thuật kiểm thử miền (Equivalence Partitioning & Boundary Value Analysis), ví dụ thực tế trên EShop SUT, hướng dẫn viết test script, và các biểu mẫu chuẩn quản lý kiểm thử trên GitHub.

---

## 1. Cấu trúc thư mục Đề xuất trong Repository
Tổ chức thư mục kiểm thử trong dự án phục vụ cho việc kiểm tra, review và thống kê:

```
project-root/
├── src/                    # Mã nguồn ứng dụng
├── tests/
│   ├── test-cases/         # Chứa thiết kế các test case chính thức
│   │   ├── register/
│   │   │   ├── TC-REG-001.md
│   │   │   └── TC-REG-002.md
│   │   ├── cart/
│   │   │   └── TC-CART-001.md
│   │   └── coupon/
│   │       └── TC-COUPON-001.md
│   ├── test-runs/          # Chứa kết quả thực thi theo sprint hoặc regression
│   │   └── sprint-1-test-run.md
│   ├── bug-reports/        # Chứa các file báo cáo lỗi cục bộ
│   │   └── BUG-CART-001.md
│   └── test-summary/       # Báo cáo tổng hợp và ma trận truy vết
│       └── traceability-matrix.md
└── .github/ISSUE_TEMPLATE/  # Chứa các biểu mẫu Bug Report
```

*Quy tắc quan trọng:* Không được sửa test case trực tiếp trên nhánh `main`. Hãy tạo branch mới và gửi Pull Request để được review thay đổi.

---

## 2. Quy ước đặt mã Test Case (Naming Convention)
Mã test case là khóa quan trọng để liên kết giữa Requirement, Test Run và Bug:
* **Cấu trúc:** `TC-[MODULE]-[NUMBER]`
* **Ví dụ đúng:**
  * `TC-LOGIN-001` (Test case số 1 của module Login)
  * `TC-REGISTER-005` (Test case số 5 của module Register)
  * `TC-CART-003` (Test case số 3 của module Cart)
  * `TC-CHECKOUT-010` (Test case số 10 của module Checkout)
* **Không nên dùng:** `test1`, `check-login`, `case-a`, `login-success-test-v2-final`.

---

## 3. Phân vùng Tương đương (EP) & Phân tích Biên (BVA) cho EShop SUT
* **Lưu ý**: Dưới đây chỉ là ví dụ, bạn cần phân tích và thiết kế test case cho EShop theo yêu cầu cụ thể của từng Module và Feature.

### A. Đăng ký tài khoản (FR-01) - Độ dài Mật khẩu (Password)
* **Đặc tả:** Mật khẩu hợp lệ dài từ 8 đến 30 ký tự.
* **Lớp tương đương (EP):**
  * Hợp lệ: `EC1: 8 <= length <= 30`
  * Không hợp lệ: `EC2: length < 8`, `EC3: length > 30`
* **Điểm biên 3 điểm (BVA):**
  * Ranh giới dưới (8): `7` (Invalid), `8` (Valid), `9` (Valid)
  * Ranh giới trên (30): `29` (Valid), `30` (Valid), `31` (Invalid)

### B. Giỏ hàng (FR-07) - Thêm số lượng sản phẩm (Quantity)
* **Đặc tả:** Số lượng mua tối thiểu là 1 và tối đa là 100 sản phẩm (số nguyên).
* **Lớp tương đương (EP):**
  * Hợp lệ: `EC4: 1 <= Quantity <= 100` (Số nguyên)
  * Không hợp lệ: `EC5: Quantity < 1`, `EC6: Quantity > 100`, `EC7: Không phải số nguyên`
* **Điểm biên 3 điểm (BVA):**
  * Ranh giới dưới (1): `0` (Invalid), `1` (Valid), `2` (Valid)
  * Ranh giới trên (100): `99` (Valid), `100` (Valid), `101` (Invalid)

### C. Áp dụng Coupon giảm giá (FR-09) - Giá trị Đơn hàng (Order Value)
* **Đặc tả:** Tổng đơn hàng tối thiểu đạt `150,000 VND`.
* **Lớp tương đương (EP):**
  * Hợp lệ: `EC8: Order Value >= 150,000`
  * Không hợp lệ: `EC9: Order Value < 150,000`
* **Điểm biên 2 điểm (BVA):**
  * `149,999 VND` (Invalid - Không được áp dụng)
  * `150,000 VND` (Valid - Được áp dụng)

---

## 4. Biểu mẫu chuẩn Markdown của Test Case
Lưu trữ dưới dạng file `.md` trong thư mục `tests/test-cases/[module]/`.

```markdown
# TC-CART-001: Thêm sản phẩm vào giỏ với số lượng hợp lệ biên dưới

## Requirement ID
FR-07: Shopping Cart

## Module / Test type / Technique
Cart / Functional / Boundary Value Analysis (3-Point)

## Preconditions
- Người dùng đã đăng nhập thành công vào EShop.
- Đang ở trang chi tiết sản phẩm còn hàng.
- Giỏ hàng hiện tại đang trống.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **Quantity** | 1 |

## Test steps
1. Nhấp vào trường nhập số lượng sản phẩm.
2. Nhập giá trị số lượng là `1`.
3. Nhấp chọn nút "Thêm vào giỏ hàng" (Add to Cart).

## Expected result
- Sản phẩm được thêm vào giỏ hàng thành công.
- Icon giỏ hàng hiển thị số lượng sản phẩm là `1`.
- Hiển thị thông báo popup: "Sản phẩm đã được thêm vào giỏ hàng".

## Status / Related bugs
Not Run / None
```

---

## 5. Tạo Test Script tự động (Automated Test Script)
Trước khi tiến hành chạy test run nghiệm thu thực tế, kịch bản kiểm thử thủ công cần được chuyển hóa thành mã script kiểm thử tự động.

### Ví dụ Test Script (Playwright / JavaScript) cho TC-CART-001:
```javascript
const { test, expect } = require('@playwright/test');

test.describe('FR-07: Shopping Cart - Boundary Value Testing', () => {
  test('TC-CART-001: Add product with minimum valid quantity (Quantity = 1)', async ({ page }) => {
    // 1. Đi đến trang sản phẩm (Precondition)
    await page.goto('/products/detail/1');
    
    // 2. Nhập số lượng = 1 (Test steps)
    const quantityInput = page.locator('#quantity-input');
    await quantityInput.fill('1');
    
    // 3. Click Add to Cart
    await page.click('#add-to-cart-btn');
    
    // 4. Kiểm tra Expected Result
    const cartBadge = page.locator('#cart-badge');
    await expect(cartBadge).toHaveText('1');
    
    const toastMessage = page.locator('.toast-success');
    await expect(toastMessage).toContainText('Sản phẩm đã được thêm vào giỏ hàng');
  });
});
```

---

## 6. Biểu mẫu Ghi nhận Nhật ký Chạy thử (Test Run Log)
Ghi nhận kết quả thực thi các test case trong đợt test hoặc sprint cụ thể.

```markdown
# Test Run: Sprint 1 Execution Log

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **TC-CART-001** | Cart | Nguyễn Văn A | Pass | | Chạy tự động và thủ công đều đạt |
| **TC-CART-002** | Cart | Nguyễn Văn A | Fail | #18 | Nhập số lượng 101 hệ thống vẫn cho thêm |
| **TC-REG-001** | Register | Trần Thị B | Blocked | #19 | Trang đăng ký bị crash khi tải |
```

*Quy tắc:* Khi `Result = Fail` hoặc `Blocked` $\rightarrow$ Bắt buộc phải có liên kết `Related Bug` hoặc lý do rõ ràng.

---

## 7. Biểu mẫu báo cáo lỗi (Bug Report) khi Test Case fail
Lưu dưới dạng file Markdown cục bộ tại thư mục `tests/bug-reports/BUG-[MODULE]-[NUMBER].md` (Ví dụ: `BUG-CART-001.md`) để sẵn sàng tạo Issue trên GitHub.

```markdown
Title: [BUG][Cart] Hệ thống cho phép thêm sản phẩm vượt quá số lượng tối đa (Quantity = 101)

## Found by Test Case
TC-CART-002

## Requirement liên quan
FR-07: Shopping Cart

## Severity / Priority
Major / P1

## Environment
Chrome 122.0, Windows 11, URL: http://localhost:3000/products/detail/1

## Steps to reproduce
1. Truy cập trang chi tiết sản phẩm.
2. Nhập số lượng sản phẩm là `101`.
3. Nhấp chọn nút "Thêm vào giỏ hàng".

## Expected result
Hệ thống hiển thị thông báo lỗi: "Số lượng sản phẩm tối đa là 100" và không cho phép thêm vào giỏ.

## Actual result
Sản phẩm vẫn được thêm vào giỏ hàng thành công với số lượng 101.

## Evidence
[Link ảnh chụp màn hình / video lỗi hoặc file log đính kèm]
```

*Nhãn (Labels) cần gắn:* `type: bug`, `module: cart`, `severity: major`, `priority: P1`, `status: new`, `found-by: test-case`.

---

## 8. Ma trận truy vết lỗi (Traceability Matrix)
Bảng tổng hợp cuối sprint giúp chứng minh độ bao phủ các yêu cầu và vết lỗi của từng phần.

| Requirement | Test Case | Result | Bug Issue | Status |
| :--- | :--- | :--- | :--- | :--- |
| **FR-07: Shopping Cart** | `TC-CART-001` | Pass | | Done |
| **FR-07: Shopping Cart** | `TC-CART-002` | Fail | #18 | Open |
| **FR-01: Registration** | `TC-REG-001` | Blocked | #19 | Ready for Retest |
