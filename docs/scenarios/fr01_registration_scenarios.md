# Kế Hoạch Kịch Bản Kiểm Thử (Scenario Planning) — FR-01: Đăng Ký Tài Khoản

**Tính năng:** FR-01 - Account Registration  
**Sinh viên:** Phan Quốc Thịnh | **MSSV:** 23127486 | **Lớp:** 23KTPM3  

---

## Danh Sách 12 Ca Kiểm Thử (Test Scenarios)

| Mã TC | Phân loại | Tên kịch bản | Mô tả chi tiết | Kỳ vọng theo SRS |
|:---|:---:|:---|:---|:---|
| **TC01** | Positive | Đăng ký thông tin hợp lệ | Nhập Tên, Email mới, Mật khẩu thỏa mãn chính sách bảo mật | Đăng ký thành công, chuyển sang `/login` |
| **TC02** | Positive | Đăng ký họ tên tiếng Việt Unicode | Nhập họ tên có dấu tiếng Việt Unicode ("Phan Quốc Thịnh") | Đăng ký thành công, hiển thị chính xác tên |
| **TC03** | Negative | Để trống trường Họ Tên | Bỏ trống Họ Tên, nhập đầy đủ Email và Mật khẩu | Trình duyệt chặn gửi (HTML5 required) |
| **TC04** | Negative | Để trống trường Email | Bỏ trống Email, nhập đầy đủ Họ Tên và Mật khẩu | Trình duyệt chặn gửi (HTML5 required) |
| **TC05** | Negative | Email sai định dạng RFC | Nhập chuỗi email không có domain/ký tự @ ("invalidemailformat") | Trình duyệt chặn gửi form, ở lại `/register` |
| **TC06** | Negative | Để trống trường Mật khẩu | Bỏ trống Mật khẩu, nhập đầy đủ Họ Tên và Email | Trình duyệt chặn gửi (HTML5 required) |
| **TC07** | Negative | Mật khẩu quá ngắn (< 8 ký tự) | Nhập mật khẩu chỉ có 3 ký tự ("Sh1 ") | Hiển thị thông báo mật khẩu quá yếu |
| **TC08** | Negative | Mật khẩu thiếu chữ in hoa | Nhập mật khẩu toàn chữ thường và số | Hiển thị thông báo mật khẩu quá yếu |
| **TC09** | Negative | Mật khẩu thiếu chữ in thường | Nhập mật khẩu toàn chữ in hoa và số | Hiển thị thông báo mật khẩu quá yếu |
| **TC10** | Negative | Mật khẩu thiếu chữ số | Nhập mật khẩu chỉ có chữ cái | Hiển thị thông báo mật khẩu quá yếu |
| **TC11** | Negative | Email đã tồn tại trong CSDL | Đăng ký với email đã có trong hệ thống ("admin@eshop.com") | Báo lỗi email đã được sử dụng |
| **TC12** | Edge | Mật khẩu mạnh có ký tự đặc biệt | Nhập mật khẩu chuẩn an toàn ("StrongPass123!@") | Đăng ký thành công, chuyển sang `/login` |
