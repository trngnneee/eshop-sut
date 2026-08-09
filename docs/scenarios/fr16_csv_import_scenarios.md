# Kế Hoạch Kịch Bản Kiểm Thử (Scenario Planning) — FR-16: Import Sản Phẩm từ CSV

**Tính năng:** FR-16 - Product Import from CSV (Admin)  
**Sinh viên:** Phan Quốc Thịnh | **MSSV:** 23127486 | **Lớp:** 23KTPM3  

---

## Danh Sách 12 Ca Kiểm Thử (Test Scenarios)

| Mã TC | Phân loại | Tên kịch bản | Mô tả chi tiết | Kỳ vọng theo SRS |
|:---|:---:|:---|:---|:---|
| **TC01** | Positive | Import file chuẩn 1 sản phẩm | Upload `fr16_sample_valid.csv` (đầy đủ các cột chuẩn) | Import thành công 1/1 sản phẩm |
| **TC02** | Positive | Import hàng loạt nhiều sản phẩm | Upload `fr16_sample_batch.csv` (3 sản phẩm thuộc nhiều danh mục) | Import thành công 3/3 sản phẩm |
| **TC03** | Positive | Header tiếng Việt | Upload `fr16_sample_vietnamese_headers.csv` (ten, gia, mo_ta, image, danh_muc) | Tự động ánh xạ cột và import thành công 1 sản phẩm |
| **TC04** | Positive | Header tiếng Anh viết hoa | Upload `fr16_sample_capitalized_headers.csv` (Name, Price, Description, Image, Category_id) | Tự động ánh xạ cột và import thành công 1 sản phẩm |
| **TC05** | Negative | Thiếu tên sản phẩm bắt buộc | Upload `fr16_sample_missing_name.csv` (dòng sản phẩm không có tên) | Báo lỗi chi tiết dòng thiếu tên sản phẩm |
| **TC06** | Negative | File CSV chứa dòng lỗi (Rollback) | Upload `fr16_sample_mixed.csv` (lẫn lộn dòng đúng và dòng thiếu tên) | **SRS: Rollback toàn bộ transaction, 0 sản phẩm được import** |
| **TC07** | Edge | Ký tự tiếng Việt Unicode & đặc biệt | Upload `fr16_sample_special_chars.csv` | Lưu trữ chính xác ký tự tiếng Việt có dấu và ký tự đặc biệt |
| **TC08** | Edge | File CSV rỗng chỉ có header | Upload `fr16_sample_empty.csv` (0 dòng dữ liệu) | Bảng preview rỗng, nút Import bị disabled |
| **TC09** | Positive | Kiểm tra link tải file mẫu | Kiểm tra link "Tải file mẫu (template.csv)" | Có thuộc tính download và href chuẩn data:text/csv |
| **TC10** | Positive | Kiểm tra bảng xem trước (Preview) | Upload file 3 sản phẩm và đếm số dòng xem trước | Hiển thị chính xác 3 dòng trước khi bấm Import |
| **TC11** | Negative | Yêu cầu xác thực Admin | Truy cập khi chưa đăng nhập Admin Token | Chặn truy cập và chuyển hướng về trang Admin Login |
| **TC12** | Edge | Kiểm tra lưu trữ vào CSDL | Import 1 sản phẩm và reload kiểm tra bảng danh sách | Sản phẩm mới hiển thị trong bảng dữ liệu sản phẩm |
