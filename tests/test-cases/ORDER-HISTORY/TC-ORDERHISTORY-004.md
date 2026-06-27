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
Kiểm tra người dùng chỉ có thể xem lịch sử đơn hàng của chính mình và không hiển thị đơn hàng của người dùng khác.

## Preconditions
- Người dùng A đã đăng nhập.
- Người dùng A có ít nhất 1 đơn hàng.
- Người dùng B có ít nhất 1 đơn hàng.

## Test Data
| Parameter | Value |
|-|-|
| Người dùng đăng nhập | User A |
| Đơn hàng của User A | Có |
| Đơn hàng của User B | Có |

## Test Steps
1. Đăng nhập bằng tài khoản User A.
2. Truy cập trang Lịch sử đơn hàng.
3. Kiểm tra danh sách đơn hàng được hiển thị.

## Expected Result
Hệ thống chỉ hiển thị các đơn hàng thuộc về User A.
Các đơn hàng của User B không được hiển thị trong danh sách lịch sử đơn hàng.

## Actual Result
User A chỉ thấy hiển thị đơn hàng của bản thân, không thấy đơn hàng của User B

## Status
PASSED

## Bug Reference
None