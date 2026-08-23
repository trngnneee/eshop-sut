---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Admin / Product Import] Xử lý sai mã lỗi (403 vs 401) khi admin token forged / expired'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-C-ST-06, TC-C-SEC-06, TC-C-SEC-07

## Requirement liên quan

FR-16 (Import sản phẩm từ JSON - Admin)

## Severity / Priority

Major / P2

## Environment

- **OS**: Windows 11 / Ubuntu 22.04 LTS (CI)
- **Browser**: N/A (API Testing via Newman 6.2.2 / Postman Runtime)
- **URL**: http://localhost:3000/api/admin/import-products
- **Build/Commit**: 26c42a637081edec1344b40665812c4ee7357160

## Steps to reproduce

1. Gửi request `POST` đến `http://localhost:3000/api/admin/import-products`.
2. Truyền header xác thực không hợp lệ:
   - Token giả mạo: `Authorization: Bearer eyJ...forged_token...`
   - Token hết hạn: `Authorization: Bearer <expired_token>`
3. Thiết lập header: `Content-Type: application/json` và `X-Student-Id: 23127486`.
4. Truyền request body hợp lệ: `{"products":[{"name":"SP1","price":10000,"description":"Mo ta","imageUrl":"","category_id":1}]}`.

## Expected result

Theo chuẩn REST API, khi xác thực token thất bại (chữ ký sai hoặc token hết hạn), server phải trả về mã trạng thái HTTP `401 Unauthorized`.

## Actual result

Server trả về mã trạng thái HTTP `403 Forbidden` thay vì `401 Unauthorized`.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api3_report.html`
- Failed Test Cases: `TC-C-ST-06`, `TC-C-SEC-06`, `TC-C-SEC-07`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/487](https://github.com/trngnneee/eshop-sut/issues/487) (#487)
