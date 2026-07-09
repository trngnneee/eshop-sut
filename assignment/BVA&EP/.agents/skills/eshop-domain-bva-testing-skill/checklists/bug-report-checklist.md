# Bug Report Checklist

Đảm bảo báo cáo lỗi đạt tiêu chuẩn chuyên nghiệp, đầy đủ thông tin phục vụ sửa lỗi.

## 1. Thông Tin Nhận Diện Lỗi
- [ ] Mã lỗi có đặt đúng định dạng `BUG-[Mã FR]-[Ký tự Pool]-[Số thứ tự]` không? (Ví dụ: `BUG-FR07-B-01`).
- [ ] Tiêu đề lỗi (Title) có cấu trúc `[BUG][Tên Module] Tóm tắt ngắn gọn lỗi` chưa?
- [ ] Mức độ nghiêm trọng (Severity) và Độ ưu tiên (Priority) đã được đánh giá đúng chưa?
- [ ] Có liên kết trực tiếp đến Test Case ID phát hiện lỗi không?

## 2. Tái Hiện Lỗi (Reproducibility)
- [ ] Thông tin môi trường (OS, Browser, URL, Commit Hash) có chính xác không?
- [ ] Các bước tái hiện (Steps to Reproduce) có được viết rõ ràng, mạch lạc, ai cũng có thể làm theo để thấy lỗi không?
- [ ] Có phân biệt rõ kết quả thực tế (Actual Result) lỗi và kết quả mong đợi (Expected Result) đúng không?

## 3. Minh Chứng Lỗi (Evidence - Cực kỳ quan trọng)
- [ ] Báo cáo đã đính kèm ảnh chụp màn hình thực tế (screenshot) chưa?
- [ ] Ảnh chụp màn hình có được khoanh đỏ hoặc đánh dấu chỉ rõ điểm lỗi không?
- [ ] Đường dẫn ảnh trong file Markdown có sử dụng đường dẫn tuyệt đối hoặc tương đối hợp lệ để hiển thị được ảnh không?
- [ ] File ảnh screenshot có được đặt tên đúng chuẩn và lưu trữ trong thư mục `evidence/` không?

## 4. GitHub Issue & Đề Xuất
- [ ] Đã đẩy lỗi lên GitHub Issues thành công chưa?
- [ ] Đã cập nhật mã Issue (ví dụ: `#23`) hoặc link Issue vào báo cáo lỗi và file Test Run tương ứng chưa?
- [ ] Có đề xuất sửa lỗi (Suggested Fix) thể hiện sự phân tích kỹ thuật của tester không?
