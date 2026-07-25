## Title
[Major] Link "Giỏ hàng" thiếu badge số lượng và không có feedback khi thêm giỏ

## Description
Link "Giỏ hàng" là link trần không badge (App.jsx:23); bấm "Thêm vào giỏ" ở trang chủ không có toast/badge nào (Home.jsx:98-103).

## Steps to Reproduce
1. Mở `/`.
2. Bấm "Thêm vào giỏ" một sản phẩm.
3. Quan sát header và vùng thao tác.

## Expected Result
Header có badge số lượng cập nhật tức thì; có phản hồi trực quan khi thêm giỏ.

## Actual Result
- (GUI-IA03-02) Link "Giỏ hàng" là link trần, không có badge số lượng; sau khi thêm 1 SP header vẫn không hiển thị counter. Header: "EShop Giỏ hàng Đăng nhập Đăng ký".
- (GUI-IA04-01) Bấm "Thêm vào giỏ" ở trang chủ không có phản hồi trực quan nào (không toast, không badge cập nhật trên header).

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA03-02, GUI-IA04-01

## Requirement
FR-23 (badge) + FR-24 (feedback)

## Severity
Major — Người dùng không biết đã thêm thành công hay giỏ có bao nhiêu món.

## Screenshot
![GUI-IA03-02](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965733/eshop-hw03/gui-checklist/GUI-IA03-02.png) ![GUI-IA04-01](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965753/eshop-hw03/gui-checklist/GUI-IA04-01.png)