# Test Case

## Test Case ID

TC-ORDER-017

## Feature

Trạng thái Đơn hàng (Order State Machine)

## Requirement Reference

FR-10

## Testing Technique

Decision Table Testing / Pair-wise Testing

## Decision Rule Reference

DT-26 | PW-17

## Test Objective

Kiểm tra User thông thường cũng không thể thực hiện bất kỳ chuyển đổi nào từ trạng thái `delivered` (final state).

## Preconditions

- Tồn tại đơn hàng với trạng thái hiện tại là `delivered` (thuộc về user đang đăng nhập)
- Người dùng đã đăng nhập với vai trò User thông thường

## Test Data

| Parameter | Value |
|-----------|-------|
| Current State | delivered |
| Target State | shipping |
| Role | User |
| JWT Token | Token hợp lệ với role=user |

## Test Steps

1. Đăng nhập với tài khoản User
2. Truy cập lịch sử đơn hàng
3. Chọn đơn hàng đang ở trạng thái `delivered`
4. Cố gắng thực hiện bất kỳ thao tác thay đổi trạng thái nào

## Expected Result

- Hệ thống từ chối yêu cầu
- Trạng thái đơn hàng KHÔNG thay đổi — vẫn là `delivered`
- Không có tùy chọn thay đổi trạng thái trên giao diện (nút hủy bị ẩn/vô hiệu hóa)

## Actual Result

Hệ thống từ chối yêu cầu, trả về HTTP 400. Trạng thái đơn hàng giữ nguyên là `delivered`.

## Status

PASS

## Risk Level

Low

## Bug Reference

Không có.
