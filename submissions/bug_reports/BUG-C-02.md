---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Admin / Product Import] Chấp nhận giá âm và kiểu dữ liệu sai cho price'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-C-DP-08, TC-C-DP-09

## Requirement liên quan

FR-16 (Import sản phẩm từ JSON - Admin)

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows 11 / Ubuntu 22.04 LTS (CI)
- **Browser**: N/A (API Testing via Newman 6.2.2 / Postman Runtime)
- **URL**: http://localhost:3000/api/admin/import-products
- **Build/Commit**: 26c42a637081edec1344b40665812c4ee7357160

## Steps to reproduce

1. Đăng nhập tài khoản admin để lấy Bearer token hợp lệ.
2. Gửi request `POST` đến `http://localhost:3000/api/admin/import-products`.
3. Thiết lập header: `Authorization: Bearer <admin_token>`, `Content-Type: application/json`, `X-Student-Id: 23127486`.
4. Truyền request body chứa sản phẩm có `price` là số âm hoặc `price` là kiểu chuỗi string:
   - Price âm: `{"products":[{"name":"SP Gia Am","price":-1,"description":"Mo ta","imageUrl":"","category_id":1}]}`
   - Price kiểu chuỗi: `{"products":[{"name":"SP Gia Chuoi","price":"10000","description":"Mo ta","imageUrl":"","category_id":1}]}`

## Expected result

API từ chối request với mã trạng thái HTTP `400 Bad Request` và thông báo lỗi giá tiền `price` phải là số không âm (number >= 0) và đúng kiểu dữ liệu number.

## Actual result

API phản hồi mã trạng thái HTTP `200 OK` và lưu thành công sản phẩm có giá âm hoặc chuỗi vào cơ sở dữ liệu.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api3_report.html`
- Failed Test Cases: `TC-C-DP-08`, `TC-C-DP-09`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/484](https://github.com/trngnneee/eshop-sut/issues/484) (#484)
