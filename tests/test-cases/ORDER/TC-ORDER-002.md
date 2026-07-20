# Test Case

## Test Case ID

TC-ORDER-002

## Feature

Trạng thái Đơn hàng (Order State Machine)

## Requirement Reference

FR-10

## Testing Technique

Decision Table Testing / Pair-wise Testing

## Decision Rule Reference

DT-02 | PW-02

## Test Objective

Kiểm tra User thông thường KHÔNG thể chuyển đơn hàng từ `pending` sang `confirmed` (chỉ Admin mới có quyền).

## Preconditions

- Tồn tại đơn hàng với trạng thái hiện tại là `pending` (thuộc về user đang đăng nhập)
- Người dùng đã đăng nhập với vai trò User thông thường
- JWT Token hợp lệ với `role = 'user'`

## Test Data

| Parameter | Value |
|-----------|-------|
| Current State | pending |
| Target State | confirmed |
| Role | User |
| JWT Token | Token hợp lệ với role=user |

## Test Steps

1. Đăng nhập vào hệ thống với tài khoản User (`test@eshop.com` / `Test1234!`)
2. Truy cập lịch sử đơn hàng của chính mình
3. Chọn một đơn hàng đang ở trạng thái `pending`
4. Cố gắng thực hiện thao tác chuyển trạng thái sang `confirmed` (qua API hoặc giao diện nếu có)

## Expected Result

- Hệ thống từ chối yêu cầu
- Trả về lỗi phân quyền (HTTP 403 Forbidden)
- Trạng thái đơn hàng KHÔNG thay đổi — vẫn là `pending`
- Thông báo lỗi phù hợp được hiển thị

## Actual Result

Hệ thống KHÔNG từ chối yêu cầu, trả về HTTP 200 và cập nhật trạng thái đơn hàng sang `confirmed` thành công mặc dù người dùng chỉ có vai trò `user`. Đây là lỗi bỏ qua kiểm tra quyền hạn (Authorization Bypass).

## Status

FAIL

## Risk Level

High

## Bug Reference

[BUG][Order State Machine] API cập nhật trạng thái đơn hàng của Admin không kiểm tra quyền truy cập theo vai trò (Role-based Authorization Bypass)