## Title
[Minor] Feedback thành công/lỗi dùng alert() native khắp nơi

## Description
Dùng `alert()` native cho feedback (ForgotPassword/Profile/Cart/Checkout).

## Steps to Reproduce
1. Thực hiện các thao tác có feedback, quan sát alert() native.

## Expected Result
Feedback dùng một pattern in-page thống nhất.

## Actual Result
- (GUI-IA04-10) Feedback cập nhật hồ sơ dùng alert() native (đã bắt được dialog alert) thay vì toast/thông báo trong trang — không nhất quán, còn 8+ chỗ dùng alert.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA04-10

## Requirement
Heuristic (feedback consistency)

## Severity
Minor — Không nhất quán, trải nghiệm kém (8+ chỗ).

## Screenshot
![GUI-IA04-10](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965768/eshop-hw03/gui-checklist/GUI-IA04-10.png)