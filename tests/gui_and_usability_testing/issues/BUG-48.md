## Title
[Minor] Thẻ <html> khai báo lang="en" trong khi UI tiếng Việt

## Description
`index.html:2` khai báo `lang="en"`.

## Steps to Reproduce
1. Mở app, kiểm tra thuộc tính `lang` của `<html>` (DevTools).

## Expected Result
`<html lang="vi">`.

## Actual Result
- (GUI-GAP-03) Thẻ <html> khai báo lang="en" trong khi toàn bộ UI là tiếng Việt — sai ngôn ngữ nội dung (WCAG 3.1.1).

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-GAP-03

## Requirement
Heuristic / WCAG 3.1.1

## Severity
Minor — Sai ngôn ngữ nội dung (WCAG 3.1.1), screen reader đọc sai giọng.

## Screenshot
![GUI-GAP-03](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965683/eshop-hw03/gui-checklist/GUI-GAP-03.png)