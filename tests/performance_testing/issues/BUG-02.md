---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Products] SQL Injection ở GET /api/products?search — nối chuỗi trực tiếp vào SQL'
labels: ['type: bug', 'status: new', 'found-by: test-case', 'severity: critical', 'security']
assignees: ''
---

## Found by Test Case

PERF-LOAD-01 / PERF-STRESS-01 / PERF-SPIKE-01 (bước read-heavy `GET /api/products?search=`) — phát hiện khi review source để chọn keyword an toàn cho CSV.

## Requirement liên quan

FR-05 (Product listing and search)

## Severity / Priority

Critical / P0

## Environment

- **OS**: macOS 15.5 (Darwin 24.5.0), Apple M4
- **Browser**: N/A — Backend REST API (curl)
- **URL**: http://localhost:3000/api/products?search=
- **Build/Commit**: eshop-sut (HW05 SUT) · `backend/server.js` dòng 143–151

## Steps to reproduce

1. Gọi: `curl "http://localhost:3000/api/products?search='"` (một dấu nháy đơn).
2. Quan sát phản hồi → trả về HTML `<h1>Database Error</h1>` lộ thông báo lỗi SQL.
3. Gọi payload boolean: `curl "http://localhost:3000/api/products?search=%25%27%20OR%20%271%27%3D%271"` (`%' OR '1'='1`) → trả về **toàn bộ** bảng products.

## Expected result

Query tham số hóa (prepared statement); input tìm kiếm được escape; không thể can thiệp cấu trúc SQL, không lộ thông báo lỗi DB ra client.

## Actual result

- `server.js:144`: `SELECT * FROM products WHERE name LIKE '%${searchQuery}%'` — nối trực tiếp query string vào câu SQL.
- `search='` gây lỗi cú pháp SQL và **lộ error HTML**; `%' OR '1'='1` bỏ qua điều kiện lọc, trả toàn bộ dữ liệu → lỗ hổng SQL Injection.

## Evidence

Output curl 2 payload ở trên (lỗi SQL + dump toàn bảng).
![BUG-02](https://res.cloudinary.com/dnqinxiwo/image/upload/v1786794396/eshop-hw05/perf-bugs/BUG-02.png)
