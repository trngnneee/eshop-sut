# Result — dữ liệu thu được từ 7 session

Thư mục này gom toàn bộ kết quả thô của từng participant, điền theo đúng template sẵn có:

- `session-P<n>.md` — ghi chú quan sát (template mục 3 của `../template/session-kit.md`), kèm ghi chú probe (mã câu hỏi theo `../template/probe-questions.md`) và 3 điều nổi bật.
- `sus-P<n>.md` — phiếu SUS đã điền (template mục B của `../template/sus-form-vi.md`), kèm phần chấm điểm của moderator.

Kịch bản tình huống dùng chung: `../task-scenario-draft.md`. Sản phẩm mục tiêu trong mọi session: **Tai nghe AirPods Pro 2** (6.000.000₫), mã `SAVE10` → còn 5.400.000₫.

## Tổng hợp nhanh

| P | Người tham gia | Ngày | Thời lượng | Hoàn thành flow | Trợ giúp | SUS |
|---|---|---|---|---|---|---|
| P1 | Đặng Đăng Khoa | 21/07/2026 | 19 phút | ✓ | Không | 67.5 |
| P2 | Võ Ngọc Bích Trâm | 21/07/2026 | 15 phút | ✓ | Không | 57.5 |
| P3 | Phan Quốc Thịnh | 22/07/2026 | 25 phút | ✓ | 1 lần (Đăng ký) | 30.0 |
| P4 | Nguyễn Thanh Gia Bảo | 22/07/2026 | 18 phút | ✓ | Không | 52.5 |
| P5 | Lê Tuấn Lộc | 23/07/2026 | 22 phút | ✓ | Không | 55.0 |
| P6 | Trương Lý Khải | 23/07/2026 | 24 phút | ✓ | 1 lần (Đăng ký) | 35.0 |
| P7 | Nguyễn Thanh Tiến | 24/07/2026 | 16 phút | ✓ | Không | 75.0 |

**SUS trung bình: 53.2** (min 30 — P3, max 75 — P7). 5/7 hoàn thành hoàn toàn độc lập; cả 2 lần trợ giúp đều rơi vào bước Đăng ký (cụm BUG-11/12, đúng dự báo trong session-kit).

## Tín hiệu lặp lại nhiều nhất (đối chiếu mục tiêu)

- **O1 (Đăng ký):** 7/7 va lỗi số điện thoại bắt đầu bằng 0 (BUG-11); 7/7 va lỗi mật khẩu do hint mâu thuẫn (BUG-12 — P1: 1, P2: 2, P3: 4, P4: 2, P5: 3, P6: 2, P7: 1 lần). 5/7 tự phục hồi, 2/7 cần trợ giúp.
- **O2 (Thêm giỏ):** 7/7 không nhận được feedback (BUG-16); 7/7 dính click đầu bị nuốt (BUG-17); 2/7 (P3, P6) tạo dòng trùng trong giỏ (BUG-47); 6/7 tự mở giỏ để kiểm tra.
- **O6 (Tìm kiếm):** 4/7 (P1, P3, P5, P6) gõ cụm dài → 0 kết quả không có empty state (BUG-42; riêng P5 gặp 2 lần — đếm theo người, không đếm theo lần); 3 người tự rút gọn từ khoá (P1, P3, P5), 1 người chuyển sang duyệt danh sách (P6), P4 duyệt ngay từ đầu không dùng search.
- **Phụ (trust):** 7/7 nhận thấy giỏ không reset sau checkout (BUG-20): 4/7 bối rối/lo (P1, P3, P5, P6), 2/7 nhận diện là lỗi nhưng bình thản (P2, P4), 1/7 bỏ qua (P7) — tất cả chỉ yên tâm sau khi thấy đơn trong Lịch sử đơn hàng.
