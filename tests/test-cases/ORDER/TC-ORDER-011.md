# Test Case

## Test Case ID

TC-ORDER-011

## Feature

Trạng thái Đơn hàng (Order State Machine)

## Requirement Reference

FR-10

## Testing Technique

Decision Table Testing / Pair-wise Testing

## Decision Rule Reference

DT-17 | PW-11

## Test Objective

Kiểm tra Admin có thể chuyển đơn hàng từ trạng thái `shipping` sang `delivered` (hoàn tất đơn hàng).

## Preconditions

- Tồn tại đơn hàng với trạng thái hiện tại là `shipping`
- Người dùng đã đăng nhập với vai trò Admin

## Test Data

| Parameter | Value |
|-----------|-------|
| Current State | shipping |
| Target State | delivered |
| Role | Admin |
| JWT Token | Token hợp lệ với role=admin |

## Test Steps

1. Đăng nhập với tài khoản Admin
2. Truy cập phân hệ Admin > Quản lý Đơn hàng
3. Chọn đơn hàng đang ở trạng thái `shipping`
4. Thực hiện thao tác chuyển trạng thái sang `delivered`
5. Xác nhận hành động

## Expected Result

- Hệ thống chấp nhận yêu cầu
- Trạng thái đơn hàng được cập nhật thành `delivered`
- Giao diện hiển thị trạng thái mới là `delivered`
- Hệ thống trả về thành công (HTTP 200)
- Đơn hàng này sẽ được tính vào doanh thu trong Dashboard (FR-13)

## Actual Result

Hệ thống chấp nhận yêu cầu, cập nhật thành công trạng thái đơn hàng sang `delivered` và trả về mã HTTP 200.

## Status

PASS

## Risk Level

High

## Bug Reference

Không có.
