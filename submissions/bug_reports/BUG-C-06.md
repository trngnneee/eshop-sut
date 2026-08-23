---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Admin / Product Import] Chấp nhận mảng products chứa phần tử không phải object'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-C-EXT-04

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
4. Truyền request body chứa mảng `products` với các phần tử là kiểu nguyên thủy (số hoặc chuỗi) thay vì JSON object:
   `{"products": [123, "invalid_item"]}`.

## Expected result

API từ chối request với mã trạng thái HTTP `400 Bad Request` do từng phần tử trong mảng `products` phải là JSON object đại diện cho một sản phẩm hợp lệ.

## Actual result

API phản hồi mã trạng thái HTTP `200 OK`, chấp nhận mảng chứa các phần tử không phải object.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api3_report.html`
- Failed Test Case: `TC-C-EXT-04`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/488](https://github.com/trngnneee/eshop-sut/issues/488) (#488)
