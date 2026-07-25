## Title
[Major] Regex mật khẩu mâu thuẫn với hint (đòi khoảng trắng, cấm ký tự đặc biệt)

## Description
Regex yêu cầu có khoảng trắng và chỉ cho phép `[A-Za-z\d\s]` (Register.jsx:16-19) trong khi hint ghi cần "ký tự đặc biệt".

## Steps to Reproduce
1. Mở `/register`.
2. Nhập mật khẩu `Abcdef1!` (đủ điều kiện theo hint) và submit.

## Expected Result
Mật khẩu đúng như hint được chấp nhận; validate và hint không mâu thuẫn.

## Actual Result
- (GUI-IA02-07) Mật khẩu "Abcdef1!" (đủ hoa/thường/số/ký tự đặc biệt như hint) bị từ chối: "Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT." — regex thực tế bắt buộc có khoảng trắng và cấm ký tự đặc biệt, mâu thuẫn với hint.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA02-07

## Requirement
FR-22 (validation)

## Severity
Major — Mật khẩu đúng như hướng dẫn vẫn bị từ chối — chặn đăng ký/đổi mật khẩu.

## Screenshot
![GUI-IA02-07](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965719/eshop-hw03/gui-checklist/GUI-IA02-07.png)