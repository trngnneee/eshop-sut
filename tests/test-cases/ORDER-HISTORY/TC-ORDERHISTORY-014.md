## Test Case ID

TC-ORDERHISTORY-014

## Feature

Xem chi tiết đơn hàng

## Requirement Reference

FR-11

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra người dùng chưa đăng nhập không thể truy cập chi tiết đơn hàng.

## Preconditions

* Người dùng chưa đăng nhập vào hệ thống.
* Có Order ID hợp lệ trong hệ thống.

## Test Data

| Parameter | Value |
| ------------------- | ---------------- |
| Authorization Token | Không có |
| Order ID | Order ID hợp lệ |

## Test Steps

1. Không đăng nhập vào hệ thống.
2. Gửi request:

```http
GET /api/orders/{{ORDER_ID}}
````

3. Kiểm tra response.

## Expected Result

* API yêu cầu xác thực người dùng trước khi truy cập dữ liệu đơn hàng.
* Trả về lỗi:

```http
401 Unauthorized
```

* Không trả về thông tin chi tiết đơn hàng.

## Actual Result

API vẫn trả về thông tin chi tiết đơn hàng mặc dù request không có Authorization Token.

## Status

FAILED

## Bug Reference
[[BUG][Order History] API xem chi tiết đơn hàng không yêu cầu xác thực người dùng](https://github.com/trngnneee/eshop-sut/issues/65#issue-4758951568)


