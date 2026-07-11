# TC-CHECKOUT-SUP-005: API từ chối header Authorization sai định dạng

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Supplementary

## Preconditions
- Backend API đang chạy

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Authorization | NotBearer sometoken (thiếu tiền tố Bearer) |

## Test steps
1. Gửi yêu cầu checkout với header `Authorization: NotBearer sometoken`.
2. Ghi nhận mã trạng thái và phản hồi.

## Expected result
- API từ chối yêu cầu (401/403); không tạo đơn hàng.

## Sub-domains covered
GAP-02 — Authorization header malformed

## Type
Invalid

## Status / Related bugs
Not Run / None
