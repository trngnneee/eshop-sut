# Test Case

## Test Case ID

TC-ORDER-014

## Feature

Trạng thái Đơn hàng (Order State Machine)

## Requirement Reference

FR-10

## Testing Technique

Decision Table Testing / Pair-wise Testing

## Decision Rule Reference

DT-20 | PW-14

## Test Objective

Kiểm tra User thông thường KHÔNG thể tự hủy đơn hàng khi đơn đang ở trạng thái `shipping` (vi phạm business rule quan trọng nhất của FR-10).

## Preconditions

- Tồn tại đơn hàng với trạng thái hiện tại là `shipping` (thuộc về user đang đăng nhập)
- Người dùng đã đăng nhập với vai trò User thông thường

## Test Data

| Parameter | Value |
|-----------|-------|
| Current State | shipping |
| Target State | canceled |
| Role | User |
| JWT Token | Token hợp lệ với role=user |

## Test Steps

1. Đăng nhập với tài khoản User
2. Truy cập lịch sử đơn hàng
3. Chọn đơn hàng đang ở trạng thái `shipping`
4. Cố gắng thực hiện thao tác hủy đơn hàng
5. Quan sát phản hồi của hệ thống

## Expected Result

- Hệ thống từ chối yêu cầu
- Trạng thái đơn hàng KHÔNG thay đổi — vẫn là `shipping`
- Hệ thống trả về mã lỗi chuyển đổi không hợp lệ (HTTP 400)

## Actual Result

Hệ thống chấp nhận yêu cầu, trả về HTTP 200 và cập nhật trạng thái đơn hàng sang `canceled` thành công. User thường vẫn có thể tự hủy đơn hàng đang ở trạng thái `shipping` thông qua API cancel thông thường (`/api/orders/:id/cancel`).

## Status

FAIL

## Risk Level

Low

## Bug Reference

[BUG][Order State Machine] Khách hàng có thể tự hủy đơn hàng khi đã chuyển sang trạng thái shipping (User Can Cancel Shipping Order)
