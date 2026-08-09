# [BUG][FR-05 Product Listing] Giá sản phẩm hiển thị sai đơn vị tiền tệ

## Found by Test Case

TC-FR05-03

## Requirement liên quan

FR-05

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows
- **Browser**: Chromium, Firefox, WebKit
- **URL**: http://localhost:5173/
- **Build/Commit**: Latest

## Steps to reproduce

1. Mở trang chủ web.
2. Chờ danh sách sản phẩm tải xong.
3. Kiểm tra giá của sản phẩm `iPhone 15 Pro Max`.

## Expected result

Giá sản phẩm hiển thị theo đặc tả FR-05 với đơn vị `₫`, ví dụ `30,000,000 ₫`.

## Actual result

Giá hiển thị là `30,000,000 VND`, sai đơn vị tiền tệ so với yêu cầu.

## Link Github Issue:
https://github.com/trngnneee/eshop-sut/issues/25#issue-4746056657