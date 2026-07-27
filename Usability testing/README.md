# Bộ bài U-01

File bắt đầu: [SUBMISSION_U01.md](SUBMISSION_U01.md).

## File dùng cho bài làm

- `SUBMISSION_U01.md`: báo cáo chính và checklist trạng thái.
- `test-plan-final.md`: kế hoạch test hoàn chỉnh.
- `sessions/P01.md`, `sessions/P02.md`, `sessions/P03.md`: form thu thập ba phiên thật.
- `findings-report-final.md`: bảng tổng hợp và candidate findings cần xác nhận bằng participant.
- `bug-report.md`: hai bug/rủi ro đã tái hiện bằng pilot kỹ thuật.
- `browserstack.md`: kịch bản, ma trận và checklist BrowserStack.
- `evidence/expert/`: ảnh pilot kỹ thuật.
- `evidence/participants/`: nơi đặt bằng chứng participant sau khi có đồng thuận.
- `evidence/browserstack/`: nơi đặt hai screenshot BrowserStack bắt buộc.

## Script tái hiện kỹ thuật

- `u01-info-walkthrough.mjs`: tái hiện desktop từ chọn suất đến `TICKET DETAILS` với dữ liệu pilot ngày 20/07/2026.
- `u01-mobile-movie-card.mjs`: tái hiện hành vi card phim cần hai lần chạm trên touch viewport.

Các script dùng ID/suất cố định của dữ liệu pilot; nếu backend đổi dữ liệu, cần cập nhật ID trước khi chạy lại.

## File nháp cũ

`test-plan.md`, `P01.md` và `findings-report.md` là draft có sẵn trước khi hoàn thiện bộ bài. Dùng các file có hậu tố `-final` và thư mục `sessions/` làm bản chính để tránh nhầm URL hoặc cấu trúc cũ.

## Phần chưa thể tạo thay người làm bài

- Quan sát, thời gian, hành vi và quote của 3 participant thật.
- Screenshot BrowserStack có thông tin browser/OS/device từ tài khoản BrowserStack Live.

Không thay hai loại bằng chứng này bằng dữ liệu giả hoặc ảnh Chromium headless.

