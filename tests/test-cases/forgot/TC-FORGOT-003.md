# TC-FORGOT-003: Kiểm thử Email sai định dạng (Bước 1)

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đang ở Bước 1 của trang Quên mật khẩu

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | not-an-email |

## Test steps
1. Truy cập trang Quên mật khẩu (Bước 1).
2. Nhập Email `not-an-email`.
3. Bấm "Lấy mã OTP".

## Expected result
- Hệ thống từ chối yêu cầu và hiển thị thông báo lỗi định dạng Email không hợp lệ.
- Không chuyển sang Bước 2.

## Sub-domains covered
SD-E02 (email sai định dạng)

## Type
Invalid

## Status / Related bugs
Fail / #8
