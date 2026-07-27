### 1. Tổng quan

Silk Performer là bộ performance/load testing thương mại của OpenText, mô phỏng VU cho web, database, distributed application và middleware, kèm Workbench/analysis ([OpenText Marketplace](https://marketplace.opentext.com/appdelivery/content/silk-performer) — truy cập 2026-07-14). Evidence: `DOC`.

### 2. Cost và licence

Installation Guide 21.0 mô tả Evaluation 45 ngày, giới hạn 10 VU; Workbench Help lại có đoạn nói 30 ngày. Giá commercial không công khai trong nguồn kiểm tra: `[CẦN BÁO GIÁ]`; entitlement thực phải xác minh, không tự hoà giải mâu thuẫn ([Installation Guide](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-installationguide-en.pdf), [Workbench Help](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-workbenchhelp-en.pdf) — truy cập 2026-07-14). Evidence: `DOC`.

### 3. Installation và platform support

Workbench/Controller 21.0 là Windows-centric, cần quyền admin; guide nêu khoảng 2,5 GB cho controller và 1 GB cho agent. Có silent installation và remote agents; container support không được xác nhận ([Installation Guide](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-installationguide-en.pdf), [Silent install](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-7DA0F053-INSTALLINGSILENTMODE-TSK.html) — truy cập 2026-07-14). Evidence: `DOC`; container: `ASSUMPTION`.

### 4. Scripting hoặc configuration model

Workbench record/generate Benchmark Description Language (BDL); có Java framework và HAR import. Project/script/workload lưu được, nhưng tooling/version/license làm Git reproducibility nặng hơn plain text tool ([Java framework](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-E71FE522-JAVAFM-CON.html), [Release Notes 19.5](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-releasenotes-en.pdf) — truy cập 2026-07-14). Evidence: `DOC` + `ASSUMPTION`.

### 5. Workload capabilities

Increasing, Steady State, Dynamic, All Day, Queuing arrival-rate và Verification models; warm-up/measurement/close-down, runtime adjustment và agent distribution. Parsing/context functions, per-VU cookies/cache, sequential/random multi-column data hỗ trợ correlation/session/parameterization ([Workload models](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-webhelp-en/SILKPERF-390794D9-WORKLOADMODELS-CON.html), [Parsing](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-0A2D472E-PARSINGFUNCTIONS-CON.html), [Agent assignment](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-webhelp-en/SILKPERF-0A0FF53D-WORKLOADCONFIGURATIONDIALOG-AGENTASSIGNMENT-REF.html) — truy cập 2026-07-14). Evidence: `DOC`.

### 6. Assertions và validation

Web verification kiểm tra response content/HTML/XML/data; baseline/performance threshold hỗ trợ pass/fail evaluation ([Web tutorial](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webloadtestingtutorial-en.pdf), [Baselines](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-B176837E-CONFIRMINGTESTBASELINES-CON.html) — truy cập 2026-07-14). Protocol-specific depth: `[CẦN THỰC NGHIỆM]`. Evidence: `DOC`.

### 7. Metrics và reporting

Real-time monitoring, browser HTML results, VU output/log và `.tsd` time-series; percentile function có accuracy/memory setting, nên p50/p95/p99 phải ghi cấu hình ([Real-time monitoring](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/GUID-626CEE1A-9989-4E61-B54D-7C6A1CCC387B.html), [Results](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-7CBD1FDA-VIEWINGRESULTSINWEBBROWSER-CON.html), [Percentile](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-webhelp-en/GUID-271C001F-FE5E-4B28-AA37-1B087F916493.html) — truy cập 2026-07-14). Evidence: `DOC`.

### 8. CI/CD và automation

`performer project.ltp /Automation 5 /WL:Workload /Resultsdir:<path>`; Jenkins integration có success conditions/performance levels. Public docs chưa cho contract exit code đủ rõ; cần positive/negative lab và Event Viewer/output audit ([CLI automation](https://www.microfocus.com/documentation/silk-performer/205/en/silkperformer-205-webhelp-en/GUID-BE43A9E4-6B4C-46CB-BCA9-6A3E7CE51F36.html), [Release Notes](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-releasenotes-en.pdf) — truy cập 2026-07-14). Evidence: `DOC`; exit semantics: `[CẦN THỰC NGHIỆM]`.

### 9. EShop suitability

Web/API flow, independent VU state, parser/correlation, data và multi-phase workload phù hợp login → catalog → cart → checkout. Access/license/Windows làm giảm fit trong seminar, không phủ nhận enterprise capability ([Web settings](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-790881A8-WEBSETTINGS-CON.html) — truy cập 2026-07-14). Evidence: `DOC` + fit `ASSUMPTION`.

### 10. AI-assisted potential

HAR + BDL/Java cho phép AI draft/audit, nhưng không tìm thấy native AI current trong docs 21.0. Human phải replay, audit parser/correlation, data/secret và workload. Evidence: `ASSUMPTION`.

### 11. Classroom suitability

Workbench trực quan nhưng Windows/admin/trial 10 VU và tài liệu 30/45 ngày mâu thuẫn cản trở activity 25 phút; chỉ khả thi nếu pre-install/pre-license, vẫn `[CẦN THỰC NGHIỆM]`. Evidence: `DOC` + `ASSUMPTION`.

### 12. Điểm mạnh trong phạm vi seminar

Workload doanh nghiệp đa dạng; correlation/parser; distributed agents; verification; real-time/percentile/baseline reporting ([Documentation 21.0](https://www.microfocus.com/documentation/silk-performer/) — truy cập 2026-07-14). Evidence: `DOC`.

### 13. Hạn chế trong phạm vi seminar

Commercial price không public; trial docs mâu thuẫn; Windows-heavy; public docs latest tìm thấy là 21.0; container và direct exit semantics chưa xác nhận. Các điểm này là scope/access limits, không phải kết luận tool “kém”. Evidence: `DOC`/`ASSUMPTION` đã đánh dấu.

### 14. Smoke Test Plan

**[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN]**

- **Mục tiêu:** 1 GET, content verification, 1 VU và result/report.
- **Prerequisites:** Windows/admin, installer checksum, Evaluation/licensed entitlement, `[VERIFIED_BASE_URL]`, quyền test.
- **Installation/setup:** cài 21.0; ghi OS/version/license; Workbench tạo Web project + Verification workload 1 VU/1 iteration.
- **Request:** `GET [VERIFIED_BASE_URL]/[VERIFIED_READ_ONLY_PATH]` với status/content verification.
- **Command/config:** `performer C:\lab\silk-smoke\silk-smoke.ltp /Automation 5 /WL:Verification /Resultsdir:C:\lab\artifacts\silk-smoke` ([CLI](https://www.microfocus.com/documentation/silk-performer/205/en/silkperformer-205-webhelp-en/GUID-BE43A9E4-6B4C-46CB-BCA9-6A3E7CE51F36.html) — truy cập 2026-07-14).
- **Kết quả mong đợi:** verification pass, output/result/report sinh; chưa quan sát.
- **Evidence:** version/license redacted, project/BDL/workload, command, stdout/stderr/exit, Event Viewer, VU output, report.
- **Lỗi có thể gặp:** trial hết/10 VU, admin/runtime, TLS/proxy, parser/marker, agent unavailable, results path.
- **Tiêu chí thành công:** đúng request/verification, không automation error, đủ artefact; marker sai phải chứng minh failure propagation.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Lý do | Evidence |
|---|---:|---:|---|---|
| Cost & access | 8% | 2 | Trial 10 VU; commercial/price cần xác minh | DOC |
| Learning curve | 8% | 2 | Workbench + BDL/agents/workloads | ASSUMPTION từ DOC |
| EShop fit | 15% | 4 | Web state/data/verification tốt, access friction | DOC + ASSUMPTION |
| Multi-step journey & state | 12% | 5 | Cookie/parser/correlation/data | DOC |
| Workload model & scalability | 10% | 5 | Arrival/concurrency/dynamic/distributed | DOC |
| Assertions & business validation | 8% | 4 | Content verification/thresholds | DOC |
| Metrics & reporting | 8% | 5 | Real-time/raw/log/HTML/percentile | DOC |
| CI/CD & automation | 7% | 4 | CLI/Jenkins; exit cần lab | DOC + ASSUMPTION |
| Reproducibility | 7% | 3 | Project lưu được; Windows/license/agents nặng | ASSUMPTION |
| Local/offline | 5% | 4 | On-prem runner; activation/air-gap cần xác minh | DOC + ASSUMPTION |
| AI-assisted potential | 7% | 3 | HAR/BDL draft được, không native AI xác nhận | ASSUMPTION |
| Classroom suitability | 5% | 2 | Trial/admin/Windows khó nhân rộng | ASSUMPTION |
| Community | 0% | 3 | Official catalog/marketplace có, nhưng public docs hiện hành hạn chế ([docs](https://www.microfocus.com/documentation/silk-performer/) — truy cập 2026-07-14) | DOC; không tính |

**Weighted Score provisional: 74,8/100; 0 EXP.**

### 16. Kết luận sơ bộ

**Survey-only.** Ghi nhận enterprise workload/analysis; không chọn live activity cho đến khi access, version và 25-minute workflow được chứng minh.

### 17. Câu hỏi phản biện

<details>
<summary><strong>Câu hỏi phản biện Silk Performer</strong></summary>

1. **Trial 30 hay 45 ngày?** Official docs mâu thuẫn; entitlement tài khoản thực mới quyết định ([Install Guide](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-installationguide-en.pdf) — truy cập 2026-07-14).
2. **10 VU chứng minh scalability?** Không; chỉ đủ smoke/learning, không đủ capacity conclusion.
3. **Report đẹp có đủ thay JMeter?** Không; access, reproducibility, local/classroom và role complementarity vẫn phải chấm.
4. **CLI tự fail build khi threshold fail?** Chưa được chứng minh; cần positive/negative run và process/report evidence.

</details>
