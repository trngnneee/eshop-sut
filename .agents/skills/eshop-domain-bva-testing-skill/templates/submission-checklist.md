# Submission Checklist Template

Sử dụng checklist này để rà soát toàn bộ hồ sơ bài tập HW02 trước khi nén zip nộp lên Moodle.

## 1. Hồ Sơ Báo Cáo Chính (Main Reports)
- [ ] File báo cáo chính `Report.md` chứa đầy đủ nội dung phân tích của 4 tính năng.
- [ ] Đã export file `Report.pdf` từ file markdown.
- [ ] Báo cáo có chứa đầy đủ phân tích Domain Testing (EP) cho cả 4 tính năng chưa?
- [ ] Báo cáo có chứa đầy đủ phân tích Boundary Value Analysis (BVA) cho cả 4 tính năng chưa?

## 2. Báo Cáo Lỗi & Minh Chứng (Bug Reports & Evidence)
- [ ] Đầy đủ các file báo cáo lỗi chi tiết cho các bug phát hiện được (nằm trong thư mục `tests/bug/`).
- [ ] Các ảnh chụp màn hình bằng chứng (evidence screenshot) được lưu đầy đủ trong thư mục `evidence/`.
- [ ] Tất cả các bug phát hiện được đều đã được tạo Issue trên repo GitHub.
- [ ] Có đầy đủ link liên kết đến từng GitHub Issue trong báo cáo.

## 3. Hồ Sơ AI Audit & Critique (AI Audit & Critique Reports)
- [ ] Có file báo cáo tương tác AI `ai-audit-report.md` ghi lại đầy đủ lịch sử prompt và output gốc.
- [ ] Đã export file `ai-audit-report.pdf` từ file markdown.
- [ ] Có phần tự phê bình AI `ai-critique.md` (hoặc nằm trong báo cáo chính) dài từ 200 - 300 từ.
- [ ] Đã export file `ai-critique.pdf` từ file markdown.

## 4. Nhật Ký Commit Git (Git Commit Log)
- [ ] Đã export lịch sử commit thành file text `git-commit-log.txt` bằng câu lệnh `git log --oneline --graph --decorate --all > git-commit-log.txt` chưa?
- [ ] Lịch sử commit có thể hiện rõ quy trình làm việc từng bước (thiết kế test case, chạy test, sửa lỗi, cập nhật matrix) không?

## 5. README.md & Demo Video
- [ ] File `README.md` ở root của dự án chứa bảng tự đánh giá điểm số (Self-assessment Table) và báo cáo tổng hợp (Test Summary).
- [ ] Có link video demo (YouTube hoặc Driver công khai) quay end-to-end quá trình sử dụng Agent Skill trên một tính năng hoàn chỉnh.
- [ ] Video demo có thuyết minh giọng nói hoặc phụ đề giải thích rõ ràng không?
- [ ] Thư mục skill `eshop-domain-bva-testing-skill/` có được đính kèm trong thư mục nộp bài không?

## 6. Đóng Gói (Packaging)
- [ ] Tên file nén đặt đúng định dạng: `<StudentID>_HW02_AI_DomainTesting_<SelfAssessedGrade>.zip`
  *Ví dụ: `21120001_HW02_AI_DomainTesting_9.5.zip`*
- [ ] Giải nén thử file zip ở một thư mục khác để kiểm tra xem các đường dẫn file và hình ảnh có bị lỗi hiển thị hay không trước khi nộp.
