# AI Gap Analysis Report: FR-21 – Mobile Cart & Checkout

## 1. Overview of Test Coverage Gaps
 
This report compares the initial test scenarios that an AI would generate based solely on reading the feature specifications (Feature Input) versus the actual technical gaps, vulnerabilities, and implementation bugs discovered during the functional verification and human review of the mobile application and backend services.
 
---
 
## 2. Gap Analysis Matrix
 
| Gap Area / Bug | Found by AI from Spec? | Found by Human in System Testing? | Description & Root Cause | Impact & Lesson Learned |
| :--- | :---: | :---: | :--- | :--- |
| **Quantity Input Auto-increment (+1 Bug)** | ❌ No | ✅ Yes | Khi người dùng nhập trực tiếp số lượng vào ô nhập liệu trong giỏ hàng, số lượng hiển thị thực tế bị tự động cộng thêm 1 đơn vị. | **Major.** Trải nghiệm người dùng và tính toán tiền tệ bị sai lệch. Cần kiểm thử hành vi tương tác thực tế trên giao diện để phát hiện. |
| **Address Omission on Checkout** | ❌ No | ✅ Yes | Hệ thống không gửi địa chỉ giao hàng khi thực hiện thanh toán, dẫn đến đơn hàng trên hệ thống có địa chỉ giao hàng bị để trống. | **Major.** Đơn hàng được tạo thành công nhưng thiếu thông tin giao hàng quan trọng. Cần kiểm thử tích hợp và kiểm tra dữ liệu đơn hàng sau khi tạo. |
| **Vietnamese Phone Regex Refusal (0-Prefix Blocked)** | ❌ No | ✅ Yes | Hệ thống không chấp nhận số điện thoại bắt đầu bằng chữ số 0 trong phần hồ sơ cá nhân. | **Medium.** Khách hàng không thể lưu số điện thoại chuẩn Việt Nam. Cần kiểm định tính hợp lệ của các số điện thoại thực tế địa phương. |
| **Missing Price Validation (Price Tampering)** | ❌ No (usually missed) | ✅ Yes | API thanh toán chấp nhận giá trị tổng số tiền do người dùng gửi lên mà không đối sánh với giá gốc của các sản phẩm. | **Critical.** Lỗ hổng bảo mật nghiêm trọng. Người dùng có thể can thiệp request để mua sản phẩm giá trị cao với giá tùy ý. AI cần tăng cường thiết kế các kịch bản kiểm thử bảo mật API. |
| **Boundary Coupon Minimum Amount Bug** | ❌ No | ✅ Yes | Hệ thống từ chối áp dụng mã giảm giá khi tổng giá trị đơn hàng bằng đúng giá trị tối thiểu (`total_amount = min_order_amount`). | **Major.** Ảnh hưởng đến quyền lợi người dùng khi mua hàng đạt đủ điều kiện biên. Cần kiểm thử giá trị biên chi tiết (BVA). |
| **Incorrect Percent Coupon Calculation** | ❌ No | ✅ Yes | API áp dụng mã giảm giá tính toán sai số tiền giảm phần trăm (lấy phần còn lại thay vì phần giảm), dẫn đến giảm 90% thay vì 10%. | **Critical.** Lỗi tính toán tài chính nghiêm trọng gây thiệt hại lớn cho cửa hàng. Cần kiểm thử logic nghiệp vụ tính toán chi tiết. |
 
---
 
## 3. Human Corrective Actions & Review Notes
 
1. **Validation Mappings:** The human tester designed test cases to verify the system behavior and edge cases:
   - [TC-MOBILE-CART-DT-002](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-002.md) and [TC-MOBILE-CART-BVA-022](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-022.md) verify checkout behavior when ordering multiple items.
   - [TC-MOBILE-CART-DT-007](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-007.md) verifies direct quantity input updates.
   - [TC-MOBILE-CART-DT-015](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-015.md) and [TC-MOBILE-CART-BVA-009](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-009.md) verify Vietnamese phone number validation behavior.
   - [TC-MOBILE-CART-DT-018](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-018.md) targets API-level price validation logic.
   - [TC-MOBILE-CART-DT-019](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-019.md) verifies address field preservation in order details.
   - [TC-MOBILE-CART-BVA-023](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-BVA-023.md) verifies coupon application when total matches min_order_amount.
   - [TC-MOBILE-CART-DT-020](../../tests/test-cases/mobile-cart/TC-MOBILE-CART-DT-020.md) verifies correct percentage discount calculations.
 
2. **Lessons Learned:**
   - Tài liệu đặc tả yêu cầu thường mô tả kịch bản lý tưởng và bỏ sót các lỗi phát sinh trong quá trình cài đặt thực tế hoặc thiết kế regex validation không phù hợp.
   - Kiểm thử khám phá thực tế (exploratory testing) trực tiếp trên giao diện và API là cực kỳ quan trọng để phát hiện lỗi logic cài đặt và bảo mật ngoài luồng lý thuyết.
