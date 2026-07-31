# [BUG][Admin] Form Admin thiếu xem trước ảnh và kiểm tra định dạng URL ảnh sản phẩm

## Found by Test Case

GUI-025

## Requirement liên quan

FR-15, FR-22, FR-24

## Severity / Priority

Minor / P2

## Environment

- **OS**: Windows 11 (Local Dev)
- **Browser**: Microsoft Edge (Chromium)
- **URL**: http://localhost:5174/ (Tab Sản phẩm)
- **Build/Commit**: Latest

## Steps to reproduce

1. Đăng nhập Admin và chọn tab "Sản phẩm".
2. Nhập một đường dẫn URL vào ô "URL Ảnh" trong form thêm/sửa sản phẩm.
3. Hoặc nhập một chuỗi không phải định dạng URL (ví dụ: `abcxyz`) vào ô "URL Ảnh".
4. Quan sát xem form có vùng xem trước hình ảnh (image preview) hoặc thông báo lỗi định dạng hay không.

## Expected result

- Form phải có vùng xem trước ảnh (preview thumbnail) trực quan để Admin kiểm tra ảnh trước khi lưu.
- Trường "URL Ảnh" phải kiểm tra định dạng URL hợp lệ (sử dụng `type="url"` hoặc validation) và hiển thị thông báo lỗi/fallback khi URL không hợp lệ.

## Actual result

- Ô "URL Ảnh" là input văn bản thuần túy, không có tính năng xem trước hình ảnh trong form.
- Không có kiểm tra định dạng URL ở frontend, cho phép nhập bất kỳ chuỗi văn bản không hợp lệ nào làm đường dẫn ảnh sản phẩm.

## Evidence
[Short Video](../screenshots/bug_admin_form_image_url_validation.mp4)


## Link Github Issue
https://github.com/trngnneee/eshop-sut/issues/256#issue-5022982674
