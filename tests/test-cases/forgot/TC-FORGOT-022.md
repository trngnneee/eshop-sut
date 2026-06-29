# TC-FORGOT-022: Kiểm thử Email với độ dài biên tối thiểu (5 ký tự) — Bước 1

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Boundary Value Analysis

## Boundary under test
Email at min — value: 5 ký tự (`aaaaa`)

## Preconditions
- Người dùng đang ở Bước 1 của trang Quên mật khẩu

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | aaaaa |

## Test steps
1. Truy cập trang Quên mật khẩu (Bước 1).
2. Nhập Email có độ dài đúng 5 ký tự.
3. Bấm "Lấy mã OTP".

## Expected result
- Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Email.
- ⚠️ Nếu Email chưa đăng ký, hệ thống trả lỗi nghiệp vụ (không phải lỗi độ dài).

## Valid / Invalid
Valid (về độ dài)

## Status / Related bugs
Pass / None
