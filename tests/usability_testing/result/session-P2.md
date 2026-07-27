# Ghi chú quan sát — Session 2 (P2)

__SESSION 2 (P2)__ — Ngày: 21/07/2026 Bắt đầu: 14:00 Kết thúc: 14:15 Reset DB trước session: ✓

Người tham gia: Võ Ngọc Bích Trâm.

| Bước flow | Hoàn thành? | Thời gian | Lỗi & do dự quan sát được | Trích lời think-aloud đáng chú ý |
|---|---|---|---|---|
| 1. Đăng ký *(O1)* | ✓ | 0:00–3:00 | SĐT `0987****21` lỗi 1 lần → đoán ngay "regex không nhận số 0 đầu", nhập lại dạng bỏ số 0 (`84987****21`) → qua. Mật khẩu lỗi 2 lần, mò ra quy tắc bằng cách thử (BUG-12) | "Hint ghi một đằng, validate một nẻo — cái này chắc regex viết sai." |
| 2. Tìm kiếm *(O6)* | ✓ | 3:00–4:00 | Gõ "tai nghe" ngay từ đầu (từ khoá ngắn), ra kết quả luôn — không chạm BUG-42 | "Search từ khoá ngắn cho chắc." |
| 3. Chi tiết sản phẩm | ✓ | 4:00–4:40 | Không do dự | — |
| 4. Thêm giỏ / Giỏ hàng *(O2)* | ✓ | 4:40–5:40 | Bấm lần 1 không phản hồi → mở giỏ thấy trống (BUG-17) → quay lại bấm lần 2 → có | "Click đầu bị nuốt luôn kìa. Không toast, không badge — người thường sao biết được." |
| 5. Coupon + Checkout | ✓ | 5:40–8:10 | Nhập SAVE10 mượt; nhăn mặt với alert() native (BUG-44) | "2026 rồi mà còn alert()..." |
| 6. Lịch sử đơn hàng | ✓ | 8:10–9:40 | Nhận ra ngay giỏ không reset (BUG-20), gọi đích danh là bug; kiểm tra đơn trong Lịch sử | "Giỏ không clear sau order — bug rõ ràng. Nhưng đơn có trong history nên ổn." |

**Ghi chú probe (C1, C2, E1, E2, S1, T1, T2):**

- **C1:** Chọn từ khoá ngắn vì "search mấy trang nhỏ thường match kiểu chứa chuỗi, gõ dài dễ trớt quớt."
- **C2:** Biết hàng vào giỏ nhờ tự mở giỏ; khẳng định "app không có bất kỳ tín hiệu nào" (đúng BUG-16).
- **E1:** Kể lại mạch lạc cả 2 lỗi form; tự sửa nhanh nhưng nhấn mạnh "mình sửa được vì mình biết code, người khác thì chịu."
- **E2:** Chiến lược khi bất ngờ: "kiểm tra lại state — mở giỏ, mở history, chứ không bấm lặp."
- **S1:** Tổng thể nhanh (15 phút) nhưng "đăng ký chiếm 1/5 buổi là quá nhiều cho một form."
- **T1:** Tin 100% sau khi thấy history, "nhưng chỉ vì mình chủ động đi kiểm tra."
- **T2:** "Không dám nhập thẻ thật — validation lỗi kiểu này thì backend chưa chắc ổn."

**3 điều nổi bật nhất của session này:**

1. Participant rành kỹ thuật vượt mọi chướng ngại nhanh, nhưng chính bạn ấy chỉ ra: tốc độ đó đến từ kiến thức lập trình, không phải từ thiết kế tốt.

2. Xác nhận sạch BUG-17 bằng quan sát trực tiếp: click đầu tiên chắc chắn bị nuốt (giỏ trống sau click 1).

3. Niềm tin vào hệ thống thấp một cách có ý thức — điểm SUS câu 9 cao (thao tác tự tin) nhưng trust khi phỏng vấn lại thấp; hai thứ này cần tách bạch khi viết findings.
