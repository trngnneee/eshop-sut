# [BUG][FR-05 Product Search] Tìm kiếm không xử lý khoảng trắng đầu/cuối

## Found by Test Case

TC-FR05-08

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
2. Nhập từ khóa có khoảng trắng đầu/cuối: `  MacBook  `.
3. Gửi form tìm kiếm.

## Expected result

Hệ thống trim khoảng trắng trước khi tìm kiếm và hiển thị sản phẩm `MacBook Pro M3`.

## Actual result

Không có sản phẩm nào hiển thị, trong khi từ khóa sau khi trim là `MacBook` phải có kết quả phù hợp.

## Link Github Issue:
https://github.com/trngnneee/eshop-sut/issues/330#issue-5102396975

