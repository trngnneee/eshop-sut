# [BUG][Cart] Không có hộp thoại xác nhận khi xóa sản phẩm khỏi giỏ hàng

## Found by Test Case

GUI-043

## Requirement liên quan

FR-07, FR-24

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows (Local Dev)
- **Browser**: Microsoft Edge (Chromium)
- **URL**: http://localhost:5173/cart
- **Build/Commit**: Latest

## Steps to reproduce

1. Thêm ít nhất một sản phẩm vào giỏ hàng.
2. Mở trang Giỏ hàng (`http://localhost:5173/cart`).
3. Bấm nút "Xóa" ở bất kỳ sản phẩm nào trong danh sách.
4. Quan sát xem có hộp thoại xác nhận không.

## Expected result

- Trước khi xóa sản phẩm khỏi giỏ hàng, hệ thống phải hiển thị hộp thoại xác nhận với nội dung đại loại "Bạn có chắc muốn xóa sản phẩm này khỏi giỏ hàng không?" để tránh việc người dùng vô tình xóa nhầm.

## Actual result

- Khi bấm "Xóa", sản phẩm bị xóa ngay lập tức mà không có bất kỳ bước xác nhận nào.
- Không có cơ chế hoàn tác (undo) sau khi xóa.

## Evidence

[Short Video](../screenshots/bug_cart_no_delete_confirm.mp4)

## Link Github Issue
https://github.com/trngnneee/eshop-sut/issues/252#issue-5022690903