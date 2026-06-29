# TC-FORGOT-SUP-003: Trường Email phải dùng type="email" (FR-22)

## Requirement ID
FR-03, FR-22

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Supplementary

## Preconditions
- Người dùng ở Bước 1 trang `/forgot-password`

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email input | (inspect DOM) |

## Test steps
1. Mở trang Quên mật khẩu.
2. Inspect thuộc tính `type` của input Email.
3. Nhập `notanemail` và thử submit.

## Expected result
- Input Email có `type="email"`.
- Trình duyệt chặn submit hoặc hiển thị lỗi HTML5 khi format không hợp lệ.

## Sub-domains covered
GAP-04 — FR-22 cross-requirement

## Type
Valid

## Status / Related bugs
Not Run / #8
