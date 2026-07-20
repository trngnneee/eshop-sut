# Test Case

## Test Case ID

TC-ORDER-001

## Feature

Trạng thái Đơn hàng (Order State Machine)

## Requirement Reference

FR-10

## Testing Technique

Decision Table Testing / Pair-wise Testing

## Decision Rule Reference

DT-01 | PW-01

## Test Objective

Kiểm tra Admin có thể chuyển đơn hàng từ trạng thái `pending` sang `confirmed`.

## Preconditions

- Tồn tại đơn hàng với trạng thái hiện tại là `pending`
- Người dùng đã đăng nhập với vai trò Admin
- JWT Token hợp lệ với `role = 'admin'`

## Test Data

| Parameter | Value |
|-----------|-------|
| Current State | pending |
| Target State | confirmed |
| Role | Admin |
| JWT Token | Token hợp lệ với role=admin |

## Test Steps

1. Đăng nhập vào hệ thống với tài khoản Admin (`admin@eshop.com` / `Admin123!`)
2. Truy cập danh sách đơn hàng trong phân hệ Admin
3. Chọn một đơn hàng đang ở trạng thái `pending`
4. Thực hiện thao tác chuyển trạng thái sang `confirmed`
5. Xác nhận hành động

## Expected Result

- Hệ thống chấp nhận yêu cầu
- Trạng thái đơn hàng được cập nhật thành `confirmed`
- Giao diện hiển thị trạng thái mới là `confirmed`
- Hệ thống trả về thành công (HTTP 200)

## Actual Result

Hệ thống chấp nhận yêu cầu. Trạng thái đơn hàng được cập nhật thành `confirmed`. Giao diện hiển thị trạng thái mới là `confirmed`. Hệ thống trả về thành công (HTTP 200).

## Status

PASS

## Risk Level

High

## Bug Reference
