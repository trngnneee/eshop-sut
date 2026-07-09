# TC-DASHBOARD-DT-012: Kiểm tra tính Responsive của Dashboard trên các thiết bị Desktop/Tablet/Mobile
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / UI/UX / Equivalence Partitioning
## Preconditions
- Admin đã đăng nhập thành công và đang ở tab Dashboard
## Test data
| Viewports | Desktop (>=1366px), Tablet (768px), Mobile (375px) |
## Test steps
1. Đăng nhập trang Admin.
2. Thay đổi kích thước trình duyệt hoặc dùng DevTools Responsive Mode lần lượt qua các kích cỡ 1920x1080, 768x1024, và 375x812.
3. Rà soát vị trí các card hiển thị số liệu.
## Expected result
- Layout co giãn mượt mà phù hợp với từng màn hình.
- Các card hiển thị không bị tràn, đè chữ hay biến mất khỏi khung nhìn.
## Status / Related bugs
Pass / None
