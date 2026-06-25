# TC-JWT-005: Kiểm tra Token JWT của User A không được truy cập dữ liệu User B

## Requirement ID
SEC-02

## Module / Test type / Technique
JWT / Security & Access Control

## Preconditions
- Đăng nhập tài khoản User A lấy token A.
- User B có tài nguyên riêng (ví dụ đơn hàng ID của B).

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Token A | User A Token |
| Order ID B | 123 |

## Test steps
1. Gửi yêu cầu lấy chi tiết đơn hàng của User B kèm Token xác thực của User A.

## Expected result
- API trả về HTTP 403 Forbidden (hoặc 404 để giấu tài nguyên) từ chối truy cập chéo.

## Status / Related bugs
Not Run / None
