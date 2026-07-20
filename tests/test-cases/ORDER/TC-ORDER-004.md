# Test Case

## Test Case ID

TC-ORDER-004

## Feature

Trạng thái Đơn hàng (Order State Machine)

## Requirement Reference

FR-10

## Testing Technique

Decision Table Testing / Pair-wise Testing

## Decision Rule Reference

DT-04 | PW-04

## Test Objective

Kiểm tra User thông thường có thể tự hủy đơn hàng của mình khi đang ở trạng thái `pending`.

## Preconditions

- Tồn tại đơn hàng với trạng thái hiện tại là `pending` (thuộc về user đang đăng nhập)
- Người dùng đã đăng nhập với vai trò User thông thường

## Test Data

| Parameter | Value |
|-----------|-------|
| Current State | pending |
| Target State | canceled |
| Role | User |
| JWT Token | Token hợp lệ với role=user |

## Test Steps

1. Đăng nhập với tài khoản User
2. Truy cập lịch sử đơn hàng
3. Chọn đơn hàng đang ở trạng thái `pending`
4. Thực hiện thao tác hủy đơn hàng
5. Xác nhận hành động hủy

## Expected Result

- Hệ thống chấp nhận yêu cầu
- Trạng thái đơn hàng được cập nhật thành `canceled`
- Giao diện hiển thị trạng thái mới là `canceled` (tiếng Việt: Đã hủy)

## Actual Result

Hệ thống chấp nhận yêu cầu, cập nhật thành công trạng thái đơn hàng sang `canceled` và trả về mã HTTP 200.

## Status

PASS

## Risk Level

Medium

## Bug Reference

Không có.
