## Title
[Minor] Empty state thiếu icon/minh hoạ; tìm kiếm 0 kết quả không có empty state

## Description
Empty state giỏ/đơn chỉ có text (Cart.jsx:20-27, Profile.jsx:169-170); tìm 0 kết quả cho grid trống hoàn toàn (Home.jsx:75-114).

## Steps to Reproduce
1. Mở `/cart` trống.
2. Tìm từ khoá `zzzzzzzz` ở `/`.

## Expected Result
Empty state có icon/hình + message thân thiện + CTA.

## Actual Result
- (GUI-IA04-05) Empty state Giỏ hàng chỉ có text + link, không có icon/hình minh hoạ (số ảnh/SVG trong main: 0). Lịch sử ĐH trống cũng chỉ là text trần.
- (GUI-IA04-06) Tìm từ khoá không tồn tại ("zzzzzzzz") cho grid trống hoàn toàn, không có empty-state ("Không tìm thấy sản phẩm...").

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA04-05, GUI-IA04-06

## Requirement
FR-24 (empty-state visuals)

## Severity
Minor — Trạng thái trống sơ sài / trống trơn gây bối rối.

## Screenshot
![GUI-IA04-05](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965759/eshop-hw03/gui-checklist/GUI-IA04-05.png) ![GUI-IA04-06](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965761/eshop-hw03/gui-checklist/GUI-IA04-06.png)