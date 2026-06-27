# Test Case Template

## Test Case ID
TC-ORDERHISTORY-009

## Feature
Xem lịch sử đơn hàng (User)

## Requirement Reference
FR-11

## Testing Technique
Domain Testing / Boundary Value Analysis

## Test Objective
Kiểm tra hiển thị trạng thái "delivered" (đã giao)

## Preconditions
Người dùng có 1 đơn hàng đã hoàn tất (trạng thái delivered)

## Test Data
| Parameter | Value |
|-|-|
| Trạng thái | delivered |

## Test Steps
1. Truy cập Lịch sử đơn hàng.
2. Tìm đơn hàng có trạng thái "delivered".
3. Kiểm tra text và màu sắc của trạng thái.

## Expected Result
Trạng thái hiển thị là "Đã giao" hoặc "Hoàn thành", có màu sắc tích cực (VD: màu xanh lá).

## Actual Result
(Chưa thực thi)

## Status
NOT EXECUTED

## Bug Reference
