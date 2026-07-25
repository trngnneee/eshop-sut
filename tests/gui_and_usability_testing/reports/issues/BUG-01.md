## Title
[Blocker] XSS: từ khoá tìm kiếm và tên người dùng render bằng dangerouslySetInnerHTML

## Description
Từ khoá tìm kiếm (Home.jsx:62-67) và tên user trên header (App.jsx:26-28) được render qua `dangerouslySetInnerHTML`, không thoát HTML. Payload chứa mã JS sẽ được thực thi.

## Steps to Reproduce
1. Mở trang chủ `localhost:5173/`.
2. Nhập vào ô tìm kiếm: `<img src=x onerror=window.__xss=1>` rồi bấm Tìm.
3. Mở Console kiểm tra biến `window.__xss`.

## Expected Result
Từ khoá hiển thị dạng text thuần, không thực thi JS (`window.__xss` không được đặt).

## Actual Result
- (GUI-IA04-13) Từ khoá tìm kiếm được render bằng dangerouslySetInnerHTML: payload "<img onerror>" THỰC THI JS (window.__xss=1) — lỗ hổng XSS. Tên user ở header cũng render tương tự.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA04-13

## Requirement
FR-24 + README mục 1 (safe rendering)

## Severity
Blocker — Cho phép thực thi JS tuỳ ý trong trình duyệt nạn nhân — lỗ hổng bảo mật nghiêm trọng nhất.

## Screenshot
![GUI-IA04-13](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965772/eshop-hw03/gui-checklist/GUI-IA04-13.png)