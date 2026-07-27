# Ghi chú quan sát — Session 6 (P6)

__SESSION 6 (P6)__ — Ngày: 23/07/2026 Bắt đầu: 16:00 Kết thúc: 16:24 Reset DB trước session: ✓

Người tham gia: Trương Lý Khải.

| Bước flow | Hoàn thành? | Thời gian | Lỗi & do dự quan sát được | Trích lời think-aloud đáng chú ý |
|---|---|---|---|---|
| 1. Đăng ký *(O1)* | ☐ trợ giúp | 0:00–8:00 | SĐT `0903****44` lỗi lặp lại: nhập lại **cùng một số** 4 lần, đổi trình duyệt tab (BUG-11); mật khẩu lỗi 2 lần (BUG-12). Kẹt hẳn >2 phút → can thiệp tối thiểu: *"Thử nhập số điện thoại không có số 0 ở đầu xem."* | "Số đúng mà nó cứ báo sai. Hay tại máy?" |
| 2. Tìm kiếm *(O6)* | ✓ | 8:00–10:00 | Gõ "tai nghe chống ồn" → trống (BUG-42) → **bỏ luôn ô tìm kiếm**, quay về trang chủ duyệt danh sách → thấy AirPods | "Tìm không ra thì mình dò tay vậy." |
| 3. Chi tiết sản phẩm | ✓ | 10:00–11:00 | Đọc mô tả, đối chiếu ngân sách | — |
| 4. Thêm giỏ / Giỏ hàng *(O2)* | ✓ *(tạo lỗi trùng, tự phát hiện muộn)* | 11:00–14:00 | Bấm 3 lần vì không thấy phản hồi (BUG-16/17) → giỏ có **2 dòng trùng** (BUG-47) nhưng **không mở giỏ kiểm tra**, đi thẳng tới checkout | "Chắc được rồi, qua bước trả tiền." |
| 5. Coupon + Checkout | ✓ | 14:00–19:00 | Nhập SAVE10 → tổng hiện **10.800.000₫** → giật mình, quay lại giỏ mới thấy 2 dòng → xoá 1 → checkout lại, tổng 5.400.000₫ | "Ủa sao tới 10 triệu 8? Mình mua có một cái mà!" |
| 6. Lịch sử đơn hàng | ✓ | 19:00–21:00 | Thấy giỏ vẫn còn hàng sau checkout (BUG-20) → lo đơn bị "kẹt"; tìm thấy Lịch sử đơn sau ~40 giây dò menu | "Còn trong giỏ tức là chưa mua được à? ... À không, đây rồi, có đơn rồi." |

**Ghi chú probe (C1, C2, E1, E2, S1, T1, T2):**

- **C1:** Từ khoá lấy nguyên từ kịch bản; ⤷ về trang trống: "nghĩ là web không có chức năng tìm, nên mình dò bằng mắt luôn."
- **C2:** Trước checkout **không hề biết** giỏ có gì — chỉ phát hiện qua tổng tiền sai; "may mà mã giảm giá làm mình nhìn kỹ số tiền."
- **E1:** "Bí nhất là số điện thoại — mình đâu nghĩ ra là phải bỏ số 0, ai đời nhập số thiếu số." ⤷ Thông báo lỗi không giúp gì, phải nhờ gợi ý.
- **E2:** Khi bất ngờ: lặp lại thao tác, rồi nghi thiết bị ("hay tại máy"), ít nghi giao diện.
- **S1:** "Chậm, chắc gấp đôi lần mua gần nhất trên Lazada" — tốn nhất ở đăng ký và vụ 2 cái tai nghe.
- **T1:** Tin ~70% sau khi thấy Lịch sử đơn; vẫn định "mai kiểm tra lại xem đơn còn không."
- **T2:** "Nếu là 10 triệu 8 thật mà lỡ bấm thanh toán thì to chuyện — nghĩ tới đó là không dám nhập thẻ."

**3 điều nổi bật nhất của session này:**

1. Kịch bản xấu nhất của O2 đã xảy ra: bấm lặp → hàng trùng → **suýt đặt đơn gấp đôi tiền**; chỉ phát hiện nhờ bước kiểm tra tổng khi áp coupon.

2. Phản ứng mới với BUG-42: từ bỏ hoàn toàn chức năng tìm kiếm (không thử lại từ khoá) — mức mất niềm tin nặng hơn P1/P3/P5.

3. Ca trợ giúp thứ hai, cùng đúng một chỗ với P3 (SĐT bắt đầu bằng 0) — BUG-11 đủ điều kiện gắn severity cao khi tổng hợp findings.
