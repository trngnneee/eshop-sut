---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Products] GET /api/products/:id trả price khác kiểu dữ liệu giữa id chẵn/lẻ'
labels: ['type: bug', 'status: new', 'found-by: test-case', 'severity: minor']
assignees: ''
---

## Found by Test Case

Phát hiện khi review source `GET /api/products/:id` trong lúc thiết kế workflow read-heavy.

## Requirement liên quan

FR-06 (Product detail view)

## Severity / Priority

Minor / P2

## Environment

- **OS**: macOS 15.5 (Darwin 24.5.0), Apple M4
- **Browser**: N/A — Backend REST API (curl)
- **URL**: http://localhost:3000/api/products/1 và /api/products/2
- **Build/Commit**: eshop-sut (HW05 SUT) · `backend/server.js` dòng 159–165

## Steps to reproduce

1. Gọi id lẻ: `curl "http://localhost:3000/api/products/1"` → `"price":30000000` (number).
2. Gọi id chẵn: `curl "http://localhost:3000/api/products/2"` → `"price":"28000000"` (string).
3. So sánh kiểu dữ liệu của trường `price` giữa 2 phản hồi.

## Expected result

Trường `price` luôn cùng một kiểu dữ liệu (number) cho mọi sản phẩm.

## Actual result

- `server.js:162`: `if (row.id % 2 === 0) row.price = row.price.toString();` — sản phẩm **id chẵn** trả `price` dạng **string**, **id lẻ** dạng **number**.
- Hệ quả: client parse giá không nhất quán, dễ sinh bug tính tiền / so sánh giá.

## Evidence

Output curl 2 sản phẩm id chẵn vs lẻ (khác kiểu `price`).
![BUG-04](https://res.cloudinary.com/dnqinxiwo/image/upload/v1786794399/eshop-hw05/perf-bugs/BUG-04.png)
