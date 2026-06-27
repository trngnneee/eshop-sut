# Test Case Template

## Test Case ID
TC-ORDERHISTORY-010

## Feature
Xem lịch sử đơn hàng (User)

## Requirement Reference
FR-11

## Testing Technique
Domain Testing / Boundary Value Analysis

## Test Objective
Kiểm tra hiển thị trạng thái "canceled" (đã hủy)

## Preconditions
Người dùng có 1 đơn hàng đã bị hủy (trạng thái canceled)

## Test Data
| Parameter | Value |
|-|-|
| Trạng thái | canceled |

## Test Steps
1. Truy cập Lịch sử đơn hàng.
2. Tìm đơn hàng có trạng thái "canceled".
3. Kiểm tra text và màu sắc của trạng thái.

## Expected Result
Trạng thái hiển thị là "Đã hủy", có màu sắc cảnh báo.

## Actual Result
Trạng thái hiển thị tiếng việt chuẩn xác, có màu sắc phân biệt.

## Status
PASSED

## Bug Reference
None