# TC-MFORGOT-023: Kiểm thử Email với độ dài ngay trên tối thiểu (6 ký tự) — Bước 1

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Boundary Value Analysis

## Boundary under test
Email at min+ — value: 6 ký tự (`aaaaaa`)

## Preconditions
- Người dùng đang ở Bước 1 của màn hình Quên Mật Khẩu trên Mobile App

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | aaaaaa |

## Test steps
1. Mở Mobile App, vào màn hình Đăng nhập, bấm "Quên mật khẩu?" để vào màn hình Quên Mật Khẩu (Bước 1).
2. Nhập Email có độ dài 6 ký tự.
3. Bấm "Lấy mã OTP".

## Expected result
- Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Email.

## Valid / Invalid
Valid (về độ dài)

## Status / Related bugs
Pass / None