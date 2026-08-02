# AI Critique — Task 2

**Status:** `HUMAN_REVIEWED`
**Target:** 200–300 words
**Student review confirmation:** Confirmed by the student in chat on 2026-08-02.

## Critique

Trong Task 2, AI giúp tôi chuyển yêu cầu của bài thành quy trình có cấu trúc: kiểm kê video, lập mốc T0–T11, chuẩn hóa P01–P07, tính metrics và truy vết findings về timestamp. AI cũng kiểm tra tính nhất quán giữa session report, CSV, bug report và summary, phát hiện clip D06 bị trùng và xác minh replacement bằng metadata cùng hash. Tuy nhiên, khả năng tổ chức tốt không đồng nghĩa AI hiểu bối cảnh nghiên cứu.

Audio của các session gần như không có speech. Một lần nhận dạng không dùng VAD sinh ra những câu không liên quan; nếu chấp nhận chúng, báo cáo sẽ chứa quote giả. Tôi đã loại transcript đó và giữ SUS, probes, consent ở trạng thái NOT_RECORDED. AI cũng ban đầu xem những file kết thúc giữa flow là recording bị cắt. Chỉ sau khi tôi xác nhận đó là toàn bộ session, outcome và task time mới được chốt đúng. Điều này cho thấy AI có thể mô tả bằng chứng chi tiết nhưng vẫn thiếu ngữ cảnh fieldwork mà người thực hiện nắm giữ.

Các template và validator ban đầu giả định pilot, SUS, consent và probes đầy đủ. Chúng hữu ích để ngăn bịa dữ liệu, nhưng không thể biến dữ liệu chưa từng thu thập thành dữ liệu hợp lệ. Nguyên tắc tôi rút ra là dùng AI cho cấu trúc, tính toán, kiểm tra chéo và traceability; còn danh tính participant, consent, quan sát, quyết định task-end và đánh giá cuối cùng phải do con người cung cấp và chịu trách nhiệm. Khi dữ liệu thiếu, báo cáo trung thực quan trọng hơn việc chỉnh nội dung để validator hiện chữ COMPLETE.

## Review confirmation

I have read this critique and confirmed that it reflects my judgement. Missing pilot, consent and probes remain disclosed and were not reconstructed during review.
