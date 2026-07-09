# Master Bug Report

Tài liệu tổng hợp danh sách toàn bộ lỗi phát hiện được trong quá trình kiểm thử hệ thống thương mại điện tử EShop đối với các Module: Đăng nhập & Khóa tài khoản (FR-02), Giỏ hàng (FR-07), Dashboard Admin (FR-13) và Mobile Cart & Checkout (FR-21).

---

## 1. Summary of Login Bugs (FR-02)

| Bug ID | Title | Severity | Priority | Related Test Case | GitHub Issue |
|---|---|---|---|---|---|
| BUG-FR02-A-01 | Bộ đếm đăng nhập sai tăng thêm 2 đơn vị thay vì 1 | Major | High | [`TC-LOGIN-002`](tests/test-cases/login/TC-LOGIN-002.md), [`TC-LOGIN-023`](tests/test-cases/login/TC-LOGIN-023.md) | [Issue #31](https://github.com/trngnneee/eshop-sut/issues/31) |
| BUG-FR02-A-02 | Thời gian khóa tài khoản bị thiết lập sai thành 3 phút | Medium | High | [`TC-LOGIN-003`](tests/test-cases/login/TC-LOGIN-003.md), [`TC-LOGIN-014`](tests/test-cases/login/TC-LOGIN-014.md), [`TC-LOGIN-025`](tests/test-cases/login/TC-LOGIN-025.md) | [Issue #32](https://github.com/trngnneee/eshop-sut/issues/32) |
| BUG-FR02-A-03 | Race condition do xử lý yêu cầu đăng nhập bất đồng bộ | Major | High | [`TC-LOGIN-002`](tests/test-cases/login/TC-LOGIN-002.md), [`TC-LOGIN-013`](tests/test-cases/login/TC-LOGIN-013.md), [`TC-LOGIN-023`](tests/test-cases/login/TC-LOGIN-023.md), [`TC-LOGIN-024`](tests/test-cases/login/TC-LOGIN-024.md) | [Issue #33](https://github.com/trngnneee/eshop-sut/issues/33) |
| BUG-FR02-A-04 | Tiêu đề trang Đăng nhập hiển thị sai thành "Đăng Ký" | Minor | Medium | [`TC-LOGIN-004`](tests/test-cases/login/TC-LOGIN-004.md) | [Issue #34](https://github.com/trngnneee/eshop-sut/issues/34) |
| BUG-FR02-A-05 | Trường nhập Email hiển thị nhãn là "Username" | Minor | Medium | [`TC-LOGIN-004`](tests/test-cases/login/TC-LOGIN-004.md) | [Issue #35](https://github.com/trngnneee/eshop-sut/issues/35) |
| BUG-FR02-A-06 | Nút submit biểu mẫu sử dụng tiếng Anh "Sign In" | Minor | Medium | [`TC-LOGIN-004`](tests/test-cases/login/TC-LOGIN-004.md) | [Issue #36](https://github.com/trngnneee/eshop-sut/issues/36) |
| BUG-FR02-A-07 | Mật khẩu hiển thị ở dạng plain text (type="text") | Critical | High | [`TC-LOGIN-004`](tests/test-cases/login/TC-LOGIN-004.md) | [Issue #37](https://github.com/trngnneee/eshop-sut/issues/37) |
| BUG-FR02-A-08 | Thiếu dấu hoa thị màu đỏ * đánh dấu trường bắt buộc | Cosmetic | Low | [`TC-LOGIN-004`](tests/test-cases/login/TC-LOGIN-004.md) | [Issue #38](https://github.com/trngnneee/eshop-sut/issues/38) |
| BUG-FR02-A-09 | Thiếu trim khoảng trắng của Email ở phía Backend | Medium | Medium | [`TC-LOGIN-005`](tests/test-cases/login/TC-LOGIN-005.md) | [Issue #39](https://github.com/trngnneee/eshop-sut/issues/39) |
| BUG-FR02-A-10 | Không tích hợp cơ chế Rate Limiting chống tấn công Brute-force | High | High | [`TC-LOGIN-008`](tests/test-cases/login/TC-LOGIN-008.md) | [Issue #40](https://github.com/trngnneee/eshop-sut/issues/40) |
| BUG-FR02-A-11 | Nút submit không hiển thị Loading và không bị khóa khi đang xử lý | Minor | Medium | [`TC-LOGIN-009`](tests/test-cases/login/TC-LOGIN-009.md) | [Issue #41](https://github.com/trngnneee/eshop-sut/issues/41) |
| BUG-FR02-A-12 | Không có nút Toggle ẩn/hiện mật khẩu trên biểu mẫu | Cosmetic | Low | [`TC-LOGIN-010`](tests/test-cases/login/TC-LOGIN-010.md) | [Issue #42](https://github.com/trngnneee/eshop-sut/issues/42) |
| BUG-FR02-A-13 | Token JWT không có thời hạn hết hạn (vô hạn hạn) | High | High | [`TC-LOGIN-011`](tests/test-cases/login/TC-LOGIN-011.md) | [Issue #43](https://github.com/trngnneee/eshop-sut/issues/43) |
| BUG-FR02-A-14 | Thiếu Route Guard ngăn truy cập lại trang Login khi đã đăng nhập | Medium | Medium | [`TC-LOGIN-012`](tests/test-cases/login/TC-LOGIN-012.md) | [Issue #44](https://github.com/trngnneee/eshop-sut/issues/44) |
| BUG-FR02-A-15 | Giao diện đăng nhập Admin thiếu nhãn thông tin, thiếu dấu * bắt buộc và nút hiện mật khẩu | Major | High | [`TC-LOGIN-013`](tests/test-cases/login/TC-LOGIN-013.md) | [Issue #45](https://github.com/trngnneee/eshop-sut/issues/45) |
| BUG-FR02-A-16 | Thông báo lỗi đăng nhập Admin sử dụng alert() gây hiển thị chữ "Code" và vi phạm vị trí thông báo | Major | Medium | [`TC-LOGIN-004`](tests/test-cases/login/TC-LOGIN-004.md), [`TC-LOGIN-020`](tests/test-cases/login/TC-LOGIN-020.md), [`TC-LOGIN-021`](tests/test-cases/login/TC-LOGIN-021.md) | [Issue #46](https://github.com/trngnneee/eshop-sut/issues/46) |
| BUG-FR02-A-17 | Đặt lại mật khẩu thành công không giải phóng trạng thái khóa tài khoản và không reset bộ đếm lần đăng nhập sai | Major | High | [`TC-LOGIN-004`](tests/test-cases/login/TC-LOGIN-004.md) | [Issue #47](https://github.com/trngnneee/eshop-sut/issues/47) |
| BUG-FR02-A-18 | Giao diện đăng nhập Frontend che khuất lỗi khóa tài khoản (luôn hiện thông báo lỗi tĩnh) | Major | High | [`TC-ERR-003`](tests/test-cases/login/TC-ERR-003.md) | [Issue #48](https://github.com/trngnneee/eshop-sut/issues/48) |
| BUG-FR02-A-19 | API và giao diện thiếu cảnh báo số lần đăng nhập sai còn lại trước khi khóa | Major | Medium | [`TC-LOGIN-030`](tests/test-cases/login/TC-LOGIN-030.md) | [Issue #49](https://github.com/trngnneee/eshop-sut/issues/49) |

---

## 2. Summary of Cart Bugs (FR-07)

| Bug ID | Title | Severity | Priority | Related Test Case | GitHub Issue |
|---|---|---|---|---|---|
| BUG-FR07-B-01 | Backend API không validate số lượng sản phẩm thêm vào giỏ hàng | Major | High | [`TC-CART-044`](tests/test-cases/cart/TC-CART-044.md), [`TC-CART-045`](tests/test-cases/cart/TC-CART-045.md), [`TC-CART-046`](tests/test-cases/cart/TC-CART-046.md), [`TC-CART-047`](tests/test-cases/cart/TC-CART-047.md) | [Issue #128](https://github.com/trngnneee/eshop-sut/issues/128) |
| BUG-FR07-B-02 | Backend API không cộng dồn số lượng cho sản phẩm trùng ID | Major | High | [`TC-CART-043`](tests/test-cases/cart/TC-CART-043.md) | [Issue #129](https://github.com/trngnneee/eshop-sut/issues/129) |
| BUG-FR07-B-03 | Frontend CartContext không cộng dồn số lượng khi thêm sản phẩm trùng | Major | High | [`TC-CART-012`](tests/test-cases/cart/TC-CART-012.md) | [Issue #130](https://github.com/trngnneee/eshop-sut/issues/130) |
| BUG-FR07-B-04 | Trang giỏ hàng thiếu nút tăng giảm số lượng (+/-) và nhập số lượng trực tiếp | Major | High | [`TC-CART-015`](tests/test-cases/cart/TC-CART-015.md), [`TC-CART-016`](tests/test-cases/cart/TC-CART-016.md), [`TC-CART-017`](tests/test-cases/cart/TC-CART-017.md), [`TC-CART-018`](tests/test-cases/cart/TC-CART-018.md), [`TC-CART-019`](tests/test-cases/cart/TC-CART-019.md), [`TC-CART-020`](tests/test-cases/cart/TC-CART-020.md), [`TC-CART-021`](tests/test-cases/cart/TC-CART-021.md), [`TC-CART-022`](tests/test-cases/cart/TC-CART-022.md), [`TC-CART-023`](tests/test-cases/cart/TC-CART-023.md), [`TC-CART-024`](tests/test-cases/cart/TC-CART-024.md), [`TC-CART-025`](tests/test-cases/cart/TC-CART-025.md) | [Issue #131](https://github.com/trngnneee/eshop-sut/issues/131) |
| BUG-FR07-B-05 | Thiếu Confirm Dialog xác nhận khi xóa sản phẩm khỏi giỏ hàng | Minor | Medium | [`TC-CART-031`](tests/test-cases/cart/TC-CART-031.md), [`TC-CART-032`](tests/test-cases/cart/TC-CART-032.md), [`TC-CART-033`](tests/test-cases/cart/TC-CART-033.md), [`TC-CART-075`](tests/test-cases/cart/TC-CART-075.md) | [Issue #132](https://github.com/trngnneee/eshop-sut/issues/132) |
| BUG-FR07-B-06 | Nhãn hiển thị tổng tiền không đúng đặc tả ('Tổng tạm tính' thay vì 'Tổng cộng') | Minor | Low | [`TC-CART-009`](tests/test-cases/cart/TC-CART-009.md) | [Issue #133](https://github.com/trngnneee/eshop-sut/issues/133) |
| BUG-FR07-B-07 | Trạng thái giỏ hàng trống thiếu hình ảnh/icon minh họa trực quan | Minor | Low | [`TC-CART-002`](tests/test-cases/cart/TC-CART-002.md) | [Issue #134](https://github.com/trngnneee/eshop-sut/issues/134) |
| BUG-FR07-B-08 | Trang giỏ hàng thiếu thanh breadcrumb điều hướng | Minor | Low | [`TC-CART-004`](tests/test-cases/cart/TC-CART-004.md) | [Issue #135](https://github.com/trngnneee/eshop-sut/issues/135) |
| BUG-FR07-B-09 | Không cần đăng nhập vẫn cho phép thêm sản phẩm vào giỏ hàng | Major | High | [`TC-CART-047`](tests/test-cases/cart/TC-CART-047.md) | [Issue #136](https://github.com/trngnneee/eshop-sut/issues/136) |
| BUG-FR07-B-10 | Backend API không validate tính toàn vẹn của sản phẩm thêm vào giỏ hàng | Major | High | [`TC-CART-051`](tests/test-cases/cart/TC-CART-051.md), [`TC-CART-053`](tests/test-cases/cart/TC-CART-053.md), [`TC-CART-057`](tests/test-cases/cart/TC-CART-057.md), [`TC-CART-058`](tests/test-cases/cart/TC-CART-058.md), [`TC-CART-059`](tests/test-cases/cart/TC-CART-059.md) | [Issue #137](https://github.com/trngnneee/eshop-sut/issues/137) |
| BUG-FR07-B-11 | Thiếu thông báo phản hồi (toast/alert) khi thêm sản phẩm vào giỏ hàng thành công | Minor | Medium | [`TC-CART-010`](tests/test-cases/cart/TC-CART-010.md), [`TC-CART-011`](tests/test-cases/cart/TC-CART-011.md), [`TC-CART-038`](tests/test-cases/cart/TC-CART-038.md), [`TC-CART-074`](tests/test-cases/cart/TC-CART-074.md) | [Issue #138](https://github.com/trngnneee/eshop-sut/issues/138) |
| BUG-FR07-B-12 | Không hiển thị số lượng hàng tồn kho khả dụng và thiếu cảnh báo khi số lượng vượt quá hàng tồn | Major | High | [`TC-CART-060`](tests/test-cases/cart/TC-CART-060.md), [`TC-CART-079`](tests/test-cases/cart/TC-CART-079.md) | [Issue #139](https://github.com/trngnneee/eshop-sut/issues/139) |
| BUG-FR07-B-13 | Backend API cho phép giả mạo đơn giá của sản phẩm (Price Tampering) | Critical | High | [`TC-CART-063`](tests/test-cases/cart/TC-CART-063.md), [`TC-CART-064`](tests/test-cases/cart/TC-CART-064.md), [`TC-CART-080`](tests/test-cases/cart/TC-CART-080.md) | [Issue #140](https://github.com/trngnneee/eshop-sut/issues/140) |
| BUG-FR07-B-14 | Backend API chấp nhận productId không tồn tại và tạo ra sản phẩm ma | Major | High | [`TC-CART-061`](tests/test-cases/cart/TC-CART-061.md), [`TC-CART-062`](tests/test-cases/cart/TC-CART-062.md), [`TC-CART-078`](tests/test-cases/cart/TC-CART-078.md) | [Issue #141](https://github.com/trngnneee/eshop-sut/issues/141) |
| BUG-FR07-B-15 | Backend API không kiểm tra kiểu dữ liệu của trường quantity (Type Validation) | Major | High | [`TC-CART-065`](tests/test-cases/cart/TC-CART-065.md), [`TC-CART-066`](tests/test-cases/cart/TC-CART-066.md), [`TC-CART-067`](tests/test-cases/cart/TC-CART-067.md), [`TC-CART-068`](tests/test-cases/cart/TC-CART-068.md) | [Issue #142](https://github.com/trngnneee/eshop-sut/issues/142) |
| BUG-FR07-B-16 | Lỗ hổng cho phép gán thuộc tính đặc quyền (Mass Assignment / Extra Fields) | Major | High | [`TC-CART-070`](tests/test-cases/cart/TC-CART-070.md) | [Issue #143](https://github.com/trngnneee/eshop-sut/issues/143) |
| BUG-FR07-B-17 | Giao diện cho phép thanh toán (Checkout) khi giỏ hàng trống | Major | Medium | [`TC-CART-076`](tests/test-cases/cart/TC-CART-076.md), [`TC-CART-077`](tests/test-cases/cart/TC-CART-077.md) | [Issue #144](https://github.com/trngnneee/eshop-sut/issues/144) |
| BUG-FR07-B-18 | Thiếu xử lý lỗi kết nối mạng hoặc sập máy chủ trên giao diện | Major | Medium | [`TC-CART-088`](tests/test-cases/cart/TC-CART-088.md) | [Issue #145](https://github.com/trngnneee/eshop-sut/issues/145) |
| BUG-FR07-B-19 | Giỏ hàng không được làm sạch sau khi thanh toán thành công (checkout success) | Major | High | [`TC-CART-089`](tests/test-cases/cart/TC-CART-089.md) | [Issue #167](https://github.com/trngnneee/eshop-sut/issues/167) |

---

## 3. Detailed Bug Reports

### BUG-FR02-A-01: Bộ đếm đăng nhập sai tăng thêm 2 đơn vị thay vì 1

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-002, TC-LOGIN-023`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Hệ thống SUT Backend và Frontend đang hoạt động bình thường.
* **Steps to Reproduce:**
  1. Đăng ký một tài khoản mới hợp lệ.
  2. Gửi một yêu cầu POST đăng nhập sai mật khẩu tới `/api/login` với tài khoản vừa tạo.
  3. Kiểm tra trường `login_attempts` trong cơ sở dữ liệu hoặc thực hiện đăng nhập sai tiếp theo để quan sát thời điểm bị khóa.
* **Expected Result:**
  * Bộ đếm lần đăng nhập sai của tài khoản phải tăng thêm đúng 1 đơn vị sau mỗi lần đăng nhập thất bại.
* **Actual Result:**
  * Bộ đếm tăng thêm 2 đơn vị sau mỗi lần đăng nhập sai, dẫn đến việc tài khoản bị tạm khóa sớm hơn quy định.
* **Impact:**
  * Người dùng bị khóa tài khoản nhanh hơn thiết kế nghiệp vụ (chỉ cần nhập sai 2 lần là bị khóa thay vì 3 lần).
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-01.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/31
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-002, TC-LOGIN-023`
  * Điều kiện retest: Bản vá sửa lỗi tăng bộ đếm được cập nhật trên Backend.
  * Expected retest result: Đăng nhập sai 1 lần chỉ tăng bộ đếm lên 1.

---

### BUG-FR02-A-02: Thời gian khóa tài khoản bị thiết lập sai thành 3 phút

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-003, TC-LOGIN-014, TC-LOGIN-025`
* **Severity / Priority:** Medium / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Tài khoản người dùng đã tồn tại trong hệ thống.
* **Steps to Reproduce:**
  1. Thực hiện đăng nhập sai mật khẩu liên tiếp cho đến khi tài khoản bị tạm khóa.
  2. Đo khoảng thời gian từ khi bị khóa cho đến khi hệ thống tự động mở khóa và chấp nhận thông tin đăng nhập đúng.
* **Expected Result:**
  * Trong môi trường demo, thời gian tạm khóa tài khoản phải là đúng 30 giây.
* **Actual Result:**
  * Tài khoản bị khóa trong thời gian thực tế là 180 giây (3 phút) trước khi có thể thử lại.
* **Impact:**
  * Thời gian khóa quá lâu gây gián đoạn lớn và khó chịu cho người dùng khi vô tình nhập sai thông tin.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-02.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/32
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-003, TC-LOGIN-014, TC-LOGIN-025`
  * Điều kiện retest: Tham số thời gian khóa trong cơ sở dữ liệu/backend được cấu hình lại thành 30 giây.
  * Expected retest result: Tài khoản tự động mở khóa và đăng nhập được bình thường sau 30 giây.

---

### BUG-FR02-A-03: Race condition do xử lý yêu cầu đăng nhập bất đồng bộ

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-002, TC-LOGIN-013, TC-LOGIN-023, TC-LOGIN-024`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Tài khoản người dùng đang hoạt động bình thường.
* **Steps to Reproduce:**
  1. Sử dụng công cụ kiểm thử hiệu năng hoặc gửi nhanh nhiều yêu cầu đăng nhập sai mật khẩu liên tiếp đồng thời (Race Condition).
  2. Kiểm tra xem tài khoản có thể thực hiện nhiều hơn 3 lần đăng nhập sai mà không bị khóa ngay lập tức hay không.
* **Expected Result:**
  * Hệ thống phải xử lý tuần tự hoặc có cơ chế khóa giao dịch để đảm bảo tài khoản bị khóa chính xác sau lần đăng nhập sai thứ 3, bất kể tốc độ gửi yêu cầu.
* **Actual Result:**
  * API backend trả về phản hồi đăng nhập trước khi cập nhật xong trạng thái đếm trong cơ sở dữ liệu, cho phép gửi nhiều yêu cầu trước khi tài khoản bị khóa thực tế.
* **Impact:**
  * Kẻ tấn công có thể brute-force mật khẩu với số lượng lớn bằng cách gửi các yêu cầu bất đồng bộ song song.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-03.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/33
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-002, TC-LOGIN-013, TC-LOGIN-023, TC-LOGIN-024`
  * Điều kiện retest: Áp dụng cơ chế xử lý đồng bộ hoặc khóa dữ liệu (database lock) when cập nhật bộ đếm đăng nhập sai.
  * Expected retest result: Hệ thống khóa tài khoản chính xác ở lần thứ 3, các yêu cầu song song sau đó bị chặn bằng HTTP 403.

---

### BUG-FR02-A-04: Tiêu đề trang Đăng nhập hiển thị sai thành "Đăng Ký"

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-004`
* **Severity / Priority:** Minor / Medium
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Giao diện người dùng đang hoạt động.
* **Steps to Reproduce:**
  1. Truy cập vào trang Đăng nhập (`/login`) trên trình duyệt Web.
  2. Quan sát tiêu đề chính (thẻ `<h2>` hoặc `<h1>`) của biểu mẫu đăng nhập.
* **Expected Result:**
  * Tiêu đề của trang đăng nhập phải hiển thị là "Đăng nhập".
* **Actual Result:**
  * Tiêu đề trang hiển thị sai thành "Đăng Ký".
* **Impact:**
  * Gây hiểu lầm lớn cho người dùng về chức năng hiện tại của trang.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-04.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/34
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-004`
  * Điều kiện retest: Thay đổi thẻ văn bản tiêu đề trong mã nguồn React của trang Đăng nhập.
  * Expected retest result: Tiêu đề hiển thị chính xác chữ "Đăng nhập".

---

### BUG-FR02-A-05: Trường nhập Email hiển thị nhãn là "Username"

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-004`
* **Severity / Priority:** Minor / Medium
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Truy cập vào trang `/login`.
* **Steps to Reproduce:**
  1. Mở trang đăng nhập `/login` trên trình duyệt.
  2. Quan sát nhãn (label) hoặc văn bản gợi ý (placeholder) của ô nhập tài khoản.
* **Expected Result:**
  * Nhãn hiển thị của trường nhập địa chỉ email phải là "Email" hoặc "Địa chỉ Email".
* **Actual Result:**
  * Nhãn hiển thị của trường nhập địa chỉ email là "Username".
* **Impact:**
  * Người dùng có thể nhầm lẫn rằng hệ thống yêu cầu nhập tên đăng nhập tự tạo thay vì địa chỉ email đã đăng ký.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-05.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/35
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-004`
  * Điều kiện retest: Đổi nội dung nhãn thành "Email" trong tệp tin JSX tương ứng.
  * Expected retest result: Nhãn hiển thị chính xác là "Email".

---

### BUG-FR02-A-06: Nút submit biểu mẫu sử dụng tiếng Anh "Sign In"

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-004`
* **Severity / Priority:** Minor / Medium
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Truy cập vào trang `/login`.
* **Steps to Reproduce:**
  1. Mở trang đăng nhập `/login` trên trình duyệt.
  2. Quan sát nút gửi biểu mẫu (submit button) ở cuối form.
* **Expected Result:**
  * Nút bấm xác nhận gửi thông tin đăng nhập phải hiển thị ngôn ngữ tiếng Việt là "Đăng nhập".
* **Actual Result:**
  * Nút bấm hiển thị ngôn ngữ tiếng Anh là "Sign In".
* **Impact:**
  * Vi phạm quy định nhất quán ngôn ngữ tiếng Việt trên toàn bộ giao diện của hệ thống.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-06.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/36
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-004`
  * Điều kiện retest: Thay đổi văn bản trên nút bấm thành "Đăng nhập".
  * Expected retest result: Nút hiển thị chữ "Đăng nhập" bằng tiếng Việt.

---

### BUG-FR02-A-07: Mật khẩu hiển thị ở dạng plain text (type="text")

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-004`
* **Severity / Priority:** Critical / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Đang ở trang đăng nhập `/login`.
* **Steps to Reproduce:**
  1. Nhập bất kỳ chuỗi ký tự nào vào ô Mật khẩu.
  2. Quan sát các ký tự vừa nhập hiển thị trên màn hình.
* **Expected Result:**
  * Ô nhập mật khẩu phải ẩn ký tự dưới dạng dấu chấm hoặc dấu hoa thị để bảo mật thông tin.
* **Actual Result:**
  * Trường nhập mật khẩu cấu hình thuộc tính `type="text"`, làm lộ mật khẩu rõ ràng trên màn hình.
* **Impact:**
  * Rò rỉ thông tin đăng nhập nhạy cảm của người dùng cho người xung quanh (shoulder surfing).
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-07.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/37
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-004`
  * Điều kiện retest: Thay đổi thuộc tính ô nhập liệu thành `type="password"`.
  * Expected retest result: Ký tự mật khẩu được ẩn tự động khi nhập.

---

### BUG-FR02-A-08: Thiếu dấu hoa thị màu đỏ * đánh dấu trường bắt buộc

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-004`
* **Severity / Priority:** Cosmetic / Low
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Giao diện đăng nhập đang hiển thị.
* **Steps to Reproduce:**
  1. Quan sát nhãn của trường Email và Mật khẩu trên biểu mẫu.
* **Expected Result:**
  * Các trường bắt buộc nhập phải có dấu hoa thị màu đỏ `*` cạnh nhãn.
* **Actual Result:**
  * Thiếu hoàn toàn dấu hoa thị màu đỏ cảnh báo tính bắt buộc nhập.
* **Impact:**
  * Giảm trải nghiệm người dùng, không cung cấp đủ chỉ dẫn nhập liệu.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-08.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/38
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-004`
  * Điều kiện retest: Thêm ký tự `*` màu đỏ vào cạnh nhãn label của các trường bắt buộc trong mã CSS/HTML.
  * Expected retest result: Dấu hoa thị màu đỏ hiển thị rõ ràng cạnh nhãn.

---

### BUG-FR02-A-09: Thiếu trim khoảng trắng của Email ở phía Backend

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-005`
* **Severity / Priority:** Medium / Medium
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Tài khoản `test@eshop.com` đã được đăng ký thành công.
* **Steps to Reproduce:**
  1. Nhập email đăng nhập có chứa khoảng trắng thừa ở đầu hoặc cuối (ví dụ: ` test@eshop.com `) và mật khẩu đúng.
  2. Nhấn nút "Đăng nhập".
* **Expected Result:**
  * Hệ thống phải tự động loại bỏ khoảng trắng và thực hiện đăng nhập thành công.
* **Actual Result:**
  * Backend API từ chối đăng nhập do so khớp nguyên bản cả khoảng trắng, báo lỗi thông tin tài khoản không chính xác.
* **Impact:**
  * Người dùng thường xuyên copy-paste email có lẫn khoảng trắng sẽ không thể đăng nhập được và không hiểu nguyên nhân.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-09.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/39
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-005`
  * Điều kiện retest: Bổ sung phương thức `.trim()` cho chuỗi email nhận được tại controller xử lý đăng nhập phía Backend SUT.
  * Expected retest result: Đăng nhập thành công khi email có chứa khoảng trắng thừa.

---

### BUG-FR02-A-10: Không tích hợp cơ chế Rate Limiting chống tấn công Brute-force

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-008`
* **Severity / Priority:** High / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Hệ thống đang chạy.
* **Steps to Reproduce:**
  1. Sử dụng công cụ kiểm thử bảo mật gửi liên tục 20 request đăng nhập sai tới API `/api/login` trong vòng 1 giây.
  2. Quan sát phản hồi lỗi từ API.
* **Expected Result:**
  * API phải chặn các yêu cầu có tần suất quá cao từ một nguồn bằng mã lỗi `429 Too Many Requests`.
* **Actual Result:**
  * API xử lý tất cả các yêu cầu và trả về mã lỗi `401 Unauthorized` bình thường mà không kích hoạt bất kỳ cơ chế giới hạn nào.
* **Impact:**
  * Hệ thống dễ bị quá tải (DoS) hoặc bị dò quét mật khẩu Brute-force với số lượng lớn tài khoản đồng thời.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-10.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/40
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-008`
  * Điều kiện retest: Tích hợp thư viện Rate Limiter (ví dụ: `express-rate-limit`) vào API đăng nhập.
  * Expected retest result: Gửi nhiều yêu cầu liên tiếp sẽ nhận phản hồi HTTP 429.

---

### BUG-FR02-A-11: Nút submit không hiển thị Loading và không bị khóa khi đang xử lý

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-009`
* **Severity / Priority:** Minor / Medium
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Ở trang đăng nhập.
* **Steps to Reproduce:**
  1. Nhập thông tin đăng nhập và nhấp nút "Đăng nhập".
  2. Trong thời gian chờ API phản hồi (có thể giả lập mạng chậm), bấm liên tiếp vào nút Đăng nhập.
* **Expected Result:**
  * Nút bấm phải đổi trạng thái sang loading và bị vô hiệu hóa (disabled = true) để tránh gửi trùng lặp dữ liệu.
* **Actual Result:**
  * Nút bấm giữ nguyên trạng thái và người dùng có thể nhấp liên tiếp nhiều lần để gửi nhiều request lên server.
* **Impact:**
  * Tạo ra các yêu cầu xử lý trùng lặp không đáng có lên server, gây ảnh hưởng hiệu năng.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-11.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/41
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-009`
  * Điều kiện retest: Cấu hình biến trạng thái `isLoading` để disable và hiển thị icon loading trên nút bấm của React component.
  * Expected retest result: Nút bị khóa khi đang xử lý gửi API.

---

### BUG-FR02-A-12: Không có nút Toggle ẩn/hiện mật khẩu trên biểu mẫu

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-010`
* **Severity / Priority:** Cosmetic / Low
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Đang ở trang đăng nhập.
* **Steps to Reproduce:**
  1. Quan sát góc bên phải của ô nhập mật khẩu trên trang đăng nhập.
* **Expected Result:**
  * Phải có nút bấm hoặc icon hình con mắt để người dùng chọn ẩn/hiện mật khẩu.
* **Actual Result:**
  * Không có nút bấm hoặc icon hỗ trợ ẩn/hiện mật khẩu.
* **Impact:**
  * Người dùng khó tự kiểm tra xem mình có nhập sai ký tự mật khẩu hay không.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-12.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/42
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-010`
  * Điều kiện retest: Bổ sung icon toggle và cập nhật state thay đổi `type="password"` thành `type="text"` trong React.
  * Expected retest result: Icon mắt xuất hiện và hoạt động ẩn/hiện mật khẩu tốt.

---

### BUG-FR02-A-13: Token JWT không có thời hạn hết hạn (vô hạn hạn)

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-011`
* **Severity / Priority:** High / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Tài khoản đã đăng nhập thành công.
* **Steps to Reproduce:**
  1. Thực hiện đăng nhập thành công để nhận chuỗi JWT token từ response.
  2. Copy chuỗi token và giải mã (decode) bằng công cụ để kiểm tra trường thời gian hết hạn (`exp`).
* **Expected Result:**
  * Token JWT phải có trường `exp` quy định thời gian hết hạn cụ thể để bảo mật phiên đăng nhập.
* **Actual Result:**
  * Token JWT không chứa thuộc tính `exp`, cho phép truy cập vĩnh viễn mà không bao giờ hết hạn.
* **Impact:**
  * Rủi ro bảo mật cực cao nếu token bị đánh cắp, kẻ xấu có thể duy trì quyền truy cập trái phép vô thời hạn.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-13.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/43
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-011`
  * Điều kiện retest: Thêm tham số `{ expiresIn: '24h' }` trong hàm `jwt.sign()` ở backend.
  * Expected retest result: Token giải mã chứa trường `exp` hợp lệ.

---

### BUG-FR02-A-14: Thiếu Route Guard ngăn truy cập lại trang Login khi đã đăng nhập

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-012`
* **Severity / Priority:** Medium / Medium
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Người dùng đã đăng nhập và lưu token.
* **Steps to Reproduce:**
  1. Thực hiện đăng nhập vào hệ thống thành công.
  2. Gõ trực tiếp địa chỉ `/login` trên thanh URL của trình duyệt và nhấn Enter.
* **Expected Result:**
  * Hệ thống phải tự động điều hướng người dùng đã đăng nhập về trang chủ hoặc trang cá nhân, không hiển thị lại form đăng nhập.
* **Actual Result:**
  * Trang đăng nhập vẫn hiển thị bình thường và cho phép thực hiện đăng nhập lại.
* **Impact:**
  * Gây trải nghiệm người dùng không tốt, không quản lý tốt trạng thái phiên làm việc của client.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-14.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/44
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-012`
  * Điều kiện retest: Áp dụng Route Guard kiểm tra trạng thái token trước khi cho phép render component Login.
  * Expected retest result: Hệ thống tự động chuyển hướng người dùng về trang chủ.

---

### BUG-FR02-A-15: Giao diện đăng nhập Admin thiếu nhãn thông tin, thiếu dấu * bắt buộc và nút hiện mật khẩu

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-013`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5174 (Web Admin)
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Giao diện Admin đang hoạt động.
* **Steps to Reproduce:**
  1. Truy cập trang đăng nhập Admin tại địa chỉ `http://localhost:5174/`.
  2. Quan sát thiết kế giao diện của biểu mẫu đăng nhập (thiếu nhãn, thiếu dấu hoa thị).
  3. Nhập dữ liệu và kiểm tra sự tồn tại của nút ẩn/hiện mật khẩu và ngôn ngữ nút submit.
* **Expected Result:**
  * Giao diện đăng nhập Admin phải hiển thị đầy đủ nhãn mô tả cho các trường nhập liệu, có dấu hoa thị đỏ `*` bắt buộc, nút Toggle ẩn/hiện mật khẩu, nút submit tiếng Việt "Đăng nhập" và trường Email có thuộc tính `type="email"`.
* **Actual Result:**
  * Giao diện Admin Login thiếu nhãn label bên ngoài (khiến placeholder biến mất khi nhập liệu), thiếu dấu hoa thị `*` bắt buộc, thiếu nút Toggle ẩn/hiện mật khẩu, nút submit hiển thị tiếng Anh `"Login"` và thiếu thuộc tính `type="email"` ở trường Email.
* **Impact:**
  * Vi phạm các quy chuẩn thiết kế UI/UX và cản trở việc quản lý tài khoản của Admin một cách thuận tiện.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-15.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/45
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-013`
  * Điều kiện retest: Cập nhật mã nguồn trang Đăng nhập Admin của dự án.
  * Expected retest result: Giao diện hiển thị đầy đủ nhãn mô tả, dấu hoa thị đỏ và nút ẩn/hiện hoạt động tốt.

---

### BUG-FR02-A-16: Thông báo lỗi đăng nhập Admin sử dụng alert() gây hiển thị chữ "Code" và vi phạm vị trí thông báo

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-004, TC-LOGIN-020, TC-LOGIN-021`
* **Severity / Priority:** Major / Medium
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5174 (Web Admin)
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Đang ở trang đăng nhập Admin.
* **Steps to Reproduce:**
  1. Truy cập trang đăng nhập Web Admin tại `http://localhost:5174/`.
  2. Nhập thông tin tài khoản sai (ví dụ: `wrong@eshop.com` / `WrongPass123`).
  3. Bấm nút submit.
  4. Quan sát hộp thoại thông báo lỗi hiện lên trên màn hình.
* **Expected Result:**
  * Khi đăng nhập thất bại ở trang Admin, thông báo lỗi phải hiển thị bằng văn bản phía trên nút submit thay vì dùng hộp thoại `alert()`.
* **Actual Result:**
  * Hệ thống sử dụng hộp thoại `alert()` mặc định của trình duyệt để hiển thị lỗi đăng nhập thất bại, gây mất mỹ quan và vi phạm đặc tả hiển thị lỗi của FR-22.
* **Impact:**
  * Giao diện thiếu chuyên nghiệp, phá vỡ cấu trúc trải nghiệm người dùng trên trang quản trị.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-16.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/46
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-004, TC-LOGIN-020, TC-LOGIN-021`
  * Điều kiện retest: Thay đổi logic bắt lỗi trong file React để cập nhật văn bản thông báo lỗi trên UI thay vì gọi `alert()`.
  * Expected retest result: Thông báo lỗi hiển thị dạng text ngay trên form đăng nhập.

---

### BUG-FR02-A-17: Đặt lại mật khẩu thành công không giải phóng trạng thái khóa tài khoản và không reset bộ đếm lần đăng nhập sai

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-004`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Tài khoản người dùng đang bị khóa do nhập sai nhiều lần.
* **Steps to Reproduce:**
  1. Nhập mật khẩu sai 3 lần liên tiếp để khóa tài khoản `test_tc31@eshop.com`.
  2. Thực hiện yêu cầu đặt lại mật khẩu thành công thông qua luồng OTP và API đặt lại mật khẩu mới.
  3. Thử thực hiện đăng nhập lại ngay lập tức bằng mật khẩu mới vừa tạo.
* **Expected Result:**
  * Đặt lại mật khẩu thành công phải tự động reset bộ đếm số lần đăng nhập sai về 0 và mở khóa tài khoản ngay lập tức.
* **Actual Result:**
  * Hệ thống cập nhật mật khẩu mới nhưng giữ nguyên trạng thái bị khóa của tài khoản, khiến người dùng vẫn bị khóa và báo lỗi tài khoản bị khóa.
* **Impact:**
  * Người dùng dù đã tự khôi phục mật khẩu thành công vẫn không thể truy cập tài khoản ngay lập tức, gây ức chế và tăng số lượng yêu cầu hỗ trợ kỹ thuật.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-17.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/47
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-004`
  * Điều kiện retest: Cập nhật hàm xử lý đặt lại mật khẩu ở backend để thiết lập lại các trường `login_attempts = 0` và `lock_until = null`.
  * Expected retest result: Đăng nhập thành công ngay lập tức bằng mật khẩu mới.

---

### BUG-FR02-A-18: Giao diện đăng nhập Frontend che khuất lỗi khóa tài khoản (luôn hiện thông báo lỗi tĩnh)

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-ERR-003`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Tài khoản đang bị khóa.
* **Steps to Reproduce:**
  1. Nhập mật khẩu sai 3 lần để tài khoản bị khóa.
  2. Thử đăng nhập lại bằng mật khẩu ĐÚNG hoặc SAI.
  3. Kiểm tra thông báo lỗi hiển thị trên giao diện đăng nhập Frontend Web.
* **Expected Result:**
  * Giao diện Frontend Web phải hiển thị chính xác thông báo lỗi khóa tài khoản nhận được từ Backend ("Tài khoản đã bị khóa...") để người dùng biết.
* **Actual Result:**
  * Giao diện Frontend Web bắt ngoại lệ và gán lỗi tĩnh cứng: `"Đăng nhập thất bại. Vui lòng kiểm tra lại."`, che khuất hoàn toàn thông tin tài khoản bị khóa.
* **Impact:**
  * Người dùng không biết tài khoản đã bị khóa, tiếp tục thử lại nhiều lần gây hoang mang.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-18.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/48
* **Retest Plan:**
  * Test case cần chạy lại: `TC-ERR-003`
  * Điều kiện retest: Cập nhật Frontend để hiển thị động thông điệp lỗi nhận từ API response (`err.response.data.error`).
  * Expected retest result: Màn hình đăng nhập hiển thị thông báo tài khoản bị khóa.

---

### BUG-FR02-A-19: API và giao diện thiếu cảnh báo số lần đăng nhập sai còn lại trước khi khóa

* **Feature:** FR-02 – Đăng nhập & Khóa tài khoản
* **Found by Test Case:** `TC-LOGIN-030`
* **Severity / Priority:** Major / Medium
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Hệ thống đang hoạt động.
* **Steps to Reproduce:**
  1. Đăng nhập sai mật khẩu lần 1 hoặc lần 2.
  2. Kiểm tra phản hồi JSON từ Backend API `/api/login` (không thấy trường thông tin số lần còn lại).
  3. Kiểm tra thông báo hiển thị trên Frontend Web (không có cảnh báo đếm ngược số lần thử).
* **Expected Result:**
  * API backend và giao diện phải hiển thị cảnh báo số lần đăng nhập sai còn lại (ví dụ: "Bạn còn 2 lần thử trước khi tài khoản bị khóa").
* **Actual Result:**
  * Hệ thống hoàn toàn thiếu cơ chế cảnh báo số lần đăng nhập sai còn lại. Khi người dùng nhập sai mật khẩu, API backend chỉ phản hồi lỗi chung `"Invalid email or password"`.
* **Impact:**
  * Người dùng không biết mình sắp bị khóa tài khoản để dừng lại hoặc cẩn thận hơn khi nhập liệu.
* **Evidence:**
  * Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-19.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/49
* **Retest Plan:**
  * Test case cần chạy lại: `TC-LOGIN-030`
  * Điều kiện retest: API bổ sung thông tin số lần còn lại vào payload trả về khi đăng nhập sai, và Frontend hiển thị thông tin này.
  * Expected retest result: Hiển thị thông điệp cảnh báo số lần thử còn lại rõ ràng.

---

### BUG-FR07-B-01: Backend API không validate số lượng sản phẩm thêm vào giỏ hàng

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-044, TC-CART-045, TC-CART-046, TC-CART-047`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Người dùng đã đăng nhập và lấy token hợp lệ.
* **Steps to Reproduce:**
  1. Đăng nhập và lấy token hợp lệ.
  2. Gửi yêu cầu `POST /api/cart` với payload chứa `productId = 1` và `quantity = 0`.
  3. Gửi tiếp yêu cầu `POST /api/cart` với `quantity = -1`.
  4. Gửi tiếp yêu cầu `POST /api/cart` với `quantity = 1.5`.
  5. Kiểm tra mã phản hồi HTTP từ server và dữ liệu giỏ hàng qua API `GET /api/cart`.
* **Expected Result:**
  * API phải từ chối quantity không phải số nguyên dương, trả lỗi 400 hoặc 422, và không lưu item vào giỏ hàng.
* **Actual Result:**
  * API thêm sản phẩm vào giỏ hàng (`POST /api/cart`) chấp nhận mọi số lượng sản phẩm không hợp lệ (như 0, số âm, số thập phân, hoặc bỏ trống) mà không trả về lỗi validate.
* **Impact:**
  * Cho phép lưu trữ số lượng sản phẩm không hợp lệ trong cơ sở dữ liệu giỏ hàng, dẫn đến sai lệch tính toán tổng tiền và có thể gây lỗi hệ thống ở các bước xử lý sau (checkout/order).
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-01.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/128
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-044, TC-CART-045, TC-CART-046, TC-CART-047`
  * Điều kiện retest: API backend `/api/cart` đã được cập nhật mã nguồn kiểm tra dữ liệu đầu vào.
  * Expected retest result: Gửi quantity = 0, -1, 1.5 nhận phản hồi HTTP 400 Bad Request kèm thông điệp lỗi. Giỏ hàng không thay đổi.

---

### BUG-FR07-B-02: Backend API không cộng dồn số lượng cho sản phẩm trùng ID

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-043`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Người dùng đã đăng nhập và lấy token hợp lệ.
* **Steps to Reproduce:**
  1. Đăng nhập vào hệ thống để lấy token.
  2. Gửi yêu cầu `POST /api/cart` để thêm sản phẩm A (`productId = 1`) với `quantity = 1`.
  3. Gửi lại yêu cầu `POST /api/cart` thêm sản phẩm A với `quantity = 2`.
  4. Gọi API `GET /api/cart` để lấy thông tin giỏ hàng hiện tại.
  5. Quan sát số lượng dòng và tổng số lượng sản phẩm A.
* **Expected Result:**
  * Giỏ hàng chỉ có duy nhất 1 dòng cho sản phẩm trùng ID với số lượng (quantity) được cộng dồn (tổng là 3).
* **Actual Result:**
  * API thêm sản phẩm vào giỏ hàng (`POST /api/cart`) không cộng dồn số lượng cho các mặt hàng trùng mã sản phẩm (ID), dẫn đến tạo nhiều dòng sản phẩm trùng lặp trong giỏ hàng.
* **Impact:**
  * Làm sai lệch cấu trúc dữ liệu giỏ hàng của người dùng, gây khó khăn cho việc quản lý số lượng và thanh toán.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-02.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/129
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-043`
  * Điều kiện retest: Backend SUT cập nhật logic xử lý cộng dồn quantity nếu sản phẩm đã tồn tại trong giỏ hàng.
  * Expected retest result: Gọi GET giỏ hàng chỉ trả về 1 dòng sản phẩm A với quantity = 3.

---

### BUG-FR07-B-03: Frontend CartContext không cộng dồn số lượng khi thêm sản phẩm trùng

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-012`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Đang ở trang sản phẩm trên giao diện Web.
* **Steps to Reproduce:**
  1. Truy cập vào trang danh sách hoặc chi tiết sản phẩm trên giao diện Web.
  2. Nhấn nút "Thêm vào giỏ hàng" cho cùng một sản phẩm 2 lần liên tiếp.
  3. Mở trang giỏ hàng tại đường dẫn `/cart`.
  4. Quan sát danh sách sản phẩm hiển thị trong giỏ hàng.
* **Expected Result:**
  * Trên giao diện Web, sản phẩm trùng ID phải được gộp thành 1 dòng duy nhất và số lượng hiển thị tăng tương ứng.
* **Actual Result:**
  * Hệ thống hiển thị thành nhiều dòng sản phẩm trùng lặp trong giỏ hàng trên giao diện Web.
* **Impact:**
  * Trải nghiệm người dùng cực kỳ tệ do giao diện giỏ hàng bị phân mảnh và không thống nhất thông tin.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-03.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/130
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-012`
  * Điều kiện retest: Sửa đổi hàm `addToCart` trong tệp `CartContext.jsx` để kiểm tra và cập nhật quantity của item trùng lặp.
  * Expected retest result: Sản phẩm trùng ID được hiển thị gộp trên 1 dòng với số lượng cộng dồn.

---

### BUG-FR07-B-04: Trang giỏ hàng thiếu nút tăng giảm số lượng (+/-) và nhập số lượng trực tiếp

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-015, TC-CART-016, TC-CART-017, TC-CART-018, TC-CART-019, TC-CART-020, TC-CART-021, TC-CART-022, TC-CART-023, TC-CART-024, TC-CART-025`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Có sản phẩm trong giỏ hàng.
* **Steps to Reproduce:**
  1. Đăng nhập tài khoản khách hàng.
  2. Thực hiện thêm một vài sản phẩm vào giỏ hàng.
  3. Truy cập trang giỏ hàng tại `/cart`.
  4. Quan sát khu vực cột hiển thị số lượng (Quantity) của từng mặt hàng.
* **Expected Result:**
  * Mỗi sản phẩm trong giỏ hàng phải có nút tăng/giảm số lượng (`+`, `-`) hoặc ô cho phép người dùng nhập trực tiếp số lượng để chỉnh sửa.
* **Actual Result:**
  * Số lượng sản phẩm chỉ hiển thị dưới dạng văn bản tĩnh (text) và không có bất kỳ nút bấm hay ô nhập liệu nào để chỉnh sửa.
* **Impact:**
  * Người dùng muốn thay đổi số lượng bắt buộc phải ra ngoài thêm lại hoặc xóa đi thêm mới, gây bất tiện cực kỳ lớn.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-04.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/131
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-015`
  * Điều kiện retest: Frontend được cập nhật thêm các nút bấm `+` / `-` liên kết với hàm cập nhật số lượng.
  * Expected retest result: Người dùng bấm nút và số lượng sản phẩm thay đổi thành công.

---

### BUG-FR07-B-05: Thiếu Confirm Dialog xác nhận khi xóa sản phẩm khỏi giỏ hàng

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-031, TC-CART-032, TC-CART-033, TC-CART-075`
* **Severity / Priority:** Minor / Medium
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Có sản phẩm trong giỏ hàng.
* **Steps to Reproduce:**
  1. Đăng nhập tài khoản và thêm ít nhất một sản phẩm vào giỏ hàng.
  2. Truy cập trang giỏ hàng tại `/cart`.
  3. Nhấn nút biểu tượng thùng rác hoặc nút "Xóa" bên cạnh sản phẩm.
  4. Quan sát xem hệ thống có hiển thị hộp thoại hỏi xác nhận hay thực hiện xóa ngay lập tức.
* **Expected Result:**
  * Hệ thống phải hiển thị một hộp thoại xác nhận (Confirm Dialog) trước khi xóa sản phẩm khỏi giỏ hàng. Chỉ thực hiện xóa khi người dùng chọn xác nhận.
* **Actual Result:**
  * Sản phẩm bị xóa ngay lập tức khỏi giỏ hàng sau khi nhấn nút mà không xuất hiện bất kỳ cảnh báo nào.
* **Impact:**
  * Người dùng dễ bị xóa nhầm sản phẩm do lỡ tay nhấp chuột, buộc phải tìm và thêm lại từ đầu.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-05.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/132
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-031`
  * Điều kiện retest: Frontend tích hợp hộp thoại confirm (ví dụ: `window.confirm` hoặc custom modal) trước khi gọi API xóa.
  * Expected retest result: Dialog xuất hiện khi nhấn xóa, chọn Cancel thì sản phẩm vẫn được giữ nguyên.

---

### BUG-FR07-B-06: Nhãn hiển thị tổng tiền không đúng đặc tả ('Tổng tạm tính' thay vì 'Tổng cộng')

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-009`
* **Severity / Priority:** Minor / Low
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Có sản phẩm trong giỏ hàng.
* **Steps to Reproduce:**
  1. Đăng nhập tài khoản và thêm sản phẩm vào giỏ hàng.
  2. Truy cập trang giỏ hàng `/cart`.
  3. Quan sát nhãn mô tả hiển thị bên cạnh số tổng tiền ở phía dưới bảng giỏ hàng.
* **Expected Result:**
  * Nhãn hiển thị tổng số tiền phải là "Tổng cộng".
* **Actual Result:**
  * Nhãn hiển thị là "Tổng tạm tính".
* **Impact:**
  * Sai lệch thông tin hiển thị so với tài liệu đặc tả yêu cầu nghiệp vụ.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-06.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/133
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-009`
  * Điều kiện retest: Thay đổi chuỗi văn bản hiển thị từ "Tổng tạm tính" thành "Tổng cộng" trong file React của trang giỏ hàng.
  * Expected retest result: Hiển thị chính xác chữ "Tổng cộng".

---

### BUG-FR07-B-07: Trạng thái giỏ hàng trống thiếu hình ảnh/icon minh họa trực quan

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-002`
* **Severity / Priority:** Minor / Low
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Tài khoản khách hàng đang có giỏ hàng hoàn toàn trống rỗng.
* **Steps to Reproduce:**
  1. Đăng nhập bằng một tài khoản mới đăng ký hoặc tài khoản chưa có sản phẩm nào trong giỏ hàng.
  2. Truy cập trang giỏ hàng `/cart`.
  3. Quan sát giao diện hiển thị trạng thái giỏ hàng trống.
* **Expected Result:**
  * Giao diện giỏ hàng trống phải có text thông báo rõ ràng kèm theo hình ảnh minh họa hoặc icon trực quan sống động.
* **Actual Result:**
  * Giao diện chỉ hiển thị duy nhất một dòng chữ đơn điệu "Giỏ hàng trống" và nút quay lại mà không có bất kỳ hình ảnh hay icon nào.
* **Impact:**
  * Giao diện đơn điệu, kém thẩm mỹ và thiếu tính trực quan cho người dùng.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-07.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/134
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-002`
  * Điều kiện retest: Thêm component SVG icon hoặc hình ảnh minh họa giỏ hàng trống vào giao diện React.
  * Expected retest result: Giao diện hiển thị trực quan và sinh động hơn với hình ảnh giỏ hàng trống.

---

### BUG-FR07-B-08: Trang giỏ hàng thiếu thanh breadcrumb điều hướng

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-004`
* **Severity / Priority:** Minor / Low
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Đang ở trang giỏ hàng.
* **Steps to Reproduce:**
  1. Đăng nhập tài khoản khách hàng.
  2. Truy cập vào trang giỏ hàng `/cart`.
  3. Quan sát khu vực phía trên tiêu đề trang xem có thanh điều hướng breadcrumb hay không.
* **Expected Result:**
  * Trang giỏ hàng phải hiển thị thanh breadcrumb dạng `Trang chủ > Giỏ hàng` để định vị vị trí trang.
* **Actual Result:**
  * Không có thanh breadcrumb điều hướng nào xuất hiện trên trang giỏ hàng.
* **Impact:**
  * Người dùng khó định vị vị trí hiện tại trong sơ đồ trang web và khó điều hướng nhanh về trang chủ.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-08.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/135
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-004`
  * Điều kiện retest: Tích hợp component Breadcrumbs vào phía trên cùng của trang `/cart`.
  * Expected retest result: Thanh breadcrumb hiển thị đúng cấu trúc điều hướng.

---

### BUG-FR07-B-09: Không cần đăng nhập vẫn cho phép thêm sản phẩm vào giỏ hàng

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-047`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Người dùng đang truy cập hệ thống ở vai trò khách vãng lai (chưa đăng nhập).
* **Steps to Reproduce:**
  1. Mở trình duyệt ở chế độ ẩn danh hoặc xóa toàn bộ localStorage/sessionStorage để đảm bảo trạng thái chưa đăng nhập (Guest).
  2. Truy cập trang chủ hoặc trang chi tiết sản phẩm.
  3. Nhấn nút "Thêm vào giỏ hàng".
  4. Hoặc gửi trực tiếp một yêu cầu `POST /api/cart` lên server mà không đính kèm mã token xác thực trong Header `Authorization`.
  5. Kiểm tra phản hồi từ phía hệ thống.
* **Expected Result:**
  * Hệ thống phải yêu cầu người dùng đăng nhập trước khi cho phép thêm sản phẩm (trả về lỗi HTTP 401 từ backend hoặc tự chuyển hướng về trang đăng nhập ở frontend).
* **Actual Result:**
  * Khách vãng lai chưa đăng nhập vẫn thực hiện thêm sản phẩm vào giỏ hàng thành công mà không nhận được bất kỳ thông báo hay yêu cầu xác thực nào.
* **Impact:**
  * Tạo ra các giỏ hàng mồ côi (không có ID người dùng liên kết) trong hệ thống, gây rác cơ sở dữ liệu và vi phạm bảo mật phiên làm việc.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-09.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/136
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-047`
  * Điều kiện retest: Bổ sung middleware xác thực JWT cho API `POST /api/cart` ở backend.
  * Expected retest result: Gửi yêu cầu khi chưa đăng nhập trả về HTTP 401 Unauthorized.

---

### BUG-FR07-B-10: Backend API không validate tính toàn vẹn của sản phẩm thêm vào giỏ hàng

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-051, TC-CART-053, TC-CART-057, TC-CART-058, TC-CART-059`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Đăng nhập và có token xác thực.
* **Steps to Reproduce:**
  1. Đăng nhập và lấy token xác thực hợp lệ.
  2. Gửi yêu cầu `POST /api/cart` với payload thiếu thuộc tính `id`.
  3. Gửi tiếp yêu cầu `POST /api/cart` với payload thiếu thuộc tính `price`.
  4. Gửi tiếp yêu cầu `POST /api/cart` với payload có `price = 0` hoặc `price = -1000`.
  5. Kiểm tra phản hồi HTTP từ server và gọi `GET /api/cart` để xem dữ liệu lưu trữ.
* **Expected Result:**
  * API phải từ chối các payload thiếu thông tin bắt buộc hoặc thông tin sai lệch bằng mã lỗi HTTP 400 Bad Request, không lưu dữ liệu lỗi.
* **Actual Result:**
  * API chấp nhận lưu trữ các sản phẩm thiếu trường thông tin quan trọng hoặc có đơn giá âm vào cơ sở dữ liệu giỏ hàng.
* **Impact:**
  * Làm hỏng tính toàn vẹn của cơ sở dữ liệu giỏ hàng, dẫn đến lỗi tính toán giá trị đơn hàng hoặc gây lỗi hệ thống ở các module thanh toán phía sau.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-10.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/137
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-051, TC-CART-053, TC-CART-057, TC-CART-058, TC-CART-059`
  * Điều kiện retest: Bổ sung lớp kiểm định dữ liệu (validation schema) ở đầu API backend.
  * Expected retest result: Các payload lỗi đều bị từ chối bằng mã HTTP 400.

---

### BUG-FR07-B-11: Thiếu thông báo phản hồi (toast/alert) khi thêm sản phẩm vào giỏ hàng thành công

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-010, TC-CART-011, TC-CART-038, TC-CART-074`
* **Severity / Priority:** Minor / Medium
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Đang ở trang chi tiết sản phẩm.
* **Steps to Reproduce:**
  1. Đăng nhập vào tài khoản khách hàng.
  2. Mở trang chi tiết của một sản phẩm bất kỳ.
  3. Nhấn nút "Thêm vào giỏ hàng".
  4. Quan sát các góc màn hình xem có xuất hiện thông báo toast/alert phản hồi thành công hay không.
* **Expected Result:**
  * Hệ thống phải hiển thị một thông báo dạng toast hoặc banner ngắn thông báo "Đã thêm sản phẩm vào giỏ hàng thành công!".
* **Actual Result:**
  * Không có bất kỳ thông báo hay phản hồi trực quan nào trên màn hình sau khi người dùng nhấn nút thêm sản phẩm.
* **Impact:**
  * Người dùng không biết thao tác của mình đã thành công chưa, dẫn đến việc bấm liên tiếp nhiều lần làm tăng số lượng sản phẩm ngoài ý muốn.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-11.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/138
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-010`
  * Điều kiện retest: Tích hợp thư viện thông báo (ví dụ: `react-toastify`) và gọi hiển thị khi API thêm sản phẩm trả về thành công.
  * Expected retest result: Hộp thoại toast báo thành công xuất hiện ở góc màn hình.

---

### BUG-FR07-B-12: Không hiển thị số lượng hàng tồn kho khả dụng và thiếu cảnh báo khi số lượng vượt quá hàng tồn

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-060, TC-CART-079`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Sản phẩm kiểm thử có số lượng tồn kho giới hạn (ví dụ còn 3 sản phẩm).
* **Steps to Reproduce:**
  1. Đăng nhập và truy cập trang chi tiết của sản phẩm có tồn kho giới hạn.
  2. Quan sát giao diện (không thấy thông tin hiển thị số lượng sản phẩm khả dụng trong kho).
  3. Thử tăng số lượng mua lên vượt quá mức tồn kho (ví dụ nhập số lượng là 10).
  4. Nhấp nút "Thêm vào giỏ hàng" và quan sát phản hồi trên giao diện.
* **Expected Result:**
  * Giao diện phải hiển thị số lượng tồn kho khả dụng và ngăn chặn người dùng chọn hoặc thêm số lượng lớn hơn mức tồn kho này.
* **Actual Result:**
  * Giao diện không hiển thị số lượng tồn kho, đồng thời cho phép người dùng thêm số lượng tùy ý vượt biên tồn kho vào giỏ hàng mà không cảnh báo.
* **Impact:**
  * Người dùng có thể đặt mua số lượng sản phẩm lớn hơn thực tế cửa hàng có, dẫn đến việc không thể hoàn thành đơn hàng ở bước xử lý kho vật lý.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-12.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/139
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-060, TC-CART-079`
  * Điều kiện retest: Frontend cập nhật thuộc tính `max` cho ô nhập số lượng dựa trên trường `countInStock` của sản phẩm.
  * Expected retest result: Ô nhập số lượng không cho phép tăng quá mức tồn kho và nút thêm hiển thị lỗi nếu cố tình vượt.

---

### BUG-FR07-B-13: Backend API cho phép giả mạo đơn giá của sản phẩm (Price Tampering)

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-063, TC-CART-064, TC-CART-080`
* **Severity / Priority:** Critical / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Sản phẩm cần thêm có giá trị cao trong cơ sở dữ liệu (ví dụ 10,000,000 ₫).
* **Steps to Reproduce:**
  1. Đăng nhập và lấy token xác thực hợp lệ.
  2. Sử dụng công cụ chặn request (như Postman hoặc Proxy) gửi yêu cầu `POST /api/cart` với payload chứa `productId = 1` nhưng sửa đổi thuộc tính `price = 1` (1 ₫).
  3. Gọi API `GET /api/cart` để kiểm tra thông tin giỏ hàng được lưu trữ.
* **Expected Result:**
  * Backend API phải tự lấy đơn giá của sản phẩm từ cơ sở dữ liệu để lưu vào giỏ hàng, không được tin tưởng đơn giá do client gửi lên.
* **Actual Result:**
  * API backend chấp nhận và lưu trực tiếp đơn giá `1` do client gửi lên, cho phép mua sản phẩm giá trị cao với giá cực rẻ.
* **Impact:**
  * Thất thoát doanh thu nghiêm trọng do người dùng có thể can thiệp kỹ thuật để thay đổi giá của bất kỳ sản phẩm nào trước khi đặt hàng.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-13.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/140
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-063, TC-CART-064, TC-CART-080`
  * Điều kiện retest: Loại bỏ trường `price` khỏi payload yêu cầu của API `POST /api/cart` ở backend, thay vào đó thực hiện truy vấn giá từ bảng `products` bằng `productId`.
  * Expected retest result: Đơn giá sản phẩm trong giỏ hàng luôn được hiển thị đúng giá niêm yết trong DB.

---

### BUG-FR07-B-14: Backend API chấp nhận productId không tồn tại và tạo ra sản phẩm ma

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-061, TC-CART-062, TC-CART-078`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Đăng nhập thành công.
* **Steps to Reproduce:**
  1. Đăng nhập và lấy token xác thực hợp lệ.
  2. Gửi yêu cầu `POST /api/cart` với payload chứa mã sản phẩm không tồn tại trong hệ thống (ví dụ: `productId = 999999`).
  3. Kiểm tra mã phản hồi HTTP từ server.
  4. Gọi API `GET /api/cart` để kiểm tra xem sản phẩm này có bị lưu vào giỏ hàng hay không.
* **Expected Result:**
  * API phải kiểm tra sự tồn tại của `productId` trong cơ sở dữ liệu và trả về lỗi `404 Not Found` nếu không tìm thấy sản phẩm.
* **Actual Result:**
  * API trả về mã thành công `200 OK` và lưu trữ một dòng sản phẩm rác (sản phẩm ma) vào giỏ hàng của người dùng.
* **Impact:**
  * Gây lỗi hiển thị ở frontend khi cố gắng tải thông tin chi tiết của sản phẩm không tồn tại này, và làm sai lệch số liệu giỏ hàng.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-14.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/141
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-061, TC-CART-062, TC-CART-078`
  * Điều kiện retest: Bổ sung bước kiểm tra sự tồn tại của sản phẩm trong DB trước khi thực hiện thêm vào giỏ.
  * Expected retest result: Gửi `productId` không tồn tại trả về lỗi HTTP 404.

---

### BUG-FR07-B-15: Backend API không kiểm tra kiểu dữ liệu của trường quantity (Type Validation)

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-065, TC-CART-066, TC-CART-067, TC-CART-068`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Đăng nhập thành công.
* **Steps to Reproduce:**
  1. Đăng nhập và lấy token xác thực hợp lệ.
  2. Gửi yêu cầu `POST /api/cart` với payload có `quantity = "2"` (kiểu chuỗi ký tự).
  3. Gửi tiếp yêu cầu với `quantity = null`.
  4. Gửi tiếp yêu cầu với `quantity = true` (kiểu boolean).
  5. Kiểm tra phản hồi HTTP nhận được từ server.
* **Expected Result:**
  * API chỉ chấp nhận trường `quantity` có kiểu dữ liệu là số nguyên dương (integer). Các kiểu dữ liệu khác phải bị từ chối bằng lỗi `400 Bad Request`.
* **Actual Result:**
  * API chấp nhận lưu trữ các kiểu dữ liệu không hợp lệ này mà không thực hiện kiểm tra hay ép kiểu đúng đắn.
* **Impact:**
  * Gây ra các lỗi tính toán logic không mong muốn (ví dụ phép cộng chuỗi ký tự thay vì cộng số học) khi xử lý tổng tiền giỏ hàng.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-15.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/142
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-065, TC-CART-066, TC-CART-067, TC-CART-068`
  * Điều kiện retest: Áp dụng ràng buộc kiểu dữ liệu số nguyên dương cho trường `quantity` ở tầng middleware/validation của backend.
  * Expected retest result: Gửi sai kiểu dữ liệu nhận phản hồi HTTP 400.

---

### BUG-FR07-B-16: Lỗ hổng cho phép gán thuộc tính đặc quyền (Mass Assignment / Extra Fields)

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-070`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Đăng nhập thành công.
* **Steps to Reproduce:**
  1. Đăng nhập và lấy token xác thực hợp lệ.
  2. Gửi yêu cầu `POST /api/cart` with payload chứa các thuộc tính ngoài đặc tả như `isAdmin: true`, `discount: 90`.
  3. Gọi API `GET /api/cart` để xem chi tiết đối tượng sản phẩm được trả về trong giỏ hàng.
  4. Kiểm tra các thuộc tính thừa này có bị lưu vào cơ sở dữ liệu hay không.
* **Expected Result:**
  * Backend phải tự động loại bỏ các trường thông tin không nằm trong đặc tả yêu cầu (chỉ nhận `productId` và `quantity`), không lưu trữ các trường dữ liệu thừa.
* **Actual Result:**
  * API chấp nhận và lưu trữ toàn bộ các thuộc tính thừa do client gửi lên, cho phép chèn các trường thông tin tùy ý vào đối tượng giỏ hàng.
* **Impact:**
  * Nguy cơ bảo mật cao do lỗ hổng Mass Assignment, kẻ xấu có thể chèn các quyền hạn hoặc tham số ưu đãi để trục lợi.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-16.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/143
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-070`
  * Điều kiện retest: Thực hiện destructering chỉ lấy `productId` và `quantity` từ request body tại controller xử lý giỏ hàng.
  * Expected retest result: Các trường thừa bị loại bỏ hoàn toàn khỏi đối tượng giỏ hàng lưu trữ.

---

### BUG-FR07-B-17: Giao diện cho phép thanh toán (Checkout) khi giỏ hàng trống

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-076, TC-CART-077`
* **Severity / Priority:** Major / Medium
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Tài khoản khách hàng có giỏ hàng hoàn toàn trống.
* **Steps to Reproduce:**
  1. Đăng nhập tài khoản khách hàng có giỏ hàng hoàn toàn trống.
  2. Truy cập vào trang giỏ hàng tại `/cart`.
  3. Quan sát trạng thái hoạt động của nút "Thanh toán".
  4. Thử gõ trực tiếp đường dẫn `/checkout` trên thanh địa chỉ trình duyệt và nhấn Enter.
* **Expected Result:**
  * Nút "Thanh toán" phải bị vô hiệu hóa (disabled) khi giỏ hàng trống, và hệ thống phải chặn không cho truy cập trang `/checkout` bằng cách chuyển hướng về `/cart`.
* **Actual Result:**
  * Nút "Thanh toán" vẫn hoạt động bình thường và hệ thống cho phép truy cập trực tiếp trang `/checkout` để tiến hành đặt hàng với giỏ hàng rỗng.
* **Impact:**
  * Người dùng có thể tạo ra các đơn hàng trống (0 sản phẩm và tổng tiền bằng 0), gây lỗi logic xử lý đơn hàng ở hệ thống.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-17.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/144
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-076, TC-CART-077`
  * Điều kiện retest: Frontend cập nhật điều kiện disable nút thanh toán nếu `cartItems.length === 0` và thêm Route Guard cho trang `/checkout`.
  * Expected retest result: Nút thanh toán bị khóa và truy cập `/checkout` bị tự động chuyển hướng về `/cart`.

---

### BUG-FR07-B-18: Thiếu xử lý lỗi kết nối mạng hoặc sập máy chủ trên giao diện

* **Feature:** FR-07 – Giỏ hàng
* **Found by Test Case:** `TC-CART-088`
* **Severity / Priority:** Major / Medium
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Người dùng đã đăng nhập thành công.
* **Steps to Reproduce:**
  1. Đăng nhập vào tài khoản khách hàng.
  2. Thực hiện ngắt kết nối mạng của thiết bị hoặc tắt máy chủ Backend SUT.
  3. Trên giao diện Frontend Web, nhấn nút "Thêm vào giỏ hàng".
  4. Quan sát số lượng hiển thị trên badge giỏ hàng ở Navbar và thông báo hiển thị trên giao diện.
* **Expected Result:**
  * Frontend phải hiển thị thông báo lỗi kết nối mạng rõ ràng cho người dùng và không được phép tăng số lượng sản phẩm hiển thị trên badge giỏ hàng nếu API lưu trữ thất bại.
* **Actual Result:**
  * Giao diện không báo lỗi mạng mà vẫn tự động tăng số lượng sản phẩm trên badge ở Navbar dù API thực tế đã thất bại, gây không đồng bộ dữ liệu.
* **Impact:**
  * Người dùng tưởng rằng sản phẩm đã được thêm vào giỏ hàng thành công nhưng thực tế khi mở giỏ hàng hoặc tải lại trang thì giỏ hàng vẫn trống.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-18.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/145
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-088`
  * Điều kiện retest: Frontend cập nhật logic chỉ tăng badge giỏ hàng sau khi nhận được phản hồi thành công (HTTP 200) từ API backend.
  * Expected retest result: Badge giỏ hàng không thay đổi và xuất hiện thông báo lỗi kết nối khi mất mạng.

---

### BUG-FR07-B-19: Giỏ hàng không được làm sạch sau khi thanh toán thành công (checkout success)

* **Feature:** FR-07 – Giỏ hàng (Shopping Cart)
* **Found by Test Case:** `TC-CART-089`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5173
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Người dùng đã đăng nhập và có sản phẩm trong giỏ hàng.
  * Người dùng đang ở màn hình thanh toán `/checkout`.
* **Steps to Reproduce:**
  1. Đăng nhập và thêm sản phẩm vào giỏ hàng.
  2. Nhấn nút Thanh toán để chuyển sang trang `/checkout`.
  3. Bấm nút Thanh toán trên trang checkout để hoàn thành đơn hàng.
  4. Nhận thông báo "Thanh toán thành công!".
  5. Nhấp nút "Quay lại trang chủ" và mở lại trang giỏ hàng `/cart` hoặc xem badge giỏ hàng trên Navbar.
* **Expected Result:**
  * Giỏ hàng phải được xóa sạch hoàn toàn sau khi thanh toán thành công, badge giỏ hàng hiển thị số 0.
* **Actual Result:**
  * Sau khi thanh toán đơn hàng thành công, giỏ hàng không tự động làm trống, các sản phẩm đã thanh toán vẫn tiếp tục hiển thị trong giỏ hàng.
* **Impact:**
  * Người dùng có thể vô tình thực hiện thanh toán lại các sản phẩm đã mua, gây phiền toái lớn trong trải nghiệm mua sắm.
* **Evidence:**
  * Giao diện thanh toán Web: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-19.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/167
* **Retest Plan:**
  * Test case cần chạy lại: `TC-CART-089`
  * Điều kiện retest: API thanh toán thành công gửi lệnh xóa sạch giỏ hàng hiện tại trong DB, hoặc Frontend tự động xóa state giỏ hàng cục bộ.
  * Expected retest result: Giỏ hàng trống rỗng và badge hiển thị số 0 sau khi đặt hàng thành công.

---

## 4. Summary of Dashboard Bugs (FR-13)

| Bug ID | Title | Severity | Priority | Related Test Case | GitHub Issue |
|---|---|---|---|---|---|
| BUG-FR13-C-01 | Giao diện Dashboard hiển thị Tổng doanh thu bị nhân đôi | Major | High | [`TC-DASHBOARD-DT-001`](tests/test-cases/dashboard/TC-DASHBOARD-DT-001.md), [`TC-DASHBOARD-BVA-006`](tests/test-cases/dashboard/TC-DASHBOARD-BVA-006.md), [`TC-DASHBOARD-DT-023`](tests/test-cases/dashboard/TC-DASHBOARD-DT-023.md) | [Issue #156](https://github.com/trngnneee/eshop-sut/issues/156) |
| BUG-FR13-C-02 | Backend API `/api/admin/orders` và `/api/admin/users` thiếu kiểm soát phân quyền (role) | Critical | High | [`TC-DASHBOARD-DT-004`](tests/test-cases/dashboard/TC-DASHBOARD-DT-004.md), [`TC-DASHBOARD-DT-013`](tests/test-cases/dashboard/TC-DASHBOARD-DT-013.md), [`TC-DASHBOARD-DT-014`](tests/test-cases/dashboard/TC-DASHBOARD-DT-014.md), [`TC-DASHBOARD-DT-024`](tests/test-cases/dashboard/TC-DASHBOARD-DT-024.md) | [Issue #157](https://github.com/trngnneee/eshop-sut/issues/157) |
| BUG-FR13-C-03 | Lỗi API `/api/admin/users` 500 ngắt toàn bộ tiến trình fetchData của dashboard | Medium | Medium | [`TC-DASHBOARD-DT-017`](tests/test-cases/dashboard/TC-DASHBOARD-DT-017.md) | [Issue #158](https://github.com/trngnneee/eshop-sut/issues/158) |
| BUG-FR13-C-04 | Order thiếu `total_amount` dẫn đến tính toán ra `NaN ₫` hiển thị trên giao diện | Medium | Medium | [`TC-DASHBOARD-DT-020`](tests/test-cases/dashboard/TC-DASHBOARD-DT-020.md) | [Issue #159](https://github.com/trngnneee/eshop-sut/issues/159) |
| BUG-FR13-C-05 | Giao diện hiển thị trực tiếp số liệu thống kê âm hoặc thập phân mà không kiểm tra tính hợp lệ dữ liệu | Minor | Low | [`TC-DASHBOARD-BVA-018`](tests/test-cases/dashboard/TC-DASHBOARD-BVA-018.md), [`TC-DASHBOARD-BVA-019`](tests/test-cases/dashboard/TC-DASHBOARD-BVA-019.md) | [Issue #160](https://github.com/trngnneee/eshop-sut/issues/160) |

---

## 5. Detailed Bug Reports for Dashboard (FR-13)

### BUG-FR13-C-01: Giao diện Dashboard hiển thị Tổng doanh thu bị nhân đôi

* **Feature:** FR-13 – Dashboard
* **Found by Test Case:** `TC-DASHBOARD-DT-001, TC-DASHBOARD-BVA-006, TC-DASHBOARD-DT-023`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5174 (Web Admin)
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Tài khoản Admin đã đăng nhập thành công và đang ở trang Dashboard.
* **Steps to Reproduce:**
  1. Đăng nhập hệ thống bằng tài khoản admin.
  2. Điều hướng tới Dashboard của Web Admin (`http://localhost:5174`).
  3. Kiểm tra số hiển thị ở 'Tổng doanh thu (Delivered)'.
  4. So sánh số hiển thị này với tổng số tiền thực tế của các đơn hàng đã giao (`delivered`) có trong database.
* **Expected Result:**
  * Tổng doanh thu hiển thị trên Dashboard phải bằng chính xác tổng số tiền của các đơn hàng có trạng thái "delivered". Không có hiện tượng nhân đôi số tiền.
* **Actual Result:**
  * Do doanh thu bị cộng lặp 2 lần trong hàm tính toán ở frontend, số tiền hiển thị bị nhân đôi so với giá trị thực tế.
* **Impact:**
  * Cung cấp số liệu thống kê sai lệch nghiêm trọng cho quản trị viên, ảnh hưởng đến việc phân tích kinh doanh.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/dashboard/evidences/BUG-FR13-C-01.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/156
* **Retest Plan:**
  * Test case cần chạy lại: `TC-DASHBOARD-DT-023`
  * Điều kiện retest: Cập nhật hàm tính tổng doanh thu ở frontend để loại bỏ bước cộng lặp.
  * Expected retest result: Doanh thu hiển thị chính xác đúng số tiền thực tế.

---

### BUG-FR13-C-02: Backend API `/api/admin/orders` và `/api/admin/users` thiếu kiểm soát phân quyền (role)

* **Feature:** FR-13 – Dashboard (Security)
* **Found by Test Case:** `TC-DASHBOARD-DT-004, TC-DASHBOARD-DT-013, TC-DASHBOARD-DT-014, TC-DASHBOARD-DT-024`
* **Severity / Priority:** Critical / High
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5174 (Web Admin)
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Tài khoản người dùng có quyền là `customer` (không phải `admin`).
* **Steps to Reproduce:**
  1. Đăng nhập bằng tài khoản người dùng thông thường (Customer) và lấy mã token JWT xác thực phiên làm việc.
  2. Gửi request GET tới endpoint `/api/admin/orders` hoặc `/api/admin/users` kèm theo mã token vừa lấy.
  3. Quan sát kết quả phản hồi từ hệ thống.
* **Expected Result:**
  * Hệ thống từ chối truy cập và trả về mã lỗi `403 Forbidden` do tài khoản không có quyền Admin.
* **Actual Result:**
  * API backend xử lý thành công và trả về toàn bộ danh sách đơn hàng hoặc người dùng cho tài khoản customer thường.
* **Impact:**
  * Lỗ hổng rò rỉ dữ liệu nghiêm trọng (Broken Object Level Authorization), cho phép người dùng thường xem thông tin cá nhân và thông tin mua hàng của toàn bộ hệ thống.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/dashboard/evidences/BUG-FR13-C-02.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/157
* **Retest Plan:**
  * Test case cần chạy lại: `TC-DASHBOARD-DT-024`
  * Điều kiện retest: Thêm middleware kiểm tra vai trò người dùng (`requireAdmin`) vào các route API admin ở backend.
  * Expected retest result: Yêu cầu từ tài khoản customer bị từ chối bằng mã lỗi HTTP 403.

---

### BUG-FR13-C-03: Lỗi API `/api/admin/users` 500 ngắt toàn bộ tiến trình fetchData của dashboard

* **Feature:** FR-13 – Dashboard (Robustness)
* **Found by Test Case:** `TC-DASHBOARD-DT-017`
* **Severity / Priority:** Medium / Medium
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5174 (Web Admin)
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Tài khoản Admin đã đăng nhập.
* **Steps to Reproduce:**
  1. Đăng nhập admin.
  2. Giả lập hoặc mock API `/api/admin/users` trả về mã lỗi HTTP 500.
  3. Mở giao diện Dashboard.
  4. Quan sát hiển thị của các card doanh thu, đơn hàng, danh mục.
* **Expected Result:**
  * Một API lỗi không được làm ngắt quãng các API độc lập khác. Giao diện vẫn hiển thị bình thường dữ liệu doanh thu, đơn hàng... và hiển thị fallback lỗi ở riêng card người dùng.
* **Actual Result:**
  * Tiến trình fetchData sử dụng `Promise.all` bị lỗi và ngắt hoàn toàn khi có 1 API bị lỗi, khiến toàn bộ màn hình dashboard bị trắng hoặc trống số liệu của tất cả các card khác.
* **Impact:**
  * Làm giảm tính chịu lỗi (robustness) của hệ thống, một lỗi nhỏ ở API phụ làm tê liệt toàn bộ giao diện quản trị.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/dashboard/evidences/BUG-FR13-C-03.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/158
* **Retest Plan:**
  * Test case cần chạy lại: `TC-DASHBOARD-DT-017`
  * Điều kiện retest: Thay thế `Promise.all` bằng `Promise.allSettled` hoặc xử lý bắt lỗi (catch) riêng biệt cho từng promise gọi API ở frontend.
  * Expected retest result: Dashboard hiển thị đầy đủ số liệu đơn hàng/doanh thu, chỉ báo lỗi ở riêng card Users.

---

### BUG-FR13-C-04: Order thiếu `total_amount` dẫn đến tính toán ra `NaN ₫` hiển thị trên giao diện

* **Feature:** FR-13 – Dashboard (Robustness)
* **Found by Test Case:** `TC-DASHBOARD-DT-020`
* **Severity / Priority:** Medium / Medium
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5174 (Web Admin)
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Tài khoản Admin đã đăng nhập.
* **Steps to Reproduce:**
  1. Đăng nhập admin.
  2. Mock API `/api/admin/orders` trả về mảng orders chứa một đối tượng order thiếu thuộc tính `total_amount` (ví dụ: `undefined` hoặc `null`).
  3. Mở Dashboard.
  4. Quan sát số hiển thị ở 'Tổng doanh thu (Delivered)'.
* **Expected Result:**
  * Dashboard phải bỏ qua đơn hàng lỗi hoặc coi giá trị của nó bằng 0 và tính toán bình thường mà không hiển thị ra chữ `NaN ₫`.
* **Actual Result:**
  * Giao diện hiển thị Tổng doanh thu là `NaN ₫` do thực hiện phép cộng với giá trị `undefined` trong hàm `reduce`.
* **Impact:**
  * Giao diện hiển thị thông tin lỗi kỹ thuật (`NaN`), gây mất thẩm mỹ và giảm độ tin cậy của báo cáo doanh thu.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/dashboard/evidences/BUG-FR13-C-04.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/159
* **Retest Plan:**
  * Test case cần chạy lại: `TC-DASHBOARD-DT-020`
  * Điều kiện retest: Cấu hình giá trị mặc định `order.total_amount || 0` khi tính tổng ở frontend.
  * Expected retest result: Tổng doanh thu hiển thị đúng số tiền của các đơn hàng hợp lệ, không hiển thị `NaN`.

---

### BUG-FR13-C-05: Giao diện hiển thị trực tiếp số liệu thống kê âm hoặc thập phân mà không kiểm tra tính hợp lệ dữ liệu

* **Feature:** FR-13 – Dashboard (UI/UX)
* **Found by Test Case:** `TC-DASHBOARD-BVA-018, TC-DASHBOARD-BVA-019`
* **Severity / Priority:** Minor / Low
* **Environment:**
  * OS: Windows 11
  * Browser / Device: Chrome
  * App URL: http://localhost:5174 (Web Admin)
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Tài khoản Admin đã đăng nhập.
* **Steps to Reproduce:**
  1. Đăng nhập admin.
  2. Giả lập API trả về số lượng người dùng là số âm (`-1`) hoặc số lượng sản phẩm là số thập phân (`10.5`).
  3. Mở Dashboard.
  4. Quan sát số liệu hiển thị trên các card thống kê tương ứng.
* **Expected Result:**
  * Giao diện phải thực hiện validate dữ liệu nhận được: tự động làm tròn số lượng sản phẩm và chuyển đổi các giá trị âm về số `0` trước khi hiển thị.
* **Actual Result:**
  * Giao diện hiển thị trực tiếp giá trị thô nhận được từ API: hiển thị `-1` người dùng và `10.5` sản phẩm trên màn hình.
* **Impact:**
  * Hiển thị số liệu thống kê vô lý và phi thực tế (không thể có nửa sản phẩm hay số lượng người dùng âm).
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/dashboard/evidences/BUG-FR13-C-05.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/160
* **Retest Plan:**
  * Test case cần chạy lại: `TC-DASHBOARD-BVA-018, TC-DASHBOARD-BVA-019`
  * Điều kiện retest: Thêm hàm xử lý kiểm tra `Math.max(0, Math.round(value))` cho các số liệu thống kê trên UI.
  * Expected retest result: Số lượng người dùng hiển thị là `0` và số lượng sản phẩm hiển thị là `11`.

---

## 6. Detailed Bug Reports for Mobile Cart & Checkout (FR-21)

### BUG-FR21-D-01: Giao dịch Checkout thiếu thuộc tính địa chỉ giao hàng gửi lên API

* **Feature:** FR-21 – Mobile Cart & Checkout
* **Found by Test Case:** `TC-MOBILE-CART-DT-019`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: iOS / Android (Mobile App)
  * Browser / Device: iPhone / Android Emulator
  * App URL: Mobile App
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Khách hàng đã thiết lập địa chỉ giao hàng trong profile của mình.
* **Steps to Reproduce:**
  1. Đăng nhập vào ứng dụng di động và thiết lập địa chỉ giao hàng trong hồ sơ cá nhân.
  2. Thêm sản phẩm vào giỏ hàng và tiến hành thanh toán.
  3. Tại màn hình Checkout, bấm 'Xác nhận thanh toán'.
  4. Kiểm tra thông tin đơn hàng vừa tạo trên hệ thống.
* **Expected Result:**
  * Đơn hàng mới được tạo phải lưu giữ đầy đủ địa chỉ giao hàng lấy từ hồ sơ cá nhân của người dùng.
* **Actual Result:**
  * Khi thực hiện đặt hàng trên ứng dụng di động, thông tin địa chỉ giao hàng không được gửi kèm theo đơn hàng, dẫn đến đơn hàng mới được tạo trên hệ thống bị bỏ trống trường địa chỉ giao hàng.
* **Impact:**
  * Cửa hàng không có thông tin địa chỉ để giao hàng cho khách, bắt buộc phải liên hệ thủ công rất mất thời gian.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/mobile-cart/evidences/BUG-FR21-D-01.jpg)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/161
* **Retest Plan:**
  * Test case cần chạy lại: `TC-MOBILE-CART-DT-019`
  * Điều kiện retest: Cập nhật API call đặt hàng trên mobile app để truyền kèm theo trường `shippingAddress`.
  * Expected retest result: Đơn hàng mới được tạo hiển thị đầy đủ địa chỉ giao hàng của khách.

---

### BUG-FR21-D-02: Nhập số lượng trực tiếp trong giỏ hàng bị cộng thêm 1 đơn vị

* **Feature:** FR-21 – Mobile Cart & Checkout
* **Found by Test Case:** `TC-MOBILE-CART-DT-007`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: iOS / Android (Mobile App)
  * Browser / Device: iPhone / Android Emulator
  * App URL: Mobile App
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Có sản phẩm trong giỏ hàng trên mobile app.
* **Steps to Reproduce:**
  1. Đăng nhập vào ứng dụng di động.
  2. Thêm 1 sản phẩm vào giỏ hàng.
  3. Mở giỏ hàng, tại ô nhập số lượng, nhập trực tiếp số lượng là 2.
  4. Quan sát số hiển thị thực tế trên ô nhập liệu.
* **Expected Result:**
  * Số lượng hiển thị đúng bằng giá trị số người dùng đã nhập trực tiếp (ví dụ nhập 2 thì hiển thị là 2).
* **Actual Result:**
  * Giao diện giỏ hàng trên ứng dụng di động tự động tăng số lượng sản phẩm thêm 1 đơn vị so với số lượng người dùng nhập trực tiếp (nhập 2 hiển thị thành 3).
* **Impact:**
  * Người dùng bị mua thừa số lượng sản phẩm mong muốn, gây khó khăn cho việc đặt hàng đúng nhu cầu.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/mobile-cart/evidences/BUG-FR21-D-02.jpg)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/162
* **Retest Plan:**
  * Test case cần chạy lại: `TC-MOBILE-CART-DT-007`
  * Điều kiện retest: Sửa đổi logic xử lý sự kiện `onChangeText` của ô nhập số lượng trên mobile để gán trực tiếp giá trị thay vì cộng thêm 1.
  * Expected retest result: Nhập số lượng bao nhiêu hiển thị đúng bấy nhiêu.

---

### BUG-FR21-D-03: Hồ sơ mobile không chấp nhận số điện thoại bắt đầu bằng số 0

* **Feature:** FR-21 – Mobile Cart & Checkout
* **Found by Test Case:** `TC-MOBILE-CART-DT-015, TC-MOBILE-CART-BVA-009`
* **Severity / Priority:** Medium / High
* **Environment:**
  * OS: iOS / Android (Mobile App)
  * Browser / Device: iPhone / Android Emulator
  * App URL: Mobile App
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Đăng nhập tài khoản user di động, đang ở tab Hồ sơ.
* **Steps to Reproduce:**
  1. Đăng nhập vào ứng dụng di động và vào trang Profile.
  2. Nhập số điện thoại hợp lệ ở Việt Nam (ví dụ: `0912345678`) vào ô Số điện thoại.
  3. Nhấn nút 'Cập nhật'.
  4. Quan sát thông báo lỗi.
* **Expected Result:**
  * Hệ thống phải chấp nhận số điện thoại hợp lệ bắt đầu bằng chữ số 0 theo định dạng số điện thoại Việt Nam.
* **Actual Result:**
  * Giao diện báo lỗi định dạng không hợp lệ và từ chối cập nhật khi số điện thoại bắt đầu bằng số 0.
* **Impact:**
  * Người dùng Việt Nam hoàn toàn không thể cập nhật được số điện thoại của mình vào hồ sơ cá nhân trên mobile.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/mobile-cart/evidences/BUG-FR21-D-03.jpg)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/163
* **Retest Plan:**
  * Test case cần chạy lại: `TC-MOBILE-CART-DT-015, TC-MOBILE-CART-BVA-009`
  * Điều kiện retest: Thay đổi biểu thức chính quy (Regex) kiểm tra số điện thoại trên mobile app để cho phép ký tự đầu tiên là số 0.
  * Expected retest result: Cập nhật thành công số điện thoại bắt đầu bằng số 0.

---

### BUG-FR21-D-04: API `/api/checkout` thiếu kiểm định tính toàn vẹn của đơn giá (Price Tampering)

* **Feature:** FR-21 – Mobile Cart & Checkout
* **Found by Test Case:** `TC-MOBILE-CART-DT-018`
* **Severity / Priority:** Critical / High
* **Environment:**
  * OS: Cross-platform (Backend API)
  * Browser / Device: iPhone / Android Emulator
  * App URL: Mobile App
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Người dùng đã đăng nhập thành công.
* **Steps to Reproduce:**
  1. Đăng nhập và thêm sản phẩm có giá trị cao (ví dụ: 30,000,000 ₫) vào giỏ hàng.
  2. Nhấn thanh toán trên giao diện ứng dụng.
  3. Sử dụng công cụ chặn request (như Proxy/Burp Suite) để bắt và can thiệp request thanh toán (`POST /api/checkout`).
  4. Sửa giá trị tổng số tiền (`total_amount`) trong nội dung request thành 1,000 ₫ và gửi lên hệ thống.
  5. Quan sát phản hồi từ hệ thống và kiểm tra thông tin đơn hàng trong trang quản lý đơn hàng.
* **Expected Result:**
  * Backend API phải tự tính lại tổng tiền dựa trên các sản phẩm đặt mua và đơn giá thực tế trong cơ sở dữ liệu, từ chối tạo đơn và trả về lỗi nếu tổng tiền client gửi lên bị sai lệch.
* **Actual Result:**
  * API thanh toán (`POST /api/checkout`) chấp nhận trực tiếp tổng số tiền (`total_amount`) do người dùng truyền lên mà không kiểm tra đối sánh, tạo đơn hàng thành công với giá trị bị sửa đổi.
* **Impact:**
  * Thất thoát tài chính cực kỳ nghiêm trọng, người dùng có thể mua bất kỳ đơn hàng giá trị cao nào với số tiền tối thiểu.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/mobile-cart/evidences/BUG-FR21-D-04.png)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/164
* **Retest Plan:**
  * Test case cần chạy lại: `TC-MOBILE-CART-DT-018`
  * Điều kiện retest: Cập nhật API `/api/checkout` ở backend để tự động truy vấn đơn giá từ DB và tính toán lại tổng tiền trước khi ghi nhận đơn hàng.
  * Expected retest result: Thay đổi tổng tiền ở client gửi lên sẽ bị API từ chối với lỗi HTTP 400.

---

### BUG-FR21-D-05: Hệ thống không áp dụng được mã giảm giá khi tổng giá trị đơn hàng bằng đúng giá trị tối thiểu quy định

* **Feature:** FR-21 – Mobile Cart & Checkout
* **Found by Test Case:** `TC-MOBILE-CART-BVA-023`
* **Severity / Priority:** Major / High
* **Environment:**
  * OS: Cross-platform (Backend API)
  * Browser / Device: iPhone / Android Emulator
  * App URL: Mobile App
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Mã giảm giá "SAVE10" (yêu cầu đơn hàng tối thiểu 300,000 ₫) đang hoạt động.
* **Steps to Reproduce:**
  1. Đăng nhập vào ứng dụng di động.
  2. Thêm các sản phẩm vào giỏ hàng sao cho tổng số tiền tạm tính đúng bằng 300,000 ₫.
  3. Điều hướng tới trang Checkout, nhập mã giảm giá "SAVE10" và nhấn "Áp dụng".
* **Expected Result:**
  * Mã giảm giá được áp dụng thành công và tổng tiền được giảm 10% (30,000 ₫).
* **Actual Result:**
  * Hệ thống báo lỗi: "Đơn hàng chưa đủ giá trị tối thiểu 300,000 ₫ để áp dụng mã này" do sử dụng so sánh lớn hơn (`>`) thay vì lớn hơn hoặc bằng (`>=`).
* **Impact:**
  * Khách hàng đạt đúng giá trị biên tối thiểu để nhận ưu đãi nhưng bị hệ thống từ chối, gây giảm trải nghiệm mua sắm và thắc mắc khiếu nại.
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/mobile-cart/evidences/BUG-FR21-D-05.jpg)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/165
* **Retest Plan:**
  * Test case cần chạy lại: `TC-MOBILE-CART-BVA-023`
  * Điều kiện retest: Sửa đổi toán tử so sánh từ `>` thành `>=` trong hàm kiểm tra điều kiện áp dụng mã giảm giá ở backend.
  * Expected retest result: Mã giảm giá áp dụng thành công khi đơn hàng bằng đúng 300,000 ₫.

---

### BUG-FR21-D-06: API áp dụng mã giảm giá tính sai số tiền giảm giá phần trăm (percent)

* **Feature:** FR-21 – Mobile Cart & Checkout
* **Found by Test Case:** `TC-MOBILE-CART-DT-020`
* **Severity / Priority:** Critical / High
* **Environment:**
  * OS: Cross-platform (Backend API)
  * Browser / Device: iPhone / Android Emulator
  * App URL: Mobile App
  * Backend/API URL: http://localhost:3000
  * Commit hash: `fed8f6e04c682d4e0397a79312a5747475780ef3`
* **Preconditions:**
  * Mã giảm giá "SAVE10" (giảm 10% - tỷ lệ 0.1) đang hoạt động.
* **Steps to Reproduce:**
  1. Đăng nhập vào ứng dụng di động.
  2. Thêm sản phẩm trị giá 350,000 ₫ vào giỏ hàng và thanh toán.
  3. Nhập mã giảm giá "SAVE10" và nhấn "Áp dụng".
  4. Kiểm tra số tiền được khấu trừ.
* **Expected Result:**
  * Số tiền giảm giá phải được tính là: 350,000 ₫ * 0.1 = 35,000 ₫ (tổng tiền thanh toán cuối cùng là 315,000 ₫).
* **Actual Result:**
  * Hệ thống tính sai số tiền được giảm thành 315,000 ₫ (tương đương giảm tới 90%), tổng tiền thanh toán cuối cùng chỉ còn 35,000 ₫.
* **Impact:**
  * Thất thoát tài chính nghiêm trọng do tính toán sai số tiền giảm giá phần trăm (bị đảo ngược giữa số tiền cần trả và số tiền được giảm).
* **Evidence:**
  * Screenshot: ![Evidence](tests/bug/mobile-cart/evidences/BUG-FR21-D-06.jpg)
  * Video: `Không áp dụng`
  * Console/API log: `Không áp dụng`
  * GitHub Issue: https://github.com/trngnneee/eshop-sut/issues/166
* **Retest Plan:**
  * Test case cần chạy lại: `TC-MOBILE-CART-DT-020`
  * Điều kiện retest: Sửa đổi công thức tính tiền giảm giá phần trăm ở backend thành `discountAmount = total * discountPercent` thay vì `total * (1 - discountPercent)`.
  * Expected retest result: Số tiền giảm giá được tính chính xác là 35,000 ₫.
