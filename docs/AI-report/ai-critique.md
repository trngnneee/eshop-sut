# **AI Critique**

Trong quá trình sử dụng AI để hỗ trợ sinh test case cho các module Product, Order History, User Management và Mobile Order, em nhận thấy AI có khả năng tạo test case nhanh và đúng theo các kỹ thuật như Domain Testing và Boundary Value Analysis. Tuy nhiên, các phân tích AI Gap cho thấy AI vẫn bỏ sót nhiều trường hợp quan trọng do hạn chế trong việc hiểu sâu ngữ cảnh hệ thống và các khía cạnh nâng cao như security, authorization và data relationship.

Cụ thể, ở module Product, AI bỏ sót các test case liên quan đến XSS nâng cao và khai thác backend (TC-PRODUCT-013, TC-PRODUCT-014) vì chỉ tập trung vào input cơ bản và kiểm thử frontend, chưa mở rộng sang các payload thực tế hoặc hành vi truy vấn database. Ở module Order History, các test case TC-ORDERHISTORY-011 đến TC-ORDERHISTORY-014 bị thiếu do AI không tự xem xét pagination, authentication bypass và phân quyền giữa nhiều user, một phần vì requirement không mô tả rõ API và agent skill chưa yêu cầu phân tích backend.

Trong module User Management, AI tiếp tục bỏ sót các trường hợp liên quan đến dữ liệu liên kết và rò rỉ thông tin sau khi xóa user (TC-USERMGMT-021, TC-USERMGMT-022). Ngoài ra, AI cũng tạo ra một số test case trùng lặp trong Mobile Order do chưa tối ưu hóa logic UI-state.

Từ đó, em nhận thấy AI mạnh ở việc sinh ý tưởng theo pattern nhưng yếu trong suy luận theo ngữ cảnh hệ thống. Vì vậy, người kiểm thử cần định hướng rõ scope, bổ sung góc nhìn về security và data flow, đồng thời luôn review lại kết quả để tránh thiếu sót các edge case quan trọng.
