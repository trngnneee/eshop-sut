## BUG-FR09-A-01 - API áp dụng coupon không yêu cầu JWT hợp lệ

**GitHub issue title:** `[BUG][FR-09][Coupon][Security] Apply coupon không yêu cầu JWT hợp lệ`

**GitHub issue:** TBD

**Labels:** `type: bug`, `status: new`, `found-by: test-case`, `security`

## Found by Test Case

- `FR09-A-TC01`
- Path: `eshop-sut/tests/test-cases/coupon_application/FR09-A-TC01.md`

## Requirement liên quan

- `FR-09`
- Điều kiện C4: Người dùng phải có JWT Token hợp lệ.
- Source: `eshop-sut/README.md`
- Source: `eshop-sut/api_specification.md`

## Severity / Priority

High / P1

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser/Runtime**: API test via Node fetch
- **URL**: `http://localhost:3000/api/apply-coupon`
- **Build/Commit**: Latest local checkout

## Steps to reproduce

1. Chạy backend API tại `http://localhost:3000`.
2. Không gửi header `Authorization`.
3. Gửi request `POST /api/apply-coupon` với body `{"code":"SAVE10","total_amount":500000,"user_id":null}`.
4. Kiểm tra response.

## Expected result

- API trả HTTP 401 hoặc 403.
- Coupon không được áp dụng khi request không có JWT hợp lệ.
- Response không chứa `discount_amount`/`final_amount` thành công.

## Actual result

- API trả HTTP 200.
- Coupon được áp dụng thành công dù không có `Authorization` header.
- Response chứa `discount_amount` và `final_amount`.

## Evidence

```json
{
  "status": 200,
  "body": {
    "success": true,
    "coupon_id": 1,
    "discount_amount": -4500000,
    "final_amount": 5000000,
    "message": "Áp dụng thành công! Giảm 10%"
  }
}
```

## Technical note

- Code path: `eshop-sut/backend/server.js`
- Route `POST /api/apply-coupon` không dùng middleware `authenticateToken` và chấp nhận `user_id` từ body/null.
