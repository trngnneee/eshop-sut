# Test Case

## Test Case ID

TC-ORDER-013

## Feature

Trạng thái Đơn hàng (Order State Machine)

## Requirement Reference

FR-10

## Testing Technique

Decision Table Testing / Pair-wise Testing

## Decision Rule Reference

DT-19 | PW-13

## Test Objective

Kiểm tra hệ thống từ chối yêu cầu chuyển đổi trạng thái từ `shipping` sang `canceled` đối với Admin (vì đây là chuyển đổi không hợp lệ).

## Preconditions

- Tồn tại đơn hàng với trạng thái hiện tại là `shipping`
- Người dùng đã đăng nhập với vai trò Admin

## Test Data

| Parameter | Value |
|-----------|-------|
| Current State | shipping |
| Target State | canceled |
| Role | Admin |
| JWT Token | Token hợp lệ với role=admin |

## Test Steps

1. Đăng nhập với tài khoản Admin
2. Truy cập phân hệ Admin > Quản lý Đơn hàng
3. Chọn đơn hàng đang ở trạng thái `shipping`
4. Cố gắng thực hiện thao tác chuyển đổi trạng thái sang `canceled`
5. Quan sát phản hồi của hệ thống

## Expected Result

- Hệ thống từ chối yêu cầu
- Trạng thái đơn hàng KHÔNG thay đổi — vẫn là `shipping`
- Hệ thống trả về mã lỗi chuyển đổi không hợp lệ (HTTP 400)

## Actual Result

Hệ thống từ chối yêu cầu, trả về HTTP 400 với thông báo lỗi: `Invalid state transition from shipping to canceled`. Trạng thái đơn hàng giữ nguyên là `shipping`.

## Status

PASS

## Risk Level

Low

## Bug Reference

Không có.
