# Desk research: năm công cụ performance testing doanh nghiệp/cloud

**Phạm vi:** Apache JMeter, OpenText Silk Performer, Tricentis NeoLoad, OpenText Professional Performance Engineering (LoadRunner Professional), Loader.io.  
**Mốc kiểm tra nguồn:** 2026-07-14 (Asia/Bangkok).  
**Trạng thái bằng chứng:** chỉ desk research từ nguồn chính thức; chưa cài đặt, chưa đăng ký trial, chưa chạy lệnh, chưa tạo tải lên EShop và chưa đo kết quả thực nghiệm.

## Quy ước, giả định và cách chấm

- `DOC` = tài liệu/trang sản phẩm/trang giá chính thức. Không có dòng nào trong bảng điểm dưới đây được gắn `EXP`, vì chưa có thực nghiệm.
- `[CẦN XÁC MINH]` = tài liệu công khai chưa đủ để kết luận hoặc entitlement có thể thay đổi theo tài khoản/hợp đồng.
- `[KẾ HOẠCH – CHƯA THỰC NGHIỆM]` = thủ tục đề xuất để nhóm tự tái lập; các đầu ra ghi trong đó là **kỳ vọng**, không phải kết quả đã quan sát.
- Giả định bài EShop cần ít nhất HTTP(S), hành trình đăng nhập → xem sản phẩm → giỏ hàng → checkout, cookie/session, dữ liệu người dùng khác nhau, ramp-up và tiêu chí lỗi/độ trễ. URL, API contract, test account, seed data và SLO thật vẫn là `[CẦN XÁC MINH]`.
- Trọng số dùng để so sánh nội bộ, không được trình bày như rubric chính thức: Chi phí 8; Dễ học 8; Phù hợp EShop 15; Hành trình nhiều bước 12; Mô hình tải 10; Assertion 8; Báo cáo 8; CI/CD 7; Tái lập 7; Local/offline 5; AI-assisted 7; Lớp học 5. Điểm tổng = `Σ(điểm 1–5 / 5 × trọng số)`, tối đa 100.

| Công cụ | Điểm đề xuất /100 | Phân loại tạm thời | Lý do quyết định ngắn |
|---|---:|---|---|
| Apache JMeter | 90,2 | **Main candidate** | Miễn phí, local, hành trình/correlation/assertion mạnh, CLI và báo cáo chuẩn; đổi lại test plan XML và mô hình thread cần dạy kỹ. |
| Tricentis NeoLoad | 87,6 | **Survey-only / enterprise benchmark** | Trải nghiệm no-code/as-code, SLA, CLI exit code và AI rất mạnh; giá niêm yết khởi điểm cao cho lớp học. |
| LoadRunner Professional | 85,0 | **Backup / enterprise benchmark** | Community license 50 Vuser, protocol rộng, VuGen–Controller–Analysis đầy đủ; Windows-heavy và đường học/cài đặt lớn. |
| Silk Performer | 74,8 | **Survey-only** | Workload/BDL/correlation/report doanh nghiệp tốt; trial, tài liệu và quy trình Windows làm giảm khả năng tái lập trong seminar. |
| Loader.io | 64,0 | **Backup cho cloud smoke/load ngắn** | Cực nhanh để tạo tải cloud và có Free 10.000 client/test, nhưng cần account + verified public host; không chạy local/offline, assertion và số liệu phân phối còn hạn chế. |

> Các điểm trên là đánh giá thiết kế dựa trên `DOC`, chưa phải benchmark. Thứ hạng phải được rà soát lại sau khi chạy cùng một smoke test và một EShop journey có SLO thống nhất.

---

## 1. Apache JMeter

### 1.1. Loại công cụ, đơn vị duy trì, giấy phép và quyền truy cập

- JMeter là ứng dụng desktop/CLI mã nguồn mở, thuần Java, do Apache Software Foundation phát triển; trang chính thức mô tả nó dùng để load test và đo hiệu năng, hỗ trợ HTTP/HTTPS, REST/SOAP, FTP, JDBC, LDAP, JMS, mail, TCP, Java objects và một số giao thức khác ([Apache JMeter – trang chủ](https://jmeter.apache.org/) — truy cập 2026-07-14).
- Phân phối Apache dùng Apache License 2.0, cho phép sử dụng, sửa đổi và phân phối theo các điều khoản của giấy phép; không có phí license/VU từ Apache ([Apache Licenses](https://www.apache.org/licenses/) — truy cập 2026-07-14).
- Đây là công cụ mức protocol, **không phải browser** và không thực thi JavaScript như trình duyệt; vì vậy phép đo HTTP backend có thể rất tốt nhưng không thay thế Web Vitals hay browser rendering ([Apache JMeter – trang chủ, mục “JMeter is not a browser”](https://jmeter.apache.org/) — truy cập 2026-07-14).

### 1.2. Nền tảng và cài đặt

- JMeter yêu cầu Java 8 trở lên và chạy trên hệ điều hành có JVM tương thích; gói binary được giải nén rồi gọi script trong thư mục `bin` ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html) — truy cập 2026-07-14).
- Apache khuyến nghị dùng GUI để tạo/debug test plan và dùng non-GUI CLI cho load test; chạy tải lớn trong GUI làm tăng overhead và có thể làm sai kết quả ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html) — truy cập 2026-07-14).
- Tài liệu Apache được kiểm tra không chỉ ra một **official Docker image** do dự án phát hành; khả năng container hoá bằng image bên thứ ba là `[CẦN XÁC MINH]`, không nên ghi như năng lực chính thức.

### 1.3. Scripting/cấu hình và hành trình EShop

- Test plan được lưu dưới dạng `.jmx` (XML); GUI ghép sampler, config element, timer, pre/post-processor, assertion và listener. HTTP(S) Test Script Recorder có thể ghi request từ browser qua proxy ([HTTP(S) Test Script Recorder](https://jmeter.apache.org/usermanual/jmeter_proxy_step_by_step) — truy cập 2026-07-14).
- Hành trình nhiều bước được mô hình bằng nhiều HTTP Request theo thứ tự trong Thread Group. HTTP Cookie Manager giữ cookie/session, còn “same user on each iteration” cho phép kiểm soát việc giữ/reset state giữa các vòng lặp ([Component Reference – Thread Group và HTTP Cookie Manager](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14).
- CSV Data Set Config nạp dữ liệu ngoài và chia sẻ theo thread/thread group theo cấu hình; extractor (JSON, regular expression, boundary, CSS/XPath) lấy token/ID động rồi truyền qua biến `${name}`. Tutorial recorder chính thức minh hoạ correlation bằng extractor và biến ([Component Reference](https://jmeter.apache.org/usermanual/component_reference.html) và [Recorder tutorial](https://jmeter.apache.org/usermanual/jmeter_proxy_step_by_step) — truy cập 2026-07-14).
- JMeter có JSR223/Groovy cho logic tuỳ biến, nhưng script tự viết phải được review vì có thể thêm CPU/memory overhead vào máy phát tải ([Component Reference – JSR223 elements](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14).

### 1.4. Mô hình tải và phân tán

- Thread Group cổ điển ánh xạ số thread sang số virtual user, với ramp-up, loop count, duration và startup delay; đây là closed/concurrency-oriented model ([Component Reference – Thread Group](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14).
- Open Model Thread Group hỗ trợ schedule arrival rate ngẫu nhiên nhưng được tài liệu đánh dấu **experimental**; timer như Constant Throughput và Precise Throughput điều khiển tốc độ ở những mức khác nhau, vì vậy nhóm phải nói rõ đang điều khiển concurrency hay arrival/throughput ([Component Reference – Open Model Thread Group và timers](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14).
- Remote testing cho phép một controller điều phối nhiều engine. Mỗi engine chạy **toàn bộ** test plan; ví dụ chính thức nêu 1.000 thread trên sáu server tạo 6.000 thread, đồng thời yêu cầu cùng phiên bản JMeter/Java và tự sao chép data file đến từng node ([Remote Testing](https://jmeter.apache.org/usermanual/remote-test.html) — truy cập 2026-07-14).
- CLI phân tán dùng dạng `jmeter -n -t test.jmx -R host1,host2 -l results.jtl`; RMI/port/firewall và đồng bộ clock là chi phí vận hành phải tính vào reproducibility ([Remote Testing](https://jmeter.apache.org/usermanual/remote-test.html) — truy cập 2026-07-14).

### 1.5. Assertion, báo cáo và dữ liệu thô

- Response Assertion có thể kiểm tra response code, text/body, headers, URL, kích thước; JSON Assertion và XPath assertion hỗ trợ cấu trúc JSON/XML. Assertion failure làm sample thất bại nhưng không mặc nhiên chứng minh trạng thái nghiệp vụ downstream đúng ([Component Reference – Assertions](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14).
- Kết quả có thể ghi CSV hoặc XML `.jtl`; Simple Data Writer là lựa chọn nhẹ hơn listener GUI khi chạy tải ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html) và [Component Reference – Simple Data Writer](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14).
- HTML dashboard sinh từ CSV/JTL hiển thị APDEX, success/failure, errors, response-time over time, active threads, bytes throughput và ba percentile cấu hình được; mặc định cấu hình dashboard dùng các percentile được nêu trong properties, cần lưu file cấu hình cùng artefact để tái lập ([Generating Dashboard](https://jmeter.apache.org/usermanual/generating-dashboard.html) — truy cập 2026-07-14).
- Aggregate Report cung cấp average, median, min/max, error %, throughput, received/sent KB/s và các percentile; listener GUI không nên bật trong load run lớn ([Component Reference – Aggregate Report](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14).

### 1.6. CLI, CI/CD, pass/fail và local/offline

- Lệnh tiêu chuẩn để chạy và sinh report là `jmeter -n -t test.jmx -l results.jtl -e -o report`; thư mục report phải không tồn tại hoặc rỗng ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html) — truy cập 2026-07-14).
- Trang chính thức nêu có thể tích hợp CI bằng giải pháp bên thứ ba như Maven, Gradle và Jenkins; tài liệu CLI không cam kết một exit code threshold/SLO tương đương NeoLoad. Vì vậy CI gate nên parse `.jtl`/dashboard hoặc dùng integration được audit, thay vì giả định “process 0 = mọi SLA đạt” ([Apache JMeter – CI integration](https://jmeter.apache.org/) và [Getting Started](https://jmeter.apache.org/usermanual/get-started.html) — truy cập 2026-07-14).
- Sau khi đã tải JMeter/JDK và dependency cần thiết, thiết kế/chạy/report có thể ở local/offline; Backend Listener chỉ cần mạng khi chủ động gửi metric ra hệ thống ngoài ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html) — truy cập 2026-07-14).

### 1.7. Cộng đồng, tài liệu và AI-assisted potential

- Dự án cung cấp user manual, component reference, issue tracker/source repository và mailing lists công khai ([JMeter source repositories](https://jmeter.apache.org/svnindex.html) và [Mailing lists](https://jmeter.apache.org/mail.html) — truy cập 2026-07-14).
- **Tiềm năng AI-assisted (suy luận có kiểm soát):** AI có thể phác thảo Groovy, assertion, extractor và giải thích `.jmx`, nhưng XML lớn khó review hơn code thuần; không tìm thấy tuyên bố chính thức về trợ lý AI native của Apache JMeter trong tài liệu đã kiểm tra. Mọi output AI phải qua human audit, chạy single-user debug và kiểm tra secret/token; nghiên cứu này không gọi công cụ AI bên thứ ba.

### 1.8. Phù hợp EShop, lớp học, điểm mạnh và giới hạn

**Phù hợp EShop:** rất cao ở lớp HTTP/API: login/session cookie, CSRF correlation, catalog/cart/checkout tuần tự, CSV account/product và assertion JSON/body đều có primitive chính thức. Không đo browser rendering/JavaScript; nếu EShop phụ thuộc SPA, cần ghép thêm browser/RUM tool ([JMeter protocol-level limitation](https://jmeter.apache.org/) — truy cập 2026-07-14).

**Lớp học:** license bằng 0 và chạy local là lợi thế; đường học cần giải thích thread ≠ request rate, listener overhead, correlation và cách lưu environment variables/secrets. `.jmx` merge conflict cũng khó đọc hơn script code.

**Điểm mạnh:** miễn phí; protocol và component phong phú; distributed; raw JTL; HTML report; recorder; local/offline.  
**Giới hạn:** không phải browser; GUI không dành cho load run; `.jmx` verbose; CI threshold/exit gate cần thiết kế thêm; remote RMI và data synchronization có operational cost.

### 1.9. Bảng điểm đề xuất — toàn bộ `DOC`, chưa benchmark

| Tiêu chí | Điểm | Lý do ngắn và bằng chứng |
|---|---:|---|
| Chi phí | 5 | Apache License 2.0, không phí VU ([license](https://www.apache.org/licenses/) — truy cập 2026-07-14). |
| Dễ học | 3 | GUI/recorder giúp khởi đầu, nhưng component tree, correlation và thread model cần đào tạo ([recorder](https://jmeter.apache.org/usermanual/jmeter_proxy_step_by_step) — truy cập 2026-07-14). |
| Phù hợp EShop | 5 | HTTP, REST/SOAP, cookie, extractor, data và assertion bao phủ backend journey ([trang chủ](https://jmeter.apache.org/), [component reference](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14). |
| Hành trình nhiều bước | 5 | Request tuần tự, cookie/session, variables và correlation đầy đủ ([component reference](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14). |
| Mô hình tải | 5 | Thread/ramp/duration, throughput timers, open model experimental, distributed engines ([component reference](https://jmeter.apache.org/usermanual/component_reference.html), [remote](https://jmeter.apache.org/usermanual/remote-test.html) — truy cập 2026-07-14). |
| Assertion | 5 | Code/body/header/JSON/XPath assertions ([component reference](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14). |
| Báo cáo | 5 | JTL raw, HTML dashboard, APDEX/error/percentile/throughput ([dashboard](https://jmeter.apache.org/usermanual/generating-dashboard.html) — truy cập 2026-07-14). |
| CI/CD | 4 | CLI mạnh, nhưng threshold gate không được core CLI mô tả như một hợp đồng exit code ([getting started](https://jmeter.apache.org/usermanual/get-started.html) — truy cập 2026-07-14). |
| Tái lập | 4 | `.jmx`, CLI và CSV version-control được; plugin/version/remote data cần khoá riêng ([remote](https://jmeter.apache.org/usermanual/remote-test.html) — truy cập 2026-07-14). |
| Local/offline | 5 | Java app chạy local, không phụ thuộc SaaS để phát tải/report ([getting started](https://jmeter.apache.org/usermanual/get-started.html) — truy cập 2026-07-14). |
| AI-assisted | 3 | Có artefact XML/Groovy để AI hỗ trợ nhưng không có native AI chính thức được xác nhận; human audit bắt buộc. |
| Lớp học | 4 | Miễn phí và đa nền tảng; cần kiểm soát resource/listener và dạy đúng mô hình tải ([getting started](https://jmeter.apache.org/usermanual/get-started.html) — truy cập 2026-07-14). |

**Tổng có trọng số: 90,2/100. Phân loại: Main candidate.**

### 1.10. Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

1. Điều kiện: xác nhận Java `>=8`, lấy binary từ Apache, lưu checksum/version; dùng `[VERIFIED_BASE_URL]` và endpoint GET chỉ đọc, được chủ hệ thống cho phép ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html) — truy cập 2026-07-14).
2. Trong GUI tạo `Test Plan → Thread Group (1 thread, ramp 1 s, 1 loop) → HTTP Request GET [VERIFIED_BASE_URL]/[HEALTH_OR_CATALOG_PATH] → Response Assertion (HTTP 200 và marker body không chứa secret) → Simple Data Writer`.
3. Lưu `jmeter-smoke.jmx`, đóng GUI, chạy:

   ```powershell
   .\bin\jmeter.bat -n -t .\jmeter-smoke.jmx -l .\artifacts\jmeter-smoke.jtl -e -o .\artifacts\jmeter-report
   ```

4. **Kỳ vọng, chưa quan sát:** một sample hoàn tất; response code/assertion đạt; JTL tồn tại; `report/index.html` sinh được. Các lỗi cần chủ động thử và ghi nhận: DNS/TLS, 401/403, 404, assertion body sai, report directory đã có dữ liệu.
5. Tiêu chí smoke đạt: không lỗi transport; đúng một sample; `success=true`; assertion đạt; artefact gồm version/checksum, `.jmx`, `.jtl`, `jmeter.log`, report và exact command. Không suy rộng từ smoke sang khả năng chịu tải.

### 1.11. Phản biện dự kiến

1. **Hỏi:** “JMeter có GUI thì tại sao không chạy 1.000 user ngay trong GUI?”  
   **Đáp:** Apache chỉ định GUI cho tạo/debug và CLI cho load run; listener/GUI thêm overhead và có thể làm méo kết quả ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html) — truy cập 2026-07-14).
2. **Hỏi:** “1.000 thread có đồng nghĩa 1.000 request/second?”  
   **Đáp:** Không. Thread Group là concurrency/closed model; throughput còn phụ thuộc response time, think time và timer. Nếu cần arrival-rate phải dùng timer/open model thích hợp và công bố rõ model ([Component Reference](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14).
3. **Hỏi:** “JMeter có thay thế browser test cho SPA EShop không?”  
   **Đáp:** Không. Apache nói rõ JMeter không phải browser và không thực thi JavaScript; nên dùng nó cho protocol load rồi ghép browser measurement riêng ([JMeter](https://jmeter.apache.org/) — truy cập 2026-07-14).
4. **Hỏi:** “CLI trả 0 thì SLA chắc chắn pass?”  
   **Đáp:** Không nên giả định. Assertion failures nằm trong sample/result, còn threshold-based build gate phải được parse/định nghĩa và kiểm thử riêng ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html) — truy cập 2026-07-14).

---

## 2. OpenText Silk Performer

### 2.1. Loại công cụ, đơn vị duy trì, license/trial

- Silk Performer là bộ performance/load testing thương mại do OpenText cung cấp; marketplace mô tả khả năng mô phỏng virtual user cho Internet server, database, distributed application và middleware, kèm phân tích/report ([OpenText Marketplace – Silk Performer](https://marketplace.opentext.com/appdelivery/content/silk-performer) — truy cập 2026-07-14).
- Documentation catalog công khai mới nhất được tìm thấy là Silk Performer 21.0 ([Silk Performer documentation](https://www.microfocus.com/documentation/silk-performer/) — truy cập 2026-07-14). Việc tài liệu vẫn ở domain `microfocus.com` là hạ tầng tài liệu lịch sử; sản phẩm hiện được marketplace OpenText duy trì.
- Installation Guide 21.0 mô tả Evaluation license dùng đầy đủ sản phẩm trong **45 ngày nhưng giới hạn 10 virtual user**, còn Licensed version yêu cầu license; giá niêm yết công khai không được tìm thấy trên trang sản phẩm đã kiểm tra nên tổng chi phí là `[CẦN BÁO GIÁ/XÁC MINH]` ([Installation Guide 21.0 PDF](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-installationguide-en.pdf) — truy cập 2026-07-14).
- Workbench Help 21.0 ở một đoạn lại mô tả trial **30 ngày**, mâu thuẫn với Installation Guide 45 ngày; nhóm phải xác nhận entitlement sau đăng ký thay vì chọn con số thuận lợi ([Workbench Help 21.0 PDF](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-workbenchhelp-en.pdf) — truy cập 2026-07-14).

### 2.2. Nền tảng, cài đặt và kiến trúc

- Guide 21.0 liệt kê Workbench/Controller trên Windows 8.1 trở lên hoặc Windows Server 2012 trở lên, khoảng 2,5 GB cho controller; agent có thể cài riêng trên máy phát tải và cần khoảng 1 GB. Installer yêu cầu quyền quản trị ([Installation Guide 21.0 PDF](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-installationguide-en.pdf) — truy cập 2026-07-14).
- Silent installation được hỗ trợ bằng response file/command-line installer, hữu ích cho lab image nhưng vẫn phải xử lý license và Windows prerequisites ([Installing in silent mode](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-7DA0F053-INSTALLINGSILENTMODE-TSK.html) — truy cập 2026-07-14).
- Workbench là trung tâm tạo project/script, cấu hình workload, chạy và phân tích; agent thực thi virtual user từ xa ([Workbench overview](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-5DDD4723-WORKBENCH-CON.html) — truy cập 2026-07-14).
- Không tìm thấy hướng dẫn container chính thức cho Silk Performer 21.0 trong bộ nguồn đã kiểm tra; container support là `[CẦN XÁC MINH]`, không chấm như năng lực có sẵn.

### 2.3. Script, session/correlation và dữ liệu

- Silk Performer dùng Benchmark Description Language (BDL) và cũng cung cấp Java framework cho user logic; Java framework có project template/runtime riêng ([Java framework](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-E71FE522-JAVAFM-CON.html) — truy cập 2026-07-14).
- Web recorder/Workbench tạo transaction từ traffic; bản phát hành 19.5 bổ sung nhập HAR, giúp chuyển network capture thành test asset nhưng vẫn phải audit correlation và assertion ([Silk Performer 19.5 Release Notes PDF](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-releasenotes-en.pdf) — truy cập 2026-07-14).
- Parsing functions trích dữ liệu động từ response và đưa vào request sau; advanced parsing/context management hỗ trợ correlation tự động trong Web workload ([Parsing functions](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-0A2D472E-PARSINGFUNCTIONS-CON.html) và [Advanced parsing/context](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/GUID-3DBE7DC1-2C3B-40EB-B9AF-D2038EDD6790.html) — truy cập 2026-07-14).
- Mỗi web virtual user có browser-level cookie/cache/history độc lập; Web settings điều khiển cookie, authentication, recording và verification, phù hợp login/cart session ([Virtual users and browser state](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-02867815-BDWLT-RUNMULTVIRTUSERS-CON.html) và [Web settings](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-790881A8-WEBSETTINGS-CON.html) — truy cập 2026-07-14).
- File functions có sequential/random access và user-data wizard hỗ trợ nhiều cột; vì vậy có thể parameterize account/product/cart data ([Extended file functions](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-53DA3120-EXTENDEDFILEFUNCTIONS-CON.html) và [Multi-column input parameter](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-50756884-CREATINGINPUTPARAMETERMULTICOLUMN-TSK.html) — truy cập 2026-07-14).

### 2.4. Workload, phân tán và scenario

- Tài liệu mô tả Increasing, Steady State, Dynamic, All Day, Queuing và Verification workload; Queuing model dùng arrival rate, còn Verification chạy virtual user để kiểm tra script trước load ([Workload models](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-webhelp-en/SILKPERF-390794D9-WORKLOADMODELS-CON.html) — truy cập 2026-07-14).
- Steady State chia warm-up, measurement, close-down và có ramp-up/ramp-down; Dynamic workload cho phép thay đổi tải trong lúc chạy ([Steady-state workload](https://www.microfocus.com/documentation/silk-performer/200/en/silkperformer-200-webhelp-en/SILKPERF-A03F6D65-CONFIGURINGSTEADYSTATEWORKLOAD-TSK.html) và [Adjust current workload](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/GUID-C4869025-15B9-4CA7-B474-E88535051425.html) — truy cập 2026-07-14).
- Workload Configuration cho phép gán agent và phân phối virtual user giữa nhiều máy phát tải ([Agent assignment](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-webhelp-en/SILKPERF-0A0FF53D-WORKLOADCONFIGURATIONDIALOG-AGENTASSIGNMENT-REF.html) — truy cập 2026-07-14).

### 2.5. Verification, báo cáo và raw output

- Web load-testing tutorial chính thức hướng dẫn verification response content; Workbench Help mô tả verification cho HTML/XML/data và đánh dấu error khi điều kiện sai ([Web Load Testing Tutorial PDF](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webloadtestingtutorial-en.pdf) và [Workbench Help PDF](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-workbenchhelp-en.pdf) — truy cập 2026-07-14).
- Performance Explorer/Workbench cung cấp real-time monitoring trong run và kết quả có thể xem/export qua browser HTML ([Real-time monitoring](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/GUID-626CEE1A-9989-4E61-B54D-7C6A1CCC387B.html) và [View results in browser](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-7CBD1FDA-VIEWINGRESULTSINWEBBROWSER-CON.html) — truy cập 2026-07-14).
- Virtual-user output/log files và time-series result data (`.tsd`) hỗ trợ điều tra; percentile function có mức chính xác/cost bộ nhớ cấu hình được, nên report phải lưu cả setting percentile ([Virtual user output files](https://cabs.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-A44C29BE-VIRTUALUSEROUTPUTFILES-CON.html), [Percentile function](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-webhelp-en/GUID-271C001F-FE5E-4B28-AA37-1B087F916493.html) — truy cập 2026-07-14).
- Baseline/performance thresholds có thể dùng để đánh giá measure so với giới hạn đã xác định ([Confirm test baselines](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-B176837E-CONFIRMINGTESTBASELINES-CON.html) — truy cập 2026-07-14).

### 2.6. CLI, CI/CD, local/offline và AI

- Automation command được tài liệu hoá theo dạng `performer project.ltp /Automation 5 /WL:Workload /Resultsdir:<path>`; lỗi được ghi vào Windows Event Viewer, nhưng tài liệu công khai được kiểm tra chưa quy định rõ một contract exit-code theo threshold cho mọi trường hợp ([Command-line automation](https://www.microfocus.com/documentation/silk-performer/205/en/silkperformer-205-webhelp-en/GUID-BE43A9E4-6B4C-46CB-BCA9-6A3E7CE51F36.html) — truy cập 2026-07-14).
- Release Notes chính thức mô tả Jenkins integration có thể chạy project, thu kết quả và dùng success conditions/performance levels; version/plugin compatibility vẫn cần xác minh trong lab ([Silk Performer 19.5 Release Notes PDF](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-releasenotes-en.pdf) — truy cập 2026-07-14).
- Licensed Workbench/agent chạy on-premises và có thể test hệ thống nội bộ; acquisition/activation của trial/license có thể cần kết nối ngoài, vì vậy “fully air-gapped” là `[CẦN XÁC MINH VỚI LICENSE SERVER]` ([Installation Guide PDF](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-installationguide-en.pdf) — truy cập 2026-07-14).
- **AI-assisted potential:** HAR + BDL/Java là đầu vào có cấu trúc để AI phác thảo/check script, nhưng không tìm thấy công bố native AI hiện hành trong tài liệu Silk Performer 21.0 đã kiểm tra. Điểm AI chỉ phản ánh khả năng trợ giúp bên ngoài, không phải tính năng được cấp license; human review, secret scrub và single-user replay bắt buộc.

### 2.7. Fit, điểm mạnh/giới hạn và bảng điểm

**EShop fit:** mạnh cho Web/API journey có session, token, data và workload nhiều pha. **Classroom fit:** thấp hơn JMeter vì Windows/admin/license, trial giới hạn 10 VU và tài liệu trial mâu thuẫn.  
**Điểm mạnh:** workload doanh nghiệp đa dạng; correlation/parser; distributed agents; analysis/percentile/threshold.  
**Giới hạn:** thương mại và giá không công khai; Windows-heavy; tài liệu public mới nhất tìm thấy ở 21.0 và có mâu thuẫn 30/45 ngày; container/exit-code contract chưa đủ bằng chứng.

| Tiêu chí | Điểm | Lý do ngắn và bằng chứng |
|---|---:|---|
| Chi phí | 2 | Trial 10 VU, commercial license và giá cần báo giá ([install guide](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-installationguide-en.pdf) — truy cập 2026-07-14). |
| Dễ học | 2 | Workbench hỗ trợ workflow nhưng BDL/agent/workload model tạo đường học dài ([Workbench](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-5DDD4723-WORKBENCH-CON.html) — truy cập 2026-07-14). |
| Phù hợp EShop | 4 | Web session, parsing, data, verification tốt; access friction làm giảm điểm ([Web settings](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-790881A8-WEBSETTINGS-CON.html) — truy cập 2026-07-14). |
| Hành trình nhiều bước | 5 | Cookie state, correlation và multi-column data đầy đủ ([parsing](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-0A2D472E-PARSINGFUNCTIONS-CON.html) — truy cập 2026-07-14). |
| Mô hình tải | 5 | Concurrency, arrival/queuing, steady/dynamic/all-day, agents ([workload models](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-webhelp-en/SILKPERF-390794D9-WORKLOADMODELS-CON.html) — truy cập 2026-07-14). |
| Assertion | 4 | Content verification và threshold tốt; mức linh hoạt cần kiểm tra theo protocol ([tutorial](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webloadtestingtutorial-en.pdf) — truy cập 2026-07-14). |
| Báo cáo | 5 | Real-time, HTML, raw/log, percentile và baseline ([result view](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-7CBD1FDA-VIEWINGRESULTSINWEBBROWSER-CON.html) — truy cập 2026-07-14). |
| CI/CD | 4 | Automation CLI và Jenkins có tài liệu; exit semantics cần lab verify ([CLI](https://www.microfocus.com/documentation/silk-performer/205/en/silkperformer-205-webhelp-en/GUID-BE43A9E4-6B4C-46CB-BCA9-6A3E7CE51F36.html) — truy cập 2026-07-14). |
| Tái lập | 3 | Project/workload lưu được, nhưng license/Windows/agent/version làm môi trường nặng. |
| Local/offline | 4 | On-premises runner; activation/air-gap cần xác minh ([install guide](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-installationguide-en.pdf) — truy cập 2026-07-14). |
| AI-assisted | 3 | HAR và BDL dễ cung cấp context, nhưng không có native AI được xác nhận ([release notes](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-releasenotes-en.pdf) — truy cập 2026-07-14). |
| Lớp học | 2 | Trial/Windows/admin và tài liệu trial mâu thuẫn làm giảm khả năng tái lập. |

**Tổng có trọng số: 74,8/100. Phân loại: Survey-only.**

### 2.8. Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

1. Trên Windows lab có admin, cài đúng Silk Performer 21.0; ghi installer checksum, OS, license type và quan sát entitlement thực (30 hay 45 ngày, 10 VU). Không nhập credential thật vào artefact.
2. Workbench tạo Web project `silk-smoke`, model một GET đến `[VERIFIED_BASE_URL]/[READ_ONLY_PATH]`, thêm status/content verification, tạo `Verification` workload 1 VU/1 iteration; lưu `.ltp`, script BDL và workload.
3. Replay trong Verification mode trước; sau đó automation dự kiến:

   ```powershell
   performer C:\lab\silk-smoke\silk-smoke.ltp /Automation 5 /WL:Verification /Resultsdir:C:\lab\artifacts\silk-smoke
   ```

4. **Kỳ vọng, chưa quan sát:** request đúng endpoint; verification pass; output/result/report được tạo; Windows Event Viewer không có automation error. Thử có kiểm soát một body marker sai để xác nhận failure propagation và process status thật.
5. Artefact bắt buộc: version/license screenshot đã che ID, project/script/workload, exact command, stdout/stderr, Event Viewer export, VU output, result/report. Chỉ sau thử nghiệm negative mới quyết định CI gate.

### 2.9. Phản biện dự kiến

1. **Hỏi:** “Trial chính xác 30 hay 45 ngày?”  
   **Đáp:** Hai tài liệu 21.0 mâu thuẫn; Installation Guide nói 45, Workbench Help có đoạn nói 30. Báo cáo phải công khai mâu thuẫn và lấy entitlement tài khoản thực làm bằng chứng, không tự hoà giải ([Install Guide](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-installationguide-en.pdf), [Workbench Help](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-workbenchhelp-en.pdf) — truy cập 2026-07-14).
2. **Hỏi:** “10 VU có đủ chứng minh scalability không?”  
   **Đáp:** Không. Nó đủ smoke/learning và kiểm tra script, không đủ kết luận capacity; workload lớn cần license và benchmark được phê duyệt.
3. **Hỏi:** “Có thể thay JMeter chỉ vì Silk có report đẹp hơn?”  
   **Đáp:** Không. Quyết định còn phụ thuộc license access, reproducibility và classroom fit; report mạnh chỉ là hai tiêu chí trong ma trận.
4. **Hỏi:** “CLI có tự động làm build fail khi threshold fail không?”  
   **Đáp:** Tài liệu public nêu automation/Jenkins success conditions nhưng chưa đủ để cam kết exit-code contract. Phải chạy cả positive/negative case và lưu process exit code trước khi gate CI.

---

## 3. Tricentis NeoLoad

### 3.1. Loại công cụ, maintainer, giá và quyền truy cập

- NeoLoad là nền tảng commercial performance testing của Tricentis, có protocol-based và RealBrowser, GUI no-code, as-code, CLI/API và cloud/on-premises execution ([NeoLoad product page](https://www.tricentis.com/products/performance-testing-neoload) — truy cập 2026-07-14).
- Giá chính thức công khai bắt đầu từ **20.000 USD/năm**, gồm 300 virtual user và annual subscription; trang giá cũng cung cấp “Try for free” ([NeoLoad pricing](https://www.tricentis.com/products/performance-testing-neoload/pricing) — truy cập 2026-07-14).
- Quick Start mô tả Free Edition/NeoLoad Web free plan và hướng liên hệ để trial sâu hơn. Tài liệu công khai kiểm tra được không nêu ổn định một giới hạn Web-VU/test chính xác cho Free Edition hiện hành, nên giới hạn đó là `[CẦN XÁC MINH TRONG ENTITLEMENT]`, không suy từ blog/version cũ ([Quick Start Guide](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/quick_start_guide.htm) — truy cập 2026-07-14).
- Khi không có key, NeoLoad cho thiết kế/phân tích nhưng không launch test; vì vậy “tải được installer” không đồng nghĩa “chạy tải được” ([Manage licenses](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/manage_licenses.htm) — truy cập 2026-07-14).

### 3.2. Platform, cài đặt và kiến trúc

- System requirements hiện hành liệt kê Windows, Linux và macOS cho các thành phần phù hợp, yêu cầu Java 21 và đưa ra CPU/RAM/disk theo Controller/Load Generator; cấu hình lab phải bám đúng matrix phiên bản ([System requirements](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/system_requirements.htm) — truy cập 2026-07-14).
- Controller 2026.2 có installer/command cho Windows, Linux và macOS; Controller chứa built-in Load Generator/Monitoring Agent và có thể quản lý agent từ xa ([Install Controller](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/install_the_controller.htm) và [Start Controller](https://docs.tricentis.com/neoload-2026.1/en-us/content/get_started/start_the_controller.htm) — truy cập 2026-07-14).
- Deployment guide mô tả container/Kubernetes cho NeoLoad runtime components; đây là official deployment path, nhưng license, networking và persistent artefact vẫn phải cấu hình ([Deployment considerations](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/deployment_considerations.htm) — truy cập 2026-07-14).

### 3.3. Design, scripting, parameterization và correlation

- Workflow chuẩn là record/import API calls, tạo User Paths, Population và Scenario, rồi run/analyze; một User Path có Init/Actions/End và các container/transactions ([Get started](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/get_started.htm) và [Design User Path](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/design_user_path.htm) — truy cập 2026-07-14).
- NeoLoad as-code cho phép khai báo project/scenario/infrastructure bằng YAML/JSON và trộn với `.nlp`; điều này cải thiện diff/review so với chỉ dùng GUI binary ([Execute YAML-based projects](https://docs.tricentis.com/neoload-2026.1/en-us/content/user_guides.htm/neoload_as_code/executing_yaml_based_projects.htm) và [Project files](https://docs.tricentis.com/neoload-2024.2/en-us/content/user_guides.htm/neoload_as_code/project_files.htm) — truy cập 2026-07-14).
- JavaScript Action bổ sung logic; Variable Extractor lấy giá trị response và tái sử dụng trong request sau, phục vụ CSRF/token/session ID ([Design User Path](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/design_user_path.htm) — truy cập 2026-07-14).
- Variables hỗ trợ constant/file/CSV, unique, sequential và random policies; dynamic parameter handling/correlation có workflow tự động nhưng cần replay kiểm chứng ([Variables and functions](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/variables_and_fuctions.htm) và [Design process](https://docs.tricentis.com/neoload-latest/en-us/content/user_guides.htm/design_process/design_process.htm) — truy cập 2026-07-14).

### 3.4. Workload, phân tán và session

- Population trộn nhiều User Path theo phần trăm và có pacing/delay; phù hợp phối hợp shopper/browser/cart/checkout personas ([Create populations](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/create_populations.htm) — truy cập 2026-07-14).
- Load policies gồm Constant, Ramp-up, Peaks và Custom, cùng số iteration/duration; tài liệu được trích không chứng minh một open-arrival-rate executor tương đương trực tiếp, vì vậy arrival-rate semantics là `[CẦN XÁC MINH]` thay vì tự đồng nhất ramp VU với request rate ([Load variation policy](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/load_variation_policy.htm) — truy cập 2026-07-14).
- Controller có thể điều phối nhiều Load Generator Agent; CLI cho phép override agent/infrastructure bằng YAML/TXT và chạy local built-in agent khi không khai báo infrastructure ([Start Controller – CLI](https://docs.tricentis.com/neoload-2026.1/en-us/content/get_started/start_the_controller.htm) — truy cập 2026-07-14).

### 3.5. Validation, SLA, reporting và raw output

- Validation có thể kiểm tra duration, content length, response content, XPath và JSONPath; failure được ghi vào request/transaction result ([Validation](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/validation.htm) — truy cập 2026-07-14).
- SLA profiles đặt threshold cho request/page/transaction và quyết định test status; có thể dùng cùng CLI/JUnit output để gate ([SLA profiles](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/service_level_agreement_sla_profiles.htm) — truy cập 2026-07-14).
- Test Summary gồm request/s, average response, error rate, min/average/max, standard deviation, throughput và ba percentile cấu hình từ 0,1 đến 99,9; report cần ghi rõ percentile đã chọn ([Test summary](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/test_summary.htm) — truy cập 2026-07-14).
- `-exportRaw` xuất raw transaction results; `-report` tạo HTML/PDF/XML, còn `-SLAJUnitReport` sinh JUnit-compatible XML ([Start Controller – CLI arguments](https://docs.tricentis.com/neoload-2026.1/en-us/content/get_started/start_the_controller.htm) — truy cập 2026-07-14).

### 3.6. CLI/CI/CD, exit code, local/offline và AI

- `NeoLoadCmd` chạy headless với `-project`, `-launch`, `-noGUI`, `-report`, `-exportRaw`; exit code chính thức là `0=PASSED`, `1=FAILED` khi test chạy được nhưng SLA fail, `2=ERROR` khi không thể chạy (ví dụ thiếu license). `-exitCodeFailIgnore` có thể ép failure thành 0 nên pipeline phải cấm option này trừ khi có lý do được review ([Start Controller](https://docs.tricentis.com/neoload-2026.1/en-us/content/get_started/start_the_controller.htm) — truy cập 2026-07-14).
- Tricentis có hướng dẫn Jenkins để trigger run và publish result; API catalog chính thức bao phủ automation/integration, cho phép CI ngoài Jenkins ([Jenkins integration](https://docs.tricentis.com/neoload-latest/en-us/content/user_guides.htm/integrate_with_third_party_tools/jenkins/jenkins.htm) và [API overview](https://docs.tricentis.com/neoload-latest/en-us/content/apis/api_overview.htm) — truy cập 2026-07-14).
- Desktop Controller/Load Generator có thể chạy on-premises; tài liệu có quy trình lease/shared license offline. Tuy vậy lần cấp/lease license và tính năng NeoLoad Web/cloud vẫn tạo dependency ngoài, nên phải phân biệt “local load generation” với “hoàn toàn air-gapped” ([Manage shared licenses offline](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/manage_shared_licenses_offline.htm?Highlight=offline+lease) — truy cập 2026-07-14).
- Project có thể quản lý trong Git và backup/restore theo operations guide; reproducibility tốt nhất khi commit YAML, project, data schema và environment overrides nhưng không commit secret ([Operations guide](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/operations_guide.htm) — truy cập 2026-07-14).
- Product page hiện quảng bá Agentic Performance Testing, AI Chat/MCP, Augmented Analysis và AI-powered automation; đây là native/current product direction, nhưng availability theo plan/data residency phải xác minh ([NeoLoad product page](https://www.tricentis.com/products/performance-testing-neoload) — truy cập 2026-07-14).
- **AI-assisted potential:** cao nhờ YAML/JS/API và tính năng AI native; rủi ro gồm prompt/data leakage, model drift, suggestion không đúng session/SLA và kết quả khó tái lập. Nhóm không gọi NeoLoad AI trong nghiên cứu này; mọi script/analysis do AI đề xuất phải được human audit và đối chiếu raw result.

### 3.7. Fit, điểm mạnh/giới hạn và bảng điểm

**EShop fit:** rất cao cho journey Web/API, data, extraction, cookie/session, SLA, mix population, report và CI. **Classroom fit:** GUI dễ trình diễn nhưng annual entry price và entitlement làm khó tái lập cho toàn lớp.  
**Điểm mạnh:** GUI + as-code; validation/SLA; exit codes rõ; reporting phong phú; official container/agents; native AI.  
**Giới hạn:** giá từ 20.000 USD/năm; Free Edition run limits chưa rõ trên docs public; Java/resource footprint; arrival-rate equivalence cần xác minh; cloud/AI feature có governance cost.

| Tiêu chí | Điểm | Lý do ngắn và bằng chứng |
|---|---:|---|
| Chi phí | 2 | Giá từ 20.000 USD/năm; free/trial có nhưng entitlement chạy phải xác minh ([pricing](https://www.tricentis.com/products/performance-testing-neoload/pricing) — truy cập 2026-07-14). |
| Dễ học | 4 | GUI record/design tốt và có as-code, dù scenario/infra/license vẫn cần học ([get started](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/get_started.htm) — truy cập 2026-07-14). |
| Phù hợp EShop | 5 | User Path, population, extractor, validation, SLA bao phủ journey ([design](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/design_user_path.htm) — truy cập 2026-07-14). |
| Hành trình nhiều bước | 5 | Init/Actions/End, session/correlation/data và mix persona ([variables](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/variables_and_fuctions.htm) — truy cập 2026-07-14). |
| Mô hình tải | 4 | Constant/ramp/peaks/custom và distributed agents; open arrival semantics chưa xác nhận ([load policy](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/load_variation_policy.htm) — truy cập 2026-07-14). |
| Assertion | 5 | Content, length, duration, XPath/JSONPath và SLA ([validation](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/validation.htm) — truy cập 2026-07-14). |
| Báo cáo | 5 | Percentile cấu hình, throughput/errors, raw export và HTML/PDF/XML ([summary](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/test_summary.htm) — truy cập 2026-07-14). |
| CI/CD | 5 | Headless, JUnit, Jenkins/API và exit `0/1/2` rõ ([CLI](https://docs.tricentis.com/neoload-2026.1/en-us/content/get_started/start_the_controller.htm) — truy cập 2026-07-14). |
| Tái lập | 5 | YAML/JSON, Git, CLI variables và infra descriptors ([as-code](https://docs.tricentis.com/neoload-2026.1/en-us/content/user_guides.htm/neoload_as_code/executing_yaml_based_projects.htm) — truy cập 2026-07-14). |
| Local/offline | 4 | On-prem Controller/agents và offline license workflow; cloud features không offline ([offline license](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/manage_shared_licenses_offline.htm?Highlight=offline+lease) — truy cập 2026-07-14). |
| AI-assisted | 5 | Native AI/agentic/augmented analysis được công bố, cộng với YAML/JS dễ audit ([product](https://www.tricentis.com/products/performance-testing-neoload) — truy cập 2026-07-14). |
| Lớp học | 2 | GUI tốt nhưng giá/license/resource làm giảm khả năng mọi sinh viên tự tái lập. |

**Tổng có trọng số: 87,6/100. Phân loại: Survey-only / enterprise benchmark.**

### 3.8. Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

1. Tải đúng NeoLoad version/OS từ Tricentis, ghi checksum/Java/hardware; kích hoạt Free/trial và chụp entitlement đã che ID để biết run limit thật.
2. Tạo project `neoload-smoke`: một User Path GET `[VERIFIED_BASE_URL]/[READ_ONLY_PATH]`, validation HTTP/content marker; Population 1 user; Scenario `Smoke` constant 1 user, 1 iteration; SLA rộng nhưng xác định rõ. Export/commit YAML nếu UI cho phép.
3. Chạy headless theo cú pháp chính thức:

   ```powershell
   .\bin\NeoLoadCmd.exe -project C:\lab\neoload-smoke\neoload-smoke.nlp -launch Smoke -noGUI -report C:\lab\artifacts\neoload-smoke.html -exportRaw C:\lab\artifacts\neoload-smoke-raw.csv -SLAJUnitReport C:\lab\artifacts\neoload-smoke-junit.xml
   ```

4. **Kỳ vọng, chưa quan sát:** exit 0, validation/SLA pass, HTML/raw/JUnit được sinh. Negative run đổi content marker/SLA để kỳ vọng exit 1; run không license trong lab riêng để xác nhận exit 2 mà không gửi tải.
5. Artefact: version/license entitlement, `.nlp`/YAML, exact command/environment overrides, stdout/stderr/exit code, report/raw/JUnit. Không bật `-exitCodeFailIgnore`.

### 3.9. Phản biện dự kiến

1. **Hỏi:** “NeoLoad Free có bao nhiêu VU?”  
   **Đáp:** Nguồn current công khai xác nhận Free Edition nhưng không cho một cap đủ chắc để trích. Phải ghi `[CẦN XÁC MINH]` và chụp entitlement tài khoản, không dùng số từ bài viết cũ ([Quick Start](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/quick_start_guide.htm) — truy cập 2026-07-14).
2. **Hỏi:** “Giá cao nhưng điểm vẫn gần JMeter có thiên vị không?”  
   **Đáp:** Ma trận tách cost khỏi capability; NeoLoad mất điểm cost/classroom nhưng thắng ở SLA, CI exit, as-code và AI. Phân loại vẫn Survey-only, không phải lựa chọn mặc định.
3. **Hỏi:** “Ramp 100 VU/phút có phải 100 arrival/phút?”  
   **Đáp:** Không được đồng nhất nếu docs chưa nói vậy. VU ramp là thay đổi concurrency; request arrival còn phụ thuộc iteration/pacing/response time. Cần experiment riêng cho arrival semantics ([load policy](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/load_variation_policy.htm) — truy cập 2026-07-14).
4. **Hỏi:** “Native AI làm kết quả đáng tin hơn?”  
   **Đáp:** Không tự động. AI giảm thời gian thiết kế/phân tích; độ tin cậy vẫn đến từ script review, validation, raw result, fixed inputs và reproduction. Paid/cloud availability cũng phải xác minh ([product](https://www.tricentis.com/products/performance-testing-neoload) — truy cập 2026-07-14).

---

## 4. OpenText Professional Performance Engineering (LoadRunner Professional)

### 4.1. Tên hiện hành, loại công cụ, access/license

- Tên thương mại hiện hành là **OpenText Professional Performance Engineering**, với “LoadRunner Professional” vẫn được dùng trong ngoặc/trang tích hợp. Đây là bộ on-premises load/performance testing cho nhóm co-located, do OpenText duy trì ([product page](https://www.opentext.com/products/professional-performance-engineering) — truy cập 2026-07-14).
- Trang sản phẩm công bố hơn 180 protocol/technology, flexible deployment và analytics; danh sách hỗ trợ thực tế phải đối chiếu đúng bản 26.1 trong Supported Protocols, không suy rằng mọi protocol chạy trên mọi OS/load generator ([product page](https://www.opentext.com/products/professional-performance-engineering) và [26.1 Supported Protocols](https://admhelp.microfocus.com/documents/lre/Supported_Protocols/26.1/LR_Protocols.htm) — truy cập 2026-07-14).
- Trang trial cho phép yêu cầu dùng thử, không cần thẻ, và quảng bá full capabilities/50+ technology; duration/entitlement cụ thể cần xác nhận trong email/license cấp cho tài khoản ([free trial](https://www.opentext.com/en-gb/products/professional-performance-engineering/trial) — truy cập 2026-07-14).
- License Utility 26.1 nói Community license tự được cài và miễn phí **50 Vuser cho mọi protocol**, gồm JMeter/Gatling, ngoại trừ COM/DCOM, Templates và GUI bundles; nhu cầu vượt community hoặc bundle đặc biệt là commercial/evaluation/VUFD license ([License Utility 26.1](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/License/R_License_Utility.htm) — truy cập 2026-07-14).
- Giá commercial công khai không được tìm thấy trên trang sản phẩm đã kiểm tra; TCO ngoài 50 VU là `[CẦN BÁO GIÁ]`.

### 4.2. Kiến trúc và cài đặt

- Ba thành phần cốt lõi là **VuGen** (record/develop virtual-user scripts), **Controller** (tổ chức, điều khiển, monitor scenario) và **Analysis** (phân tích/so sánh results) ([Get started 26.1](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/WelcomeContent/c_Welcome.htm) — truy cập 2026-07-14).
- Full Professional installation/VuGen/Controller/Analysis là Windows-centric; OneLG/load generator độc lập có lựa chọn Windows hoặc Linux theo component/protocol. Cài full host yêu cầu quyền phù hợp và phải theo support matrix ([Installation/components](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Install/About-install.htm) và [VuGen install](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/LandingPages/Installation_LandingPage.htm) — truy cập 2026-07-14).
- Load generator có official Docker images cho Ubuntu, RHEL và Windows; Controller gán container bằng host/port. Dockerized LG không hỗ trợ qua firewall và một số protocol có giới hạn, nên “có Docker” không có nghĩa toàn bộ stack/controller chạy container hoặc protocol parity hoàn toàn ([Dockerized load generators](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/dockerized_load_generator.htm) — truy cập 2026-07-14).

### 4.3. VuGen scripting, protocol và EShop correlation

- VuGen ghi client-server traffic và sinh script; phần lớn recorded scripts sinh C, trong khi protocol cụ thể có thể dùng C#, VB.NET, Java hoặc JavaScript. Script thường có init/action/end, giúp tách login, business loop và logout ([About Vuser scripts](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/100050_c_vugen_overview.htm), [Editor languages](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/UI/ui_Editor.htm) — truy cập 2026-07-14).
- VuGen hỗ trợ record và HAR-based/offline generation theo protocol; script phải replay/debug trước khi đưa vào Controller ([Recording](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/tocs/103100_toc_recording.htm) — truy cập 2026-07-14).
- Parameterization dùng file/generated/custom data; Correlation Studio và automatic correlation tìm dynamic value/session token rồi thay bằng parameter ([Parameters](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/tocs/113750_toc_parameters.htm), [Correlation Studio](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/tocs/109650_toc_correlation_studio.htm), [Automatic correlation](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/Correlation/AutomaticCorrelation.htm) — truy cập 2026-07-14).
- Web text/image checks xác minh đúng page/object dưới tải; với API EShop cần thêm status/body/business check phù hợp, không chỉ transaction timing ([Text and image verification](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/c_web_text_and_image_verification.htm) — truy cập 2026-07-14).

### 4.4. Controller workload, VU, ramp và phân tán

- Manual Scenario ghép script/group, số lượng hoặc tỷ lệ Vuser, load generators và SLA; schedule có thể theo scenario hoặc group ([Manual scenarios](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_manual_scenarios.htm) và [Schedule type](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_schedule_type.htm) — truy cập 2026-07-14).
- Schedule điều khiển start/ramp, duration và stop/ramp-down; Controller có thể gán nhiều load generator on-premises hoặc cloud/container cho group ([Schedules overview](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_schedules_overview.htm) và [Add load generators](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/t_add_load_generator.htm) — truy cập 2026-07-14).
- Goal-oriented Scenario đặt mục tiêu Vuser, pages/minute, hits/second hoặc transactions/second và Controller tự thay đổi số Vuser để theo goal; đây gần throughput-goal hơn một fixed open-arrival executor, nên phải công bố thuật toán/model khi so với k6/JMeter ([Goal-oriented scenarios](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_goal_oriented_scenarios.htm) — truy cập 2026-07-14).

### 4.5. SLA, Analysis, percentile và raw results

- SLA có thể được định nghĩa trong Controller/Analysis; sau run, Analysis so sánh dữ liệu với mục tiêu và trả status succeeded/failed/APDEX ([Service level agreements](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/toc_SLAs_main.htm) và [Define SLAs](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/104800_t_define_SLAs.htm) — truy cập 2026-07-14).
- Analysis cung cấp transaction, throughput/web-resource, error và monitoring graphs, report HTML/Excel cùng raw result model; Summary Report gồm HTTP status, transaction pass/fail, APDEX và một percentile x cấu hình ([Analysis workflow](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/c_analysis_workflow.htm), [Summary Report](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/116850_ui_summary_report.htm), [Web Resource graphs](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/toc_Web_Resources_graphs.htm) — truy cập 2026-07-14).
- Transaction graphs có percentile và transactions/second; kết quả Controller được lưu trong result directory và có đường xuất JSON/InfluxDB để phân tích ngoài ([Transaction graphs](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/toc_transaction_graphs.htm) và [Results file structure](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/r_results_file_structure.htm) — truy cập 2026-07-14).
- Known Issues 26.1 cảnh báo Transaction Response Time percentile graph có thể hiển thị kết quả không chính xác trong một trường hợp đã liệt kê; vì vậy percentile quan trọng nên được cross-check với raw/export và đúng patch level ([Analysis known issues 26.1](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/tl_Analysis.htm) — truy cập 2026-07-14).

### 4.6. CLI, CI/CD, pass/fail, offline và AI

- `CLIControllerApp.exe` chạy `.lrs` hoặc XML input, có `Run`, `Collate`, `CollateAndAnalyze`, `-ResultName`, load-generator override và `-SilentMode`; chỉ một Controller instance chạy một lúc, argument case-sensitive và results có thể bị overwrite ([Run scenarios using CLI](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/scenario-run-cli.htm) — truy cập 2026-07-14).
- CLI page nói kiểm tra Microsoft error code nếu application terminate nhưng không đưa ra contract “SLA fail = exit N” tổng quát. Do đó direct CLI gate cần parse SLA/report hoặc được negative-test; không suy luận từ process exit 0 ([Run scenarios using CLI](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/scenario-run-cli.htm) — truy cập 2026-07-14).
- OpenText Application Automation Tools plugin chạy file-system LoadRunner Professional scenarios từ Jenkins, hỗ trợ freestyle/pipeline. Tích hợp chỉ nhận scenario có SLA để xác định pass/fail, và yêu cầu Professional Performance Engineering trên build node ([Jenkins integration 26.1](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_jenkins.htm) và [Jenkins plugin](https://plugins.jenkins.io/hp-application-automation-tools-plugin/) — truy cập 2026-07-14).
- Full Controller/Analysis và load generator có thể đặt trong mạng on-premises; Help Center có local-download mode. License acquisition/paid Aviator/cloud LG là các dependency riêng, vì vậy offline claim phải kèm license type và topology ([Get started – local Help](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/WelcomeContent/c_Welcome.htm) — truy cập 2026-07-14).
- VuGen 26.1 có **Aviator for Scripting**: chọn protocol, coding support, phân tích lỗi, tối ưu và tóm tắt script; Aviator là cloud-based enterprise service kết nối tới paid service, còn AI-assisted Analysis nằm trong Core Performance Engineering Analysis ([VuGen 26.1 What's New](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/WelcomeContent/c_WhatsNew.htm) — truy cập 2026-07-14).
- **AI-assisted potential:** cao nhưng không mặc định miễn phí/offline. AI có thể hỗ trợ C/JavaScript/correlation, song protocol choice và auto-correlation sai có thể tạo “script chạy nhưng sai journey”. Nghiên cứu này không gọi Aviator; output AI phải human-review, replay từng Vuser, scrub secret và đối chiếu snapshot/raw requests.

### 4.7. So sánh ngữ cảnh với JMeter

| Khía cạnh | LoadRunner Professional | JMeter | Hàm ý cho seminar |
|---|---|---|---|
| Access | Community 50 Vuser; thương mại ngoài entitlement ([license](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/License/R_License_Utility.htm) — truy cập 2026-07-14) | Apache License 2.0, không VU fee ([license](https://www.apache.org/licenses/) — truy cập 2026-07-14) | JMeter dễ cho cả lớp; LoadRunner vẫn có thể demo hợp pháp ở ≤50 VU. |
| Protocol | Hơn 180 technology và protocol chuyên biệt/legacy theo matrix ([product](https://www.opentext.com/products/professional-performance-engineering) — truy cập 2026-07-14) | HTTP/API/JDBC/JMS/TCP… mạnh nhưng không rộng bằng bundle enterprise ([JMeter](https://jmeter.apache.org/) — truy cập 2026-07-14) | EShop HTTP không tự động cần protocol breadth của LoadRunner. |
| Workflow | VuGen → Controller → Analysis, recorder/correlation/SLA/report tích hợp | GUI design + CLI + JTL/dashboard, CI gate cần lắp thêm | LoadRunner minh hoạ enterprise lifecycle; JMeter dễ tái lập trong repo. |
| Platform | Controller/VuGen/Analysis Windows-centric; LG có Win/Linux/Docker | Java đa nền tảng | Hạ tầng Windows là cost/reproducibility factor, không phải chất lượng engine. |
| AI | Native paid cloud Aviator 26.1 | Không có native AI được xác nhận | Native AI không bù được license/data-governance nếu lớp học không truy cập. |

### 4.8. Fit, điểm mạnh/giới hạn và bảng điểm

**EShop fit:** rất cao ở Web HTTP/API, session/correlation, Vuser mix, SLA và enterprise monitoring. **Classroom fit:** community 50 VU có giá trị, nhưng full Windows install, nhiều component và đường học làm lab khó hơn JMeter/k6.  
**Điểm mạnh:** protocol breadth; mature recorder/correlation; Controller scheduling/distribution; Analysis/SLA; community 50 VU; Jenkins/Docker LG; native AI.  
**Giới hạn:** Windows-heavy; commercial pricing không công khai; artefact/scenario nhiều thành phần; CLI SLA exit contract không đơn giản; known percentile issue cần cross-check; paid/cloud AI.

| Tiêu chí | Điểm | Lý do ngắn và bằng chứng |
|---|---:|---|
| Chi phí | 4 | Community 50 VU rất hữu ích, nhưng scale/bundle ngoài đó cần license thương mại ([license](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/License/R_License_Utility.htm) — truy cập 2026-07-14). |
| Dễ học | 2 | VuGen–Controller–Analysis và protocol-specific scripting tạo đường học dài ([components](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/WelcomeContent/c_Welcome.htm) — truy cập 2026-07-14). |
| Phù hợp EShop | 5 | Web/API, correlation, data, Controller và SLA đầy đủ ([correlation](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/tocs/109650_toc_correlation_studio.htm) — truy cập 2026-07-14). |
| Hành trình nhiều bước | 5 | init/action/end, parameterization, session correlation và check ([Vuser scripts](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/100050_c_vugen_overview.htm) — truy cập 2026-07-14). |
| Mô hình tải | 5 | Manual/goal-oriented, ramp/schedule, nhiều LG/cloud/container ([scenario](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_manual_scenarios.htm) — truy cập 2026-07-14). |
| Assertion | 5 | Web checks, transaction status và SLA pass/fail ([verification](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/c_web_text_and_image_verification.htm) — truy cập 2026-07-14). |
| Báo cáo | 5 | Analysis graphs/report/raw export/SLA/APDEX; known issue phải kiểm soát ([Analysis](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/c_analysis_workflow.htm) — truy cập 2026-07-14). |
| CI/CD | 4 | CLI + Jenkins/SLA tốt, nhưng build-node Windows và direct CLI exit semantics cần kiểm tra ([Jenkins](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_jenkins.htm) — truy cập 2026-07-14). |
| Tái lập | 3 | Script/scenario/template lưu được, nhưng nhiều component/license/patch/OS làm environment nặng. |
| Local/offline | 5 | Controller/Analysis/LG và help có thể on-prem/local; ghi rõ license/topology ([Get started](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/WelcomeContent/c_Welcome.htm) — truy cập 2026-07-14). |
| AI-assisted | 4 | Native Aviator scripting/analysis mạnh nhưng là paid cloud service ([What's New 26.1](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/WelcomeContent/c_WhatsNew.htm) — truy cập 2026-07-14). |
| Lớp học | 2 | 50 VU miễn phí giúp demo, nhưng Windows install và ba-component workflow khó nhân rộng. |

**Tổng có trọng số: 85,0/100. Phân loại: Backup / enterprise benchmark.**

### 4.9. Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

1. Trên Windows support-matrix compliant, cài bản 26.1 với VuGen/Controller/Analysis; ghi installer checksum, patch, OS và xác nhận Community 50-Vuser license trong License Utility.
2. VuGen tạo Web HTTP/HTML script `lr-smoke`: `web_reg_find`/text check cho marker rồi một `web_url` GET `[VERIFIED_BASE_URL]/[READ_ONLY_PATH]`; replay 1 Vuser, parameter hoá base URL, không ghi secret.
3. Controller tạo manual scenario `lr-smoke.lrs`: 1 Vuser, local LG, init → 1 iteration → end, short schedule; thêm SLA transaction rộng nhưng rõ. Chạy automation dự kiến:

   ```powershell
   .\bin\CLIControllerApp.exe -TestPath C:\lab\lr-smoke\lr-smoke.lrs -CollateAndAnalyze -ResultName C:\lab\artifacts\lr-smoke -SilentMode
   ```

4. **Kỳ vọng, chưa quan sát:** Vuser pass, check đúng, result collated, Analysis/SLA report sinh. Chạy negative copy với marker/SLA sai để quan sát SLA status, plugin/direct CLI process exit và report propagation.
5. Artefact: version/license, VuGen source/data/runtime settings, `.lrs`, SLA/schedule/LG mapping, exact command/stdout/stderr/exit code, raw result directory và HTML/Analysis report. Không tuyên bố capacity từ 1 Vuser.

### 4.10. Phản biện dự kiến

1. **Hỏi:** “LoadRunner có thật sự miễn phí không?”  
   **Đáp:** Community license 26.1 miễn phí đến 50 Vuser cho các protocol được nêu, với exclusions; scale/bundle khác vẫn commercial ([License Utility](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/License/R_License_Utility.htm) — truy cập 2026-07-14).
2. **Hỏi:** “180+ protocol có khiến nó tốt hơn JMeter cho EShop?”  
   **Đáp:** Không tự động. EShop chủ yếu HTTP/API nên access, script clarity, CI và reproducibility có thể quan trọng hơn protocol breadth; protocol chuyên biệt chỉ là lợi thế nếu hệ thống thực sự dùng chúng.
3. **Hỏi:** “Docker support nghĩa là chạy toàn bộ LoadRunner bằng container?”  
   **Đáp:** Nguồn chính thức ở đây nói về **load generator** images; Controller/VuGen/Analysis vẫn có yêu cầu riêng và Docker LG có protocol/firewall limitations ([Docker LG](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/dockerized_load_generator.htm) — truy cập 2026-07-14).
4. **Hỏi:** “Aviator có thể tự sửa mọi correlation?”  
   **Đáp:** Không. OpenText mô tả assistance/chẩn đoán/tối ưu; correctness vẫn phải được chứng minh bằng replay, request snapshot, business assertion và raw result ([VuGen What's New](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/WelcomeContent/c_WhatsNew.htm) — truy cập 2026-07-14).
5. **Hỏi:** “Percentile trong Analysis có thể dùng ngay làm ground truth?”  
   **Đáp:** Cần đúng patch/settings và cross-check raw/export vì OpenText có documented known issue cho percentile graph ([Known issues](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/tl_Analysis.htm) — truy cập 2026-07-14).

---

## 5. Loader.io

### 5.1. Loại công cụ, access và giá hiện hành

- Loader.io là dịch vụ **cloud-based web application/API load testing** dùng web UI hoặc REST API; load generator do dịch vụ vận hành, không có local runner cần cài ([Loader.io homepage](https://loader.io/) và [API v2](https://loader.io/docs/v2/) — truy cập 2026-07-14).
- Trang đăng ký nói Loader là “Beta Offering” theo Twilio Terms of Service; vì vậy governance/ToS/data handling phải được xem như SaaS bên ngoài ([Free sign-up](https://loader.io/register/signup) — truy cập 2026-07-14).
- Free plan hiện niêm yết **0 USD/tháng, 10.000 clients/test, 1 target host, test 1 phút, 2 URL/test**. Pro là **99,95 USD/tháng, 100.000 clients/test, unlimited target hosts, unlimited 10-minute tests, 10 URL/test**, kèm advanced analytics, concurrent tests, DNS verification, team/priority features; subscription theo tháng ([Loader.io pricing](https://loader.io/pricing) — truy cập 2026-07-14).

### 5.2. Platform, target verification và hệ quả local

- Người dùng cấu hình qua browser/API, nhưng trước khi test phải đăng ký và xác minh từng hostname/IP/port. HTTP verification đặt token file ở web root; DNS TXT verification chỉ có ở paid plan ([Verify target host](https://support.loader.io/article/20-verifying-an-app) và [API v2 – Target Hosts](https://loader.io/docs/v2/) — truy cập 2026-07-14).
- Loader.io nói rõ load generators được host trên AWS nên service đích **phải public**; localhost/private-only EShop không thể được test trực tiếp. Tunnel có thể phơi local service ra Internet nhưng thay đổi topology/risk và không nên dùng cho benchmark chính nếu chưa được phê duyệt ([Can I test local services?](https://support.loader.io/article/80-can-i-test-the-local-services-hosted-on-local-machine) — truy cập 2026-07-14).
- API cảnh báo IP load generator có thể thay đổi và cung cấp endpoint lấy allow-list; firewall/WAF/CDN có thể ảnh hưởng kết quả cloud run ([API v2 – Load Generators](https://loader.io/docs/v2/) — truy cập 2026-07-14).
- Không có install/container/local agent trong tài liệu chính thức đã kiểm tra; container support phía người dùng không áp dụng. Dịch vụ không chạy offline.

### 5.3. Request configuration, multi-step, data và session

- Test có chuỗi `urls`; mỗi client truy cập các URL **tuần tự**, trong khi nhiều client chạy song song. API hỗ trợ GET/POST và request options/headers/body/basic auth theo HTTP configuration ([Multiple URLs](https://support.loader.io/article/81-when-i-specify-multiple-urls-does-it-run-the-test-concurrently-for-each-url), [Creating a test](https://support.loader.io/article/15-creating-a-test) và [API v2](https://loader.io/docs/v2/) — truy cập 2026-07-14).
- Cookie từ `Set-Cookie` được gửi ở request sau trong cùng client; có thể set Cookie header thủ công ([Cookie support](https://support.loader.io/article/37-do-you-support-cookies) — truy cập 2026-07-14).
- Response Variables chỉ trích giá trị từ **response header** rồi dùng `{{var}}` ở URL/options; không có bằng chứng trong docs đã kiểm tra cho JSONPath/body extraction. Điều này giới hạn correlation khi token EShop chỉ nằm trong JSON/body ([Variables](https://support.loader.io/article/18-variables) — truy cập 2026-07-14).
- Expression syntax tạo numeric sequential/range/random data. Payload file JSON tạo classic/variable datasets và có unique splitting cho clients-per-test/per-second; payload phải nằm ở URL public, làm tăng data/privacy risk ([Expression syntax](https://support.loader.io/article/21-expression-syntax) và [Payload files](https://support.loader.io/article/17-payload-files) — truy cập 2026-07-14).
- Loader chỉ gọi URL được cung cấp; không parse HTML và không tải JavaScript/CSS/image linked resources, nên không phải real browser/page-load test ([Linked resources](https://support.loader.io/article/39-do-you-load-linked-resources-assets) — truy cập 2026-07-14).

### 5.4. Workload model

- Ba loại tải là `clients per test` (tổng client phân đều theo duration), `clients per second` (khởi tạo N client mỗi giây) và `maintain client load` (tăng từ initial đến target concurrent clients; client lặp chuỗi request) ([Test types](https://support.loader.io/article/16-test-types) và [API v2 – Create a test](https://loader.io/docs/v2/) — truy cập 2026-07-14).
- `clients per second` là start/arrival rate chứ không phải active concurrency; active clients có thể cao hơn nếu response chậm. `maintain-load` gần closed/concurrency model và lặp journey ([Test types](https://support.loader.io/article/16-test-types) — truy cập 2026-07-14).
- Dịch vụ tự phân tán trên cloud loaders; người dùng không điều khiển topology/agent placement chi tiết trong API public, và IP có thể đổi giữa các run ([API v2 – Load Generators](https://loader.io/docs/v2/) — truy cập 2026-07-14).

### 5.5. Assertion, threshold, reporting và dữ liệu thô

- `error_threshold` là tỷ lệ tối đa của HTTP status `>=400` hoặc timeout; khi chạm ngưỡng, test bị abort. Timeout mặc định 10.000 ms ([API v2 – Create test](https://loader.io/docs/v2/) và [Timeout/Error](https://support.loader.io/article/36-what-does-timeout-in-error-mean) — truy cập 2026-07-14).
- Đây không phải content/business assertion: status `<400`, kể cả redirect, được đếm success; redirect đến host chưa verify không được follow. Một HTTP 200 chứa error page vẫn có thể “pass” theo cơ chế này ([Test Results](https://support.loader.io/article/19-test-results) — truy cập 2026-07-14).
- Result UI có average/min/max response time, success/4xx/5xx/timeout/network counts, sent/received bandwidth và time/detail/bandwidth graphs; Pro thêm distribution histogram. Không thấy percentile p90/p95/p99 hay per-request raw sample export trong docs public đã kiểm tra ([Test Results](https://support.loader.io/article/19-test-results) — truy cập 2026-07-14).
- Results API trả summary gồm success/error/timeout/network, bytes, average response time, average error rate và public result URL; nó không trả histogram/raw timing trong schema công khai được trích ([API v2 – Test Results](https://loader.io/docs/v2/) — truy cập 2026-07-14).
- Support article thừa nhận error detail còn hạn chế và chủ yếu chỉ ra nhóm 4xx/5xx/timeout/network; điều tra nguyên nhân cần server logs/APM ([How do I see errors?](https://support.loader.io/article/33-how-do-i-see-what-errors-are-occurring-in-a-test) — truy cập 2026-07-14).

### 5.6. API/CI/CD, pass/fail, community và AI

- API v2 tạo/chạy/dừng test và polling result; tạo test sẽ tự khởi chạy nếu không schedule, nên CI phải có explicit approval/guard để không vô tình phát tải ([API v2](https://loader.io/docs/v2/) — truy cập 2026-07-14).
- Run webhook cho phép `POST` để khởi chạy; notify webhook callback khi hoàn tất. Help Desk cũng có Jenkins plugin/webhook article, nhưng các bài integration này cũ nên plugin compatibility hiện tại là `[CẦN XÁC MINH]` ([Webhooks](https://support.loader.io/article/23-webhook) và [Jenkins](https://support.loader.io/article/26-jenkins) — truy cập 2026-07-14).
- Không có native CLI binary hay documented process exit code trong nguồn đã kiểm tra. Pipeline cần dùng HTTP status để phát hiện API failure, polling result, rồi tự map `error_threshold`/result fields sang build status; phải negative-test logic đó.
- Documentation gồm API v2 và Help Desk, nhưng nhiều Help Desk articles có last-updated 2014–2021; trang giá/API hiện hành nên được ưu tiên, và behavior cũ phải smoke-test ([Loader.io Docs](https://support.loader.io/collection/3-loaderio-docs), [API v2](https://loader.io/docs/v2/), [pricing](https://loader.io/pricing) — truy cập 2026-07-14).
- **AI-assisted potential:** API JSON nhỏ, workload types và URL sequence dễ để AI phác thảo config/pipeline parser. Không tìm thấy native AI chính thức. AI không thể bù cho thiếu body assertion/p95/raw samples; human phải review target ownership, client math, secret, error gate và tránh tạo tải ngoài ý muốn.

### 5.7. Fit, điểm mạnh/giới hạn và bảng điểm

**EShop fit:** hợp cho public endpoint smoke/load nhanh và arrival/concurrency cơ bản. Không phù hợp làm primary tool nếu EShop chỉ chạy localhost/private, cần body-token correlation, rich business assertions, browser assets hoặc p95/p99/raw analysis.  
**Classroom fit:** signup/free tier và UI dễ; nhưng mỗi nhóm phải có target public do mình sở hữu/được phép verify, nếu không lab sẽ bị block hoặc có nguy cơ tạo tải sai đích.  
**Điểm mạnh:** zero-install; free 10.000 clients/test; transparent price; cloud scale; ba load model; API/webhook; cookie/header variable.  
**Giới hạn:** SaaS-only/public target; 1-minute/2-URL free limit; no browser assets; correlation header-only; weak assertion; no published percentiles/raw samples; old support articles; cloud topology less controlled.

| Tiêu chí | Điểm | Lý do ngắn và bằng chứng |
|---|---:|---|
| Chi phí | 3 | Free plan có quota và Pro price công khai, nhưng account + verified public host là access condition đáng kể ([pricing](https://loader.io/pricing), [verification](https://support.loader.io/article/20-verifying-an-app) — truy cập 2026-07-14). |
| Dễ học | 5 | Web UI/API đơn giản, ba bước add target–run–watch ([homepage](https://loader.io/) — truy cập 2026-07-14). |
| Phù hợp EShop | 3 | HTTP/API public được, nhưng không local/browser và assertion hạn chế ([local](https://support.loader.io/article/80-can-i-test-the-local-services-hosted-on-local-machine), [assets](https://support.loader.io/article/39-do-you-load-linked-resources-assets) — truy cập 2026-07-14). |
| Hành trình nhiều bước | 3 | URL tuần tự/cookie/header variable; Free chỉ 2 URL, không body extractor ([variables](https://support.loader.io/article/18-variables) — truy cập 2026-07-14). |
| Mô hình tải | 4 | Per-test, per-second và maintain-load/ramp; topology do SaaS quản lý ([test types](https://support.loader.io/article/16-test-types) — truy cập 2026-07-14). |
| Assertion | 2 | Error-rate/status/timeout gate, không rich content/business assertion ([API](https://loader.io/docs/v2/) — truy cập 2026-07-14). |
| Báo cáo | 3 | Avg/min/max/errors/bandwidth; Pro histogram nhưng không documented percentile/raw samples ([results](https://support.loader.io/article/19-test-results) — truy cập 2026-07-14). |
| CI/CD | 4 | API/webhooks/Jenkins path có, nhưng custom polling/gate và docs integration cũ ([webhook](https://support.loader.io/article/23-webhook) — truy cập 2026-07-14). |
| Tái lập | 3 | API JSON tái tạo config; dynamic loader IP/SaaS state/result hosting làm giảm control ([API](https://loader.io/docs/v2/) — truy cập 2026-07-14). |
| Local/offline | 1 | AWS load generators yêu cầu target public; không offline ([local FAQ](https://support.loader.io/article/80-can-i-test-the-local-services-hosted-on-local-machine) — truy cập 2026-07-14). |
| AI-assisted | 3 | JSON/API dễ hỗ trợ, nhưng không native AI và capability validation/report còn mỏng. |
| Lớp học | 4 | Free/easy UI tốt; public target verification và safe-load governance là rào cản ([verify](https://support.loader.io/article/20-verifying-an-app) — truy cập 2026-07-14). |

**Tổng có trọng số: 64,0/100. Phân loại: Backup cho cloud smoke/load ngắn.**

### 5.8. Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

1. Chỉ dùng `[AUTHORIZED_PUBLIC_HOST]` thuộc nhóm hoặc có văn bản cho phép; kiểm tra WAF/cost/rate-limit và đặt maintenance window. Đăng ký Free account, ghi plan limits; đặt verification token file ở web root (không dùng target bên thứ ba).
2. Qua UI hoặc API tạo một test `per-test`, `total=15` (minimum schema API), `duration=60`, một GET `[AUTHORIZED_PUBLIC_HOST]/[READ_ONLY_PATH]`, timeout 10.000 ms, `error_threshold=1`; Free plan cho 1 phút/2 URL ([API v2](https://loader.io/docs/v2/) và [pricing](https://loader.io/pricing) — truy cập 2026-07-14).
3. API command **minh hoạ, chưa chạy**; token chỉ lấy từ secret store, không commit:

   ```powershell
   $headers = @{ 'loaderio-auth' = $env:LOADER_IO_API_KEY }
   $body = @{
     test_type = 'per-test'; total = 15; duration = 60; timeout = 10000
     error_threshold = 1; name = 'authorized-smoke'
     urls = @(@{ url = 'https://[AUTHORIZED_PUBLIC_HOST]/[READ_ONLY_PATH]'; request_type = 'GET' })
   } | ConvertTo-Json -Depth 6
   Invoke-RestMethod -Method Post -Uri 'https://api.loader.io/v2/tests' -Headers $headers -ContentType 'application/json' -Body $body
   ```

4. **Kỳ vọng, chưa quan sát:** target verify; test hoàn tất không abort; result summary có `error=0`, `timeout_error=0`, `network_error=0`, `success>0`. Không đặt p95 criterion vì API/report public không chứng minh p95.
5. Negative validation ở window riêng: endpoint test-only trả 404 hoặc timeout có kiểm soát, xác nhận threshold abort và CI polling chuyển build fail. Artefact: plan/account limits, authorization, verification method, redacted request JSON, API HTTP responses/result JSON/public report snapshot, server logs, start/end timezone và loader IP list.

### 5.9. Phản biện dự kiến

1. **Hỏi:** “Free 10.000 clients có nghĩa an toàn bắn 10.000 vào EShop?”  
   **Đáp:** Không. Đó là entitlement tối đa, không phải safe workload. Bắt đầu 15-client smoke, cần phê duyệt/capacity hypothesis/WAF-cost guard trước khi tăng ([pricing](https://loader.io/pricing) — truy cập 2026-07-14).
2. **Hỏi:** “Có test localhost bằng Loader.io được không?”  
   **Đáp:** Không trực tiếp; official FAQ yêu cầu service public vì generators ở AWS. Tunnel thay topology và security exposure nên không phải bằng chứng tương đương local deployment ([local FAQ](https://support.loader.io/article/80-can-i-test-the-local-services-hosted-on-local-machine) — truy cập 2026-07-14).
3. **Hỏi:** “HTTP 200 có chứng minh checkout đúng?”  
   **Đáp:** Không. Loader.io error logic chủ yếu status ≥400/timeout; 200 error page vẫn có thể được đếm success. Cần server-side invariant/API verification hoặc tool có body/business assertions ([results](https://support.loader.io/article/19-test-results) — truy cập 2026-07-14).
4. **Hỏi:** “Clients per second có phải concurrent users?”  
   **Đáp:** Không. Nó là số client bắt đầu mỗi giây; active concurrency còn phụ thuộc response time. Maintain-load mới nhắm giữ/tăng concurrent client ([test types](https://support.loader.io/article/16-test-types) — truy cập 2026-07-14).
5. **Hỏi:** “Vì sao không dùng Loader.io làm công cụ chính dù setup rất nhanh?”  
   **Đáp:** Primary selection cần local EShop, multi-step correlation, assertions, p95/raw evidence và reproducibility; Loader.io thiếu hoặc hạn chế nhiều điểm đó dù rất hợp cloud smoke.

---

## Kết luận xuyên công cụ và khoảng trống cần thực nghiệm

- JMeter là lựa chọn chính hợp lý nhất cho seminar EShop nếu mục tiêu là miễn phí, local, journey sâu và artefact có thể giao nộp; NeoLoad/LoadRunner là enterprise benchmark để chỉ ra giá trị của SLA/analysis/AI/protocol breadth; Silk Performer là khảo sát chức năng doanh nghiệp; Loader.io là cloud smoke comparator.
- Không nên dùng điểm desk research để tuyên bố throughput/capacity. Năm công cụ phải chạy cùng endpoint read-only trước, sau đó cùng một journey/SLO/data window; đồng bộ clock, warm-up, client hardware/network, server telemetry và số lần lặp.
- Các khoảng trống ưu tiên: entitlement Free của NeoLoad; trial 30/45 ngày của Silk; giá commercial Silk/LoadRunner; direct CLI failure propagation của JMeter/Silk/LoadRunner; p95/raw export của Loader.io; arrival-rate semantics tương đương giữa NeoLoad/LoadRunner và k6/JMeter.
- Human review gate trước mọi run: xác nhận quyền tạo tải; target/environment; safe cap; dữ liệu test/secret; teardown; abort condition; resource/cost monitoring; raw artefact retention.

## AI Usage Declaration

- Nghiên cứu này được soạn với sự hỗ trợ của mô hình ngôn ngữ để tổ chức nội dung, chuẩn hoá ma trận tiêu chí và đề xuất kế hoạch smoke test.
- Không gọi hoặc vận hành bất kỳ tính năng AI native nào của NeoLoad, LoadRunner/Aviator, Silk Performer, JMeter hay Loader.io; không cài đặt và không chạy năm công cụ.
- Mọi nhận định có thể kiểm chứng được gắn URL chính thức và ngày truy cập; chỗ thiếu bằng chứng được đánh dấu `[CẦN XÁC MINH]`. Điểm số, phân loại, EShop fit và AI-assisted potential là đánh giá/suy luận của nhóm, không phải tuyên bố của nhà cung cấp.
- Trước khi nộp seminar, con người phải mở lại link, kiểm tra version/entitlement, audit lệnh và placeholder, xác nhận không có secret/PII, chạy smoke positive + negative theo quyền được cấp, rồi thay `DOC` bằng `EXP` **chỉ** ở những dòng có artefact tái lập thực sự.
