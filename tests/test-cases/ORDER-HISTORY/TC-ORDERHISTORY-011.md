## Test Case ID

TC-ORDERHISTORY-011

## Feature

Xem lịch sử đơn hàng (User)

## Requirement Reference

FR-11

## Testing Technique

Boundary Value Analysis

## Test Objective

Kiểm tra hệ thống hỗ trợ hiển thị nhiều đơn hàng bằng cơ chế phân trang khi số lượng lịch sử đơn hàng lớn.

## Preconditions

* Người dùng đã đăng nhập.
* Người dùng có nhiều hơn số lượng đơn hàng tối đa trên một trang.
* API hỗ trợ tham số phân trang (page, limit).

## Test Data

| Parameter         | Value |
| ----------------- | ----- |
| Số lượng đơn hàng | 50    |
| Page              | 1     |
| Limit             | 10    |

## Test Steps

1. Đăng nhập bằng tài khoản có nhiều đơn hàng.
2. Gọi API:
```http
GET /api/orders/my-orders?page=1&limit=10
```
3. Kiểm tra dữ liệu trả về.
4. Gọi tiếp:

```http
GET /api/orders/my-orders?page=2&limit=10
```

## Expected Result

* Trang 1 chỉ trả về tối đa 10 đơn hàng.
* Trang 2 trả về các đơn hàng tiếp theo.
* Không bị trùng lặp hoặc mất dữ liệu giữa các trang.
* API trả thông tin phân trang nếu có (total, currentPage, totalPages).

## Actual Result
Hệ thống trả về toàn bộ đơn hàng, không có phân trang

## Status

FAILED

## Bug Reference
[BUG-FR11-01](https://github.com/trngnneee/eshop-sut/issues/64#issue-4758846657)


