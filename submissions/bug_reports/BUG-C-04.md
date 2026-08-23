---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Admin / Product Import] RBAC không được áp dụng cho import endpoint'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-C-ST-04, TC-C-SEC-02

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

1. Đăng nhập tài khoản người dùng thông thường (`role: "user"`) để lấy Bearer token.
2. Gửi request `POST` đến endpoint quản trị `http://localhost:3000/api/admin/import-products`.
3. Thiết lập header: `Authorization: Bearer <user_token>`, `Content-Type: application/json`, `X-Student-Id: 23127486`.
4. Truyền request body chứa danh sách sản phẩm hợp lệ:
   `{"products":[{"name":"SP Hack By User","price":50000,"description":"Hack","imageUrl":"","category_id":1}]}`.

## Expected result

Hệ thống phải kiểm tra quyền hạn (Role-Based Access Control - RBAC) và từ chối request của người dùng không có role admin bằng mã trạng thái HTTP `403 Forbidden`.

## Actual result

Hệ thống không kiểm tra role admin cho endpoint này, trả về mã trạng thái HTTP `200 OK` và cho phép user thường import thành công sản phẩm vào catalog hệ thống (lỗ hổng bảo mật nghiêm trọng Broken Access Control / Privilege Escalation).

## Evidence

- File Newman HTML Report: `newman_reports/newman_api3_report.html`
- Failed Test Cases: `TC-C-ST-04`, `TC-C-SEC-02`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/486](https://github.com/trngnneee/eshop-sut/issues/486) (#486)
