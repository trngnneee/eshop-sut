# Test Case

## Test Case ID

TC-ORDER-005

## Feature

Trạng thái Đơn hàng (Order State Machine)

## Requirement Reference

FR-10

## Testing Technique

Decision Table Testing / Pair-wise Testing

## Decision Rule Reference

DT-05 | PW-05

## Test Objective

Kiểm tra hệ thống từ chối chuyển đổi không hợp lệ từ `pending` trực tiếp sang `shipping` (bỏ qua bước `confirmed`).

## Preconditions

- Tồn tại đơn hàng với trạng thái hiện tại là `pending`
- Người dùng đã đăng nhập với vai trò Admin

## Test Data

| Parameter | Value |
|-----------|-------|
| Current State | pending |
| Target State | shipping |
| Role | Admin |
| JWT Token | Token hợp lệ với role=admin |

## Test Steps

1. Đăng nhập với tài khoản Admin
2. Truy cập phân hệ Admin > Quản lý Đơn hàng
3. Chọn đơn hàng đang ở trạng thái `pending`
4. Cố gắng chuyển trạng thái sang `shipping` (bỏ qua bước `confirmed`)
5. Quan sát phản hồi của hệ thống

## Expected Result

- Hệ thống từ chối yêu cầu
- Trả về lỗi chuyển đổi không hợp lệ
- Trạng thái đơn hàng KHÔNG thay đổi — vẫn là `pending`
- Thông báo lỗi phù hợp được hiển thị

## Actual Result

Hệ thống từ chối yêu cầu, trả về HTTP 400 và thông báo lỗi: `Invalid state transition from pending to shipping`. Trạng thái đơn hàng giữ nguyên là `pending`.

## Status

PASS

## Risk Level

Low

## Bug Reference

Không có.
