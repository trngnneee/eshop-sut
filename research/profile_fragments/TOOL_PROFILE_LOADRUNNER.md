### 1. Tổng quan

Tên hiện hành là **OpenText Professional Performance Engineering (LoadRunner Professional)**, bộ enterprise on-prem performance testing cho co-located teams. Ba thành phần chính: VuGen tạo script, Controller điều phối/monitor scenario, Analysis phân tích result ([Product](https://www.opentext.com/products/professional-performance-engineering), [Get started 26.1](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/WelcomeContent/c_Welcome.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 2. Cost và licence

Community license 26.1 tự cài, miễn phí 50 Vuser cho các protocol, gồm JMeter/Gatling, trừ COM/DCOM, Templates và GUI bundles. Scale/bundle khác dùng evaluation/permanent/VUFD/commercial; giá public chưa tìm thấy: `[CẦN BÁO GIÁ]`. Trial được request không cần card, entitlement/duration phải xác minh ([License Utility](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/License/R_License_Utility.htm), [Trial](https://www.opentext.com/en-gb/products/professional-performance-engineering/trial) — truy cập 2026-07-14). Evidence: `DOC`.

### 3. Installation và platform support

VuGen/Controller/Analysis full stack là Windows-centric; standalone OneLG có Windows/Linux tùy protocol. Official Docker images chỉ cho load generators Ubuntu/RHEL/Windows, có firewall/protocol limitations; không đồng nghĩa full stack container ([Install](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Install/About-install.htm), [Docker LG](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/dockerized_load_generator.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 4. Scripting hoặc configuration model

VuGen record client-server traffic; recorded scripts chủ yếu C, một số protocol dùng C#/VB.NET/Java/JavaScript; init/action/end tách login/business/logout. Có HAR/offline generation, file/generated parameters, Correlation Studio và automatic correlation ([Vuser scripts](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/100050_c_vugen_overview.htm), [Recording](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/tocs/103100_toc_recording.htm), [Correlation](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/tocs/109650_toc_correlation_studio.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 5. Workload capabilities

Manual Scenario ghép scripts/groups, VU số lượng/tỷ lệ, load generators và SLA; schedule theo scenario/group có ramp/duration/stop. Goal-oriented targets VUs/pages/min/hits/s/transactions/s và tự điều chỉnh VU; nhiều on-prem/cloud/container LG phân tán tải ([Manual scenarios](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_manual_scenarios.htm), [Schedules](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_schedules_overview.htm), [Goal-oriented](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_goal_oriented_scenarios.htm) — truy cập 2026-07-14). Goal throughput không tự động tương đương fixed open-arrival executor (`ASSUMPTION`).

### 6. Assertions và validation

VuGen Web text/image checks xác minh đúng page/object; transactions và Controller/Analysis SLA cho pass/fail/APDEX. API flow vẫn cần status/body/business invariant cụ thể ([Web checks](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/c_web_text_and_image_verification.htm), [SLAs](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/toc_SLAs_main.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 7. Metrics và reporting

Analysis có transaction/TPS, throughput/web resources, errors/monitoring, HTML/Excel, raw result/export JSON/InfluxDB; Summary có HTTP status, pass/fail, APDEX và configurable percentile. Known Issues 26.1 ghi một Transaction Response Time percentile graph có thể sai, nên cross-check raw/export và patch ([Analysis](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/c_analysis_workflow.htm), [Summary](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/116850_ui_summary_report.htm), [Known issues](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/tl_Analysis.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 8. CI/CD và automation

`CLIControllerApp.exe` chạy `.lrs`/XML, Run/Collate/CollateAndAnalyze, result path/LG override/`-SilentMode`; chỉ một Controller, args case-sensitive và có overwrite risk. Direct CLI không công bố universal “SLA fail = exit N”; Jenkins OpenText plugin chạy scenarios có SLA để xác định pass/fail ([CLI](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/scenario-run-cli.htm), [Jenkins](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_jenkins.htm) — truy cập 2026-07-14). Evidence: `DOC`; direct exit: `[CẦN THỰC NGHIỆM]`.

### 9. EShop suitability

Web/API, recorder, data, token/session correlation, user mix, scheduling, SLA và monitoring rất phù hợp enterprise EShop. Nhiều protocol (>180 technologies theo product claim) hữu ích khi có legacy/packaged systems, nhưng HTTP EShop không tự động cần breadth đó ([Product](https://www.opentext.com/products/professional-performance-engineering), [Supported Protocols 26.1](https://admhelp.microfocus.com/documents/lre/Supported_Protocols/26.1/LR_Protocols.htm) — truy cập 2026-07-14). Evidence: `DOC` + fit `ASSUMPTION`.

### 10. AI-assisted potential

VuGen 26.1 có paid cloud **Aviator for Scripting**: protocol selection, coding help, error analysis, optimization, summary; AI analysis thuộc Core Performance Engineering Analysis. Không mặc định free/offline; output vẫn phải replay/audit ([VuGen What's New 26.1](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/WelcomeContent/c_WhatsNew.htm) — truy cập 2026-07-14). Evidence: `DOC` + governance `ASSUMPTION`; nghiên cứu không gọi Aviator.

### 11. Classroom suitability

Community 50 VU cho demo, nhưng Windows/admin, ba-component workflow, protocol concepts và artefact nặng khó hoàn tất trong 25 phút nếu không pre-install/prebuild; `[CẦN THỰC NGHIỆM]`. Evidence: `DOC` + `ASSUMPTION`.

### 12. Điểm mạnh trong phạm vi seminar

Enterprise protocol breadth; mature recording/correlation; Controller scheduling/distribution; Analysis/SLA; Community 50 VU; Jenkins/Docker LG; native AI ([Get started](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/WelcomeContent/c_Welcome.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 13. Hạn chế trong phạm vi seminar

Windows-heavy; commercial price không public; nhiều component/license/patch làm reproducibility nặng; direct CLI SLA exit cần test; documented percentile issue; Aviator paid/cloud. So với JMeter, LoadRunner có lifecycle/protocol enterprise tích hợp hơn, còn JMeter dễ access/local/version-control hơn; không kết luận công cụ nào mạnh tuyệt đối ([JMeter](https://jmeter.apache.org/), [LoadRunner product](https://www.opentext.com/products/professional-performance-engineering) — truy cập 2026-07-14). Evidence: `DOC` + contextual `ASSUMPTION`.

### 14. Smoke Test Plan

**[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN]**

- **Mục tiêu:** VuGen GET/check → Controller 1 VU → collate/Analysis/SLA; không đo capacity.
- **Prerequisites:** supported Windows/admin, installer checksum/patch, Community license, `[VERIFIED_BASE_URL]`, quyền test.
- **Installation/setup:** cài VuGen/Controller/Analysis; ghi License Utility; Web HTTP/HTML script + text check; manual `.lrs`, 1 VU/local LG/1 iteration + SLA.
- **Request:** `GET [VERIFIED_BASE_URL]/[VERIFIED_READ_ONLY_PATH]` bằng `web_url`, đăng ký text check trước request.
- **Command/config:** `CLIControllerApp.exe -TestPath C:\lab\lr-smoke\lr-smoke.lrs -CollateAndAnalyze -ResultName C:\lab\artifacts\lr-smoke -SilentMode` ([CLI](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/scenario-run-cli.htm) — truy cập 2026-07-14).
- **Kết quả mong đợi:** Vuser/check/SLA pass, collated result + Analysis report; chưa quan sát.
- **Evidence:** version/license redacted, VuGen source/data/runtime, `.lrs`/SLA/schedule/LG, command/stdout/stderr/exit, raw result/report.
- **Lỗi có thể gặp:** license/protocol, Windows privilege, recording/TLS/correlation, LG down, only-one-Controller, result overwrite/path, Analysis issue.
- **Tiêu chí thành công:** đúng request/check/SLA, collate/report đủ; marker/SLA sai phải chứng minh plugin/direct-CLI failure propagation.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Lý do | Evidence |
|---|---:|---:|---|---|
| Cost & access | 8% | 4 | Community 50 VU; ngoài đó commercial | DOC |
| Learning curve | 8% | 2 | VuGen–Controller–Analysis/protocol depth | ASSUMPTION từ DOC |
| EShop fit | 15% | 5 | Full Web/API state/data/SLA | DOC + ASSUMPTION |
| Multi-step journey & state | 12% | 5 | init/action/end/parameter/correlation | DOC |
| Workload model & scalability | 10% | 5 | Manual/goal/ramp/multi-LG/cloud | DOC |
| Assertions & business validation | 8% | 5 | Checks/transactions/SLA | DOC |
| Metrics & reporting | 8% | 5 | Analysis/raw/export/SLA/APDEX | DOC |
| CI/CD & automation | 7% | 4 | CLI/Jenkins; direct exit needs lab | DOC + ASSUMPTION |
| Reproducibility | 7% | 3 | Assets saveable; multi-component/license/OS | ASSUMPTION |
| Local/offline | 5% | 5 | Full on-prem runner/analysis/help | DOC |
| AI-assisted potential | 7% | 4 | Native Aviator, paid cloud dependency | DOC + ASSUMPTION |
| Classroom suitability | 5% | 2 | 50 VU helps; setup/workflow difficult | ASSUMPTION |
| Community | 0% | 4 | Current 26.1 Help Center, plugin/support ecosystem ([Help](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/WelcomeContent/c_Welcome.htm) — truy cập 2026-07-14) | DOC; không tính |

**Weighted Score provisional: 85,0/100; 0 EXP.**

### 16. Kết luận sơ bộ

**Backup** / enterprise reference. Community tier cho phép demo, nhưng không phải lựa chọn live mặc định khi JMeter/k6 tái lập gọn hơn cho EShop seminar.

### 17. Câu hỏi phản biện

<details>
<summary><strong>Câu hỏi phản biện LoadRunner Professional</strong></summary>

1. **Có thật sự miễn phí?** Community miễn phí đến 50 VU với exclusions; scale/bundle khác commercial ([License](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/License/R_License_Utility.htm) — truy cập 2026-07-14).
2. **180+ protocol làm nó tốt hơn JMeter cho EShop?** Không tự động; HTTP EShop còn phụ thuộc access, script clarity, CI và reproducibility.
3. **Docker nghĩa full LoadRunner container?** Không; source ở đây xác nhận Dockerized **load generators**, không full Controller/VuGen/Analysis ([Docker LG](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/dockerized_load_generator.htm) — truy cập 2026-07-14).
4. **Aviator tự sửa correlation chính xác?** Không; assistance phải qua replay, request snapshot, business assertions và raw evidence.
5. **Analysis percentile là ground truth?** Cần đúng patch/settings và raw cross-check vì có known issue ([Known issues](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/tl_Analysis.htm) — truy cập 2026-07-14).

</details>
