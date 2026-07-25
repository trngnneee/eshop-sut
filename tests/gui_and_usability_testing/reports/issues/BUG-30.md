## Title
[Minor] Ô OTP không giới hạn 4 chữ số

## Description
Ô OTP nhận "123456abcd" — không có maxLength/pattern (ForgotPassword.jsx:71-77).

## Steps to Reproduce
1. Vào bước 2, nhập `123456abcd` vào ô OTP.

## Expected Result
Chỉ nhận tối đa 4 chữ số.

## Actual Result
- (GUI-IA02-08) Ô OTP (nhãn "4 số") nhận giá trị "123456abcd" (dài 10, cả chữ) — không có maxLength/pattern giới hạn 4 chữ số.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA02-08

## Requirement
FR-22 (format constraints)

## Severity
Minor — Nhận input sai định dạng so với nhãn "4 số".

## Screenshot
![GUI-IA02-08](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965722/eshop-hw03/gui-checklist/GUI-IA02-08.png)