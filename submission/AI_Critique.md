# Bài Phê Bình AI Phản Biện (AI Critique) — HW04

**Khoa Công nghệ Thông tin – Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM**  
**Môn học: CS423 / CSC13003 – Kiểm thử phần mềm (AI-augmented · 2026)**

---

## Thông Tin Sinh Viên

| Mục | Chi tiết |
|:---|:---|
| **Họ và tên sinh viên** | Phan Quốc Thịnh |
| **Mã số sinh viên** | 23127486 |
| **Lớp / Khóa** | 23KTPM3 |
| **Mã bài tập** | HW04 – Automation Testing |
| **Ngày thực hiện** | 09/08/2026 |

---

## Bài Phê Bình và Đánh Giá Phản Biện AI (200–300 từ — Bắt buộc)

Trong quá trình sử dụng các mô hình ngôn ngữ lớn (AI) để sinh kịch bản kiểm thử tự động (Playwright) cho hệ thống EShop ở bài tập HW04, tôi ghi nhận một số điểm hạn chế và sai lệch đáng chú ý:

Thứ nhất, AI mắc phải thiên kiến giả định hệ thống lý tưởng (happy path assumption). Khi sinh script cho tính năng Đăng ký (FR-01) và Mã giảm giá (FR-09), AI tự động tạo các assertion giả định rằng hệ thống kiểm tra định dạng email bằng `type="email"` và kiểm tra mật khẩu hợp lệ với các ký tự đặc biệt như `@!#$`. Tuy nhiên, mã nguồn thực tế của SUT lại dùng regex có lỗi `(?=.*\s)` (đòi hỏi khoảng trắng và cấm ký tự đặc biệt), cũng như không đặt ràng buộc `UNIQUE` trên cột `email`. AI đã hoàn toàn bỏ sót các khiếm khuyết tiềm ẩn này trong lần sinh đầu tiên.

Thứ hai, AI thường sinh các selector dễ vỡ (fragile selectors) dựa trên text hiển thị cứng như `page.getByRole('heading', { name: 'Đăng Nhập' })`, dẫn đến test bị fail do trang Login của SUT thực tế mang nhãn `Đăng Ký`. Nguyên nhân chính là AI thiếu khả năng truy cập trực tiếp vào DOM runtime động và chỉ suy luận dựa trên ngữ cảnh chung của ứng dụng thương mại điện tử.

Bài học cốt lõi tôi rút ra: AI là công cụ tăng tốc tuyệt vời để sinh khung test case, dữ liệu data-driven và cú pháp boilerplate, nhưng không thể thay thế năng lực kiểm thử phê phán (critical testing) của con người. Người kiểm thử phải kiểm chứng mã nguồn SUT, áp dụng kỹ thuật Boundary Value Analysis và Equivalence Partitioning theo chuẩn ISTQB, đồng thời đối chiếu assertion theo đặc tả SRS để phát hiện đúng các khiếm khuyết phần mềm.

---

*Số lượng từ: 274 từ (đáp ứng đúng chuẩn quy định 200–300 từ)*
