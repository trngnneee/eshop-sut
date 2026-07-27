## Title
[Major] Không có trang 404 / xử lý not-found thân thiện

## Description
Không có route catch-all (App.jsx:50-59) → `/abc` render vùng trống; `/product/999` hiện text "Lỗi trắng trang do data rỗng" không có link về.

## Steps to Reproduce
1. Truy cập `/abc-khong-ton-tai`.
2. Truy cập `/product/999`.

## Expected Result
Hiển thị trang 404/not-found thân thiện có link về trang chủ.

## Actual Result
- (GUI-IA03-05) URL không tồn tại /abc-khong-ton-tai render vùng nội dung trống ("") — không có route catch-all, không có trang 404 thân thiện.
- (GUI-IA03-06) /product/999 hiển thị text kỹ thuật "Sản phẩm không tồn tại (Lỗi trắng trang do data rỗng)" và không có link quay về — không thân thiện, không lối thoát.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA03-05, GUI-IA03-06

## Requirement
Heuristic (invalid-URL/404)

## Severity
Major — URL sai hoặc sản phẩm không tồn tại cho trang trắng / text kỹ thuật, không lối thoát.

## Screenshot
![GUI-IA03-05](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965739/eshop-hw03/gui-checklist/GUI-IA03-05.png) ![GUI-IA03-06](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965740/eshop-hw03/gui-checklist/GUI-IA03-06.png)