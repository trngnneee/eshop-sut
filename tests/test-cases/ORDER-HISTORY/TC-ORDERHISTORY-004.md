# Test Case Template

## Test Case ID
TC-ORDERHISTORY-004

## Feature
Xem lịch sử đơn hàng (User)

## Requirement Reference
FR-11

## Testing Technique
Domain Testing / Boundary Value Analysis

## Test Objective
Kiểm tra người dùng không thể xem đơn hàng của người khác

## Preconditions
Người dùng A đã đăng nhập, người dùng B có 1 đơn hàng

## Test Data
| Parameter | Value |
|-|-|
| ID người dùng | User A |
| Đơn hàng của | User B |

## Test Steps
1. Đăng nhập bằng tài khoản User A.
2. Truy cập trang Lịch sử đơn hàng.
3. Nếu có API hoặc URL chi tiết đơn hàng của User B, thử truy cập trực tiếp bằng ID đơn hàng của B.

## Expected Result
Ở bước 2, chỉ hiển thị đơn hàng của User A. Ở bước 3, hệ thống trả về lỗi 403 Forbidden hoặc không tìm thấy (404).

## Actual Result
(Chưa thực thi)

## Status
NOT EXECUTED

## Bug Reference
