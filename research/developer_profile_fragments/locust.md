**1. Tổng quan.** **[DOC]** Locust là open-source Python load-testing framework có Web UI và headless mode. Official repository ghi Lars Holmberg là maintainer, Jonatan Heyman là creator; Microsoft được ghi nhận tài trợ/đóng góp cho maintenance. ([Locust repository](https://github.com/locustio/locust), [Stable docs](https://docs.locust.io/en/stable/) — truy cập 2026-07-14)

**2. Cost và licence.** **[DOC]** Locust dùng MIT licence; local/distributed OSS không đòi SaaS account. Current stable docs giới thiệu Azure Load Testing như hosted option, nhưng account/cost thuộc dịch vụ ngoài OSS. ([Repository/licence](https://github.com/locustio/locust), [Hosted load testing](https://docs.locust.io/en/stable/hosted-load-testing.html) — truy cập 2026-07-14) **[ASSUMPTION]** Access cho sinh viên cao khi dùng local runner.

**3. Installation và platform support.** **[DOC]** Official install dùng **pip install locust** hoặc uvx; trang cài có Windows troubleshooting và Docker alternative. Image **locustio/locust** cùng Docker Compose hỗ trợ standalone và master/worker. ([Installation](https://docs.locust.io/en/stable/installation.html), [Docker](https://docs.locust.io/en/stable/running-in-docker.html) — truy cập 2026-07-14) **[ASSUMPTION]** Cần pin Python/Locust/dependencies bằng lockfile hoặc image digest; strict offline cần wheel/image cache.

**4. Scripting hoặc configuration model.** **[DOC]** Locustfile là Python module; **HttpUser**, task/task weight, wait_time và on_start mô tả flow, modularization và per-user lifecycle, thuận lợi cho Git/code review. Mỗi User chạy trong một greenlet. **har2locust** chuyển HAR sang code nhưng được docs đánh dấu beta và output có thể không chính xác. ([Writing a locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14)

**5. Workload capabilities.** **[DOC]** Headless/Web UI điều khiển user count, spawn rate và run time; **LoadTestShape** cho stage/ramp/spike và user-class mix. ([Headless](https://docs.locust.io/en/stable/running-without-web-ui.html), [Custom shapes](https://docs.locust.io/en/stable/configuration.html#custom-load-shapes) — truy cập 2026-07-14) **constant_throughput** chỉ giới hạn task iterations và không tự tăng user để bù khi task chậm; open-arrival target cần care. ([Wait-time helpers](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14) Master/worker hỗ trợ nhiều process/máy; docs lưu ý thường dùng worker/core do GIL, còn **--processes** dựa trên fork và không chạy Windows. ([Distributed load](https://docs.locust.io/en/stable/running-distributed.html) — truy cập 2026-07-14)

**6. Assertions và validation.** **[DOC]** Với **catch_response=True**, Python có thể gọi response.failure/success dựa trên HTTP status, body hoặc business JSON. Headless mặc định trả exit 1 nếu có failed sample; docs minh họa events.quitting để gate fail ratio, average và p95 bằng process_exit_code. ([Validating responses](https://docs.locust.io/en/stable/writing-a-locustfile.html#validating-responses), [Headless exit policy](https://docs.locust.io/en/stable/running-without-web-ui.html) — truy cập 2026-07-14) **[ASSUMPTION]** Linh hoạt nhưng custom SLO gate cần nhiều code review hơn declarative threshold DSL.

**7. Metrics và reporting.** **[DOC]** Web UI hiển thị request count, failures, response times, RPS và running users. CLI CSV theo prefix tạo stats, stats_history, failures và exceptions; percentile list cấu hình có p50, p95, p99 và các mức khác. ([Quickstart](https://docs.locust.io/en/stable/quickstart.html), [Configuration/CSV](https://docs.locust.io/en/stable/configuration.html) — truy cập 2026-07-14) Raw CSV/log phải được giữ; screenshot UI chỉ là evidence phụ.

**8. CI/CD và automation.** **[DOC]** Headless mode là non-interactive runner, có run time và exit-code controls; official page đưa GitHub Actions example. Docker/Compose đóng gói standalone/master-worker. ([Headless/CI](https://docs.locust.io/en/stable/running-without-web-ui.html), [Docker](https://docs.locust.io/en/stable/running-in-docker.html) — truy cập 2026-07-14)

**9. EShop suitability.** **[DOC]** HttpSession bao quanh requests.Session, giữ cookies; HttpUser không render browser/assets. Python có thể parse JSON/token/ID và giữ state per user cho multi-step login → product → cart → checkout. ([Writing a locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14) **[ASSUMPTION]** EShop fit cao, nhưng CSV/account uniqueness giữa distributed workers, token refresh và cleanup cần thiết kế/EXP.

**10. AI-assisted potential.** Locust **không phải AI tool**. **[ASSUMPTION]** Python/HAR tạo bề mặt tốt cho AI draft tasks, correlation, data và quality-gate hook; har2locust beta là lý do không tin generated code mặc định. ([Writing a locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14) Human audit: side effects/dependencies, target/secret, user lifecycle, wait time/task weights, LoadTestShape, worker data uniqueness, response.failure và exit policy.

**11. Classroom suitability.** **[ASSUMPTION]** Web UI trực quan và Python phổ biến; activity ≤25 phút khả thi nếu venv/image đã chuẩn bị. Lớp phải hiểu greenlet/process, user loop và custom gate; thời gian thật là **[CẦN THỰC NGHIỆM]**. Local path không cần account/Internet sau khi dependencies được cache.

**12. Điểm mạnh trong phạm vi seminar.**

- **[DOC]** Full Python cho complex business logic/correlation, state và cookies per user. ([Locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14)
- **[DOC]** Web UI nhanh cho demo, headless/CSV tốt cho automation/evidence. ([Quickstart](https://docs.locust.io/en/stable/quickstart.html), [Configuration](https://docs.locust.io/en/stable/configuration.html) — truy cập 2026-07-14)
- **[DOC]** Custom LoadTestShape và master/worker hỗ trợ workload/distribution linh hoạt. ([Shapes](https://docs.locust.io/en/stable/configuration.html#custom-load-shapes), [Distributed](https://docs.locust.io/en/stable/running-distributed.html) — truy cập 2026-07-14)

**13. Hạn chế trong phạm vi seminar.**

- **[DOC]** HttpUser không phải browser. ([Locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14)
- **[DOC]** constant_throughput không tự bù user, nên actual RPS phải quan sát. ([Locustfile/wait helpers](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14)
- **[DOC]** p95/fail-ratio gate thường cần event hook; distributed path có GIL/process/Windows fork caveat. ([Headless](https://docs.locust.io/en/stable/running-without-web-ui.html), [Distributed](https://docs.locust.io/en/stable/running-distributed.html) — truy cập 2026-07-14)
- **[ASSUMPTION]** Arbitrary Python làm bề mặt dependency/side-effect review rộng; worker data uniqueness và generator saturation cần EXP.

**14. Smoke Test Plan.** **[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN; 0 EXP]**

- **Mục tiêu:** xác nhận package/import, một HttpUser gọi GET idempotent, response validation, CSV/log và exit.
- **Prerequisites:** authorized target; thay **[VERIFIED_BASE_URL]** và **[VERIFIED_PRODUCT_ENDPOINT]**; pin Python/Locust; tạo artifacts directory.
- **Installation/setup:** venv + locked requirements hoặc pinned official image; lưu Python/Locust versions, OS và Git commit.
- **Request/config mẫu:**

~~~python
from locust import HttpUser, task, between

class SmokeUser(HttpUser):
    wait_time = between(1, 1)

    @task
    def get_product(self):
        with self.client.get(
            "[VERIFIED_PRODUCT_ENDPOINT]",
            name="GET product",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"unexpected status: {response.status_code}"
                )
~~~

- **Command:** **locust -f locustfile.py --headless --users 1 --spawn-rate 1 --run-time 5s --host [VERIFIED_BASE_URL] --csv artifacts/locust-smoke**.
- **Kết quả mong đợi:** một user, ít nhất một valid sample, failure 0, exit 0, CSV files được tạo; user loop có thể phát hơn một request trong 5 giây, nên không gọi đây là exactly-one-request test.
- **Evidence cần thu:** Python/Locust/lock/image; script/hash; exact command; stdout/stderr; exit; mọi CSV; request count; timestamps; worker/process/machine/SUT metadata.
- **Lỗi có thể gặp:** venv/PATH, TLS/proxy/auth, run quá ngắn, CSV permission, host/path ghép sai, repeated side effect.
- **Tiêu chí thành công:** ít nhất một sample trong scope, failure 0, exit 0 và complete artifacts; muốn đúng một request phải thêm stop logic và xác minh riêng.

**15. Điểm đánh giá provisional.** Mọi điểm là **DOC + ASSUMPTION**, **không có EXP**.

| Tiêu chí | Điểm | Lý do, evidence và nguồn |
|---|---:|---|
| Cost & access (8%) | 5/5 | MIT/local OSS, account không bắt buộc. **DOC** ([repo](https://github.com/locustio/locust) — truy cập 2026-07-14) |
| Learning curve (8%) | 4/5 | Dễ với Python; lifecycle/gevent/distributed cần học. **DOC + ASSUMPTION** ([locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14) |
| EShop fit (15%) | 5/5 | HttpSession/cookie/state/Python correlation. **DOC + ASSUMPTION** ([locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14) |
| Multi-step journey (12%) | 5/5 | Sequential task/lifecycle/per-user state. **DOC** ([locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14) |
| Workload control (10%) | 4/5 | Users/spawn/custom shape; open-rate caveat. **DOC + ASSUMPTION** ([shapes](https://docs.locust.io/en/stable/configuration.html#custom-load-shapes) — truy cập 2026-07-14) |
| Assertions/checks (8%) | 4/5 | catch_response mạnh, SLO gate cần hook. **DOC** ([validation](https://docs.locust.io/en/stable/writing-a-locustfile.html#validating-responses), [headless](https://docs.locust.io/en/stable/running-without-web-ui.html) — truy cập 2026-07-14) |
| Reporting (8%) | 4/5 | Live UI + multi-file CSV; local polished HTML không là core path. **DOC** ([configuration](https://docs.locust.io/en/stable/configuration.html) — truy cập 2026-07-14) |
| CI/CD (7%) | 4/5 | Headless/exit/Actions; custom threshold glue. **DOC** ([headless](https://docs.locust.io/en/stable/running-without-web-ui.html) — truy cập 2026-07-14) |
| Reproducibility (7%) | 5/5 | Python/lock/config/CSV dễ version; pin workers/deps. **DOC + ASSUMPTION** |
| Local/offline (5%) | 5/5 | Runner/UI/workers local; cache dependencies. **DOC + ASSUMPTION** ([docs](https://docs.locust.io/en/stable/) — truy cập 2026-07-14) |
| AI-assisted potential (7%) | 5/5 | Python/HAR dễ draft/audit; tool không AI. **ASSUMPTION** ([locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14) |
| Classroom suitability (5%) | 4/5 | UI/Python tốt; process/custom gate cần thời gian. **ASSUMPTION** |
| Community (0%) | 5/5 | Current official docs, active repo, Discussions/Discord; không vào Weighted Score. **DOC** ([repo](https://github.com/locustio/locust), [docs](https://docs.locust.io/en/stable/) — truy cập 2026-07-14) |

**Weighted Score provisional: 90.8/100.** Chưa hiệu chỉnh bằng EXP.

**16. Kết luận sơ bộ.** **Shortlist.** Locust là Python counterfactual mạnh và có EShop fit cao; chưa được chọn vào pair chính vì code-first learning objective trùng nhiều với k6 và cần đối chứng arrival/gate/classroom time. Đây không phải đánh giá Locust yếu.

**17. Câu hỏi phản biện.**

<details>
<summary><strong>Câu hỏi phản biện</strong></summary>

### Câu 1. Vì sao không chọn Locust?

**Trả lời:** Không phải vì thiếu capability; pair chỉ có hai tool ưu tiên complementarity visual/Test Plan versus code-first. Locust vẫn phải là counterfactual smoke candidate.

### Câu 2. Locust có mô phỏng browser thật không?

**Trả lời:** Không; HttpUser giữ cookie ở HTTP layer nhưng không render/tải browser assets. ([Writing a locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14)

### Câu 3. constant_throughput bảo đảm đạt target RPS không?

**Trả lời:** Không; nó không tự tăng users để bù slow iterations, nên achieved RPS/dropped capacity phải đo. ([Writing a locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14)

### Câu 4. Nhiều workers có tự bảo đảm mỗi account CSV dùng đúng một lần?

**Trả lời:** Không; partition/queue/uniqueness là trách nhiệm test design và cần EXP.

</details>
