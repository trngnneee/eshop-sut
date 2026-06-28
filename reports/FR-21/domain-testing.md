# Domain Testing Report: FR-21 – Mobile Cart & Checkout

## 1. Feature Specifications & Analysis
- **Feature ID:** FR-21 / FR24
- **Feature Name:** Mobile Cart & Checkout – Giỏ hàng và Thanh toán trên ứng dụng di động
- **Actors:**
  - **Guest User (Khách vãng lai):** Có thể xem sản phẩm, thêm sản phẩm vào giỏ, cập nhật số lượng, xóa sản phẩm khỏi giỏ, xem tổng tiền tạm tính. Không được thực hiện checkout (đặt hàng).
  - **Logged-in Customer (Khách hàng đã đăng nhập):** Có đầy đủ quyền của Guest, thêm thông tin giao hàng qua hồ sơ và thực hiện đặt hàng.
  - **Mobile App Frontend:** Ứng dụng di động (React Native) gửi các yêu cầu API và hiển thị giao diện cho người dùng.
  - **Backend API:** Hệ thống máy chủ xử lý các API đăng nhập, giỏ hàng, thông tin cá nhân và thanh toán.
- **Related UI Screens:**
  - Trang chủ Mobile (Danh sách sản phẩm)
  - Trang Chi tiết sản phẩm (Product Detail)
  - Trang Giỏ hàng (Cart Screen)
  - Trang Xác nhận đơn hàng (Checkout Screen)
  - Trang Hồ sơ cá nhân (Profile Screen - nơi thiết lập Họ tên, SĐT, Địa chỉ)
- **Related API Endpoints:**
  - `POST /api/checkout` (Thực hiện đặt hàng)
  - `PUT /api/users/me` (Cập nhật thông tin giao hàng bao gồm họ tên, SĐT, địa chỉ)
  - `GET /api/orders/my-orders` (Lấy danh sách đơn hàng đã mua)
- **Preconditions:**
  - Ứng dụng di động đã được cài đặt và mở thành công.
  - Backend API đang hoạt động bình thường.
  - Có dữ liệu sản phẩm trong cơ sở dữ liệu.
  - Khách hàng phải đăng nhập (có JWT token hợp lệ) để chuyển sang màn hình checkout và đặt hàng.
  - Thông tin giao hàng phải được điền và cập nhật trong Profile trước khi đặt hàng.
  - Sản phẩm trong giỏ hàng phải còn tồn kho.

- **Business Rules:**
  - Người dùng chưa đăng nhập không được phép checkout.
  - Không được phép đặt hàng khi giỏ hàng rỗng.
  - Không được phép đặt hàng với sản phẩm không tồn tại hoặc đã hết hàng.
  - Số lượng sản phẩm phải là số nguyên dương lớn hơn 0.
  - Số lượng đặt hàng không được vượt quá tồn kho khả dụng.
  - Khi thêm cùng một sản phẩm nhiều lần, hệ thống phải cộng dồn số lượng thay vì tạo dòng mới.
  - Khi cập nhật hoặc xóa sản phẩm khỏi giỏ, tổng tiền phải được tính lại chính xác.
  - Thông tin giao hàng bắt buộc phải có Họ tên, Số điện thoại và Địa chỉ.
  - Số điện thoại phải đúng định dạng hợp lệ.
  - Sau khi đặt hàng thành công, đơn hàng mới được tạo và giỏ hàng phải được làm trống.
  - Phải chống double-click (không tạo nhiều đơn trùng lặp khi người dùng nhấn nút Đặt hàng nhiều lần liên tiếp).

---

## 2. Equivalence Partitions (Phân vùng tương đương)

### 2.1. Authentication & Session Partitions
| Partition ID | Input Domain | Class Type | Description / Value | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| VP-MCART-001 | User Token | Valid | Token JWT hợp lệ của Customer đã đăng nhập | Cho phép truy cập Checkout và đặt hàng |
| IP-MCART-001 | User Token | Invalid | Không có token (Guest User) | Báo lỗi yêu cầu đăng nhập, điều hướng về trang Login |
| IP-MCART-002 | User Token | Invalid | Token bị hết hạn hoặc sai chữ ký | Báo lỗi token không hợp lệ, yêu cầu đăng nhập lại |

### 2.2. Cart State Partitions
| Partition ID | Input Domain | Class Type | Description / Value | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| VP-MCART-002 | Cart Items | Valid | Giỏ hàng chứa ít nhất 1 sản phẩm hợp lệ, còn tồn kho | Cho phép tiến hành thanh toán |
| IP-MCART-003 | Cart Items | Invalid | Giỏ hàng rỗng (`cart.length = 0`) | Chặn nút đặt hàng hoặc báo lỗi không thể đặt hàng |
| IP-MCART-004 | Cart Items | Invalid | Sản phẩm trong giỏ không còn tồn tại trên server | Báo lỗi sản phẩm không tồn tại, cập nhật lại giỏ |
| IP-MCART-005 | Cart Items | Invalid | Số lượng sản phẩm vượt quá tồn kho của cửa hàng | Báo lỗi vượt quá tồn kho, không cho đặt hàng |

### 2.3. Cart Quantity Partitions
| Partition ID | Input Domain | Class Type | Description / Value | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| VP-MCART-003 | Product Quantity | Valid | Số nguyên dương nằm trong khoảng [1, tồn kho] | Cập nhật số lượng thành công, tính lại tổng tiền đúng |
| IP-MCART-006 | Product Quantity | Invalid | Số lượng = 0 | Yêu cầu nhập số lớn hơn 0 hoặc đề xuất xóa sản phẩm |
| IP-MCART-007 | Product Quantity | Invalid | Số âm (ví dụ: -5) | Từ chối cập nhật, đưa về giá trị mặc định (1) |
| IP-MCART-008 | Product Quantity | Invalid | Số thập phân (ví dụ: 1.5) | Chỉ nhận phần nguyên hoặc báo lỗi dữ liệu không hợp lệ |
| IP-MCART-009 | Product Quantity | Invalid | Ký tự chữ hoặc đặc biệt (ví dụ: "abc", "@#$") | Từ chối hoặc tự động đưa về giá trị mặc định (1) |

### 2.4. Shipping Information Partitions (Profile data)
| Partition ID | Input Domain | Class Type | Description / Value | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| VP-MCART-004 | Full Name | Valid | Chuỗi ký tự không rỗng, độ dài hợp lệ [2, 50] | Chấp nhận và lưu thông tin giao hàng |
| IP-MCART-010 | Full Name | Invalid | Bỏ trống hoặc chỉ chứa khoảng trắng | Báo lỗi Họ tên bắt buộc và không hợp lệ |
| IP-MCART-011 | Full Name | Invalid | Độ dài quá dài (> 50 ký tự) | Báo lỗi Họ tên không vượt quá 50 ký tự |
| VP-MCART-005 | Phone Number | Valid | 9-10 chữ số bắt đầu bằng các đầu số hợp lệ (ví dụ: 912345678) | Chấp nhận số điện thoại |
| IP-MCART-012 | Phone Number | Invalid | Bỏ trống số điện thoại | Báo lỗi Số điện thoại bắt buộc |
| IP-MCART-013 | Phone Number | Invalid | Sai độ dài (8 chữ số hoặc 11 chữ số) | Báo lỗi độ dài SĐT không đúng 9-10 chữ số |
| IP-MCART-014 | Phone Number | Invalid | Chứa chữ cái hoặc ký tự đặc biệt | Báo lỗi định dạng SĐT |
| IP-MCART-015 | Phone Number | Invalid | Số điện thoại bắt đầu bằng số 0 (ví dụ: 0912345678) | Hệ thống phải chấp nhận ở Việt Nam (nhưng regex SUT đang bị lỗi chặn đầu số 0) |
| VP-MCART-006 | Address | Valid | Chuỗi không rỗng, độ dài hợp lệ [5, 255] | Chấp nhận địa chỉ giao hàng |
| IP-MCART-016 | Address | Invalid | Bỏ trống hoặc chỉ chứa khoảng trắng | Báo lỗi Địa chỉ bắt buộc |
| IP-MCART-017 | Address | Invalid | Quá ngắn (< 5 ký tự) | Báo lỗi địa chỉ quá ngắn, cần chi tiết hơn |
| IP-MCART-018 | Address | Invalid | Quá dài (> 255 ký tự) | Báo lỗi địa chỉ không vượt quá 255 ký tự |

### 2.5. Checkout API Security & Behavior Partitions
| Partition ID | Input Domain | Class Type | Description / Value | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| VP-MCART-007 | Order Creation | Valid | Gửi yêu cầu checkout hợp lệ 1 lần | Tạo đơn hàng thành công, làm trống giỏ hàng |
| IP-MCART-019 | Double Click | Invalid | Bấm nút đặt hàng nhiều lần liên tiếp cực nhanh | Hệ thống chặn yêu cầu trùng lặp, chỉ tạo 1 đơn hàng duy nhất |
| IP-MCART-020 | Price Tampering | Invalid | Gửi request API `POST /api/checkout` sửa đổi `total_amount` sai lệch | Backend từ chối đặt hàng, yêu cầu tính lại tổng tiền đúng |

---

## 3. Domain Test Cases List
All test cases are detailed in separate files in [tests/test-cases/mobile-cart/](../../tests/test-cases/mobile-cart):

- [TC-MOBILE-CART-DT-001: Đặt hàng thành công trên Mobile với giỏ hàng có 1 sản phẩm hợp lệ](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-001.md)
- [TC-MOBILE-CART-DT-002: Đặt hàng thành công trên Mobile với giỏ hàng có nhiều sản phẩm khác loại](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-002.md)
- [TC-MOBILE-CART-DT-003: Chặn truy cập màn hình Checkout khi người dùng chưa đăng nhập (Guest)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-003.md)
- [TC-MOBILE-CART-DT-004: Chặn truy cập màn hình Checkout khi giỏ hàng trống](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-004.md)
- [TC-MOBILE-CART-DT-005: Đặt hàng thất bại khi Token đăng nhập hết hạn hoặc sai chữ ký](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-005.md)
- [TC-MOBILE-CART-DT-006: Thêm trùng sản phẩm vào giỏ hàng trên mobile phải cộng dồn số lượng](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-006.md)
- [TC-MOBILE-CART-DT-007: Cập nhật tăng số lượng trực tiếp trong giỏ hàng thành công](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-007.md)
- [TC-MOBILE-CART-DT-008: Cập nhật giảm số lượng trực tiếp trong giỏ hàng thành công](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-008.md)
- [TC-MOBILE-CART-DT-009: Xóa sản phẩm khỏi giỏ hàng trên mobile thành công](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-009.md)
- [TC-MOBILE-CART-DT-010: Cập nhật số lượng về 0 hoặc số âm phải tự động đưa về 1 hoặc báo lỗi](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-010.md)
- [TC-MOBILE-CART-DT-011: Cập nhật số lượng bằng chữ hoặc ký tự đặc biệt trên mobile](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-011.md)
- [TC-MOBILE-CART-DT-012: Chặn đặt hàng khi sản phẩm trong giỏ hàng vượt quá số lượng tồn kho](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-012.md)
- [TC-MOBILE-CART-DT-013: Chặn cập nhật hồ sơ khi họ tên bị trống hoặc chỉ chứa khoảng trắng](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-013.md)
- [TC-MOBILE-CART-DT-014: Chặn cập nhật hồ sơ khi số điện thoại bị trống](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-014.md)
- [TC-MOBILE-CART-DT-015: Chặn cập nhật hồ sơ khi số điện thoại chứa chữ cái hoặc ký tự đặc biệt](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-015.md)
- [TC-MOBILE-CART-DT-016: Chặn cập nhật hồ sơ khi địa chỉ giao hàng bị trống hoặc chỉ khoảng trắng](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-016.md)
- [TC-MOBILE-CART-DT-017: Ngăn chặn tạo đơn hàng trùng lặp khi người dùng bấm nút đặt hàng nhiều lần liên tiếp](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-017.md)
- [TC-MOBILE-CART-DT-018: Backend kiểm tra và từ chối đặt hàng khi đơn giá hoặc tổng tiền bị thay đổi bất thường (Price Tampering)](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-018.md)
- [TC-MOBILE-CART-DT-019: Đặt hàng thành công nhưng kiểm tra tính toàn vẹn của địa chỉ giao hàng trong CSDL orders](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-019.md)
