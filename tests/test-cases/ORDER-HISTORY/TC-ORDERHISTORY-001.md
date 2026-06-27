# Test Case Template

## Test Case ID
TC-ORDERHISTORY-001

## Feature
Xem lịch sử đơn hàng (User)

## Requirement Reference
FR-11

## Testing Technique
Domain Testing / Boundary Value Analysis

## Test Objective
Kiểm tra người dùng chưa đăng nhập không thể xem lịch sử đơn hàng

## Preconditions
Người dùng chưa đăng nhập vào hệ thống

## Test Data
| Parameter | Value |
|-|-|
| Trạng thái đăng nhập | False |

## Test Steps
1. Mở trang web EShop.
2. Cố gắng truy cập trực tiếp vào URL trang Lịch sử đơn hàng (`/profile`).

## Expected Result
Hệ thống chặn truy cập và yêu cầu đăng nhập.

## Actual Result
Hệ thống không cho phép truy cập và yêu cầu đăng nhập.

## Status
PASSED

## Bug Reference
None