# Test Case

## Test Case ID

TC-ORDER-016

## Feature

Trạng thái Đơn hàng (Order State Machine)

## Requirement Reference

FR-10

## Testing Technique

Decision Table Testing / Pair-wise Testing

## Decision Rule Reference

DT-25 | PW-16

## Test Objective

Kiểm tra hệ thống từ chối bất kỳ chuyển đổi nào từ trạng thái `delivered` (đây là final state — không thể thay đổi).

## Preconditions

- Tồn tại đơn hàng với trạng thái hiện tại là `delivered`
- Người dùng đã đăng nhập với vai trò Admin

## Test Data

| Parameter | Value |
|-----------|-------|
| Current State | delivered |
| Target State | confirmed |
| Role | Admin |
| JWT Token | Token hợp lệ với role=admin |

## Test Steps

1. Đăng nhập với tài khoản Admin
2. Truy cập phân hệ Admin > Quản lý Đơn hàng
3. Chọn đơn hàng đang ở trạng thái `delivered`
4. Cố gắng chuyển trạng thái sang `confirmed` (hoặc bất kỳ trạng thái nào khác)
5. Quan sát phản hồi của hệ thống

## Expected Result

- Hệ thống từ chối yêu cầu
- Trả về lỗi — đây là final state, không được phép thay đổi
- Trạng thái đơn hàng KHÔNG thay đổi — vẫn là `delivered`
- Thông báo lỗi phù hợp được hiển thị
- Không có nút chuyển đổi trạng thái trên giao diện cho đơn hàng `delivered`

## Actual Result

Hệ thống từ chối yêu cầu, trả về HTTP 400 và thông báo lỗi: `Invalid state transition from delivered to confirmed`. Trạng thái đơn hàng giữ nguyên là `delivered`.

## Status

PASS

## Risk Level

High

## Bug Reference

Không có.
