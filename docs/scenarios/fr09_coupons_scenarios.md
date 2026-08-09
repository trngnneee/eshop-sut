# Kế Hoạch Kịch Bản Kiểm Thử (Scenario Planning) — FR-09: Mã Giảm Giá

**Tính năng:** FR-09 - Discount Coupons  
**Sinh viên:** Phan Quốc Thịnh | **MSSV:** 23127486 | **Lớp:** 23KTPM3  

---

## Danh Sách 12 Ca Kiểm Thử (Test Scenarios)

| Mã TC | Phân loại | Tên kịch bản | Mô tả chi tiết | Kỳ vọng theo SRS |
|:---|:---:|:---|:---|:---|
| **TC01** | Positive | Áp dụng mã phần trăm SAVE10 | Đơn hàng 500k (> 300k min order), nhập SAVE10 | Áp dụng thành công, giảm 10% |
| **TC02** | Positive | Áp dụng mã cố định BIGBUY | Đơn hàng 600k (> 500k min order), nhập BIGBUY | Áp dụng thành công, giảm 50.000 ₫ |
| **TC03** | Positive | Áp dụng mã cố định VIP100 | Đơn hàng 400k (> 300k min order), nhập VIP100 | Áp dụng thành công, giảm 100.000 ₫ |
| **TC04** | Positive | Nhập mã chữ thường 'save10' | Nhập 'save10', hệ thống tự động uppercase | Áp dụng thành công như SAVE10 |
| **TC05** | Negative | Mã không tồn tại | Nhập mã 'INVALIDCODE99' | Báo lỗi mã không hợp lệ |
| **TC06** | Negative | Mã đã hết hạn | Nhập mã 'EXPIRED' | Báo lỗi mã đã hết hạn sử dụng |
| **TC07** | Negative | Đơn hàng dưới mức tối thiểu | Đơn hàng 200k (< 500k min order), nhập BIGBUY | Báo lỗi đơn hàng chưa đủ giá trị tối thiểu |
| **TC08** | Edge | Đơn hàng bằng đúng mức tối thiểu | Đơn hàng 300k (== 300k min order), nhập SAVE10 | Áp dụng thành công, giảm 10% |
| **TC09** | Negative | Để trống ô nhập mã | Không nhập mã giảm giá | Nút "Áp dụng" bị disabled |
| **TC10** | Edge | SQL Injection payload | Nhập mã payload `' OR '1'='1` | Hệ thống xử lý an toàn, báo lỗi không hợp lệ |
| **TC11** | Edge | Khoảng trắng thừa | Nhập mã `'  SAVE10  '` | Tự động trim khoảng trắng và áp dụng thành công |
| **TC12** | Edge | Đổi tổng tiền sau khi áp dụng | Đổi tổng tiền giỏ hàng sau khi đã áp dụng mã | Hệ thống tự động reset trạng thái mã giảm giá |
