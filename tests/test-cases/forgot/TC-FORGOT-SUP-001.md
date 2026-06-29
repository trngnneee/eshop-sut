# TC-FORGOT-SUP-001: API sinh OTP đúng 6 chữ số (kiểm tra backend)

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Supplementary

## Preconditions
- Tài khoản `test@eshop.com` tồn tại
- Backend API đang chạy tại `http://localhost:3000`

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |

## Test steps
1. Gửi `POST /api/forgot-password` với body `{"email":"test@eshop.com"}`.
2. Đọc trường `resetToken` trong response JSON.
3. Kiểm tra độ dài và định dạng của `resetToken`.

## Expected result
- `resetToken` là chuỗi gồm **đúng 6 chữ số** (regex `^\d{6}$`).
- UI demo hiển thị cùng giá trị và label phải mô tả OTP 6 số.

## Sub-domains covered
GAP-02 — OTP length contract

## Type
Valid

## Status / Related bugs
Not Run / #6
