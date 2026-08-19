# API-2 — Danh sách test case chốt cho `POST /api/checkout`

> 36 case AI sau audit + 6 case human extension. `Kỳ vọng chạy` phản ánh SUT hiện tại, còn `Expected` luôn theo đặc tả.

| TC ID | Requirement | Nhóm | Kỹ thuật | Preconditions | Method + Endpoint / Test data | Expected | Nguồn | Kỳ vọng chạy | Bug ID |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| TC-API-CHECKOUT-001 | FR-08/FR-10 | Partition | EP | User có JWT; giỏ có một sản phẩm | `POST /api/checkout`; total_amount=200000; shipping_address='123 Le Loi' | 200; orderId là số nguyên; đơn có total theo giỏ; status=pending | AI/audit | FAIL | D-CHK-01 |
| TC-API-CHECKOUT-002 | FR-08/FR-10 | Partition | EP | Giỏ không quan trọng | `POST /api/checkout`; Không gửi Authorization | 401; không tạo đơn | AI/audit | PASS | — |
| TC-API-CHECKOUT-003 | FR-08/FR-10 | Partition | EP | Không gửi request trước | `POST /api/checkout`; Authorization='abc' | 403; không tạo đơn | AI/audit | PASS | — |
| TC-API-CHECKOUT-004 | FR-08/FR-10 | Partition | EP | Có token giả | `POST /api/checkout`; Authorization='Bearer invalid.signature.token' | 403; không tạo đơn | AI/audit | PASS | — |
| TC-API-CHECKOUT-005 | FR-08/FR-10 | Partition | BVA | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; total_amount=0; shipping_address='A' | 400; không tạo đơn | AI/audit | FAIL | D-CHK-02 |
| TC-API-CHECKOUT-006 | FR-08/FR-10 | Partition | BVA | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; total_amount=-500000; shipping_address='A' | 400; không tạo đơn | AI/audit | FAIL | D-CHK-02 |
| TC-API-CHECKOUT-007 | FR-08/FR-10 | Partition | EP/type | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; total_amount='200000' | 400; không tạo đơn | AI/audit | PASS | — |
| TC-API-CHECKOUT-008 | FR-08/FR-10 | Partition | EP/type | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; total_amount=null | 400; không tạo đơn | AI/audit | PASS | — |
| TC-API-CHECKOUT-009 | FR-08/FR-10 | Partition | EP | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; Chỉ gửi total_amount=200000 | Controlled client error nếu contract yêu cầu; không 5xx | AI/audit | PASS | — |
| TC-API-CHECKOUT-010 | FR-08/FR-10 | Partition | EP/BVA | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; shipping_address='' | Controlled client error hoặc contract được chốt; không 5xx | AI/audit | PASS | — |
| TC-API-CHECKOUT-011 | FR-08/FR-10 | Partition | BVA | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; Chuỗi 1001 ký tự | Không 5xx; status cụ thể cần contract | AI/audit | PASS | — |
| TC-API-CHECKOUT-012 | FR-08/FR-10 | Partition | Security | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; <img src=x onerror=alert(1)> | Request bị từ chối hoặc dữ liệu được escape khi đọc lại | AI/audit | FAIL | D-CHK-05 |
| TC-API-CHECKOUT-013 | FR-08/FR-10 | Partition | Security | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; ' OR 1=1 -- | Không bypass; không 5xx; không phản chiếu payload | AI/audit | PASS | — |
| TC-API-CHECKOUT-014 | FR-08/FR-10 | Partition | EP | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; 12 Lê Lợi, Quận 1, TP.HCM | Controlled result; nếu tạo đơn thì status=pending và địa chỉ không hỏng mã hóa | AI/audit | PASS | — |
| TC-API-CHECKOUT-015 | FR-08/FR-10 | Partition | BVA/type | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; total_amount=200000.5 | 400; không tạo đơn | AI/audit | PASS | — |
| TC-API-CHECKOUT-016 | FR-08/FR-10 | Partition | BVA | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; total_amount=9000000000000000000 | 400 hoặc controlled client error; không 5xx | AI/audit | PASS | — |
| TC-API-CHECKOUT-017 | FR-08/FR-10 | Partition | Schema | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; extra role='admin' cùng body hợp lệ | Nếu tạo đơn, user_id lấy từ JWT; field thừa không nâng quyền | AI/audit | PASS | — |
| TC-API-CHECKOUT-018 | FR-08/FR-10 | Partition | EP | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; total_amount=2e5 | Không 5xx; nếu tạo đơn thì tổng phải theo giỏ | AI/audit | PASS | — |
| TC-API-CHECKOUT-019 | FR-08/FR-10 | State | State-transition | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; Body hợp lệ; gọi POST /api/checkout | 200; orderId số nguyên; status=pending khi đọc lại đơn | AI/audit | PASS | — |
| TC-API-CHECKOUT-020 | FR-08/FR-10 | State | State/post-condition | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; Checkout rồi GET /api/cart | Giỏ rỗng sau checkout thành công | AI/audit | FAIL | D-CHK-03 |
| TC-API-CHECKOUT-021 | FR-08/FR-10 | State | State | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; Gửi cùng body hai lần | Không đặt strict oracle; ghi số đơn thực tế để audit | AI/audit | PASS | — |
| TC-API-CHECKOUT-022 | FR-08/FR-10 | State | State-transition | User có JWT; không thêm sản phẩm | `POST /api/checkout`; Body total_amount=1 | 400; không tạo đơn | AI/audit | FAIL | D-CHK-04 |
| TC-API-CHECKOUT-023 | FR-08/FR-10 | State | State/flow | User có JWT | `POST /api/checkout`; POST cart rồi POST checkout rồi GET my-orders | Order của đúng user xuất hiện với status=pending | AI/audit | PASS | — |
| TC-API-CHECKOUT-024 | FR-08/FR-10 | State | Schema/state | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; Checkout thành công | orderId là integer dương | AI/audit | PASS | — |
| TC-API-CHECKOUT-025 | FR-08/FR-10 | State | Security/state | User A có JWT; body cố gửi user_id của B | `POST /api/checkout`; user_id=999 trong body | Đơn thuộc user trong JWT, không thể giả mạo chủ đơn | AI/audit | PASS | — |
| TC-API-CHECKOUT-026 | FR-08/FR-10 | State | State-transition | User đăng nhập; giỏ có sản phẩm | `POST /api/checkout`; Login → add cart → checkout | 200; pending; order thuộc user vừa login | AI/audit | PASS | — |
| TC-API-CHECKOUT-027 | FR-08/FR-10 | Security | Security | Giỏ có thể có hoặc không | `POST /api/checkout`; POST checkout không Authorization | 401; không tạo đơn | AI/audit | PASS | — |
| TC-API-CHECKOUT-028 | FR-08/FR-10 | Security | Security | Có token giả | `POST /api/checkout`; Bearer token bị sửa payload | 403; không tạo đơn | AI/audit | PASS | — |
| TC-API-CHECKOUT-029 | FR-08/FR-10 | Security | Security | Có JWT exp trong quá khứ | `POST /api/checkout`; Bearer expired JWT | 403; không tạo đơn | AI/audit | PASS | — |
| TC-API-CHECKOUT-030 | FR-08/FR-10 | Security | Security/IDOR | User A có cart; User B có JWT | `POST /api/checkout`; B checkout với body cố trỏ tới cart/order của A | Đơn chỉ thuộc user B; không đọc/ghi cart của A | AI/audit | PASS | — |
| TC-API-CHECKOUT-031 | FR-08/FR-10 | Security | Security/IDOR | Có orderId của user khác | `POST /api/checkout`; GET /api/orders/{id} không Authorization | 401/403; không lộ order | AI/audit | FAIL | D-CHK-07 |
| TC-API-CHECKOUT-032 | FR-08/FR-10 | Security | Security | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; shipping_address='<script>alert(1)</script>' | Payload bị từ chối hoặc được escape khi đọc lại | AI/audit | FAIL | D-CHK-05 |
| TC-API-CHECKOUT-033 | FR-08/FR-10 | Schema | Schema | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; Body hợp lệ | 200; message:string; orderId:integer | AI/audit | PASS | — |
| TC-API-CHECKOUT-034 | FR-08/FR-10 | Schema | Schema | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; Checkout hợp lệ | Content-Type application/json | AI/audit | PASS | — |
| TC-API-CHECKOUT-035 | FR-08/FR-10 | Schema | Schema | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; Checkout thành công | orderId là integer dương | AI/audit | PASS | — |
| TC-API-CHECKOUT-036 | FR-08/FR-10 | Schema | Schema/security | User có JWT; giỏ có sản phẩm | `POST /api/checkout`; Checkout thành công rồi đọc order | Không có password/reset_token/login_attempts/locked_until | AI/audit | PASS | — |
| TC-API-CHECKOUT-037 | FR-08/FR-10/SEC-02/SEC-04 | Extension | Flow/security | Có giỏ chứa sản phẩm 30 triệu; gửi total_amount=1 | `POST /api/checkout` + chained endpoint; Dùng tổng giả trong body | Đơn phải có tổng tính từ giỏ, không phải 1 | Human | FAIL | D-CHK-01 |
| TC-API-CHECKOUT-038 | FR-08/FR-10/SEC-02/SEC-04 | Extension | Flow/security | Có JWT và giỏ có sản phẩm; gửi total_amount=-500000 | `POST /api/checkout` + chained endpoint; Biên total_amount âm | 400; không tạo đơn | Human | FAIL | D-CHK-02 |
| TC-API-CHECKOUT-039 | FR-08/FR-10/SEC-02/SEC-04 | Extension | Flow/security | Checkout thành công rồi GET /api/cart | `POST /api/checkout` + chained endpoint; Hậu điều kiện xóa giỏ | Response là []; không còn item cũ | Human | FAIL | D-CHK-03 |
| TC-API-CHECKOUT-040 | FR-08/FR-10/SEC-02/SEC-04 | Extension | Flow/security | Không thêm item; gọi checkout | `POST /api/checkout` + chained endpoint; Giỏ rỗng không thể thanh toán | 400; không tạo order | Human | FAIL | D-CHK-04 |
| TC-API-CHECKOUT-041 | FR-08/FR-10/SEC-02/SEC-04 | Extension | Flow/security | User A tạo order; request không token hoặc user B GET /api/orders/:id | `POST /api/checkout` + chained endpoint; IDOR khi đọc order | 401/403; không lộ order A | Human | FAIL | D-CHK-07 |
| TC-API-CHECKOUT-042 | FR-08/FR-10/SEC-02/SEC-04 | Extension | Flow/security | Địa chỉ là <img src=x onerror=alert(1)>; đọc lại order | `POST /api/checkout` + chained endpoint; XSS trong shipping_address | Payload bị reject hoặc escape, không lưu raw | Human | FAIL | D-CHK-05 |

## Summary

| Nguồn | Số lượng |
| :--- | ---: |
| AI-generated sau audit | 36 |
| Human extension | 6 |
| **Tổng** | **42** |
| Expected fail do defect catalog | 12 strict/extension observations |
