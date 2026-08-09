# [BUG][FR-05 Product Listing] Trang chủ có nhiều hơn một thẻ h1

## Found by Test Case

TC-FR05-13

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
3. Đếm số lượng thẻ `<h1>` trong document.

## Expected result

Trang chủ chỉ có đúng một thẻ `<h1>`.

## Actual result

Trang chủ có 2 thẻ `<h1>`.

## Link Github Issue
https://github.com/trngnneee/eshop-sut/issues/29#issue-4746987185
