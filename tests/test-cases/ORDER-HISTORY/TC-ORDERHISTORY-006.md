# Test Case Template

## Test Case ID
TC-ORDERHISTORY-006

## Feature
Xem lịch sử đơn hàng (User)

## Requirement Reference
FR-11

## Testing Technique
Domain Testing / Boundary Value Analysis

## Test Objective
Kiểm tra hiển thị trạng thái "pending" (chờ xác nhận)

## Preconditions
Người dùng đã đăng nhập và có 1 đơn hàng vừa đặt thành công (trạng thái pending)

## Test Data
| Parameter | Value |
|-|-|
| Trạng thái | pending |

## Test Steps
1. Truy cập Lịch sử đơn hàng.
2. Tìm đơn hàng có trạng thái "pending".
3. Kiểm tra text và màu sắc của trạng thái.

## Expected Result
Trạng thái hiển thị là "Chờ xác nhận" (hoặc tương đương bằng tiếng Việt), có màu sắc nổi bật (VD: màu cam/vàng).

## Actual Result
(Chưa thực thi)

## Status
NOT EXECUTED

## Bug Reference
