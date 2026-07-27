# Minh Chứng Kiểm Thử Đa Trình Duyệt / Đa Nền Tảng (Cross-Browser & Cross-Platform Evidence)

Tài liệu này tổng hợp các ảnh chụp màn hình kiểm thử đa trình duyệt/đa nền tảng trên hệ thống SUT EShop (Task 3).

---

## 1. Danh Sách Các Nền Tảng Kiểm Thử (Platforms Used)

Sinh viên thực hiện kiểm thử trên **tối thiểu 3 nền tảng** khác nhau. Dưới đây là các nền tảng được chọn:

1. **Nền tảng 1 (Web - Chrome):**
   - Hệ điều hành: `[Ví dụ: Windows 11]`
   - Trình duyệt & Phiên bản: `[Ví dụ: Google Chrome v120.0]`
   - Công cụ sử dụng: `[Ví dụ: Trình duyệt máy tính thực tế / BrowserStack]`
2. **Nền tảng 2 (Web - Firefox/Safari):**
   - Hệ điều hành: `[Ví dụ: macOS Sonoma / iOS 17]`
   - Trình duyệt & Phiên bản: `[Ví dụ: Firefox v121.0 / Apple Safari]`
   - Công cụ sử dụng: `[Ví dụ: LambdaTest / Thiết bị di động thực tế]`
3. **Nền tảng 3 (Web Mobile hoặc Mobile App qua Expo Go):**
   - Thiết bị: `[Ví dụ: iPhone 13 / Samsung Galaxy S22]`
   - Trình duyệt/Ứng dụng: `[Ví dụ: Safari Mobile / Expo Go Mobile App]`
   - Công cụ sử dụng: `[Ví dụ: Thiết bị thực tế của sinh viên]`

---

## 2. Ảnh Chụp Màn Hình Minh Chứng (Screenshots with Watermark)

*LƯU Ý QUAN TRỌNG: Mọi ảnh chụp màn hình dưới đây bắt buộc phải hiển thị rõ thông tin xác thực bao gồm: Địa chỉ URL localhost của SUT, thông tin hệ điều hành/trình duyệt, và có chèn chìm (overlay watermark) dạng text: **Địa chỉ Email sinh viên hoặc Mã số sinh viên + Họ tên** để chứng minh tính trung thực.*

### 2.1. Minh chứng trên Nền tảng 1: Chrome (Windows/macOS)
- **Màn hình/Chức năng chụp:** `[Ví dụ: Trang chủ EShop trên Chrome]`
- **Ảnh chụp:**
  `![Nền tảng 1 Screenshot](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/docs/submission/screenshots/platform_01_chrome.png)`

---

### 2.2. Minh chứng trên Nền tảng 2: Firefox hoặc Safari (macOS/iOS)
- **Màn hình/Chức năng chụp:** `[Ví dụ: Giỏ hàng trên Safari]`
- **Ảnh chụp:**
  `![Nền tảng 2 Screenshot](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/docs/submission/screenshots/platform_02_safari.png)`

---

### 2.3. Minh chứng trên Nền tảng 3: Mobile Web hoặc Mobile App (Expo Go)
- **Màn hình/Chức năng chụp:** `[Ví dụ: Chi tiết sản phẩm trên thiết bị di động thực tế]`
- **Ảnh chụp:**
  `![Nền tảng 3 Screenshot](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/docs/submission/screenshots/platform_03_mobile.png)`

---

## 3. Nhật Ký Ghi Nhận Lỗi Đa Nền Tảng (Cross-Platform Specific Findings)

*Ghi lại bất kỳ lỗi nào chỉ xảy ra trên một trình duyệt hoặc nền tảng cụ thể mà không xuất hiện trên các nền tảng khác.*

- **Lỗi tương thích 1:** `[Ví dụ: Hiệu ứng chuyển động bị giật lag trên trình duyệt Firefox di động, trong khi Chrome chạy mượt mà]` (Liên kết lỗi: BUG-xx nếu có)
- **Lỗi tương thích 2:** `[Ví dụ: Giao diện trang Thanh toán bị tràn viền (overflow) trên Safari iOS khiến thanh cuộn ngang xuất hiện]`
