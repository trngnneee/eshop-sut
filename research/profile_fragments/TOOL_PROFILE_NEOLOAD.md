### 1. Tổng quan

NeoLoad là commercial performance platform của Tricentis, có protocol + RealBrowser, no-code/as-code, desktop/Web, CLI/API và cloud/on-prem execution ([NeoLoad](https://www.tricentis.com/products/performance-testing-neoload) — truy cập 2026-07-14). Evidence: `DOC`.

### 2. Cost và licence

Giá niêm yết từ 20.000 USD/năm, gồm 300 VU; có “Try for free” và Free Edition. Không-key mode chỉ design/analyze, không launch; exact current Free run cap không rõ trong public docs: `[CẦN XÁC MINH ENTITLEMENT]` ([Pricing](https://www.tricentis.com/products/performance-testing-neoload/pricing), [Manage licenses](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/manage_licenses.htm), [Quick Start](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/quick_start_guide.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 3. Installation và platform support

Controller/components hỗ trợ Windows/Linux/macOS theo matrix và Java 21; có built-in Load Generator/Monitoring Agent, remote agents, official container/Kubernetes deployment ([System requirements](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/system_requirements.htm), [Install Controller](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/install_the_controller.htm), [Deployment](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/deployment_considerations.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 4. Scripting hoặc configuration model

Record/import API → User Paths → Populations → Scenarios. User Path có Init/Actions/End; YAML/JSON as-code trộn với `.nlp`; JavaScript Action mở rộng logic. Git-friendly nhất khi commit YAML/data schema/environment overrides, không commit secret ([Get started](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/get_started.htm), [As-code](https://docs.tricentis.com/neoload-2026.1/en-us/content/user_guides.htm/neoload_as_code/executing_yaml_based_projects.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 5. Workload capabilities

Populations trộn User Paths theo %, có pacing; policies Constant/Ramp-up/Peaks/Custom và distributed agents/infrastructure override. Variables hỗ trợ CSV, unique/sequential/random; extractors/automatic dynamic-parameter handling làm correlation/session. Public section được kiểm tra chưa chứng minh open arrival-rate executor tương đương: `[CẦN XÁC MINH]` ([Populations](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/create_populations.htm), [Load policy](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/load_variation_policy.htm), [Variables](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/variables_and_fuctions.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 6. Assertions và validation

Validation kiểm tra duration, content length/body, XPath, JSONPath; SLA profiles đặt threshold và test status ([Validation](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/validation.htm), [SLA profiles](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/service_level_agreement_sla_profiles.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 7. Metrics và reporting

Test Summary có request/s, error rate, min/avg/max, stddev, throughput và ba percentile cấu hình 0,1–99,9. CLI xuất raw transactions, HTML/PDF/XML và SLA JUnit XML ([Test Summary](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/test_summary.htm), [Controller CLI](https://docs.tricentis.com/neoload-2026.1/en-us/content/get_started/start_the_controller.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 8. CI/CD và automation

`NeoLoadCmd -project ... -launch ... -noGUI -report ... -exportRaw ...`; exit `0=PASSED`, `1=FAILED` do SLA, `2=ERROR`; `-exitCodeFailIgnore` có thể ép 0 nên pipeline phải cấm nếu không được review. Có Jenkins và APIs ([Controller CLI](https://docs.tricentis.com/neoload-2026.1/en-us/content/get_started/start_the_controller.htm), [Jenkins](https://docs.tricentis.com/neoload-latest/en-us/content/user_guides.htm/integrate_with_third_party_tools/jenkins/jenkins.htm), [APIs](https://docs.tricentis.com/neoload-latest/en-us/content/apis/api_overview.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 9. EShop suitability

Rất mạnh cho Web/API journey, login/token, data, population mix, validation/SLA, report và CI; local agents có thể gọi EShop private. Cost/entitlement làm giảm seminar fit, không giảm enterprise capability. Evidence: `DOC` + fit `ASSUMPTION`.

### 10. AI-assisted potential

Product page công bố Agentic Performance Testing, AI Chat/MCP và Augmented Analysis. YAML/JS thuận lợi human audit; availability theo plan/data residency và correctness vẫn cần xác minh. Nghiên cứu không gọi NeoLoad AI ([NeoLoad](https://www.tricentis.com/products/performance-testing-neoload) — truy cập 2026-07-14). Evidence: `DOC` + governance `ASSUMPTION`.

### 11. Classroom suitability

GUI/no-code dễ trình diễn, nhưng entry price, entitlement, Java/resources và account làm khó tái lập toàn lớp trong 25 phút; cần pre-install/license. `[CẦN THỰC NGHIỆM]`. Evidence: `ASSUMPTION` từ DOC.

### 12. Điểm mạnh trong phạm vi seminar

GUI + as-code; validation/SLA; explicit CI exit codes; configurable percentiles/raw export; agents/container; native AI ([NeoLoad docs](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/get_started.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 13. Hạn chế trong phạm vi seminar

Giá từ 20.000 USD/năm; Free cap chưa rõ; environment/license nặng; arrival equivalence cần xác minh; AI/cloud tăng governance/data dependency. Evidence: `DOC`/`ASSUMPTION` đã đánh dấu.

### 14. Smoke Test Plan

**[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN]**

- **Mục tiêu:** 1 GET, validation/SLA, raw/HTML/JUnit và exit code.
- **Prerequisites:** supported OS/Java, installer checksum, Free/trial entitlement screenshot redacted, `[VERIFIED_BASE_URL]`, quyền test.
- **Installation/setup:** cài Controller; User Path GET + validation; Population 1; Scenario `Smoke`, 1 VU/1 iteration; SLA rõ.
- **Request:** `GET [VERIFIED_BASE_URL]/[VERIFIED_READ_ONLY_PATH]`.
- **Command/config:** `NeoLoadCmd -project ...\smoke.nlp -launch Smoke -noGUI -report ...\smoke.html -exportRaw ...\raw.csv -SLAJUnitReport ...\junit.xml` ([CLI](https://docs.tricentis.com/neoload-2026.1/en-us/content/get_started/start_the_controller.htm) — truy cập 2026-07-14).
- **Kết quả mong đợi:** exit 0, validation/SLA pass và ba artefact; chưa quan sát.
- **Evidence:** version/entitlement, `.nlp`/YAML, command/env, stdout/stderr/exit, HTML/raw/JUnit.
- **Lỗi có thể gặp:** no license (exit 2), Java/resource, agent certificate, TLS/proxy, wrong extraction/validation, report path.
- **Tiêu chí thành công:** request + validation/SLA + artefacts đạt; marker/SLA sai phải cho exit 1; không dùng `-exitCodeFailIgnore`.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Lý do | Evidence |
|---|---:|---:|---|---|
| Cost & access | 8% | 2 | 20k USD/year; free cap cần xác minh | DOC |
| Learning curve | 8% | 4 | GUI/no-code + as-code; infra vẫn phức tạp | ASSUMPTION từ DOC |
| EShop fit | 15% | 5 | Full journey/state/data/SLA | DOC + ASSUMPTION |
| Multi-step journey & state | 12% | 5 | Init/Actions/End/extractor/data | DOC |
| Workload model & scalability | 10% | 4 | Policies/agents; arrival gap | DOC + ASSUMPTION |
| Assertions & business validation | 8% | 5 | Body/XPath/JSONPath/SLA | DOC |
| Metrics & reporting | 8% | 5 | Percentiles/raw/multi-format | DOC |
| CI/CD & automation | 7% | 5 | Headless/JUnit/Jenkins/API/exit 0-1-2 | DOC |
| Reproducibility | 7% | 5 | YAML/JSON/Git/CLI overrides | DOC |
| Local/offline | 5% | 4 | On-prem agents/offline lease; cloud features ngoài | DOC + ASSUMPTION |
| AI-assisted potential | 7% | 5 | Native agentic/AI/augmented + text artefacts | DOC + ASSUMPTION |
| Classroom suitability | 5% | 2 | Cost/license/resource khó nhân rộng | ASSUMPTION |
| Community | 0% | 4 | Current 2026 docs/API/support ecosystem ([Docs](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/get_started.htm) — truy cập 2026-07-14) | DOC; không tính |

**Weighted Score provisional: 87,6/100; 0 EXP.**

### 16. Kết luận sơ bộ

**Survey-only** / enterprise alternative. Capability mạnh nhưng không vượt access/reproducibility blocker của live seminar.

### 17. Câu hỏi phản biện

<details>
<summary><strong>Câu hỏi phản biện NeoLoad</strong></summary>

1. **Free có bao nhiêu VU?** Current public docs không cho cap đủ chắc; phải dùng entitlement screenshot, không số từ version cũ.
2. **Giá cao mà điểm gần JMeter có thiên vị?** Ma trận tách capability khỏi cost/classroom; classification vẫn Survey-only.
3. **Ramp 100 VU/phút = 100 arrivals/phút?** Không được đồng nhất; concurrency ramp khác arrival, cần experiment.
4. **Native AI làm script đúng?** Không; vẫn phải audit extraction, workload, SLA và raw results.

</details>
