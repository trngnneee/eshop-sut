# [BUG][Admin] Giao diện không đổi tiêu đề và thiếu chỉ báo trạng thái Chế độ Sửa (Edit Mode) khi bấm nút Sửa sản phẩm

## Found by Test Case

Usability Evaluation (Task 2 - Session P04, P06)

## Requirement liên quan

FR-15, FR-22

## Severity / Priority

Major / P2

## Environment

- **OS**: Windows 11 / macOS (Local Dev)
- **Browser**: Microsoft Edge / Google Chrome (Chromium)
- **URL**: http://localhost:5174/ (Tab Quản lý Sản phẩm)
- **Build/Commit**: HW03 SUT Frontend Admin

## Steps to reproduce

1. Đăng nhập Admin và chọn tab "Sản phẩm".
2. Tìm một sản phẩm bất kỳ trong bảng danh sách phía dưới và bấm nút "Sửa" ở cột Hành động.
3. Quan sát sự thay đổi giao diện ở khu vực Form nhập liệu phía trên.

## Expected result

- Khi nhấp nút "Sửa", hệ thống phải cung cấp phản hồi trạng thái rõ ràng thể hiện người dùng đang ở chế độ chỉnh sửa:
  1. Tự động cuộn màn hình (auto-scroll) lên vị trí Form nhập liệu.
  2. Đổi tiêu đề Form từ "Thêm sản phẩm" thành "Cập nhật sản phẩm: [Tên sản phẩm]".
  3. Hiển thị nút "Hủy chỉnh sửa" (Cancel) để cho phép người dùng thoát khỏi chế độ Sửa quay về Thêm mới.

## Actual result

- Giao diện Form vẫn giữ nguyên tiêu đề "Thêm sản phẩm". Dữ liệu của sản phẩm được chọn chỉ được nạp âm thầm vào các ô input mà không có bất kỳ hiệu ứng cuộn, đổi màu viền form hay tiêu đề chỉ báo mode. Người dùng P06 đã kỳ vọng có popup chỉnh sửa riêng nên bấm nút "Sửa" nhiều lần, trong khi P04 do dự không biết thông tin trên form có phải đúng sản phẩm đã chọn hay không.

## Evidence
- Quan sát từ video ghi hình Usability Session P04 (00:57- 01:00) và P06 (00:40).
- P04:
https://drive.google.com/file/d/1At7DY65G0_ATfIWPJqOwTLCnlHwkvc8i/view?usp=drive_link
- P06:
https://drive.google.com/file/d/1pcHWy1eifNEX7UhcaACDaop1unuk8Dj7/view?usp=drive_link

## Link Github Issue
https://github.com/trngnneee/eshop-sut/issues/289#issue-5043391211
