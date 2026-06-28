# Boundary Value Analysis Report: FR-21 – Mobile Cart & Checkout

## 1. Boundary Variables & Analysis

We apply the **3-point boundary value testing** (where appropriate) or standard boundary verification to identify boundary values for critical inputs.

### 1.1. Quantity (Số lượng sản phẩm)
- **Ràng buộc:** Là số nguyên dương từ 1 đến số lượng tồn kho khả dụng (`maxStock`). Giả định sản phẩm kiểm thử có tồn kho `maxStock = 5`.
- **Biên dưới (1):**
  - **0 (Min-1):** Không hợp lệ. Hệ thống phải từ chối hoặc hồi quy về 1.
  - **1 (Min):** Hợp lệ. Cho phép thêm/cập nhật.
  - **2 (Min+1):** Hợp lệ. Cho phép thêm/cập nhật.
- **Biên trên (maxStock = 5):**
  - **4 (maxStock-1):** Hợp lệ.
  - **5 (maxStock):** Hợp lệ.
  - **6 (maxStock+1):** Không hợp lệ. Hệ thống phải báo lỗi vượt quá hàng tồn.
- **Biên cực đoan:** `-1` (số âm), `null`, `undefined`.

### 1.2. Phone Number Length (Độ dài số điện thoại trong hồ sơ)
- **Ràng buộc:** Độ dài từ 9 đến 10 chữ số (theo regex `/^[1-9][0-9]{8,9}$/`).
- **Độ dài 0 (Rỗng):** Không hợp lệ.
- **Độ dài 8 (Min-1):** Không hợp lệ.
- **Độ dài 9 (Min):** Hợp lệ.
- **Độ dài 10 (Max):** Hợp lệ.
- **Độ dài 11 (Max+1):** Không hợp lệ.

### 1.3. Full Name Length (Độ dài họ tên trong hồ sơ)
- **Ràng buộc:** Độ dài từ 1 đến 50 ký tự.
- **Độ dài 0 (Rỗng):** Không hợp lệ.
- **Độ dài 1 (Min):** Hợp lệ.
- **Độ dài 2 (Min+1):** Hợp lệ.
- **Độ dài 49 (Max-1):** Hợp lệ.
- **Độ dài 50 (Max):** Hợp lệ.
- **Độ dài 51 (Max+1):** Không hợp lệ.

### 1.4. Address Length (Độ dài địa chỉ giao hàng trong hồ sơ)
- **Ràng buộc:** Độ dài từ 5 đến 255 ký tự.
- **Độ dài 0 (Rỗng):** Không hợp lệ.
- **Độ dài 4 (Min-1):** Không hợp lệ.
- **Độ dài 5 (Min):** Hợp lệ.
- **Độ dài 6 (Min+1):** Hợp lệ.
- **Độ dài 254 (Max-1):** Hợp lệ.
- **Độ dài 255 (Max):** Hợp lệ.
- **Độ dài 256 (Max+1):** Không hợp lệ.

### 1.5. Number of Cart Items (Số lượng dòng sản phẩm khác nhau trong giỏ)
- **Biên dưới (1 dòng sản phẩm):**
  - **0 dòng (Giỏ rỗng):** Không hợp lệ. Chặn checkout.
  - **1 dòng:** Hợp lệ.
  - **2 dòng:** Hợp lệ.

---

## 2. Boundary Value Analysis Table

| Variable | Boundary Value | Class | Expected Result |
| :--- | :---: | :---: | :--- |
| **Quantity** | -1 | Invalid | Từ chối hoặc tự động hồi quy về 1 |
| | 0 | Invalid | Từ chối hoặc tự động hồi quy về 1 |
| | 1 | Valid | Cập nhật thành công |
| | 2 | Valid | Cập nhật thành công |
| | 4 (maxStock - 1) | Valid | Cập nhật thành công |
| | 5 (maxStock) | Valid | Cập nhật thành công |
| | 6 (maxStock + 1) | Invalid | Báo lỗi vượt quá tồn kho |
| **Phone Number Length** | 0 (trống) | Invalid | Báo lỗi Số điện thoại không hợp lệ |
| | 8 | Invalid | Báo lỗi Số điện thoại không hợp lệ |
| | 9 | Valid | Cập nhật hồ sơ thành công |
| | 10 | Valid | Cập nhật hồ sơ thành công |
| | 11 | Invalid | Báo lỗi Số điện thoại không hợp lệ |
| **Full Name Length** | 0 (trống) | Invalid | Báo lỗi Họ tên không được để trống |
| | 1 | Valid | Cập nhật hồ sơ thành công |
| | 2 | Valid | Cập nhật hồ sơ thành công |
| | 50 | Valid | Cập nhật hồ sơ thành công |
| | 51 | Invalid | Báo lỗi Họ tên quá dài |
| **Address Length** | 0 (trống) | Invalid | Báo lỗi Địa chỉ không được để trống |
| | 4 | Invalid | Báo lỗi Địa chỉ quá ngắn (từ 5 ký tự) |
| | 5 | Valid | Cập nhật hồ sơ thành công |
| | 6 | Valid | Cập nhật hồ sơ thành công |
| | 255 | Valid | Cập nhật hồ sơ thành công |
| | 256 | Invalid | Báo lỗi Địa chỉ quá dài |
| **Cart Items Count** | 0 | Invalid | Chặn nút đặt hàng / Không được thanh toán |
| | 1 | Valid | Thanh toán thành công |
| | 2 | Valid | Thanh toán thành công |

---

## 3. BVA Test Cases List
All test cases are detailed in separate files in [tests/test-cases/mobile-cart/](../../tests/test-cases/mobile-cart):

- [TC-MOBILE-CART-BVA-001: Cập nhật số lượng sản phẩm trong giỏ hàng về biên dưới cực tiểu (Quantity = 0)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-001.md)
- [TC-MOBILE-CART-BVA-002: Cập nhật số lượng sản phẩm trong giỏ hàng bằng 1 (Min)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-002.md)
- [TC-MOBILE-CART-BVA-003: Cập nhật số lượng sản phẩm trong giỏ hàng bằng 2 (Min+1)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-003.md)
- [TC-MOBILE-CART-BVA-004: Đặt hàng thành công với số lượng ở biên tồn kho cận trên (Quantity = maxStock - 1)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-004.md)
- [TC-MOBILE-CART-BVA-005: Đặt hàng thành công với số lượng ở biên tồn kho cực đại (Quantity = maxStock)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-005.md)
- [TC-MOBILE-CART-BVA-006: Chặn đặt hàng với số lượng vượt biên tồn kho (Quantity = maxStock + 1)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-006.md)
- [TC-MOBILE-CART-BVA-007: Chặn cập nhật hồ sơ với Số điện thoại có độ dài dưới biên (8 chữ số)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-007.md)
- [TC-MOBILE-CART-BVA-008: Cập nhật hồ sơ thành công với Số điện thoại có độ dài ở biên cực tiểu (9 chữ số)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-008.md)
- [TC-MOBILE-CART-BVA-009: Cập nhật hồ sơ thành công với Số điện thoại có độ dài ở biên cực đại (10 chữ số)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-009.md)
- [TC-MOBILE-CART-BVA-010: Chặn cập nhật hồ sơ với Số điện thoại có độ dài vượt biên cực đại (11 chữ số)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-010.md)
- [TC-MOBILE-CART-BVA-011: Cập nhật hồ sơ thành công với Họ tên có độ dài 1 ký tự (Min)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-011.md)
- [TC-MOBILE-CART-BVA-012: Cập nhật hồ sơ thành công với Họ tên có độ dài 2 ký tự (Min+1)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-012.md)
- [TC-MOBILE-CART-BVA-013: Cập nhật hồ sơ thành công với Họ tên có độ dài 50 ký tự (Max)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-013.md)
- [TC-MOBILE-CART-BVA-014: Chặn cập nhật hồ sơ với Họ tên có độ dài 51 ký tự (Max+1)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-014.md)
- [TC-MOBILE-CART-BVA-015: Chặn cập nhật hồ sơ với Địa chỉ có độ dài 4 ký tự (Min-1)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-015.md)
- [TC-MOBILE-CART-BVA-016: Cập nhật hồ sơ thành công với Địa chỉ có độ dài 5 ký tự (Min)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-016.md)
- [TC-MOBILE-CART-BVA-017: Cập nhật hồ sơ thành công với Địa chỉ có độ dài 6 ký tự (Min+1)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-017.md)
- [TC-MOBILE-CART-BVA-018: Cập nhật hồ sơ thành công với Địa chỉ có độ dài 255 ký tự (Max)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-018.md)
- [TC-MOBILE-CART-BVA-019: Chặn cập nhật hồ sơ với Địa chỉ có độ dài 256 ký tự (Max+1)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-019.md)
- [TC-MOBILE-CART-BVA-020: Chặn đặt hàng khi số dòng sản phẩm trong giỏ hàng bằng 0](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-020.md)
- [TC-MOBILE-CART-BVA-021: Đặt hàng thành công khi số dòng sản phẩm trong giỏ hàng bằng 1](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-021.md)
- [TC-MOBILE-CART-BVA-022: Đặt hàng thành công khi số dòng sản phẩm trong giỏ hàng bằng 2](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-022.md)
