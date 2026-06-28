# Boundary Value Analysis (BVA) Checklist

Rà soát chất lượng thiết kế test case giá trị biên của bạn trước khi thực thi.

## 1. Xác Định Biên (Boundary Identification)
- [ ] Đã lọc ra tất cả các biến có tính chất giới hạn hoặc khoảng giá trị số/độ dài chuỗi chưa?
- [ ] Khoảng giá trị hợp lệ `[Min, Max]` đã được xác định chính xác theo tài liệu spec chưa?

## 2. Xác Định Điểm Biên (Boundary Value Selection)
- [ ] Đã sử dụng quy tắc thiết kế 3-điểm-biên (3-point BVA) cho mỗi biên chưa?
  - [ ] Với biên dưới: Đã kiểm thử `Min-1` (invalid), `Min` (valid), và `Min+1` (valid) chưa?
  - [ ] Với biên trên: Đã kiểm thử `Max-1` (valid), `Max` (valid), và `Max+1` (invalid) chưa?
- [ ] Đối với trường độ dài chuỗi, đã kiểm thử chuỗi rỗng (`""`, độ dài = 0) chưa?
- [ ] Đối với các trường hợp đặc biệt, đã kiểm thử giá trị mặc định (Nominal value) chưa?

## 3. Định Dạng Test Case (Test Case Formatting)
- [ ] Test Case ID có đặt đúng định dạng `TC-<FEATURE_ID>-BVA-001` không?
- [ ] Trường Type có để là `Edge` hoặc `Negative`/`Positive` tương ứng không?
- [ ] Test steps có ghi rõ cách nhập giá trị biên cụ thể để kiểm tra phản ứng của hệ thống không?
