## Title
[Minor] Link "Quên mật khẩu?" reload toàn trang

## Description
Dùng thẻ `<a href>` (Login.jsx:49-51) gây full page load.

## Steps to Reproduce
1. Mở `/login`, bấm "Quên mật khẩu?", quan sát Network tab.

## Expected Result
Điều hướng SPA, không reload toàn trang.

## Actual Result
- (GUI-IA03-07) Link "Quên mật khẩu?" dùng <a href> gây tải lại toàn trang (cờ SPA đặt trước khi click đã mất) — không điều hướng kiểu SPA như các link khác.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA03-07

## Requirement
Heuristic (navigation consistency)

## Severity
Minor — Không điều hướng SPA như các link khác.

## Screenshot
![GUI-IA03-07](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965742/eshop-hw03/gui-checklist/GUI-IA03-07.png)