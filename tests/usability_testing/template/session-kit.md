# Session Kit — bộ tài liệu điều phối session

---

## 1. Kịch bản mở đầu của moderator (đọc NGUYÊN VĂN, mọi session như nhau)

> Cảm ơn bạn đã dành thời gian giúp mình hôm nay. Mình đang làm bài tập môn kiểm thử phần mềm: **đánh giá một trang web mua sắm, chứ không đánh giá bạn** — bạn không thể làm sai, và mọi chỗ bạn thấy vướng đều là thông tin quý cho mình.
>
> Trong lúc làm, bạn hãy **nói to suy nghĩ của mình** — bất kể bạn đang nhìn gì, định làm gì, thắc mắc gì. Ví dụ như thế này: *"Mình đang tìm chỗ để xem giá... ủa, sao bấm rồi mà không thấy gì đổi nhỉ?"* — cứ tự nhiên như vậy.
>
> Mình sẽ ngồi quan sát và ghi chú, và sẽ **không hướng dẫn hay trả lời trong lúc bạn làm** — không phải mình khó tính đâu, mà vì mình cần thấy trải nghiệm thật của bạn. Bạn có thể dừng bất cứ lúc nào, không cần lý do.
>
> Cuối cùng: để phục vụ bài tập, **mình xin phép ghi lại màn hình và âm thanh** của buổi này — tư liệu chỉ dùng cho môn học. Bạn đồng ý chứ?

## 2. Dòng consent

> Tôi đồng ý tham gia buổi đánh giá trải nghiệm này và đồng ý cho ghi lại màn hình cùng âm thanh của buổi làm việc, với điều kiện tư liệu chỉ được dùng cho mục đích học tập của môn học.
>
> Họ tên: ______________________  Ngày: ____ / ____ / ______

## 3. Template ghi chú quan sát (1 trang A4 / session)

---

__SESSION ___ (P__)__ — Ngày: ______ Bắt đầu: ______ Kết thúc: ______ Reset DB trước session: ☐

| Bước flow | Hoàn thành? | Thời gian | Lỗi & do dự quan sát được | Trích lời think-aloud đáng chú ý |
|---|---|---|---|---|
| 1. Đăng ký *(O1)* | ☐ ✓ ☐ trợ giúp ☐ thất bại | | | |
| 2. Tìm kiếm *(O6)* | ☐ ✓ ☐ trợ giúp ☐ thất bại | | | |
| 3. Chi tiết sản phẩm | ☐ ✓ ☐ trợ giúp ☐ thất bại | | | |
| 4. Thêm giỏ / Giỏ hàng *(O2)* | ☐ ✓ ☐ trợ giúp ☐ thất bại | | | |
| 5. Coupon + Checkout | ☐ ✓ ☐ trợ giúp ☐ thất bại | | | |
| 6. Lịch sử đơn hàng | ☐ ✓ ☐ trợ giúp ☐ thất bại | | | |

**Ghi chú probe (C1, C2, E1, E2, S1, T1, T2):**

---

---

**3 điều nổi bật nhất của session này:**

1. 

   ---

2. 

   ---

3. 

   ---

---

*Quy ước: "trợ giúp" = mình phải can thiệp theo quy tắc mục 4; ghi rõ đã nói gì. Cột thời gian ghi phút:giây tương đối từ lúc bắt đầu task (đối chiếu lại recording khi gõ note).*

## 4. Cheat-sheet giữ trung lập

Khi participant hỏi/cầu cứu, chọn 1 trong 5 câu (không thêm thông tin nào khác):

1. "Bạn nghĩ nó **nên** hoạt động thế nào?"
2. "Bạn đang mong đợi điều gì xảy ra?"
3. "Cứ làm theo cách bạn thấy hợp lý nhất."
4. "Không có đúng sai gì đâu — bạn cứ thử theo cách của bạn."
5. "Câu này hay lắm — cho mình khất đến cuối buổi trả lời nhé."

**Quy tắc can thiệp (duy nhất):** chỉ can thiệp khi participant **kẹt hẳn quá 2 phút** — tức đã ngừng thử cách mới hoặc lặp lại cùng một thao tác thất bại, và đã nhận đủ câu trung lập mà không nhúc nhích. Khi can thiệp: đưa **gợi ý nhỏ nhất có thể** để vượt đúng chỗ kẹt (không giải thích thêm), đánh dấu bước đó là "trợ giúp" và ghi nguyên văn gợi ý đã đưa. Participant kẹt **chính là dữ liệu** — điểm kẹt dự báo trước: đăng ký (BUG-11/12), thêm giỏ (BUG-16/17).

## 5. Checklist trước mỗi session (logistics)

- ☐ Reset `database.sqlite` về seed, restart backend, mở sẵn `localhost:5173`
- ☐ Đăng xuất session cũ / xoá localStorage của lần trước
- ☐ Bật thử ghi màn hình + mic 10 giây, kiểm tra file lưu được
- ☐ Kit giấy: script mở đầu, consent, template ghi chú, phiếu SUS, kịch bản tình huống
- ☐ Sau session: lưu recording thành `P<n>_<yyyy-mm-dd>.mp4`, gõ note thành `session-P<n>.md` trong vòng 15 phút
