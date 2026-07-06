## BUG-FR09-P-01 - Công thức giảm giá percent tính sai `discount_amount`

**GitHub issue title:** `[BUG][FR-09][Coupon] Công thức giảm giá percent tính sai discount_amount`

**GitHub issue:** TBD

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `FR09-P-TC01`
- Path: `eshop-sut/tests/test-cases/coupon_application/FR09-P-TC01.md`

## Requirement liên quan

- `FR-09`
- Công thức loại `percent`: `discount_amount = total x discount_value / 100`.
- `final_amount = total - discount_amount`.
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
2. Đăng nhập bằng `test@eshop.com` / `Test1234!`.
3. Gửi request `POST /api/apply-coupon` với body `{"code":"SAVE10","total_amount":500000,"user_id":2}`.
4. Kiểm tra `discount_amount` và `final_amount` trong response.

## Expected result

- API trả HTTP 200.
- `discount_amount = 50000`.
- `final_amount = 450000`.

## Actual result

- API trả HTTP 200.
- `discount_amount = -4500000`.
- `final_amount = 5000000`.

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
- Implementation hiện tính `discount_amount` bằng `total_amount * (1 - coupon.discount_value)` cho coupon `percent`, thay vì `total_amount * coupon.discount_value / 100`.
