# HW03 AI Critique

**Student:** Đặng Đăng Khoa  
**Student ID:** 23127207  
**Review date:** 2026-08-03  
**Review state:** `HUMAN_REVIEWED — confirmed by the student`

## Critique (200–300 words)

AI giúp tôi mở rộng checklist, chuẩn hóa bảy session usability, tính SUS, liên kết finding với timestamp và lặp lại 58 kiểm tra trên nhiều browser. Tuy nhiên, AI đã sai hoặc thiếu ở ba kiểu quan trọng. Thứ nhất, nó từng suy verdict runtime từ source code và năm ảnh tĩnh, đồng thời hiểu FR-14 thành đầy đủ CRUD. Tôi chỉ chấp nhận kết luận sau khi đối chiếu requirement và chạy SUT. Thứ hai, khi audio usability gần như im lặng, một lần ASR không dùng VAD tạo câu nói không liên quan. Tôi loại toàn bộ transcript đó, không tạo quote, consent, probe hay hành vi participant không quan sát được. Thứ ba, harness cross-platform từng dùng locator quá rộng, proxy thiếu `await` và thay đổi focus trước khi kiểm tra; nếu không đọc console và chạy lại, lỗi công cụ có thể bị báo thành lỗi sản phẩm. AI cũng không được gọi WebKit trên Windows là Safari hoặc emulation là thiết bị Android thật. Những sai lệch này xảy ra vì mô hình tạo mẫu hợp lý trong ngữ cảnh chưa đầy đủ, trong khi provenance và ý nghĩa requirement cần bằng chứng cụ thể. Nguyên tắc tôi rút ra là dùng AI để tăng coverage, tính toán và kiểm tra chéo, nhưng mỗi kết luận phải có ba neo: requirement, quan sát runtime và artefact truy vết được. Khi một neo thiếu, tôi ghi giới hạn thay vì ép validator báo hoàn tất. Human review không phải bước ký tên cuối cùng mà là quá trình bác bỏ, sửa và tái kiểm chứng đầu ra AI.

**Word-count target:** 200–300 words; validated automatically before packaging.
