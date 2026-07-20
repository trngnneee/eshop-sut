# Test Case

## Test Case ID

TC-ORDER-003

## Feature

Trạng thái Đơn hàng (Order State Machine)

## Requirement Reference

FR-10

## Testing Technique

Decision Table Testing / Pair-wise Testing

## Decision Rule Reference

DT-03 | PW-03

## Test Objective

Kiểm tra Admin có thể hủy đơn hàng đang ở trạng thái `pending`.

## Preconditions

- Tồn tại đơn hàng với trạng thái hiện tại là `pending`
- Người dùng đã đăng nhập với vai trò Admin

## Test Data

| Parameter | Value |
|-----------|-------|
| Current State | pending |
| Target State | canceled |
| Role | Admin |
| JWT Token | Token hợp lệ với role=admin |

## Test Steps

1. Đăng nhập với tài khoản Admin
2. Truy cập phân hệ Admin > Quản lý Đơn hàng
3. Chọn đơn hàng đang ở trạng thái `pending`
4. Thực hiện thao tác hủy đơn hàng (chuyển sang `canceled`)
5. Xác nhận hành động

## Expected Result

- Hệ thống chấp nhận yêu cầu
- Trạng thái đơn hàng được cập nhật thành `canceled`
- Trạng thái `canceled` là final state — không thể chuyển tiếp nữa

## Actual Result

Hệ thống chấp nhận yêu cầu, cập nhật thành công trạng thái đơn hàng sang `canceled` và trả về mã HTTP 200.

## Status

PASS

## Risk Level

Medium

## Bug Reference

Không có.
