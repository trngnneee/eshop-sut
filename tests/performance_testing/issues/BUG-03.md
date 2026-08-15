---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Products] GET /api/products/:id trả HTTP 200 + {} cho id không tồn tại (đúng ra phải 404)'
labels: ['type: bug', 'status: new', 'found-by: test-case', 'severity: minor']
assignees: ''
---

## Found by Test Case

Phát hiện khi review source lúc thiết kế assertion cho các plan (lý do dùng content-assertion thay vì chỉ status code — xem AI Audit Finding #7).

## Requirement liên quan

FR-06 (Product detail view)

## Severity / Priority

Minor / P2

## Environment

- **OS**: macOS 15.5 (Darwin 24.5.0), Apple M4
- **Browser**: N/A — Backend REST API (curl)
- **URL**: http://localhost:3000/api/products/999
- **Build/Commit**: eshop-sut (HW05 SUT) · `backend/server.js` dòng 159–165

## Steps to reproduce

1. Gọi: `curl -i "http://localhost:3000/api/products/999"` (id không tồn tại).
2. Quan sát status code và body.

## Expected result

Trả về **HTTP 404 Not Found** (hoặc mã lỗi phù hợp) khi sản phẩm không tồn tại.

## Actual result

- `server.js:161`: `if (!row) return res.status(200).json({});` — id không tồn tại vẫn trả **HTTP 200** với body rỗng `{}`.
- Hệ quả: client/monitor khó phát hiện lỗi; test nào chỉ assert status code sẽ báo "0% error" trong khi dữ liệu sai.

## Evidence

Output `curl -i` (HTTP/1.1 200 OK + body `{}`).
![BUG-03](https://res.cloudinary.com/dnqinxiwo/image/upload/v1786794397/eshop-hw05/perf-bugs/BUG-03.png)
