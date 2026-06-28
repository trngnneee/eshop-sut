# FR-02 – Authentication & Lockout

## 1. Feature Overview
- Pool: Pool A (Authentication & Authorization)
- Actor: Customer / Web Admin / System
- Related UI: `/login` (Web), `/login` (Admin)
- Related API: `POST /api/login`, `POST /api/admin/login`
- Preconditions: User account has been registered in the database.
- Business Rules: Lockout after 3 consecutive failures, lockout duration is 30s in demo environment, JWT token returned upon success.

## 2. Domain Testing Summary
- Link/detail: [tests/test-cases/login/](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-cases/login/)
- Number of Domain Test Cases: 41
- Main valid partitions: Đúng email + mật khẩu, Định dạng email hợp lệ, Casing mật khẩu chính xác
- Main invalid partitions: Sai email/mật khẩu, Thiếu email/mật khẩu, Sai định dạng email, Mật khẩu quá ngắn/quá dài
- Human review notes: AI ban đầu bỏ sót việc phân vùng kiểm thử độ nhạy chữ hoa/thường (casing) của email và tab navigation accessibility.

## 3. Boundary Value Analysis Summary
- Link/detail: [tests/test-cases/login/](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-cases/login/)
- Boundary variables: Độ dài email, độ dài mật khẩu, số lần thử sai, thời gian khóa
- Number of BVA Test Cases: 19
- Important boundary values: Password length (7, 8, 9, 39, 40, 41), Attempts count (2, 3, 4), Duration (29s, 30s, 31s)
- Human review notes: BVA phát hiện SUT đặt thời gian khóa cứng là 180s thay vì 30s trong database backend.

## 4. Test Execution Summary
| Total TC | Executed | Passed | Failed | Blocked | Not Executed |
|---|---:|---:|---:|---:|---:|
| 80 | 30 | 11 | 19 | 0 | 50 |

## 5. Bugs Found
| Bug ID | Title | Related Test Case | Severity | Priority | GitHub Issue | Evidence |
|---|---|---|---|---|---|---|
| BUG-FR02-A-01 | Bộ đếm đăng nhập sai tăng thêm 2 đơn vị thay vì 1 | TC-LOGIN-002, TC-LOGIN-023 | Major | High | [Issue #31](https://github.com/trngnneee/eshop-sut/issues/31) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/evidences/BUG-FR02-A-01.png) |
| BUG-FR02-A-02 | Thời gian khóa tài khoản bị thiết lập sai thành 3 phút | TC-LOGIN-003, TC-LOGIN-014, TC-LOGIN-025 | Medium | High | [Issue #32](https://github.com/trngnneee/eshop-sut/issues/32) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/evidences/BUG-FR02-A-02.png) |
| BUG-FR02-A-03 | Race condition do xử lý yêu cầu đăng nhập bất đồng bộ | TC-LOGIN-002, TC-LOGIN-013, TC-LOGIN-023, TC-LOGIN-024 | Major | High | [Issue #33](https://github.com/trngnneee/eshop-sut/issues/33) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/../evidence/BUG-FR02-A-03_screenshot.png) |
| BUG-FR02-A-04 | Tiêu đề trang Đăng nhập hiển thị sai thành "Đăng Ký" | TC-LOGIN-004 | Minor | Medium | [Issue #34](https://github.com/trngnneee/eshop-sut/issues/34) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/evidences/BUG-FR02-A-04.png) |
| BUG-FR02-A-05 | Trường nhập Email hiển thị nhãn là "Username" | TC-LOGIN-004 | Minor | Medium | [Issue #35](https://github.com/trngnneee/eshop-sut/issues/35) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/evidences/BUG-FR02-A-05.png) |
| BUG-FR02-A-06 | Nút submit biểu mẫu sử dụng tiếng Anh "Sign In" | TC-LOGIN-004 | Minor | Medium | [Issue #36](https://github.com/trngnneee/eshop-sut/issues/36) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/evidences/BUG-FR02-A-06.png) |
| BUG-FR02-A-07 | Mật khẩu hiển thị ở dạng plain text (type="text") | TC-LOGIN-004 | Critical | High | [Issue #37](https://github.com/trngnneee/eshop-sut/issues/37) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/evidences/BUG-FR02-A-07.png) |
| BUG-FR02-A-08 | Thiếu dấu hoa thị màu đỏ * đánh dấu trường bắt buộc | TC-LOGIN-004 | Cosmetic | Low | [Issue #38](https://github.com/trngnneee/eshop-sut/issues/38) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/evidences/BUG-FR02-A-08.png) |
| BUG-FR02-A-09 | Thiếu trim khoảng trắng của Email ở phía Backend | TC-LOGIN-005 | Medium | Medium | [Issue #39](https://github.com/trngnneee/eshop-sut/issues/39) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/evidences/BUG-FR02-A-09.png) |
| BUG-FR02-A-10 | Không tích hợp cơ chế Rate Limiting chống tấn công Brute-force | TC-LOGIN-008 | High | High | [Issue #40](https://github.com/trngnneee/eshop-sut/issues/40) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/evidences/BUG-FR02-A-10.png) |
| BUG-FR02-A-11 | Nút submit không hiển thị Loading và không bị khóa khi đang xử lý | TC-LOGIN-009 | Minor | Medium | [Issue #41](https://github.com/trngnneee/eshop-sut/issues/41) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/../evidence/BUG-FR02-A-11_screenshot.png) |
| BUG-FR02-A-12 | Không có nút Toggle ẩn/hiện mật khẩu trên biểu mẫu | TC-LOGIN-010 | Cosmetic | Low | [Issue #42](https://github.com/trngnneee/eshop-sut/issues/42) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/evidences/BUG-FR02-A-12.png) |
| BUG-FR02-A-13 | Token JWT không có thời hạn hết hạn (vô hạn hạn) | TC-LOGIN-011 | High | High | [Issue #43](https://github.com/trngnneee/eshop-sut/issues/43) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/evidences/BUG-FR02-A-13.png) |
| BUG-FR02-A-14 | Thiếu Route Guard ngăn truy cập lại trang Login khi đã đăng nhập | TC-LOGIN-012 | Medium | Medium | [Issue #44](https://github.com/trngnneee/eshop-sut/issues/44) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/../evidence/BUG-FR02-A-14_screenshot.png) |
| BUG-FR02-A-15 | Giao diện đăng nhập Admin thiếu nhãn thông tin, thiếu dấu * bắt buộc và nút hiện mật khẩu | TC-LOGIN-013 | Major | High | [Issue #45](https://github.com/trngnneee/eshop-sut/issues/45) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/../evidence/BUG-FR02-A-15_screenshot.png) |
| BUG-FR02-A-16 | Thông báo lỗi đăng nhập Admin sử dụng alert() gây hiển thị chữ "Code" và vi phạm vị trí thông báo | TC-LOGIN-004, TC-LOGIN-020, TC-LOGIN-021 | Major | Medium | [Issue #46](https://github.com/trngnneee/eshop-sut/issues/46) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/../evidence/BUG-FR02-A-16_screenshot.png) |
| BUG-FR02-A-17 | Đặt lại mật khẩu thành công không giải phóng trạng thái khóa tài khoản và không reset bộ đếm lần đăng nhập sai | TC-LOGIN-004 | Major | High | [Issue #47](https://github.com/trngnneee/eshop-sut/issues/47) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/../evidence/BUG-FR02-A-17_screenshot.png) |
| BUG-FR02-A-18 | Giao diện đăng nhập Frontend che khuất lỗi khóa tài khoản (luôn hiện thông báo lỗi tĩnh) | TC-LOGIN-... | Major | High | [Issue #48](https://github.com/trngnneee/eshop-sut/issues/48) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/../evidence/BUG-FR02-A-18_screenshot.png) |
| BUG-FR02-A-19 | API và giao diện thiếu cảnh báo số lần đăng nhập sai còn lại trước khi khóa | TC-LOGIN-030 | Major | Medium | [Issue #49](https://github.com/trngnneee/eshop-sut/issues/49) | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/../evidence/BUG-FR02-A-19_screenshot.png) |

## 6. AI Gap Analysis Summary
- What AI missed: Sai sót trong cấu hình lockout thời gian 180s ở DB, lỗi tab index bàn phím, race condition do query DB bất đồng bộ.
- What human corrected: Sinh viên phát hiện thêm lỗi race condition khi test thủ công nhiều tab và check tab focus UI.
- Why the gap happened: AI không có trải nghiệm giao diện trực quan và khả năng bắt đúng thời gian trễ ghi CSDL thực tế.
- Lesson learned: Cần kết hợp phân tích code backend để phát hiện bất đồng bộ race condition.

## 7. Evidence
- Screenshot folder: [tests/bug/login/evidences/](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/evidences/)
- Video/demo link nếu có: N/A
- GitHub Issue links: #31 đến #49

---

# FR-07 – Shopping Cart

## 1. Feature Overview
- Pool: Pool B (Shopping Cart)
- Actor: Customer
- Related UI: `/cart`, Product Details, Homepage Grid
- Related API: `GET /api/cart`, `POST /api/cart`, `DELETE /api/cart`
- Preconditions: User must be logged in.
- Business Rules: Add product increases quantity, confirmation dialog on delete, show total label as 'Tổng cộng', empty cart illustration.

## 2. Domain Testing Summary
- Link/detail: [tests/test-cases/cart/](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-cases/cart/)
- Number of Domain Test Cases: 75
- Main valid partitions: Thêm sản phẩm, Xem giỏ hàng, Xóa sản phẩm xác nhận, Tính tổng tiền, Đồng bộ badge Navbar
- Main invalid partitions: Thêm không đăng nhập, Thêm thiếu id/price, price <= 0, Xóa không xác nhận
- Human review notes: SUT thiếu hoàn toàn nút tăng giảm số lượng (+/-) trực tiếp trên trang `/cart` nên không thể thay đổi số lượng sau khi thêm.

## 3. Boundary Value Analysis Summary
- Link/detail: [tests/test-cases/cart/](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-cases/cart/)
- Boundary variables: Số lượng quantity, giá sản phẩm price, dung lượng request body
- Number of BVA Test Cases: 15
- Important boundary values: Quantity (-1, 0, 1, 999999999), Price (0, 1, 1000, max_int)
- Human review notes: SUT cho phép thêm sản phẩm với quantity âm, bằng 0, thập phân và giá tiền giả mạo từ client.

## 4. Test Execution Summary
| Total TC | Executed | Passed | Failed | Blocked | Not Executed |
|---|---:|---:|---:|---:|---:|
| 90 | 90 | 35 | 55 | 0 | 0 |

## 5. Bugs Found
| Bug ID | Title | Related Test Case | Severity | Priority | GitHub Issue | Evidence |
|---|---|---|---|---|---|---|
| BUG-FR07-B-01 | Backend API không validate số lượng sản phẩm thêm vào giỏ hàng | TC-CART-044, TC-CART-045, TC-CART-046, TC-CART-047 | Major | High | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-01.png) |
| BUG-FR07-B-02 | Backend API không cộng dồn số lượng cho sản phẩm trùng ID | TC-CART-043 | Major | High | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-02.png) |
| BUG-FR07-B-03 | Frontend CartContext không cộng dồn số lượng khi thêm sản phẩm trùng | TC-CART-012 | Major | High | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-03.png) |
| BUG-FR07-B-04 | Trang giỏ hàng thiếu nút tăng giảm số lượng (+/-) và nhập số lượng trực tiếp | TC-CART-015, TC-CART-016, TC-CART-017, TC-CART-018, TC-CART-019, TC-CART-020, TC-CART-021, TC-CART-022, TC-CART-023, TC-CART-024, TC-CART-025 | Major | High | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-04.png) |
| BUG-FR07-B-05 | Thiếu Confirm Dialog xác nhận khi xóa sản phẩm khỏi giỏ hàng | TC-CART-031, TC-CART-032, TC-CART-033, TC-CART-075 | Minor | Medium | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-05.png) |
| BUG-FR07-B-06 | Nhãn hiển thị tổng tiền không đúng đặc tả ('Tổng tạm tính' thay vì 'Tổng cộng') | TC-CART-009 | Minor | Low | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-06.png) |
| BUG-FR07-B-07 | Trạng thái giỏ hàng trống thiếu hình ảnh/icon minh họa trực quan | TC-CART-002 | Minor | Low | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-07.png) |
| BUG-FR07-B-08 | Trang giỏ hàng thiếu thanh breadcrumb điều hướng | TC-CART-004 | Minor | Low | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-08.png) |
| BUG-FR07-B-09 | Không cần đăng nhập vẫn cho phép thêm sản phẩm vào giỏ hàng | TC-CART-... | Major | High | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-09.png) |
| BUG-FR07-B-10 | Backend API không validate tính toàn vẹn của sản phẩm thêm vào giỏ hàng | TC-CART-051, TC-CART-053, TC-CART-057, TC-CART-058, TC-CART-059 | Major | High | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-10.png) |
| BUG-FR07-B-11 | Thiếu thông báo phản hồi (toast/alert) khi thêm sản phẩm vào giỏ hàng thành công | TC-CART-010, TC-CART-011, TC-CART-038, TC-CART-074 | Minor | Medium | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-11.png) |
| BUG-FR07-B-12 | Không hiển thị số lượng hàng tồn kho khả dụng và thiếu cảnh báo khi số lượng vượt quá hàng tồn | TC-CART-060, TC-CART-079 | Major | High | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-12.png) |
| BUG-FR07-B-13 | Backend API cho phép giả mạo đơn giá của sản phẩm (Price Tampering) | TC-CART-063, TC-CART-064, TC-CART-080 | Critical | High | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-13.png) |
| BUG-FR07-B-14 | Backend API chấp nhận productId không tồn tại và tạo ra sản phẩm ma | TC-CART-061, TC-CART-062, TC-CART-078 | Major | High | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-14.png) |
| BUG-FR07-B-15 | Backend API không kiểm tra kiểu dữ liệu của trường quantity (Type Validation) | TC-CART-065, TC-CART-066, TC-CART-067, TC-CART-068 | Major | High | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-15.png) |
| BUG-FR07-B-16 | Lỗ hổng cho phép gán thuộc tính đặc quyền (Mass Assignment / Extra Fields) | TC-CART-070 | Major | High | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-16.png) |
| BUG-FR07-B-17 | Giao diện cho phép thanh toán (Checkout) khi giỏ hàng trống | TC-CART-076, TC-CART-077 | Major | Medium | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-17.png) |
| BUG-FR07-B-18 | Thiếu xử lý lỗi kết nối mạng hoặc sập máy chủ trên giao diện | TC-CART-... | Major | Medium | N/A | [Evidence](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/BUG-FR07-B-18.png) |

## 6. AI Gap Analysis Summary
- What AI missed: Lỗi không validate tính toàn vẹn của body JSON (thiếu id, price), cho phép giả mạo giá tiền của admin để mua rẻ.
- What human corrected: Sinh viên phân tích API payload và thực hiện giả mạo HTTP Request để phát hiện backend thiếu kiểm tra tính hợp lệ của giá bán gốc.
- Why the gap happened: AI sinh testcase tĩnh dựa trên mô tả cơ bản của giao diện mà bỏ qua các kịch bản kiểm tra bảo mật dữ liệu ở API backend.
- Lesson learned: Phải kiểm tra tính toàn vẹn và đồng bộ dữ liệu giữa Frontend và Backend DB.

## 7. Evidence
- Screenshot folder: [tests/bug/cart/evidences/](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/cart/evidences/)
- Video/demo link nếu có: N/A
- GitHub Issue links: N/A (local execution)
