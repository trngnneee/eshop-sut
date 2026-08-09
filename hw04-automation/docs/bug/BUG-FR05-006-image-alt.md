# [BUG][FR-05 Product Listing] Ảnh sản phẩm thiếu alt text mô tả

## Found by Test Case

TC-FR05-12

## Requirement liên quan

FR-05

## Severity / Priority

Minor / P2

## Environment

- **OS**: Windows
- **Browser**: Chromium, Firefox, WebKit
- **URL**: http://localhost:5173/
- **Build/Commit**: Latest

## Steps to reproduce

1. Mở trang chủ web.
2. Chờ danh sách sản phẩm tải xong.
3. Kiểm tra thuộc tính `alt` của ảnh sản phẩm `iPhone 15 Pro Max`.

## Expected result

Ảnh sản phẩm có `alt` khác rỗng và mô tả đúng sản phẩm, ví dụ `iPhone 15 Pro Max`.

## Actual result

Ảnh sản phẩm có `alt=""`.

## Link Github Issue
https://github.com/trngnneee/eshop-sut/issues/331#issue-5102431313

