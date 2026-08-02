# [BUG][Admin] Form Admin thiếu thông báo phản hồi (Toast/Alert) sau khi Thêm hoặc Sửa sản phẩm thành công

## Found by Test Case

Usability Evaluation (Task 2 - Session P02, P06)

## Requirement liên quan

FR-22, FR-24

## Severity / Priority

Major / P2

## Environment

- **OS**: Windows 11 / macOS (Local Dev)
- **Browser**: Microsoft Edge / Google Chrome (Chromium)
- **URL**: http://localhost:5174/ (Tab Quản lý Sản phẩm)
- **Build/Commit**: HW03 SUT Frontend Admin

## Steps to reproduce

1. Đăng nhập Admin và chọn tab "Sản phẩm".
2. Điền đầy đủ thông tin hợp lệ vào form "Thêm sản phẩm" (Tên, Giá, Danh mục, Hình ảnh).
3. Bấm nút "Thêm sản phẩm" (hoặc chọn "Sửa" một sản phẩm và bấm "Lưu sản phẩm").
4. Quan sát phản hồi của giao diện ứng dụng ngay sau khi click nút Submit.

## Expected result

- Hệ thống phải hiển thị thông báo phản hồi trực quan rõ ràng (ví dụ: Toast notification "Thêm sản phẩm thành công!" hoặc Banner xanh ở góc trên/dưới form) để xác nhận thao tác thành công theo tiêu chuẩn phản hồi giao diện FR-22, FR-24.

## Actual result

- Giao diện không hiển thị bất kỳ thông báo phản hồi xác nhận thành công nào. Form chỉ âm thầm reset/clear dữ liệu (hoặc ghi nhận dữ liệu xuống bảng bên dưới), khiến người dùng phân vân không biết hệ thống đã lưu hay chưa. Người dùng P06 đã nhấp nút lưu/sửa liên tục nhiều lần, và P04/P02 phải cuộn danh sách kiểm tra thủ công.

## Evidence

- Quan sát từ video ghi hình Usability Session P02 (00:47) và P06 (00:20 - 00:40).
- P02:
https://drive.google.com/file/d/1kswcDppiDF5CHbD2J8N4UO6oj2hwL-d9/view?usp=drive_link
- P06:
https://drive.google.com/file/d/1pcHWy1eifNEX7UhcaACDaop1unuk8Dj7/view?usp=drive_link

## Link Github Issue
https://github.com/trngnneee/eshop-sut/issues/290#issue-5043422680
