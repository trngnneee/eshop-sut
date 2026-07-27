## Title
[Minor] Thông báo bắt buộc nhập hiển thị tiếng Anh (HTML5 native)

## Description
Dựa vào `required` native → tooltip "Please fill out this field." theo ngôn ngữ trình duyệt.

## Steps to Reproduce
1. Submit form khi để trống field bắt buộc.

## Expected Result
Thông báo required bằng tiếng Việt, cùng style lỗi khác.

## Actual Result
- (GUI-IA02-14) Thông báo required dựa vào HTML5 native → hiển thị theo ngôn ngữ trình duyệt: "Please fill out this field." (tiếng Anh), không nhất quán tiếng Việt với các lỗi khác của app.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA02-14

## Requirement
Heuristic (validation consistency)

## Severity
Minor — Không nhất quán ngôn ngữ.

## Screenshot
![GUI-IA02-14](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965730/eshop-hw03/gui-checklist/GUI-IA02-14.png)