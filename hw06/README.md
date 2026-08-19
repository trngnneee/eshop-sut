# HW06 — AI-first API Testing (MSSV 23127207)

## Trạng thái kỹ thuật

Bộ artifact đã có đủ pipeline kỹ thuật: phân tích → AI generation → audit → mở rộng → Postman/Newman → CI workflow → bug/traceability → generator → report. Số liệu dưới đây được đọc trực tiếp từ bảng test, tên assertion và `run.stats` trong Newman JSON; không phải số liệu ước lượng. Đối soát từng TC ID nằm ở [execution-coverage.md](newman/reports/execution-coverage.md).

Repository công khai: [trngnneee/eshop-sut](https://github.com/trngnneee/eshop-sut), branch `HW6-Khoa`.

| Chỉ số | Giá trị |
| :--- | ---: |
| Số API | 3 |
| AI-generated cases | 110 (36 + 36 + 38) |
| Human extension cases | 18 (6/API) |
| Final test cases | 128 (42 + 42 + 44) |
| Test cases có assertion Newman thật | 123/128 (96.1%) |
| Execution classification | 123 Automated · 1 Manual · 4 Blocked |
| Newman off assertions | 18, failed 0 |
| Newman canary assertions | 19, failed 1 |
| Newman full assertions | 26, failed 8 |
| Data-driven rows/assertions | 123 (39 + 41 + 43) |
| DDT assertion results | 76 passed · 47 failed (23 + 17 + 7) |
| Defect IDs reported | 15 |

Xem [báo cáo chính](report/main-report.md), [AI audit](report/ai-audit-report.md), [bug report](report/bug-report.md), [CI/CD report](report/cicd-report.md), [Newman reports](newman/reports/) và [Excel](excel/).

## Tự chấm theo rubric

| No. | Criteria | Max | Technical completion | Self-assessed now |
| ---: | :--- | ---: | :--- | ---: |
| 1 | API-1 full pipeline | 30 | Generation/audit/extend/execute/report complete; external evidence còn thiếu | 25 |
| 2 | API-2 full pipeline | 30 | Generation/audit/extend/execute/report complete; external evidence còn thiếu | 25 |
| 3 | API-3 full pipeline | 30 | Matrix/generation/extend/execute complete; audit file có metadata sign-off cần người học tự xác minh | 25 |
| 4 | Agent Skill/test-generator | 10 | Design, generator, drawing brief và audit hook; `diagram.png` HUMAN-only còn thiếu | 7 |
| **Tổng kỹ thuật hiện tại** |  | **100** |  | **80/100 trước human gates** |

Điểm 100 chỉ có thể tự tin nộp sau khi hoàn tất các gate bắt buộc của đề: xác minh API-3 audit, kiểm tra 15 GitHub Issues + 15 screenshot local, chụp Postman Console/Newman/CI, tự vẽ `test-generator/diagram.png`, viết lại critique bằng lời của người học, xuất PDF, đặt repo public và đóng zip đúng tên.

## Chạy lại

```powershell
# terminal 1 — backend (port 3000 nếu trống; dùng 3001 khi port 3000 bận)
$env:PORT = '3001'
node backend/server.js

# terminal 2
cd hw06
npm ci
# Lấy hai fixture password từ môi trường riêng; không commit giá trị vào repo.
$env:HW06_USER_PASSWORD = '<local fixture value>'
$env:HW06_ADMIN_PASSWORD = '<local fixture value>'
.\newman\run-newman.ps1 -Mode off -BaseUrl http://127.0.0.1:3001 -ReportName 00-off-suite
.\newman\run-newman.ps1 -Mode canary -BaseUrl http://127.0.0.1:3001 -ReportName 00-canary-suite
.\newman\run-newman.ps1 -Mode full -BaseUrl http://127.0.0.1:3001 -ReportName 00-full-suite
.\newman\run-newman.ps1 -DataDriven -BaseUrl http://127.0.0.1:3001
```

`run-newman.ps1 -DataDriven` tự chạy setup và export environment trước checkout/status. Mỗi DDT iteration tự tạo user/cart/order và dựng state cần thiết; ba report cuối có `requests.failed=0` và `testScripts/prerequestScripts.failed=0`, nên 47 failed assertions là chênh lệch oracle/SUT chứ không phải lỗi hạ tầng test.

Runner tự gọi `tooling/sanitize_public_artifacts.py` sau mỗi lần chạy. Chỉ giá trị password/JWT bị thay bằng marker `<redacted-…>`; tên assertion, status, pass/fail và cấu trúc report được giữ nguyên. CI nhận fixture qua GitHub Actions secrets `HW06_USER_PASSWORD`/`HW06_ADMIN_PASSWORD` và cũng redaction artifact trước khi upload.

## Đóng gói

Script `tooling/package_submission.py` kiểm tra đủ artifact mục 1 của deliverables checklist, xuất ba PDF bằng Pandoc hoặc HTML + Chrome/Edge, làm mới Git commit log trong staging và tạo file `23127207_HW06_AI_API_<grade>.zip`. Grade bắt buộc có ba chữ số:

```powershell
python hw06/tooling/package_submission.py --grade 080 --check-only
python hw06/tooling/package_submission.py --grade 080
```

Nếu không có PDF engine, script lưu HTML in-ready rồi dừng; sau khi người học tự Print to PDF, chạy lại với `--pdf-dir <thu-muc-pdf>`. Script luôn dừng trước khi xuất/zip nếu thiếu `diagram.png`, ảnh console, hai ảnh CI hoặc critique vẫn là bản nháp HUMAN-only. Nó không tạo hoặc thay thế bất kỳ bằng chứng HUMAN-only nào.

## Human evidence checklist

- [ ] Xác minh metadata/signature API-3 `02-audit.md`.
- [ ] `evidence/screenshots/01-x-student-id-console.png`, `02-newman-cli-run.png`.
- [x] Hai URL/SHA CI thật trong `report/cicd-report.md`: run `off` xanh và `canary` đỏ đúng một assertion `TC-API-LOGIN-018`.
- [ ] Hai ảnh HUMAN-only `evidence/screenshots/04-ci-pass.png` và `05-ci-fail.png`.
- [x] 15 GitHub Issue public và 15 screenshot local trong `evidence/screenshots/github-issues/` (manifest: `report/github-issues.json`).
- [ ] `test-generator/diagram.png` HUMAN-only do người học tự vẽ — hiện chưa có; dùng `test-generator/DRAWING-BRIEF.md` làm checklist, không render file trong `_reference/`.
- [ ] `report/ai-critique.md` được viết lại (bản hiện tại ghi rõ là draft).
- [x] Repository public và script `tooling/package_submission.py` đã có fail-closed gate cho artifact HUMAN-only.
- [ ] Sau khi hoàn tất các human gate, xuất `main-report.pdf`, `ai-audit-report.pdf`, `ai-critique.pdf` và zip `23127207_HW06_AI_API_<grade>.zip`.
