# TC-LOGIN-BVA-006: Kiểm tra Email biên độ dài max + 1 (255 ký tự)

## Requirement ID
FR-02, FR-22

## Module / Test type / Technique
Login / Boundary Value Analysis (BVA)

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@eshop.com |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Nhập email dài 255 ký tự.
2. Nhấn 'Đăng nhập'.

## Expected result
- Hệ thống báo lỗi định dạng hoặc vượt quá độ dài tối đa cho phép.

## Status / Related bugs
Pass / None
