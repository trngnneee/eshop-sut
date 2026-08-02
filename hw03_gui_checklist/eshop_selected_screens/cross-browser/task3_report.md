# Task 3 — Cross-Browser / Cross-Platform Report

## 1. Mục tiêu kiểm thử

Task 3 xác nhận mức độ ổn định giao diện và hành vi chức năng của EShop trên 3 nền tảng được ghi nhận trong checklist:

- Microsoft Edge
- Firefox
- Mobile (Expo Go)

Checklist dùng để lập báo cáo gồm 52 tiêu chí, bao phủ 4 nhóm IA:
- IA-01 General UI standards
- IA-02 Forms
- IA-03 Navigation
- IA-04 Feedback / state

## 2. Môi trường và minh chứng

- Desktop browser: Microsoft Edge, Firefox
- Mobile runtime: Expo Go
- Minh chứng ảnh chụp hiện có trong thư mục `cross-browser/`:
  - [Microsoft Edge](microsoft_edge.png)
  - [Firefox](firefox.png)

## 3. Tóm tắt kết quả theo nền tảng

| Nền tảng | Tổng số Items | Pass | Fail | N/A | Tỷ lệ Pass |
|---|---:|---:|---:|---:|---:|
| Microsoft Edge | 52 | 31 | 21 | 0 | 59.6% |
| Firefox | 52 | 31 | 21 | 0 | 59.6% |
| Mobile (Expo Go) | 52 | 23 | 9 | 20 | 44.2% trên các mục áp dụng |

Ghi chú:
- Với Mobile (Expo Go), 20 mục được đánh dấu N/A vì checklist có nhiều tiêu chí riêng cho giao diện web admin không áp dụng trên mobile.
- Các kết quả Edge và Firefox giống nhau hoàn toàn trong bộ checklist hiện tại.

## 4. Các lỗi nổi bật trên Microsoft Edge và Firefox

Hai trình duyệt desktop cho kết quả giống nhau và cùng gặp 21 lỗi sau:

- GUI-008: Nhãn tổng tiền hiển thị "Tổng tạm tính" thay vì "Tổng cộng"
- GUI-014: Ô số lượng chấp nhận giá trị không hợp lệ
- GUI-015: Không hiển thị lỗi khi nhập số lượng không hợp lệ
- GUI-018: Thiếu điều khiển tăng/giảm số lượng trong giỏ hàng
- GUI-019: Không hỗ trợ chỉnh sửa số lượng trực tiếp đúng chuẩn
- GUI-020: Form Admin thiếu dấu * cho trường bắt buộc
- GUI-021: Validation Tên sản phẩm chưa đúng
- GUI-022: Validation Giá sản phẩm chưa đúng
- GUI-025: Thiếu preview và validation URL ảnh
- GUI-026: Import CSV không chặn file sai định dạng
- GUI-027: Parse CSV bị vỡ cột khi có dấu phẩy trong dấu nháy kép
- GUI-028: Trang Product Detail thiếu breadcrumb
- GUI-030: Badge số lượng trên navbar không cập nhật ngay
- GUI-032: Trang Cart thiếu breadcrumb
- GUI-039: Hiển thị text debug khi sản phẩm không tồn tại
- GUI-040: Phản hồi thêm vào giỏ chưa tức thì
- GUI-041: Xử lý số lượng không hợp lệ khi thêm vào giỏ chưa an toàn
- GUI-042: Giỏ hàng trống thiếu minh họa thân thiện
- GUI-043: Xóa sản phẩm không có hộp thoại xác nhận
- GUI-045: Sửa sản phẩm trong Admin làm ghi đè tên toàn bộ danh sách
- GUI-046: Xóa sản phẩm trong Admin không có xác nhận

## 5. Kết quả trên Mobile (Expo Go)

Mobile có 9 lỗi thực tế và 20 mục N/A do không áp dụng trên nền tảng này.

Lỗi chỉ xuất hiện trên Mobile và đã được report riêng dưới dạng lỗi đa nền tảng:
- GUI-003: Ảnh sản phẩm có alt rỗng

### 5.1. Các lỗi gặp trên Mobile

- GUI-003: Ảnh sản phẩm có alt rỗng
- GUI-008: Nhãn tổng tiền sai
- GUI-015: Không chặn nhập số lượng không hợp lệ
- GUI-018: Thiếu tăng/giảm số lượng trong giỏ hàng
- GUI-028: Thiếu breadcrumb ở Product Detail
- GUI-032: Thiếu breadcrumb ở Cart
- GUI-039: Hiển thị text debug khi sản phẩm không tồn tại
- GUI-042: Giỏ hàng trống thiếu minh họa
- GUI-043: Xóa sản phẩm không có xác nhận

### 5.2. Các mục N/A trên Mobile

Các mục liên quan đến Admin Web không áp dụng trên Expo Go, gồm:
- GUI-011 đến GUI-013
- GUI-020 đến GUI-027
- GUI-035 đến GUI-037
- GUI-045 đến GUI-047

## 6. Nhận xét tổng quan

- Checklist cho thấy các lỗi lặp lại nhất quán giữa Edge và Firefox, nên đây là vấn đề ở tầng ứng dụng chứ không phải lỗi riêng của một trình duyệt.
- Mobile chỉ giữ lại một phần luồng storefront, do đó nhiều mục Admin được ghi N/A hợp lý.
- Các lỗi có ảnh hưởng lớn nhất nằm ở nhóm Navigation, Forms, và Feedback/state: breadcrumb thiếu, validation số lượng lỗi, phản hồi thêm giỏ hàng chậm, và thiếu xác nhận khi xóa.

## 7. Kết luận

Task 3 đạt yêu cầu báo cáo đa nền tảng với 3 môi trường kiểm thử. Kết quả cho thấy Microsoft Edge và Firefox có cùng hồ sơ lỗi, còn Mobile (Expo Go) có ít lỗi hơn nhưng vẫn tồn tại một số vấn đề quan trọng trên luồng storefront. Bộ checklist hiện là cơ sở đủ để đối chiếu và ưu tiên khắc phục theo mức độ ảnh hưởng thực tế.
