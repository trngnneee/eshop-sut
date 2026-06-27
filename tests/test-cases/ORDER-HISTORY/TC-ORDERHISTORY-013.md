# Test Case Template

## Test Case ID

TC-ORDERHISTORY-013

## Feature

Xem lịch sử đơn hàng (User)

## Requirement Reference

FR-11

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra người dùng chỉ nhận được lịch sử đơn hàng của chính mình.

## Preconditions

* User A đã đăng nhập.
* User A có ít nhất một đơn hàng.
* User B có ít nhất một đơn hàng.

## Test Data

| Parameter           | Value                     |
| ------------------- | ------------------------- |
| Authorization Token | User A                    |
| API Endpoint        | GET /api/orders/my-orders |

## Test Steps

1. Đăng nhập bằng User A.
2. Gửi request:

```http
GET /api/orders/my-orders
```

3. Kiểm tra danh sách đơn hàng trả về.

## Expected Result

* Response chỉ chứa các đơn hàng của User A.
* Không chứa đơn hàng của User B.

## Actual Result

Response trả về chỉ chứa các đơn hàng của User A

## Status

PASSED

## Bug Reference

None