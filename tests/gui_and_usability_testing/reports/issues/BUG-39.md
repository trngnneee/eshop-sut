## Title
[Minor] Sau khi buộc đăng nhập từ checkout, mất ngữ cảnh (về trang chủ)

## Description
Login luôn về `/` (Login.jsx:16) thay vì quay lại giỏ/checkout.

## Steps to Reproduce
1. Chưa login, từ giỏ bấm thanh toán → bị chuyển login → đăng nhập.

## Expected Result
Quay lại giỏ/checkout sau khi đăng nhập.

## Actual Result
- (GUI-IA03-09) Sau khi buộc đăng nhập từ luồng checkout, người dùng bị đưa về "http://localhost:5173/" (trang chủ) thay vì quay lại giỏ/checkout — mất ngữ cảnh.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA03-09

## Requirement
Heuristic (redirect flow)

## Severity
Minor — Người dùng phải tự tìm lại giỏ/checkout.

## Screenshot
![GUI-IA03-09](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965745/eshop-hw03/gui-checklist/GUI-IA03-09.png)