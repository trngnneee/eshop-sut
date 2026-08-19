# AI Critique — bản nháp để người học viết lại

> HUMAN-ONLY: đây là bản nháp dữ liệu, không phải bài critique đã ký của sinh viên. Vui lòng viết lại bằng nhận xét của chính bạn trước khi nộp.

AI tạo được độ phủ khá rộng ở ba API, đặc biệt là các phân vùng dữ liệu, ma trận trạng thái và nhóm kiểm thử bảo mật. Tuy nhiên, output ban đầu vẫn có những expected result không bám đặc tả, chẳng hạn coi việc bypass SQL injection là kết quả hợp lệ hoặc bỏ qua điều kiện hậu nghiệm của checkout. Audit đã phải sửa các case đó thành INVALID hoặc INCOMPLETE. Đây là dấu hiệu AI có xu hướng dự đoán theo mẫu API phổ biến thay vì đọc chính xác oracle của SUT.

AI cũng bỏ sót các lỗi nằm ngoài endpoint chính. Ví dụ, IDOR ở GET `/api/orders/:id`, việc giỏ hàng không bị xóa, và các nhánh trạng thái kết thúc chỉ xuất hiện sau khi mở rộng ngữ cảnh bằng flow nghiệp vụ. Ma trận 5×5 của API-3 cho thấy câu trả lời một request không đủ để kiểm thử hệ thống có state; mỗi ô cần precondition độc lập và phải ghi rõ `from_status`.

Bài học quan trọng là không xem số lượng test case do AI sinh như bằng chứng chất lượng. Cần chia prompt thành các bước có thể audit, đối chiếu từng expected result với đặc tả và mã SUT, rồi chạy các case quan trọng trên Newman. Human review vẫn cần thiết cho quyết định VALID/INVALID, cho nhận định mức độ nghiêm trọng và cho các bằng chứng external như GitHub Issue, screenshot, diagram. AI hữu ích nhất khi tạo scaffold có cấu trúc; trách nhiệm oracle và kết luận cuối cùng vẫn thuộc về người kiểm thử.
