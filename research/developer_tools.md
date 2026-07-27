# Nghiên cứu công cụ kiểm thử hiệu năng: nhóm developer-centric và orchestration

**Mốc kiểm chứng:** 2026-07-14 (Asia/Bangkok)  
**Phạm vi:** k6, Locust, Gatling, Artillery, Taurus  
**Bối cảnh:** EShop có journey đăng nhập → duyệt/tìm sản phẩm → xem chi tiết → thêm giỏ → checkout  
**Trạng thái:** **chưa chạy thực nghiệm**. Không có số đo, screenshot hay kết luận hiệu năng giả lập trong tài liệu này.

## Quy ước bằng chứng và rubric

- **DOC**: tài liệu, kho mã nguồn, giấy phép, pricing hoặc trang sản phẩm chính thức. Claim kiểm chứng được có link ngay sau claim.
- **EXP**: bằng chứng do nhóm chạy. Hồ sơ này chưa có EXP; vị trí cần chạy ghi **[CẦN THỰC NGHIỆM]**.
- **ASSUMPTION**: suy luận kỹ thuật hoặc đánh giá phù hợp; không phải claim của vendor.
- **[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**: lệnh/cấu hình dự kiến, không phải kết quả quan sát.
- Chỉ phát tải vào hệ thống được cấp quyền; URL đều là placeholder. Không benchmark các demo URL công cộng của vendor.

Điểm 1–5 và trọng số là đề xuất của nhóm, không phải rubric do vendor công bố. Công thức: **Weighted Score = tổng(điểm / 5 × trọng số)**, thang 0–100.

| Tiêu chí | Trọng số |
|---|---:|
| Cost & access | 8% |
| Learning curve | 8% |
| EShop fit | 15% |
| Multi-step journey | 12% |
| Workload control | 10% |
| Assertions/checks | 8% |
| Reporting | 8% |
| CI/CD | 7% |
| Reproducibility | 7% |
| Local/offline | 5% |
| AI-assisted potential | 7% |
| Classroom suitability | 5% |

> **Lưu ý bắt buộc:** Taurus là orchestration framework gọi executor bên dưới. Điểm Taurus mô tả trải nghiệm **Taurus + executor**, mặc định minh họa bằng JMeter; không phải điểm một load generator độc lập ngang hàng k6, Locust, Gatling hoặc Artillery.

---

# 1. k6

## 1.1 Overview, maintainer, licence, cost và access

k6 là công cụ load testing test-as-code do Grafana Labs duy trì, hỗ trợ tải tầng giao thức và browser testing. **(DOC; [k6 repository](https://github.com/grafana/k6), truy cập 2026-07-14; [k6 docs](https://grafana.com/docs/k6/latest/), truy cập 2026-07-14)**

Kho chính thức hiện cấp phép **AGPL-3.0**; bản CLI mã nguồn mở chạy local không cần tài khoản Cloud. **(DOC; [k6 repository and licence](https://github.com/grafana/k6), truy cập 2026-07-14)** Grafana Cloud k6 là tùy chọn; trang giá hiện có Free 0 USD với 500 VUh/tháng và các gói trả phí theo VUh/dịch vụ. Giá dễ đổi nên phải chụp lại khi nộp bài nếu dùng con số. **(DOC; [Grafana pricing](https://grafana.com/pricing/), truy cập 2026-07-14)**

**Provisional category:** **Main candidate** cho EShop API/backend; browser VU là lớp bổ sung có chủ đích, không phải mặc định để phát toàn bộ tải.

## 1.2 Install, platform, scripting và authoring

- Tài liệu cài đặt bao phủ Linux, macOS, Windows, binary độc lập và image Docker **grafana/k6**. **(DOC; [Install k6](https://grafana.com/docs/k6/latest/set-up/install-k6/), truy cập 2026-07-14)**
- Script dùng JavaScript nhưng chạy trên runtime riêng của k6, **không phải Node.js và không phải browser**; Node built-ins không mặc định tồn tại và npm compatibility phải được kiểm tra/bundle. **(DOC; [Write first test](https://grafana.com/docs/k6/latest/get-started/write-your-first-test/), truy cập 2026-07-14; [Modules](https://grafana.com/docs/k6/latest/using-k6/modules/), truy cập 2026-07-14)**
- k6 Studio có thể record browser flow/HAR, sinh và debug test trên Windows/macOS/Linux. HAR converter **har-to-k6** tạo điểm khởi đầu nhưng tài liệu yêu cầu chỉnh workload, data và correlation; browser-recorder extension cũ đã deprecated. **(DOC; [k6 Studio](https://grafana.com/docs/k6/latest/k6-studio/), truy cập 2026-07-14; [HAR converter](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-har-converter/), truy cập 2026-07-14; [Browser recorder status](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-browser-recorder/), truy cập 2026-07-14)**

## 1.3 Workload controls

Scenarios hỗ trợ shared/per-VU iterations, constant/ramping VUs, constant/ramping arrival rate; mỗi scenario có start time, hàm, environment và tag riêng. **(DOC; [k6 scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/), truy cập 2026-07-14)** Điều này cho phép tách browse/cart/checkout thành các population và tỷ lệ khác nhau. **(ASSUMPTION)** Với arrival-rate, phải cấu hình pre-allocated/max VUs và theo dõi dropped iterations; target arrival không bảo đảm đạt nếu load generator thiếu capacity. **(DOC; [k6 executors](https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/), truy cập 2026-07-14)**

## 1.4 Session, correlation và data

- Mỗi VU có cookie jar; cookie từ Set-Cookie được lưu và gửi lại theo phạm vi. **(DOC; [Cookies](https://grafana.com/docs/k6/latest/using-k6/cookies/), truy cập 2026-07-14)**
- Response API cho đọc body/JSON nên có thể lấy access token, CSRF, product/cart/order ID cho bước sau. **(DOC; [HTTP Response](https://grafana.com/docs/k6/latest/javascript-api/k6-http/response/), truy cập 2026-07-14; [Response.json](https://grafana.com/docs/k6/latest/javascript-api/k6-http/response/response-json/), truy cập 2026-07-14)**
- Variables, JSON và SharedArray hỗ trợ parameterization/test data. **(DOC; [Data parameterization](https://grafana.com/docs/k6/latest/examples/data-parameterization/), truy cập 2026-07-14)**
- Token refresh, uniqueness tài khoản/cart/order, cleanup và race condition của EShop phải xác nhận trên SUT thật. **[CẦN THỰC NGHIỆM]**

## 1.5 Checks, thresholds và pass/fail

Checks đánh giá Boolean status/body và tạo rate metric, nhưng check thất bại **không tự làm process fail**. **(DOC; [Checks](https://grafana.com/docs/k6/latest/using-k6/checks/), truy cập 2026-07-14)** Thresholds là acceptance criteria trên trend/rate/counter/gauge, hỗ trợ percentile và abortOnFail; threshold fail tạo exit code khác 0. **(DOC; [Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/), truy cập 2026-07-14)** Vì vậy CI phải có cả check nghiệp vụ và threshold, không chỉ check.

## 1.6 Metrics, report, raw output, CLI/CI/container

- k6 in end-of-test summary, hỗ trợ custom metrics, JSON/CSV, stream ra backend và custom summary HTML/JSON/XML. **(DOC; [Results output](https://grafana.com/docs/k6/latest/get-started/results-output/), truy cập 2026-07-14)**
- Web dashboard tích hợp hiển thị realtime và export self-contained HTML. **(DOC; [Web dashboard](https://grafana.com/docs/k6/latest/results-output/web-dashboard/), truy cập 2026-07-14)**
- CLI là **k6 run**; official integrations liệt kê GitHub Actions, GitLab, Jenkins, Azure Pipelines và AWS CodeBuild. **(DOC; [k6 integrations](https://grafana.com/docs/k6/latest/reference/integrations/), truy cập 2026-07-14)**
- Docker image chính thức hỗ trợ containerized run. Browser module chạy Chromium và có footprint khác protocol load; capacity phải đo. **(DOC; [Install/Docker](https://grafana.com/docs/k6/latest/set-up/install-k6/), truy cập 2026-07-14; [Browser tests](https://grafana.com/docs/k6/latest/using-k6-browser/running-browser-tests/), truy cập 2026-07-14; capacity cụ thể: [CẦN THỰC NGHIỆM])**

## 1.7 Local/offline, docs/community và AI-assisted potential

CLI, raw JSON/CSV và HTML dashboard chạy local, không cần Cloud account. **(DOC; [Install](https://grafana.com/docs/k6/latest/set-up/install-k6/), truy cập 2026-07-14; [Results](https://grafana.com/docs/k6/latest/get-started/results-output/), truy cập 2026-07-14)** Offline tuyệt đối cần pin/cache binary, image và modules; ngoài SUT, script không được import tài nguyên mạng. **[CẦN THỰC NGHIỆM]**

Docs chính thức bao phủ authoring, execution, result và integrations; GitHub có issues/releases. **(DOC; [k6 docs](https://grafana.com/docs/k6/latest/), truy cập 2026-07-14; [repo](https://github.com/grafana/k6), truy cập 2026-07-14)**

k6 **không phải AI**. AI chỉ nên hỗ trợ dựng skeleton JavaScript từ OpenAPI/HAR, sinh data, gợi ý correlation/threshold và review result. HAR/Studio không tự hiểu business semantics và vẫn cần chỉnh script. **(DOC nền; [HAR converter](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-har-converter/), truy cập 2026-07-14; tiềm năng AI: ASSUMPTION)** Human audit bắt buộc: URL/method/payload, secrets, correlation, think time, scenario mix, VU capacity, checks, SLO threshold và authorization.

## 1.8 EShop/classroom fit, strengths và limitations

**EShop fit:** cao nhờ HTTP, cookie, JSON, data, multi-scenario và cả closed/open workload. **(ASSUMPTION dựa trên DOC trên)**  
**Classroom fit:** tốt vì script ngắn và evidence local rõ; phải dạy ba caveat: runtime không phải Node, check khác threshold, browser VU khác protocol VU.

**Strengths**

1. Test-as-code gọn, workload model rộng.
2. Check + threshold + exit code tạo CI gate rõ.
3. Raw output và local HTML tốt cho audit.
4. Session/correlation/data đủ cho EShop.
5. HAR/Studio/browser là authoring và frontend layer bổ sung.

**Limitations**

1. npm/Node assumption dễ sai. **(DOC; [Modules](https://grafana.com/docs/k6/latest/using-k6/modules/), truy cập 2026-07-14)**
2. Check không tự fail build. **(DOC; [Checks](https://grafana.com/docs/k6/latest/using-k6/checks/), truy cập 2026-07-14)**
3. HAR output chưa production-ready. **(DOC; [HAR converter](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-har-converter/), truy cập 2026-07-14)**
4. Browser VU tốn tài nguyên; scale phải đo. **[CẦN THỰC NGHIỆM]**
5. AGPL implications khi sửa/nhúng/phân phối cần legal review; đây không phải tư vấn pháp lý. **(DOC về licence; [repo](https://github.com/grafana/k6), truy cập 2026-07-14)**

## 1.9 Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

- **Objective:** xác nhận install, một GET idempotent, status check, threshold, raw JSON và exit.
- **Prerequisites:** SUT được cấp quyền; thay **[VERIFIED_BASE_URL]** và **[VERIFIED_PRODUCT_ENDPOINT]**; pin k6; tạo artifacts directory.
- **Install/setup:** theo official install hoặc image pin; ghi OS/CPU/RAM, version, Git commit. **(DOC; [Install](https://grafana.com/docs/k6/latest/set-up/install-k6/), truy cập 2026-07-14)**
- **Sample:**

~~~javascript
import http from "k6/http";
import { check } from "k6";

export const options = {
  scenarios: {
    smoke: { executor: "shared-iterations", vus: 1, iterations: 1 },
  },
  thresholds: {
    checks: ["rate==1"],
    http_req_failed: ["rate==0"],
  },
};

export default function () {
  const r = http.get("[VERIFIED_BASE_URL][VERIFIED_PRODUCT_ENDPOINT]");
  check(r, { "status is 200": (x) => x.status === 200 });
}
~~~

- **Command:** **k6 run --out json=artifacts/k6-smoke.json smoke.js**
- **Expected:** một iteration, checks/thresholds đạt, exit 0, JSON + summary có mặt; đây là acceptance condition, không phải observation.
- **Evidence:** version/command, script/hash, stdout/stderr, exit, raw JSON, summary/HTML, timestamps, machine/SUT metadata, Git commit.
- **Possible errors:** DNS/TLS/proxy, auth, 301/401/403/404, volume/permission, threshold syntax, remote module.
- **Success criteria:** đủ artifacts, đúng scope, exit 0, check/threshold đạt; nếu không ghi failed/inconclusive.

## 1.10 Scoring

| Tiêu chí | Điểm | Lý do + DOC |
|---|---:|---|
| Cost & access | 5 | OSS local; Cloud optional. [Repo](https://github.com/grafana/k6), [pricing](https://grafana.com/pricing/) *(truy cập 2026-07-14)* |
| Learning curve | 4 | JS dễ, runtime riêng. [Modules](https://grafana.com/docs/k6/latest/using-k6/modules/) *(truy cập 2026-07-14)* |
| EShop fit | 5 | HTTP/cookie/JSON/data. [Cookies](https://grafana.com/docs/k6/latest/using-k6/cookies/), [data](https://grafana.com/docs/k6/latest/examples/data-parameterization/) *(truy cập 2026-07-14)* |
| Multi-step journey | 5 | State + scenarios. [Scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/) *(truy cập 2026-07-14)* |
| Workload control | 5 | VU, iteration, arrival rate. [Scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/) *(truy cập 2026-07-14)* |
| Assertions/checks | 5 | Checks + threshold gate. [Checks](https://grafana.com/docs/k6/latest/using-k6/checks/), [thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) *(truy cập 2026-07-14)* |
| Reporting | 5 | Summary/raw/HTML/stream. [Results](https://grafana.com/docs/k6/latest/get-started/results-output/), [dashboard](https://grafana.com/docs/k6/latest/results-output/web-dashboard/) *(truy cập 2026-07-14)* |
| CI/CD | 5 | CLI, exit gate, integrations. [Integrations](https://grafana.com/docs/k6/latest/reference/integrations/) *(truy cập 2026-07-14)* |
| Reproducibility | 5 | Code + binary/image pin + raw output. [Install](https://grafana.com/docs/k6/latest/set-up/install-k6/) *(truy cập 2026-07-14)* |
| Local/offline | 5 | Local binary/report; cache trước. [Install](https://grafana.com/docs/k6/latest/set-up/install-k6/) *(truy cập 2026-07-14)* |
| AI-assisted potential | 5 | JS/HAR phù hợp hỗ trợ; tool không phải AI. [HAR](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-har-converter/) *(truy cập 2026-07-14; score là ASSUMPTION)* |
| Classroom suitability | 4 | Demo/evidence tốt, có runtime/threshold caveat. *(ASSUMPTION dựa trên DOC trên)* |

**Weighted Score: 97.4/100; chưa hiệu chỉnh bằng EXP.**

## 1.11 Critical questions

1. **Checks đều đúng thì cần threshold không?** Có; checks không tự fail process, threshold mới gate exit. **(DOC; [checks](https://grafana.com/docs/k6/latest/using-k6/checks/), [thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/), truy cập 2026-07-14)**
2. **JavaScript nghĩa là dùng mọi npm package?** Không; k6 không phải Node runtime. **(DOC; [modules](https://grafana.com/docs/k6/latest/using-k6/modules/), truy cập 2026-07-14)**
3. **Có browser module thì nên phát toàn bộ tải bằng browser?** Không thể suy ra; browser và protocol phục vụ mục tiêu khác, capacity cần đo. **[CẦN THỰC NGHIỆM]**
4. **HAR/Studio tự xử lý correlation?** Không; generated script vẫn phải audit và chỉnh. **(DOC; [HAR converter](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-har-converter/), truy cập 2026-07-14)**

---

# 2. Locust

## 2.1 Overview, maintainer, licence, cost và access

Locust là framework load testing Python có Web UI và headless mode. Kho chính thức ghi Lars Holmberg là maintainer, Jonatan Heyman là creator; Microsoft được ghi nhận tài trợ/đóng góp bảo trì. **(DOC; [Locust repository](https://github.com/locustio/locust), truy cập 2026-07-14; [stable docs](https://docs.locust.io/en/stable/), truy cập 2026-07-14)**

Locust dùng giấy phép **MIT**, chạy local/distributed không cần SaaS account. **(DOC; [repo/licence](https://github.com/locustio/locust), truy cập 2026-07-14)** Tài liệu stable hiện giới thiệu Azure Load Testing cho hosted load; chi phí và account thuộc dịch vụ ngoài lớp OSS. **(DOC; [Hosted load testing](https://docs.locust.io/en/stable/hosted-load-testing.html), truy cập 2026-07-14)**

**Provisional category:** **Shortlist**.

## 2.2 Install/platform và scripting

- Official install: **pip install locust** hoặc uvx; trang cài có Windows troubleshooting và dẫn Docker alternative. **(DOC; [Installation](https://docs.locust.io/en/stable/installation.html), truy cập 2026-07-14)**
- Official image **locustio/locust** và Compose hỗ trợ standalone/master-worker. **(DOC; [Docker](https://docs.locust.io/en/stable/running-in-docker.html), truy cập 2026-07-14)**
- Locustfile là Python module. HttpUser, task weight, wait_time và on_start mô tả flow; mỗi User chạy trong greenlet. **(DOC; [Writing locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html), truy cập 2026-07-14)**
- har2locust chuyển HAR sang Python nhưng đang beta và output có thể không chính xác. **(DOC; [Writing locustfile – HAR](https://docs.locust.io/en/stable/writing-a-locustfile.html), truy cập 2026-07-14)**

## 2.3 Workload controls

Headless CLI điều khiển user count, spawn rate và run time. **(DOC; [Headless mode](https://docs.locust.io/en/stable/running-without-web-ui.html), truy cập 2026-07-14)** LoadTestShape dựng stage/ramp/spike và user-class mix. **(DOC; [Custom load shapes](https://docs.locust.io/en/stable/configuration.html#custom-load-shapes), truy cập 2026-07-14)** constant_throughput giới hạn tốc độ task nhưng không tự tăng user để bù khi iteration chậm, nên open-arrival model cần care. **(DOC; [wait-time helpers](https://docs.locust.io/en/stable/writing-a-locustfile.html), truy cập 2026-07-14)**

Master/worker hỗ trợ nhiều process/máy; docs lưu ý thường cần worker/core do GIL, còn **--processes** dựa trên fork và không chạy trên Windows. **(DOC; [Distributed load](https://docs.locust.io/en/stable/running-distributed.html), truy cập 2026-07-14)**

## 2.4 Session, correlation và data

HttpSession bao quanh requests.Session, giữ cookies; HttpUser **không phải browser**, không render hoặc tự tải mọi asset. **(DOC; [Writing locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html), truy cập 2026-07-14)** Python cho phép parse JSON/token/ID và lưu state per user cho bước sau. **(DOC nền cùng nguồn; ánh xạ EShop: ASSUMPTION)** CSV/JSON/DB/queue có thể dùng qua Python, nhưng uniqueness giữa workers cần partition/queue và test duplicate/exhaustion. **[CẦN THỰC NGHIỆM]**

## 2.5 Checks, metrics, report và CI

- Với catch_response=True, script có thể response.failure/success dựa trên status, body hoặc business JSON. **(DOC; [Validating responses](https://docs.locust.io/en/stable/writing-a-locustfile.html#validating-responses), truy cập 2026-07-14)**
- Headless mặc định exit 1 nếu có failed sample; tùy chọn **--exit-code-on-error** thay mã. Docs minh họa events.quitting để gate fail ratio, average và p95. **(DOC; [Headless/exit](https://docs.locust.io/en/stable/running-without-web-ui.html), truy cập 2026-07-14)**
- Web UI có RPS, response times, failures, user charts. CLI CSV tạo stats, history, failures, exceptions; percentile list cấu hình gồm p50/p95/p99 và mức khác. **(DOC; [Quickstart](https://docs.locust.io/en/stable/quickstart.html), truy cập 2026-07-14; [Configuration](https://docs.locust.io/en/stable/configuration.html), truy cập 2026-07-14)**
- Headless docs có GitHub Actions example; Docker/Compose hỗ trợ pipeline. SLO gate nâng cao cần code hook được review/version-control. **(DOC; [Headless](https://docs.locust.io/en/stable/running-without-web-ui.html), truy cập 2026-07-14; [Docker](https://docs.locust.io/en/stable/running-in-docker.html), truy cập 2026-07-14)**

## 2.6 Local/offline, docs/community và AI

Runner, Web UI, CSV và distributed workers chạy local không cần account. **(DOC; [Locust docs](https://docs.locust.io/en/stable/), truy cập 2026-07-14)** Offline strict cần wheel/image/dependency cache và lockfile. **[CẦN THỰC NGHIỆM]** Official docs, GitHub issues/discussions và Discord link tạo cộng đồng hỗ trợ công khai. **(DOC; [repo](https://github.com/locustio/locust), truy cập 2026-07-14)**

Locust **không phải AI**. AI có thể draft task/class, data/correlation và exit hook vì Python dễ đọc; har2locust beta chứng minh generated code vẫn cần human audit. **(DOC nền; [locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html), truy cập 2026-07-14; AI potential: ASSUMPTION)** Audit: side effects, dependencies, secrets, user lifecycle, task weights, wait time, shape, worker data uniqueness, response.failure và quality gate.

## 2.7 EShop/classroom fit, strengths và limitations

**EShop fit:** cao cho journey có state/cookie/correlation và logic rẽ nhánh. **Classroom fit:** rất tốt nếu sinh viên biết Python; gevent/process/shape và custom exit gate cần giải thích.

**Strengths:** Python đầy đủ; state per user; Web UI + headless; custom shape; distributed; MIT/local.  
**Limitations:** không phải browser; arrival-rate chính xác kém trực tiếp hơn executor chuyên biệt; p95/SLO gate cần hook; GIL/process/Windows fork caveat; data uniqueness và generator saturation phải đo.

## 2.8 Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

- **Objective:** import/package, 1 user gọi GET idempotent, validate response, CSV/log/exit.
- **Prerequisites:** authorized **[VERIFIED_BASE_URL]**, endpoint path, pinned Python/Locust, account test nếu cần.
- **Install/setup:** venv + lockfile hoặc pinned image; ghi versions/OS/Git. **(DOC; [Installation](https://docs.locust.io/en/stable/installation.html), truy cập 2026-07-14)**
- **Sample:**

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
        ) as r:
            if r.status_code != 200:
                r.failure(f"unexpected status: {r.status_code}")
~~~

- **Command:** **locust -f locustfile.py --headless --users 1 --spawn-rate 1 --run-time 5s --host [VERIFIED_BASE_URL] --csv artifacts/locust-smoke**
- **Expected:** ít nhất một sample, failure 0, exit 0, CSV được tạo; chưa quan sát.
- **Evidence:** versions/lock, command, script/hash, stdout/stderr, exit, mọi CSV, request count, timestamps, worker/process/machine/SUT metadata.
- **Possible errors:** venv/PATH, TLS/proxy/auth, run quá ngắn, CSV permission, loop gửi nhiều request hơn tưởng, side effect.
- **Success:** artifacts đủ, failure 0, exit 0, request trong scope. Muốn chính xác một request cần stop logic riêng.

## 2.9 Scoring

| Tiêu chí | Điểm | Lý do + DOC |
|---|---:|---|
| Cost & access | 5 | MIT/local OSS. [Repo](https://github.com/locustio/locust) *(truy cập 2026-07-14)* |
| Learning curve | 4 | Python quen, lifecycle/gevent cần học. [Locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) *(truy cập 2026-07-14)* |
| EShop fit | 5 | HttpSession/state/correlation. [Locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) *(truy cập 2026-07-14)* |
| Multi-step journey | 5 | Flow tuần tự, on_start, per-user state. [Locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) *(truy cập 2026-07-14)* |
| Workload control | 4 | Users/spawn/custom shape; open rate caveat. [Shapes](https://docs.locust.io/en/stable/configuration.html#custom-load-shapes) *(truy cập 2026-07-14)* |
| Assertions/checks | 4 | catch_response mạnh, SLO gate cần hook. [Validation](https://docs.locust.io/en/stable/writing-a-locustfile.html#validating-responses), [exit](https://docs.locust.io/en/stable/running-without-web-ui.html) *(truy cập 2026-07-14)* |
| Reporting | 4 | Live UI + CSV; không trọng tâm polished local HTML. [Configuration](https://docs.locust.io/en/stable/configuration.html) *(truy cập 2026-07-14)* |
| CI/CD | 4 | Headless/exit/Actions; custom gate code. [Headless](https://docs.locust.io/en/stable/running-without-web-ui.html) *(truy cập 2026-07-14)* |
| Reproducibility | 5 | Python/lock/CLI/CSV dễ version. *(DOC nền; ASSUMPTION)* |
| Local/offline | 5 | Local UI/runner/worker; cache trước. [Docs](https://docs.locust.io/en/stable/) *(truy cập 2026-07-14)* |
| AI-assisted potential | 5 | Python/HAR tốt cho hỗ trợ, tool không AI. [Locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) *(truy cập 2026-07-14; ASSUMPTION)* |
| Classroom suitability | 4 | UI trực quan/Python phổ biến; process/gate caveat. *(ASSUMPTION)* |

**Weighted Score: 90.8/100; chưa hiệu chỉnh bằng EXP.**

## 2.10 Critical questions

1. **Locust có browser thật?** Không; HttpUser không render UI/assets. **(DOC; [locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html), truy cập 2026-07-14)**
2. **constant_throughput luôn đạt target?** Không; nó không tự tăng user để bù iteration chậm. **(DOC; cùng nguồn)**
3. **Business failure làm CI fail?** Nếu đánh dấu failed sample, headless có exit lỗi; p95/fail-ratio gate tùy biến cần hook. **(DOC; [headless](https://docs.locust.io/en/stable/running-without-web-ui.html), truy cập 2026-07-14)**
4. **Nhiều worker tự chia CSV unique?** Không; script/feeder phải bảo đảm và cần EXP. **[CẦN THỰC NGHIỆM]**

---

# 3. Gatling

## 3.1 Overview, maintainer, licence, cost và access

Gatling là performance-testing platform do Gatling Corp duy trì. Community engine hỗ trợ Java, JavaScript, TypeScript, Kotlin và Scala. **(DOC; [Gatling repository](https://github.com/gatling/gatling), truy cập 2026-07-14; [Gatling docs](https://docs.gatling.io/), truy cập 2026-07-14)**

Main open-source project dùng **Apache-2.0**, nhưng bundled Highcharts report module có licence riêng: được dùng miễn phí trong phạm vi Gatling chuẩn nhưng không được tùy ý sửa/ngoài phạm vi nếu thiếu Highcharts licence; một số Enterprise components có licence riêng. Không nên rút gọn thành “mọi thứ đều Apache-2.0”. **(DOC; [Gatling project licences](https://docs.gatling.io/project/licenses/project-licenses/), truy cập 2026-07-14)**

Community chạy local miễn phí. Trang giá Gatling Enterprise hiện niêm yết Basic từ 89 EUR/tháng khi trả năm hoặc 99 EUR theo tháng, Team từ 356/396 EUR và Enterprise custom; phải kiểm tra lại trước nộp vì giá thay đổi. **(DOC; [Gatling pricing](https://gatling.io/pricing), truy cập 2026-07-14)** Self-service trial kéo dài 14 ngày với hạn mức được mô tả trong docs. **(DOC; [Enterprise trial](https://docs.gatling.io/evaluate-enterprise/trial-plan/), truy cập 2026-07-14)**

**Provisional category:** **Shortlist**; mạnh về workload/assertions nhưng có learning/setup cost cao hơn k6.

## 3.2 Install/platform và scripting

- Gatling chạy JVM. JVM SDK hỗ trợ Java/Kotlin/Scala; JS/TS dùng npm tooling. Current install docs hỗ trợ OpenJDK LTS 11–25 và khuyến nghị Gatling 3.15.1 ở mốc truy cập. **(DOC; [Install local](https://docs.gatling.io/reference/deploy/install-local/), truy cập 2026-07-14)**
- Current JavaScript SDK yêu cầu Node.js 24+ LTS và npm 11+. Official install page nói JS chỉ HTTP nhưng current official gRPC/SSE/MQTT pages có JS/TS examples; đây là documentation conflict, nên phải pin version/module/edition và smoke-test parity. **(DOC; [Install local](https://docs.gatling.io/reference/deploy/install-local/), [gRPC JS/TS](https://docs.gatling.io/guides/use-cases/grpc-js/), [SSE](https://docs.gatling.io/reference/script/sse/), [MQTT](https://docs.gatling.io/reference/script/mqtt/protocol/), truy cập 2026-07-14)**
- Maven/Gradle/sbt, npm hoặc standalone bundle đều được hỗ trợ; standalone phù hợp môi trường firewall/offline. **(DOC; [Install local](https://docs.gatling.io/reference/deploy/install-local/), truy cập 2026-07-14)**
- Recorder có thể capture HTTP proxy/HAR thành simulation, nhưng generated code vẫn cần correlation/data/workload audit. **(DOC; [HTTP recorder](https://docs.gatling.io/reference/script/http/), truy cập 2026-07-14; production readiness: ASSUMPTION)**

## 3.3 Workload controls

Injection DSL phân biệt open và closed models. Open profiles có atOnceUsers, rampUsers, constantUsersPerSec, rampUsersPerSec, stressPeakUsers; closed profiles có constant/ramp concurrent users; nhiều scenario có thể setUp cùng simulation. **(DOC; [Injection](https://docs.gatling.io/concepts/injection/), truy cập 2026-07-14)** Đây là phạm vi workload rất mạnh cho browse arrival, concurrent checkout và spike. **(ASSUMPTION)**

## 3.4 Session, cookies, correlation và data

- Mỗi VU có Session map; check có thể **saveAs** giá trị để dùng ở request sau. **(DOC; [Session API](https://docs.gatling.io/concepts/session/api/), truy cập 2026-07-14; [Checks](https://docs.gatling.io/concepts/checks/), truy cập 2026-07-14)**
- HTTP cookie handling hoạt động tự động và có API add/get/flush cookie jar. Gatling hoạt động tầng HTTP, không chạy JavaScript/CSS/UI event như browser. **(DOC; [HTTP helpers/cookies](https://docs.gatling.io/reference/script/http/helpers/), truy cập 2026-07-14; [HTTP protocol](https://docs.gatling.io/reference/script/http/protocol/), truy cập 2026-07-14)**
- Feeders hỗ trợ CSV/JSON/sitemap/in-memory và các chiến lược queue/shuffle/random/circular; queue exhaustion làm test crash. Một số feeder capability khác nhau giữa SDK. **(DOC; [Feeders](https://docs.gatling.io/concepts/session/feeders/), truy cập 2026-07-14)**
- EShop correlation dùng JSONPath/CSS/regex saveAs cho token, product/cart/order ID; exact business flow cần EXP.

## 3.5 Checks, assertions, metrics và exit

Checks xác nhận status/body và capture data. **(DOC; [Checks](https://docs.gatling.io/concepts/checks/), truy cập 2026-07-14)** Assertions đặt acceptance criteria global/forAll/details trên response time, request count/failures và RPS, gồm configured/explicit percentiles; nếu một assertion fail, simulation fail. **(DOC; [Assertions](https://docs.gatling.io/concepts/assertions/), truy cập 2026-07-14)** Official glossary nói assertion failure làm Gatling trả error status code cho toàn test. **(DOC; [Gatling glossary](https://docs.gatling.io/reference/glossary/), truy cập 2026-07-14)**

## 3.6 Reporting, raw data và CI/CD

- Community sinh portable static HTML report với response time, percentile, OK/KO, users và requests/s. **(DOC; [Community reports](https://docs.gatling.io/reference/stats/reports/oss/), truy cập 2026-07-14)**
- **simulation.log không phải public raw contract**: official FAQ gọi đây là implementation detail, undocumented và có thể đổi; không nên parse để làm integration. Các file nội bộ cũ như stats.json/assertions.json đã bị loại. **(DOC; [Gatling FAQ](https://docs.gatling.io/tutorials/faq/), truy cập 2026-07-14)**
- Community test chạy qua Maven/Gradle/sbt/npm trong CI; assertions cung cấp exit gate. Enterprise có CI integrations/dashboard/distributed execution riêng và cần account/token. **(DOC; [Build tools/JS CLI](https://docs.gatling.io/integrations/build-tools/js-cli/), truy cập 2026-07-14; [CI/CD integrations](https://docs.gatling.io/integrations/ci-cd/), truy cập 2026-07-14)**
- Không xác nhận được một official Community Docker image hiện hành tương đương k6/Artillery trong docs đã kiểm; nếu containerize, nhóm phải tự pin JDK/build image và kiểm licence/dependencies. **(ASSUMPTION; [CẦN THỰC NGHIỆM])**

## 3.7 Local/offline, docs/community và AI

Community engine và static HTML chạy local; standalone bundle được docs mô tả cho offline/firewall. Build-tool route cần cache dependency. **(DOC; [Install local](https://docs.gatling.io/reference/deploy/install-local/), truy cập 2026-07-14)** Official docs/repo/forum có tutorial và reference đa ngôn ngữ. **(DOC; [Docs](https://docs.gatling.io/), [repo](https://github.com/gatling/gatling), truy cập 2026-07-14)**

Gatling core **không phải AI**. Năm 2026, Gatling Enterprise có AI extensions/MCP và AI Analysis; MCP yêu cầu Enterprise account/API token, còn vendor nhấn mạnh engineering judgment vẫn cần thiết. **(DOC; [Gatling AI](https://docs.gatling.io/ai/), truy cập 2026-07-14; [MCP](https://gatling.io/product/mcp), truy cập 2026-07-14; [AI Analysis](https://gatling.io/product/ai-analysis), truy cập 2026-07-14; [AI Analysis guidance](https://gatling.io/blog/how-to-get-started-with-ai-analysis), truy cập 2026-07-14)** External AI có thể draft typed DSL nhưng phải audit imports/SDK parity, session immutability, feeder exhaustion, correlation, workload model và assertions.

## 3.8 EShop/classroom fit, strengths và limitations

**EShop fit:** rất cao: sessions, feeders, checks/saveAs, open/closed injection, assertions. **Classroom fit:** trung bình-khá; typed DSL và build tooling dạy nhiều khái niệm tốt nhưng tốn setup/thời gian.

**Strengths:** workload modelling rất mạnh; checks/correlation; assertions + error exit; static HTML; đa ngôn ngữ JVM/JS.  
**Limitations:** learning/build cost; JS/TS protocol scope có documentation conflict và cần pin module/edition; feature parity feeder/SDK khác nhau; simulation.log không phải stable raw API; Enterprise reporting/distributed/AI có phí/account; không phải browser.

## 3.9 Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

- **Objective:** current JS SDK install, one VU/GET, status check, global assertion, local HTML và exit.
- **Prerequisites:** authorized target/path; Node 24+ LTS/npm11+; cloned/pinned official JS starter and lockfile.
- **Install/setup:** npm install trong project; ghi Node/npm/Gatling versions, lockfile, OS/Git. **(DOC; [JS install](https://docs.gatling.io/tutorials/test-as-code/javascript/installation-guide/), truy cập 2026-07-14)**
- **Sample – src/smokeSimulation.gatling.js:**

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

- **Command:** **npx gatling run --simulation smokeSimulation**
- **Expected:** 1 VU, request check/assertion đạt, error exit không xảy ra, HTML trong target/gatling; chưa quan sát. Command/current project convention được official JS CLI hỗ trợ. **(DOC; [JS CLI](https://docs.gatling.io/integrations/build-tools/js-cli/), truy cập 2026-07-14)**
- **Evidence:** versions/lock, command, script/hash, stdout/stderr, exit, full HTML folder, build log, timestamps, machine/SUT metadata.
- **Possible errors:** Node version, npm network/cache, file naming/location, SDK syntax, TLS/auth, assertion fail, report permission.
- **Success:** exit 0, check/assertion pass, portable report + logs + config present; otherwise failed/inconclusive.

## 3.10 Scoring

| Tiêu chí | Điểm | Lý do + DOC |
|---|---:|---|
| Cost & access | 4 | Free Community; Highcharts nuance/Enterprise cost. [Licences](https://docs.gatling.io/project/licenses/project-licenses/), [pricing](https://gatling.io/pricing) *(truy cập 2026-07-14)* |
| Learning curve | 3 | JVM/npm/build + typed DSL. [Install](https://docs.gatling.io/reference/deploy/install-local/) *(truy cập 2026-07-14)* |
| EShop fit | 5 | HTTP/session/feeders/checks. [Session](https://docs.gatling.io/concepts/session/api/), [feeders](https://docs.gatling.io/concepts/session/feeders/) *(truy cập 2026-07-14)* |
| Multi-step journey | 5 | saveAs/session/chains. [Checks](https://docs.gatling.io/concepts/checks/) *(truy cập 2026-07-14)* |
| Workload control | 5 | Rich open/closed injection. [Injection](https://docs.gatling.io/concepts/injection/) *(truy cập 2026-07-14)* |
| Assertions/checks | 5 | Request checks + global/detail assertions. [Assertions](https://docs.gatling.io/concepts/assertions/) *(truy cập 2026-07-14)* |
| Reporting | 4 | Excellent HTML; raw log not stable contract. [Reports](https://docs.gatling.io/reference/stats/reports/oss/), [FAQ](https://docs.gatling.io/tutorials/faq/) *(truy cập 2026-07-14)* |
| CI/CD | 5 | Build tools + assertion exit; Enterprise integrations optional. [JS CLI](https://docs.gatling.io/integrations/build-tools/js-cli/) *(truy cập 2026-07-14)* |
| Reproducibility | 5 | Typed code/build lock/static report. *(DOC nền; ASSUMPTION)* |
| Local/offline | 5 | Community local/standalone offline. [Install](https://docs.gatling.io/reference/deploy/install-local/) *(truy cập 2026-07-14)* |
| AI-assisted potential | 4 | Code + official Enterprise AI/MCP, nhưng gated/human review. [AI](https://docs.gatling.io/ai/), [MCP](https://gatling.io/product/mcp) *(truy cập 2026-07-14)* |
| Classroom suitability | 3 | Giá trị học thuật cao nhưng setup/DSL nặng. *(ASSUMPTION)* |

**Weighted Score: 90.2/100; chưa hiệu chỉnh bằng EXP.**

## 3.11 Critical questions

1. **Toàn bộ Gatling là Apache-2.0?** Không; main project là Apache-2.0 nhưng Highcharts report module và Enterprise components có điều khoản riêng. **(DOC; [licences](https://docs.gatling.io/project/licenses/project-licenses/), truy cập 2026-07-14)**
2. **simulation.log là raw API ổn định?** Không; official FAQ cấm dựa vào format nội bộ này cho integration. **(DOC; [FAQ](https://docs.gatling.io/tutorials/faq/), truy cập 2026-07-14)**
3. **JS SDK có mọi protocol như JVM SDK?** Không được suy ra. Install page nói JS chỉ HTTP nhưng current official gRPC/SSE/MQTT pages có JS/TS examples; phải pin version/module/edition và kiểm tra capability cụ thể. **(DOC; [install](https://docs.gatling.io/reference/deploy/install-local/), [gRPC JS/TS](https://docs.gatling.io/guides/use-cases/grpc-js/), truy cập 2026-07-14)**
4. **Gatling chạy JavaScript của website như browser?** Không; HTTP engine không chạy JS/CSS/UI. **(DOC; [HTTP protocol](https://docs.gatling.io/reference/script/http/protocol/), truy cập 2026-07-14)**

---

# 4. Artillery

## 4.1 Overview, maintainer, licence, cost và access

Artillery là load-testing toolkit do Artillery Software Inc. duy trì, dùng Node.js và script YAML/JavaScript/TypeScript; hỗ trợ HTTP, WebSocket, Socket.IO và Playwright engine. **(DOC; [Artillery repository](https://github.com/artilleryio/artillery), truy cập 2026-07-14; [Docs](https://www.artillery.io/docs), truy cập 2026-07-14)**

Phần lớn repository dùng **MPL-2.0**, nhưng một số Azure-specific modules dùng BSL và commercial/production Azure use cần commercial licence; evaluation/PoC được điều khoản repo mô tả riêng. Không nên ghi toàn bộ là MPL thuần. **(DOC; [Repository licence notice](https://github.com/artilleryio/artillery), truy cập 2026-07-14)**

Local CLI là OSS. Artillery Cloud Free hiện 0 USD, 30 reports/tháng, 1-month retention, 2 users và distributed AWS/Azure tối đa 5 workers/test; paid tiers có Starter 199 USD và Scale 499 USD/tháng ở mốc truy cập. **(DOC; [Artillery pricing](https://www.artillery.io/pricing), truy cập 2026-07-14)** Cloud không bắt buộc cho local CLI.

**Provisional category:** **Backup**; rất dễ dùng/CI tốt nhưng local HTML đã bị loại và workload chủ đạo thiên arrival.

## 4.2 Install/platform và scripting

- Official docs hỗ trợ Windows, macOS và Linux, yêu cầu current recent Node LTS; có thể chạy **npx artillery@latest**. **(DOC; [Get Artillery](https://www.artillery.io/docs/get-started/get-artillery), truy cập 2026-07-14)**
- Official image **artilleryio/artillery** có latest và version tags. **(DOC; [Artillery Docker](https://www.artillery.io/docs/docker), truy cập 2026-07-14)**
- Test definition viết YAML, TypeScript hoặc JavaScript với config + scenarios; environments, env vars, processor/hooks hỗ trợ cấu hình và logic custom. **(DOC; [Test scripts](https://www.artillery.io/docs/reference/test-script), truy cập 2026-07-14)**
- Playwright engine chạy browser/headless và thu Web Vitals, nhưng không nên dùng browser VU để thay protocol load nếu mục tiêu là backend capacity. **(DOC; [Playwright engine](https://www.artillery.io/docs/reference/engines/playwright), truy cập 2026-07-14; khuyến nghị: ASSUMPTION)**

## 4.3 Workload controls

Load phases hỗ trợ constant arrival rate, linear rampTo, fixed arrivalCount và pause; maxVusers giới hạn concurrency. Scenario weights tạo journey mix. **(DOC; [Test script phases](https://www.artillery.io/docs/reference/test-script), truy cập 2026-07-14)** Đây là arrival-centric model; maxVusers là cap, không phải closed-model concurrent-user target hoàn chỉnh. **(ASSUMPTION dựa trên semantics docs)**

## 4.4 Session, correlation và data

HTTP VU giữ cookies; capture hỗ trợ JSONPath, XPath, regex, headers và CSS, rồi dùng giá trị ở request sau; think time và hooks có sẵn. Capture strict mặc định dừng scenario VU khi không lấy được giá trị. **(DOC; [HTTP engine](https://www.artillery.io/docs/reference/engines/http), truy cập 2026-07-14)** CSV và variables hỗ trợ parameterization; distributed uniqueness có Redis example. **(DOC; [Artillery examples](https://www.artillery.io/docs/get-started/examples), truy cập 2026-07-14)**

## 4.5 Checks, ensure và exit behavior

Plugin **expect** hỗ trợ status/body/header/JMESPath và smoke/acceptance checks, nhưng chỉ tương thích HTTP engine và không tương thích before/after hooks. **(DOC; [Expect plugin](https://www.artillery.io/docs/reference/extensions/expect), truy cập 2026-07-14)** Plugin **ensure** đặt threshold/condition trên metric và trả nonzero khi strict condition fail. **(DOC; [Ensure plugin](https://www.artillery.io/docs/reference/extensions/ensure), truy cập 2026-07-14)**

Mặc định, HTTP 5xx/network timeout **không nhất thiết làm CLI exit nonzero**; phải cấu hình ensure/check explicit. Syntax/unrecoverable error/interruption mới có exit error mặc định. **(DOC; [CLI exit codes](https://www.artillery.io/docs/reference/cli/exit-codes), truy cập 2026-07-14)** Đây là caveat CI quan trọng.

## 4.6 Metrics, report, raw output và CI/CD

- Console in snapshot mỗi 10 giây + final summary; metrics gồm counts/rates/errors/VUs và histogram min/max/mean/median/p50/p75/p90/p95/p99/p999. **(DOC; [Reported metrics](https://www.artillery.io/docs/reference/reported-metrics), truy cập 2026-07-14)**
- CLI **--output** tạo JSON report gồm intermediate và aggregate data. **(DOC; [Run CLI](https://www.artillery.io/docs/reference/cli/run), truy cập 2026-07-14)**
- Lệnh local HTML **artillery report** đã bị loại từ v2.0.22; web report hiện dựa vào Artillery Cloud. Không được tuyên bố Artillery v2 hiện sinh local HTML bằng lệnh cũ. **(DOC; [Report command](https://www.artillery.io/docs/reference/cli/report), truy cập 2026-07-14)**
- Official CI guides có GitHub Actions, GitLab, Jenkins, Azure, AWS CodeBuild và CircleCI; ensure nonzero exit làm gate. **(DOC; [Artillery CI/CD](https://www.artillery.io/docs/cicd), truy cập 2026-07-14)**

## 4.7 Local/offline, docs/community và AI

CLI/JSON/console chạy local không cần Cloud; strict offline cần pin/cache npm package hoặc Docker image. Cloud dashboard/report cần account/network. **(DOC; [Get Artillery](https://www.artillery.io/docs/get-started/get-artillery), truy cập 2026-07-14; [Report](https://www.artillery.io/docs/reference/cli/report), truy cập 2026-07-14; offline strict: [CẦN THỰC NGHIỆM])** Docs và GitHub Discussions công khai. **(DOC; [Docs](https://www.artillery.io/docs), [repo](https://github.com/artilleryio/artillery), truy cập 2026-07-14)**

Artillery **không phải AI**. Homepage định vị tool làm việc với coding agents, nhưng engine vẫn deterministic; AI có thể draft YAML/TS, data/capture/ensure và phân tích JSON. **(DOC nền; [Artillery homepage](https://www.artillery.io/), truy cập 2026-07-14; AI potential: ASSUMPTION)** Audit: arrival vs concurrency intent, hook side effects, expect/ensure, 5xx exit caveat, secrets, capture strictness, Cloud upload và Azure licence.

## 4.8 EShop/classroom fit, strengths và limitations

**EShop fit:** cao với HTTP cookies/capture/data và flow YAML; processor code dùng cho logic phức tạp. **Classroom fit:** rất cao vì YAML ngắn, nhưng phải dạy rõ expect khác ensure và local HTML đã removed.

**Strengths:** YAML/JS/TS dễ bắt đầu; arrival phases; strong HTTP capture/cookie; raw JSON; official Docker/CI; optional Playwright.  
**Limitations:** concurrent closed model kém trực tiếp; complex YAML phân mảnh sang processor; expect HTTP-only và xung đột before/after; 5xx không tự fail exit; no current local HTML; Azure licence nuance.

## 4.9 Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

- **Objective:** install, fixed one arrival, status expect, ensure gate, JSON/exit.
- **Prerequisites:** authorized base/path, pinned Node/Artillery or image, artifacts dir.
- **Install/setup:** npm local dependency/lockfile hoặc pinned image; ghi versions/OS/Git. **(DOC; [Install](https://www.artillery.io/docs/get-started/get-artillery), truy cập 2026-07-14)**
- **Sample – smoke.yml:**

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

- **Command:** **artillery run --output artifacts/artillery-smoke.json smoke.yml**
- **Expected:** one arrival, expect/ensure pass, exit 0, JSON created; metric name/config must be validated against pinned version. Chưa quan sát. **(DOC; [Expect](https://www.artillery.io/docs/reference/extensions/expect), [Ensure](https://www.artillery.io/docs/reference/extensions/ensure), truy cập 2026-07-14)**
- **Evidence:** versions/lock/image, script/hash, command, stdout/stderr, exit, JSON, timestamps, machine/SUT metadata.
- **Possible errors:** Node/PowerShell execution policy, npm/network, plugin version/metric name, auth/TLS, output permission, target/path.
- **Success:** exact one arrival, expect failed=0, strict ensure passes, exit 0, evidence complete.

## 4.10 Scoring

| Tiêu chí | Điểm | Lý do + DOC |
|---|---:|---|
| Cost & access | 4 | OSS local; Azure licence nuance/Cloud limits. [Repo](https://github.com/artilleryio/artillery), [pricing](https://www.artillery.io/pricing) *(truy cập 2026-07-14)* |
| Learning curve | 4 | YAML/JS dễ; plugin/processor semantics. [Scripts](https://www.artillery.io/docs/reference/test-script) *(truy cập 2026-07-14)* |
| EShop fit | 5 | HTTP cookies/capture/data. [HTTP engine](https://www.artillery.io/docs/reference/engines/http) *(truy cập 2026-07-14)* |
| Multi-step journey | 4 | Flow/capture/hooks tốt; complex logic sang processor. [HTTP](https://www.artillery.io/docs/reference/engines/http) *(truy cập 2026-07-14)* |
| Workload control | 4 | Arrival/ramp/count/cap; closed model hạn chế. [Phases](https://www.artillery.io/docs/reference/test-script) *(truy cập 2026-07-14)* |
| Assertions/checks | 4 | expect + ensure mạnh nhưng separate/caveats. [Expect](https://www.artillery.io/docs/reference/extensions/expect), [ensure](https://www.artillery.io/docs/reference/extensions/ensure) *(truy cập 2026-07-14)* |
| Reporting | 4 | Rich console/JSON; local HTML removed. [Metrics](https://www.artillery.io/docs/reference/reported-metrics), [report](https://www.artillery.io/docs/reference/cli/report) *(truy cập 2026-07-14)* |
| CI/CD | 5 | Official CI guides/Docker/ensure exit. [CI/CD](https://www.artillery.io/docs/cicd) *(truy cập 2026-07-14)* |
| Reproducibility | 5 | YAML/lock/image/raw JSON. *(DOC nền; ASSUMPTION)* |
| Local/offline | 4 | CLI/JSON local; npm cache and no local HTML. [Install](https://www.artillery.io/docs/get-started/get-artillery), [report](https://www.artillery.io/docs/reference/cli/report) *(truy cập 2026-07-14)* |
| AI-assisted potential | 4 | Agent-friendly text/code; tool không AI. [Homepage](https://www.artillery.io/) *(truy cập 2026-07-14; ASSUMPTION)* |
| Classroom suitability | 5 | YAML + quick feedback, caveats teachable. *(ASSUMPTION)* |

**Weighted Score: 86.8/100; chưa hiệu chỉnh bằng EXP.**

## 4.11 Critical questions

1. **HTTP 500 tự làm CI fail?** Không mặc định; phải dùng expect/ensure quality gate. **(DOC; [exit codes](https://www.artillery.io/docs/reference/cli/exit-codes), truy cập 2026-07-14)**
2. **Artillery v2 còn local HTML report?** Lệnh report đã removed từ v2.0.22; Cloud là web-report path hiện tại. **(DOC; [report command](https://www.artillery.io/docs/reference/cli/report), truy cập 2026-07-14)**
3. **expect dùng cho mọi engine và before/after?** Không; expect chỉ HTTP và không tương thích before/after hooks. **(DOC; [expect](https://www.artillery.io/docs/reference/extensions/expect), truy cập 2026-07-14)**
4. **Toàn bộ repository MPL-2.0?** Không; Azure modules có BSL/commercial-use nuance. **(DOC; [repo](https://github.com/artilleryio/artillery), truy cập 2026-07-14)**

---

# 5. Taurus

## 5.1 Bản chất công cụ, maintainer, licence, cost và access

Taurus, CLI tên **bzt**, là automation-friendly orchestration/convenience framework. Nó che bớt độ phức tạp và gọi các underlying tools; repository nêu JMeter, Gatling, Locust, Selenium và nhiều executor khác. Taurus **không tự là load engine tương đương k6**. **(DOC; [Taurus repository](https://github.com/Blazemeter/taurus), truy cập 2026-07-14; [Execution settings/executors](https://gettaurus.org/docs/ExecutionSettings/), truy cập 2026-07-14)**

Repository được tổ chức BlazeMeter duy trì, giấy phép **Apache-2.0**, release 1.16.51 ngày 2026-06-15 ở mốc truy cập. **(DOC; [Taurus repository](https://github.com/Blazemeter/taurus), truy cập 2026-07-14)** BlazeMeter help hiện nói BlazeMeter bảo trì/support package Taurus. **(DOC; [Taurus cloud vulnerability guidance](https://help.blazemeter.com/docs/answers/answers-mitigate-taurus-cloud-vulnerabilities.htm), truy cập 2026-07-14)**

Local Taurus OSS miễn phí và không cần account. BlazeMeter report/cloud là tùy chọn thương mại/free-tier; current pricing có Free Starter và paid Basic/Pro. **(DOC; [BlazeMeter pricing](https://www.blazemeter.com/pricing), truy cập 2026-07-14; [Cloud provisioning](https://gettaurus.org/docs/Cloud/), truy cập 2026-07-14)**

**Provisional category:** **Orchestration framework**; supporting benchmark/config-abstraction tool, không xếp là load generator độc lập.

## 5.2 Install/platform và cấu hình

- Official install dùng **pip install bzt**, có hướng dẫn Linux/macOS/Windows và image Docker **blazemeter/taurus**; Python 3.7+ được docs nêu, executor có thể cần Java/tool riêng. **(DOC; [Taurus installation](https://gettaurus.org/docs/Installation/), truy cập 2026-07-14)**
- bzt nhận YAML/JSON, merge nhiều config, CLI overrides và sinh merged/effective configs. **(DOC; [Command line](https://gettaurus.org/docs/CommandLine/), truy cập 2026-07-14; [Config syntax](https://gettaurus.org/docs/ConfigSyntax/), truy cập 2026-07-14)**
- Default executor là **jmeter**. Supported executor list hiện gồm JMeter, Selenium, Gatling, Playwright, Locust, Apiritif, k6 và nhiều tool khác. **(DOC; [Execution settings](https://gettaurus.org/docs/ExecutionSettings/), truy cập 2026-07-14)**

### Semantics bắt buộc khi dùng JMeter

Khi YAML ghi hoặc mặc định chọn **executor: jmeter**, Taurus tạo/chỉnh test plan và orchestration, còn **Apache JMeter là engine thực thi request và phát tải**. Nếu JMeter chưa có ở configured path, Taurus có thể auto-download JMeter/plugins; default executor JMeter và minimum version được trang executor tài liệu hóa. **(DOC; [JMeter executor](https://gettaurus.org/docs/JMeter/), truy cập 2026-07-14)**

Vì vậy mọi kết quả/capacity/protocol limitation phải quy cho tổ hợp **Taurus + JMeter version/plugins/JVM**, không quy cho Taurus một cách độc lập. Đây là **ASSUMPTION diễn giải kiến trúc dựa trên DOC**.

## 5.3 Workload controls và abstraction cost

Common execution profile có concurrency, ramp-up, hold-for, iterations, throughput và steps. **(DOC; [Load profile](https://gettaurus.org/docs/ExecutionSettings/), truy cập 2026-07-14)** Tuy nhiên support/semantics phụ thuộc executor; cùng một YAML field có thể được translate/overridden khác nhau. Với JMX nhiều thread groups, JMeter executor có logic phân bổ/override concurrency riêng. **(DOC; [JMeter executor](https://gettaurus.org/docs/JMeter/), truy cập 2026-07-14)**

**Abstraction benefit:** một YAML ngắn thống nhất load/report/passfail và có thể wrap script sẵn có.  
**Abstraction cost:** mất một phần feature parity, khó thấy exact engine config nếu chỉ đọc YAML, auto-download gây version drift, debug phải đọc cả bzt log lẫn engine log/generated script. merged.yml/effective.yml và generated JMX là bằng chứng bắt buộc để biết Taurus thực sự chạy gì. **(DOC nền; [Artifacts](https://gettaurus.org/docs/ArtifactsDir/), truy cập 2026-07-14; đánh giá cost: ASSUMPTION)**

## 5.4 Journey, session, correlation và data

Request-based YAML có method/body/headers/think-time, extractors regex/boundary/JSONPath/CSS/XPath và assertions; Taurus generate underlying JMeter plan. **(DOC; [JMeter executor/request scenario](https://gettaurus.org/docs/JMeter/), truy cập 2026-07-14)** Data sources hỗ trợ external CSV nhưng option availability khác theo JMeter/Apiritif/Gatling executor. **(DOC; [Data sources](https://gettaurus.org/docs/DataSources/), truy cập 2026-07-14)** Include-scenario có thể compose login/shop/checkout. **(DOC; [Gatling executor include scenario example](https://gettaurus.org/docs/Gatling/), truy cập 2026-07-14)**

Cookie/session thực tế do underlying executor xử lý. Với default JMeter, cần kiểm generated JMX/cookie manager và token extractors; không được giả định một Taurus-level cookie jar độc lập. **(ASSUMPTION dựa trên executor architecture; [CẦN THỰC NGHIỆM])**

## 5.5 Assertions, pass/fail và exit code

Request assertions có body/headers/http-code, JSONPath và XPath; assertion đặt fail status cho response trong JMeter plan. **(DOC; [JMeter assertions](https://gettaurus.org/docs/JMeter/), truy cập 2026-07-14)**

Taurus **passfail** module đặt criteria như fail rate, avg response time, p90/p99, response code; có timeframe, stop/continue và per-execution/scenario criteria. **(DOC; [Pass/fail criteria](https://gettaurus.org/docs/PassFail/), truy cập 2026-07-14)** bzt exit codes: 0 no problem, 1 generic error, 2 manual shutdown, 3 automatic shutdown như pass/fail/cloud failure. **(DOC; [Command-line exit codes](https://gettaurus.org/docs/CommandLine/), truy cập 2026-07-14)**

## 5.6 Metrics, reports, raw artifacts và CI/CD

- Default reporters console + final-stats; optional JUnit XML, InfluxDB và BlazeMeter online report. final-stats có sample count, failure, average, latency/connect và percentiles; dump CSV/XML được hỗ trợ. **(DOC; [Taurus reporting](https://gettaurus.org/docs/Reporting/), truy cập 2026-07-14)**
- Artifacts chứa bzt.log, original/merged/effective config, executor stdout/stderr/log, KPI JTL/LDJSON và generated engine scripts như JMX/Scala/Python tùy executor. **(DOC; [Artifacts directory](https://gettaurus.org/docs/ArtifactsDir/), truy cập 2026-07-14)**
- JUnit XML có thể dùng pass-fail data source trong Jenkins; bzt exit code phù hợp pipeline. Official knowledge base có Jenkins integration. **(DOC; [Reporting/JUnit](https://gettaurus.org/docs/Reporting/), truy cập 2026-07-14; [Jenkins integration](https://gettaurus.org/kb/Jenkins/), truy cập 2026-07-14)**
- Docker image nhận YAML và mount artifacts. **(DOC; [Installation/Docker](https://gettaurus.org/install/Installation/), truy cập 2026-07-14)**

## 5.7 Local/offline, docs/community và AI

Default provisioning là local; Cloud provisioning yêu cầu BlazeMeter API key. **(DOC; [Cloud provisioning](https://gettaurus.org/docs/Cloud/), truy cập 2026-07-14)** Taurus/engines có thể auto-download, nhưng setting environment **TAURUS_DISABLE_DOWNLOADS** làm Taurus error thay vì tải tool; offline strict cần preinstall/pin JMeter/plugins/Python packages và tắt update checks. **(DOC; [Config syntax](https://gettaurus.org/docs/ConfigSyntax/), truy cập 2026-07-14)** Đây là local/offline capability có điều kiện, không phải “pip install xong luôn offline”.

Official docs, knowledge base, support forum và GitHub issues có sẵn; active 2026 release là tín hiệu bảo trì, không tự chứng minh quality. **(DOC; [Docs index](https://gettaurus.org/docs/Index/), truy cập 2026-07-14; [repo](https://github.com/Blazemeter/taurus), truy cập 2026-07-14)**

Taurus **không phải AI**. YAML thống nhất dễ để AI draft/review; repository hiện có CLAUDE.md mô tả architecture cho coding agent, nhưng đó là contributor guidance, không phải tự động sinh test đúng nghiệp vụ. **(DOC; [Taurus CLAUDE.md](https://github.com/Blazemeter/taurus/blob/master/CLAUDE.md), truy cập 2026-07-14; AI potential: ASSUMPTION)** Human audit: executor choice/version, supported fields, generated JMX, auto-download, plugins/JVM, secret redaction, passfail placement, artifact retention và Cloud upload.

## 5.8 EShop/classroom fit, strengths và limitations

**EShop fit:** khá-cao khi dùng JMeter executor vì YAML có multi-step requests, extractors, data và assertions; khả năng thật thuộc JMeter/plugins.  
**Classroom fit:** YAML dễ demo và rất tốt để dạy orchestration/abstraction, nhưng dễ che executor semantics; phải cho sinh viên đọc effective YAML + generated JMX.

**Strengths:** unified YAML; wraps existing scripts; common workload/report/passfail; artifacts/reproducibility; nhiều executors; local/cloud switch.  
**Limitations:** không phải load engine; executor-dependent parity; abstraction/debug cost; auto-download/version drift; Python + Java + engine dependencies; Cloud report/account optional; score không thể tách khỏi executor.

## 5.9 Smoke Test Plan — explicit JMeter executor

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

- **Objective:** chứng minh Taurus orchestration gọi JMeter, 1 VU/1 iteration, request assertion, passfail, JUnit và artifacts.
- **Prerequisites:** authorized target; Java/JMeter/Taurus versions pin; plugins pre-cached; đặt TAURUS_DISABLE_DOWNLOADS trong offline run; artifacts dir writable.
- **Install/setup:** pip/venv hoặc pinned image; explicit **executor: jmeter**; ghi bzt/Python/Java/JMeter/plugin/OS versions. **(DOC; [Installation](https://gettaurus.org/docs/Installation/), [JMeter executor](https://gettaurus.org/docs/JMeter/), truy cập 2026-07-14)**
- **Sample – smoke.yml:**

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

- **Command:** **bzt smoke.yml**
- **Expected:** Taurus prepares/generated JMX, JMeter executes one iteration, request assertion passes, passfail not triggered, exit 0, JTL/JMX/log/effective/merged/JUnit artifacts exist. Nếu passfail triggers, expected bzt exit class là 3. Đây chưa phải observation. **(DOC; [JMeter](https://gettaurus.org/docs/JMeter/), [PassFail](https://gettaurus.org/docs/PassFail/), [Exit codes](https://gettaurus.org/docs/CommandLine/), truy cập 2026-07-14)**
- **Evidence:** versions, original YAML/hash, command/env, bzt.log, merged/effective YAML+JSON, generated/modified JMX, JMeter log/JTL, executor stdout/stderr, xunit.xml, exit, timestamps, machine/SUT metadata.
- **Possible errors:** Python/Java/JMeter mismatch, auto-download blocked, plugin resolution, YAML translate difference, assertion subject, JUnit reporter order/path, TLS/auth, permission.
- **Success:** evidence proves executor JMeter; exactly one iteration/sample; assertion/passfail pass; exit 0; no hidden network download.

## 5.10 Scoring — conditional on JMeter executor

| Tiêu chí | Điểm | Lý do + DOC |
|---|---:|---|
| Cost & access | 5 | Apache-2.0 local; Cloud optional. [Repo](https://github.com/Blazemeter/taurus), [pricing](https://www.blazemeter.com/pricing) *(truy cập 2026-07-14)* |
| Learning curve | 4 | YAML ngắn nhưng phải hiểu executor/generated plan. [Execution](https://gettaurus.org/docs/ExecutionSettings/) *(truy cập 2026-07-14)* |
| EShop fit | 4 | JMeter-backed request/extractor/data; executor-dependent. [JMeter](https://gettaurus.org/docs/JMeter/) *(truy cập 2026-07-14)* |
| Multi-step journey | 4 | Requests/include/extractors tốt; abstraction parity cost. [JMeter](https://gettaurus.org/docs/JMeter/), [data](https://gettaurus.org/docs/DataSources/) *(truy cập 2026-07-14)* |
| Workload control | 4 | Unified concurrency/ramp/throughput, semantics vary executor. [Execution](https://gettaurus.org/docs/ExecutionSettings/) *(truy cập 2026-07-14)* |
| Assertions/checks | 4 | Request assertions + passfail; generated-engine semantics. [PassFail](https://gettaurus.org/docs/PassFail/) *(truy cập 2026-07-14)* |
| Reporting | 4 | Console/final/JUnit/CSV/XML/online; quality depends executor/report path. [Reporting](https://gettaurus.org/docs/Reporting/) *(truy cập 2026-07-14)* |
| CI/CD | 5 | bzt exit 0/1/2/3, JUnit, Docker/Jenkins. [CLI](https://gettaurus.org/docs/CommandLine/), [reporting](https://gettaurus.org/docs/Reporting/) *(truy cập 2026-07-14)* |
| Reproducibility | 5 | merged/effective config + generated scripts/artifacts. [Artifacts](https://gettaurus.org/docs/ArtifactsDir/) *(truy cập 2026-07-14)* |
| Local/offline | 4 | Local default, disable downloads; pre-cache executor/plugins. [Cloud](https://gettaurus.org/docs/Cloud/), [config](https://gettaurus.org/docs/ConfigSyntax/) *(truy cập 2026-07-14)* |
| AI-assisted potential | 4 | YAML/agent guidance; tool không AI, generated plan needs review. [CLAUDE.md](https://github.com/Blazemeter/taurus/blob/master/CLAUDE.md) *(truy cập 2026-07-14; ASSUMPTION)* |
| Classroom suitability | 3 | Dạy orchestration tốt nhưng dễ che JMeter semantics/setup. *(ASSUMPTION)* |

**Weighted Score: 83.4/100, có điều kiện trên JMeter executor; không dùng để tuyên bố Taurus “phát tải tốt hơn/kém hơn” engine độc lập. Chưa có EXP.**

## 5.11 Critical questions

1. **Taurus tự phát HTTP load khi executor là JMeter?** Không; Taurus orchestrate/generate, JMeter là underlying tool thực thi. **(DOC; [JMeter executor](https://gettaurus.org/docs/JMeter/), truy cập 2026-07-14)**
2. **Có thể so Taurus trực tiếp với k6 theo throughput/resource?** Không công bằng nếu không ghi executor/version/plugins; phải so “Taurus+JMeter” và đo abstraction overhead riêng. **(ASSUMPTION kiến trúc; [CẦN THỰC NGHIỆM])**
3. **Một YAML chạy giống hệt trên mọi executor?** Không; support và semantics load/data/assertion phụ thuộc executor. **(DOC; [Execution settings](https://gettaurus.org/docs/ExecutionSettings/), [Data sources](https://gettaurus.org/docs/DataSources/), truy cập 2026-07-14)**
4. **Taurus offline tự động?** Không; auto-install có thể tải JMeter/plugins. Phải pre-cache và dùng TAURUS_DISABLE_DOWNLOADS để phát hiện download. **(DOC; [JMeter](https://gettaurus.org/docs/JMeter/), [Config syntax](https://gettaurus.org/docs/ConfigSyntax/), truy cập 2026-07-14)**
5. **Chỉ giữ smoke.yml có đủ tái lập?** Không; cần effective/merged config, generated JMX, engine versions/plugins, logs/JTL và exit. **(DOC; [Artifacts](https://gettaurus.org/docs/ArtifactsDir/), truy cập 2026-07-14)**

---

# 6. Tóm tắt định vị và điểm

| Tool | Bản chất | Provisional category | Weighted score | Cách đọc đúng |
|---|---|---|---:|---|
| k6 | Load generator test-as-code | Main candidate | 97.4 | Điểm engine/tool trực tiếp; vẫn cần EXP |
| Locust | Python load framework | Shortlist | 90.8 | Mạnh logic; custom SLO gate/open-rate cần care |
| Gatling | Typed DSL load engine/platform | Shortlist | 90.2 | Mạnh workload/assertions; setup/licence/report nuance |
| Artillery | Node/YAML load toolkit | Backup | 86.8 | Arrival-centric; ensure bắt buộc; local HTML removed |
| Taurus | Orchestration/abstraction framework | Orchestration framework | 83.4 | Có điều kiện trên executor JMeter; không rank như engine |

Các score trên là **DOC-based preliminary scoring**, không phải benchmark. Thứ hạng có thể thay đổi sau smoke test, journey prototype và controlled experiment.

## Evidence bundle chung cần thu khi thực nghiệm

1. Tool/runtime/OS/container image versions và hashes.
2. Script/config/test data đã redacted; Git commit.
3. Exact command, env names, start/end timestamps, timezone.
4. stdout/stderr, exit code, raw result, local report.
5. Load-generator CPU/RAM/network và SUT build/config.
6. Request count, achieved VUs/RPS, dropped/missed work.
7. Authorization/scope và cleanup record.
8. Với Taurus: executor/JVM/plugins, merged/effective config và generated engine plan.

## AI Usage Declaration

AI đã được dùng để hỗ trợ lập cấu trúc nghiên cứu, đối chiếu các mục cần kiểm chứng, soạn bản nháp tiếng Việt, đề xuất scoring và smoke-test skeleton. AI **không chạy bất kỳ load test nào**, không tạo kết quả thực nghiệm và không được xem là nguồn chứng cứ. Mọi claim kiểm chứng được trong hồ sơ phải truy về official URL đặt ngay sau claim; mọi script do AI gợi ý phải được người phụ trách review, thay placeholder, kiểm quyền, pin version và chạy smoke test có lưu artifacts. Khi nộp bài, nhóm cần thay tuyên bố chung này bằng tên AI/tool cụ thể, prompt/action chính, phần nào đã được con người kiểm tra và thay đổi.
