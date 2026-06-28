# TC-FORGOT-002: Kiểm thử Email để trống (Bước 1)

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đang ở Bước 1 của trang Quên mật khẩu

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | [Để trống] |

## Test steps
1. Truy cập trang Quên mật khẩu (Bước 1).
2. Để trống trường Email.
3. Bấm "Lấy mã OTP".

## Expected result
- Hệ thống từ chối gửi yêu cầu và hiển thị thông báo lỗi bắt buộc nhập Email.
- Không chuyển sang Bước 2.

## Sub-domains covered
SD-E01 (email rỗng)

## Type
Invalid

## Status / Related bugs
Not Run / None
