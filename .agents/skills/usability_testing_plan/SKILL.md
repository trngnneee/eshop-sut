---
name: usability_testing_plan
description: "Hướng dẫn thiết kế kịch bản, chuẩn bị công cụ đo lường (SUS/UEQ-S), tuyển chọn 7 người tham gia và lập cấu trúc ghi chép (Session Notes) cho Usability Testing."
---

# Hướng Dẫn Kỹ Năng: Usability Testing - Lập Kế Hoạch & Chuẩn Bị (Plan & Prepare)

Kỹ năng này hướng dẫn Agent/Người dùng cách lên kế hoạch, chuẩn bị và thiết lập môi trường kiểm thử trải nghiệm người dùng (Usability Testing) cho hệ thống SUT EShop dựa trên các tiêu chí nghiệp vụ và bài giảng thực hành.

---

## 1. Thiết Kế Kịch Bản Tác Vụ (Task Scenario Design)

Kịch bản usability phải là kịch bản **hướng mục tiêu (goal-oriented)** thay vì một danh sách các bước click chuột cụ thể. Người dùng cần tự mình khám phá giao diện để hoàn thành mục tiêu.

### Ví dụ mẫu kịch bản chuẩn:
> "Bạn hãy tìm mua một sản phẩm quần/áo thời trang bất kỳ có giá dưới 500,000 đ trên trang web EShop, thêm sản phẩm vào giỏ hàng, tiến hành thanh toán và áp dụng một mã giảm giá khả dụng. Hãy thực hiện việc này trong khi liên tục chia sẻ suy nghĩ thành tiếng (think-aloud) về những gì bạn đang thấy và cảm nhận."

---

## 2. Chuẩn Bị Công Cụ Đo Lường (Usability Instruments)

Trước khi tiến hành, Người dùng cần chuẩn bị sẵn hai công cụ chính:

### A. Thang đo khảo sát sau buổi test (Post-Session Questionnaire)
- **SUS (System Usability Scale):** Gồm 10 câu hỏi chuẩn (phổ biến nhất).

### B. Bộ câu hỏi phỏng vấn đào sâu (Probe Questions)
Phỏng vấn nhanh ngay sau khi kết thúc tác vụ để ghi nhận phản hồi định tính:
1. **Clarity (Mức độ rõ ràng):** Giao diện có dễ hiểu không? Có yếu tố nào gây bối rối không?
2. **Error Recovery (Khả năng sửa lỗi):** Khi làm sai hoặc gặp sự cố, bạn có tự khắc phục được không?
3. **Speed (Tốc độ):** Bạn thấy tốc độ phản hồi của hệ thống thế nào?
4. **Trust (Độ tin cậy):** Bạn có cảm thấy an toàn và tin tưởng khi nhập thông tin thanh toán/cá nhân trên hệ thống không?

---

## 3. Tuyển Chọn 7 Người Tham Gia (Participant Recruitment)

- **Số lượng bắt buộc:** Tối thiểu 7 người tham gia thực tế để đảm bảo độ tin cậy.
- **Tiêu chuẩn:**
  - Không thuộc lớp học phần Software Testing này (để tránh thiên vị).
  - Khuyến khích người dùng Non-IT hoặc Non-tester để có phản hồi tự nhiên nhất.
- **Bảo mật:** Số điện thoại hoặc thông tin Zalo/Email của người tham gia trong báo cáo phải được che (mask) 4 chữ số ở giữa (ví dụ: `0912.xxx.567`).

---

## 4. Thực Hiện Phiên Thử Nghiệm Thử (Pilot Session)

- **Mục tiêu:** Chạy thử kịch bản với 1 người (người tham gia số 1) để rà soát xem kịch bản có mập mờ, hệ thống có lỗi chặn luồng (blocker) làm hỏng buổi test, hoặc thời gian chạy có quá dài không.
- **Hành động:** Tinh chỉnh lại kịch bản hoặc chuẩn bị phương án dự phòng (workaround) trước khi chạy chính thức với 6 người còn lại.

---

## 5. Cấu Trúc Ghi Chép Dữ Liệu Sau Mỗi Session (Suggested Session Notes Structure)

> Khi quan sát người dùng thực hiện tác vụ, người dùng thực tế phải ghi chép lại theo cấu trúc sau (không tự bịa kết quả khi thiết kế kế hoạch, phần này chỉ là gợi ý cấu trúc, kết quả thực tế không phải do AI bịa ra):

```markdown
### Buổi test số X (Participant X)
- **Thông tin đối tượng:** [IT / Non-IT | Sinh viên / Người đi làm]
- **Thời gian hoàn thành tác vụ (Time on Task):** [Số phút, giây]
- **Ghi chép hành vi (Think-aloud notes):**
  - [Người dùng tìm kiếm nút A ở đâu...]
  - [Người dùng ngập ngừng ở trường nhập B...]
- **Khó khăn gặp phải (Friction points):**
  - [Khó khăn 1...]
  - [Khó khăn 2...]
- **Điểm đánh giá SUS:** [Nhập điểm SUS theo thang 1-5 sau khi hoàn thành 10 câu hỏi]
- **Kết quả trả lời Probe Questions:**
  - *Clarity:* ...
  - *Error Recovery:* ...
  - *Speed:* ...
  - *Trust:* ...
- **Liên kết bằng chứng:** [Link video ghi hình / Ảnh chụp màn hình nếu có]
```

---

## 6. Hướng Dẫn Cập Nhật Tài Liệu Bàn Giao (Deliverables Update)

Khi hoàn tất giai đoạn Plan & Prepare, Agent cập nhật thông tin vào tài liệu:

### Cập nhật [Usability_Session_Evidence.md](../../../docs/submission/Usability_Session_Evidence.md)
- **Mục 1 (Kịch bản kiểm thử):** Điền kịch bản hướng mục tiêu cụ thể đã thiết kế.
- **Mục 2 (Bảng danh sách 7 người tham gia):** Điền khung sườn cho mục bảng danh sách 7 người dùng (họ tên, đối tượng, SĐT đã che 4 số giữa, phương thức liên lạc, trạng thái buổi test).
- **Mục 3 (Ghi chép quan sát):** Dựng sẵn khung sườn trống cho 7 buổi test theo cấu trúc ở phần 5 để sẵn sàng ghi nhận dữ liệu trong quá trình chạy kiểm thử thực tế.
