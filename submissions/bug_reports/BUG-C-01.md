---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Admin / Product Import] Không validate required fields trong product'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-C-DP-04, TC-C-DP-05, TC-C-DP-06, TC-C-DP-10

## Requirement liên quan

FR-16 (Import sản phẩm từ JSON - Admin)

## Severity / Priority

Critical / P0

## Environment

- **OS**: Windows 11 / Ubuntu 22.04 LTS (CI)
- **Browser**: N/A (API Testing via Newman 6.2.2 / Postman Runtime)
- **URL**: http://localhost:3000/api/admin/import-products
- **Build/Commit**: 26c42a637081edec1344b40665812c4ee7357160

## Steps to reproduce

1. Đăng nhập tài khoản admin để lấy Bearer token hợp lệ.
2. Gửi request `POST` đến `http://localhost:3000/api/admin/import-products`.
3. Thiết lập header: `Authorization: Bearer <admin_token>`, `Content-Type: application/json`, `X-Student-Id: 23127486`.
4. Truyền request body chứa các sản phẩm thiếu trường bắt buộc hoặc có giá trị rỗng:
   - Thiếu `name`: `{"products":[{"price":10000,"description":"Mo ta","imageUrl":"","category_id":1}]}`
   - `name` rỗng: `{"products":[{"name":"","price":10000,"description":"Mo ta","imageUrl":"","category_id":1}]}`
   - Thiếu `price`: `{"products":[{"name":"SP1","description":"Mo ta","imageUrl":"","category_id":1}]}`
   - Thiếu `category_id`: `{"products":[{"name":"SP1","price":10000,"description":"Mo ta","imageUrl":""}]}`

## Expected result

API từ chối request với mã trạng thái HTTP `400 Bad Request` cùng thông báo lỗi validation chi tiết về các trường bắt buộc (`name`, `price`, `category_id`) bị thiếu hoặc không hợp lệ.

## Actual result

API phản hồi mã trạng thái HTTP `200 OK` và lưu trữ các sản phẩm thiếu thông tin / mang giá trị `null` vào cơ sở dữ liệu.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api3_report.html`
- Failed Test Cases: `TC-C-DP-04`, `TC-C-DP-05`, `TC-C-DP-06`, `TC-C-DP-10`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/483](https://github.com/trngnneee/eshop-sut/issues/483) (#483)
