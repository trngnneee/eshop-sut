# Ghi chú quan sát — Session 4 (P4)

__SESSION 4 (P4)__ — Ngày: 22/07/2026 Bắt đầu: 15:00 Kết thúc: 15:18 Reset DB trước session: ✓

Người tham gia: Nguyễn Thanh Gia Bảo.

| Bước flow | Hoàn thành? | Thời gian | Lỗi & do dự quan sát được | Trích lời think-aloud đáng chú ý |
|---|---|---|---|---|
| 1. Đăng ký *(O1)* | ✓ | 0:00–5:00 | SĐT `0358****39` thử 3 định dạng (`0358****39`, `+84358****39`, `358****39`) mới qua (BUG-11); mật khẩu lỗi 2 lần (BUG-12). Phàn nàn thông báo lỗi chung chung | "Lỗi thì phải nói rõ *sai gì* chứ, đỏ lòm mà không chỉ chỗ." |
| 2. Tìm kiếm *(O6)* | ✓ | 5:00–6:00 | **Không dùng ô tìm kiếm** — lướt danh sách 5 sản phẩm ở trang chủ, nhận diện bằng mắt | "Có nhiêu đây món, lướt còn nhanh hơn gõ." |
| 3. Chi tiết sản phẩm | ✓ | 6:00–7:00 | Soi ảnh placeholder, đối chiếu giá nhanh | "Ảnh placeholder thế này nhìn hơi... demo." |
| 4. Thêm giỏ / Giỏ hàng *(O2)* | ✓ | 7:00–8:30 | Bấm lần 1 → chờ ~5 giây không thấy gì → mở giỏ thấy **trống** (BUG-17) → quay lại trang sản phẩm bấm lần 2 → có | "Trống trơn? Rõ ràng mình bấm rồi mà. Chơi vậy ai chơi." |
| 5. Coupon + Checkout | ✓ | 8:30–11:30 | Nhập SAVE10 ổn; chê popup alert() (BUG-44) | "Alert mặc định nhìn như lỗi hệ thống, không phải xác nhận." |
| 6. Lịch sử đơn hàng | ✓ | 11:30–13:00 | Thấy giỏ chưa reset (BUG-20), tự suy ra cần đối chiếu Lịch sử đơn; xác nhận đơn có, tổng 5.400.000₫ | "Giỏ còn nguyên — thôi tin cái history vậy." |

**Ghi chú probe (C1, C2, E1, E2, S1, T1, T2):**

- **C1:** Duyệt thay vì tìm — "catalog bé xíu, mắt scan nhanh hơn". Nói thêm: nếu nhiều hàng mới cần search.
- **C2:** Chỉ tin hàng vào giỏ sau khi *nhìn thấy trong giỏ*; "nút bấm phải đổi trạng thái hoặc có toast, đây là feedback 101."
- **E1:** Tự sửa được nhờ thử nhiều định dạng, nhưng đánh giá form "đánh đố"; nhấn mạnh lỗi hiển thị không actionable.
- **E2:** Khi bất ngờ: nghi bản thân trước ("chắc mình bấm hụt"), rồi mới nghi hệ thống sau lần lặp thứ hai.
- **S1:** Tương đương các shop nhỏ khác; chậm nhất ở đăng ký, "checkout thì lại nhanh bất ngờ."
- **T1:** Tin ~90% nhờ Lịch sử đơn; trừ 10% vì "giỏ còn hàng là dấu hiệu backend làm ẩu."
- **T2:** "Nhập thông tin thì được, nhưng tới bước thẻ thật chắc mình dừng — UI cẩu thả làm mình nghi phần bảo mật cũng cẩu thả."

**3 điều nổi bật nhất của session này:**

1. Ca đầu tiên **không dùng tìm kiếm** — dữ liệu O6 dạng đối chứng: với catalog 5 món, duyệt là chiến lược hợp lý và search bị bỏ qua hoàn toàn.

2. Xác nhận độc lập BUG-17 giống P2: giỏ trống sau click đầu, phải click lần 2 — pattern đã lặp ở 4/4 session.

3. Nhận xét "UI cẩu thả → nghi ngờ bảo mật" nối thẳng trục trust: chất lượng feedback bề mặt ảnh hưởng niềm tin giao dịch.
