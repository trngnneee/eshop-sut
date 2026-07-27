## Title
[Minor] Cấu trúc thẻ <h1> sai trên nhiều trang

## Description
Trang chủ có 2 `<h1>` (Home.jsx:44,110); 6 trang (login/register/forgot/cart/checkout/profile) không có `<h1>` nào.

## Steps to Reproduce
1. Mở từng trang, chạy `document.querySelectorAll('h1').length`.

## Expected Result
Mỗi trang có đúng 1 `<h1>` mô tả nội dung.

## Actual Result
- (GUI-IA01-09) Trang chủ có 2 thẻ <h1> (tiêu đề "Danh sách sản phẩm" và dòng đếm "Hiển thị N sản phẩm" đều là h1) — vượt quá 1.
- (GUI-IA01-10) Số thẻ <h1> mỗi trang: /login=0, /register=0, /forgot-password=0, /cart=0, /checkout=0, /profile=0 — các trang này chỉ có <h2>, thiếu <h1> mô tả nội dung.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA01-09, GUI-IA01-10

## Requirement
FR-21 (tiêu đề trang)

## Severity
Minor — Ảnh hưởng SEO và screen reader (đọc cấu trúc trang).

## Screenshot
![GUI-IA01-09](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965698/eshop-hw03/gui-checklist/GUI-IA01-09.png) ![GUI-IA01-10](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965699/eshop-hw03/gui-checklist/GUI-IA01-10.png)