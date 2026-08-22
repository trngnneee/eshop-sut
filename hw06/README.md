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
| Test cases có assertion Newman thật | 127/128 (99.2%) |
| Execution classification | 127 Automated · 1 Blocked |
| Newman off assertions | 18, failed 0 |
| Newman canary assertions | 19, failed 1 |
| Newman full assertions | 26, failed 8 |
| Data-driven rows/assertions | 123 (39 + 41 + 43) |
| DDT assertion results | 76 passed · 47 failed (23 + 17 + 7) |
| Defect IDs reported | 19 |

Video demo Agent Skill: [https://youtu.be/GT9lxje6NJE](https://youtu.be/GT9lxje6NJE)

Xem [báo cáo chính](report/main-report.md), [AI audit](report/ai-audit-report.md), [bug report](report/bug-report.md), [CI/CD report](report/cicd-report.md), [Newman reports](newman/reports/) và [Excel](excel/).

## Tự chấm theo rubric

| No. | Criteria | Max | Technical completion | Self-assessed now |
| ---: | :--- | ---: | :--- | ---: |
| 1 | API-1 full pipeline | 30 | 36 AI + 6 human = 42 case; audit 100%; execution coverage **42/42 = 100%**; mọi bug có issue + screenshot | 30 |
| 2 | API-2 full pipeline | 30 | 36 AI + 6 human = 42 case; audit 100%; execution coverage **42/42 = 100%**; mọi bug có issue + screenshot | 30 |
| 3 | API-3 full pipeline | 30 | 38 AI + 6 human = 44 case gồm đủ ma trận 5×5; human sign-off đã ký; 43/44 = 97.7% — `TC-API-ORDER-STATUS-041` không thể chạy vì SUT không có endpoint dashboard/revenue | 29 |
| 4 | Agent Skill/test-generator | 10 | Design, generator, audit hook, `diagram.png` tự vẽ và [video demo](https://youtu.be/GT9lxje6NJE) — đã đủ | 10 |
| **Tổng** |  | **100** |  | **99** |

Đã hoàn tất toàn bộ gate bắt buộc: sơ đồ tự vẽ, critique tự viết, sign-off cả ba API, screenshot console + Newman CLI + hai run CI, 19 GitHub Issue kèm 19 screenshot, video demo Agent Skill, repo public, Pull Request [#428](https://github.com/trngnneee/eshop-sut/pull/428) theo `Rule.pdf` §H.3.

Không tự chấm 100 vì đúng **một** case không thể thực thi: `TC-API-ORDER-STATUS-041` cần quan sát doanh thu sau khi chuyển trạng thái, nhưng SUT không có endpoint dashboard/revenue nào — đã rà toàn bộ route `/api/admin/*` trong `backend/server.js`. Đây là giới hạn của hệ thống được kiểm thử, được nêu rõ thay vì giấu. Việc dùng Bruno cho ảnh bằng chứng client đã được giảng viên chấp thuận.

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
- [x] `evidence/screenshots/01-x-student-id-console.png` (Bruno Timeline — header do script cấp collection gắn runtime) và `02-newman-cli-run.png` + `02b-newman-cli-summary.png` (Newman CLI).
- [x] Hai URL/SHA CI thật trong `report/cicd-report.md`: run `off` xanh và `canary` đỏ đúng một assertion `TC-API-LOGIN-018`.
- [x] Hai ảnh HUMAN-only `evidence/screenshots/04-ci-pass.png` (run `#3`, SHA `4bf4e5f`, Success) và `05-ci-fail.png` (run `#4`, SHA `03f3699`, Failure) do người học tự chụp từ tab Actions.
- [x] 19 GitHub Issue public (#413–#432) và 19 screenshot local trong `evidence/screenshots/github-issues/` (manifest: `report/github-issues.json`).
- [x] `test-generator/diagram.png` HUMAN-only do người học tự vẽ (draw.io) — đã có, đủ 7 nhóm khối, 4 nhánh technique, human review gate và 2 nhánh hồi tiếp.
- [x] `report/ai-critique.md` đã được người học viết lại; không còn marker draft HUMAN-only.
- [x] Repository public và script `tooling/package_submission.py` đã có fail-closed gate cho artifact HUMAN-only.
- [ ] Sau khi hoàn tất các human gate, xuất `main-report.pdf`, `ai-audit-report.pdf`, `ai-critique.pdf` và zip `23127207_HW06_AI_API_<grade>.zip`.
