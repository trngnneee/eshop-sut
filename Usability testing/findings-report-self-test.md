# Báo cáo findings — U-01

## 1. Phạm vi và phương pháp

- Website: <https://lumierecinema-testing-demo-ui.vercel.app/>
- Flow: **U-01**.
- FR được kiểm tra: **FR-14, FR-15, FR-18, FR-19, FR-20, FR-35, FR-37**.
- Ngày thực hiện: **20/07/2026**.
- Persona tham chiếu: sinh viên đại học năm 3, thường xuyên dùng website/app và có kinh nghiệm đặt vé online.
- Phương pháp thực tế: **self-test kết hợp expert/cognitive walkthrough**, không có participant bên ngoài.
- Môi trường chính: Chromium desktop 1440×1000.
- Kiểm tra bổ sung: touch emulation 390×844, `isMobile=true`, `hasTouch=true`.

> Báo cáo này không phải moderated usability test với người tham gia thật. Vì không có participant, báo cáo không sử dụng quote, hesitation, intervention hoặc rating giả. Frequency `1/1 walkthrough` chỉ thể hiện vấn đề được tái hiện trong một lượt tự kiểm tra, không phải tỷ lệ người dùng gặp vấn đề.

## 2. Task scenario

> Bạn muốn xem một phim đang chiếu tại Lumiere Cinema vào cuối tuần này. Hãy tìm một phim phù hợp, chọn rạp, chọn suất chiếu, chọn ghế cho 2 người và hoàn tất đến khi bạn thấy thông tin vé.

## 3. Dữ liệu walkthrough

- Phim: `A Minecraft Movie`.
- Rạp: `Nhà Hát Múa Rối Nước Rồng Vàng`.
- Ngày/suất: 22/07/2026 lúc 20:00.
- Deviation: chọn ngày gần nhất có suất thay vì cuối tuần.
- Vé: 2 Adult.
- Ghế: A1, A2.
- Tổng: 160.000 VND.
- End state: `TICKET DETAILS`.

Thông tin cuối hiển thị đúng phim, địa chỉ `55B Nguyễn Thị Minh Khai, Bến Thành`, ngày, 2 vé Adult, ghế A1/A2, thời gian 20:00–21:39, phòng `Medium screen 3` và tổng 160.000 VND.

## 4. Kết quả tổng quan

| Lượt | Phương pháp | Kết quả | Error chức năng | Vấn đề usability | End state |
| --- | --- | --- | ---: | ---: | --- |
| EW-01 | Expert/self walkthrough desktop | `WALKTHROUGH_PASS` | 0 | 1 | `TICKET DETAILS` |
| EW-02 | Touch-emulation walkthrough | `ISSUE_REPRODUCED` | 0 | 1 | Mở chi tiết sau hai lần chạm |

- Walkthrough desktop hoàn thành: **1/1**.
- Findings tái hiện: **2**.
- Rating, task time usability, quote và moderator intervention: **Không áp dụng vì không có participant**.

## 5. Findings

### F-01 — CTA sau bước chọn ghế vẫn ghi “SEATINGS”

- Flow: U-01.
- FR liên quan: **FR-19, FR-20, FR-35, FR-37**.
- Occurrence: **1/1 desktop walkthrough**.
- Bằng chứng: sau khi chọn 2 vé Adult và A1–A2, summary hiển thị tổng 160.000 VND nhưng CTA vẫn ghi `SEATINGS`. Bấm CTA lại chuyển sang màn hình snack. Ở mobile, CTA tương ứng ghi `INFO`, nên copy không nhất quán giữa breakpoint.
- Quote participant: **Không có — self-test, không tạo quote giả**.
- Tác động dự kiến: người dùng có thể nghĩ CTA mở lại/giữ nguyên bước chọn ghế, không nhận ra đây là nút tiếp tục và do dự tại bước chuyển.
- Severity tạm thời: **S3 — provisional**.
- Lý do: không chặn chức năng nhưng nhãn sai ngữ cảnh có khả năng gây do dự đáng kể. Cần user test thật để xác nhận severity hành vi.
- Nguyên nhân khả dĩ: desktop dùng tên bước hiện tại thay cho hành động kế tiếp; desktop/mobile lấy copy khác nhau.
- Đề xuất:
  - Đổi nhãn thành `CONTINUE`, `NEXT` hoặc `SNACKS`.
  - Dùng cùng nguồn label cho desktop và mobile.
  - Không dùng tên bước hiện tại cho CTA đi tiếp.
- Tiêu chí retest:
  - Desktop/mobile có cùng nhãn và nhãn mô tả đúng bước kế tiếp.
  - Nếu retest với người dùng, participant nhận ra CTA trong dưới 5 giây và không cần trợ giúp.
- Ảnh:
  - [A1–A2 đã chọn nhưng CTA vẫn là SEATINGS](evidence/expert/09-two-seats-selected.png).
  - [Bấm CTA chuyển sang snack](evidence/expert/10-after-seat-next.png).

### F-02 — Card phim trên touch viewport cần hai lần chạm

- Flow: U-01.
- FR liên quan: **FR-14, FR-15, FR-35, FR-37**.
- Occurrence: **1/1 touch-emulation walkthrough**.
- Bằng chứng:
  - Trước tương tác, container tên/mô tả có computed `opacity: 0` do `opacity-0 group-hover:opacity-100`.
  - Lần chạm đầu chỉ làm overlay xuất hiện; URL vẫn là `/movies`.
  - Lần chạm thứ hai vào tên phim mới mở `/movie?movieId=...`.
- Quote participant: **Không có — self-test, không tạo quote giả**.
- Tác động dự kiến: người dùng touch có thể nghĩ card không hoạt động, không biết tên phim hoặc phải khám phá target nhỏ ở lần chạm thứ hai.
- Severity tạm thời: **S3 — provisional**.
- Lý do: ảnh hưởng trực tiếp bước chọn phim nhưng vẫn có thể hoàn thành sau khi khám phá overlay; chưa có bằng chứng participant bị chặn hoặc cần trợ giúp.
- Nguyên nhân khả dĩ: nội dung quan trọng phụ thuộc hover; chỉ tên phim là target điều hướng; không có thiết kế cho `hover: none`.
- Đề xuất:
  - Luôn hiển thị tên phim trên touch layout.
  - Biến toàn card thành semantic link/button với accessible name là tên phim.
  - Với `@media (hover: none)`, không ẩn overlay quan trọng.
- Tiêu chí retest:
  - Trên Safari iOS/Chrome Android, tên phim hiển thị trước tương tác.
  - Một lần tap vào card mở chi tiết.
  - Card thao tác được bằng bàn phím.
- Ảnh:
  - [Card trước lần chạm](evidence/expert/12-mobile-movies-before-tap.png).
  - [Overlay sau lần chạm đầu](evidence/expert/13-mobile-movies-after-tap.png).

## 6. Điểm hoạt động tốt

- `Buy Tickets` và `BUY A TICKET` dễ nhận ra.
- Chọn rạp xong, ngày và suất được tải thành công.
- Suất chiếu hiển thị số ghế còn lại.
- Sơ đồ ghế có legend Normal, VIP, Taken, Couple và Selected.
- Summary hiển thị số vé, ghế và tổng tiền.
- `TICKET DETAILS` phản ánh đúng phim, rạp, ngày, suất, 2 vé, A1–A2 và tổng tiền.

Đây là kết quả kiểm tra chức năng/heuristic, không phải đánh giá hài lòng của participant.

## 7. Bug report và bằng chứng

Hai finding tương ứng với [bug-report.md](bug-report.md):

- BR-U01-01 — CTA `SEATINGS` sai/ngược ngữ cảnh.
- BR-U01-02 — card touch cần hai lần chạm.

Ảnh end state: [TICKET DETAILS](evidence/expert/11-ticket-info.png).

## 8. BrowserStack

BrowserStack chưa được chạy. Kịch bản nằm tại [browserstack.md](browserstack.md). Cần xác minh Chrome/Windows 11 và Safari/iPhone hoặc browser thứ hai. Ảnh trong `evidence/expert/` không được ghi là ảnh BrowserStack.

## 9. Kết luận

Self-test xác nhận U-01 có thể hoàn thành tới `TICKET DETAILS` với 2 vé và 2 ghế. Hai vấn đề ưu tiên là CTA `SEATINGS` sai ngữ cảnh trên desktop và card phim phụ thuộc hover trên touch device. Cả hai được xếp **S3 tạm thời** theo tác động dự kiến, chưa phải severity được chứng minh từ hành vi participant.

## 10. Giới hạn

- Không có participant thật; đây là self-test/expert walkthrough.
- Không có quote, rating, hesitation hoặc intervention của người dùng.
- Một evaluator không đại diện cho toàn bộ sinh viên năm 3.
- Touch test dùng emulation, chưa phải Safari/iPhone thật hoặc BrowserStack.
- `1/1 walkthrough` không có nghĩa 100% người dùng sẽ gặp vấn đề.
- Đề gốc yêu cầu 3 participant thật; báo cáo này không đáp ứng phần participant evidence của rubric đó.

