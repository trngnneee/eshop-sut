# [BUG][Storefront] Nút "Thêm vào giỏ hàng" yêu cầu bấm 2 lần mới có phản hồi ở lần bấm đầu tiên

## Found by Test Case

GUI-047

## Requirement liên quan

FR-06, FR-24

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows 11 (Local Dev)
- **Browser**: Microsoft Edge Headless (Chromium)
- **URL**: http://localhost:5173/product/1
- **Build/Commit**: Latest

## Steps to reproduce

1. Mở trang chi tiết sản phẩm bất kỳ (ví dụ: `http://localhost:5173/product/1`).
2. Ở lần đầu tiên thêm sản phẩm, bấm nút "Thêm vào giỏ hàng" duy nhất một lần.
3. Quan sát phản hồi của trang web và badge giỏ hàng trên navbar.

## Expected result

- Ngay khi người dùng click vào nút lần đầu tiên, hệ thống phải thực hiện thêm sản phẩm vào giỏ hàng, cập nhật badge giỏ hàng lập tức, và thay đổi trạng thái nút thành "Đã thêm" hoặc hiển thị thông báo phản hồi (toast/alert) để người dùng biết.

## Actual result

- Khi bấm nút lần đầu tiên, không có bất kỳ hành động nào được thực hiện (badge không tăng, không có thông báo, trạng thái nút giữ nguyên).

## Evidence

[Short Video](../screenshots/bug_add_to_cart_clicks.mp4)

## Link Github Issue
https://github.com/trngnneee/eshop-sut/issues/261#issue-5023186020
