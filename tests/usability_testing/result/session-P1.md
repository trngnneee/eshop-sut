# Ghi chú quan sát — Session 1 (P1)

__SESSION 1 (P1)__ — Ngày: 21/07/2026 Bắt đầu: 10:00 Kết thúc: 10:19 Reset DB trước session: ✓

Người tham gia: Đặng Đăng Khoa.

> **Session này đồng thời là pilot.** Ngoài việc thu dữ liệu như 6 session sau, buổi này được dùng để kiểm tra kịch bản (goal có rõ không), bộ probe questions và phiếu SUS trước khi chạy P2–P7. Kết luận: không phải sửa gì — participant hiểu goal ngay, không hỏi lại nghĩa, thời lượng 19 phút nằm trong khung dự kiến 15–25 phút. Vì vậy dữ liệu P1 được giữ lại trong phân tích. Hạn chế của pilot gộp: xem `report.md` mục 5 và 10.

| Bước flow | Hoàn thành? | Thời gian | Lỗi & do dự quan sát được | Trích lời think-aloud đáng chú ý |
|---|---|---|---|---|
| 1. Đăng ký *(O1)* | ✓ | 0:00–4:30 | SĐT `0376****49` bị từ chối 2 lần (BUG-11); đọc kỹ thông báo lỗi rồi thử bỏ số 0 đầu → qua. Mật khẩu lỗi 1 lần (BUG-12) | "Số điện thoại mình xài hằng ngày mà, sao lại không hợp lệ?" |
| 2. Tìm kiếm *(O6)* | ✓ | 4:30–6:30 | Gõ "tai nghe chống ồn" → trang trống không một dòng giải thích (BUG-42), khựng ~15 giây; rút gọn còn "tai nghe" → ra kết quả | "Ủa, hết hàng hả? Hay mình gõ sai... thử ngắn hơn xem." |
| 3. Chi tiết sản phẩm | ✓ | 6:30–7:30 | Đối chiếu giá 6.000.000₫ với ngân sách 6–7 triệu, không do dự | "6 triệu, vừa đúng tầm tiền." |
| 4. Thêm giỏ / Giỏ hàng *(O2)* | ✓ | 7:30–9:00 | Bấm "Thêm vào giỏ hàng" lần 1 không thấy phản hồi gì (BUG-16/17), bấm lần 2, rồi chủ động mở giỏ kiểm tra → 1 món | "Bấm rồi mà im re... thôi vô giỏ coi cho chắc." |
| 5. Coupon + Checkout | ✓ | 9:00–12:00 | Tìm thấy ô nhập mã nhanh; kiểm tra thấy −600.000₫, tổng 5.400.000₫ | "Có trừ 600 nghìn nè, ok đúng 10%." |
| 6. Lịch sử đơn hàng | ✓ | 12:00–14:00 | Sau checkout thấy giỏ vẫn còn hàng (BUG-20) → hoang mang, tự vào mục Đơn hàng thấy đơn → yên tâm | "Sao đặt rồi mà giỏ vẫn còn? ... À, trong Đơn hàng có rồi, chắc là được." |

**Ghi chú probe (C1, C2, E1, E2, S1, T1, T2):**

- **C1:** Tìm bằng ô tìm kiếm vì "quen tay như Shopee". ⤷ Khi ra trang trống: "tưởng shop không bán, may mà thử lại từ khoá ngắn — chứ nó phải ghi là không tìm thấy chứ."
- **C2:** Chỉ chắc chắn hàng vào đơn sau khi mở giỏ nhìn tận mắt; "nút bấm xong không nói gì hết."
- **E1:** Đoạn tạo tài khoản "hơi bực" — lỗi số điện thoại "vô lý", nhưng tự đoán được cách sửa nhờ đọc thông báo.
- **E2:** Khi kết quả khác mong đợi thì "thử lại cách khác trước, không được mới hỏi."
- **S1:** Chậm hơn Shopee, tốn thời gian nhất ở đăng ký ("nhập đi nhập lại").
- **T1:** Tin ~80% đơn đã ghi nhận — nhờ thấy trong Lịch sử đơn hàng; giỏ chưa xoá làm "lấn cấn".
- **T2:** Nếu là tiền thật "sẽ hơi ngại" vì trang báo lỗi/xác nhận sơ sài, "nhìn không được chuyên nghiệp."

**3 điều nổi bật nhất của session này:**

1. Tự phục hồi được cả 2 lỗi validation ở Đăng ký nhờ chịu đọc thông báo — nhưng mất 4 phút rưỡi cho một form.

2. Hành vi xác minh giỏ hàng chủ động (mở giỏ đếm món) xuất hiện ngay sau lần bấm không có feedback — đúng kịch bản O2.

3. Giỏ không reset sau checkout (BUG-20) là khoảnh khắc mất niềm tin rõ nhất; Lịch sử đơn hàng là thứ cứu lại niềm tin.
