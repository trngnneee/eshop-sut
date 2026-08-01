---
name: usability_testing_analysis
description: "Hướng dẫn xử lý dữ liệu, tính điểm thang đo (SUS/UEQ-S), phân tích tổng hợp định tính và đồng bộ hóa báo cáo Usability Testing."
---

# Hướng Dẫn Kỹ Năng: Usability Testing - Phân Tích & Báo Cáo (Analyse & Report)

Kỹ năng này hướng dẫn Agent/Người dùng cách xử lý các dữ liệu thu thập được sau 7 phiên kiểm thử trải nghiệm người dùng, tính điểm số khảo sát, phân loại lỗi theo mức độ nghiêm trọng và cập nhật đồng bộ các tài liệu bàn giao.

---

## 1. Công Thức Tính Điểm Thang Đo (SUS)

### A. Cách tính điểm System Usability Scale (SUS)
Thang đo SUS gồm 10 câu hỏi với điểm số từ 1 (Rất không đồng ý) đến 5 (Rất đồng ý).
- **Với các câu số lẻ (1, 3, 5, 7, 9):** `Điểm quy đổi = Trả lời - 1`
- **Với các câu số chẵn (2, 4, 6, 8, 10):** `Điểm quy đổi = 5 - Trả lời`
- **Điểm SUS của 1 người dùng:** `SUS_Score = (Tổng điểm quy đổi của 10 câu) * 2.5` (Giá trị nằm trong khoảng từ 0 đến 100).
- **Xếp hạng điểm trung bình hệ thống (SUS Score Interpretation):**
  - `SUS > 80.3`: Excellent (Hệ thống rất tốt, dễ sử dụng).
  - `68 <= SUS <= 80.3`: Good (Hệ thống tốt, người dùng hài lòng).
  - `51 <= SUS < 68`: OK (Hệ thống ở mức trung bình, cần cải tiến).
  - `SUS < 51`: Poor (Hệ thống kém, khó sử dụng).

---

## 2. Tổng Hợp & Phân Tích Trải Nghiệm (Qualitative Synthesis)

- Gom nhóm các ghi chép quan sát từ 7 buổi test lại với nhau.
- Tìm kiếm các **điểm nghẽn phổ biến (friction points)** - nơi nhiều người dùng ngập ngừng, thực hiện sai thao tác hoặc biểu thị sự bối rối/ức chế.
- Phân biệt giữa **lỗi hệ thống (systemic usability bugs)** ảnh hưởng đến hầu hết người dùng và các phản hồi cá nhân (personal preferences) mang tính chủ quan.

---

## 3. Phân Loại Lỗi Theo Mức Độ Nghiêm Trọng (Severity)

Phân loại các vấn đề usability phát hiện được để ưu tiên khắc phục:
1. **Blocker (Lỗi chặn dòng tác vụ):** Người dùng hoàn toàn không thể hoàn thành mục tiêu (ví dụ: không thể tìm thấy nút Checkout, hoặc nút Áp dụng mã giảm giá bị lỗi làm đứng trang).
2. **Major (Lỗi lớn gây khó khăn lớn):** Người dùng vẫn có thể hoàn thành mục tiêu nhưng mất rất nhiều thời gian, loay hoay nhiều bước hoặc cần sự hướng dẫn (ví dụ: nút tăng giảm số lượng quá nhỏ khó bấm).
3. **Minor (Lỗi nhỏ / thẩm mỹ):** Người dùng hoàn thành nhanh nhưng phàn hồi về màu sắc, căn lề, hoặc kích thước chữ (ví dụ: phông chữ chói mắt).

---

## 4. Hướng Dẫn Cập Nhật Đồng Bộ Các Tài Liệu Bàn Giao (Deliverables Sync)

Khi đã phân tích xong dữ liệu, Agent cập nhật kết quả vào các tệp bàn giao sau:

### 1. Cập nhật [Usability_Session_Evidence.md](../../../docs/submission/Usability_Session_Evidence.md)
- **Mục 3 (Ghi chép quan sát):** Điền các quan sát thực tế thu thập được cho từng buổi test từ 1 đến 7.
- **Mục 4 (Kết quả thang đo):** Điền bảng tổng hợp điểm quy đổi SUS của 7 người tham gia và tính điểm trung bình.
- **Mục 5 (Xếp hạng độ nghiêm trọng):** Liệt kê các lỗi Blockers, Major, và Minor phát hiện được sau khi tổng hợp.

### 2. Cập nhật [Bug_Report.md](../../../docs/submission/Bug_Report.md)
Log các lỗi Usability phát hiện được thành các mã lỗi `BUG-XX` (sau các lỗi GUI đã log trước đó).
Mỗi bug cần ghi rõ:
- Mô tả hành vi bối rối của người dùng.
- Các bước tái hiện.
- Kết quả thực tế vs. Kết quả mong đợi.
- Độ nghiêm trọng (Severity: Blocker / Major / Minor).
- Link GitHub Issue tương ứng (Place holder).
- Ảnh chụp màn hình lỗi có chèn watermark email sinh viên (Place holder).

### 3. Cập nhật [Main_Report.md](../../../docs/submission/Main_Report.md)
- **Mục 2.2 (Kịch bản nhiệm vụ):** Ghi rõ kịch bản đã giao cho người dùng.
- **Mục 2.3 (Nhận xét định lượng):** Ghi nhận điểm SUS trung bình và đánh giá hệ thống thuộc mức độ nào (Excellent, Good, OK, Poor).
- **Mục 2.4 (Phân tích định tính):** Mô tả tóm tắt các điểm nghẽn, và phân loại lỗi usability theo mức độ nghiêm trọng.

### 4. Cập nhật [README.md](../../../docs/submission/README.md)
- Cập nhật số lỗi Usability phát hiện được vào mục 2 (Báo cáo tóm tắt).
- Điền điểm tự đánh giá cho Task 2 tại Bảng tự đánh giá.
