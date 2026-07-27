> **Trạng thái bằng chứng:** chỉ **[DOC]**, **[DOC + ASSUMPTION]**, **[ASSUMPTION]** và kế hoạch chưa chạy; ngày chốt 2026-07-14.

### 1. Tổng quan

Siege là CLI web load/benchmark do Jeffrey Fulmer/JoeDog duy trì, hỗ trợ URL list, GET/POST, cookie, Basic auth và các mode regression, internet simulation, brute-force. [Repository](https://github.com/JoeDog/siege), [Manual](https://www.joedog.org/siege/manual) (truy cập 2026-07-14). **[DOC]**

### 2. Cost và licence

Source mở GPL-3.0; README/COPYING ghi ngoại lệ liên kết OpenSSL. Không cần tài khoản/trial, phù hợp sinh viên nếu môi trường POSIX đã sẵn. [COPYING](https://github.com/JoeDog/siege/blob/master/COPYING), [README](https://github.com/JoeDog/siege/blob/master/README.md) (truy cập 2026-07-14). **[DOC]**

### 3. Installation và platform support

Nhắm POSIX/UNIX; FAQ nói không có native Windows, Cygwin là một đường khả dĩ. Có `apt-get install siege`; build HTTPS/gzip cần OpenSSL/zlib development package. Repo có Dockerfile guide để tự build image. [FAQ](https://www.joedog.org/siege/faq), [Dockerfile guide](https://github.com/JoeDog/siege/blob/master/Dockerfile.md) (truy cập 2026-07-14). **[DOC]**

### 4. Scripting hoặc configuration model

CLI + `.siegerc` + `urls.txt`; `siege.config` tạo config. URL file và biến tĩnh `$()`/`${}` dễ version-control nhưng không phải scripting/correlation DSL. [Manual](https://www.joedog.org/siege/manual) (truy cập 2026-07-14). **[DOC]**

### 5. Workload capabilities

`-c` users, `-t` duration, `-r` repetition, `-d` delay, `-b` benchmark, URL tuần tự hoặc `-i` random. Nhiều URL + cookie per-thread tạo page sequence tĩnh; không có staged arrival, response extractor hoặc dynamic token correlation được tài liệu hóa. [Manual](https://www.joedog.org/siege/manual), [FAQ](https://www.joedog.org/siege/faq) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 6. Assertions và validation

Status nhỏ hơn 400 được coi thành công. Không có custom response-body/business assertion hoặc SLA threshold native, nên redirect sai flow vẫn có thể được tính success. [Manual](https://www.joedog.org/siege/manual) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 7. Metrics và reporting

Báo transactions, availability, elapsed, data, average response, transaction rate, throughput, concurrency, success/fail; `-l` ghi aggregate log kiểu CSV. Standard report không có p50/p95/p99, raw per-request schema hay dashboard HTML. [Manual](https://www.joedog.org/siege/manual) (truy cập 2026-07-14). **[DOC]**

### 8. CI/CD và automation

CLI/container tự build phù hợp pipeline/local/offline, nhưng gate/parser/artifact policy và cookie isolation phải tự triển khai. Cookie có thể persist tại `$HOME/.siege/cookies.txt`. [Dockerfile guide](https://github.com/JoeDog/siege/blob/master/Dockerfile.md), [FAQ](https://www.joedog.org/siege/faq) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 9. EShop suitability

API/page tĩnh, POST và cookie hỗ trợ flow đơn giản. Login→product→cart→checkout có CSRF/JWT/ID động không phù hợp nếu không có correlation/extractor; hard-code token không đại diện session và dễ lộ secret. [Manual](https://www.joedog.org/siege/manual), [FAQ](https://www.joedog.org/siege/faq) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 10. AI-assisted potential

AI có thể sinh URL file/config/parser và Failure Mode checklist; phải audit cookie persistence, encoding, POST format, secret, `<400` semantics và Windows/WSL. AI không thể giả định correlation/assertion không có trong docs. [Manual](https://www.joedog.org/siege/manual), [FAQ](https://www.joedog.org/siege/faq) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 11. Classroom suitability

User/URL/delay trực quan và có thể demo trong 25 phút nếu WSL/image được chuẩn bị; tự setup Windows hoặc debug build có thể vượt timebox. [FAQ](https://www.joedog.org/siege/faq), [Dockerfile guide](https://github.com/JoeDog/siege/blob/master/Dockerfile.md) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 12. Điểm mạnh trong phạm vi seminar

Sequence URL tĩnh, cookie theo client, pacing dễ hiểu, CLI/log gọn và Dockerfile source chính thức. [Manual](https://www.joedog.org/siege/manual), [Dockerfile guide](https://github.com/JoeDog/siege/blob/master/Dockerfile.md) (truy cập 2026-07-14). **[DOC]**

### 13. Hạn chế trong phạm vi seminar

Thiếu dynamic correlation/business checks/percentile chuẩn; FAQ công bố HTTP/1.1 còn hạn chế (không pipelining/`100 Continue`, persistent connection chưa tốt) và không multipart POST. Đây là ranh giới traffic tĩnh, không phải kết luận tuyệt đối. [FAQ](https://www.joedog.org/siege/faq) (truy cập 2026-07-14). **[DOC]**

### 14. Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

- **Mục tiêu:** hai clients lặp một GET và tạo aggregate log.
- **Prerequisites:** `[VERIFIED_BASE_URL]`, `[VERIFIED_PRODUCT_PATH]`, `[EXPECTED_STATUS]`; Linux/WSL/image pin; `$HOME`/cookies cô lập. **[ASSUMPTION]**
- **Installation/setup:** cài theo [FAQ](https://www.joedog.org/siege/faq) hoặc build [Dockerfile](https://github.com/JoeDog/siege/blob/master/Dockerfile.md) (truy cập 2026-07-14); lưu version/source/image digest.
- **Một request:** `GET [VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]`.
- **Command:** đặt `logfile = [ARTIFACT_PATH]` trong isolated `.siegerc`, rồi chạy `siege -l -c 2 -r 5 -b "[VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]"`; `-l` chỉ bật logging, không nhận path. ([Manual](https://www.joedog.org/siege/manual), [`siegerc.in`](https://github.com/JoeDog/siege/blob/master/doc/siegerc.in) — truy cập 2026-07-14)
- **Expected result:** dự kiến 10 transactions, status theo contract, không transport/failure ở smoke load; chưa có latency giả định.
- **Evidence:** version/provenance, `.siegerc`, command, stdout/stderr/exit, log/hash, cookie isolation, EShop commit, time/timezone, client/SUT resources.
- **Possible errors:** native Windows; container routing; TLS/OpenSSL; stale cookie; 3xx false-success; HTTP/1.1 limitation; file descriptor; encoding; client saturation.
- **Success criteria:** count/status đúng, không transport error, cookie sạch, generator headroom, artifacts đủ rerun; không đặt p95 vì standard report không có.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Evidence |
|---|---:|---:|---|
| Cost & access | 8% | 5 | GPL/source mở. **[DOC]** |
| Learning curve | 8% | 4 | CLI/URL file dễ; POSIX setup. **[DOC]** |
| EShop fit | 15% | 3 | POST/cookie/URLs, thiếu correlation. **[DOC + ASSUMPTION]** |
| Multi-step journey | 12% | 2 | Sequence tĩnh. **[DOC + ASSUMPTION]** |
| Workload control | 10% | 3 | Users/duration/delay/random, không stage. **[DOC]** |
| Assertions/checks | 8% | 2 | `<400`, không business check. **[DOC + ASSUMPTION]** |
| Reporting | 8% | 2 | Aggregate, thiếu percentile/raw. **[DOC]** |
| CI/CD | 7% | 2 | Wrapper/gate/cookie isolation. **[DOC + ASSUMPTION]** |
| Reproducibility | 7% | 4 | Config pin được; kiểm soát cookies. **[DOC]** |
| Local/offline | 5% | 5 | Không SaaS/Dockerfile. **[DOC]** |
| AI-assisted potential | 7% | 3 | Hữu ích cho config/parser; audit semantics. **[DOC + ASSUMPTION]** |
| Classroom suitability | 5% | 4 | Trực quan nếu setup sẵn. **[DOC + ASSUMPTION]** |
| Community | 0% | 3 | Manual/FAQ/repo công khai; không ảnh hưởng tổng. [Repository](https://github.com/JoeDog/siege) (truy cập 2026-07-14). **[DOC]** |

**Tổng có trọng số: 62.2/100**; Community 0% không tham gia công thức.

### 16. Kết luận sơ bộ

**Supporting benchmark tool.** Hợp page-sequence tĩnh và demo concurrency, không phải runner cho checkout động.

### 17. Câu hỏi phản biện

<details>
<summary>Phản biện và trả lời</summary>

1. **URL list + cookie đã là journey?** Chỉ là sequence tĩnh; docs không có extractor/correlation/body assertion. [Manual](https://www.joedog.org/siege/manual) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
2. **`-c 100` là 100 người mua?** Là simulated clients của Siege, không bảo đảm business flow/pacing/session production. [Manual](https://www.joedog.org/siege/manual) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
3. **Vì sao còn hợp lớp học?** User/URL/delay trực quan; chỉ cần giới hạn claim và chuẩn bị WSL/image trước. [Manual](https://www.joedog.org/siege/manual), [Dockerfile guide](https://github.com/JoeDog/siege/blob/master/Dockerfile.md) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

</details>
