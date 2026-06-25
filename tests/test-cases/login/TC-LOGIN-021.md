# TC-LOGIN-021: Kiểm tra thứ tự di chuyển tiêu điểm (Tab Order) và khả năng tiếp cận bàn phím
## Requirement ID
FR-21, FR-22
## Module / Test type / Technique
Login / UI/UX & Accessibility / Accessibility Testing
## Preconditions
- Người dùng đang ở trang đăng nhập của Web hoặc Admin.
- Không sử dụng chuột, chỉ sử dụng bàn phím.
## Test data
Không yêu cầu dữ liệu nhập cụ thể.
## Test steps
1. Nhấn phím `Tab` để di chuyển tiêu điểm (focus) vào trang đăng nhập.
2. Nhấn liên tục phím `Tab` và quan sát thứ tự di chuyển của tiêu điểm qua các phần tử.
3. Kiểm tra xem tiêu điểm có di chuyển tuần tự từ trên xuống dưới, từ trái sang phải hay không.
4. Kiểm tra xem có thể nhấn `Space` hoặc `Enter` để kích hoạt các nút bấm (Login, Toggle hiện mật khẩu) hay không.
## Expected result
- Tiêu điểm phải bắt đầu ở trường nhập Email -> Mật khẩu -> Nút Toggle -> Nút Submit (Đăng nhập) theo đúng thứ tự logic.
- Không được xảy ra tình trạng nút Submit được focus trước các ô nhập liệu (lỗi `tabIndex={1}` thiết lập sai vị trí).
- Có thể dùng bàn phím để kích hoạt toàn bộ tính năng trên form đăng nhập.
## Status / Related bugs
Failed / BUG-FR02-A-16
