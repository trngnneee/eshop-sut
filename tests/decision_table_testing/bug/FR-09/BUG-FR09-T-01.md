## BUG-FR09-T-01 - Hệ thống từ chối đơn hàng bằng đúng ngưỡng tối thiểu

**GitHub issue title:** `[BUG][FR-09][Coupon] Không áp dụng coupon khi total_amount bằng min_order_amount`

**GitHub issue:** TBD

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `FR09-T-TC01`
- `FR09-T-TC03`
- Paths:
  - `eshop-sut/tests/test-cases/coupon_application/FR09-T-TC01.md`
  - `eshop-sut/tests/test-cases/coupon_application/FR09-T-TC03.md`

## Requirement liên quan

- `FR-09`
- Điều kiện C3: Tổng đơn hàng phải `>= min_order_amount`.
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
3. Gửi request `POST /api/apply-coupon` với body `{"code":"SAVE10","total_amount":300000,"user_id":2}`.
4. Gửi request `POST /api/apply-coupon` với body `{"code":"BIGBUY","total_amount":500000,"user_id":2}`.
5. Kiểm tra response tại điều kiện `total_amount = min_order_amount`.

## Expected result

- Cả hai request được chấp nhận vì FR-09 yêu cầu `total_amount >= min_order_amount`.
- `SAVE10` với `300000` được áp dụng.
- `BIGBUY` với `500000` được áp dụng.

## Actual result

- Request `SAVE10` trả HTTP 400: `Đơn hàng chưa đủ giá trị tối thiểu 300,000 ₫ để áp dụng mã này`.
- Request `BIGBUY` trả HTTP 400: `Đơn hàng chưa đủ giá trị tối thiểu 500,000 ₫ để áp dụng mã này`.

## Evidence

```json
[
  {
    "test_case": "FR09-T-TC01",
    "status": 400,
    "body": {
      "error": "Đơn hàng chưa đủ giá trị tối thiểu 300,000 ₫ để áp dụng mã này"
    }
  },
  {
    "test_case": "FR09-T-TC03",
    "status": 400,
    "body": {
      "error": "Đơn hàng chưa đủ giá trị tối thiểu 500,000 ₫ để áp dụng mã này"
    }
  }
]
```

## Technical note

- Code path: `eshop-sut/backend/server.js`
- Implementation hiện kiểm tra `total_amount > coupon.min_order_amount`, trong khi requirement cần `total_amount >= coupon.min_order_amount`.
