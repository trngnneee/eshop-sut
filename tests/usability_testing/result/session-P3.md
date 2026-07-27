# Ghi chú quan sát — Session 3 (P3)

__SESSION 3 (P3)__ — Ngày: 22/07/2026 Bắt đầu: 09:30 Kết thúc: 09:55 Reset DB trước session: ✓

Người tham gia: Phan Quốc Thịnh.

| Bước flow | Hoàn thành? | Thời gian | Lỗi & do dự quan sát được | Trích lời think-aloud đáng chú ý |
|---|---|---|---|---|
| 1. Đăng ký *(O1)* | ☐ trợ giúp | 0:00–9:00 | SĐT `0912****58` lỗi 3 lần (nhập nguyên số, `+84` có khoảng trắng, gõ lại y nguyên — BUG-11); mật khẩu lỗi 4 lần (BUG-12). Kẹt hẳn >2 phút, lặp lại cùng thao tác dù đã nhận 2 câu trung lập → can thiệp tối thiểu: *"Thử bỏ số 0 ở đầu số điện thoại xem sao."* | "Mình nhập đúng số của mình mà? Cái này nó khó quá..." |
| 2. Tìm kiếm *(O6)* | ✓ | 9:00–12:00 | Gõ "tai nghe chống ồn" → trang trống (BUG-42) → tưởng lỗi mạng, bấm tìm lại y nguyên lần nữa; sau đó xoá dần từ khoá còn "tai nghe" → ra | "Sao không có gì hết vậy? Chắc mạng lỗi... để mình bấm lại." |
| 3. Chi tiết sản phẩm | ✓ | 12:00–13:30 | Đọc kỹ mô tả, đối chiếu giá chậm nhưng chắc | "Chống ồn chủ động — đúng loại em mình dặn." |
| 4. Thêm giỏ / Giỏ hàng *(O2)* | ✓ | 13:30–17:00 | Bấm 3 lần liên tiếp vì không thấy phản hồi (BUG-16/17) → giỏ ra **2 dòng trùng** (BUG-47); hoảng, loay hoay ~1 phút tìm cách xoá bớt 1 dòng | "Chết rồi, sao thành 2 cái? Mình đâu có mua 2 cái đâu!" |
| 5. Coupon + Checkout | ✓ | 17:00–21:00 | Tìm ô nhập mã khá lâu (~1 phút); nhập SAVE10 thành công, không tự kiểm tra số tiền giảm | "Cái ô này hả? Nó trừ chưa ta?" |
| 6. Lịch sử đơn hàng | ✓ | 21:00–24:00 | Không tin đơn thành công vì giỏ vẫn còn hàng (BUG-20); hỏi moderator → đáp câu trung lập #2; cuối cùng tự lần ra mục Đơn hàng | "Đặt rồi mà sao trong giỏ vẫn còn? Vậy là được hay chưa được?" |

**Ghi chú probe (C1, C2, E1, E2, S1, T1, T2):**

- **C1:** "Mình gõ nguyên cụm trong tình huống" — kỳ vọng máy hiểu như người. ⤷ Về trang trống: "mình tưởng nó bị đứng, đâu có chữ nào nói là không tìm thấy."
- **C2:** Chỉ biết hàng đã vào giỏ khi thấy 2 dòng trùng — tức là biết qua *hậu quả của lỗi*, không qua feedback.
- **E1:** "Nó cứ báo sai mà không nói sai chỗ nào, mình muốn bỏ cuộc rồi đó." ⤷ Thông báo lỗi không giúp sửa được ngay — phải có gợi ý mới qua.
- **E2:** Khi bất ngờ: lặp lại đúng thao tác cũ ("bấm lại thử"), sau đó hỏi người bên cạnh.
- **S1:** "Chậm hơn mấy lần mua chỗ khác nhiều" — tốn nhất là đoạn tạo tài khoản.
- **T1:** Chỉ tin ~50%; "thấy trong Đơn hàng thì chắc là rồi, mà cái giỏ còn đồ làm mình cứ lo lo."
- **T2:** "Tiền thật thì mình không dám đâu — nó cứ trục trặc vầy lỡ trừ tiền 2 lần thì sao."

**3 điều nổi bật nhất của session này:**

1. Ca trợ giúp đầu tiên: cụm BUG-11/12 chặn hẳn participant — 9 phút và 7 lần submit thất bại cho một form đăng ký.

2. Tái hiện trọn chuỗi BUG-16 → 17 → 47: không feedback → bấm lặp → hàng trùng → hoảng loạn xoá — bằng chứng mạnh nhất cho O2 đến giờ.

3. Mô hình tâm lý "trang trống = máy đứng/lỗi mạng" trước BUG-42: người dùng không hề nghĩ đó là kết quả tìm kiếm rỗng.
