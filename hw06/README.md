# HW06 — AI-first API Testing (MSSV 23127207)

## Trạng thái kỹ thuật

Bộ artifact đã có đủ pipeline kỹ thuật: phân tích → AI generation → audit → mở rộng → Postman/Newman → CI workflow → bug/traceability → generator → report. Số liệu dưới đây được đọc từ bảng test và Newman JSON trong repo; không phải số liệu ước lượng.

| Chỉ số | Giá trị |
| :--- | ---: |
| Số API | 3 |
| AI-generated cases | 110 (36 + 36 + 38) |
| Human extension cases | 18 (6/API) |
| Final test cases | 128 (42 + 42 + 44) |
| Newman off assertions | 18, failed 0 |
| Newman canary assertions | 19, failed 1 |
| Newman full assertions | 26, failed 8 |
| Data-driven rows | 59 (16 + 18 + 25) |
| Defect IDs reported | 15 |

Xem [báo cáo chính](report/main-report.md), [AI audit](report/ai-audit-report.md), [bug report](report/bug-report.md), [CI/CD report](report/cicd-report.md), [Newman reports](newman/reports/) và [Excel](excel/).

## Tự chấm theo rubric

| No. | Criteria | Max | Technical completion | Self-assessed now |
| ---: | :--- | ---: | :--- | ---: |
| 1 | API-1 full pipeline | 30 | Generation/audit/extend/execute/report complete; external evidence còn thiếu | 25 |
| 2 | API-2 full pipeline | 30 | Generation/audit/extend/execute/report complete; external evidence còn thiếu | 25 |
| 3 | API-3 full pipeline | 30 | Matrix/generation/extend/execute complete; audit file có metadata sign-off cần người học tự xác minh | 25 |
| 4 | Agent Skill/test-generator | 10 | Design, generator, Mermaid và audit hook; `diagram.png` human-only còn thiếu | 7 |
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
.\newman\run-newman.ps1 -Mode off -BaseUrl http://127.0.0.1:3001 -ReportName 00-off-suite
.\newman\run-newman.ps1 -Mode canary -BaseUrl http://127.0.0.1:3001 -ReportName 00-canary-suite
.\newman\run-newman.ps1 -Mode full -BaseUrl http://127.0.0.1:3001 -ReportName 00-full-suite
.\newman\run-newman.ps1 -DataDriven -BaseUrl http://127.0.0.1:3001
```

`run-newman.ps1 -DataDriven` tự chạy setup và export environment trước checkout/status, nên không tạo 401 giả vì thiếu token/orderId.

## Human evidence checklist

- [ ] Xác minh metadata/signature API-3 `02-audit.md`.
- [ ] `evidence/screenshots/01-x-student-id-console.png`, `02-newman-cli-run.png`.
- [ ] Hai ảnh CI xanh/đỏ và hai URL/SHA thật trong `report/cicd-report.md`.
- [x] 15 GitHub Issue public và 15 screenshot local trong `evidence/screenshots/github-issues/` (manifest: `report/github-issues.json`).
- [ ] `test-generator/diagram.png` do người học tự vẽ.
- [ ] `report/ai-critique.md` được viết lại (bản hiện tại ghi rõ là draft).
- [ ] Xuất `main-report.pdf`, `ai-audit-report.pdf`, `ai-critique.pdf`, repo public và zip `23127207_HW06_AI_API_<grade>.zip`.
