### 1. Tổng quan

Loader.io là SaaS cloud load testing cho web application/API, điều khiển bằng web UI hoặc REST API; load generator do dịch vụ vận hành ([Loader.io](https://loader.io/), [API v2](https://loader.io/docs/v2/) — truy cập 2026-07-14). Trang đăng ký đặt Loader dưới Twilio Terms như “Beta Offering” ([Sign-up](https://loader.io/register/signup) — truy cập 2026-07-14). Evidence: `DOC`.

### 2. Cost và licence

Free: 0 USD/tháng, 10.000 clients/test, 1 target host, test 1 phút, 2 URL/test. Pro: 99,95 USD/tháng, 100.000 clients/test, unlimited hosts/10-minute tests, 10 URL/test và advanced analytics/team features ([Pricing](https://loader.io/pricing) — truy cập 2026-07-14). Evidence: `DOC`.

### 3. Installation và platform support

Không cài local runner; dùng browser/API. Mỗi host phải verify bằng HTTP token file; DNS verification chỉ paid. Generators ở AWS nên target phải public; localhost/private EShop không chạy trực tiếp ([Verify host](https://support.loader.io/article/20-verifying-an-app), [Local services FAQ](https://support.loader.io/article/80-can-i-test-the-local-services-hosted-on-local-machine) — truy cập 2026-07-14). Không offline/container phía người dùng. Evidence: `DOC`.

### 4. Scripting hoặc configuration model

Web form hoặc API JSON mô tả URL/method/headers/body/basic auth; nhiều URL chạy tuần tự. Cookie được giữ; response variable chỉ lấy response **header**; numeric expressions và public JSON payload files parameterize data ([Creating a test](https://support.loader.io/article/15-creating-a-test), [Variables](https://support.loader.io/article/18-variables), [Payload files](https://support.loader.io/article/17-payload-files) — truy cập 2026-07-14). API JSON lưu Git được; secret/payload public URL cần audit. Evidence: `DOC`.

### 5. Workload capabilities

`clients per test` phân tổng client theo duration; `clients per second` khởi tạo N client/giây; `maintain client load` tăng concurrency từ initial đến target và lặp URL sequence. Arrival start rate không bằng active concurrency ([Test types](https://support.loader.io/article/16-test-types), [API v2](https://loader.io/docs/v2/) — truy cập 2026-07-14). Cloud service tự phân tán; user không kiểm soát agent topology chi tiết và loader IP có thể đổi. Evidence: `DOC`.

### 6. Assertions và validation

`error_threshold` dựa trên HTTP `>=400` hoặc timeout và abort khi chạm ngưỡng. Không có documented response-body/business assertion; status `<400`, kể cả redirect, được tính success, nên HTTP 200 error page có thể lọt ([API v2](https://loader.io/docs/v2/), [Test Results](https://support.loader.io/article/19-test-results) — truy cập 2026-07-14). Evidence: `DOC`.

### 7. Metrics và reporting

UI/report có average/min/max response, success/4xx/5xx/timeout/network, bandwidth và graphs; Pro thêm histogram. Results API trả summary/average error rate/public URL. Không thấy p50/p95/p99 hay per-request raw timing export trong public schema: `[CẦN XÁC MINH]` ([Test Results](https://support.loader.io/article/19-test-results), [API v2](https://loader.io/docs/v2/) — truy cập 2026-07-14). Evidence: `DOC` + gap `ASSUMPTION`.

### 8. CI/CD và automation

API tạo/run/stop/poll; run/notify webhooks và Jenkins article có đường integration. Tạo test API tự chạy nếu không schedule; không có native CLI/exit-code contract, nên CI phải tự poll/map result và negative-test. Integration articles cũ nên compatibility cần xác minh ([Webhooks](https://support.loader.io/article/23-webhook), [Jenkins](https://support.loader.io/article/26-jenkins), [API v2](https://loader.io/docs/v2/) — truy cập 2026-07-14). Evidence: `DOC` + `[CẦN THỰC NGHIỆM]`.

### 9. EShop suitability

Tốt cho public endpoint smoke và basic URL sequence/cookie. Không phù hợp primary tool cho EShop local/private, token trong JSON body, rich business checks, browser assets hoặc mandatory p95/raw evidence. Loader không parse HTML/tải JS/CSS/image ([Linked resources](https://support.loader.io/article/39-do-you-load-linked-resources-assets) — truy cập 2026-07-14). Evidence: `DOC` + fit `ASSUMPTION`.

### 10. AI-assisted potential

AI dễ draft/audit API JSON và client math, nhưng không có native AI được công bố và không bù được thiếu body assertion/percentile/raw timing. Human phải kiểm tra target ownership, secret, workload và abort gate. Evidence: `ASSUMPTION`.

### 11. Classroom suitability

Zero-install/Free/UI rất nhanh, nhưng mỗi nhóm cần public host mình sở hữu/được phép verify, Internet và safe-load governance; activity 25 phút là `[CẦN THỰC NGHIỆM]` ([Verify host](https://support.loader.io/article/20-verifying-an-app) — truy cập 2026-07-14). Evidence: `DOC` + `ASSUMPTION`.

### 12. Điểm mạnh trong phạm vi seminar

Transparent free/pro pricing; zero-install; cloud scale; ba load models; API/webhook; cookie/header variables ([Pricing](https://loader.io/pricing), [API](https://loader.io/docs/v2/) — truy cập 2026-07-14). Evidence: `DOC`.

### 13. Hạn chế trong phạm vi seminar

SaaS/public-target only; free 1 phút/2 URL; no browser assets; header-only extraction; weak assertions; no documented percentiles/raw timing; nhiều Help articles cũ ([Docs collection](https://support.loader.io/collection/3-loaderio-docs) — truy cập 2026-07-14). Evidence: `DOC`/`ASSUMPTION` đã ghi.

### 14. Smoke Test Plan

**[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN]**

- **Mục tiêu:** verify host và chạy GET cloud tối thiểu; không đo capacity.
- **Prerequisites:** Free account, `[AUTHORIZED_PUBLIC_HOST]`, văn bản cho phép, WAF/cost guard, API key trong secret store.
- **Installation/setup:** đăng ký host; đặt HTTP verification token; ghi plan limits và loader IP list.
- **Request:** `GET https://[AUTHORIZED_PUBLIC_HOST]/[VERIFIED_READ_ONLY_PATH]`.
- **Command/config:** API JSON `test_type=per-test`, `total=15`, `duration=60`, `timeout=10000`, `error_threshold=1`, một GET; POST `/v2/tests` tự chạy ([API v2](https://loader.io/docs/v2/) — truy cập 2026-07-14).
- **Kết quả mong đợi:** completed, `success>0`, `error=timeout_error=network_error=0`; chưa quan sát; không đặt p95 gate.
- **Evidence:** authorization, plan/verification, redacted JSON/API responses, result JSON/report, server logs, loader IPs, time/timezone.
- **Lỗi có thể gặp:** verification/DNS, non-public host, TLS/WAF/429, threshold abort, leaked API key, unexpected hosting cost.
- **Tiêu chí thành công:** verify + completed + zero error/timeout/network và đủ artefact; test-only 404/timeout phải làm CI fail trước automation claim.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Lý do | Evidence |
|---|---:|---:|---|---|
| Cost & access | 8% | 3 | Free plan có quota công khai, nhưng bắt buộc account và verified public host nên access có điều kiện | DOC + ASSUMPTION |
| Learning curve | 8% | 5 | Web/API workflow ngắn | ASSUMPTION từ DOC |
| EShop fit | 15% | 3 | Public HTTP tốt; local/assertion hạn chế | DOC + ASSUMPTION |
| Multi-step journey & state | 12% | 3 | URL/cookie/header variable; Free 2 URL | DOC |
| Workload model & scalability | 10% | 4 | Per-test/per-second/maintain cloud | DOC |
| Assertions & business validation | 8% | 2 | Status/error/timeout, không body check | DOC |
| Metrics & reporting | 8% | 3 | Avg/min/max/errors; no documented percentile/raw | DOC + ASSUMPTION |
| CI/CD & automation | 7% | 4 | API/webhooks; custom gate/docs cũ | DOC + ASSUMPTION |
| Reproducibility | 7% | 3 | JSON lưu được; SaaS/IP/state biến động | DOC + ASSUMPTION |
| Local/offline | 5% | 1 | AWS generators cần public target | DOC |
| AI-assisted potential | 7% | 3 | JSON dễ draft; không native/capability mỏng | ASSUMPTION |
| Classroom suitability | 5% | 4 | Free/easy; public host governance | ASSUMPTION |
| Community | 0% | 3 | API/docs public nhưng nhiều Help articles cũ ([Docs](https://support.loader.io/collection/3-loaderio-docs) — truy cập 2026-07-14) | DOC; không tính |

**Weighted Score provisional: 64,0/100; 0 EXP.**

### 16. Kết luận sơ bộ

**Survey-only** với vai trò cloud supporting tool. Không chọn cho EShop local/live activity; có thể dùng comparator nếu có authorized public host.

### 17. Câu hỏi phản biện

<details>
<summary><strong>Câu hỏi phản biện Loader.io</strong></summary>

1. **Free 10.000 clients nghĩa là an toàn bắn 10.000?** Không; entitlement không phải safe workload. Bắt đầu minimum smoke và cần approval/capacity guard.
2. **Test localhost được không?** Không trực tiếp; AWS generator cần public target ([Local FAQ](https://support.loader.io/article/80-can-i-test-the-local-services-hosted-on-local-machine) — truy cập 2026-07-14).
3. **HTTP 200 chứng minh checkout đúng?** Không; body/business invariant không được kiểm tra bởi error threshold.
4. **Clients/s là concurrent users?** Không; đó là start rate, active concurrency phụ thuộc response time ([Test types](https://support.loader.io/article/16-test-types) — truy cập 2026-07-14).

</details>
