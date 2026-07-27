**1. Tổng quan.** **[DOC]** Taurus, CLI tên **bzt**, là automation-friendly orchestration/convenience framework: nó thống nhất config, gọi executor và tổng hợp/report kết quả; **không phải load generator độc lập ngang hàng k6, Locust, Gatling hoặc Artillery**. Repository do tổ chức BlazeMeter duy trì; supported executors hiện gồm JMeter, Gatling, Locust, k6, Selenium, Playwright, Apiritif và nhiều tool khác. ([Taurus repository](https://github.com/Blazemeter/taurus), [Execution settings/executors](https://gettaurus.org/docs/ExecutionSettings/) — truy cập 2026-07-14)

**2. Cost và licence.** **[DOC]** Taurus dùng Apache-2.0 và local OSS không cần account. BlazeMeter report/cloud là tùy chọn có Free Starter và paid plans; Cloud provisioning cần API key. Repository hiện hiển thị release 1.16.51 ngày 2026-06-15, là tín hiệu activity chứ không phải bằng chứng chất lượng runtime. ([Taurus repository](https://github.com/Blazemeter/taurus), [BlazeMeter pricing](https://www.blazemeter.com/pricing), [Cloud provisioning](https://gettaurus.org/docs/Cloud/) — truy cập 2026-07-14)

**3. Installation và platform support.** **[DOC]** Official install dùng **pip install bzt**, có hướng dẫn Linux/macOS/Windows và image **blazemeter/taurus**. Docs nêu Python 3.7+; executor có dependency riêng, ví dụ Java/JMeter. ([Installation](https://gettaurus.org/docs/Installation/), [Docker installation](https://gettaurus.org/install/Installation/) — truy cập 2026-07-14) **[ASSUMPTION]** “Cài Taurus” chưa đồng nghĩa toàn stack sẵn sàng; reproducible setup phải pin Python, bzt, executor, runtime và plugins.

**4. Scripting hoặc configuration model.** **[DOC]** bzt nhận YAML/JSON, merge nhiều config, hỗ trợ CLI overrides và sinh merged/effective configs; text artefact phù hợp Git. Default executor là **jmeter**. ([Command line](https://gettaurus.org/docs/CommandLine/), [Config syntax](https://gettaurus.org/docs/ConfigSyntax/), [Execution settings](https://gettaurus.org/docs/ExecutionSettings/) — truy cập 2026-07-14)

**5. Workload capabilities.** **[DOC]** Common execution profile có concurrency, ramp-up, hold-for, iterations, throughput, steps và multiple executions. Support/semantics phụ thuộc executor. ([Execution settings/load profile](https://gettaurus.org/docs/ExecutionSettings/) — truy cập 2026-07-14) Khi chọn hoặc mặc định **executor: jmeter**, Taurus generate/modify/orchestrate plan nhưng **Apache JMeter là engine thực thi request và phát tải**; Taurus có thể auto-download JMeter/plugins nếu thiếu. Existing JMX/thread groups và YAML load settings có override/proportional rules riêng. ([JMeter executor](https://gettaurus.org/docs/JMeter/) — truy cập 2026-07-14)

**Abstraction cost — [ASSUMPTION dựa trên DOC]:** YAML ngắn che bớt engine complexity, nhưng feature parity và exact semantics khác giữa executors; debug phải đọc cả bzt log, executor log và generated script. Merged/effective config + generated JMX là evidence bắt buộc để biết test thực chạy. ([Artifacts](https://gettaurus.org/docs/ArtifactsDir/) — truy cập 2026-07-14)

**6. Assertions và validation.** **[DOC]** Với JMeter executor, request YAML hỗ trợ status/body/header, JSONPath/XPath assertions và extractors regex/boundary/JSONPath/CSS/XPath. Taurus **passfail** module đặt criteria trên failure/success, response code, average response time, percentiles và timeframe; có stop/continue, global/per-execution/per-scenario criteria. ([JMeter request/assertions](https://gettaurus.org/docs/JMeter/), [Pass/fail criteria](https://gettaurus.org/docs/PassFail/) — truy cập 2026-07-14)

**7. Metrics và reporting.** **[DOC]** Default console/final-stats có sample/failure, average, latency/connect và percentiles; optional JUnit XML, CSV/XML dump, InfluxDB và BlazeMeter online report. Artifacts chứa bzt.log, original/merged/effective config, executor stdout/stderr/log, JTL/LDJSON và generated executor scripts. ([Reporting](https://gettaurus.org/docs/Reporting/), [Artifacts directory](https://gettaurus.org/docs/ArtifactsDir/) — truy cập 2026-07-14)

**8. CI/CD và automation.** **[DOC]** bzt exit codes: 0 no problem, 1 generic error, 2 manual shutdown, 3 automatic shutdown như pass/fail hoặc Cloud failure. JUnit XML có thể dùng pass-fail data source; official knowledge base có Jenkins integration, Docker image nhận config/mount artifacts. ([Command-line exit codes](https://gettaurus.org/docs/CommandLine/), [Reporting/JUnit](https://gettaurus.org/docs/Reporting/), [Jenkins](https://gettaurus.org/kb/Jenkins/), [Docker](https://gettaurus.org/install/Installation/) — truy cập 2026-07-14)

**9. EShop suitability.** **[DOC]** Request YAML có method/body/headers/think-time, data sources, extractors, assertions và include-scenario composition; option availability khác theo executor. ([JMeter executor](https://gettaurus.org/docs/JMeter/), [Data sources](https://gettaurus.org/docs/DataSources/), [Include scenario example](https://gettaurus.org/docs/Gatling/) — truy cập 2026-07-14) **[ASSUMPTION]** Với explicit JMeter executor, EShop journey khả thi, nhưng cookie/session/correlation thật do JMeter/generated plan xử lý; phải inspect JMX, không giả định Taurus có independent cookie engine.

**10. AI-assisted potential.** Taurus **không phải AI tool**. **[ASSUMPTION]** Unified YAML dễ cho AI draft/review và compare executors; repository có CLAUDE.md mô tả contributor architecture cho coding agent, nhưng không chứng minh end-user test tự đúng. ([Taurus CLAUDE.md](https://github.com/Blazemeter/taurus/blob/master/CLAUDE.md) — truy cập 2026-07-14) Human audit bắt buộc: executor/version, supported fields, generated JMX, plugins/JVM, auto-download, data/secrets, passfail placement, artifacts và Cloud upload.

**11. Classroom suitability.** **[ASSUMPTION]** YAML ngắn rất tốt để dạy orchestration/abstraction, nhưng dễ che JMeter semantics và thêm Python + Java + executor setup. Activity ≤25 phút chỉ khả thi nếu stack pre-pinned; cần **[CẦN THỰC NGHIỆM]**. Default provisioning là local; Cloud/account không cần cho local activity. ([Cloud/local provisioning](https://gettaurus.org/docs/Cloud/) — truy cập 2026-07-14)

**12. Điểm mạnh trong phạm vi seminar.**

- **[DOC]** Unified YAML cho nhiều executors và existing scripts. ([Execution settings](https://gettaurus.org/docs/ExecutionSettings/) — truy cập 2026-07-14)
- **[DOC]** Common passfail/reporting/exit/JUnit tạo automation layer rõ. ([PassFail](https://gettaurus.org/docs/PassFail/), [Reporting](https://gettaurus.org/docs/Reporting/), [CLI](https://gettaurus.org/docs/CommandLine/) — truy cập 2026-07-14)
- **[DOC]** Merged/effective config và generated artefacts hỗ trợ audit nếu được giữ đầy đủ. ([Artifacts](https://gettaurus.org/docs/ArtifactsDir/) — truy cập 2026-07-14)
- **[ASSUMPTION]** Có giá trị giảng dạy để minh họa abstraction benefit/cost và orchestration CI.

**13. Hạn chế trong phạm vi seminar.**

- **[DOC]** Capability/semantics phụ thuộc executor; Taurus không phải engine phát tải. ([Execution settings](https://gettaurus.org/docs/ExecutionSettings/), [JMeter executor](https://gettaurus.org/docs/JMeter/) — truy cập 2026-07-14)
- **[DOC]** Auto-download JMeter/plugins có thể gây version/network drift. ([JMeter executor](https://gettaurus.org/docs/JMeter/) — truy cập 2026-07-14)
- **[ASSUMPTION]** Debug complexity tăng vì phải đọc YAML → effective config → generated plan → engine log.
- **[DOC]** Strict offline cần preinstall/cache; **TAURUS_DISABLE_DOWNLOADS** làm Taurus error thay vì tải tool. ([Config syntax](https://gettaurus.org/docs/ConfigSyntax/) — truy cập 2026-07-14)
- **[ASSUMPTION]** Không được dùng score/throughput của Taurus mà không ghi executor/version/plugins/JVM.

**14. Smoke Test Plan — explicit JMeter executor.** **[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN; 0 EXP]**

- **Mục tiêu:** chứng minh Taurus orchestrate **JMeter**, 1 VU/1 iteration, request assertion, passfail, JUnit, artifacts và exit.
- **Prerequisites:** authorized target; pin Python/bzt/Java/JMeter/plugins; pre-cache; tạo writable artifacts; thay placeholders.
- **Installation/setup:** venv/pinned image; explicit **executor: jmeter**; trong offline run đặt TAURUS_DISABLE_DOWNLOADS; lưu all versions.
- **Request/config mẫu:**

~~~yaml
execution:
  - executor: jmeter
    concurrency: 1
    iterations: 1
    scenario: smoke

scenarios:
  smoke:
    requests:
      - url: "[VERIFIED_BASE_URL][VERIFIED_PRODUCT_ENDPOINT]"
        label: "GET product"
        method: GET
        assert:
          - contains:
              - "200"
            subject: http-code
            regexp: false

reporting:
  - final-stats
  - module: passfail
    criteria:
      - "fail>0%"
  - module: junit-xml
    filename: "xunit.xml"
    data-source: pass-fail
~~~

- **Command:** **bzt smoke.yml**.
- **Kết quả mong đợi:** Taurus generates/prepares JMX, JMeter executes one iteration, assertion/passfail pass, exit 0; JMX/JTL/log/merged/effective/JUnit artifacts exist. Nếu passfail automatic shutdown xảy ra, documented exit class là 3. ([JMeter](https://gettaurus.org/docs/JMeter/), [PassFail](https://gettaurus.org/docs/PassFail/), [Exit codes](https://gettaurus.org/docs/CommandLine/) — truy cập 2026-07-14)
- **Evidence cần thu:** Python/bzt/Java/JMeter/plugin/image versions; original YAML/hash; exact command/env; bzt.log; merged/effective YAML+JSON; generated/modified JMX; JMeter log/JTL; executor stdout/stderr; xunit.xml; exit; timestamps; machine/SUT metadata.
- **Lỗi có thể gặp:** Python/Java/JMeter mismatch, hidden auto-download/plugin resolution, YAML translation/override, assertion subject, reporter order/path, TLS/auth/permission.
- **Tiêu chí thành công:** evidence chứng minh JMeter executor, đúng one iteration/sample, assertion/passfail pass, exit 0 và không có unapproved download.

**15. Điểm đánh giá provisional — conditional on JMeter executor.** Mọi điểm là **DOC + ASSUMPTION**, **không có EXP**.

| Tiêu chí | Điểm | Lý do, evidence và nguồn |
|---|---:|---|
| Cost & access (8%) | 5/5 | Apache-2.0 local; Cloud optional. **DOC** ([repo](https://github.com/Blazemeter/taurus), [pricing](https://www.blazemeter.com/pricing) — truy cập 2026-07-14) |
| Learning curve (8%) | 4/5 | YAML ngắn, nhưng phải hiểu executor/generated plan. **DOC + ASSUMPTION** ([execution](https://gettaurus.org/docs/ExecutionSettings/) — truy cập 2026-07-14) |
| EShop fit (15%) | 4/5 | JMeter-backed request/extractor/data; executor-dependent. **DOC + ASSUMPTION** ([JMeter](https://gettaurus.org/docs/JMeter/) — truy cập 2026-07-14) |
| Multi-step journey (12%) | 4/5 | Requests/include/extractors tốt; parity cost. **DOC + ASSUMPTION** ([JMeter](https://gettaurus.org/docs/JMeter/), [data](https://gettaurus.org/docs/DataSources/) — truy cập 2026-07-14) |
| Workload control (10%) | 4/5 | Unified profile; exact semantics vary executor. **DOC** ([execution](https://gettaurus.org/docs/ExecutionSettings/) — truy cập 2026-07-14) |
| Assertions/checks (8%) | 4/5 | Request assertions + passfail; generated-engine semantics. **DOC** ([PassFail](https://gettaurus.org/docs/PassFail/) — truy cập 2026-07-14) |
| Reporting (8%) | 4/5 | Console/final/JUnit/CSV/XML/online, executor-dependent. **DOC** ([reporting](https://gettaurus.org/docs/Reporting/) — truy cập 2026-07-14) |
| CI/CD (7%) | 5/5 | bzt exit classes, JUnit, Docker/Jenkins. **DOC** ([CLI](https://gettaurus.org/docs/CommandLine/), [reporting](https://gettaurus.org/docs/Reporting/) — truy cập 2026-07-14) |
| Reproducibility (7%) | 5/5 | merged/effective config + generated scripts/artifacts. **DOC** ([artifacts](https://gettaurus.org/docs/ArtifactsDir/) — truy cập 2026-07-14) |
| Local/offline (5%) | 4/5 | Local default/disable downloads; pre-cache stack. **DOC + ASSUMPTION** ([Cloud](https://gettaurus.org/docs/Cloud/), [config](https://gettaurus.org/docs/ConfigSyntax/) — truy cập 2026-07-14) |
| AI-assisted potential (7%) | 4/5 | YAML/agent guidance; tool không AI, generated plan needs review. **ASSUMPTION** ([CLAUDE.md](https://github.com/Blazemeter/taurus/blob/master/CLAUDE.md) — truy cập 2026-07-14) |
| Classroom suitability (5%) | 3/5 | Orchestration lesson tốt; dễ che JMeter/setup semantics. **ASSUMPTION** |
| Community (0%) | 4/5 | Current docs/repo/support forum/release activity; không vào Weighted Score. **DOC** ([docs](https://gettaurus.org/docs/Index/), [repo](https://github.com/Blazemeter/taurus) — truy cập 2026-07-14) |

**Weighted Score provisional: 83.4/100, conditional on JMeter executor.** Không diễn giải là Taurus phát tải tốt hơn/kém hơn engine độc lập.

**16. Kết luận sơ bộ.** **Orchestration framework.** Giữ Taurus để minh họa unified YAML, pass/fail/reporting và CI orchestration; không chọn như load generator thứ hai. Nếu dùng JMeter executor, mọi claim execution/capacity phải ghi **Taurus + JMeter + version/plugins/JVM**.

**17. Câu hỏi phản biện.**

<details>
<summary><strong>Câu hỏi phản biện</strong></summary>

### Câu 1. Taurus có phải load generator không?

**Trả lời:** Không trong cách phân loại này; Taurus orchestrate executor. Với executor JMeter, JMeter mới thực thi request/phát tải. ([JMeter executor](https://gettaurus.org/docs/JMeter/) — truy cập 2026-07-14)

### Câu 2. Có thể so raw throughput Taurus trực tiếp với k6 không?

**Trả lời:** Không công bằng nếu không ghi underlying executor/version/plugins và không đo abstraction overhead; phải so tổ hợp Taurus+engine trên cùng logical workload.

### Câu 3. Một YAML có semantics giống nhau trên mọi executor không?

**Trả lời:** Không; supported settings/data/assertions và translation phụ thuộc executor. ([Execution settings](https://gettaurus.org/docs/ExecutionSettings/), [Data sources](https://gettaurus.org/docs/DataSources/) — truy cập 2026-07-14)

### Câu 4. Taurus có tự chạy offline sau pip install không?

**Trả lời:** Không bảo đảm; nó có thể auto-download JMeter/plugins. Cần pre-cache/pin và TAURUS_DISABLE_DOWNLOADS để phát hiện download. ([JMeter](https://gettaurus.org/docs/JMeter/), [Config syntax](https://gettaurus.org/docs/ConfigSyntax/) — truy cập 2026-07-14)

### Câu 5. Chỉ giữ smoke.yml có đủ reproducibility không?

**Trả lời:** Không; cần merged/effective config, generated JMX, engine/plugin versions, logs/JTL, exit và environment metadata. ([Artifacts](https://gettaurus.org/docs/ArtifactsDir/) — truy cập 2026-07-14)

</details>
