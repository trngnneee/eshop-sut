# TC-PRODUCT-SUP-002: User thường không truy cập được trang Quản lý Sản phẩm (FR-12)

## Requirement ID
FR-15, FR-12

## Module / Test type / Technique
Admin Product / Security / Domain Testing – Supplementary

## Preconditions
- Tài khoản `test@eshop.com` / `Test1234!` tồn tại (role user)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| URL | `/admin/products` |

## Test steps
1. Đăng nhập bằng user thường.
2. Truy cập `/admin/products`.
3. Quan sát URL và nội dung trang.

## Expected result
- User thường **không** truy cập được trang Admin CRUD sản phẩm.
- Bị chuyển hướng ra khỏi `/admin/products`.

## Sub-domains covered
GAP-02 — FR-12 UI access control

## Type
Invalid

## Status / Related bugs
Fail / #15, #18
