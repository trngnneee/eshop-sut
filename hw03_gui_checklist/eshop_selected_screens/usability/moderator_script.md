# Moderator Script — Admin Product Management Flow

**Flow được đánh giá:** Admin Login → Product Management → Add Product → Edit Product → Delete Product
**Thời gian ước tính:** 15–25 phút/phiên (bao gồm task + SUS + probe questions)

---

## Trước khi bắt đầu

- Mở sẵn trình duyệt tại `http://localhost:5174/`
- Đảm bảo backend đang chạy và đã có ít nhất 3 sản phẩm trong DB
- Chuẩn bị giấy/thiết bị để người tham gia điền SUS
- Bật ghi màn hình nếu được phép

---

## [GIAI ĐOẠN 1 — Stage Setting] (~2 phút)

> *Đọc nguyên văn:*

"Xin chào, cảm ơn bạn đã tham gia. Hôm nay chúng tôi đang **kiểm tra hệ thống**, không phải kiểm tra bạn. Bạn không thể làm sai — mọi thao tác của bạn đều giúp chúng tôi cải thiện sản phẩm.

Trong quá trình thực hiện, vui lòng **nói to những gì bạn đang nghĩ** — ví dụ 'Tôi đang tìm nút này', 'Tôi không chắc phải làm gì tiếp theo'. Không cần giải thích nhiều, chỉ cần nói ra những gì xuất hiện trong đầu.

Tôi sẽ ngồi quan sát và ghi chú, có thể không trả lời câu hỏi trong lúc bạn làm task — nhưng tôi sẽ giải đáp sau khi phiên kết thúc. Bạn có câu hỏi gì trước khi bắt đầu không?"

---

## [GIAI ĐOẠN 2 — Task Scenario] (~10–15 phút)

> *Đọc nguyên văn (chọn 1 phiên bản đã thống nhất):*

**Phiên bản A:**
> "EShop cần cập nhật kho hàng. Bạn là người quản trị — hãy đăng nhập và thêm một sản phẩm mới bất kỳ (tên, giá, danh mục tự chọn). Sau đó cập nhật lại giá của sản phẩm vừa tạo, rồi xóa nó khỏi danh sách vì hàng hết."

> ⚠️ **Lưu ý cho moderator:**
> - **KHÔNG** gợi ý bất kỳ bước thao tác cụ thể nào
> - **KHÔNG** nói "Bấm vào đây" hay "Tìm mục Sản phẩm"
> - Chỉ được nói: *"Bạn sẽ làm gì tiếp theo?"* nếu người dùng ngừng hoàn toàn quá 60 giây
> - Ghi chép: thời gian, điểm dừng, lời nói, lỗi xảy ra

**Ghi chép trong phiên:**

| Thời gian | Quan sát / Lời nói think-aloud | Loại (friction/error/hesitation/quote) |
|---|---|---|
| | | |
| | | |
| | | |

**Task outcome:**
- [ ] Hoàn thành không cần hỗ trợ
- [ ] Hoàn thành có do dự
- [ ] Hoàn thành nhờ hỗ trợ moderator (ghi rõ lúc nào / vì sao)
- [ ] Bỏ cuộc (ghi rõ bước nào / vì sao)

---

## [GIAI ĐOẠN 3 — SUS] (~3 phút)

> *Đưa cho người tham gia tờ câu hỏi SUS và nói:*

"Bây giờ tôi sẽ nhờ bạn trả lời 10 câu hỏi ngắn về trải nghiệm vừa rồi. Không có câu trả lời đúng sai. Thang điểm từ 1 (hoàn toàn không đồng ý) đến 5 (hoàn toàn đồng ý)."

**Ghi lại 10 đáp án:** `Q1:__ Q2:__ Q3:__ Q4:__ Q5:__ Q6:__ Q7:__ Q8:__ Q9:__ Q10:__`

---

## [GIAI ĐOẠN 4 — Probe Questions] (~5 phút)

> *Hỏi lần lượt, ghi lại câu trả lời:*

1. **Clarity:** "Có thời điểm nào bạn không biết mình phải làm gì tiếp theo không? Cụ thể là ở đâu trong quy trình?"

2. **Error recovery:** "Bạn có gặp lỗi hoặc thao tác nhầm không? Bạn đã xử lý như thế nào?"

3. **Speed:** "Quy trình thêm/sửa/xóa sản phẩm có nhanh hơn hay chậm hơn bạn mong đợi? Tại sao?"

4. **Trust:** "Khi bấm nút Xóa sản phẩm, bạn cảm thấy thế nào? Có lo lắng xóa nhầm không?"

5. **Open:** "Điều gì trong giao diện Admin khiến bạn bực bội nhất? Điều gì bạn thích nhất?"

---

## Kết thúc phiên

> *Nói với người tham gia:*

"Cảm ơn bạn rất nhiều! Những phản hồi của bạn rất có giá trị. Nếu có câu hỏi gì về hệ thống, tôi có thể giải đáp bây giờ."

---

## Sau phiên (dành cho moderator)

- [ ] Điền session notes vào `session_notes_P[số].md` ngay sau khi kết thúc
- [ ] Lưu file ghi màn hình/âm thanh (nếu có)
- [ ] Tính SUS score tạm thời bằng `scripts/score_sus.py`

