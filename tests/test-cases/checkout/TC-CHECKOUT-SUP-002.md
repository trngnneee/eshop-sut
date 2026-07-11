# TC-CHECKOUT-SUP-002: API checkout không có JWT Token bị từ chối

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Supplementary

## Preconditions
- Backend API đang chạy

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Authorization | [Không gửi header Authorization] |
| total_amount | 100000 |

## Test steps
1. Gửi yêu cầu checkout tới API (ví dụ `POST /api/checkout`) **không** kèm JWT Token.
2. Ghi nhận mã trạng thái HTTP và nội dung phản hồi.

## Expected result
- API từ chối yêu cầu vì người dùng chưa xác thực (FR-08: chỉ người đã đăng nhập mới thanh toán được).
- Không tạo đơn hàng mới.

## Sub-domains covered
SD-A01 (chưa đăng nhập — kiểm tra tầng API)

## Type
Invalid

## Status / Related bugs
Not Run / None
