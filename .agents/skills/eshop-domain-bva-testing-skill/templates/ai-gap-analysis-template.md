# AI Gap Analysis: [FEATURE_ID] - [FEATURE_NAME]

Báo cáo này phân tích khoảng cách giữa các kết quả do công cụ AI tự động sinh ra và những phát hiện thực tế sau khi có sự can thiệp, kiểm tra trực tiếp của con người (Human-in-the-loop).

## 1. Kết Quả Do AI Tự Động Tạo Ra (What AI Generated)
* **Số lượng test case ban đầu:** [Ví dụ: 12 test cases]
* **Nội dung chính:** [Tóm tắt sơ lược các trường hợp AI đã bao phủ tốt, ví dụ: kiểm tra các giá trị biên của quantity, kiểm tra email đúng/sai định dạng]

## 2. Những Gì AI Đã Bỏ Sót (What AI Missed)

### Các test case bị thiếu (Missing Test Cases)
* [Liệt kê các kịch bản kiểm thử quan trọng mà AI không tự nghĩ ra được, ví dụ: test case đồng thời (concurrency), kiểm thử logic giỏ hàng khi người dùng chuyển tab trình duyệt, kiểm thử cookie/session hết hạn].

### Các lỗi thực tế bị thiếu (Missing Bugs)
* [Liệt kê các bug thực tế tìm thấy trên hệ thống SUT nhưng AI không dự đoán được trong quá trình thiết kế test case tĩnh].

## 3. Lý Do AI Bỏ Sót (Why AI Missed Them)

### Vấn đề về chất lượng Prompt (Prompt Quality Issues)
* [Ví dụ: Prompt ban đầu chưa cung cấp đủ các trạng thái lưu trữ của session và cookie trên trình duyệt].

### Hạn chế của công cụ AI (AI Limitations)
* [Ví dụ: AI không có khả năng tương tác trực tiếp với giao diện người dùng động (dynamic UI) hoặc không cảm nhận được trải nghiệm phản hồi chậm trễ từ server].

### Độ phức tạp của tính năng (Feature Complexity)
* [Ví dụ: Logic tích hợp giữa API Backend và Client-side State Manager của tính năng này quá phức tạp, tài liệu spec không mô tả chi tiết].

## 4. Sự Điều Chỉnh Của Con Người (Human Correction)
* [Mô tả chi tiết những thay đổi, bổ sung cụ thể mà bạn (sinh viên) đã thực hiện để hoàn thiện bộ test case và tài liệu báo cáo].

## 5. Bài Học Rút Ra (Lessons Learned)
* [Rút ra kinh nghiệm xương máu về việc cộng tác với AI trong quá trình kiểm thử phần mềm, thể hiện mức Bloom G9.3].
