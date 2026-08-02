# AI Critique — Task 1

**Status:** `HUMAN_REVIEWED`
**Student review date:** `2026-08-02`

AI giúp mở rộng checklist lên 58 mục và gợi ý các nhóm quan trọng như accessibility, loading, empty state, network failure, double submit và responsive 320 px. Tuy nhiên, đầu ra ban đầu có ba sai lệch nghiêm trọng. Thứ nhất, AI dựa vào source code rồi ghi Actual/Status như thể đã quan sát runtime; năm ảnh tĩnh không chứng minh được các lỗi động. Thứ hai, nó hiểu FR-14 thành đầy đủ CRUD nên xem việc thiếu Edit Category là defect, đồng thời tự đặt yêu cầu cấm tên danh mục trùng. Thứ ba, summary 40 Pass/18 Fail không khớp checklist 36 Pass/22 Fail, cho thấy nhiều artefact không đồng nghĩa với dữ liệu nhất quán.

Lần hiệu chỉnh dùng 58 result rows từ execution Chrome đã sửa harness, lưu execution mode và liên kết mỗi row với screenshot có overlay. Các state cần kiểm soát timing được ghi MOCKED, còn core flows là LIVE_LOCAL_SUT. Hai expectation sai FR-14 và edge case trim không có requirement được viết lại trước khi phân loại; threshold lockout cũng được sửa về ba lần và 30 giây. Mobile soft keyboard vẫn Blocked vì Expo Web không tạo bằng chứng thiết bị thật.

Bài học là AI phù hợp để tăng coverage và tự động hóa đối chiếu, nhưng không được tự quyết định provenance. Mỗi verdict phải truy ngược về requirement, runtime observation và evidence. Validator chỉ đáng tin khi kiểm tra ngữ nghĩa, URL thật, execution mode và blocker bên ngoài, không chỉ kiểm tra file tồn tại.
