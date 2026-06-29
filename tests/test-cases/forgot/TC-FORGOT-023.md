# TC-FORGOT-023: Kiểm thử Email với độ dài ngay trên tối thiểu (6 ký tự) — Bước 1

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Boundary Value Analysis

## Boundary under test
Email at min+ — value: 6 ký tự (`aaaaaa`)

## Preconditions
- Người dùng đang ở Bước 1 của trang Quên mật khẩu

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | aaaaaa |

## Test steps
1. Truy cập trang Quên mật khẩu (Bước 1).
2. Nhập Email có độ dài 6 ký tự.
3. Bấm "Lấy mã OTP".

## Expected result
- Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Email.

## Valid / Invalid
Valid (về độ dài)

## Status / Related bugs
Pass / None
