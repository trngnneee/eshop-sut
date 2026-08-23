---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Admin / Product Import] Không kiểm tra FK constraint category_id'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-C-DP-11

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
4. Truyền request body chứa sản phẩm có `category_id` không tồn tại trong database (ví dụ: `9999`):
   `{"products":[{"name":"SP1","price":10000,"description":"Mo ta","imageUrl":"","category_id":9999}]}`.

## Expected result

API từ chối request với mã trạng thái HTTP `400 Bad Request` do vi phạm ràng buộc toàn vẹn khóa ngoại (Foreign Key constraint category_id không tồn tại trong bảng categories).

## Actual result

API phản hồi mã trạng thái HTTP `200 OK` và lưu trữ bản ghi sản phẩm mồ côi (orphaned record) với category_id không có thực.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api3_report.html`
- Failed Test Case: `TC-C-DP-11`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/485](https://github.com/trngnneee/eshop-sut/issues/485) (#485)
