# Test Case Template

## Test Case ID
TC-ORDERHISTORY-007

## Feature
Xem lịch sử đơn hàng (User)

## Requirement Reference
FR-11

## Testing Technique
Domain Testing / Boundary Value Analysis

## Test Objective
Kiểm tra hiển thị trạng thái "confirmed" (đã xác nhận)

## Preconditions
Người dùng có 1 đơn hàng đã được Admin xác nhận (trạng thái confirmed)

## Test Data
| Parameter | Value |
|-|-|
| Trạng thái | confirmed |

## Test Steps
1. Truy cập Lịch sử đơn hàng.
2. Tìm đơn hàng có trạng thái "confirmed".
3. Kiểm tra text và màu sắc của trạng thái.

## Expected Result
Trạng thái hiển thị là "Đã xác nhận", có màu sắc phân biệt (VD: màu xanh dương).

## Actual Result
Trạng thái hiển thị tiếng việt chuẩn xác, có màu sắc phân biệt.

## Status
PASSED

## Bug Reference
None