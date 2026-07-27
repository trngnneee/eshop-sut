**1. Tổng quan.** **[DOC]** Gatling là performance-testing engine/platform do Gatling Corp duy trì. Community engine hỗ trợ Java, JavaScript, TypeScript, Kotlin và Scala; không còn đúng nếu mô tả Gatling “chỉ có Scala”. ([Gatling repository](https://github.com/gatling/gatling), [Gatling documentation](https://docs.gatling.io/) — truy cập 2026-07-14)

**2. Cost và licence.** **[DOC]** Main open-source project dùng Apache-2.0, nhưng bundled Highcharts report module có licence riêng với phạm vi dùng/sửa giới hạn; Enterprise components có điều khoản riêng. Community chạy local miễn phí. Current Enterprise pricing niêm yết Basic từ 89 EUR/tháng khi annual hoặc 99 EUR monthly, Team từ 356/396 EUR và custom Enterprise; giá phải re-check trước nộp. ([Project licences](https://docs.gatling.io/project/licenses/project-licenses/), [Gatling pricing](https://gatling.io/pricing) — truy cập 2026-07-14) Trial self-service là 14 ngày với hạn mức chính thức. ([Trial plan](https://docs.gatling.io/evaluate-enterprise/trial-plan/) — truy cập 2026-07-14)

**3. Installation và platform support.** **[DOC]** Gatling chạy trên JVM; JVM SDK hỗ trợ Java/Kotlin/Scala và build tools Maven/Gradle/sbt. Current install docs hỗ trợ OpenJDK LTS 11–25. Current JS/TS route yêu cầu Node.js 24+ LTS và npm 11+. Official docs đang có documentation conflict: trang install vẫn nói JavaScript SDK chỉ HTTP, trong khi current gRPC/SSE/MQTT pages có JS/TS examples. Vì vậy phải pin version, protocol module và edition thay vì suy ra parity. ([Install local](https://docs.gatling.io/reference/deploy/install-local/), [gRPC JS/TS](https://docs.gatling.io/guides/use-cases/grpc-js/), [SSE](https://docs.gatling.io/reference/script/sse/), [MQTT](https://docs.gatling.io/reference/script/mqtt/protocol/) — truy cập 2026-07-14)

**4. Scripting hoặc configuration model.** **[DOC]** Typed DSL mô tả simulation, protocol, reusable chains/scenarios, feeders, checks, injection và assertions; source/build lockfiles phù hợp Git/code review. JS/TS file convention là **src/*.gatling.js** hoặc **src/*.gatling.ts**, chạy bằng npm CLI. ([Simulation](https://docs.gatling.io/concepts/simulation/), [JS CLI](https://docs.gatling.io/integrations/build-tools/js-cli/) — truy cập 2026-07-14) HTTP Recorder/HAR hỗ trợ authoring nhưng generated code vẫn cần human audit. ([HTTP reference/Recorder](https://docs.gatling.io/reference/script/http/) — truy cập 2026-07-14)

**5. Workload capabilities.** **[DOC]** Injection DSL phân biệt open và closed models: at-once/ramp users, constant/ramping users per second, stress peak, constant/ramp concurrent users; nhiều populations/scenarios có thể setUp cùng simulation. ([Injection](https://docs.gatling.io/concepts/injection/) — truy cập 2026-07-14) Session là map per VU; checks saveAs data cho bước sau. Feeders có CSV/JSON/sitemap/in-memory cùng queue/shuffle/random/circular; queue exhaustion làm run crash. ([Session](https://docs.gatling.io/concepts/session/api/), [Checks](https://docs.gatling.io/concepts/checks/), [Feeders](https://docs.gatling.io/concepts/session/feeders/) — truy cập 2026-07-14) HTTP cookies được xử lý tự động và có add/get/flush helpers. ([HTTP helpers](https://docs.gatling.io/reference/script/http/helpers/) — truy cập 2026-07-14)

**6. Assertions và validation.** **[DOC]** Request checks xác nhận status/body và capture correlation data. Simulation assertions đặt criteria global/forAll/details trên response time, failed/successful requests, RPS và percentiles; nếu ít nhất một assertion fail thì simulation fail, và official glossary mô tả error status code cho toàn test. ([Checks](https://docs.gatling.io/concepts/checks/), [Assertions](https://docs.gatling.io/concepts/assertions/), [Glossary](https://docs.gatling.io/reference/glossary/) — truy cập 2026-07-14)

**7. Metrics và reporting.** **[DOC]** Community sinh portable static HTML report với response-time distribution/percentiles, OK/KO, concurrent users và requests/s. ([Community reports](https://docs.gatling.io/reference/stats/reports/oss/) — truy cập 2026-07-14) **simulation.log không phải stable raw API**: official FAQ gọi đây là undocumented implementation detail có thể đổi và khuyên không parse cho in-house integration; các internal stats/assertions JSON/XML cũ đã removed. ([Gatling FAQ](https://docs.gatling.io/tutorials/faq/) — truy cập 2026-07-14)

**8. CI/CD và automation.** **[DOC]** Community simulations chạy non-interactively qua Maven/Gradle/sbt/npm; assertions tạo build/error exit gate. Enterprise có official CI/CD integrations, distributed runs, dashboard và token/account path riêng. ([JS CLI](https://docs.gatling.io/integrations/build-tools/js-cli/), [CI/CD integrations](https://docs.gatling.io/integrations/ci-cd/) — truy cập 2026-07-14) **[ASSUMPTION]** Không thấy official Community Docker image tương đương k6 trong current install docs đã kiểm; container route cần nhóm pin JDK/build image và xác minh.

**9. EShop suitability.** **[ASSUMPTION dựa trên DOC]** Session, cookies, feeders, checks/saveAs, reusable chains và open/closed workload rất phù hợp login → product → cart → checkout. HTTP engine không phải browser: không chạy page JavaScript/CSS/UI events. ([HTTP protocol](https://docs.gatling.io/reference/script/http/protocol/) — truy cập 2026-07-14) Exact token/data/cleanup và SDK feature parity trên chosen language là **[CẦN THỰC NGHIỆM]**.

**10. AI-assisted potential.** Gatling core **không phải AI tool**. **[DOC]** Gatling Enterprise hiện có AI extensions/MCP và AI Analysis; MCP yêu cầu Enterprise account/API token, và official guidance vẫn yêu cầu engineering judgment. ([Gatling AI](https://docs.gatling.io/ai/), [MCP](https://gatling.io/product/mcp), [AI Analysis](https://gatling.io/product/ai-analysis), [AI-analysis guidance](https://gatling.io/blog/how-to-get-started-with-ai-analysis) — truy cập 2026-07-14) **[ASSUMPTION]** External AI có thể draft typed DSL, nhưng human audit phải kiểm imports/current SDK, session immutability, feeder exhaustion, correlation, workload model, assertions và secrets.

**11. Classroom suitability.** **[ASSUMPTION]** Typed DSL dạy workload/correlation rất tốt nhưng JVM/npm/build setup và language choice làm activity ≤25 phút khó hơn k6/Artillery nếu không preconfigure. Community local không cần account; Enterprise AI/dashboard cần account/Internet. Actual time là **[CẦN THỰC NGHIỆM]**.

**12. Điểm mạnh trong phạm vi seminar.**

- **[DOC]** Open/closed injection DSL rất rộng và explicit. ([Injection](https://docs.gatling.io/concepts/injection/) — truy cập 2026-07-14)
- **[DOC]** Session/feeders/checks/saveAs giải quyết stateful journey và data. ([Session](https://docs.gatling.io/concepts/session/api/), [Feeders](https://docs.gatling.io/concepts/session/feeders/) — truy cập 2026-07-14)
- **[DOC]** Assertions + error exit và portable HTML tốt cho automation/reporting. ([Assertions](https://docs.gatling.io/concepts/assertions/), [Reports](https://docs.gatling.io/reference/stats/reports/oss/) — truy cập 2026-07-14)
- **[DOC]** Đa ngôn ngữ JVM/JS/TS cho phép khớp skillset của nhóm. ([Install](https://docs.gatling.io/reference/deploy/install-local/) — truy cập 2026-07-14)

**13. Hạn chế trong phạm vi seminar.**

- **[DOC]** Official install page và protocol guides không nhất quán về JS/TS scope; pin version/module/edition và smoke-test parity. ([Install](https://docs.gatling.io/reference/deploy/install-local/), [gRPC JS/TS](https://docs.gatling.io/guides/use-cases/grpc-js/), [SSE](https://docs.gatling.io/reference/script/sse/), [MQTT](https://docs.gatling.io/reference/script/mqtt/protocol/) — truy cập 2026-07-14)
- **[DOC]** simulation.log không phải stable integration contract. ([FAQ](https://docs.gatling.io/tutorials/faq/) — truy cập 2026-07-14)
- **[DOC]** Highcharts report licence khác main Apache licence; advanced Enterprise features có cost/account. ([Licences](https://docs.gatling.io/project/licenses/project-licenses/), [Pricing](https://gatling.io/pricing) — truy cập 2026-07-14)
- **[ASSUMPTION]** Build/typed DSL learning cost và lack of confirmed official Community image có thể làm live setup dài; cần EXP.

**14. Smoke Test Plan.** **[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN; 0 EXP]**

- **Mục tiêu:** xác nhận current JS SDK, one VU/GET, status check, global assertion, local HTML và exit.
- **Prerequisites:** authorized target; Node 24+ LTS/npm11+; pinned official JS starter + lockfile; thay placeholders.
- **Installation/setup:** npm install từ lockfile; ghi Node/npm/Gatling versions, OS, Git commit.
- **Request/config mẫu — src/smokeSimulation.gatling.js:**

~~~javascript
import {
  simulation,
  scenario,
  atOnceUsers,
  global,
} from "@gatling.io/core";
import { http, status } from "@gatling.io/http";

export default simulation((setUp) => {
  const protocol = http.baseUrl("[VERIFIED_BASE_URL]");
  const scn = scenario("smoke").exec(
    http("GET product")
      .get("[VERIFIED_PRODUCT_ENDPOINT]")
      .check(status().is(200))
  );

  setUp(scn.injectOpen(atOnceUsers(1)))
    .protocols(protocol)
    .assertions(global().failedRequests().count().is(0));
});
~~~

- **Command:** **npx gatling run --simulation smokeSimulation**. Current JS CLI supports selecting simulation by filename stem. ([JS CLI](https://docs.gatling.io/integrations/build-tools/js-cli/) — truy cập 2026-07-14)
- **Kết quả mong đợi:** one VU/request, check/assertion pass, exit 0, portable HTML dưới target/gatling; chưa quan sát.
- **Evidence cần thu:** Node/npm/Gatling/lock versions; script/hash; exact command; stdout/stderr; exit; full HTML folder; build log; timestamps; machine/SUT metadata.
- **Lỗi có thể gặp:** Node/npm version, package cache/network, file naming/location, SDK syntax, TLS/auth, assertion fail, report permission.
- **Tiêu chí thành công:** exactly one request trong report, status/global assertion đạt, exit 0, HTML/log/config evidence đầy đủ.

**15. Điểm đánh giá provisional.** Mọi điểm là **DOC + ASSUMPTION**, **không có EXP**.

| Tiêu chí | Điểm | Lý do, evidence và nguồn |
|---|---:|---|
| Cost & access (8%) | 4/5 | Free Community, nhưng Highcharts nuance/Enterprise cost. **DOC** ([licences](https://docs.gatling.io/project/licenses/project-licenses/), [pricing](https://gatling.io/pricing) — truy cập 2026-07-14) |
| Learning curve (8%) | 3/5 | JVM/npm/build + typed DSL. **DOC + ASSUMPTION** ([install](https://docs.gatling.io/reference/deploy/install-local/) — truy cập 2026-07-14) |
| EShop fit (15%) | 5/5 | HTTP/session/feeders/checks. **DOC + ASSUMPTION** ([session](https://docs.gatling.io/concepts/session/api/), [feeders](https://docs.gatling.io/concepts/session/feeders/) — truy cập 2026-07-14) |
| Multi-step journey (12%) | 5/5 | saveAs/session/reusable chains. **DOC** ([checks](https://docs.gatling.io/concepts/checks/) — truy cập 2026-07-14) |
| Workload control (10%) | 5/5 | Rich explicit open/closed profiles. **DOC** ([injection](https://docs.gatling.io/concepts/injection/) — truy cập 2026-07-14) |
| Assertions/checks (8%) | 5/5 | Request checks + global/detail assertions/error exit. **DOC** ([assertions](https://docs.gatling.io/concepts/assertions/) — truy cập 2026-07-14) |
| Reporting (8%) | 4/5 | Strong static HTML; raw log not stable contract. **DOC** ([reports](https://docs.gatling.io/reference/stats/reports/oss/), [FAQ](https://docs.gatling.io/tutorials/faq/) — truy cập 2026-07-14) |
| CI/CD (7%) | 5/5 | Build-tool/npm CLI + assertion gate. **DOC** ([JS CLI](https://docs.gatling.io/integrations/build-tools/js-cli/) — truy cập 2026-07-14) |
| Reproducibility (7%) | 5/5 | Typed code/build lock/static report. **DOC + ASSUMPTION** |
| Local/offline (5%) | 5/5 | Community local/standalone offline path. **DOC** ([install](https://docs.gatling.io/reference/deploy/install-local/) — truy cập 2026-07-14) |
| AI-assisted potential (7%) | 4/5 | Code + official Enterprise AI/MCP, gated và human-reviewed. **DOC + ASSUMPTION** ([AI](https://docs.gatling.io/ai/), [MCP](https://gatling.io/product/mcp) — truy cập 2026-07-14) |
| Classroom suitability (5%) | 3/5 | Learning value cao nhưng setup/DSL nặng hơn. **ASSUMPTION** |
| Community (0%) | 5/5 | Current official docs, repo và forum; không vào Weighted Score. **DOC** ([docs](https://docs.gatling.io/), [repo](https://github.com/gatling/gatling) — truy cập 2026-07-14) |

**Weighted Score provisional: 90.2/100.** Chưa hiệu chỉnh bằng EXP.

**16. Kết luận sơ bộ.** **Shortlist.** Gatling có workload/assertion capability rất mạnh và là đối chứng quan trọng; chưa chọn pair chính vì typed/build learning path có thể giảm classroom throughput và vai trò code-first trùng k6. Không kết luận Gatling yếu hơn tuyệt đối.

**17. Câu hỏi phản biện.**

<details>
<summary><strong>Câu hỏi phản biện</strong></summary>

### Câu 1. Vì sao không chọn Gatling?

**Trả lời:** Không phải do capability; pair ưu tiên complementarity và activity time. Cần measured 25-minute trial trước khi loại khỏi final shortlist.

### Câu 2. Gatling hiện chỉ viết Scala phải không?

**Trả lời:** Không; official docs hỗ trợ Java, Kotlin, Scala, JavaScript và TypeScript. Protocol parity cần pin theo version/module/edition vì install page và current gRPC/SSE/MQTT pages đang conflict. ([Install](https://docs.gatling.io/reference/deploy/install-local/), [gRPC JS/TS](https://docs.gatling.io/guides/use-cases/grpc-js/) — truy cập 2026-07-14)

### Câu 3. Có thể parse simulation.log làm raw integration ổn định?

**Trả lời:** Không; official FAQ gọi nó là undocumented implementation detail có thể đổi. ([FAQ](https://docs.gatling.io/tutorials/faq/) — truy cập 2026-07-14)

### Câu 4. Toàn bộ Gatling có Apache-2.0 không?

**Trả lời:** Không; main project là Apache-2.0 nhưng Highcharts report module và Enterprise components có licence riêng. ([Licences](https://docs.gatling.io/project/licenses/project-licenses/) — truy cập 2026-07-14)

</details>
