**1. Tổng quan.** **[DOC]** Artillery là developer-oriented load-testing toolkit do Artillery Software Inc. duy trì; test có thể viết bằng YAML, JavaScript hoặc TypeScript và các engine chính thức bao gồm HTTP, WebSocket, Socket.IO cùng Playwright. Mục tiêu phù hợp nhất ở đây là test-as-code/API load và CI automation. ([Artillery repository](https://github.com/artilleryio/artillery), [Test scripts](https://www.artillery.io/docs/reference/test-script) — truy cập 2026-07-14)

**2. Cost và licence.** **[DOC]** Phần lớn repository dùng MPL-2.0, nhưng một số Azure-specific modules dùng BSL và production/commercial use trên Azure có điều kiện licence riêng; do đó không nên mô tả toàn bộ distribution là “MPL thuần”. Local CLI là open-source; Artillery Cloud là tùy chọn có Free và paid plans/hạn mức theo trang giá hiện hành. ([Repository/licence notice](https://github.com/artilleryio/artillery), [Artillery pricing](https://www.artillery.io/pricing) — truy cập 2026-07-14) **[ASSUMPTION]** Sinh viên có thể làm activity local không cần Cloud account nếu package/image đã chuẩn bị trước.

**3. Installation và platform support.** **[DOC]** Official getting-started hỗ trợ Windows, macOS và Linux, yêu cầu một bản Node.js LTS gần nhất và cho phép chạy bằng **npx artillery@latest**; image **artilleryio/artillery** có latest/version tags. ([Get Artillery](https://www.artillery.io/docs/get-started/get-artillery), [Docker](https://www.artillery.io/docs/docker) — truy cập 2026-07-14) **[ASSUMPTION]** Setup ngắn nếu pre-install/pin package, nhưng offline classroom cần npm cache hoặc image đã kéo sẵn.

**4. Scripting hoặc configuration model.** **[DOC]** Test có hai phần **config** và **scenarios**; YAML phù hợp quick activity, còn JS/TS và processor/hooks phục vụ modularization, logic custom, environment variables và version control. ([Test scripts](https://www.artillery.io/docs/reference/test-script) — truy cập 2026-07-14)

**5. Workload capabilities.** **[DOC]** Phases hỗ trợ constant arrival rate, linear **rampTo**, fixed **arrivalCount**, pause và **maxVusers** để cap concurrency; scenario weights tạo nhiều hành vi. HTTP VU giữ cookies, có think time, CSV/variables, capture JSONPath/XPath/regex/header/CSS cho correlation. ([Test-script load phases](https://www.artillery.io/docs/reference/test-script), [HTTP engine](https://www.artillery.io/docs/reference/engines/http), [Examples/data](https://www.artillery.io/docs/get-started/examples) — truy cập 2026-07-14) **[ASSUMPTION]** Đây là workload arrival-oriented; maxVusers là cap chứ không thay thế đầy đủ một closed concurrent-user model. Distributed AWS/Azure thuộc đường Cloud và chịu plan/licence tương ứng. ([Artillery pricing](https://www.artillery.io/pricing) — truy cập 2026-07-14)

**6. Assertions và validation.** **[DOC]** Plugin **expect** kiểm status/body/header/JMESPath nhưng chỉ dùng với HTTP engine và không tương thích before/after hooks. Plugin **ensure** đặt metric threshold/condition và làm CLI trả non-zero khi strict condition fail. HTTP 5xx hoặc network timeout không mặc định bảo đảm exit non-zero, nên CI phải cấu hình expect/ensure rõ. ([Expect](https://www.artillery.io/docs/reference/extensions/expect), [Ensure](https://www.artillery.io/docs/reference/extensions/ensure), [Exit codes](https://www.artillery.io/docs/reference/cli/exit-codes) — truy cập 2026-07-14)

**7. Metrics và reporting.** **[DOC]** Console có snapshot và final summary; metrics gồm request/error/VU/rate cùng min, max, mean, median, p50, p75, p90, p95, p99 và p999. **--output** lưu JSON gồm intermediate và aggregate result. Lệnh local HTML **artillery report** đã bị loại từ v2.0.22; web dashboard/report hiện thuộc Artillery Cloud. ([Reported metrics](https://www.artillery.io/docs/reference/reported-metrics), [Run/output](https://www.artillery.io/docs/reference/cli/run), [Report command removal](https://www.artillery.io/docs/reference/cli/report) — truy cập 2026-07-14)

**8. CI/CD và automation.** **[DOC]** Artillery có CLI non-interactive, official Docker image và guides cho GitHub Actions, GitLab, Jenkins, Azure, AWS CodeBuild và CircleCI; ensure là quality gate phù hợp pipeline. ([CI/CD guides](https://www.artillery.io/docs/cicd), [Ensure](https://www.artillery.io/docs/reference/extensions/ensure), [Docker](https://www.artillery.io/docs/docker) — truy cập 2026-07-14)

**9. EShop suitability.** **[ASSUMPTION dựa trên DOC]** HTTP cookies, capture, data variables, weighted multi-step flow và local target phù hợp login → product → cart → checkout; processor dùng khi business logic phức tạp. ([HTTP engine](https://www.artillery.io/docs/reference/engines/http), [Test scripts](https://www.artillery.io/docs/reference/test-script) — truy cập 2026-07-14) Endpoint, token refresh, data uniqueness và cleanup thật vẫn là **[CẦN THỰC NGHIỆM]**.

**10. AI-assisted potential.** Artillery **không phải AI tool**. **[ASSUMPTION]** AI có thể draft YAML/TS, capture, expect/ensure, workload và tóm tắt JSON vì artefact là text-as-code; homepage cũng định vị workflow với coding agents. ([Artillery homepage](https://www.artillery.io/) — truy cập 2026-07-14) Human audit bắt buộc cho target/secret, arrival-versus-concurrency intent, data uniqueness, hooks, expect-versus-ensure, Failure Modes và Cloud upload.

**11. Classroom suitability.** **[ASSUMPTION]** YAML ngắn và CLI feedback phù hợp activity ≤25 phút nếu Node/package/image được pre-install; activity không cần account nhưng Cloud dashboard cần Internet/account. Thời gian thật chưa đo: **[CẦN THỰC NGHIỆM]**.

**12. Điểm mạnh trong phạm vi seminar.**

- **[DOC]** YAML/JS/TS dễ version-control; workload phases và HTTP capture/cookies rõ. ([Test scripts](https://www.artillery.io/docs/reference/test-script), [HTTP engine](https://www.artillery.io/docs/reference/engines/http) — truy cập 2026-07-14)
- **[DOC]** Raw JSON, official Docker và CI guides tạo evidence/automation tốt. ([Run/output](https://www.artillery.io/docs/reference/cli/run), [CI/CD](https://www.artillery.io/docs/cicd) — truy cập 2026-07-14)
- **[DOC]** Playwright là browser layer tùy chọn; protocol load vẫn có thể giữ riêng. ([Playwright engine](https://www.artillery.io/docs/reference/engines/playwright) — truy cập 2026-07-14)

**13. Hạn chế trong phạm vi seminar.**

- **[DOC]** expect chỉ HTTP và xung đột before/after; failure cần ensure/exit policy rõ. ([Expect](https://www.artillery.io/docs/reference/extensions/expect), [Exit codes](https://www.artillery.io/docs/reference/cli/exit-codes) — truy cập 2026-07-14)
- **[DOC]** Local HTML command hiện không còn; polished web report phụ thuộc Cloud. ([Report command](https://www.artillery.io/docs/reference/cli/report) — truy cập 2026-07-14)
- **[ASSUMPTION]** Complex journey có thể làm YAML phân tán sang processor; arrival-centric model không biểu đạt closed concurrency trực tiếp như một số đối thủ.
- **[DOC]** Azure modules có licence nuance cần kiểm tra theo deployment. ([Repository](https://github.com/artilleryio/artillery) — truy cập 2026-07-14)

**14. Smoke Test Plan.** **[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN; 0 EXP]**

- **Mục tiêu:** xác nhận install, đúng một arrival/GET idempotent, status expectation, automated gate, JSON và exit code.
- **Prerequisites:** target được cấp quyền; thay **[VERIFIED_BASE_URL]** và **[VERIFIED_PRODUCT_ENDPOINT]**; pin Node/Artillery hoặc image; tạo artifacts directory.
- **Installation/setup:** cài local dependency từ lockfile hoặc dùng pinned official image; lưu Node version, Artillery version, OS, Git commit.
- **Request/config mẫu:**

~~~yaml
config:
  target: "[VERIFIED_BASE_URL]"
  phases:
    - duration: 1
      arrivalCount: 1
  plugins:
    expect:
      reportFailuresAsErrors: true
    ensure:
      conditions:
        - expression: "plugins.expect.failed == 0"
scenarios:
  - name: smoke
    flow:
      - get:
          url: "[VERIFIED_PRODUCT_ENDPOINT]"
          name: "GET product"
          expect:
            - statusCode: 200
~~~

- **Command:** **artillery run --output artifacts/artillery-smoke.json smoke.yml**.
- **Kết quả mong đợi:** một arrival, plugins.expect.failed = 0, strict ensure pass, exit 0, JSON được tạo; đây là expected result, không phải observation. ([Expect](https://www.artillery.io/docs/reference/extensions/expect), [Ensure](https://www.artillery.io/docs/reference/extensions/ensure) — truy cập 2026-07-14)
- **Evidence cần thu:** versions/lock/image digest; config/hash; exact command; stdout/stderr; exit code; raw JSON; timestamps/timezone; load-generator và SUT metadata.
- **Lỗi có thể gặp:** Node/PowerShell policy, npm/cache, plugin/metric-version mismatch, TLS/proxy/auth, output permission, target/path ghép sai.
- **Tiêu chí thành công:** đúng một arrival trong raw result, status/ensure đạt, exit 0, artifacts đầy đủ và không vượt authorized scope.

**15. Điểm đánh giá provisional.** Mọi điểm dưới đây là **DOC + ASSUMPTION**, **không có EXP**.

| Tiêu chí | Điểm | Lý do, evidence và nguồn |
|---|---:|---|
| Cost & access (8%) | 4/5 | OSS local, nhưng Azure licence nuance/Cloud limits. **DOC** ([repo](https://github.com/artilleryio/artillery), [pricing](https://www.artillery.io/pricing) — truy cập 2026-07-14) |
| Learning curve (8%) | 4/5 | YAML dễ bắt đầu; plugin/processor cần hướng dẫn. **DOC + ASSUMPTION** ([scripts](https://www.artillery.io/docs/reference/test-script) — truy cập 2026-07-14) |
| EShop fit (15%) | 5/5 | Cookie/capture/data/HTTP flow. **DOC + ASSUMPTION** ([HTTP engine](https://www.artillery.io/docs/reference/engines/http) — truy cập 2026-07-14) |
| Multi-step journey (12%) | 4/5 | Flow/capture/hooks tốt; logic phức tạp sang processor. **DOC + ASSUMPTION** ([HTTP engine](https://www.artillery.io/docs/reference/engines/http) — truy cập 2026-07-14) |
| Workload control (10%) | 4/5 | Arrival/ramp/count/cap mạnh; closed model hạn chế. **DOC + ASSUMPTION** ([phases](https://www.artillery.io/docs/reference/test-script) — truy cập 2026-07-14) |
| Assertions/checks (8%) | 4/5 | expect + ensure, nhưng là hai lớp và có caveat. **DOC** ([Expect](https://www.artillery.io/docs/reference/extensions/expect), [Ensure](https://www.artillery.io/docs/reference/extensions/ensure) — truy cập 2026-07-14) |
| Reporting (8%) | 4/5 | Rich console/JSON; local HTML removed. **DOC** ([metrics](https://www.artillery.io/docs/reference/reported-metrics), [report](https://www.artillery.io/docs/reference/cli/report) — truy cập 2026-07-14) |
| CI/CD (7%) | 5/5 | Official CI/Docker và non-zero ensure gate. **DOC** ([CI/CD](https://www.artillery.io/docs/cicd) — truy cập 2026-07-14) |
| Reproducibility (7%) | 5/5 | Text config + lock/image + raw JSON. **DOC + ASSUMPTION** ([run](https://www.artillery.io/docs/reference/cli/run) — truy cập 2026-07-14) |
| Local/offline (5%) | 4/5 | Local CLI/JSON; strict offline cần cache, no local HTML. **DOC + ASSUMPTION** ([install](https://www.artillery.io/docs/get-started/get-artillery), [report](https://www.artillery.io/docs/reference/cli/report) — truy cập 2026-07-14) |
| AI-assisted potential (7%) | 4/5 | Text/agent-friendly, nhưng tool không AI và cần audit. **ASSUMPTION** ([homepage](https://www.artillery.io/) — truy cập 2026-07-14) |
| Classroom suitability (5%) | 5/5 | YAML activity ngắn nếu pre-install; thời gian cần EXP. **ASSUMPTION** |
| Community (0%) | 4/5 | Official docs, repo và Discussions hiện hành; không vào Weighted Score. **DOC** ([docs](https://www.artillery.io/docs), [repo](https://github.com/artilleryio/artillery) — truy cập 2026-07-14) |

**Weighted Score provisional: 86.8/100.** Chênh lệch nhỏ chưa có ý nghĩa trước calibration/EXP.

**16. Kết luận sơ bộ.** **Shortlist.** Artillery là counterfactual code/config-first mạnh và rất phù hợp quick activity; chưa chọn làm pair chính vì vai trò trùng k6, local HTML đã removed và cần kiểm chứng workload/exit semantics trên EShop. Đây không phải kết luận Artillery “kém”.

**17. Câu hỏi phản biện.**

<details>
<summary><strong>Câu hỏi phản biện</strong></summary>

### Câu 1. Vì sao không chọn Artillery nếu YAML có vẻ dễ nhất?

**Trả lời:** Dễ authoring là một tiêu chí, không thay thế complementarity, local evidence path và workload semantics. Cần chạy cùng smoke/EShop workload trước quyết định cuối.

### Câu 2. HTTP 500 có tự làm pipeline fail không?

**Trả lời:** Không mặc định; official exit-code docs yêu cầu explicit checks/ensure để tạo non-zero gate. ([Exit codes](https://www.artillery.io/docs/reference/cli/exit-codes) — truy cập 2026-07-14)

### Câu 3. Artillery v2 còn tạo local HTML bằng artillery report không?

**Trả lời:** Không; command đã removed từ v2.0.22 và web-report path hiện là Cloud. ([Report command](https://www.artillery.io/docs/reference/cli/report) — truy cập 2026-07-14)

### Câu 4. AI draft YAML có đủ để gọi đây là AI tool không?

**Trả lời:** Không. AI-assisted potential chỉ đánh giá artefact dễ draft/audit; engine Artillery vẫn deterministic và script phải human review.

</details>
