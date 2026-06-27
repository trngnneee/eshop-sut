## Test Case ID

TC-ORDERHISTORY-012

## Feature

Xem lịch sử đơn hàng (User)

## Requirement Reference

FR-11

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra người dùng chưa đăng nhập không thể lấy lịch sử đơn hàng.

## Preconditions

* Người dùng chưa đăng nhập vào hệ thống.

## Test Data

| Parameter           | Value    |
| ------------------- | -------- |
| Authorization Token | Không có |

## Test Steps

1. Gửi request:

```http
GET /api/orders/my-orders
```

2. Không truyền header Authorization.

## Expected Result

* API từ chối truy cập.
* Trả về:

```http
401 Unauthorized
```

* Không trả dữ liệu đơn hàng.

## Actual Result

API trả lỗi 401 Unauthorized.

## Status

PASSED

## Bug Reference

None