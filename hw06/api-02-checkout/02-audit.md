# API-2 — Human-review worksheet for AI-generated checkout cases

> Oracle: FR-08/FR-10, `api_specification.md`, `backend/server.js` và `docs/hw06/02-sut-defect-catalog.md` §2.

## Bảng audit 100% test case AI sinh

| TC ID | Nhãn | Lý do review | Hành động sửa |
| :--- | :--- | :--- | :--- |
| TC-API-CHECKOUT-001 | INVALID | AI lấy total_amount từ client làm oracle, trái FR-08 yêu cầu tính lại từ giỏ. | Sửa expected theo tổng thực của giỏ, không theo body. |
| TC-API-CHECKOUT-002 | VALID | FR-08 yêu cầu chỉ user đã đăng nhập mới checkout. | Giữ nguyên. |
| TC-API-CHECKOUT-003 | VALID | Token có header nhưng không theo dạng Bearer được middleware coi là token không hợp lệ. | Giữ nguyên. |
| TC-API-CHECKOUT-004 | VALID | Theo middleware của SUT, token sai chữ ký trả 403; đây là nhánh invalid-token riêng với thiếu header. | Giữ nguyên. |
| TC-API-CHECKOUT-005 | VALID | FR-08 không chấp nhận total do client; dữ liệu 0 phải bị từ chối theo invariant tổng đơn dương. | Giữ nguyên. |
| TC-API-CHECKOUT-006 | VALID | Giá trị âm là phân vùng invalid rõ ràng của total tiền. | Giữ nguyên. |
| TC-API-CHECKOUT-007 | VALID | Schema request mô tả số; chuỗi không được coi là số tiền. | Giữ nguyên. |
| TC-API-CHECKOUT-008 | VALID | Null không phải số tiền hợp lệ. | Giữ nguyên. |
| TC-API-CHECKOUT-009 | INCOMPLETE | API spec không tuyên bố status khi thiếu shipping_address; ý tưởng đúng nhưng oracle chưa chốt. | Ghi controlled 4xx/không 5xx; không khẳng định 400 nếu chưa chốt contract. |
| TC-API-CHECKOUT-010 | INCOMPLETE | FR-08 không nêu độ dài tối thiểu địa chỉ và API spec không định status. | Sửa expected thành robustness: không 5xx, không phản chiếu nguy hiểm. |
| TC-API-CHECKOUT-011 | INCOMPLETE | Không có giới hạn 1000 trong đặc tả; AI tự bịa boundary. | Bỏ con số 1000; kiểm tra server không 5xx và lưu/đọc an toàn theo contract. |
| TC-API-CHECKOUT-012 | VALID | SEC-04/FR-18 yêu cầu dữ liệu địa chỉ không gây XSS khi hiển thị. | Giữ nguyên security expectation. |
| TC-API-CHECKOUT-013 | VALID | Địa chỉ là dữ liệu; query phải parameterized và lỗi không được lộ. | Giữ nguyên. |
| TC-API-CHECKOUT-014 | VALID | Unicode là input hợp lệ và cần bảo toàn khi lưu/đọc. | Giữ nguyên. |
| TC-API-CHECKOUT-015 | VALID | Tiền đơn hàng được đặc tả là giá trị tiền nguyên; số thực là type/boundary partition. | Giữ nguyên. |
| TC-API-CHECKOUT-016 | VALID | Giá trị vượt miền an toàn phải bị từ chối, không làm sai số hoặc crash. | Giữ nguyên. |
| TC-API-CHECKOUT-017 | INCOMPLETE | Spec không nói strict/loose schema đối với field thừa; cần nêu assumption. | Cho phép field vô hại nhưng kiểm tra không đổi user_id/role; không assert exact body. |
| TC-API-CHECKOUT-018 | VALID | JSON number hợp lệ; server không nên lỗi chỉ vì notation. | Giữ nguyên nhưng không dùng làm oracle tính tổng. |
| TC-API-CHECKOUT-019 | VALID | FR-10 quy định đơn mới luôn pending. | Giữ nguyên. |
| TC-API-CHECKOUT-020 | VALID | Đây là post-condition bắt buộc của FR-08. | Giữ nguyên. |
| TC-API-CHECKOUT-021 | INCOMPLETE | Idempotency không được nêu rõ trong FR-08/API spec. | Ghi nhận quan sát nhưng không dùng làm strict assertion nếu contract chưa bổ sung. |
| TC-API-CHECKOUT-022 | VALID | Thanh toán không có hàng là trạng thái invalid theo nghiệp vụ. | Giữ nguyên. |
| TC-API-CHECKOUT-023 | VALID | Đây là luồng end-to-end mà execution plan yêu cầu. | Giữ nguyên. |
| TC-API-CHECKOUT-024 | VALID | Response schema tối thiểu cần định danh đơn để chain request. | Giữ nguyên. |
| TC-API-CHECKOUT-025 | INVALID | AI expected hành vi không an toàn; FR-08 yêu cầu identity lấy từ token. | Sửa expected: user_id phải bằng req.user.id, bỏ qua body. |
| TC-API-CHECKOUT-026 | VALID | Kiểm tra state auth được nối giữa các request. | Giữ nguyên. |
| TC-API-CHECKOUT-027 | VALID | SEC-02: endpoint bảo vệ phải yêu cầu JWT. | Giữ nguyên. |
| TC-API-CHECKOUT-028 | VALID | JWT sai chữ ký thuộc nhánh invalid token; middleware trả 403 và không cho tạo đơn. | Giữ nguyên. |
| TC-API-CHECKOUT-029 | VALID | JWT hết hạn bị jsonwebtoken verify từ chối với 403 trong middleware. | Giữ nguyên. |
| TC-API-CHECKOUT-030 | VALID | Identity phải lấy từ token và không được truy cập cart của user khác. | Giữ nguyên security expectation. |
| TC-API-CHECKOUT-031 | VALID | SEC-02 áp dụng cho order data; endpoint kề bên là IDOR cần kiểm tra. | Giữ nguyên. |
| TC-API-CHECKOUT-032 | VALID | Response và endpoint đọc lại không được trả dữ liệu nguy hiểm chưa escape. | Giữ nguyên. |
| TC-API-CHECKOUT-033 | INVALID | Plan/API chain cần orderId số nguyên; AI tự chọn string trái schema dữ liệu. | Sửa orderId thành integer dương. |
| TC-API-CHECKOUT-034 | VALID | Endpoint JSON phải trả JSON content type. | Giữ nguyên. |
| TC-API-CHECKOUT-035 | VALID | ID SQLite là integer và được dùng để chain GET order. | Giữ nguyên. |
| TC-API-CHECKOUT-036 | VALID | Không response nào được lộ credential hoặc secret nội bộ. | Giữ nguyên; không cấm metadata vô hại ngoài field nhạy cảm. |

## Phiên bản expected sau audit cho case cần sửa

| TC ID | Expected đã chốt |
| :--- | :--- |
| TC-API-CHECKOUT-001 | 200; orderId là số nguyên; đơn có total theo giỏ; status=pending |
| TC-API-CHECKOUT-009 | Controlled client error nếu contract yêu cầu; không 5xx |
| TC-API-CHECKOUT-010 | Controlled client error hoặc contract được chốt; không 5xx |
| TC-API-CHECKOUT-011 | Không 5xx; status cụ thể cần contract |
| TC-API-CHECKOUT-017 | Nếu tạo đơn, user_id lấy từ JWT; field thừa không nâng quyền |
| TC-API-CHECKOUT-021 | Không đặt strict oracle; ghi số đơn thực tế để audit |
| TC-API-CHECKOUT-025 | Đơn thuộc user trong JWT, không thể giả mạo chủ đơn |
| TC-API-CHECKOUT-033 | 200; message:string; orderId:integer |

## Thống kê audit

| Nhãn | Số case | Tỷ lệ |
| :--- | ---: | ---: |
| VALID | 28 | 77.78% |
| INVALID | 3 | 8.33% |
| INCOMPLETE | 5 | 13.89% |
| **Tổng đã audit** | **36/36** | **100%** |

## HUMAN checkpoint — bắt buộc trước khi sang API-3

- [x] Tôi đã đối chiếu đủ 36 dòng với FR-08/FR-10, API spec và mã nguồn.
- [x] Tôi đồng ý hoặc đã chỉnh lại nhãn/lý do cho các case INVALID/INCOMPLETE.
- [x] Tôi hiểu vì sao expected phải theo đặc tả, không sửa để khớp bug của SUT.

**Reviewed by:** Đặng Đăng Khoa
**Student ID:** `23127207`  
**Reviewed at:** 10:40 19-08-2026 
**Signature / confirmation:** Đã duyệt
