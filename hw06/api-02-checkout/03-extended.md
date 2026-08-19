# API-2 — Test case do người học mở rộng cho `POST /api/checkout`

| TC ID | Test case tự bổ sung | Preconditions / Test data | Expected result theo đặc tả | Bug nhắm tới | Vì sao AI bỏ sót |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TC-API-CHECKOUT-037 | Dùng tổng giả trong body | Có giỏ chứa sản phẩm 30 triệu; gửi total_amount=1 | Đơn phải có tổng tính từ giỏ, không phải 1 | D-CHK-01 | AI test request độc lập và không đặt bất biến giữa POST /api/cart và POST /api/checkout; nguyên nhân là giới hạn phạm vi prompt. |
| TC-API-CHECKOUT-038 | Biên total_amount âm | Có JWT và giỏ có sản phẩm; gửi total_amount=-500000 | 400; không tạo đơn | D-CHK-02 | Prompt bám schema API nhưng không nối invariant nghiệp vụ FR-08 rằng tiền phải dương; cần suy luận từ requirement. |
| TC-API-CHECKOUT-039 | Hậu điều kiện xóa giỏ | Checkout thành công rồi GET /api/cart | Response là []; không còn item cũ | D-CHK-03 | AI thường chỉ assert response của endpoint đang được hỏi, bỏ qua post-condition ở endpoint khác. |
| TC-API-CHECKOUT-040 | Giỏ rỗng không thể thanh toán | Không thêm item; gọi checkout | 400; không tạo order | D-CHK-04 | Spec API không mô tả rõ empty-cart oracle nên AI không tự suy luận trạng thái nghiệp vụ này. |
| TC-API-CHECKOUT-041 | IDOR khi đọc order | User A tạo order; request không token hoặc user B GET /api/orders/:id | 401/403; không lộ order A | D-CHK-07 | Đây là endpoint liền kề ngoài endpoint checkout; AI bị giới hạn ngữ cảnh theo một endpoint. |
| TC-API-CHECKOUT-042 | XSS trong shipping_address | Địa chỉ là <img src=x onerror=alert(1)>; đọc lại order | Payload bị reject hoặc escape, không lưu raw | D-CHK-05 | AI dễ đẩy XSS về frontend và không dựng assertion persistence/read-back ở API. |

**Số case mở rộng:** 6. Mỗi lý do được phân loại theo chất lượng prompt, giới hạn model hoặc đặc thù API.
