# Findings — Tổng hợp phân tích 7 session (GĐ8)

**Dữ liệu nền:** 7/7 hoàn thành flow (2 ca cần trợ giúp, đều ở bước Đăng ký). SUS: mean **53.2**, median 55.0, min 30 (P3) – max 75 (P7), band "OK" — dưới benchmark trung bình 68. Hai điểm SUS thấp nhất (P3: 30, P6: 35) chính là 2 ca cần trợ giúp — điểm số bám sát mức độ vấp ở Đăng ký.

---

## 1. Bảng theme (xếp theo severity đề xuất, nặng → nhẹ)

| ID | Theme | Ai gặp (x/7) | Bước | Bug / Design | Severity | Căn cứ |
|---|---|---|---|---|---|---|
| UF-01 | Validation SĐT từ chối số VN hợp lệ bắt đầu bằng 0 | **7/7** (P1–P7) | Đăng ký | **Bug** (= BUG-11, issue 204) | **Blocker** | 2/7 (P3, P6) kẹt hẳn, chỉ qua nhờ moderator gợi ý — tức nếu không có trợ giúp thì **không hoàn thành task**; 5/7 còn lại đều mất ≥1 lần submit thất bại; chỉ 1/7 (P1) rút được hướng sửa nhờ đọc kỹ thông báo lỗi, 6/7 còn lại qua bằng đoán mò từ kinh nghiệm hoặc trợ giúp |
| UF-02 | Thêm giỏ: không feedback + click đầu bị nuốt | **7/7** | Thêm giỏ | **Bug** (= BUG-16 issue 209, BUG-17 issue 210) | **Major** | 0/7 nhận biết được thành công qua hệ thống; 6/7 phải tự mở giỏ xác minh; 4/7 bấm lặp không kiểm tra giữa chừng (P1, P3, P5, P6) — pattern: 2 click → 1 món (P1, P5), 3 click → 2 dòng trùng (P3, P6), đúng dấu vết BUG-17 nuốt đúng 1 click đầu; là nguồn trực tiếp sinh ra UF-03. Giữ Major, không nâng Blocker: bước này không chặn ai, hậu quả tài chính đã tính riêng ở UF-03 |
| UF-03 | Bấm lặp tạo dòng trùng trong giỏ → suýt trả gấp đôi | **2/7** (P3, P6) | Giỏ → Checkout | **Bug** (= BUG-47, issue 240) | **Major** (nhánh hậu quả tài chính) | P6 đi tới checkout với tổng **10.800.000₫** mà không biết — chỉ phát hiện nhờ nhìn kỹ số tiền khi áp coupon. P3 hoảng, mất ~1 phút xoá dòng trùng. Ghi chú: P5 bấm đúp nhưng ra đúng 1 món vì BUG-17 "che" BUG-47 |
| UF-04 | Quy tắc mật khẩu mâu thuẫn với hint | **7/7** *(đã chốt — xem §4.1)* | Đăng ký | **Bug** (= BUG-12, issue 205) | **Major** | 1–4 lần submit thất bại/người; tất cả vượt qua bằng thử-sai chứ không nhờ thông báo ("Hint bảo một đằng, lỗi báo một nẻo" — P5); góp phần chính vào 4–9 phút/form |
| UF-05 | Tìm kiếm 0 kết quả = trang trống, không một dòng giải thích | **4/7** (P1, P3, P5, P6) *(đã chốt — xem §4.2)* | Tìm kiếm | **Bug** (= BUG-42, issue 235 — FR-24 yêu cầu empty state) | **Major** | Không ai diễn giải đúng là "0 kết quả": P1 tưởng hết hàng, P3 tưởng lỗi mạng (bấm lại y nguyên), P5 **suýt bỏ cuộc** ("chắc không bán"), P6 **bỏ hẳn chức năng tìm kiếm**. Người thoát được là nhờ kinh nghiệm nền (rút gọn từ khoá), không nhờ giao diện |
| UF-06 | Giỏ không reset sau checkout → nghi ngờ đơn chưa thành công | **7/7** nhận thấy: 4/7 bối rối/lo (P1, P3, P5, P6), 2/7 nhận diện là lỗi nhưng bình thản (P2, P4), 1/7 bỏ qua (P7 — "web lười") | Sau checkout | **Bug** (= BUG-20, issue 213) | **Major** (trục trust) | Tự phục hồi được 7/7 nhờ Lịch sử đơn hàng, nhưng đây là khoảnh khắc sụt niềm tin rõ nhất flow: P3 chỉ tin ~50%, P6 lo đơn "kẹt", P1 "lấn cấn". Severity Major vì đánh thẳng vào câu hỏi "giao dịch xong chưa" |
| UF-07 | Thông báo lỗi form không actionable (không chỉ sai gì, sửa thế nào) | **4/7** phàn nàn rõ (P3, P4, P5, P6); P1 ngược lại đọc và tự đoán được | Đăng ký | **Design issue** (chất lượng nội dung message) | **Major** | Là "chất xúc tác" biến UF-01/UF-04 từ phiền toái thành kẹt: 2 ca trợ giúp đều rơi vào nhóm phàn nàn này. Tách khỏi UF-01/04 vì sửa regex xong vẫn phải sửa message |
| UF-08 | Feedback hệ thống dùng `alert()` native, xác nhận giảm giá mờ nhạt | 2/7 chê alert (P2, P4); 1/7 không tự xác nhận được đã trừ tiền (P3) | Checkout | **Design issue** (một phần = BUG-44, issue 237) | **Minor** | Không chặn ai; nhưng P3 rời bước coupon mà không biết mã đã áp chưa ("nó trừ chưa ta?") — với đơn thật đây là rủi ro khiếu nại |
| UF-09 | Ô nhập coupon khó thấy | **1/7** (P3, ~1 phút) | Checkout | Design issue | **Cosmetic** (tín hiệu đơn lẻ) | Chỉ 1 người, tự tìm ra; chưa đủ dữ liệu kết luận — ghi nhận để theo dõi, không đưa khuyến nghị mạnh |

## 2. Vấn đề hệ thống (systemic) — không phải bug đơn lẻ

**SYS-01 — "Chất lượng bề mặt thấp → không dám giao dịch thật": 7/7.**
Khi hỏi trust (T2), cả 7 đều từ chối hoặc dè dặt việc nhập thẻ/tiền thật trên app này, và đều viện dẫn các trục trặc bề mặt làm bằng chứng suy đoán về độ tin cậy phía sau: "validation lỗi kiểu này thì backend chưa chắc ổn" (P2), "UI cẩu thả làm mình nghi phần bảo mật cũng cẩu thả" (P4), "lỡ trừ tiền 2 lần thì sao" (P3), "nghĩ tới [10.8 triệu] là không dám nhập thẻ" (P6), COD-only (P5, P7), "hơi ngại" (P1). Đây là hệ quả cộng dồn của UF-01→08, không sửa được bằng một fix đơn lẻ — thuộc phần khuyến nghị thiết kế, không mở issue bug.

**SYS-02 — Lịch sử đơn hàng là "mỏ neo niềm tin" duy nhất: 7/7.**
Mọi participant chỉ kết luận "đơn đã thành công" sau khi tự thấy đơn trong Lịch sử đơn hàng; P5 cần thêm *con số khớp 5.400.000₫*. Hàm ý thiết kế: màn xác nhận sau checkout (số đơn + tổng tiền + link tới đơn) sẽ thay được hành trình tự đi tìm bằng chứng.

**SYS-03 — App "sống được" nhờ kinh nghiệm nền của người dùng, không nhờ thiết kế.**
Mọi chiến lược thoát kẹt đều import từ nơi khác: từ khoá ngắn "vì web nhỏ tìm dở" (P2, P7), bấm đúp "vì Shopee có toast" (P5), mở giỏ xác minh (6/7), bỏ số 0 "kiểu quốc tế" (P7). Người ít kinh nghiệm nhất (P3) là người kẹt nặng nhất — SUS 30, 25 phút, 1 lần trợ giúp.

## 3. Trả lời 3 mục tiêu nghiên cứu (chỉ từ dữ liệu trên)

**O1 — Tự phục hồi lỗi ở Đăng ký:** Có, nhưng đắt và không nhờ hệ thống. 5/7 tự phục hồi bằng thử-sai (1–3 định dạng SĐT, 1–4 lần mật khẩu), 2/7 cần trợ giúp trực tiếp. Chỉ P1 rút được hướng sửa từ *nội dung* thông báo lỗi; form Đăng ký ngốn 3–9 phút (⅕–⅓ thời lượng session). → Câu trả lời: **khả năng tự phục hồi phụ thuộc kinh nghiệm người dùng, hệ thống gần như không đóng góp**.

**O2 — Nhận biết "đã thêm vào giỏ":** Không ai nhận biết được qua hệ thống (0/7). Hành vi bù đắp: 6/7 mở giỏ xác minh thủ công; 3/7 bấm lặp, sinh 2 ca hàng trùng, 1 ca suýt thanh toán gấp đôi. P6 là counter-example quan trọng: người *không* tự xác minh chính là người suýt mất tiền — tức hậu quả rơi vào nhóm người dùng "tin app" nhất.

**O6 — Tìm kiếm phục vụ mục tiêu mua:** Search chỉ "hoạt động" với người đã biết luật ngầm từ-khoá-ngắn (P2, P7 — học từ nền tảng khác). Người gõ tự nhiên như nói (4/7) rơi vào trang trống và không ai hiểu đúng nghĩa; hậu quả leo thang từ thử lại (P1) → tưởng lỗi mạng (P3) → suýt bỏ cuộc (P5) → bỏ hẳn tính năng (P6). P4 bỏ qua search có chủ đích vì catalog 5 món — lưu ý bối cảnh: catalog nhỏ làm hành vi "duyệt thay tìm" trở nên hợp lý, kết quả O6 sẽ khác với catalog lớn.

## 4. AMBIGUOUS

1. **Số người dính lỗi mật khẩu (UF-04) — chốt 7/7.** Cả 7 session note đều ghi rõ số lần lỗi mật khẩu kèm mã BUG-12 (P1: 1, P2: 2, P3: 4, P4: 2, P5: 3, P6: 2, P7: 1) — riêng P7, dòng ghi chú ghi "mật khẩu lỗi 1 lần rồi qua (BUG-12)", tức đã quy về BUG-12 chứ không phải lỗi khác. `result/README.md` ghi 6/7 là sai và **đã sửa thành 7/7**.
2. **Số người gặp trang trống tìm kiếm (UF-05) — chốt 4/7 (P1, P3, P5, P6).** Con số 5/7 trong README là do đếm đôi P5 (gặp 2 *lần*: không dấu rồi có dấu, nhưng là 1 *người*). Quy ước thống kê: cột "Ai gặp" đếm theo **người**, số lần chỉ ghi trong phần căn cứ. README **đã sửa thành 4/7** kèm chú thích quy ước. P2/P7 né nhờ từ khoá ngắn, P4 không dùng search.
3. **Trạng thái bước 4 của P6 — chốt giữ ✓, quy ước "hoàn thành có lỗi".** Cột "Hoàn thành?" của template đo theo mức *can thiệp* (✓ / trợ giúp / thất bại): P6 tự đi tiếp không cần moderator nên là ✓; hậu quả hàng trùng là **error** thuộc chỉ số lỗi, đã được đếm riêng ở UF-03 (2/7 tạo dòng trùng). Khi lập bảng thống kê theo bước: ghi "✓ (có lỗi)" như chú thích, **không** tính là "thất bại một phần" — tránh một sự kiện bị đếm vào cả hai chỉ số hoàn thành lẫn lỗi.

## 5. Ghi chú cho GĐ9 (bug → GitHub Issues)

Cả 7 bug Task 1 trong bảng (thuộc 6 theme UF-01→06) **đều đã có issue từ Task 1** (204, 209, 210, 240, 205, 235, 213), nên không mở issue trùng.

**Đã thực hiện (27/07/2026):** comment bằng chứng usability (tần suất x/7, trích think-aloud, hậu quả quan sát được, link findings này) vào cả 7 issue + gắn label `usability`; nâng severity **#204 Major → Blocker** và **#240 Minor → Major** (giữ đánh giá gốc Task 1 trong body); **#235 giữ Minor** theo quyết định của người thực hiện dù dữ liệu usability xếp theme UF-05 ở mức Major (4/7 người gặp đều tự thoát được bằng đổi từ khoá). Mọi comment công khai chỉ dùng mã P1–P7, không kèm thông tin cá nhân participant.
