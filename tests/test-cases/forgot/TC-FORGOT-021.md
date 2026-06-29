# TC-FORGOT-021: Kiểm thử Email với độ dài dưới tối thiểu (4 ký tự) — Bước 1

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Boundary Value Analysis

## Boundary under test
Email at min− — value: 4 ký tự (`aaaa`)

## Preconditions
- Người dùng đang ở Bước 1 của trang Quên mật khẩu

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | aaaa |

## Test steps
1. Truy cập trang Quên mật khẩu (Bước 1).
2. Nhập Email có độ dài 4 ký tự.
3. Bấm "Lấy mã OTP".

## Expected result
- Hệ thống báo lỗi độ dài Email tối thiểu là 5 ký tự.
- Không chuyển sang Bước 2.

## Valid / Invalid
Invalid

## Status / Related bugs
Fail / None
