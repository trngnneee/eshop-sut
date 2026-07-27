# Ghi chú quan sát — Session 7 (P7)

__SESSION 7 (P7)__ — Ngày: 24/07/2026 Bắt đầu: 09:00 Kết thúc: 09:16 Reset DB trước session: ✓

Người tham gia: Nguyễn Thanh Tiến.

| Bước flow | Hoàn thành? | Thời gian | Lỗi & do dự quan sát được | Trích lời think-aloud đáng chú ý |
|---|---|---|---|---|
| 1. Đăng ký *(O1)* | ✓ | 0:00–3:30 | SĐT `0933****77` lỗi 1 lần → bỏ số 0 ngay lần 2 (`933****77` — BUG-11); mật khẩu lỗi 1 lần rồi qua (BUG-12) | "Chắc nó thích kiểu quốc tế, bỏ số 0 thử... à được." |
| 2. Tìm kiếm *(O6)* | ✓ | 3:30–4:15 | Gõ "tai nghe" ngay từ đầu (thói quen từ khoá ngắn từ Shopee) → ra luôn, không chạm BUG-42 | "Gõ ngắn thôi, gõ dài nó kiếm không ra à." |
| 3. Chi tiết sản phẩm | ✓ | 4:15–5:00 | Lướt nhanh, chốt giá 6 triệu trong ngân sách | — |
| 4. Thêm giỏ / Giỏ hàng *(O2)* | ✓ | 5:00–6:15 | Bấm 1 lần → không thấy gì → mở giỏ ngay → **trống** (BUG-17) → quay lại bấm lần 2 → có 1 món | "Ủa? Trống trơn. App gì kỳ. Bấm lại phát nữa." |
| 5. Coupon + Checkout | ✓ | 6:15–8:45 | Nhập SAVE10 mượt, liếc xác nhận −600.000₫ | "Ok trừ rồi, 5 triệu 4." |
| 6. Lịch sử đơn hàng | ✓ | 8:45–10:15 | Thấy giỏ còn hàng (BUG-20) → nhíu mày nhưng tự tin mở mục Đơn hàng đối chiếu → chốt | "Giỏ chưa xoá là do web lười thôi, đơn có trong này là được rồi." |

**Ghi chú probe (C1, C2, E1, E2, S1, T1, T2):**

- **C1:** Chiến lược từ khoá ngắn có chủ đích — "mấy web nhỏ tìm dở lắm, gõ ít chữ cho nó dễ khớp." (né BUG-42 nhờ kinh nghiệm nền, không phải nhờ thiết kế)
- **C2:** Biết hàng vào giỏ *chỉ* nhờ tự mở giỏ; so sánh trực tiếp: "Shopee rung cái giỏ, đổi số — ở đây phải tự đi soi."
- **E1:** Xử lý cả 2 lỗi form trong 1 lần thử lại mỗi lỗi; đoán quy ước ("kiểu quốc tế") thay vì đọc kỹ thông báo.
- **E2:** Khi bất ngờ: kiểm tra hậu quả ngay (mở giỏ) thay vì bấm lặp — hành vi ít rủi ro nhất trong 7 participant.
- **S1:** "Nhanh hơn mình tưởng, chậm mỗi khúc đăng ký" — tổng 16 phút, nhanh thứ nhì sau P2.
- **T1:** Tin ~95% — "đơn nằm trong Đơn hàng là bằng chứng rồi"; giỏ chưa reset bị quy thành lỗi thẩm mỹ, không phải lỗi giao dịch.
- **T2:** "Đặt COD thì đặt, chứ nhập thẻ thì không — web nhỏ mình toàn chọn trả khi nhận."

**3 điều nổi bật nhất của session này:**

1. Session trơn tru nhất (16 phút, 0 trợ giúp) — nhưng độ trơn đến từ *kinh nghiệm nền của participant* (từ khoá ngắn, mở giỏ xác minh), không phải app tốt lên.

2. BUG-17 tái hiện lần thứ 7/7 — click đầu bị nuốt là hành vi chắc chắn, đủ dữ liệu để nâng mức nghiêm trọng khi tổng hợp.

3. Cách diễn giải BUG-20 khoan dung nhất nhóm ("web lười") cho thấy kiểu người dùng đã quen sai sót của web nhỏ — trust không sụp nhưng mặc định né nhập thẻ.
