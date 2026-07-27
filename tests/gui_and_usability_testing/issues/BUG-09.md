## Title
[Major] Nút "Thêm vào giỏ hàng" lệch khỏi khung ở mobile ≤640px

## Description
Class `bug-mobile-hidden` áp `margin-right:-100px` ở ≤640px (index.css:10-14) đẩy nút lệch/tràn khỏi khung.

## Steps to Reproduce
1. Mở `/product/1`.
2. Bật DevTools device toolbar, đặt viewport 375px.
3. Quan sát vị trí nút "Thêm vào giỏ hàng".

## Expected Result
Nút nằm trọn trong khung, bấm được ở 375px.

## Actual Result
- (GUI-IA01-14) Ở viewport 375px, nút "Thêm vào giỏ hàng" có margin-right -100px (class bug-mobile-hidden) → bị đẩy lệch/tràn khỏi khung.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA01-14

## Requirement
Heuristic (responsive)

## Severity
Major — Chức năng chính không dùng được trên mobile.

## Screenshot
![GUI-IA01-14](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965705/eshop-hw03/gui-checklist/GUI-IA01-14.png)