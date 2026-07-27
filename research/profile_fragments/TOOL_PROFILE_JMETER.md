### 1. Tổng quan

Apache JMeter là công cụ performance/load testing mã nguồn mở, thuần Java, do Apache Software Foundation duy trì. Nó tạo tải ở lớp protocol cho HTTP(S), REST/SOAP, JDBC, JMS, TCP và nhiều protocol khác; JMeter **không phải browser** và không thực thi JavaScript phía client ([Apache JMeter](https://jmeter.apache.org/) — truy cập 2026-07-14). Evidence: `DOC`.

### 2. Cost và licence

Apache License 2.0, không phí theo VU và không cần account/trial ([Apache Licenses](https://www.apache.org/licenses/) — truy cập 2026-07-14). Evidence: `DOC`.

### 3. Installation và platform support

Yêu cầu Java 8+, chạy trên OS có JVM tương thích. Apache khuyến nghị GUI để thiết kế/debug và non-GUI CLI để tạo tải ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html) — truy cập 2026-07-14). Không tìm thấy official Docker image trong nguồn Apache đã kiểm tra: `[CẦN XÁC MINH]`. Evidence: `DOC`; container gap: `ASSUMPTION`.

### 4. Scripting hoặc configuration model

Test Plan `.jmx` là XML/component tree; HTTP(S) Recorder ghi traffic. CSV Data Set, Cookie Manager, JSON/Regex/XPath extractor, `${variable}` và JSR223/Groovy hỗ trợ data/session/correlation/logic ([Recorder tutorial](https://jmeter.apache.org/usermanual/jmeter_proxy_step_by_step), [Component Reference](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14). Lưu Git được nhưng XML diff khó review hơn code thuần (`ASSUMPTION`).

### 5. Workload capabilities

Thread Group có VU/thread, ramp, loop, duration; timers điều khiển throughput; Open Model Thread Group hỗ trợ arrival schedule nhưng còn experimental. Remote testing dùng controller + nhiều engine, mỗi engine chạy toàn plan và phải đồng bộ JMeter/Java/data ([Component Reference](https://jmeter.apache.org/usermanual/component_reference.html), [Remote Testing](https://jmeter.apache.org/usermanual/remote-test.html) — truy cập 2026-07-14). Có multi-scenario, parameterization, correlation và cookie session. Evidence: `DOC`.

### 6. Assertions và validation

Response Assertion kiểm tra status/text/body/header/URL/size; có JSON/XPath assertions. Assertion làm sample fail, còn business invariant phải thiết kế riêng ([Component Reference](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14). Evidence: `DOC`.

### 7. Metrics và reporting

CSV/XML `.jtl`; Aggregate Report có latency/throughput/error/percentile; HTML dashboard có APDEX, failures, active threads, bytes throughput và ba percentile cấu hình được ([Generating Dashboard](https://jmeter.apache.org/usermanual/generating-dashboard.html), [Aggregate Report](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14). Phải lưu percentile properties để p50/p95/p99 tái lập. Evidence: `DOC`.

### 8. CI/CD và automation

`jmeter -n -t test.jmx -l results.jtl -e -o report`; dự án nêu Maven/Gradle/Jenkins integrations. Core CLI không công bố contract threshold exit-code, nên CI phải audit parser/wrapper và negative-test ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html), [JMeter](https://jmeter.apache.org/) — truy cập 2026-07-14). Evidence: `DOC`; gate: `[CẦN THỰC NGHIỆM]`.

### 9. EShop suitability

HTTP/API, login cookie, CSRF/token extractor, catalog → cart → checkout, CSV account/product và assertions đều có primitive; local runner gọi được EShop private. Không thay thế browser rendering/Web Vitals ([JMeter](https://jmeter.apache.org/), [Component Reference](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14). Evidence: `DOC` + fit `ASSUMPTION`.

### 10. AI-assisted potential

AI có thể draft/explain Groovy, extractor, assertion hoặc `.jmx`, nhưng XML lớn và workload semantics khó audit; không có native AI được Apache công bố. Human phải review endpoint, secret, data, think time, assertion và single-user replay. Evidence: `ASSUMPTION`; không gọi AI feature.

### 11. Classroom suitability

Không licence/account, đa nền tảng, GUI minh hoạ “Test Plan → CLI”. Activity 25 phút cần pre-install và endpoint/data; thời lượng là `[CẦN THỰC NGHIỆM]` ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html) — truy cập 2026-07-14). Evidence: `DOC` + `ASSUMPTION`.

### 12. Điểm mạnh trong phạm vi seminar

Miễn phí; local; recorder/state/correlation/assertion sâu; workload/distributed; raw JTL + HTML; có giá trị dạy visual design sang CLI ([JMeter manual](https://jmeter.apache.org/usermanual/) — truy cập 2026-07-14). Evidence: `DOC`.

### 13. Hạn chế trong phạm vi seminar

Không phải browser; GUI/listener overhead; `.jmx` verbose; remote RMI/data sync tăng setup; threshold CI cần lớp bổ sung ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html), [Remote Testing](https://jmeter.apache.org/usermanual/remote-test.html) — truy cập 2026-07-14). Evidence: `DOC`.

### 14. Smoke Test Plan

**[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN]**

- **Mục tiêu:** 1 GET, status/body assertion, JTL và HTML; không đo capacity.
- **Prerequisites:** Java `>=8`, binary/checksum, `[VERIFIED_BASE_URL]`, endpoint read-only và quyền test.
- **Installation/setup:** giải nén; ghi `java -version`, `jmeter -v`; GUI tạo 1 Thread/1 loop + HTTP Request + Response Assertion + Simple Data Writer.
- **Request:** `GET [VERIFIED_BASE_URL]/[VERIFIED_READ_ONLY_PATH]`.
- **Command/config:** `jmeter -n -t jmeter-smoke.jmx -l artifacts/jmeter-smoke.jtl -e -o artifacts/jmeter-report` ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html) — truy cập 2026-07-14).
- **Kết quả mong đợi:** một sample `success=true`, assertion đạt, JTL và `report/index.html`; chưa quan sát.
- **Evidence:** version/checksum, `.jmx`, command, stdout/stderr/exit, log, JTL, HTML, timestamp/timezone.
- **Lỗi có thể gặp:** Java mismatch, DNS/TLS/401/404, marker sai, output folder không rỗng, proxy/cookie sai.
- **Tiêu chí thành công:** status/body đúng, 0 assertion/transport error, đủ artefact; negative marker phải chứng minh CI nhận failure.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Lý do | Evidence |
|---|---:|---:|---|---|
| Cost & access | 8% | 5 | Apache 2.0, không account/VU fee | DOC |
| Learning curve | 8% | 3 | GUI tốt; correlation/thread model cần học | ASSUMPTION từ DOC |
| EShop fit | 15% | 5 | HTTP/state/data/assertion/local | DOC + ASSUMPTION |
| Multi-step journey & state | 12% | 5 | Cookie, extractor, CSV, controllers | DOC |
| Workload model & scalability | 10% | 5 | Thread/ramp/timers/open/remote | DOC |
| Assertions & business validation | 8% | 5 | Response/JSON/XPath | DOC |
| Metrics & reporting | 8% | 5 | JTL, percentile, throughput, HTML/APDEX | DOC |
| CI/CD & automation | 7% | 4 | Headless; threshold gate cần wrapper | DOC + ASSUMPTION |
| Reproducibility | 7% | 4 | `.jmx`/CSV/CLI; phải pin plugin/version | DOC + ASSUMPTION |
| Local/offline | 5% | 5 | Runner/report local | DOC |
| AI-assisted potential | 7% | 3 | Draft được, XML khó audit, không native | ASSUMPTION |
| Classroom suitability | 5% | 4 | Free/GUI nếu pre-install | ASSUMPTION |
| Community | 0% | 5 | Manual, source, mailing lists ([Mailing lists](https://jmeter.apache.org/mail.html) — truy cập 2026-07-14) | DOC; không tính |

**Weighted Score provisional: 90,2/100; 0 EXP.**

### 16. Kết luận sơ bộ

**Main candidate.** Quyết định theo seminar, phải qua smoke positive/negative và EShop Fit Test.

### 17. Câu hỏi phản biện

<details>
<summary><strong>Câu hỏi phản biện Apache JMeter</strong></summary>

1. **Chạy 1.000 VU trong GUI?** Không nên; Apache dành GUI cho design/debug và CLI cho load ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html) — truy cập 2026-07-14).
2. **1.000 thread = 1.000 request/s?** Không; thread là concurrency, throughput phụ thuộc response/think time/timer.
3. **Thay browser test SPA?** Không; JMeter không thực thi browser JavaScript ([JMeter](https://jmeter.apache.org/) — truy cập 2026-07-14).
4. **Exit 0 chắc SLA đạt?** Không; phải kiểm tra JTL/assertion và negative-test CI parser.

</details>
