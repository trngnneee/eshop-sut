# TC-CHECKOUT-SUP-001: API checkout với JWT Token không hợp lệ bị từ chối

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Supplementary

## Preconditions
- Backend API đang chạy

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Authorization | Bearer {chuỗi token không hợp lệ hoặc đã hết hạn} |
| total_amount | 100000 |

## Test steps
1. Gửi yêu cầu checkout tới API kèm JWT Token không hợp lệ hoặc đã hết hạn.
2. Ghi nhận mã trạng thái HTTP và nội dung phản hồi.

## Expected result
- API từ chối yêu cầu vì token không hợp lệ.
- Không tạo đơn hàng mới.

## Sub-domains covered
SD-A03 (token không hợp lệ / hết hạn)

## Type
Invalid

## Status / Related bugs
Not Run / None
