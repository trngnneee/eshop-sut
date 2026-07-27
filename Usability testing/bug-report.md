# Bug report — U-01 self-test

## BR-U01-01 — CTA sau bước chọn ghế vẫn ghi “SEATINGS”

- FR: FR-19, FR-20, FR-35, FR-37.
- Môi trường: Chromium desktop 1440×1000.
- Actual: sau khi chọn 2 vé và A1–A2, CTA vẫn ghi `SEATINGS`; bấm vào lại chuyển sang snack.
- Expected: CTA mô tả bước kế tiếp, ví dụ `CONTINUE`, `NEXT` hoặc `SNACKS`, và nhất quán desktop/mobile.
- Priority: Medium.
- Ảnh: [trước khi đi tiếp](evidence/expert/09-two-seats-selected.png), [sau khi đi tiếp](evidence/expert/10-after-seat-next.png).

## BR-U01-02 — Card phim trên touch viewport cần hai lần chạm

- FR: FR-14, FR-15, FR-35, FR-37.
- Môi trường: touch emulation 390×844.
- Actual: overlay tên/mô tả có opacity 0; tap đầu chỉ hiện overlay và vẫn ở `/movies`; tap thứ hai vào tên mới mở chi tiết.
- Expected: tên phim hiển thị trước tương tác và một tap vào card mở chi tiết.
- Priority: Medium.
- Ảnh: [trước tap](evidence/expert/12-mobile-movies-before-tap.png), [sau tap đầu](evidence/expert/13-mobile-movies-after-tap.png).

Severity trong findings là provisional vì không có participant thật.

