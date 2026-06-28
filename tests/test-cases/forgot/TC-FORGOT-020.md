# TC-FORGOT-020: Kiểm thử nút Quay lại đăng nhập

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đang ở trang Quên mật khẩu (Bước 1 hoặc Bước 2)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| (Không áp dụng) | — |

## Test steps
1. Truy cập trang Quên mật khẩu.
2. Tìm và bấm nút "Quay lại đăng nhập".
3. (Tùy chọn) Lặp lại sau khi chuyển sang Bước 2.

## Expected result
- Hệ thống điều hướng người dùng về trang Đăng nhập (`/login`).

## Sub-domains covered
SD-UI02 (nút quay lại đăng nhập)

## Type
Valid

## Status / Related bugs
Not Run / None
