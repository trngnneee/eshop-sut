> **Trạng thái bằng chứng:** chỉ **[DOC]**, **[DOC + ASSUMPTION]**, **[ASSUMPTION]** và kế hoạch chưa chạy; ngày chốt 2026-07-14.

### 1. Tổng quan

Vegeta là HTTP load testing CLI/library do Tomás Senart (`tsenart`) duy trì, thiết kế chủ yếu cho constant request-rate attacks và report có thể xử lý tiếp. Bản phát hành chính thức hiện hành khi chốt là v12.13.0 (2025-10-31). [Repository](https://github.com/tsenart/vegeta), [release v12.13.0](https://github.com/tsenart/vegeta/releases/tag/v12.13.0) (truy cập 2026-07-14). **[DOC]**

### 2. Cost và licence

Source mở MIT, binary/source truy cập không cần tài khoản/trial. [LICENSE](https://github.com/tsenart/vegeta/blob/master/LICENSE), [Releases](https://github.com/tsenart/vegeta/releases) (truy cập 2026-07-14). **[DOC]**

### 3. Installation và platform support

README cung cấp precompiled executables và Homebrew, MacPorts, Arch, FreeBSD, hoặc build bằng `git clone`/`make vegeta`. Repo có Dockerfile để tự build image; phải pin asset/checksum hoặc image digest, không coi image cùng tên bất kỳ là first-party. [Install](https://github.com/tsenart/vegeta#install), [Dockerfile](https://github.com/tsenart/vegeta/blob/master/Dockerfile) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 4. Scripting hoặc configuration model

CLI pipeline + HTTP/line-delimited JSON targets; JSON hỗ trợ method/URL, headers và body base64. Go v12 API cung cấp `Targeter`, `Pacer`, `Attacker`; target/config dễ version-control, logic nâng cao cần code Go. [Targets](https://github.com/tsenart/vegeta#targets), [Go API](https://pkg.go.dev/github.com/tsenart/vegeta/v12/lib) (truy cập 2026-07-14). **[DOC]**

### 5. Workload capabilities

CLI có duration, constant `-rate`, workers/max-workers, connections, timeout; `-rate=0` có fixed-worker semantics. Go có Constant/Linear/Sine/custom Pacer. Static targeter phát nhiều target round-robin, không tạo VU session/cookie jar/correlation; staged ramp cần Go/orchestration. Distributed pattern chính thức chia rate qua SSH/pdsh và merge results, không phải controller-agent native. [Attack](https://github.com/tsenart/vegeta#attack-command), [Pacer API](https://pkg.go.dev/github.com/tsenart/vegeta/v12/lib#Pacer), [Distributed](https://github.com/tsenart/vegeta#distributed-attacks) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 6. Assertions và validation

Success mặc định là không lỗi và status 200–399; không có response-body/business assertion hoặc SLA threshold native. Policy script ngoài phải quyết định pass/fail. [Report](https://github.com/tsenart/vegeta#report-command) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 7. Metrics và reporting

Text/JSON/histogram/hdrplot có latency min/mean/percentiles/max, total/rate/throughput/success/status/errors/bytes. Raw binary/gob encode được JSON/CSV; CSV chứa timestamp/status/latency/bytes/error/body/name/sequence/method/URL/headers. `plot` sinh HTML, attack có Prometheus output. [Report](https://github.com/tsenart/vegeta#report-command), [Encode](https://github.com/tsenart/vegeta#encode-command), [Plot](https://github.com/tsenart/vegeta#plot-command) (truy cập 2026-07-14). **[DOC]**

### 8. CI/CD và automation

CLI, raw artifact và JSON report rất hợp pipeline/local/offline; performance gate/exit policy cần script riêng. Dockerfile source hỗ trợ build container có provenance. [Usage](https://github.com/tsenart/vegeta#usage), [Dockerfile](https://github.com/tsenart/vegeta/blob/master/Dockerfile) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 9. EShop suitability

Rất phù hợp catalog/product/search API độc lập và target mix tĩnh. Nhiều target round-robin không phải login→cart→checkout: request sau không lấy token/ID từ response trước của cùng user. Custom Go harness có thể làm thêm nhưng phải được test riêng. [NewStaticTargeter](https://pkg.go.dev/github.com/tsenart/vegeta/v12/lib#NewStaticTargeter), [Targeter API](https://pkg.go.dev/github.com/tsenart/vegeta/v12/lib#Targeter) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 10. AI-assisted potential

AI có thể sinh targets, parser JSON, policy, chart và Failure Mode audit; phải kiểm tra base64, secret/raw body, rate-vs-VU semantics, target round-robin, generator headroom và exit policy. [Targets](https://github.com/tsenart/vegeta#targets), [Report](https://github.com/tsenart/vegeta#report-command) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 11. Classroom suitability

Pipeline attack→raw→report→plot trực quan và có thể hoàn tất trong 25 phút nếu binary/endpoint sẵn, không cần tài khoản/Internet sau cài đặt. [Usage](https://github.com/tsenart/vegeta#usage) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 12. Điểm mạnh trong phạm vi seminar

Rate-based API benchmark, raw artifact giàu, percentile/report/plot tốt, tái lập và CI-friendly. [Attack](https://github.com/tsenart/vegeta#attack-command), [Report](https://github.com/tsenart/vegeta#report-command), [Encode](https://github.com/tsenart/vegeta#encode-command) (truy cập 2026-07-14). **[DOC]**

### 13. Hạn chế trong phạm vi seminar

Target độc lập không phải journey; thiếu business assertion/SLA gate; ramp phong phú cần Go Pacer; distributed là external orchestration. Đây là ranh giới endpoint/rate benchmark, không phải kết luận công cụ “kém”. [Targets](https://github.com/tsenart/vegeta#targets), [Pacer](https://pkg.go.dev/github.com/tsenart/vegeta/v12/lib#Pacer) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 14. Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

- **Mục tiêu:** GET constant-rate nhỏ, lưu raw binary→JSON→HTML.
- **Prerequisites:** `[VERIFIED_BASE_URL]`, `[VERIFIED_PRODUCT_PATH]`, `[EXPECTED_STATUS]`, binary pin, clock/resource monitoring. **[ASSUMPTION]**
- **Installation/setup:** cài/build theo [Install](https://github.com/tsenart/vegeta#install) và pin [release](https://github.com/tsenart/vegeta/releases/tag/v12.13.0) (truy cập 2026-07-14); lưu checksum/version.
- **Một request:** `targets.txt` chứa `GET [VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]` theo [HTTP target format](https://github.com/tsenart/vegeta#http-format) (truy cập 2026-07-14).
- **Command:** `vegeta attack -targets=targets.txt -rate=2/s -duration=10s -output=results.bin`; `vegeta report -type=json results.bin > report.json`; `vegeta plot results.bin > plot.html`. [Usage](https://github.com/tsenart/vegeta#usage) (truy cập 2026-07-14).
- **Expected result:** khoảng 20 requests nếu client theo kịp; report parse được; status theo contract; chưa dự đoán latency.
- **Evidence:** target/hash, version/checksum, commands, stdout/stderr/exit từng bước, `results.bin`, JSON, HTML, EShop commit, time/timezone, client/SUT resources, policy version.
- **Possible errors:** quoting/redirection; JSON body chưa base64; secret trong raw; TLS/timeout; rate vượt client; 3xx false-success; pipe che exit; container network/clock; report format mismatch.
- **Success criteria:** artifact chain đủ, report parse, status/error đúng contract, generator headroom, rerun được; chỉ gate SLA sau review.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Evidence |
|---|---:|---:|---|
| Cost & access | 8% | 5 | MIT/source/releases mở. **[DOC]** |
| Learning curve | 8% | 4 | CLI rõ; Go chỉ cho nâng cao. **[DOC]** |
| EShop fit | 15% | 3 | API tốt, session yếu. **[DOC + ASSUMPTION]** |
| Multi-step journey | 12% | 1 | Targets độc lập. **[DOC + ASSUMPTION]** |
| Workload control | 10% | 4 | Rate/workers + Go Pacers. **[DOC]** |
| Assertions/checks | 8% | 1 | Protocol success, không body check. **[DOC + ASSUMPTION]** |
| Reporting | 8% | 5 | Raw/JSON/CSV/hist/HTML/Prometheus. **[DOC]** |
| CI/CD | 7% | 3 | Pipeline tốt, gate ngoài. **[DOC + ASSUMPTION]** |
| Reproducibility | 7% | 5 | Version/target/rate/raw pin được. **[DOC]** |
| Local/offline | 5% | 5 | Binary/Dockerfile, không SaaS. **[DOC]** |
| AI-assisted potential | 7% | 4 | Target/policy/report dễ hỗ trợ. **[DOC + ASSUMPTION]** |
| Classroom suitability | 5% | 5 | Artifact pipeline trực quan. **[DOC + ASSUMPTION]** |
| Community | 0% | 4 | Repo/docs/releases công khai; không ảnh hưởng tổng. [Repository](https://github.com/tsenart/vegeta) (truy cập 2026-07-14). **[DOC]** |

**Tổng có trọng số: 70.2/100**; Community 0% không tham gia công thức.

### 16. Kết luận sơ bộ

**Supporting benchmark tool.** Là lựa chọn endpoint benchmark ưu tiên trong nhóm này, không thay journey tool.

### 17. Câu hỏi phản biện

<details>
<summary>Phản biện và trả lời</summary>

1. **Nhiều target là journey?** Không; static targeter round-robin các target độc lập. [NewStaticTargeter](https://pkg.go.dev/github.com/tsenart/vegeta/v12/lib#NewStaticTargeter) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
2. **Success 100% chứng minh checkout?** Không; success chỉ là không lỗi và status 200–399. [Report](https://github.com/tsenart/vegeta#report-command) (truy cập 2026-07-14). **[DOC]**
3. **Rate giống VU?** Không; rate là request arrival, worker giúp phát kịp nhưng không tạo business session. [Attack](https://github.com/tsenart/vegeta#attack-command) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
4. **Khi nào distributed?** Khi một generator chạm open-file/memory/CPU/network hoặc không đạt target rate. [Distributed](https://github.com/tsenart/vegeta#distributed-attacks) (truy cập 2026-07-14). **[DOC]**

</details>
