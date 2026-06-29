# TC-FORGOT-019: Kiểm thử hiển thị chỉ báo bước (Step Indicator)

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng truy cập trang Quên mật khẩu

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email (Bước 1) | test@eshop.com |

## Test steps
1. Truy cập trang Quên mật khẩu.
2. Quan sát chỉ báo bước trên giao diện Bước 1.
3. Nhập Email `test@eshop.com` và bấm "Lấy mã OTP".
4. Quan sát chỉ báo bước trên giao diện Bước 2.

## Expected result
- Bước 1: Giao diện hiển thị chỉ báo bước, ví dụ "Bước 1 / 2".
- Bước 2: Giao diện hiển thị chỉ báo bước, ví dụ "Bước 2 / 2".

## Sub-domains covered
SD-UI01 (step indicator hiển thị đúng theo bước)

## Type
Valid

## Status / Related bugs
Fail / #5
