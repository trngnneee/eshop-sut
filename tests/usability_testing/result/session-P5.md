# Ghi chú quan sát — Session 5 (P5)

__SESSION 5 (P5)__ — Ngày: 23/07/2026 Bắt đầu: 10:00 Kết thúc: 10:22 Reset DB trước session: ✓

Người tham gia: Lê Tuấn Lộc.

| Bước flow | Hoàn thành? | Thời gian | Lỗi & do dự quan sát được | Trích lời think-aloud đáng chú ý |
|---|---|---|---|---|
| 1. Đăng ký *(O1)* | ✓ | 0:00–6:00 | SĐT `0369****05` lỗi 2 lần (BUG-11) → bỏ số 0 (`369****05`) sau khi thử lại; mật khẩu lỗi 3 lần (BUG-12), so hint với thông báo lỗi và bối rối rõ rệt | "Hint bảo một đằng, lỗi báo một nẻo — rốt cuộc nghe bên nào?" |
| 2. Tìm kiếm *(O6)* | ✓ | 6:00–8:30 | Gõ "tai nghe chong on" (không dấu) → trống; gõ lại có dấu "tai nghe chống ồn" → vẫn trống (BUG-42); suýt kết luận không bán → thử lần 3 "tai nghe" → ra | "Chắc ở đây không bán rồi... khoan, thử gõ mỗi 'tai nghe' xem." |
| 3. Chi tiết sản phẩm | ✓ | 8:30–9:30 | Đối chiếu giá và mô tả nhanh | "6 triệu, chống ồn chủ động — chuẩn bài." |
| 4. Thêm giỏ / Giỏ hàng *(O2)* | ✓ | 9:30–11:30 | Bấm 2 lần liền theo phản xạ (quen có toast ở Shopee); mở giỏ kiểm tra → 1 món (click đầu bị nuốt nên 2 click = 1 món — BUG-17 "che" BUG-47) | "Bên Shopee nó hiện cái rẹt, bên này im ru nên mình bấm 2 phát cho chắc." |
| 5. Coupon + Checkout | ✓ | 11:30–15:00 | Nhập SAVE10, chủ động lấy máy tính điện thoại bấm kiểm tra 10% | "600 nghìn, đúng, khớp 10%." |
| 6. Lịch sử đơn hàng | ✓ | 15:00–17:00 | Bối rối vì giỏ còn hàng (BUG-20); vào Lịch sử đơn đối chiếu **tổng 5.400.000₫** rồi mới yên tâm | "Đơn có, số tiền khớp — vậy là xong. Nhưng cái giỏ phải tự xoá chứ?" |

**Ghi chú probe (C1, C2, E1, E2, S1, T1, T2):**

- **C1:** Tìm bằng search vì "quen tay"; ⤷ về 2 lần trang trống: "không có chữ nào nói là không tìm thấy, mình tưởng web lỗi hoặc hết hàng thật."
- **C2:** Biết hàng vào giỏ nhờ mở giỏ đếm; thừa nhận bấm 2 lần là "phản xạ vì app này không nói gì."
- **E1:** Mất nhiều lượt nhất ở mật khẩu; ⤷ dựa vào *thử-sai* chứ không dựa được vào thông báo — "lỗi không chỉ ra ký tự nào không được."
- **E2:** Khi bất ngờ: đổi cách nhập (bỏ dấu, rút gọn) một cách có hệ thống — người dùng thành thạo tự có chiến lược.
- **S1:** "Chậm hơn Shopee kha khá" — nhất là đăng ký và đoạn dò từ khoá.
- **T1:** Tin ~90% nhờ đối chiếu được *số tiền* trong Lịch sử đơn — con số khớp là bằng chứng mạnh nhất với participant.
- **T2:** "Thông tin cá nhân thì tạm, chứ tiền thật thì mình chuyển khoản khi nhận hàng thôi."

**3 điều nổi bật nhất của session này:**

1. BUG-42 suýt gây **bỏ cuộc thật**: 2 lần trang trống liên tiếp làm participant kết luận "không bán" — chỉ thói quen thử-sai cứu lại task.

2. Phát hiện thú vị cho O2: BUG-17 (nuốt click đầu) vô tình *che* BUG-47 — người bấm đúp theo phản xạ Shopee lại ra đúng 1 món.

3. "Con số khớp" trong Lịch sử đơn là tín hiệu trust quyết định với participant này — mạnh hơn mọi thông báo xác nhận.
