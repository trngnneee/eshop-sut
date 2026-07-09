# Đánh Giá Tự Phê Bình AI (AI Critique)

*Yêu cầu độ dài: 200 - 300 từ. Trình bày suy nghĩ sâu sắc của sinh viên về việc đánh giá năng lực của AI, các giới hạn gặp phải và bài học rút ra (Bloom G9.3).*

## Nội Dung Bản Tự Phê Bình (Critique Content)

Trong quá trình sử dụng AI để hỗ trợ kiểm thử các chức năng FR-02, FR-07, FR-13 và FR-21, tôi nhận thấy AI rất hữu ích trong việc tạo nhanh cấu trúc test case, chia phân vùng tương đương, đề xuất giá trị biên và chuẩn hóa báo cáo Markdown. Tuy nhiên, AI vẫn có nhiều điểm thiếu sót khi chỉ dựa vào đặc tả hoặc prompt ban đầu. Với FR-02, AI ban đầu chưa phát hiện đầy đủ các lỗi liên quan đến race condition, độ nhạy chữ hoa/thường của email và trạng thái khóa tài khoản sau khi reset mật khẩu. Với FR-07 và FR-21, AI thường giả định backend sẽ tự kiểm tra dữ liệu hợp lệ, nên bỏ sót các lỗi nghiêm trọng như giả mạo đơn giá, thiếu kiểm tra productId, sai logic số lượng và lỗi tính mã giảm giá. Với FR-13, nếu không kiểm thử trực tiếp, AI khó phát hiện lỗi doanh thu bị nhân đôi hoặc API admin thiếu kiểm tra role.

Nguyên nhân chính là AI không trực tiếp trải nghiệm UI, không quan sát database/runtime và không tự xác minh phản hồi API nếu người dùng không yêu cầu cụ thể. Bài học tôi rút ra là AI chỉ nên được dùng như một trợ lý có kỷ luật, không phải nguồn kết quả cuối cùng. Người kiểm thử vẫn phải phản biện output, chạy test thực tế, kiểm tra evidence và bổ sung exploratory testing để phát hiện các lỗi logic/bảo mật mà AI dễ bỏ qua.
