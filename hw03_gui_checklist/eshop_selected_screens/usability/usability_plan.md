# Usability Test Plan
## EShop Admin — Quản lý Sản phẩm

| Thông tin | Chi tiết |
|---|---|
| **Flow được đánh giá** | Admin Login → Product Management → Add Product → Edit Product → Delete Product |
| **Phương pháp** | Moderated usability evaluation |
| **Thang đo** | SUS (System Usability Scale) |
| **Số người tham gia** | 7 người |
| **Thời gian/phiên** | 1-2 phút |
| **Môi trường** | http://localhost:5174/ (EShop Admin) |

---

## 1. Objectives (Mục tiêu đánh giá)

1. **Clarity (Rõ ràng):** Người dùng có hiểu ngay luồng thao tác quản lý sản phẩm (thêm, sửa, xóa) mà không cần hướng dẫn thêm không?
2. **Efficiency (Hiệu quả):** Người dùng mất bao nhiêu bước/thời gian để hoàn thành một tác vụ thêm mới sản phẩm từ khi đăng nhập?
3. **Error recovery (Phục hồi lỗi):** Khi gặp lỗi form (ví dụ: bỏ trống trường bắt buộc), người dùng có tự xác định và sửa được không?
4. **Trust (Tin tưởng):** Người dùng cảm thấy thế nào khi thực hiện thao tác xóa sản phẩm — họ có tin rằng hành động của mình không gây hậu quả ngoài ý muốn không?

---

## 2. Task Scenario

> *Đọc nguyên văn cho người tham gia — không thêm gợi ý hay hướng dẫn từng bước.*

**"EShop cần cập nhật kho hàng. Bạn là người quản trị — hãy đăng nhập và thêm một sản phẩm mới bất kỳ (tên, giá, danh mục tự chọn). Sau đó cập nhật lại giá của sản phẩm vừa tạo, rồi xóa nó khỏi danh sách vì hàng hết."**

**Điều kiện hoàn thành task:**
- Đăng nhập Admin thành công
- Điều hướng được đến màn hình quản lý sản phẩm
- Thêm sản phẩm mới thành công (có trong danh sách)
- Sửa thông tin sản phẩm vừa tạo (ít nhất 1 trường)
- Xóa sản phẩm vừa tạo khỏi danh sách

---

## 3. Thang đo — SUS (System Usability Scale)

Sử dụng **SUS** (10 câu, thang Likert 1–5). Phù hợp với flow quản trị ngắn, cho ra điểm 0–100 để so sánh benchmark:
- > 68: Trên trung bình
- ≥ 80.3: Xuất sắc (Excellent)
- < 50: Kém (Poor)

**Phiếu SUS (phát cho người tham gia sau task):**

| # | Câu hỏi | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 1 | Tôi nghĩ mình sẽ muốn sử dụng hệ thống này thường xuyên. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Tôi thấy hệ thống này phức tạp một cách không cần thiết. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Tôi thấy hệ thống này dễ sử dụng. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Tôi nghĩ mình sẽ cần hỗ trợ của chuyên gia kỹ thuật để sử dụng hệ thống này. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Tôi thấy các chức năng trong hệ thống được tích hợp tốt với nhau. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Tôi thấy có quá nhiều sự mâu thuẫn trong hệ thống này. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Tôi hình dung hầu hết mọi người đều có thể học cách sử dụng hệ thống này rất nhanh. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Tôi thấy hệ thống này rất cồng kềnh khi sử dụng. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Tôi cảm thấy rất tự tin khi sử dụng hệ thống này. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Tôi cần học rất nhiều thứ trước khi bắt đầu sử dụng hệ thống này. | ☐ | ☐ | ☐ | ☐ | ☐ |

*1 = Hoàn toàn không đồng ý → 5 = Hoàn toàn đồng ý*

---

## 4. Probe Questions (Câu hỏi sau SUS)

Hỏi sau khi người tham gia hoàn thành phiếu SUS. Ghi lại câu trả lời vào session notes.

| Chủ đề | Câu hỏi |
|---|---|
| **Clarity** | "Có thời điểm nào bạn không biết mình phải làm gì tiếp theo không? Cụ thể là ở đâu trong quy trình?" |
| **Error recovery** | "Bạn có gặp lỗi hoặc thao tác nhầm không? Bạn đã xử lý như thế nào?" |
| **Speed** | "Quy trình thêm/sửa/xóa sản phẩm có nhanh hơn hay chậm hơn bạn mong đợi? Tại sao?" |
| **Trust** | "Khi bấm nút Xóa sản phẩm, bạn cảm thấy thế nào? Có lo lắng xóa nhầm không?" |
| **Open** | "Điều gì trong giao diện Admin khiến bạn bực bội nhất? Điều gì bạn thích nhất?" |

---

## 5. Moderator Script (Tóm tắt)

### Stage-setting (đọc nguyên văn):
> "Xin chào, cảm ơn bạn đã tham gia. Hôm nay chúng tôi đang **kiểm tra hệ thống**, không phải kiểm tra bạn. Bạn không thể làm sai. Vui lòng **nói to những gì bạn đang nghĩ** trong quá trình thực hiện. Tôi sẽ ngồi quan sát và không trả lời câu hỏi trong lúc bạn làm task."

### Quy trình một phiên:
1. Stage-setting (~2 phút)
2. Đọc task scenario — người tham gia thực hiện (~10–15 phút)
3. Phiếu SUS (~3 phút)
4. Probe questions (~5 phút)

### Nguyên tắc quan sát:
- Không gợi ý bất kỳ bước cụ thể nào
- Chỉ được hỏi: *"Bạn đang nghĩ gì vậy?"* hoặc *"Bạn sẽ làm gì tiếp theo?"*
- Can thiệp hỗ trợ chỉ khi người dùng ngừng hoàn toàn > 60 giây (ghi rõ lý do)

---

## 6. Participants (Thông tin người tham gia)

> **Yêu cầu tuyển chọn:**
> - 7 người thật, bên ngoài lớp học
> - Có thông tin liên hệ xác minh được (Zalo/email/SĐT — che 4 số giữa)
> - Ưu tiên người không có nền tảng IT để đánh giá tính dễ dùng thực tế
> - Điền đầy đủ vào `participant_list.csv`

| # | Mã | Tuổi | Nghề nghiệp | IT background | Liên hệ (masked) | Ngày phiên |
|---|---|---|---|---|---|---|
| 1 | P01 | | | | | |
| 2 | P02 | | | | | |
| 3 | P03 | | | | | |
| 4 | P04 | | | | | |
| 5 | P05 | | | | | |
| 6 | P06 | | | | | |
| 7 | P07 | | | | | |

---

## 7. Pilot Session

Chạy **1 phiên thử (pilot)** trước 7 phiên chính thức. Ghi chú kết quả pilot:

| Hạng mục kiểm tra | Kết quả / Điều chỉnh |
|---|---|
| Scenario có rõ ràng không? | |
| Flow có bước nào bị hỏng (broken step)? | |
| Thời gian thực tế một phiên? | |
| Probe questions có cần chỉnh sửa không? | |

---

## 8. Session Notes Template

Ghi chép từng phiên vào file riêng: `session_notes_P[số].md` (dùng `session_notes_template.md` làm mẫu).

**Ví dụ:** `session_notes_P01.md`, `session_notes_P02.md`, ..., `session_notes_P07.md`

---

## 9. Scoring & Analysis Plan

### SUS Scoring (sau khi có đủ 7 phiên):
```bash
python scripts/score_sus.py
```

Đầu vào: 10 đáp án thô Q1–Q10 của mỗi người tham gia
Đầu ra: Điểm SUS từng người + điểm trung bình + benchmark

### Analysis:
1. **Cluster pain points** từ 7 session notes theo chủ đề
2. **Phân loại:** Lỗi hệ thống (bug) vs. Vấn đề thiết kế (design issue)
3. **Xếp mức độ nghiêm trọng:** Blocker > Major > Minor
4. **Viết bug report** cho các lỗi thực sự phát hiện trong phiên (nếu có)

