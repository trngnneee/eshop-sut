# AI Critique — Task 3

**Status:** `READY_FOR_STUDENT_REVIEW`

## Critique

AI hỗ trợ tốt ở phần biến checklist 58 mục thành một quy trình có thể lặp lại trên nhiều browser. Nó tạo overlay chứa họ tên, MSSV, email, phiên bản browser, thiết bị, URL localhost và timestamp, đồng thời nối mỗi kết quả với screenshot cụ thể. Việc dùng dữ liệu synthetic và cleanup sau test cũng giúp tránh làm bẩn database bằng category, product hoặc account thử nghiệm.

Tuy nhiên, AI đã sai ở ba điểm quan trọng. Đầu tiên, locator điều hướng ban đầu khớp cả link trong header và trong form, khiến ba kết quả Chrome bị thiếu. Thứ hai, proxy cho Expo Web truyền `Content-Type` khi Promise chưa được `await`, làm backend trả 500 và suýt biến lỗi test harness thành bug Mobile Login. Thứ ba, AI click vào trang trước khi kiểm tra bàn phím, vô tình thay đổi điểm bắt đầu focus và tạo ra khác biệt WebKit không có thật. Chỉ khi đối chiếu console, source và chuỗi Tab đầy đủ, các lỗi này mới được phát hiện và evidence được chụp lại.

Bài học quan trọng là automation output không tự động trở thành bằng chứng đáng tin. Mỗi kết quả bất thường phải được kiểm tra xem nguyên nhân nằm ở SUT, browser hay test harness. Ngoài ra, WebKit trên Windows và Pixel emulation có giá trị cho kiểm tra tương thích nhưng không thể được gọi là Safari hoặc Android thật chỉ để đủ ba nền tảng. Trung thực về giới hạn môi trường quan trọng hơn việc đổi nhãn để validator báo Complete.

## Student review

- Review date: `PENDING_STUDENT_REVIEW`
- Confirmation: `PENDING_STUDENT_REVIEW`

