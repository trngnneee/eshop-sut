# Bản Tự Phê Bình AI trong Kiểm Thử Hiệu Năng (AI Critique)

> **Mã số sinh viên:** 23127207 (Khoa)  
> **Kịch bản:** Browse-to-buy · **Phạm vi:** 5 Endpoints SUT EShop  

Trong bài tập HW05 về Kiểm thử Hiệu năng, AI thể hiện năng lực vượt trội trong việc tự động hóa các tác vụ lặp đi lặp lại như sinh cấu trúc XML cho Apache JMeter, xây dựng kịch bản CI/CD trên GitHub Actions và viết script toán học phân tích log `.jtl`. Nhờ đó, thời gian thiết lập hạ tầng kiểm thử được rút ngắn đáng kể từ nhiều ngày xuống còn vài giờ.

Tuy nhiên, khi đối diện với các bài toán phân tích chuyên sâu và hiểu biết ngữ cảnh hệ thống, AI bộc lộ những điểm yếu chí mạng. Điển hình nhất là xu hướng "suy diễn theo khuôn mẫu chung" (generic pattern bias): khi thấy độ trễ tăng cao, AI lập tức đổ lỗi cho cơ sở dữ liệu thiếu Index mà không nhận ra truy vấn `SELECT * FROM products` vốn quét toàn bộ bảng không có điều kiện lọc. Tương tự, AI nhầm lẫn giữa lỗi quá tải CPU và lỗi nghiệp vụ khóa tài khoản do bug logic phần mềm (`login_attempts += 2`), đồng thời đề xuất các giải pháp phi thực tế như cấu hình Connection Pool cho SQLite.

Những sai sót này khẳng định AI chưa thể thay thế tư duy phản biện của kỹ sư kiểm thử. AI chỉ thực sự phát huy tối đa giá trị khi được vận hành dưới sự định hướng, chất vấn và kiểm chứng chéo chặt chẽ từ con người.
