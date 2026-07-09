# Domain Testing Checklist

Rà soát chất lượng thiết kế test case phân vùng tương đương của bạn trước khi thực thi.

## 1. Phân Tích Phân Vùng Tương Đương (EP)
- [ ] Tất cả các trường dữ liệu đầu vào đã được liệt kê đầy đủ chưa?
- [ ] Đã xác định rõ kiểu dữ liệu và các ràng buộc nghiệp vụ cho từng trường chưa?
- [ ] Các phân vùng hợp lệ (Valid Partitions) có bao phủ toàn bộ các trường hợp nghiệp vụ thông thường không?
- [ ] Các phân vùng không hợp lệ (Invalid Partitions) đã bao phủ:
  - [ ] Trường để trống (Empty/Blank)?
  - [ ] Giá trị null?
  - [ ] Sai kiểu dữ liệu (chữ nhập vào số, ký tự đặc biệt)?
  - [ ] Quá độ dài cho phép?
  - [ ] Dữ liệu không logic (ví dụ: ngày kết thúc trước ngày bắt đầu)?

## 2. Thiết Kế Test Case (Test Case Design)
- [ ] Test Case ID có đặt đúng định dạng `TC-<FEATURE_ID>-DT-001` không?
- [ ] Mỗi phân vùng không hợp lệ có được kiểm thử bởi một test case độc lập không (Single Fault Assumption)?
- [ ] Kết quả mong đợi (Expected Result) có cụ thể không (tránh ghi chung chung "hệ thống báo lỗi", phải ghi rõ "hiển thị thông báo lỗi 'Mật khẩu phải chứa ít nhất 8 ký tự'")?
- [ ] Trạng thái ban đầu (Status) của các test case mới tạo có được để là `Not Executed` không?
- [ ] Đã chỉ ra được tiền điều kiện (Preconditions) và dữ liệu test cụ thể (Test Data) cho từng case chưa?
