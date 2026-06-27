# Test Case Template

## Test Case ID
TC-ORDERHISTORY-002

## Feature
Xem lịch sử đơn hàng (User)

## Requirement Reference
FR-11

## Testing Technique
Domain Testing / Boundary Value Analysis

## Test Objective
Kiểm tra hiển thị khi người dùng không có đơn hàng nào (BVA: 0 đơn hàng)

## Preconditions
Người dùng đã đăng nhập, tài khoản chưa từng đặt hàng

## Test Data
| Parameter | Value |
|-|-|
| Số lượng đơn hàng | 0 |

## Test Steps
1. Đăng nhập vào hệ thống với tài khoản hợp lệ.
2. Điều hướng đến trang Lịch sử đơn hàng.

## Expected Result
Giao diện hiển thị thông báo "Chưa có đơn hàng nào" (Empty state) kèm theo icon minh họa và nút "Tiếp tục mua sắm".

## Actual Result
(Chưa thực thi)

## Status
NOT EXECUTED

## Bug Reference
