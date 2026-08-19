# API-3 — Test case do người học mở rộng cho `PUT /api/admin/orders/:id/status`

| TC ID | Test case tự bổ sung | Preconditions / Test data | Expected result theo đặc tả | Bug nhắm tới | Vì sao AI bỏ sót |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TC-API-ORDER-STATUS-039 | Role escalation bằng user token | User thường có JWT; order tồn tại; PUT status=confirmed | 403; không cập nhật order | D-ADM-01 | AI mặc định endpoint `/admin/` đã kiểm tra role; đây là assumption bias về chức năng. |
| TC-API-ORDER-STATUS-040 | Cross-user order mutation | User A dùng token sửa order của user B | 403; user không có quyền admin | D-ADM-01 | Case cần hai danh tính và dữ liệu liên kết; prompt generate không yêu cầu kịch bản multi-identity. |
| TC-API-ORDER-STATUS-041 | Canceled không hồi sinh và dashboard không tăng doanh thu | Admin thử canceled→delivered rồi kiểm tra dữ liệu delivered/dashboard | 400; không tăng delivered revenue | D-ADM-02 | AI thường chỉ assert response endpoint, bỏ qua tác động dây chuyền sang FR-13. |
| TC-API-ORDER-STATUS-042 | Admin hủy đơn shipping | Admin JWT; order shipping; status=canceled | 200; order chuyển canceled | D-ADM-03 | Đặc tả diễn đạt quyền Admin gián tiếp; AI bám whitelist hiện tại thay vì suy luận từ state rule. |
| TC-API-ORDER-STATUS-043 | User không hủy order shipping qua endpoint user | User JWT; order shipping; PUT /api/orders/:id/cancel | 400; user không được hủy shipping | D-ADM-08 | Endpoint cancel nằm ngoài prompt về admin status, nên AI không nối hai endpoint cùng state machine. |
| TC-API-ORDER-STATUS-044 | Status sai kiểu dữ liệu | Admin JWT; status=['delivered'] hoặc {value:'delivered'} | 400; phân biệt type invalid với transition invalid | D-ADM-06 | AI thường chỉ sinh enum sai dạng chuỗi, bỏ qua type confusion của JSON body. |

**Số case mở rộng:** 6; tất cả đều nhắm security hoặc state-transition liên API.
