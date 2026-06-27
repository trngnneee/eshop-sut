# Test Case Template

## Test Case ID
TC-ORDERHISTORY-008

## Feature
Xem lịch sử đơn hàng (User)

## Requirement Reference
FR-11

## Testing Technique
Domain Testing / Boundary Value Analysis

## Test Objective
Kiểm tra hiển thị trạng thái "shipping" (đang giao)

## Preconditions
Người dùng có 1 đơn hàng đang trong quá trình vận chuyển (trạng thái shipping)

## Test Data
| Parameter | Value |
|-|-|
| Trạng thái | shipping |

## Test Steps
1. Truy cập Lịch sử đơn hàng.
2. Tìm đơn hàng có trạng thái "shipping".
3. Kiểm tra text và màu sắc của trạng thái.

## Expected Result
Trạng thái hiển thị là "Đang giao", có màu sắc phân biệt (VD: màu xanh lơ/xanh lam).

## Actual Result
(Chưa thực thi)

## Status
NOT EXECUTED

## Bug Reference
