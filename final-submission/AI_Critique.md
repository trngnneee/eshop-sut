# HW03 Consolidated AI Critique

**Student:** Đặng Đăng Khoa  
**Student ID:** 23127207  
**Review date:** 2026-08-02  
**Review state:** `HUMAN_REVIEWED — confirmed by the student`

This file preserves one 200–300-word, human-reviewed critique for each task. The critique evaluates where AI accelerated the work, where it produced an unsafe or incorrect inference, how the output was corrected, and what responsibility remained with the student.

## Task 1 critique — GUI checklist testing

AI giúp mở rộng checklist lên 58 mục và gợi ý các nhóm quan trọng như accessibility, loading, empty state, network failure, double submit và responsive 320 px. Tuy nhiên, đầu ra ban đầu có ba sai lệch nghiêm trọng. Thứ nhất, AI dựa vào source code rồi ghi Actual/Status như thể đã quan sát runtime; năm ảnh tĩnh không chứng minh được các lỗi động. Thứ hai, nó hiểu FR-14 thành đầy đủ CRUD nên xem việc thiếu Edit Category là defect, đồng thời tự đặt yêu cầu cấm tên danh mục trùng. Thứ ba, summary 40 Pass/18 Fail không khớp checklist 36 Pass/22 Fail, cho thấy nhiều artefact không đồng nghĩa với dữ liệu nhất quán.

Lần hiệu chỉnh dùng 58 result rows từ execution Chrome đã sửa harness, lưu execution mode và liên kết mỗi row với screenshot có overlay. Các state cần kiểm soát timing được ghi `MOCKED`, còn core flows là `LIVE_LOCAL_SUT`. Hai expectation sai FR-14 và edge case trim không có requirement được viết lại trước khi phân loại; threshold lockout cũng được sửa về ba lần và 30 giây. Mobile soft keyboard vẫn Blocked vì Expo Web không tạo bằng chứng thiết bị thật.

Bài học là AI phù hợp để tăng coverage và tự động hóa đối chiếu, nhưng không được tự quyết định provenance. Mỗi verdict phải truy ngược về requirement, runtime observation và evidence. Validator chỉ đáng tin khi kiểm tra ngữ nghĩa, URL thật, execution mode và blocker bên ngoài, không chỉ kiểm tra file tồn tại.

**Section length:** 263 words under the repository validator’s whitespace-token method.

## Task 2 critique — usability testing

Trong Task 2, AI giúp tôi chuyển yêu cầu của bài thành quy trình có cấu trúc: kiểm kê video, lập mốc T0–T11, chuẩn hóa P01–P07, tính metrics và truy vết findings về timestamp. AI cũng kiểm tra tính nhất quán giữa session report, CSV, bug report và summary, phát hiện clip D06 bị trùng và xác minh replacement bằng metadata cùng hash. Tuy nhiên, khả năng tổ chức tốt không đồng nghĩa AI hiểu bối cảnh nghiên cứu.

Audio của các session gần như không có speech. Một lần nhận dạng không dùng VAD sinh ra những câu không liên quan; nếu chấp nhận chúng, báo cáo sẽ chứa quote giả. Tôi đã loại transcript đó và giữ SUS, probes, consent ở trạng thái `NOT_RECORDED`. AI cũng ban đầu xem những file kết thúc giữa flow là recording bị cắt. Chỉ sau khi tôi xác nhận đó là toàn bộ session, outcome và task time mới được chốt đúng. Điều này cho thấy AI có thể mô tả bằng chứng chi tiết nhưng vẫn thiếu ngữ cảnh fieldwork mà người thực hiện nắm giữ.

Các template và validator ban đầu giả định pilot, SUS, consent và probes đầy đủ. Chúng hữu ích để ngăn bịa dữ liệu, nhưng không thể biến dữ liệu chưa từng thu thập thành dữ liệu hợp lệ. Nguyên tắc tôi rút ra là dùng AI cho cấu trúc, tính toán, kiểm tra chéo và traceability; còn danh tính participant, consent, quan sát, quyết định task-end và đánh giá cuối cùng phải do con người cung cấp và chịu trách nhiệm. Khi dữ liệu thiếu, báo cáo trung thực quan trọng hơn việc chỉnh nội dung để validator hiện chữ `COMPLETE`.

**Section length:** 289 words under the repository validator’s whitespace-token method.

## Task 3 critique — cross-platform testing

AI hỗ trợ tốt ở phần biến checklist 58 mục thành một quy trình có thể lặp lại trên nhiều browser. Nó tạo overlay chứa họ tên, MSSV, email, phiên bản browser, thiết bị, URL localhost và timestamp, đồng thời nối mỗi kết quả với screenshot cụ thể. Việc dùng dữ liệu synthetic và cleanup sau test cũng giúp tránh làm bẩn database bằng category, product hoặc account thử nghiệm.

Tuy nhiên, AI đã sai ở ba điểm quan trọng. Đầu tiên, locator điều hướng ban đầu khớp cả link trong header và trong form, khiến ba kết quả Chrome bị thiếu. Thứ hai, proxy cho Expo Web truyền `Content-Type` khi Promise chưa được `await`, làm backend trả 500 và suýt biến lỗi test harness thành bug Mobile Login. Thứ ba, AI click vào trang trước khi kiểm tra bàn phím, vô tình thay đổi điểm bắt đầu focus và tạo ra khác biệt WebKit không có thật. Chỉ khi đối chiếu console, source và chuỗi Tab đầy đủ, các lỗi này mới được phát hiện và evidence được chụp lại.

Bài học quan trọng là automation output không tự động trở thành bằng chứng đáng tin. Mỗi kết quả bất thường phải được kiểm tra xem nguyên nhân nằm ở SUT, browser hay test harness. Ngoài ra, WebKit trên Windows và Pixel emulation có giá trị cho kiểm tra tương thích nhưng không thể được gọi là Safari hoặc Android thật chỉ để đủ ba nền tảng. Trung thực về giới hạn môi trường quan trọng hơn việc đổi nhãn để validator báo `Complete`.

**Section length:** 265 words under the repository validator’s whitespace-token method.

## Human accountability statement

The student reviewed and accepted all three sections on 2026-08-02. That review confirms the critique as the student’s judgement; it does not convert missing pilot, consent, probes, participant speech, external publication or physical-device evidence into completed work. The source critiques remain available in the three evidence archives, but this consolidated file is the submission entry point.
