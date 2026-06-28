# Master Bug Report

Tài liệu tổng hợp danh sách toàn bộ lỗi phát hiện được trong quá trình kiểm thử Module Đăng nhập & Khóa tài khoản (FR-02) và Module Giỏ hàng (FR-07).

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
| BUG-FR02-A-18 | Giao diện đăng nhập Frontend che khuất lỗi khóa tài khoản (luôn hiện thông báo lỗi tĩnh) | Major | High | [`TC-LOGIN-...`](tests/test-cases/login/TC-LOGIN-....md) | [Issue #48](https://github.com/trngnneee/eshop-sut/issues/48) |
| BUG-FR02-A-19 | API và giao diện thiếu cảnh báo số lần đăng nhập sai còn lại trước khi khóa | Major | Medium | [`TC-LOGIN-030`](tests/test-cases/login/TC-LOGIN-030.md) | [Issue #49](https://github.com/trngnneee/eshop-sut/issues/49) |

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
| BUG-FR07-B-09 | Không cần đăng nhập vẫn cho phép thêm sản phẩm vào giỏ hàng | Major | High | [`TC-CART-...`](tests/test-cases/cart/TC-CART-....md) | [Issue #136](https://github.com/trngnneee/eshop-sut/issues/136) |
| BUG-FR07-B-10 | Backend API không validate tính toàn vẹn của sản phẩm thêm vào giỏ hàng | Major | High | [`TC-CART-051`](tests/test-cases/cart/TC-CART-051.md), [`TC-CART-053`](tests/test-cases/cart/TC-CART-053.md), [`TC-CART-057`](tests/test-cases/cart/TC-CART-057.md), [`TC-CART-058`](tests/test-cases/cart/TC-CART-058.md), [`TC-CART-059`](tests/test-cases/cart/TC-CART-059.md) | [Issue #137](https://github.com/trngnneee/eshop-sut/issues/137) |
| BUG-FR07-B-11 | Thiếu thông báo phản hồi (toast/alert) khi thêm sản phẩm vào giỏ hàng thành công | Minor | Medium | [`TC-CART-010`](tests/test-cases/cart/TC-CART-010.md), [`TC-CART-011`](tests/test-cases/cart/TC-CART-011.md), [`TC-CART-038`](tests/test-cases/cart/TC-CART-038.md), [`TC-CART-074`](tests/test-cases/cart/TC-CART-074.md) | [Issue #138](https://github.com/trngnneee/eshop-sut/issues/138) |
| BUG-FR07-B-12 | Không hiển thị số lượng hàng tồn kho khả dụng và thiếu cảnh báo khi số lượng vượt quá hàng tồn | Major | High | [`TC-CART-060`](tests/test-cases/cart/TC-CART-060.md), [`TC-CART-079`](tests/test-cases/cart/TC-CART-079.md) | [Issue #139](https://github.com/trngnneee/eshop-sut/issues/139) |
| BUG-FR07-B-13 | Backend API cho phép giả mạo đơn giá của sản phẩm (Price Tampering) | Critical | High | [`TC-CART-063`](tests/test-cases/cart/TC-CART-063.md), [`TC-CART-064`](tests/test-cases/cart/TC-CART-064.md), [`TC-CART-080`](tests/test-cases/cart/TC-CART-080.md) | [Issue #140](https://github.com/trngnneee/eshop-sut/issues/140) |
| BUG-FR07-B-14 | Backend API chấp nhận productId không tồn tại và tạo ra sản phẩm ma | Major | High | [`TC-CART-061`](tests/test-cases/cart/TC-CART-061.md), [`TC-CART-062`](tests/test-cases/cart/TC-CART-062.md), [`TC-CART-078`](tests/test-cases/cart/TC-CART-078.md) | [Issue #141](https://github.com/trngnneee/eshop-sut/issues/141) |
| BUG-FR07-B-15 | Backend API không kiểm tra kiểu dữ liệu của trường quantity (Type Validation) | Major | High | [`TC-CART-065`](tests/test-cases/cart/TC-CART-065.md), [`TC-CART-066`](tests/test-cases/cart/TC-CART-066.md), [`TC-CART-067`](tests/test-cases/cart/TC-CART-067.md), [`TC-CART-068`](tests/test-cases/cart/TC-CART-068.md) | [Issue #142](https://github.com/trngnneee/eshop-sut/issues/142) |
| BUG-FR07-B-16 | Lỗ hổng cho phép gán thuộc tính đặc quyền (Mass Assignment / Extra Fields) | Major | High | [`TC-CART-070`](tests/test-cases/cart/TC-CART-070.md) | [Issue #143](https://github.com/trngnneee/eshop-sut/issues/143) |
| BUG-FR07-B-18 | Thiếu xử lý lỗi kết nối mạng hoặc sập máy chủ trên giao diện | Major | Medium | [`TC-CART-...`](tests/test-cases/cart/TC-CART-....md) | [Issue #145](https://github.com/trngnneee/eshop-sut/issues/145) |
| BUG-FR07-B-19 | Giỏ hàng không được làm sạch sau khi thanh toán thành công (checkout success) | Major | High | [`TC-CART-089`](tests/test-cases/cart/TC-CART-089.md) | N/A |

---

## 3. Detailed Bug Reports

# BUG-FR02-A-01: Bộ đếm đăng nhập sai tăng thêm 2 đơn vị thay vì 1

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-002, TC-LOGIN-023`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Đăng ký tài khoản mới.\n2. Gửi 1 yêu cầu POST đăng nhập sai tới `/api/login` với tài khoản vừa tạo.\n3. Thử đăng nhập bằng tài khoản khác hoặc kiểm tra trạng thái đăng nhập qua API.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Ở `API backend`, mỗi lần người dùng đăng nhập sai mật khẩu, hệ thống tăng bộ đếm thêm `2` đơn vị thay vì `1` đơn vị như đặc tả.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-01.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/31
- Labels: type:bug, status:open

---

# BUG-FR02-A-02: Thời gian khóa tài khoản bị thiết lập sai thành 3 phút

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-003, TC-LOGIN-014, TC-LOGIN-025`

## Severity / Priority
Medium / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Thực hiện đăng nhập sai liên tiếp cho đến khi tài khoản bị khóa.\n2. Đo khoảng thời gian tài khoản bị từ chối đăng nhập (đúng mật khẩu) cho đến khi tài khoản có thể đăng nhập lại thành công.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Khi tài khoản đăng nhập sai đạt ngưỡng, thời gian khóa bị đặt là 180000 ms (3 phút) thay vì 30000 ms (30 giây) theo đặc tả môi trường demo.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-02.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/32
- Labels: type:bug, status:open

---

# BUG-FR02-A-03: Race condition do xử lý yêu cầu đăng nhập bất đồng bộ

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-002, TC-LOGIN-013, TC-LOGIN-023, TC-LOGIN-024`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Gửi request đăng nhập sai mật khẩu.\n2. Thực hiện nhanh yêu cầu đăng nhập tiếp theo trước khi hệ thống kịp ghi nhận trạng thái.\n3. Kiểm tra xem tài khoản có thể vượt quá số lần đăng nhập sai quy định mà không bị khóa ngay lập tức hay không.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Backend trả về phản hồi HTTP ngay lập tức mà không đợi giao dịch xử lý yêu cầu đăng nhập hoàn thành, dẫn đến việc đọc dữ liệu kế tiếp bị sai lệch.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-03.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/33
- Labels: type:bug, status:open

---

# BUG-FR02-A-04: Tiêu đề trang Đăng nhập hiển thị sai thành "Đăng Ký"

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-004`

## Severity / Priority
Minor / Medium

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Truy cập vào trang đăng nhập (`/login`).\n2. Kiểm tra thẻ tiêu đề `<h2>` trên biểu mẫu.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Tại giao diện đăng nhập dành cho web, tiêu đề trang hiển thị không đúng ngữ cảnh là `"Đăng Ký"`.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-04.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/34
- Labels: type:bug, status:open

---

# BUG-FR02-A-05: Trường nhập Email hiển thị nhãn là "Username"

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-004`

## Severity / Priority
Minor / Medium

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Truy cập trang đăng nhập `/login`.\n2. Nhìn nhãn mô tả của ô nhập liệu đầu tiên.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Trường nhập thông tin định danh hiển thị nhãn là `"Username"` thay vì `"Email"`.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-05.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/35
- Labels: type:bug, status:open

---

# BUG-FR02-A-06: Nút submit biểu mẫu sử dụng tiếng Anh "Sign In"

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-004`

## Severity / Priority
Minor / Medium

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Xem trang đăng nhập `/login`.\n2. Đọc văn bản hiển thị trên nút submit chính của form.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Giao diện nút gửi biểu mẫu hiển thị tiếng Anh `"Sign In"` thay vì tiếng Việt `"Đăng nhập"`.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-06.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/36
- Labels: type:bug, status:open

---

# BUG-FR02-A-07: Mật khẩu hiển thị ở dạng plain text (type="text")

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-004`

## Severity / Priority
Critical / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Nhập mật khẩu vào trường mật khẩu trên form đăng nhập.\n2. Các ký tự hiển thị rõ và không được che ẩn dạng dấu chấm.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Trường nhập mật khẩu cấu hình `type="text"`, khiến ký tự nhập vào hiển thị rõ ràng trên màn hình, vi phạm nghiêm trọng tính bảo mật.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-07.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/37
- Labels: type:bug, status:open

---

# BUG-FR02-A-08: Thiếu dấu hoa thị màu đỏ * đánh dấu trường bắt buộc

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-004`

## Severity / Priority
Cosmetic / Low

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Quan sát nhãn của trường Email và Mật khẩu trên form đăng nhập.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Các trường bắt buộc nhập (Email và Mật khẩu) thiếu dấu hoa thị đỏ `*` cạnh nhãn label theo tiêu chuẩn thiết kế form.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-08.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/38
- Labels: type:bug, status:open

---

# BUG-FR02-A-09: Thiếu trim khoảng trắng của Email ở phía Backend

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-005`

## Severity / Priority
Medium / Medium

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Nhập email hợp lệ kèm khoảng trắng (ví dụ: ` test@eshop.com `) và mật khẩu đúng.\n2. Nhấp đăng nhập và hệ thống từ chối đăng nhập.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Gửi email có khoảng trắng đầu hoặc cuối chuỗi lên API `/api/login` sẽ đăng nhập thất bại do backend không trim khoảng trắng trước khi xác thực thông tin tài khoản.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-09.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/39
- Labels: type:bug, status:open

---

# BUG-FR02-A-10: Không tích hợp cơ chế Rate Limiting chống tấn công Brute-force

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-008`

## Severity / Priority
High / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Gửi liên tục 15-20 request tới `/api/login` trong vòng vài giây.\n2. Tất cả đều trả về mã 401 bình thường thay vì bị chặn với mã 429.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Hệ thống chấp nhận số lượng yêu cầu đăng nhập tốc độ cao từ một IP mà không có giới hạn, dễ bị brute force.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-10.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/40
- Labels: type:bug, status:open

---

# BUG-FR02-A-11: Nút submit không hiển thị Loading và không bị khóa khi đang xử lý

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-009`

## Severity / Priority
Minor / Medium

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Nhấp nút Đăng nhập.\n2. Nút vẫn giữ nguyên chữ "Đăng nhập" và không bị disabled trong quá trình xử lý gửi API.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Trong quá trình gửi request đăng nhập lên API, nút submit không hiển thị trạng thái đang xoay/chờ và người dùng có thể bấm nhiều lần liên tục.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-11.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/41
- Labels: type:bug, status:open

---

# BUG-FR02-A-12: Không có nút Toggle ẩn/hiện mật khẩu trên biểu mẫu

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-010`

## Severity / Priority
Cosmetic / Low

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Xem ô nhập mật khẩu trên trang đăng nhập `/login`.\n2. Không có bất kỳ nút "Hiện" hay "Ẩn" nào kế bên.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Người dùng không thể tự chọn ẩn hay hiện mật khẩu để kiểm tra vì thiếu hoàn toàn nút/icon toggle ẩn hiện.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-12.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/42
- Labels: type:bug, status:open

---

# BUG-FR02-A-13: Token JWT không có thời hạn hết hạn (vô hạn hạn)

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-011`

## Severity / Priority
High / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Đăng nhập thành công và lấy chuỗi Token.\n2. Giải mã Token qua jwt.io và kiểm tra không tồn tại trường `exp`.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Token trả về khi đăng nhập thành công không cấu hình tham số `expiresIn`, cho phép truy cập vĩnh viễn không hết hạn.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-13.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/43
- Labels: type:bug, status:open

---

# BUG-FR02-A-14: Thiếu Route Guard ngăn truy cập lại trang Login khi đã đăng nhập

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-012`

## Severity / Priority
Medium / Medium

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Thực hiện đăng nhập thành công.\n2. Thay đổi đường dẫn URL trên trình duyệt thành `/login`.\n3. Trang biểu mẫu đăng nhập vẫn hiển thị bình thường.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Người dùng đã đăng nhập thành công vẫn có thể gõ trực tiếp URL `/login` để truy cập lại trang đăng nhập bình thường mà không bị redirect về Home.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-14.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/44
- Labels: type:bug, status:open

---

# BUG-FR02-A-15: Giao diện đăng nhập Admin thiếu nhãn thông tin, thiếu dấu * bắt buộc và nút hiện mật khẩu

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-013`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Di chuyển vào `frontend-admin` và khởi chạy giao diện admin bằng `npm run dev`.\n2. Truy cập `http://localhost:5174/` trên trình duyệt.\n3. Nhập dữ liệu `admin@eshop.com` vào trường Email (quan sát thấy gợi ý placeholder biến mất và không có nhãn label bên ngoài để hướng dẫn người dùng).\n4. Kiểm tra sự xuất hiện của dấu `*`, nút ẩn/hiện mật khẩu và ngôn ngữ nút bấm submit.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Giao diện Đăng nhập Admin (`http://localhost:5174/`) thiếu nhãn label mô tả trường thông tin (khiến placeholder biến mất khi nhập liệu), thiếu dấu hoa thị đỏ `*` bắt buộc, thiếu nút Toggle ẩn/hiện mật khẩu, nút submit bằng tiếng Anh và thiếu thuộc tính `type="email"` ở trường Email.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-15.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/45
- Labels: type:bug, status:open

---

# BUG-FR02-A-16: Thông báo lỗi đăng nhập Admin sử dụng alert() gây hiển thị chữ "Code" và vi phạm vị trí thông báo

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-004, TC-LOGIN-020, TC-LOGIN-021`

## Severity / Priority
Major / Medium

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Truy cập trang đăng nhập Web Admin tại `http://localhost:5174/`.\n2. Nhập thông tin tài khoản sai (ví dụ: `wrong@eshop.com` / `WrongPass123`).\n3. Bấm nút submit.\n4. Quan sát hộp thoại thông báo lỗi hiện lên trên màn hình.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Khi đăng nhập thất bại tại trang Admin (`http://localhost:5174/`), hệ thống sử dụng hàm `alert()` mặc định của trình duyệt để hiển thị lỗi. Việc này khiến tiêu đề hộp thoại hiển thị chữ `"Code"` (hoặc tên miền chạy local), đồng thời vi phạm đặc tả **FR-22** (yêu cầu thông báo lỗi phải hiển thị dạng chữ phía trên nút submit).

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-16.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/46
- Labels: type:bug, status:open

---

# BUG-FR02-A-17: Đặt lại mật khẩu thành công không giải phóng trạng thái khóa tài khoản và không reset bộ đếm lần đăng nhập sai

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-004`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Nhập mật khẩu sai 3 lần liên tiếp để khóa tài khoản `test_tc31@eshop.com`.\n2. Gọi API `/api/forgot-password` để lấy reset token.\n3. Gọi API `/api/reset-password` bằng reset token để cập nhật mật khẩu mới.\n4. Thử đăng nhập ngay bằng mật khẩu mới.\n5. Đăng nhập vẫn bị chặn bằng HTTP 403 do tài khoản vẫn bị hệ thống coi là đang trong trạng thái khóa.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Khi người dùng thực hiện đặt lại mật khẩu thành công bằng API `/api/reset-password`, hệ thống chỉ cập nhật trường `password` và `reset_token = NULL`, nhưng quên không reset bộ đếm số lần đăng nhập sai và mở khóa cho tài khoản trên hệ thống. Điều này khiến tài khoản vẫn giữ nguyên trạng thái bị khóa ngay cả khi người dùng đã cập nhật xong mật khẩu mới, bắt buộc người dùng phải đợi hết thời gian khóa mới đăng nhập được.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-17.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/47
- Labels: type:bug, status:open

---

# BUG-FR02-A-18: Giao diện đăng nhập Frontend che khuất lỗi khóa tài khoản (luôn hiện thông báo lỗi tĩnh)

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-...`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Nhập mật khẩu sai 3 lần để tài khoản bị khóa.\n2. Thử đăng nhập lại bằng mật khẩu ĐÚNG hoặc SAI.\n3. Kiểm tra thông báo lỗi hiển thị trên giao diện đăng nhập Frontend Web.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Khi người dùng đăng nhập vào tài khoản đang bị tạm khóa, mặc dù Backend API trả về lỗi HTTP 403 với nội dung `"Tài khoản đã bị khóa. Vui lòng thử lại sau."`, giao diện Frontend Web (giao diện đăng nhập) bắt ngoại lệ và gán lỗi tĩnh cứng: `"Đăng nhập thất bại. Vui lòng kiểm tra lại."`, khiến người dùng không biết tài khoản của mình đã bị tạm khóa.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-18.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/48
- Labels: type:bug, status:open

---

# BUG-FR02-A-19: API và giao diện thiếu cảnh báo số lần đăng nhập sai còn lại trước khi khóa

## Feature
FR-02 – Đăng nhập & Khóa tài khoản

## Found by Test Case
`TC-LOGIN-030`

## Severity / Priority
Major / Medium

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Đăng nhập sai mật khẩu lần 1 hoặc lần 2.\n2. Kiểm tra phản hồi JSON từ Backend API `/api/login` (không thấy trường thông tin số lần còn lại).\n3. Kiểm tra thông báo hiển thị trên Frontend Web (không có cảnh báo đếm ngược số lần thử).

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-02.

## Actual Result
Hệ thống hoàn toàn thiếu cơ chế cảnh báo số lần đăng nhập sai còn lại. Khi người dùng nhập sai mật khẩu, API backend chỉ phản hồi lỗi chung `"Invalid email or password"` mà không đính kèm thông tin số lần còn lại, và Frontend Web không hiển thị bất kỳ cảnh báo đếm ngược số lần còn lại trước khi tài khoản bị tạm khóa.

## Evidence
- Screenshot: ![Screenshot](tests/bug/login/evidences/BUG-FR02-A-19.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: https://github.com/trngnneee/eshop-sut/issues/49
- Labels: type:bug, status:open

---

# BUG-FR07-B-01: Backend API không validate số lượng sản phẩm thêm vào giỏ hàng

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-044, TC-CART-045, TC-CART-046, TC-CART-047`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
API thêm sản phẩm vào giỏ hàng (`POST /api/cart`) chấp nhận mọi số lượng sản phẩm không hợp lệ (như 0, số âm, số thập phân, hoặc bỏ trống) mà không trả về lỗi validate.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-01.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-02: Backend API không cộng dồn số lượng cho sản phẩm trùng ID

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-043`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
API thêm sản phẩm vào giỏ hàng (`POST /api/cart`) không cộng dồn số lượng cho các mặt hàng trùng mã sản phẩm (ID), dẫn đến tạo nhiều dòng sản phẩm trùng lặp trong giỏ hàng.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-02.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-03: Frontend CartContext không cộng dồn số lượng khi thêm sản phẩm trùng

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-012`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
Trên giao diện Web, khi thêm cùng một sản phẩm nhiều lần vào giỏ hàng, hệ thống không tự động cộng dồn số lượng mà hiển thị thành nhiều dòng sản phẩm trùng lặp trong giỏ hàng.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-03.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-04: Trang giỏ hàng thiếu nút tăng giảm số lượng (+/-) và nhập số lượng trực tiếp

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-015, TC-CART-016, TC-CART-017, TC-CART-018, TC-CART-019, TC-CART-020, TC-CART-021, TC-CART-022, TC-CART-023, TC-CART-024, TC-CART-025`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
Trang giỏ hàng `/cart` hiển thị số lượng sản phẩm dưới dạng text tĩnh và không có các nút '+' / '-' hay ô nhập liệu, khiến người dùng không thể điều chỉnh số lượng.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-04.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-05: Thiếu Confirm Dialog xác nhận khi xóa sản phẩm khỏi giỏ hàng

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-031, TC-CART-032, TC-CART-033, TC-CART-075`

## Severity / Priority
Minor / Medium

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
Nút 'Xóa' sản phẩm trực tiếp kích hoạt hàm `removeFromCart` xóa bản ghi ngay lập tức mà không hiển thị hộp thoại xác nhận (Confirm Dialog), tăng nguy cơ xóa nhầm dữ liệu.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-05.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-06: Nhãn hiển thị tổng tiền không đúng đặc tả ('Tổng tạm tính' thay vì 'Tổng cộng')

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-009`

## Severity / Priority
Minor / Low

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
Trang `/cart` hiển thị nhãn tổng số tiền của giỏ hàng là 'Tổng tạm tính' thay vì 'Tổng cộng' như yêu cầu trong đặc tả.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-06.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-07: Trạng thái giỏ hàng trống thiếu hình ảnh/icon minh họa trực quan

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-002`

## Severity / Priority
Minor / Low

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
Khi giỏ hàng trống, giao diện chỉ hiển thị dòng chữ thông báo và nút quay về mà thiếu hình ảnh hoặc biểu tượng (icon) trực quan minh họa.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-07.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-08: Trang giỏ hàng thiếu thanh breadcrumb điều hướng

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-004`

## Severity / Priority
Minor / Low

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
Giao diện trang `/cart` thiếu thanh breadcrumb dạng 'Trang chủ > Giỏ hàng' để định vị và giúp điều hướng ngược lại.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-08.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-09: Không cần đăng nhập vẫn cho phép thêm sản phẩm vào giỏ hàng

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-...`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
Hệ thống cho phép người dùng chưa đăng nhập thực hiện thêm sản phẩm vào giỏ hàng thành công (không yêu cầu token xác thực hoặc không chặn ở Frontend/Backend), dẫn đến việc giỏ hàng hoạt động không có định danh người dùng.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-09.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-10: Backend API không validate tính toàn vẹn của sản phẩm thêm vào giỏ hàng

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-051, TC-CART-053, TC-CART-057, TC-CART-058, TC-CART-059`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
API `POST /api/cart` không validate sự tồn tại và tính hợp lệ của các trường bắt buộc như `id` và `price`. Backend chấp nhận thêm sản phẩm thiếu ID, thiếu giá, hoặc giá <= 0 vào giỏ hàng.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-10.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-11: Thiếu thông báo phản hồi (toast/alert) khi thêm sản phẩm vào giỏ hàng thành công

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-010, TC-CART-011, TC-CART-038, TC-CART-074`

## Severity / Priority
Minor / Medium

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
Giao diện không hiển thị bất kỳ thông báo (toast/alert/popup) nào để thông báo cho người dùng biết sản phẩm đã được thêm vào giỏ hàng thành công, vi phạm yêu cầu phản hồi trạng thái của FR-24.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-11.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-12: Không hiển thị số lượng hàng tồn kho khả dụng và thiếu cảnh báo khi số lượng vượt quá hàng tồn

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-060, TC-CART-079`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce
1. Đăng nhập và truy cập trang chi tiết của một sản phẩm (ví dụ: sản phẩm chỉ còn 3 cái trong kho).\n2. Quan sát giao diện (không thấy thông tin hiển thị số lượng sản phẩm khả dụng trong kho).\n3. Thử tăng số lượng mua lên thành 10 cái (hoặc một số lượng bất kỳ vượt quá mức tồn kho).\n4. Nhấp nút "Thêm vào giỏ hàng" hoặc quan sát phản hồi trên giao diện.

## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
Trên giao diện chi tiết sản phẩm và giỏ hàng, hệ thống không hiển thị số lượng sản phẩm còn lại trong kho. Đồng thời, khi người dùng chọn hoặc nhập số lượng mua lớn hơn số lượng hàng tồn kho khả dụng thực tế, hệ thống vẫn cho phép thực hiện hoặc không hiển thị bất kỳ cảnh báo/lỗi nào để người dùng biết.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-12.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-13: Backend API cho phép giả mạo đơn giá của sản phẩm (Price Tampering)

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-063, TC-CART-064, TC-CART-080`

## Severity / Priority
Critical / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
API `POST /api/cart` trực tiếp sử dụng giá trị `price` truyền từ Client-side và lưu vào giỏ hàng mà không đối chiếu với giá trị thực tế trong Cơ sở dữ liệu.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-13.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-14: Backend API chấp nhận productId không tồn tại và tạo ra sản phẩm ma

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-061, TC-CART-062, TC-CART-078`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
API `POST /api/cart` không kiểm tra sự tồn tại của sản phẩm (`productId`) trong bảng cơ sở dữ liệu `products`, dẫn đến việc thêm các sản phẩm không có thực hoặc sai tên vào giỏ hàng.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-14.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-15: Backend API không kiểm tra kiểu dữ liệu của trường quantity (Type Validation)

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-065, TC-CART-066, TC-CART-067, TC-CART-068`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
API `POST /api/cart` chấp nhận lưu trữ các giá trị số lượng `quantity` không phải số nguyên như chuỗi ký tự `"2"` hoặc giá trị `null` mà không báo lỗi.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-15.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-16: Lỗ hổng cho phép gán thuộc tính đặc quyền (Mass Assignment / Extra Fields)

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-070`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
API `POST /api/cart` chấp nhận lưu trữ và trả về tất cả các trường dữ liệu thừa gửi lên từ client-side như `isAdmin: true` hay `discount: 90` mà không thực hiện lọc bỏ.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-16.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-17: Giao diện cho phép thanh toán (Checkout) khi giỏ hàng trống

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-076, TC-CART-077`

## Severity / Priority
Major / Medium

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
Giao diện giỏ hàng `/cart` không vô hiệu hóa nút Thanh toán và không chặn chuyển hướng sang `/checkout` khi giỏ hàng hoàn toàn trống rỗng hoặc chứa số lượng sản phẩm không hợp lệ.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-17.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-18: Thiếu xử lý lỗi kết nối mạng hoặc sập máy chủ trên giao diện

## Feature
FR-07 – Giỏ hàng

## Found by Test Case
`TC-CART-...`

## Severity / Priority
Major / Medium

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- SUT backend & frontend are running and database has test accounts.

## Steps to Reproduce


## Expected Result
SUT hoạt động đúng theo tài liệu đặc tả FR-07.

## Actual Result
Khi API thêm sản phẩm thất bại do mất kết nối mạng hoặc sập server, Frontend vẫn tự động tăng số lượng badge trên Navbar mà không hiển thị thông báo lỗi phù hợp cho người dùng.

## Evidence
- Screenshot: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-18.png)
- Video: N/A
- Console/API log nếu có: N/A

## GitHub Issue
- Link: Local issue (Not pushed to GitHub)
- Labels: type:bug

---

# BUG-FR07-B-19: Giỏ hàng không được làm sạch sau khi thanh toán thành công (checkout success)

## Feature
FR-07 – Giỏ hàng (Shopping Cart)

## Found by Test Case
`TC-CART-089`

## Severity / Priority
Major / High

## Environment
- OS: Windows 11
- Browser: Chrome
- App URL: http://localhost:5173
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- User has logged in and has items in their cart.
- User is on the checkout page `/checkout`.

## Steps to Reproduce
1. Đăng nhập và thêm sản phẩm vào giỏ hàng.
2. Nhấn nút Thanh toán để chuyển sang trang `/checkout`.
3. Bấm nút Thanh toán trên trang checkout để hoàn thành đơn hàng.
4. Nhận thông báo "Thanh toán thành công!".
5. Nhấp nút "Quay lại trang chủ" và mở lại trang giỏ hàng `/cart` hoặc xem badge giỏ hàng trên Navbar.

## Expected Result
Giỏ hàng phải được xóa sạch hoàn toàn sau khi thanh toán thành công, badge giỏ hàng hiển thị số 0.

## Actual Result
Sau khi thanh toán đơn hàng thành công, giỏ hàng không tự động làm trống, các sản phẩm đã thanh toán vẫn tiếp tục hiển thị trong giỏ hàng.

## Evidence
- Giao diện thanh toán Web: ![Evidence](tests/bug/cart/evidences/BUG-FR07-B-19.png)

---

## 3. Summary of Dashboard Bugs (FR-13)

| Bug ID | Title | Severity | Priority | Related Test Case | GitHub Issue |
|---|---|---|---|---|---|
| BUG-FR13-C-01 | Giao diện Dashboard hiển thị Tổng doanh thu bị nhân đôi | Major | High | [`TC-DASHBOARD-DT-001`](tests/test-cases/dashboard/TC-DASHBOARD-DT-001.md), [`TC-DASHBOARD-BVA-006`](tests/test-cases/dashboard/TC-DASHBOARD-BVA-006.md), [`TC-DASHBOARD-DT-023`](tests/test-cases/dashboard/TC-DASHBOARD-DT-023.md) | [Issue #156](https://github.com/trngnneee/eshop-sut/issues/156) |
| BUG-FR13-C-02 | Backend API `/api/admin/orders` và `/api/admin/users` thiếu kiểm soát phân quyền (role) | Critical | High | [`TC-DASHBOARD-DT-004`](tests/test-cases/dashboard/TC-DASHBOARD-DT-004.md), [`TC-DASHBOARD-DT-013`](tests/test-cases/dashboard/TC-DASHBOARD-DT-013.md), [`TC-DASHBOARD-DT-014`](tests/test-cases/dashboard/TC-DASHBOARD-DT-014.md), [`TC-DASHBOARD-DT-024`](tests/test-cases/dashboard/TC-DASHBOARD-DT-024.md) | [Issue #157](https://github.com/trngnneee/eshop-sut/issues/157) |
| BUG-FR13-C-03 | Lỗi API `/api/admin/users` 500 ngắt toàn bộ tiến trình fetchData của dashboard | Medium | Medium | [`TC-DASHBOARD-DT-017`](tests/test-cases/dashboard/TC-DASHBOARD-DT-017.md) | [Issue #158](https://github.com/trngnneee/eshop-sut/issues/158) |
| BUG-FR13-C-04 | Order thiếu `total_amount` dẫn đến tính toán ra `NaN ₫` hiển thị trên giao diện | Medium | Medium | [`TC-DASHBOARD-DT-020`](tests/test-cases/dashboard/TC-DASHBOARD-DT-020.md) | [Issue #159](https://github.com/trngnneee/eshop-sut/issues/159) |
| BUG-FR13-C-05 | Giao diện hiển thị trực tiếp số liệu thống kê âm hoặc thập phân mà không kiểm tra tính hợp lệ dữ liệu | Minor | Low | [`TC-DASHBOARD-BVA-018`](tests/test-cases/dashboard/TC-DASHBOARD-BVA-018.md), [`TC-DASHBOARD-BVA-019`](tests/test-cases/dashboard/TC-DASHBOARD-BVA-019.md) | [Issue #160](https://github.com/trngnneee/eshop-sut/issues/160) |

---

## 4. Detailed Bug Reports for Dashboard (FR-13)

# BUG-FR13-C-01: Giao diện Dashboard hiển thị Tổng doanh thu bị nhân đôi

## Feature
FR-13 – Dashboard

## Found by Test Case
`TC-DASHBOARD-DT-001, TC-DASHBOARD-BVA-006`

## Severity / Priority
Major / High

## Environment
- OS: Windows
- Browser: Chrome
- App URL: http://localhost:5174 (Web Admin)
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- Admin logged in and navigating to Dashboard.

## Steps to Reproduce
1. Đăng nhập hệ thống bằng tài khoản admin.
2. Điều hướng tới Dashboard của Web Admin (`http://localhost:5174`).
3. Kiểm tra số hiển thị ở 'Tổng doanh thu (Delivered)'.
4. So sánh số hiển thị này với tổng số tiền thực tế của các đơn hàng đã giao (`delivered`) có trong database.

## Expected Result
Tổng doanh thu hiển thị trên Dashboard phải bằng chính xác tổng số tiền của các đơn hàng có trạng thái "delivered". Không có hiện tượng nhân đôi số tiền.

## Actual Result
Doanh thu hiển thị bị nhân đôi.

## Evidence
- Giao diện Dashboard hiển thị sai lệch số liệu: ![Evidence](tests/bug/dashboard/evidences/BUG-FR13-C-01.png)

---

# BUG-FR13-C-02: Backend API `/api/admin/orders` và `/api/admin/users` thiếu kiểm soát phân quyền (role)

## Feature
FR-13 – Dashboard (Security)

## Found by Test Case
`TC-DASHBOARD-DT-004`

## Severity / Priority
Critical / High

## Environment
- OS: Windows
- App URL: http://localhost:5174 (Web Admin)
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- User has logged in and has a valid JWT token, but user role is customer/user (not admin).

## Steps to Reproduce
1. Đăng nhập bằng tài khoản người dùng thông thường (Customer) và lấy mã token JWT xác thực phiên làm việc.
2. Gửi request GET tới endpoint `/api/admin/orders` hoặc `/api/admin/users` kèm theo mã token vừa lấy.
3. Quan sát kết quả phản hồi từ hệ thống.

## Expected Result
Hệ thống từ chối truy cập và trả về mã lỗi `403 Forbidden` do tài khoản không có quyền Admin.

## Actual Result
Backend trả về HTTP 200 OK kèm danh sách dữ liệu nhạy cảm.

## Evidence
- Giao diện API trả về HTTP 200 thành công: ![Evidence](tests/bug/dashboard/evidences/BUG-FR13-C-02.png)

# BUG-FR13-C-03: Lỗi API /api/admin/users 500 ngắt toàn bộ tiến trình fetchData của dashboard

## Feature
FR-13 – Dashboard (Robustness)

## Found by Test Case
`TC-DASHBOARD-DT-017`

## Severity / Priority
Medium / Medium

## Environment
- OS: Windows
- Browser: Chrome
- App URL: http://localhost:5174 (Web Admin)
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- Admin logged in.
- API `/api/admin/users` returns HTTP 500.

## Steps to Reproduce
1. Đăng nhập admin.
2. Giả lập hoặc mock API `/api/admin/users` trả về mã lỗi HTTP 500.
3. Mở giao diện Dashboard.
4. Quan sát hiển thị của các card doanh thu, đơn hàng, danh mục (chúng không hiển thị số liệu hoặc giữ số liệu cũ).

## Expected Result
Một API lỗi không được làm ngắt quãng các API độc lập khác. Giao diện vẫn hiển thị bình thường dữ liệu doanh thu, đơn hàng... và hiển thị fallback lỗi ở riêng card người dùng.

## Actual Result
Tiến trình fetchData bị ngắt hoàn toàn khi gọi API đầu tiên bị lỗi, làm trắng Dashboard hoặc mất số liệu của tất cả các card khác.

## Evidence
- Giao diện Dashboard trắng/mất số liệu: ![Evidence](tests/bug/dashboard/evidences/BUG-FR13-C-03.png)

---

# BUG-FR13-C-04: Order thiếu total_amount dẫn đến tính toán ra NaN hiển thị trên giao diện

## Feature
FR-13 – Dashboard (Robustness)

## Found by Test Case
`TC-DASHBOARD-DT-020`

## Severity / Priority
Medium / Medium

## Environment
- OS: Windows
- App URL: http://localhost:5174 (Web Admin)
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- Admin logged in.
- Orders in API response contain at least one order object missing `total_amount`.

## Steps to Reproduce
1. Đăng nhập admin.
2. Mock API `/api/admin/orders` trả về mảng orders chứa order thiếu thuộc tính `total_amount` (ví dụ: `undefined` hoặc `null`).
3. Mở Dashboard.
4. Quan sát số hiển thị ở 'Tổng doanh thu (Delivered)' hiển thị `NaN ₫`.

## Expected Result
Dashboard bỏ qua order lỗi hoặc mặc định giá trị bằng 0 và không bị tính toán ra `NaN`.

## Actual Result
Doanh thu hiển thị là `NaN ₫` do phép cộng với `undefined` trong hàm `reduce`.

## Evidence
- Giao diện Dashboard hiển thị lỗi NaN: ![Evidence](tests/bug/dashboard/evidences/BUG-FR13-C-04.png)

---

# BUG-FR13-C-05: Giao diện hiển thị trực tiếp số liệu thống kê âm hoặc thập phân mà không kiểm tra tính hợp lệ dữ liệu

## Feature
FR-13 – Dashboard (UI/UX)

## Found by Test Case
`TC-DASHBOARD-BVA-018, TC-DASHBOARD-BVA-019`

## Severity / Priority
Minor / Low

## Environment
- OS: Windows
- App URL: http://localhost:5174 (Web Admin)
- Backend/API URL: http://localhost:3000
- Commit hash: N/A

## Preconditions
- Admin logged in.
- Mock API trả về số lượng users = -1, số lượng products = 10.5.

## Steps to Reproduce
1. Đăng nhập admin.
2. Giả lập API users/products trả về số lượng `-1` hoặc số lượng `10.5`.
3. Mở Dashboard.
4. Quan sát card số lượng người dùng hiển thị `-1` và số lượng sản phẩm hiển thị `10.5`.

## Expected Result
UI có validate để làm tròn số lượng (sản phẩm) hoặc fallback về 0 (đối với số âm), không hiển thị các giá trị bất hợp lý.

## Actual Result
UI hiển thị trực tiếp giá trị thô nhận được từ API: `-1` người dùng và `10.5` sản phẩm.

## Evidence
- Giao diện hiển thị trực tiếp dữ liệu thô: ![Evidence](tests/bug/dashboard/evidences/BUG-FR13-C-05.png)

---

## 4. Summary of Mobile Cart & Checkout Bugs (FR-21)

| Bug ID | Title | Severity | Priority | Related Test Case | GitHub Issue |
|---|---|---|---|---|---|
| BUG-FR21-D-01 | Giao dịch Checkout thiếu thuộc tính địa chỉ giao hàng gửi lên API | Major | High | [`TC-MOBILE-CART-DT-019`](tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-019.md) | [Issue #161](https://github.com/trngnneee/eshop-sut/issues/161) |
| BUG-FR21-D-02 | Nhập số lượng trực tiếp trong giỏ hàng bị cộng thêm 1 đơn vị | Major | High | [`TC-MOBILE-CART-DT-007`](tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-007.md) | [Issue #162](https://github.com/trngnneee/eshop-sut/issues/162) |
| BUG-FR21-D-03 | Hồ sơ mobile không chấp nhận số điện thoại bắt đầu bằng số 0 | Medium | High | [`TC-MOBILE-CART-DT-015`](tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-015.md), [`TC-MOBILE-CART-BVA-009`](tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-009.md) | [Issue #163](https://github.com/trngnneee/eshop-sut/issues/163) |
| BUG-FR21-D-04 | API `/api/checkout` thiếu kiểm định tính toàn vẹn của đơn giá (Price Tampering) | Critical | High | [`TC-MOBILE-CART-DT-018`](tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-018.md) | [Issue #164](https://github.com/trngnneee/eshop-sut/issues/164) |
| BUG-FR21-D-05 | Hệ thống không áp dụng được mã giảm giá khi tổng giá trị đơn hàng bằng đúng giá trị tối thiểu quy định | Major | High | [`TC-MOBILE-CART-BVA-023`](tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-023.md) | [Issue #165](https://github.com/trngnneee/eshop-sut/issues/165) |
| BUG-FR21-D-06 | API áp dụng mã giảm giá tính sai số tiền giảm giá phần trăm (percent) | Critical | High | [`TC-MOBILE-CART-DT-020`](tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-020.md) | [Issue #166](https://github.com/trngnneee/eshop-sut/issues/166) |

---

## 5. Detailed Bug Reports for Mobile Cart & Checkout (FR-21)



# BUG-FR21-D-01: Giao dịch Checkout thiếu thuộc tính địa chỉ giao hàng gửi lên API

## Feature
FR-21 – Mobile Cart & Checkout

## Found by Test Case
`TC-MOBILE-CART-DT-019`

## Severity / Priority
Major / High

## Environment
- OS: iOS / Android (Mobile App)

## Preconditions
- Khách hàng đã thiết lập địa chỉ giao hàng trong profile của mình.

## Steps to Reproduce
1. Đăng nhập vào ứng dụng di động và thiết lập địa chỉ giao hàng trong hồ sơ cá nhân.<br>2. Thêm sản phẩm vào giỏ hàng và tiến hành thanh toán.<br>3. Tại màn hình Checkout, bấm 'Xác nhận thanh toán'.<br>4. Kiểm tra thông tin đơn hàng vừa tạo trên hệ thống: địa chỉ giao hàng của đơn hàng bị để trống.

## Expected Result
Đơn hàng được lưu giữ đầy đủ địa chỉ giao hàng lấy từ profile của người dùng hoặc do mobile gửi lên.

## Actual Result
Khi thực hiện đặt hàng trên ứng dụng di động, thông tin địa chỉ giao hàng không được gửi kèm theo đơn hàng, dẫn đến đơn hàng mới được tạo trên hệ thống bị bỏ trống trường địa chỉ giao hàng.

## Evidence
- Đơn hàng mới bị trống địa chỉ giao hàng: ![Evidence](tests/bug/mobile-cart/evidences/BUG-FR21-D-01.jpg)

## GitHub Issue
- Status: Open

---

# BUG-FR21-D-02: Nhập số lượng trực tiếp trong giỏ hàng bị cộng thêm 1 đơn vị

## Feature
FR-21 – Mobile Cart & Checkout

## Found by Test Case
`TC-MOBILE-CART-DT-007`

## Severity / Priority
Major / High

## Environment
- OS: iOS / Android (Mobile App)

## Preconditions
- Có sản phẩm trong giỏ hàng trên mobile app.

## Steps to Reproduce
1. Đăng nhập vào ứng dụng di động.<br>2. Thêm 1 sản phẩm vào giỏ hàng.<br>3. Mở giỏ hàng, tại ô nhập số lượng, nhập trực tiếp số lượng là 2.<br>4. Quan sát số hiển thị thực tế trên ô nhập liệu (sẽ bị nhảy thành 3).

## Expected Result
Số lượng hiển thị đúng bằng giá trị số người dùng đã nhập.

## Actual Result
Giao diện giỏ hàng trên ứng dụng di động tự động tăng số lượng sản phẩm thêm 1 đơn vị so với số lượng người dùng thực tế nhập trực tiếp vào ô số lượng.

## Evidence
- Số lượng tự tăng thêm 1 trên giao diện: ![Evidence](tests/bug/mobile-cart/evidences/BUG-FR21-D-02.jpg)

## GitHub Issue
- Status: Open

---

# BUG-FR21-D-03: Hồ sơ mobile không chấp nhận số điện thoại bắt đầu bằng số 0

## Feature
FR-21 – Mobile Cart & Checkout

## Found by Test Case
`TC-MOBILE-CART-DT-015, TC-MOBILE-CART-BVA-009`

## Severity / Priority
Medium / High

## Environment
- OS: iOS / Android (Mobile App)

## Preconditions
- Đăng nhập tài khoản user di động, đang ở tab Hồ sơ.

## Steps to Reproduce
1. Đăng nhập vào ứng dụng di động và vào trang Profile.<br>2. Nhập số điện thoại hợp lệ ở Việt Nam (ví dụ: 0912345678) vào ô Số điện thoại.<br>3. Nhấn nút 'Cập nhật'.<br>4. Quan sát thông báo lỗi.

## Expected Result
Hệ thống chấp nhận số điện thoại hợp lệ ở Việt Nam bắt đầu bằng chữ số 0.

## Actual Result
Tại phần cập nhật hồ sơ cá nhân trên ứng dụng di động, hệ thống không chấp nhận số điện thoại bắt đầu bằng chữ số 0, dẫn đến việc từ chối các số điện thoại hợp lệ tại Việt Nam (luôn bắt đầu bằng số 0) và báo lỗi định dạng.

## Evidence
- Lỗi từ chối số điện thoại đầu số 0: ![Evidence](tests/bug/mobile-cart/evidences/BUG-FR21-D-03.jpg)

## GitHub Issue
- Status: Open

---

# BUG-FR21-D-04: API `/api/checkout` thiếu kiểm định tính toàn vẹn của đơn giá (Price Tampering)

## Feature
FR-21 – Mobile Cart & Checkout

## Found by Test Case
`TC-MOBILE-CART-DT-018`

## Severity / Priority
Critical / High

## Environment
- OS: Cross-platform (Backend API)

## Preconditions
- Người dùng gửi yêu cầu đặt hàng.

## Steps to Reproduce
1. Đăng nhập và thêm sản phẩm có giá trị cao (ví dụ: 30,000,000 ₫) vào giỏ hàng.<br>2. Nhấn thanh toán trên giao diện ứng dụng.<br>3. Sử dụng công cụ chặn request (như Proxy/Burp Suite) để bắt và can thiệp request thanh toán (`POST /api/checkout`).<br>4. Sửa giá trị tổng số tiền (`total_amount`) trong nội dung request thành 1,000 ₫ và gửi lên hệ thống.<br>5. Quan sát phản hồi: hệ thống báo thanh toán thành công.<br>6. Kiểm tra thông tin đơn hàng trên hệ thống: đơn hàng được ghi nhận thành công với tổng số tiền thanh toán là 1,000 ₫.

## Expected Result
Backend API phải tự tính lại tổng tiền dựa trên các sản phẩm đặt mua và đơn giá lưu giữ trong DB, từ chối tạo đơn nếu tổng tiền client gửi lên bị sai lệch.
 
## Actual Result
API thanh toán (`POST /api/checkout`) chấp nhận trực tiếp tổng số tiền (`total_amount`) do người dùng truyền lên mà không kiểm tra đối sánh giá trị thực tế của các mặt hàng, cho phép người dùng thay đổi giá trị đơn hàng tùy ý (Price Tampering).
 
## Evidence
- Đơn hàng tạo thành công với số tiền bị sửa đổi: ![Evidence](tests/bug/mobile-cart/evidences/BUG-FR21-D-04.png)
 
## GitHub Issue
- Status: Open
 
---
 
# BUG-FR21-D-05: Hệ thống không áp dụng được mã giảm giá khi tổng giá trị đơn hàng bằng đúng giá trị tối thiểu quy định
 
## Feature
FR-21 – Mobile Cart & Checkout
 
## Found by Test Case
`TC-MOBILE-CART-BVA-023`
 
## Severity / Priority
Major / High
 
## Environment
- OS: Cross-platform (Backend API)
 
## Preconditions
- Đăng nhập tài khoản khách hàng thành công.
- Mã giảm giá "SAVE10" (yêu cầu tối thiểu 300,000 ₫) đang hoạt động.
 
## Steps to Reproduce
1. Đăng nhập vào ứng dụng di động.<br>2. Thêm các sản phẩm vào giỏ hàng sao cho tổng số tiền tạm tính đúng bằng 300,000 ₫.<br>3. Điều hướng tới trang Checkout, nhập mã giảm giá "SAVE10" và nhấn "Áp dụng".
 
## Expected Result
Mã giảm giá áp dụng thành công, tổng tiền được giảm 10% (30,000 ₫) và người dùng tiếp tục các bước thanh toán.
 
## Actual Result
Hệ thống báo lỗi: "Đơn hàng chưa đủ giá trị tối thiểu 300,000 ₫ để áp dụng mã này" do biểu thức logic so sánh lớn hơn (`>`) thay vì lớn hơn hoặc bằng (`>=`).
 
## Evidence
- Lỗi từ chối áp dụng mã giảm giá tại biên tối thiểu: ![Evidence](tests/bug/mobile-cart/evidences/BUG-FR21-D-05.jpg)
 
## GitHub Issue
- Status: Open
 
---
 
# BUG-FR21-D-06: API áp dụng mã giảm giá tính sai số tiền giảm giá phần trăm (percent)
 
## Feature
FR-21 – Mobile Cart & Checkout
 
## Found by Test Case
`TC-MOBILE-CART-DT-020`
 
## Severity / Priority
Critical / High
 
## Environment
- OS: Cross-platform (Backend API)
 
## Preconditions
- Đăng nhập tài khoản khách hàng thành công.
- Mã giảm giá "SAVE10" (giảm 10% - tỷ lệ 0.1) đang hoạt động.
 
## Steps to Reproduce
1. Đăng nhập vào ứng dụng di động.<br>2. Thêm sản phẩm trị giá 350,000 ₫ vào giỏ hàng và thanh toán.<br>3. Nhập mã giảm giá "SAVE10" và nhấn "Áp dụng".<br>4. Kiểm tra số tiền được khấu trừ.
 
## Expected Result
Số tiền giảm giá được tính là: 350,000 ₫ * 0.1 = 35,000 ₫. Tổng tiền thanh toán cuối cùng là 315,000 ₫.
 
## Actual Result
Số tiền giảm giá bị tính sai thành: 350,000 ₫ * (1 - 0.1) = 315,000 ₫ (tương đương giảm giá tới 90%), tổng tiền thanh toán cuối cùng chỉ còn 35,000 ₫.
 
## Evidence
- API phản hồi sai số tiền giảm giá phần trăm: ![Evidence](tests/bug/mobile-cart/evidences/BUG-FR21-D-06.jpg)
 
## GitHub Issue
- Status: Open
