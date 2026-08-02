# [BUG][Admin] Ô nhập Giá sản phẩm không tự động loại bỏ khoảng trắng và thông báo lỗi không rõ ràng

## Found by Test Case

Usability Evaluation (Task 2 - Session P05, P07)

## Requirement liên quan

FR-15, FR-22

## Severity / Priority

Minor / P3

## Environment

- **OS**: Windows 11 / macOS (Local Dev)
- **Browser**: Microsoft Edge / Google Chrome (Chromium)
- **URL**: http://localhost:5174/ (Tab Quản lý Sản phẩm)
- **Build/Commit**: Latest

## Steps to reproduce

1. Đăng nhập Admin và chọn tab "Sản phẩm".
2. Tại ô "Giá tiền", nhập giá trị có chứa khoảng trắng theo thói quen định dạng tiền tệ (ví dụ: `40 000 000`).
3. Nhập đầy đủ các trường khác và bấm "Thêm sản phẩm" hoặc "Lưu sản phẩm".
4. Quan sát thông báo lỗi và phản hồi của ô nhập liệu.

## Expected result

- Hệ thống nên tự động loại bỏ khoảng trắng (auto-trim spaces) để xử lý dữ liệu nhập của người dùng, hoặc nếu không cho phép thì phải hiển thị thông báo hướng dẫn cụ thể (ví dụ: "Giá tiền không được chứa khoảng trắng"). Đồng thời ô nhập giá nên hỗ trợ định dạng phân cách hàng nghìn (ví dụ: `40.000.000 ₫`) khi hiển thị để tăng khả năng quan sát.

## Actual result

- Hệ thống chặn submit và chỉ hiển thị thông báo lỗi chung chung tiếng Anh `"Please enter a number."` mà không hướng dẫn định dạng hợp lệ, khiến người dùng P05 lúng túng phải thử xóa khoảng trắng. Ngoài ra, giao diện không có phân cách hàng nghìn khiến người dùng P07 phản ánh khó kiểm tra xem mình đã nhập đúng số lượng số 0 hay chưa.

## Evidence

- Quan sát từ video ghi hình Usability Session P05 (00:45).
https://drive.google.com/file/d/17Nz75CL29KE1X-YRbGxbDcsGLFaZZ9mJ/view?usp=drive_link

## Link Github Issue
https://github.com/trngnneee/eshop-sut/issues/284#issue-5043367692
