# [BUG][Admin] Không có hộp thoại xác nhận trước khi xóa sản phẩm

## Found by Test Case

GUI-053

## Requirement liên quan

FR-24

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows 11 (Local Dev)
- **Browser**: Microsoft Edge (Chromium)
- **URL**: http://localhost:5174/ (Tab Sản phẩm)
- **Build/Commit**: Latest

## Steps to reproduce

1. Đăng nhập Admin và chọn tab "Sản phẩm".
2. Tìm bất kỳ sản phẩm nào trong danh sách.
3. Bấm nút "Xóa" ở cột Hành động.
4. Quan sát xem có hộp thoại xác nhận (confirmation dialog) hiện ra hay không.

## Expected result

- Vì xóa sản phẩm là thao tác phá hủy dữ liệu (destructive action), hệ thống phải hiển thị hộp thoại xác nhận "Bạn có chắc muốn xóa sản phẩm này không?" trước khi thực sự xóa theo tiêu chuẩn FR-24.

## Actual result

- Khi bấm nút "Xóa", hệ thống lập tức gửi request xóa và gỡ sản phẩm khỏi danh sách mà không qua bất kỳ bước xác nhận nào, tiềm ẩn rủi ro mất dữ liệu do thao tác nhầm.

## Evidence

[Short Video](../screenshots/bug_admin_no_delete_confirm.mp4)

## Link Github Issue
https://github.com/trngnneee/eshop-sut/issues/255#issue-5022909296
