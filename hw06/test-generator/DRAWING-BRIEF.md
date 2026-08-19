# Drawing brief — HUMAN-only

Tài liệu này chỉ liệt kê yêu cầu để người học tự thiết kế và tự vẽ `diagram.png`. Nó không phải sơ đồ nộp bài, không quyết định bố cục/hình thức thay người học và không được render trực tiếp thành ảnh. Theo R-16, người học phải tự giải thích được từng khối và từng quan hệ khi vấn đáp.

## Các khối bắt buộc

Sơ đồ tự vẽ cần thể hiện tối thiểu:

1. **Nguồn đầu vào**: API Spec và các yêu cầu FR/SEC.
2. **Parser**: đọc/chuẩn hoá mô tả endpoint.
3. **Parameter & State Model**: mô hình tham số, miền giá trị, precondition và trạng thái.
4. **Bốn hướng sinh test độc lập**:
   - Equivalence Partitioning / Boundary Value Analysis;
   - State Transition;
   - Security;
   - Schema validation.
5. **Test Case IR**: cấu trúc trung gian có ID, technique, data, expected và requirement/source.
6. **Audit hook / Human review gate**: phát hiện ID trùng, expected thiếu hoặc oracle không an toàn; chưa duyệt thì không được coi output là test case chốt.
7. **Đầu ra**: Markdown test cases và Postman JSON/skeleton.

## Quan hệ cần tự thể hiện

- Nguồn đầu vào đi qua Parser rồi mới tạo Parameter & State Model.
- Parameter & State Model cấp dữ liệu cho cả bốn hướng sinh test.
- Kết quả của bốn hướng hội tụ về Test Case IR.
- Test Case IR phải đi qua Audit hook / Human review gate trước khi render.
- Sau audit, luồng tách ra các đầu ra Markdown và Postman.
- Nên thể hiện vòng phản hồi từ audit về model/case khi phát hiện expected thiếu hoặc sai oracle. Người học tự quyết định cách vẽ vòng này và ký hiệu pass/fail.

## Gợi ý công cụ

Có thể dùng draw.io/diagrams.net, Excalidraw, PowerPoint, Figma hoặc vẽ tay rồi chụp rõ nét. File cuối phải do chính người học tạo và lưu tại `hw06/test-generator/diagram.png`.

Không dùng Mermaid/reference do AI sinh để export ảnh nộp bài. File `_reference/diagram-notes.mmd` chỉ giữ lịch sử minh bạch và phải nằm ngoài artifact sơ đồ HUMAN-only.

## Checklist tự kiểm tra trước khi lưu

- [ ] Có đủ bảy nhóm khối và bốn technique branch.
- [ ] Mũi tên thể hiện đúng input → model → generation → IR → audit → output.
- [ ] Có Human review gate, không ngụ ý AI tự quyết định oracle cuối cùng.
- [ ] Chữ đọc rõ khi mở ảnh ở kích thước thông thường.
- [ ] Người học có thể giải thích mọi khối mà không đọc tài liệu.
- [ ] Tên file cuối là `diagram.png`; ảnh do chính người học vẽ.
