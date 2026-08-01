# Minh Chứng Kiểm Thử Đa Trình Duyệt / Đa Nền Tảng (Cross-Browser & Cross-Platform Evidence)

Tài liệu này tổng hợp các ảnh chụp màn hình kiểm thử đa trình duyệt/đa nền tảng trên hệ thống SUT EShop (Task 3).

---

## 1. Danh Sách Các Nền Tảng Kiểm Thử (Platforms Used)

Sinh viên thực hiện kiểm thử trên **tối thiểu 3 nền tảng** khác nhau. Dưới đây là các nền tảng được chọn:

1. **Nền tảng 1 (Web - Google Chrome):**
   - Hệ điều hành: Windows 11
   - Trình duyệt & Phiên bản: Google Chrome v127
   - Công cụ sử dụng: Trình duyệt máy tính thực tế (chạy cục bộ)
2. **Nền tảng 2 (Web - Microsoft Edge):**
   - Hệ điều hành: Windows 11
   - Trình duyệt & Phiên bản: Microsoft Edge v127
   - Công cụ sử dụng: Trình duyệt máy tính thực tế (chạy cục bộ)
3. **Nền tảng 3 (Web Mobile Responsive):**
   - Thiết bị: iPhone 12 Pro Emulation
   - Trình duyệt/Ứng dụng: Google Chrome DevTools Mobile Emulator
   - Công cụ sử dụng: Trình duyệt máy tính của sinh viên emulating thiết bị di động

---

## 2. Ảnh Chụp Màn Hình Minh Chứng (Screenshots with Watermark)

*LƯU Ý QUAN TRỌNG: Mọi ảnh chụp màn hình dưới đây bắt buộc phải hiển thị rõ thông tin xác thực bao gồm: Địa chỉ URL localhost của SUT, thông tin hệ điều hành/trình duyệt, và có chèn chìm (overlay watermark) dạng text: **pqthinh231@clc.fitus.edu.vn** để chứng minh tính trung thực.*

### 2.1. Minh chứng trên Nền tảng 1: Chrome (Windows)
- **Màn hình/Chức năng chụp:** Trang Cá nhân người dùng trên Chrome (http://localhost:5173/profile) hiển thị đầy đủ form thông tin và Lịch sử đơn hàng rỗng ban đầu.
- **Ảnh chụp:**
  `![Nền tảng 1 Screenshot](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/docs/submission/screenshots/customer_profile.png)`

---

### 2.2. Minh chứng trên Nền tảng 2: Microsoft Edge / Chrome Admin
- **Màn hình/Chức năng chụp:** Trang Quản lý người dùng của Admin (http://localhost:5174/) hiển thị danh sách người dùng đã đăng ký trong cơ sở dữ liệu.
- **Ảnh chụp:**
  `![Nền tảng 2 Screenshot](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/docs/submission/screenshots/admin_users.png)`

---

### 2.3. Minh chứng trên Nền tảng 3: Mobile Web (iPhone 12 Pro responsive)
- **Màn hình/Chức năng chụp:** Biểu mẫu cập nhật hồ sơ hiển thị báo lỗi regex khi nhập số điện thoại bắt đầu bằng 0 trên chế độ di động.
- **Ảnh chụp:**
  `![Nền tảng 3 Screenshot](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/docs/submission/screenshots/bug_profile_phone.png)`

---

## 3. Nhật Ký Ghi Nhận Lỗi Đa Nền Tảng (Cross-Platform Specific Findings)

*Ghi lại bất kỳ lỗi nào chỉ xảy ra trên một trình duyệt hoặc nền tảng cụ thể mà không xuất hiện trên các nền tảng khác.*

- **Lỗi tương thích 1:** Tiêu đề của tab trình duyệt luôn là "Vite + React" trên cả Chrome và Edge cho cả User Portal và Admin Portal, không thay đổi linh hoạt theo phân hệ trang hiện tại (lỗi chung cả 2 trình duyệt).
- **Lỗi tương thích 2:** Bảng Lịch sử đơn hàng hiển thị tốt trên Desktop, nhưng khi thu nhỏ về chiều rộng màn hình Mobile (dưới 375px), bảng bị tràn ngang nhẹ (overflow-x) khiến người dùng phải vuốt ngang để xem hết cột Thao tác "Hủy đơn" (phát hiện trên Nền tảng 3).
