# Hồ sơ desk research: ApacheBench, wrk, Siege, Vegeta và Tsung

**Ngày chốt thông tin:** 2026-07-14 (Asia/Bangkok)  
**Phạm vi:** nguồn chính thức của dự án/tác giả; không dùng blog tổng hợp để làm bằng chứng.  
**Trạng thái thực nghiệm:** **chưa cài đặt, chưa chạy lệnh, chưa sinh log và chưa đo EShop trong hồ sơ này**.

## 1. Quy ước bằng chứng và cách chấm

- **[DOC]**: thông tin đọc được từ tài liệu, mã nguồn hoặc trang phát hành chính thức; mỗi dẫn chiếu ghi ngày truy cập 2026-07-14.
- **[DOC + ASSUMPTION]**: đánh giá được suy ra trực tiếp từ giao diện/tính năng mà tài liệu chính thức mô tả. Đây không phải kết quả chạy thử.
- **[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**: lệnh, cấu hình, tiêu chí hoặc artifact dự kiến phải được nhóm chạy và xác minh sau.
- **[GIẢ ĐỊNH CẦN XÁC MINH]**: giá trị phụ thuộc môi trường EShop, ví dụ URL, path, mã trạng thái hoặc marker nội dung. Hồ sơ không tự điền các giá trị này.

Điểm tổng dùng đúng công thức `Σ(điểm/5 × trọng số)`, thang 0–100. Mười hai tiêu chí và trọng số lần lượt là: Chi phí & khả năng truy cập 8%; Độ dễ học 8%; Phù hợp EShop 15%; Hành trình nhiều bước 12%; Điều khiển workload 10%; Assertion/check 8%; Reporting 8%; CI/CD 7%; Khả năng tái lập 7%; Local/offline 5%; Tiềm năng hỗ trợ bằng AI 7%; Phù hợp lớp học 5%.

### Kết luận nhanh

| Công cụ | Điểm có trọng số | Phân loại tạm thời | Vai trò hợp lý trong bài seminar |
|---|---:|---|---|
| ApacheBench | 56.0 | **Supporting benchmark tool** | Baseline rất ngắn cho một HTTP endpoint; không đại diện hành trình người dùng. |
| wrk | 58.2 | **Supporting benchmark tool** | Endpoint benchmark hiệu suất cao, có Lua để biến đổi request/quan sát response. |
| Siege | 62.2 | **Supporting benchmark tool** | Danh sách URL và cookie theo client phù hợp demo tải web tĩnh/đơn giản. |
| Vegeta | 70.2 | **Supporting benchmark tool** | Lựa chọn benchmark API theo rate mạnh nhất trong nhóm, artifact thô và report tốt. |
| Tsung | 81.0 | **Survey-only** cho phạm vi lớp học hiện tại | Có năng lực journey/correlation/distributed thực sự, nhưng chi phí học và vận hành vượt phạm vi smoke EShop cục bộ ngắn. |

**Diễn giải quan trọng.** Điểm cao đo **năng lực theo bộ tiêu chí**, không tự động quyết định công cụ chính. Tsung đạt điểm cao vì có session, dynamic data, correlation và workload theo phase; tuy nhiên thời lượng lớp học và mục tiêu EShop chạy cục bộ khiến chi phí XML/Erlang/distributed có thể lớn hơn lợi ích. Ngược lại, bốn công cụ benchmark không bị coi là “kém” vì thiếu journey: đó là **ranh giới vai trò** của công cụ chuyên benchmark endpoint. Chúng trả lời rất tốt câu hỏi “endpoint này chịu rate/concurrency và có latency ra sao”, nhưng không tự động trả lời câu hỏi “một người dùng đăng nhập–duyệt–thêm giỏ–checkout có thành công về nghiệp vụ không”. Nhận định này dựa trên các giao diện chính thức của [ApacheBench](https://httpd.apache.org/docs/current/en/programs/ab.html), [wrk](https://github.com/wg/wrk/blob/master/SCRIPTING), [Siege](https://www.joedog.org/siege/manual) và [Vegeta](https://github.com/tsenart/vegeta#usage) (đều truy cập 2026-07-14). **[DOC + ASSUMPTION]**

---

## 2. ApacheBench (`ab`)

### 2.1. Danh tính, quyền truy cập và hệ sinh thái

ApacheBench là chương trình `ab` đi cùng Apache HTTP Server, được Apache Software Foundation quản trị theo mô hình Project Management Committee và cộng đồng tình nguyện. Trang chương trình mô tả mục đích là benchmark một cài đặt HTTP server bằng cách cho biết số request mỗi giây mà server có thể phục vụ; mã nguồn HTTP Server dùng Apache License 2.0. [Tài liệu `ab`](https://httpd.apache.org/docs/current/en/programs/ab.html), [About Apache HTTP Server](https://httpd.apache.org/ABOUT_APACHE.html), [LICENSE chính thức](https://github.com/apache/httpd/blob/trunk/LICENSE) (truy cập 2026-07-14). **[DOC]**

Trang tải chính thức ghi bản HTTP Server hiện hành là 2.4.68, phát hành 2026-06-08; ASF cung cấp source distribution, còn binary Windows trên trang tải là các bản do bên thứ ba cung cấp. Vì vậy “miễn phí/mã nguồn mở” là chắc chắn, nhưng đường cài đặt Windows phải được ghi rõ là package/third-party build chứ không gán nhãn binary ASF. [Trang tải Apache HTTP Server](https://httpd.apache.org/download.cgi) (truy cập 2026-07-14). **[DOC]**

Tài liệu build HTTP Server từ source yêu cầu toolchain và các thư viện như APR/APR-util, PCRE cùng các dependency tùy cấu hình; `ab` nằm trong danh sách chương trình của HTTP Server. [Hướng dẫn compile/install](https://httpd.apache.org/docs/2.4/install.html), [danh sách chương trình](https://httpd.apache.org/docs/2.4/en/programs/) (truy cập 2026-07-14). **[DOC]**

Tài liệu chính thức đầy đủ theo từng option, còn hỗ trợ cộng đồng đi qua kênh người dùng/mailing list và tài nguyên của dự án HTTP Server. [Support](https://httpd.apache.org/userslist.html), [tài liệu `ab`](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC]**

### 2.2. Cách dùng, workload, dữ liệu và kết quả

Mẫu lệnh là `ab [options] [http[s]://]hostname[:port]/path`. Các nút điều khiển chính gồm `-n` tổng request, `-c` concurrency, `-t` giới hạn thời gian, `-k` HTTP KeepAlive, `-s` timeout, `-m` method, `-p` file POST, `-u` file PUT, `-T` content type, `-H` header, `-C` cookie và `-A` Basic Authentication. [Tài liệu `ab`](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC]**

Workload của một invocation là **một URL cuối cùng với một tập request option dùng chung**. Có thể phát lại header/cookie tĩnh và gửi body từ file, nhưng tài liệu không cung cấp VU session, danh sách step, arrival-rate stage, response extractor hay cơ chế lấy token từ response trước để đưa vào request sau. Do đó việc ghép login–browse–cart–checkout bằng nhiều lệnh shell không tạo ra session/correlation nguyên tử và không nên được trình bày như journey native. [Cú pháp và toàn bộ option chính thức](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

Kết quả console gồm document length, concurrency, elapsed time, complete/failed requests, lỗi connect/read/length/exception, non-2xx, requests/second, time/request và transfer rate. `-e` ghi CSV các percentile được chia bin 1–100%, `-g` ghi dữ liệu đo dạng TSV để đưa vào gnuplot, và `-w` xuất bảng HTML đơn giản. [Tài liệu `ab`](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC]**

`ab` phân biệt lỗi giao thức/kết nối và non-2xx trong báo cáo, nhưng danh sách option không có assertion nội dung, business check hoặc ngưỡng SLA làm build fail. CI/CD vì vậy cần wrapper kiểm tra exit code công cụ, parse output/CSV và tự áp ngưỡng; không được đồng nhất “process chạy xong” với “SLA đạt”. [Tài liệu `ab`](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

Tài liệu cũng tự nêu giới hạn: buffer tĩnh có thể gây lỗi, chương trình không triển khai đầy đủ HTTP/1.x và chính `ab` có thể trở thành bottleneck thay vì server. Những cảnh báo này bắt buộc phải xuất hiện khi diễn giải benchmark. [Mục Bugs của `ab`](https://httpd.apache.org/docs/current/en/programs/ab.html#bugs) (truy cập 2026-07-14). **[DOC]**

Sau khi đã cài binary, công cụ chạy hoàn toàn local/offline với hệ thống đích cục bộ. CLI nhỏ, cấu hình nằm ngay trong lệnh/file body nên dễ lưu vào repository. Không có tài liệu container first-party dành riêng cho `ab`; nhóm có thể tự đóng image hoặc dùng package hệ điều hành, nhưng phải ghi nguồn image và phiên bản trong evidence. [Danh sách chương trình HTTP Server](https://httpd.apache.org/docs/2.4/en/programs/), [trang tải](https://httpd.apache.org/download.cgi) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

AI có thể hỗ trợ tạo lệnh, ma trận `n/c/keep-alive`, parser CSV/console và checklist đọc lỗi. Giá trị AI bị giới hạn ở automation xung quanh công cụ: AI không thể thêm session/correlation/assertion native vào `ab`, và phải được con người kiểm tra quoting, URL, header bí mật, ý nghĩa hai biến thể “time per request” và nguy cơ generator bottleneck. [Tài liệu output/options](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 2.3. Chấm 12 tiêu chí

| Tiêu chí (trọng số) | Điểm | Bằng chứng và lý do |
|---|---:|---|
| Chi phí & truy cập (8%) | 5 | Mã nguồn mở Apache-2.0, source chính thức tải tự do. [LICENSE](https://github.com/apache/httpd/blob/trunk/LICENSE), [download](https://httpd.apache.org/download.cgi) (truy cập 2026-07-14). **[DOC]** |
| Độ dễ học (8%) | 5 | Một lệnh và ít option cốt lõi; tài liệu option trực tiếp. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC]** |
| Phù hợp EShop (15%) | 2 | Phù hợp đo endpoint HTTP đơn; không biểu diễn logic mua hàng. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Hành trình nhiều bước (12%) | 1 | Một URL/invocation, không session/extractor/correlation được tài liệu hóa. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Điều khiển workload (10%) | 2 | Có tổng request, concurrency, duration và keep-alive; không ramp/arrival phase/mix scenario. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC]** |
| Assertion/check (8%) | 1 | Có failure/non-2xx nhưng không có content assertion hay SLA threshold. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Reporting (8%) | 3 | Console khá đủ, có percentile CSV và TSV; HTML chỉ là bảng, không phải dashboard phân tích. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC]** |
| CI/CD (7%) | 2 | CLI dễ gọi nhưng performance gate phải tự parse/wrap. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Tái lập (7%) | 4 | Lệnh, version, URL và body file dễ lưu; kết quả vẫn nhạy với client bottleneck mà tài liệu cảnh báo. [Bugs](https://httpd.apache.org/docs/current/en/programs/ab.html#bugs) (truy cập 2026-07-14). **[DOC]** |
| Local/offline (5%) | 5 | Binary gọi trực tiếp server local, không phụ thuộc SaaS. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC]** |
| Hỗ trợ bằng AI (7%) | 2 | AI dễ soạn lệnh/parser nhưng không bù được mô hình một URL và thiếu check. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Phù hợp lớp học (5%) | 5 | Setup/mental model nhỏ, cho feedback nhanh khi dạy baseline endpoint; cần giảng rõ giới hạn. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |

**Tổng:** `(5/5×8)+(5/5×8)+(2/5×15)+(1/5×12)+(2/5×10)+(1/5×8)+(3/5×8)+(2/5×7)+(4/5×7)+(5/5×5)+(2/5×7)+(5/5×5) = 56.0/100`.  
**Điểm mạnh theo vai trò:** cực nhanh để có endpoint baseline; lệnh và artifact gọn; chi phí gần như bằng 0.  
**Giới hạn/ranh giới vai trò:** không phải journey runner; protocol implementation và generator bottleneck phải được kiểm soát; không có business assertion hoặc SLA gate native.  
**Phân loại:** **Supporting benchmark tool**.

### 2.4. Smoke Test Plan đầy đủ

> **[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN]** Không có output hoặc kết quả nào dưới đây đã được quan sát.

1. **Mục tiêu:** xác nhận `ab` có thể gửi một GET ổn định tới một endpoint EShop đã biết và sinh console + percentile artifact.
2. **Điều kiện tiên quyết:** nhóm xác minh `[VERIFIED_BASE_URL]`, `[VERIFIED_PRODUCT_PATH]`, `[EXPECTED_STATUS]`, TLS/proxy; endpoint không yêu cầu flow login; ghi lại CPU/RAM của máy phát và máy SUT. **[GIẢ ĐỊNH CẦN XÁC MINH]**
3. **Cài đặt/setup:** lấy `ab` từ package có provenance ghi nhận hoặc build HTTP Server theo [hướng dẫn chính thức](https://httpd.apache.org/docs/2.4/install.html) (truy cập 2026-07-14); lưu `ab -V`, nguồn binary và checksum/package version.
4. **Một request đại diện:** `GET [VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]`, không chèn sẵn endpoint giả.
5. **Lệnh mẫu:** `ab -n 20 -c 2 -e ab-percentiles.csv "[VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]"`. Cú pháp dựa trên [manual chính thức](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). Nếu cần header xác thực tĩnh, dùng secret injection của CI thay vì commit `-H "Authorization: ..."`.
6. **Kết quả mong đợi:** process hoàn tất; `Complete requests` đúng 20; không có lỗi connect/read/exception; non-2xx phù hợp `[EXPECTED_STATUS]`; file `ab-percentiles.csv` tồn tại và parse được. Đây là expectation, không phải observation.
7. **Evidence phải lưu:** command đã redaction; `ab -V`; stdout/stderr; exit code; `ab-percentiles.csv`; timestamp/timezone; commit SHA EShop; cấu hình máy; snapshot CPU/network; hash của artifact.
8. **Lỗi có thể gặp:** connection refused/DNS/TLS; URL thiếu dấu `/`; response length biến đổi bị tính failed length; giới hạn file descriptor; client CPU/network bão hòa; binary Windows không có provenance ASF; header secret bị lộ.
9. **Tiêu chí thành công:** toàn bộ evidence có mặt; request count và status đúng theo endpoint đã xác minh; không có lỗi transport; generator chưa bão hòa; người chấm có thể chạy lại cùng lệnh. Không đặt số p95/RPS pass tùy tiện trước khi có SLA/baseline được phê duyệt.

### 2.5. Câu hỏi phản biện và trả lời

1. **“Không chạy được journey thì vì sao còn dùng?”** Vì câu hỏi endpoint baseline khác câu hỏi journey. `ab` có thể nhanh chóng phát hiện biến động latency/RPS ở một route cô lập; nó chỉ không được dùng để tuyên bố checkout end-to-end thành công. [Mục đích chính thức](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
2. **“`-e` có nghĩa là đã có p95 đáng tin cậy?”** `-e` thực sự xuất percentile CSV, nhưng chất lượng kết luận còn phụ thuộc sample size, warm-up, generator saturation và cảnh báo chính `ab` có thể là bottleneck. [Options và Bugs](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC]**
3. **“HTTP 200 có chứng minh sản phẩm trả đúng không?”** Không. Báo cáo protocol/non-2xx không tương đương assertion body/nghiệp vụ; phải có kiểm tra riêng hoặc công cụ journey có assertion. [Danh sách output/options](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

---

## 3. wrk

### 3.1. Danh tính, license, cài đặt và cộng đồng

`wrk` là dự án do Will Glozer (`wg`) duy trì trên repository chính thức. Dự án dùng **Modified Apache 2.0 License, Version 2.0.1 (February 2015)**; không nên rút gọn thành Apache-2.0 thuần vì file license chính thức tự ghi qualifier này. [Repository chính thức](https://github.com/wg/wrk), [LICENSE](https://raw.githubusercontent.com/wg/wrk/master/LICENSE), [tài khoản maintainer](https://github.com/wg) (truy cập 2026-07-14). **[DOC]**

Hướng dẫn cài đặt hỗ trợ phần lớn hệ điều hành kiểu UNIX, dùng GNU make, LuaJIT và OpenSSL; repository có thể build dependency được bundle bằng `make`, BSD dùng `gmake`, và có tùy chọn liên kết dependency hệ thống. Không có tuyên bố hỗ trợ native Windows trong hướng dẫn chính thức, nên trên máy Windows của lớp cần WSL/container/VM hoặc tự port có kiểm chứng. [INSTALL](https://github.com/wg/wrk/blob/master/INSTALL) (truy cập 2026-07-14). **[DOC]**

README, `SCRIPTING` và source tree là tài liệu chính; repository không công bố GitHub Release đóng gói trên trang Releases, vì vậy phải ghi commit/tag/binary provenance thay vì giả định “latest release” từ một package không chính thức. [README](https://github.com/wg/wrk), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING), [Releases](https://github.com/wg/wrk/releases) (truy cập 2026-07-14). **[DOC]**

### 3.2. CLI, mô hình tải, Lua, session và metrics

Mẫu cơ bản `wrk -t12 -c400 -d30s http://127.0.0.1:8080/index.html`; option gồm threads `-t`, open connections `-c`, duration `-d`, script Lua `-s`, header `-H`, timeout và `--latency`. Công cụ dùng cơ chế I/O event notification như epoll/kqueue để tạo tải đáng kể trên máy đa lõi. [README chính thức](https://github.com/wg/wrk) (truy cập 2026-07-14). **[DOC]**

Đây chủ yếu là workload closed/fixed-concurrency trong một khoảng thời gian: threads vận hành số connection được yêu cầu. CLI không tài liệu hóa staged ramp, arrival-rate schedule, weighted scenarios hay distributed controller. Có thể chạy nhiều process/máy do người dùng điều phối, nhưng đó là orchestration bên ngoài chứ không phải tính năng distributed native. [CLI options trong README](https://github.com/wg/wrk#command-line-options) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

Lua cung cấp hook `setup`, `init`, `delay`, `request`, `response`, `done`; callback response nhận `status`, `headers`, `body`, còn `done` nhận summary, latency histogram và request-rate data. Mỗi thread có một Lua environment riêng. Tài liệu đồng thời cảnh báo parse response làm giảm khả năng tạo tải. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC]**

Lua có thể tạo request động, đọc body/status và đếm validation tùy biến. Tuy nhiên state được định nghĩa theo **thread**, trong khi một thread quản lý nhiều connection; API script không cung cấp một VU/session object tương ứng mỗi connection. Vì vậy lưu token/cookie theo một biến Lua của thread cho login–cart có nguy cơ trộn session khi concurrency > threads. Đây là ranh giới thiết kế quan trọng: script tốt cho request generation/response instrumentation, không tự biến `wrk` thành engine hành trình business an toàn. [Mô hình thread và callback](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

Output chuẩn gồm latency và Req/Sec với average, standard deviation, maximum, total requests, requests/sec, transfer/sec; `--latency` thêm phân bố latency. Trong `done`, script có thể lấy percentile tùy ý và duyệt histogram value/count, cùng số lỗi connect/read/write/timeout và status >399. [README](https://github.com/wg/wrk), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC]**

Không có assertion DSL hoặc threshold/SLA gate được mô tả trong CLI. Lua có thể kiểm tra và in/đếm status/body, nhưng muốn CI fail theo p95/error ratio cần quy ước script/wrapper và kiểm tra exit code do nhóm tự xây. Repository cũng không đưa ra image/container first-party như một interface phát hành; custom image phải pin source/dependency. Sau khi build, công cụ hoàn toàn local/offline. [README options](https://github.com/wg/wrk#command-line-options), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING), [INSTALL](https://github.com/wg/wrk/blob/master/INSTALL) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

AI có thể hỗ trợ draft Lua, tách config qua environment, xuất JSON/CSV tùy biến, và phân tích histogram. Review con người phải đặc biệt kiểm tra thread-state versus connection-state, cost của callback response, request formatting, secret và điều kiện exit; nếu không, script “trông giống journey” nhưng đo sai semantics. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 3.3. Chấm 12 tiêu chí

| Tiêu chí (trọng số) | Điểm | Bằng chứng và lý do |
|---|---:|---|
| Chi phí & truy cập (8%) | 5 | Source mở với license công khai. [LICENSE](https://raw.githubusercontent.com/wg/wrk/master/LICENSE) (truy cập 2026-07-14). **[DOC]** |
| Độ dễ học (8%) | 3 | CLI ngắn, nhưng build UNIX và Lua nâng độ khó khi cần customize. [INSTALL](https://github.com/wg/wrk/blob/master/INSTALL), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC]** |
| Phù hợp EShop (15%) | 2 | Tốt cho API/route cô lập, không có business journey model. [README](https://github.com/wg/wrk), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Hành trình nhiều bước (12%) | 2 | Lua thay request/đọc response nhưng state theo thread, không theo VU/connection. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Điều khiển workload (10%) | 3 | Điều khiển threads/connections/duration/delay; không có stage/rate profile native. [README options](https://github.com/wg/wrk#command-line-options) (truy cập 2026-07-14). **[DOC]** |
| Assertion/check (8%) | 2 | Lua có thể đọc status/body, nhưng không có assertion/threshold contract native. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Reporting (8%) | 3 | Console và percentile/histogram API tốt; artifact/report chuẩn hóa phải tự viết. [README](https://github.com/wg/wrk), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC]** |
| CI/CD (7%) | 2 | CLI phù hợp automation, nhưng gate và format machine-readable ổn định là trách nhiệm wrapper. [README](https://github.com/wg/wrk) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Tái lập (7%) | 4 | Lệnh/Lua có thể version-control; phải pin build/dependency và tránh client saturation. [INSTALL](https://github.com/wg/wrk/blob/master/INSTALL), [README](https://github.com/wg/wrk) (truy cập 2026-07-14). **[DOC]** |
| Local/offline (5%) | 5 | Binary standalone gọi EShop cục bộ sau khi build. [INSTALL](https://github.com/wg/wrk/blob/master/INSTALL) (truy cập 2026-07-14). **[DOC]** |
| Hỗ trợ bằng AI (7%) | 3 | AI hữu ích cho Lua/reporting, nhưng semantics state và overhead cần audit sâu. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Phù hợp lớp học (5%) | 3 | Demo CLI dễ; setup Windows và giải thích Lua/thread model tốn thời gian. [INSTALL](https://github.com/wg/wrk/blob/master/INSTALL), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |

**Tổng:** 58.2/100.  
**Điểm mạnh theo vai trò:** endpoint load generator hiệu quả, percentile/histogram khả dụng, Lua mở rộng tốt cho request-level logic.  
**Giới hạn/ranh giới vai trò:** fixed-concurrency, không có session/VU journey rõ ràng, không có SLA gate/report artifact chuẩn native; parsing response giảm load capacity.  
**Phân loại:** **Supporting benchmark tool**.

### 3.4. Smoke Test Plan đầy đủ

> **[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN]**

1. **Mục tiêu:** xác nhận binary chạy workload GET nhỏ, xuất latency distribution, quan sát status bằng reviewed Lua callback và không bão hòa client.
2. **Điều kiện tiên quyết:** `[VERIFIED_BASE_URL]`, `[VERIFIED_PRODUCT_PATH]`, `[EXPECTED_STATUS]`, network path và endpoint không cần journey; quyết định WSL/Linux/container có provenance. **[GIẢ ĐỊNH CẦN XÁC MINH]**
3. **Cài đặt/setup:** build theo [INSTALL chính thức](https://github.com/wg/wrk/blob/master/INSTALL); lưu provenance. Version-control/human-review `status_check.lua` dùng official response callback và thread aggregation; callback overhead chỉ chấp nhận ở smoke. ([SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) — truy cập 2026-07-14)
4. **Một request:** GET tới `[VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]`.
5. **Lệnh mẫu:** `wrk -t2 -c4 -d10s --latency -s status_check.lua "[VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]"`, theo [README](https://github.com/wg/wrk) và [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14).
6. **Kết quả mong đợi:** hoàn tất 10 giây, có requests/sec, latency distribution, status counters và zero socket error; chưa dự đoán metrics.
7. **Evidence:** binary/script hashes, review record, command, stdout/stderr/exit, aggregated status counters, timestamps, EShop commit và resources.
8. **Lỗi có thể gặp:** build/routing/TLS/file descriptor; client saturation; Lua aggregation sai; callback overhead; nhầm threads với VU; wrapper che failure.
9. **Tiêu chí thành công:** duration/connections đúng, `unexpected_status=0`, zero socket error, client headroom và artifacts đủ; negative status làm wrapper fail.

### 3.5. Câu hỏi phản biện và trả lời

1. **“Có Lua thì đã đủ làm login–cart–checkout chưa?”** Chưa. Lua state là per-thread trong khi thread có thể điều khiển nhiều connection; correlation token theo VU cần thiết kế riêng và rất dễ trộn session. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
2. **“RPS cao hơn có chứng minh SUT tốt hơn không?”** Không tự động. README nói `wrk` có thể tạo tải lớn, nhưng callback response làm giảm load; vẫn phải quan sát CPU/network của generator và giữ workload tương đương. [README](https://github.com/wg/wrk), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC]**
3. **“Đưa thẳng vào CI có được không?”** Có thể gọi CLI, nhưng không có performance threshold contract mặc định; nhóm phải chuẩn hóa parser, exit policy và artifact, nếu không CI xanh chỉ nghĩa là process không crash. [README options](https://github.com/wg/wrk#command-line-options) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

---

## 4. Siege

### 4.1. Danh tính, license, platform và cài đặt

Siege là dự án open-source do Jeffrey Fulmer/JoeDog duy trì. Repository chính thức khai báo GPL-3.0; README/COPYING ghi GPL và ngoại lệ cho liên kết OpenSSL. Vì vậy báo cáo phải giữ nguyên danh tính license/exception thay vì ghi chung chung “freeware”. [Repository chính thức](https://github.com/JoeDog/siege), [COPYING](https://github.com/JoeDog/siege/blob/master/COPYING), [README](https://github.com/JoeDog/siege/blob/master/README.md) (truy cập 2026-07-14). **[DOC]**

Dự án nhắm tới POSIX/UNIX. FAQ nói không có bản native Windows; Cygwin là một đường khả dĩ. Trên lớp học Windows, lựa chọn thực tế là WSL/Linux VM/container hoặc Cygwin đã kiểm chứng. [FAQ chính thức](https://www.joedog.org/siege/faq), [trang dự án](https://www.joedog.org/siege-home/) (truy cập 2026-07-14). **[DOC]**

FAQ nêu có thể cài bằng `apt-get install siege`; khi build source, HTTPS cần OpenSSL development package và gzip cần zlib development package. Repository có Dockerfile và hướng dẫn `docker build -t siege .`, nên container có đường dẫn first-party ở mức source recipe, nhưng image/tag cụ thể vẫn phải do nhóm tự build/pin. [FAQ](https://www.joedog.org/siege/faq), [README](https://github.com/JoeDog/siege/blob/master/README.md), [Dockerfile guide](https://github.com/JoeDog/siege/blob/master/Dockerfile.md) (truy cập 2026-07-14). **[DOC]**

Manual, FAQ, man pages và repository/issues là hệ tài liệu/cộng đồng chính. Manual bao quát mode, option, URL file, cấu hình và output; FAQ giải thích các giới hạn giao thức nên là nguồn bắt buộc khi diễn giải kết quả. [Manual](https://www.joedog.org/siege/manual), [FAQ](https://www.joedog.org/siege/faq), [repository](https://github.com/JoeDog/siege) (truy cập 2026-07-14). **[DOC]**

### 4.2. Workload, session, data, assertions và reporting

Siege có ba cách dùng được manual mô tả: regression, internet simulation và brute-force/benchmark. Các option trọng tâm gồm `-c` concurrent users, `-t` duration, `-r` repetitions, `-f` URL file, `-d` delay, `-i` chọn URL ngẫu nhiên, `-b` bỏ delay để benchmark, `-l` log và `-m` đánh dấu log. `siege.config` sinh `.siegerc`. [Manual chính thức](https://www.joedog.org/siege/manual) (truy cập 2026-07-14). **[DOC]**

`urls.txt` có thể chứa nhiều URL và request POST; mặc định mỗi simulated user đi qua file tuần tự, còn `-i` chọn ngẫu nhiên. Cấu hình hỗ trợ biến tĩnh dạng `$()`/`${}`. Siege hỗ trợ GET/POST, Basic authentication, header/cookie và lưu cookie theo thread; cookie có thể được persist ở `$HOME/.siege/cookies.txt`. [Manual](https://www.joedog.org/siege/manual), [FAQ](https://www.joedog.org/siege/faq), [README](https://github.com/JoeDog/siege/blob/master/README.md) (truy cập 2026-07-14). **[DOC]**

Nhiều URL tuần tự cộng cookie theo client mô phỏng được **page sequence tĩnh** tốt hơn benchmark một URL. Tuy nhiên tài liệu chính thức không mô tả response extractor, tự lấy CSRF/JWT/product ID rồi gắn vào request sau, vòng lặp theo data động hay assertion body nghiệp vụ. Biến trong config là substitution đầu vào chứ không phải correlation từ response. Vì vậy EShop login–cart–checkout có token động vượt ranh giới native của Siege; hard-code token chỉ có thể là smoke tạm thời và không nên commit secret. [Manual](https://www.joedog.org/siege/manual), [FAQ](https://www.joedog.org/siege/faq) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

Siege coi transaction thành công khi HTTP status nhỏ hơn 400 và báo transactions, availability, elapsed time, data transferred, response time trung bình, transaction rate, throughput, concurrency, successful/failed transactions. `-l` ghi một dòng aggregate kiểu CSV cho mỗi run. Bộ metric chuẩn được tài liệu hóa không có p50/p95/p99 hay time-series/raw sample per request; verbose output có thể capture để chẩn đoán nhưng không thay thế raw result schema ổn định. [Manual, mục Output và Logging](https://www.joedog.org/siege/manual) (truy cập 2026-07-14). **[DOC]**

Phân loại `<400` là protocol check, không phải business assertion. CLI không tài liệu hóa custom content assertion, SLA threshold hoặc performance-specific exit gate, nên CI phải parse log/output và áp policy riêng; cũng cần xóa/cô lập cookie file giữa run để tái lập. [Manual](https://www.joedog.org/siege/manual), [FAQ về cookies](https://www.joedog.org/siege/faq) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

FAQ ghi hỗ trợ HTTP/1.1 còn hạn chế: không pipelining, không xử lý `100 Continue`, và persistent connection không tốt/thiên về đóng connection. POST multipart cũng không được hỗ trợ. Các giới hạn này có thể làm workload khác traffic browser/app thật và phải được nêu trong Threats to Validity. [FAQ chính thức](https://www.joedog.org/siege/faq) (truy cập 2026-07-14). **[DOC]**

Sau khi cài, Siege chạy local/offline; `.siegerc`, `urls.txt`, command và log có thể version-control/archival. AI hữu ích để soạn URL file, sinh data tĩnh, chuẩn hóa parser và kiểm tra redaction; nhưng AI không được giả định dynamic correlation/assertion không tồn tại, và phải audit cookie persistence, URL encoding, POST format cùng khác biệt Windows/WSL. [Manual](https://www.joedog.org/siege/manual), [FAQ](https://www.joedog.org/siege/faq) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 4.3. Chấm 12 tiêu chí

| Tiêu chí (trọng số) | Điểm | Bằng chứng và lý do |
|---|---:|---|
| Chi phí & truy cập (8%) | 5 | GPL-3.0, source công khai. [Repository](https://github.com/JoeDog/siege), [COPYING](https://github.com/JoeDog/siege/blob/master/COPYING) (truy cập 2026-07-14). **[DOC]** |
| Độ dễ học (8%) | 4 | CLI/URL file dễ đọc; POSIX setup và `.siegerc` thêm chút ma sát. [Manual](https://www.joedog.org/siege/manual), [FAQ](https://www.joedog.org/siege/faq) (truy cập 2026-07-14). **[DOC]** |
| Phù hợp EShop (15%) | 3 | Nhiều URL, POST và cookie hữu ích cho web/API đơn giản, nhưng thiếu correlation động. [Manual](https://www.joedog.org/siege/manual), [FAQ](https://www.joedog.org/siege/faq) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Hành trình nhiều bước (12%) | 2 | Có sequence tĩnh/cookie, không có response-to-request extraction được tài liệu hóa. [Manual](https://www.joedog.org/siege/manual) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Điều khiển workload (10%) | 3 | Concurrent users, duration/repetition, delay, sequential/random và benchmark mode; không staged arrival/ramp. [Manual](https://www.joedog.org/siege/manual) (truy cập 2026-07-14). **[DOC]** |
| Assertion/check (8%) | 2 | `<400` là success; không có body/business assertion hoặc SLA threshold native. [Manual](https://www.joedog.org/siege/manual) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Reporting (8%) | 2 | Aggregate console/log hữu ích nhưng không percentile/raw schema/HTML dashboard chuẩn. [Manual](https://www.joedog.org/siege/manual) (truy cập 2026-07-14). **[DOC]** |
| CI/CD (7%) | 2 | CLI dễ gọi; gate, parser, cookie isolation và artifact policy phải tự xây. [Manual](https://www.joedog.org/siege/manual), [FAQ](https://www.joedog.org/siege/faq) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Tái lập (7%) | 4 | URL/config/log có thể pin; cookie persist và protocol limitations phải kiểm soát. [Manual](https://www.joedog.org/siege/manual), [FAQ](https://www.joedog.org/siege/faq) (truy cập 2026-07-14). **[DOC]** |
| Local/offline (5%) | 5 | Không cần SaaS; có source Dockerfile. [Dockerfile guide](https://github.com/JoeDog/siege/blob/master/Dockerfile.md) (truy cập 2026-07-14). **[DOC]** |
| Hỗ trợ bằng AI (7%) | 3 | AI soạn URL/config/parser tốt, nhưng không giải quyết correlation/assertion native. [Manual](https://www.joedog.org/siege/manual) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Phù hợp lớp học (5%) | 4 | Mental model user/URL/delay dễ demo; Windows cần WSL/container và phải giải thích giới hạn. [FAQ](https://www.joedog.org/siege/faq), [Dockerfile guide](https://github.com/JoeDog/siege/blob/master/Dockerfile.md) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |

**Tổng:** 62.2/100.  
**Điểm mạnh theo vai trò:** sequence URL tĩnh, user/delay dễ hiểu, cookie per client, Dockerfile chính thức ở source.  
**Giới hạn/ranh giới vai trò:** không correlation động/business assertion/percentile chuẩn; protocol HTTP/1.1 có giới hạn đã được chính dự án công bố; không native Windows.  
**Phân loại:** **Supporting benchmark tool**.

### 4.4. Smoke Test Plan đầy đủ

> **[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN]**

1. **Mục tiêu:** kiểm tra hai simulated clients lặp một GET EShop đơn và tạo aggregate output/log.
2. **Điều kiện tiên quyết:** xác minh `[VERIFIED_BASE_URL]`, `[VERIFIED_PRODUCT_PATH]`, `[EXPECTED_STATUS]`; cô lập `$HOME`/cookie file; chọn Linux/WSL hoặc image tự build đã pin. **[GIẢ ĐỊNH CẦN XÁC MINH]**
3. **Cài đặt/setup:** package theo [FAQ](https://www.joedog.org/siege/faq) hoặc build image theo [Dockerfile guide](https://github.com/JoeDog/siege/blob/master/Dockerfile.md) (truy cập 2026-07-14); lưu `siege --version`, package/source commit và image digest.
4. **Một request:** GET `[VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]`.
5. **Lệnh mẫu:** đặt `logfile = [ARTIFACT_PATH]` trong isolated `.siegerc`, rồi chạy `siege -l -c 2 -r 5 -b [VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]`. `-l` chỉ bật logging, không nhận path argument. ([Manual](https://www.joedog.org/siege/manual), [`siegerc.in`](https://github.com/JoeDog/siege/blob/master/doc/siegerc.in) — truy cập 2026-07-14)
6. **Kết quả mong đợi:** 10 transaction được dự kiến từ 2 clients × 5 repetitions; status theo `[EXPECTED_STATUS]`; failed transactions bằng 0 ở smoke load; đây chưa phải observation.
7. **Evidence:** version/provenance; `.siegerc` hiệu lực; command redacted; stdout/stderr; exit code; log; cookie isolation evidence; EShop commit; client/SUT resource snapshot; timestamp/timezone; artifact hashes.
8. **Lỗi có thể gặp:** không có native Windows; container-to-host routing; TLS/OpenSSL; stale cookie; status 3xx bị tính success dù sai flow; partial HTTP/1.1; file descriptor; URL/POST encoding; generator saturation.
9. **Tiêu chí thành công:** transaction count/status đã xác minh, không failure/transport error, artifacts đủ, cookie state sạch, generator còn headroom và một người khác tái chạy được. Không tự đặt p95 vì standard output không cung cấp metric đó.

### 4.5. Câu hỏi phản biện và trả lời

1. **“Có URL list và cookie thì đã đủ journey chưa?”** Chỉ đủ sequence tĩnh. Tài liệu không có response extractor/correlation cho CSRF/JWT/ID động và không có business body assertion. [Manual](https://www.joedog.org/siege/manual), [FAQ](https://www.joedog.org/siege/faq) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
2. **“`-c 100` có đúng bằng 100 người mua hàng không?”** Nó là 100 simulated concurrent clients theo mô hình Siege; không bảo đảm mỗi client thực hiện đầy đủ logic người mua hoặc có pacing/session giống production. [Manual](https://www.joedog.org/siege/manual) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
3. **“Tại sao vẫn hợp lớp học?”** Vì `concurrency + URL file + delay` trực quan và có thể demo nhanh endpoint/page sequence, miễn là giảng viên giới hạn claim ở traffic tĩnh và dùng WSL/container đã chuẩn bị trước. [Manual](https://www.joedog.org/siege/manual), [Dockerfile guide](https://github.com/JoeDog/siege/blob/master/Dockerfile.md) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

---

## 5. Vegeta

### 5.1. Danh tính, license, phát hành và cài đặt

Vegeta là HTTP load testing tool do Tomás Senart (`tsenart`) duy trì, source chính thức dùng MIT License. Bản phát hành chính thức hiện hành tại thời điểm chốt là v12.13.0, phát hành 2025-10-31. [Repository](https://github.com/tsenart/vegeta), [maintainer](https://github.com/tsenart), [LICENSE](https://github.com/tsenart/vegeta/blob/master/LICENSE), [release v12.13.0](https://github.com/tsenart/vegeta/releases/tag/v12.13.0) (truy cập 2026-07-14). **[DOC]**

README cung cấp executable đóng gói và các đường cài qua Homebrew, MacPorts, Arch Linux, FreeBSD, hoặc build source bằng `git clone`/`make vegeta`. Mọi smoke run phải lưu version, asset name và checksum/digest thay vì chỉ ghi “cài latest”. [Installation](https://github.com/tsenart/vegeta#install), [release assets](https://github.com/tsenart/vegeta/releases/tag/v12.13.0) (truy cập 2026-07-14). **[DOC]**

Repository có Dockerfile chính thức để tự build image; không suy ra rằng mọi public registry image cùng tên đều do maintainer phát hành. Sau khi có binary/image, tool chạy local/offline và không phụ thuộc SaaS. [Dockerfile](https://github.com/tsenart/vegeta/blob/master/Dockerfile), [repository](https://github.com/tsenart/vegeta) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

README chi tiết cho CLI/formats và Go package docs mô tả API/Pacer/Targeter. Repository/issues/releases tạo hệ hỗ trợ kỹ thuật; khi dùng API phải trích đúng major version v12. [README](https://github.com/tsenart/vegeta), [Go package docs](https://pkg.go.dev/github.com/tsenart/vegeta/v12/lib), [Releases](https://github.com/tsenart/vegeta/releases) (truy cập 2026-07-14). **[DOC]**

### 5.2. Command, workload, targets, session và checks

Pipeline chuẩn là `echo 'GET http://localhost/' | vegeta attack -duration=5s | tee results.bin | vegeta report`. `attack` hỗ trợ duration, rate, workers/max-workers, connections/max-connections, timeout, keepalive, redirect, HTTP/2, h2c, TLS, header, target format và Prometheus exporter. [Usage và attack](https://github.com/tsenart/vegeta#usage) (truy cập 2026-07-14). **[DOC]**

Target dùng HTTP text hoặc line-delimited JSON; JSON chứa method/URL bắt buộc, header và body base64. Nhiều target được phát round-robin bởi static targeter, nên phù hợp mix endpoint độc lập và input tĩnh version-control. [Targets](https://github.com/tsenart/vegeta#targets), [NewStaticTargeter](https://pkg.go.dev/github.com/tsenart/vegeta/v12/lib#NewStaticTargeter) (truy cập 2026-07-14). **[DOC]**

CLI mặc định là **constant request rate**; `-rate=0` kết hợp giới hạn worker có thể tạo fixed-concurrency. Thư viện Go có `ConstantPacer`, `LinearPacer`, `SinePacer` và interface `Pacer`. Vì vậy staged/ramp rõ ràng cần code/library hoặc orchestration nhiều phase, không chỉ CLI một dòng. [Attack flags](https://github.com/tsenart/vegeta#attack-command), [Pacer API](https://pkg.go.dev/github.com/tsenart/vegeta/v12/lib#Pacer) (truy cập 2026-07-14). **[DOC]**

Vegeta không mô tả cookie jar/VU session hay response extractor trong target CLI. Static targeter round-robin request độc lập, không bảo đảm request sau dùng token/ID từ response trước của cùng user. Custom Go `Targeter`/`Client` là harness mới phải được test. Đây là ranh giới endpoint/rate benchmark, không phải khuyết điểm mục tiêu thiết kế. [Targeter API](https://pkg.go.dev/github.com/tsenart/vegeta/v12/lib#Targeter), [Targets](https://github.com/tsenart/vegeta#targets) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

`report` hỗ trợ text, JSON, histogram và hdrplot. Metrics gồm latency min/mean/percentile/max, total, rate, throughput, success ratio, status, errors và bytes. Success là không lỗi và status 200–399: protocol-level, không phải business assertion. [Report](https://github.com/tsenart/vegeta#report-command), [Metrics API](https://pkg.go.dev/github.com/tsenart/vegeta/v12/lib#Metrics) (truy cập 2026-07-14). **[DOC]**

Raw result có thể giữ ở binary/gob, encode thành JSON hoặc CSV; CSV chứa timestamp, status, latency, bytes out/in, error, body, attack name, sequence, method, URL và headers. `plot` tạo HTML time-series; attack cũng có Prometheus exporter. Đây là reporting/artifact mạnh nhất trong nhóm benchmark khảo sát. [Encode](https://github.com/tsenart/vegeta#encode-command), [Plot](https://github.com/tsenart/vegeta#plot-command), [Prometheus](https://github.com/tsenart/vegeta#prometheus) (truy cập 2026-07-14). **[DOC]**

Tài liệu không cung cấp DSL assertion hay SLA threshold tự làm process fail. CI có thể giữ `results.bin`, gọi `report -type=json`, rồi dùng policy script kiểm tra p95/success/error; exit code command không nên được coi là performance gate nếu thiếu bước policy. [Commands](https://github.com/tsenart/vegeta#usage) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

README hướng dẫn distributed execution khi một máy phát chạm open files, memory, CPU hoặc network: chia target rate cho nhiều host qua SSH/pdsh rồi hợp nhất results. Đây là pattern chính thức, không phải controller/agent cluster native. Smoke EShop cục bộ chỉ cần distributed khi evidence cho thấy generator đơn là bottleneck hoặc rate mục tiêu vượt khả năng một máy. [Distributed attacks](https://github.com/tsenart/vegeta#distributed-attacks) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

AI có thể sinh target file, lệnh, parser JSON, threshold wrapper, redaction và notebook phân tích raw artifact. Audit con người phải kiểm tra base64 body, secret, rate semantics, duration, target round-robin, generator resource và policy exit; AI không được gọi nhiều target là một journey. [Targets](https://github.com/tsenart/vegeta#targets), [Attack](https://github.com/tsenart/vegeta#attack-command), [Report](https://github.com/tsenart/vegeta#report-command) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 5.3. Chấm 12 tiêu chí

| Tiêu chí (trọng số) | Điểm | Bằng chứng và lý do |
|---|---:|---|
| Chi phí & truy cập (8%) | 5 | MIT, source và releases công khai. [LICENSE](https://github.com/tsenart/vegeta/blob/master/LICENSE), [Releases](https://github.com/tsenart/vegeta/releases) (truy cập 2026-07-14). **[DOC]** |
| Độ dễ học (8%) | 4 | Pipeline CLI/target file rõ; Go API chỉ cần cho workload nâng cao. [README](https://github.com/tsenart/vegeta) (truy cập 2026-07-14). **[DOC]** |
| Phù hợp EShop (15%) | 3 | Tốt cho API endpoint/mix độc lập; thiếu business session/correlation. [Targets](https://github.com/tsenart/vegeta#targets) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Hành trình nhiều bước (12%) | 1 | Static targets round-robin, không response-to-next-request/VU session native. [Targeter API](https://pkg.go.dev/github.com/tsenart/vegeta/v12/lib#Targeter) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Điều khiển workload (10%) | 4 | CLI constant-rate/fixed workers; Go Pacers có constant/linear/sine/custom. [Attack](https://github.com/tsenart/vegeta#attack-command), [Pacer API](https://pkg.go.dev/github.com/tsenart/vegeta/v12/lib#Pacer) (truy cập 2026-07-14). **[DOC]** |
| Assertion/check (8%) | 1 | Success theo protocol 200–399; không body assertion/SLA gate native. [Report](https://github.com/tsenart/vegeta#report-command) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Reporting (8%) | 5 | JSON/text/hist/hdrplot, raw encode, HTML plot và Prometheus. [Report](https://github.com/tsenart/vegeta#report-command), [Encode](https://github.com/tsenart/vegeta#encode-command), [Plot](https://github.com/tsenart/vegeta#plot-command) (truy cập 2026-07-14). **[DOC]** |
| CI/CD (7%) | 3 | CLI/artifact phù hợp pipeline; performance gate vẫn cần policy script. [Usage](https://github.com/tsenart/vegeta#usage) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Tái lập (7%) | 5 | Binary version, target file, rate và raw result đều pin/archive được. [Releases](https://github.com/tsenart/vegeta/releases), [Encode](https://github.com/tsenart/vegeta#encode-command) (truy cập 2026-07-14). **[DOC]** |
| Local/offline (5%) | 5 | Binary/image tự build hoạt động không SaaS. [Install](https://github.com/tsenart/vegeta#install), [Dockerfile](https://github.com/tsenart/vegeta/blob/master/Dockerfile) (truy cập 2026-07-14). **[DOC]** |
| Hỗ trợ bằng AI (7%) | 4 | Target/JSON/policy dễ sinh và audit; semantics journey vẫn phải do người kiểm tra. [Targets](https://github.com/tsenart/vegeta#targets), [Report](https://github.com/tsenart/vegeta#report-command) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Phù hợp lớp học (5%) | 5 | Pipeline raw→report→plot minh họa rõ rate, latency và artifacts. [Usage](https://github.com/tsenart/vegeta#usage) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |

**Tổng:** 70.2/100.  
**Điểm mạnh theo vai trò:** rate-based API benchmark, raw artifact giàu dữ liệu, report/plot/Prometheus, tái lập và CI-friendly.  
**Giới hạn/ranh giới vai trò:** target độc lập không phải journey; không business assertion/SLA gate native; ramp giàu biểu đạt cần Go Pacer/harness; distributed là pattern shell/SSH.  
**Phân loại:** **Supporting benchmark tool** và là công cụ endpoint benchmark ưu tiên nhất trong năm công cụ này.

### 5.4. Smoke Test Plan đầy đủ

> **[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN]**

1. **Mục tiêu:** gửi GET ở rate nhỏ cố định, giữ raw binary, xuất JSON report và xác nhận artifact chain.
2. **Điều kiện tiên quyết:** xác minh `[VERIFIED_BASE_URL]`, `[VERIFIED_PRODUCT_PATH]`, `[EXPECTED_STATUS]`; pin binary/version; đồng bộ clock và quan sát resource. **[GIẢ ĐỊNH CẦN XÁC MINH]**
3. **Cài đặt/setup:** dùng asset/build theo [Install](https://github.com/tsenart/vegeta#install) và [release chính thức](https://github.com/tsenart/vegeta/releases/tag/v12.13.0) (truy cập 2026-07-14); lưu checksum, version output và provenance.
4. **Một request:** `targets.txt` chứa `GET [VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]` theo [HTTP target format](https://github.com/tsenart/vegeta#http-format) (truy cập 2026-07-14).
5. **Lệnh mẫu:** `vegeta attack -targets=targets.txt -rate=2/s -duration=10s -output=results.bin`; `vegeta report -type=json results.bin > report.json`; tùy chọn `vegeta plot results.bin > plot.html`. [Attack](https://github.com/tsenart/vegeta#attack-command), [Report](https://github.com/tsenart/vegeta#report-command), [Plot](https://github.com/tsenart/vegeta#plot-command) (truy cập 2026-07-14). Pipeline thật phải capture exit code từng bước.
6. **Kết quả mong đợi:** khoảng 20 request nếu client theo kịp 2/s × 10s; report parse được; status distribution phù hợp `[EXPECTED_STATUS]`. Không giả định latency.
7. **Evidence:** target redacted + hash; commands; version/checksum; `results.bin`, `report.json`, `plot.html`; stdout/stderr/exit code; EShop commit; timestamp/timezone; client/SUT CPU/RAM/network; policy script/version nếu dùng.
8. **Lỗi có thể gặp:** quoting/redirection; body JSON chưa base64; secret lộ trong raw; timeout/TLS; rate vượt client capacity; 3xx được tính success dù sai flow; pipe che exit code; container network/clock; report sai format/version.
9. **Tiêu chí thành công:** đủ artifact chain, report parse ổn định, request/status/error khớp contract, generator có headroom và rerun tái tạo cấu hình. Chỉ bật CI gate khi SLA/policy được review.

### 5.5. Câu hỏi phản biện và trả lời

1. **“Nhiều target có phải journey không?”** Không. Static targeter round-robin target độc lập; tài liệu không bảo đảm session/correlation response-to-next-request. [NewStaticTargeter](https://pkg.go.dev/github.com/tsenart/vegeta/v12/lib#NewStaticTargeter) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
2. **“Success ratio 100% có chứng minh checkout đúng?”** Không. Success mặc định chỉ là không lỗi và status 200–399; cần business assertion ở lớp khác. [Report](https://github.com/tsenart/vegeta#report-command) (truy cập 2026-07-14). **[DOC]**
3. **“`-rate` có giống số virtual users không?”** Không. Rate điều khiển request arrival; worker/concurrency giúp theo kịp rate. `-rate=0` có semantics đặc biệt nhưng không tạo business VU session. [Attack](https://github.com/tsenart/vegeta#attack-command) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
4. **“Khi nào mới chia tải nhiều máy?”** Khi đo được generator đơn chạm open-file, memory, CPU/network hoặc rate mục tiêu vượt một máy; đây chính là các dấu hiệu tài liệu distributed nêu. [Distributed attacks](https://github.com/tsenart/vegeta#distributed-attacks) (truy cập 2026-07-14). **[DOC]**

---

## 6. Tsung

### 6.1. Danh tính, license, phiên bản, protocol và cài đặt

Tsung là framework load test distributed, multi-protocol, repository chính thức thuộc tổ chức ProcessOne; tài liệu ghi tác giả ban đầu Nicolas Niclausse. Dự án dùng GPL v2. [Repository chính thức](https://github.com/processone/tsung), [Introduction](https://tsung.readthedocs.io/en/latest/introduction.html), [COPYING](https://github.com/processone/tsung/blob/develop/COPYING) (truy cập 2026-07-14). **[DOC]**

Source branch `develop` khai báo phiên bản 1.8.0 trong `vsn.mk`, trong khi hosted documentation tự mang nhãn 1.7.0. Vì vậy hồ sơ dùng README/source hiện hành để nhận diện protocol/version, còn manual 1.7.0 để mô tả interface đã công bố và đánh dấu rõ version skew; mọi run sau này phải pin tag/commit và đối chiếu schema/DTD của đúng binary. [`vsn.mk`](https://github.com/processone/tsung/blob/develop/vsn.mk), [trang đầu manual](https://tsung.readthedocs.io/en/latest/) (truy cập 2026-07-14). **[DOC]**

README hiện hành liệt kê HTTP, WebDAV, SOAP, PostgreSQL, MySQL, LDAP, MQTT, AMQP và Jabber/XMPP. Manual 1.7.0 còn mô tả HTTP methods GET/POST/PUT/DELETE/HEAD/OPTIONS/PATCH, automatic cookies, recorder; WebSocket RFC6455, AMQP 0.9.1 và MQTT v3.1 được gắn trạng thái experimental trong tài liệu đó. Không nên nâng các protocol/version experimental này thành bảo đảm hiện hành nếu chưa kiểm tra tag 1.8.0. [README](https://github.com/processone/tsung), [Features](https://tsung.readthedocs.io/en/latest/features.html) (truy cập 2026-07-14). **[DOC]**

Hướng dẫn cài đặt được kiểm thử trên Linux, FreeBSD, Solaris và nêu MacPorts; về nguyên tắc có thể chạy ở hệ điều hành được Erlang hỗ trợ. Dependency cốt lõi là Erlang/OTP và build tools; gnuplot, Perl 5/Template Toolkit hoặc Python/matplotlib được dùng cho một số đường sinh graph/report. Các minimum-version trong hosted manual phải hiểu trong bối cảnh manual 1.7.0, không tự coi là recommendation năm 2026. [Installation](https://tsung.readthedocs.io/en/latest/installation.html), [manual version](https://tsung.readthedocs.io/en/latest/) (truy cập 2026-07-14). **[DOC]**

Build source theo `./configure`, `make`, `make install`; chạy điển hình `tsung -f myconfig.xml start`. Distributed mode cần Erlang nodes/host resolution và SSH không mật khẩu giữa controller–clients theo hướng dẫn. Một node local có thể cấu hình `use_controller_vm='true'`, nên distributed là năng lực tùy chọn chứ không bắt buộc cho mọi test. [Installation](https://tsung.readthedocs.io/en/latest/installation.html), [Client/server configuration](https://tsung.readthedocs.io/en/latest/conf-client-server.html) (truy cập 2026-07-14). **[DOC]**

Tài liệu chính gồm manual Read the Docs, examples/source và issue tracker. Version skew 1.7.0/1.8.0 là rủi ro documentation phải ghi nhận; repository vẫn là nguồn canonical để pin code/DTD. [Documentation](https://tsung.readthedocs.io/en/latest/), [repository](https://github.com/processone/tsung) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 6.2. XML, workload, session, dữ liệu động và assertion

Cấu hình XML tách clients, servers, load phases và sessions. `load` hỗ trợ nhiều `arrivalphase`, duration, `interarrival`, `arrivalrate` và `maxnumber`; session có probability/weight, các request tuần tự, transaction và think time. Đây là mô hình staged arrival/mixed-session thực sự, mạnh hơn các benchmark CLI cố định. [Load configuration](https://tsung.readthedocs.io/en/latest/conf-load.html), [Sessions](https://tsung.readthedocs.io/en/latest/conf-sessions.html) (truy cập 2026-07-14). **[DOC]**

HTTP session tự quản lý cookie. Dynamic variables có thể đến từ file CSV theo sequential/random, regular expression, XPath, JSONPath giới hạn, header/body response, unique ID và random strings; `subst` chèn giá trị vào request sau. Cấu hình nâng cao còn có loop, `if`, `foreach`. Vì vậy Tsung có thể xây login→browse→cart→checkout với correlation thật nếu endpoint/schema EShop đã được xác minh. [Features](https://tsung.readthedocs.io/en/latest/features.html), [Advanced features](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

`match` kiểm tra response và có các action như continue, log, abort session, abort test, restart, loop hoặc dump; bộ đếm match/nomatch hỗ trợ theo dõi check. Đây là business/content assertion đáng kể, dù performance SLA threshold theo p95/error budget vẫn cần policy/reporting bên ngoài nếu không được thể hiện bằng match. [Match trong advanced features](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html#checking-the-server-s-response) (truy cập 2026-07-14). **[DOC]**

### 6.3. Metrics, raw data, report, CLI/CI và distributed scope

Tsung ghi statistics log hoặc JSON backend, theo dõi request/page/connect/session/users, response time, status, traffic và nhiều counter protocol. Standard engine tính mean/standard deviation theo cửa sổ thay vì mặc định giữ mọi sample thô; web dashboard trong lúc chạy và `tsung_stats.pl` sinh HTML/graphs sau run. Vì vậy reporting phong phú, nhưng raw per-request và các percentile cụ thể phải được kiểm chứng theo backend/fullstats của đúng phiên bản, không tự tuyên bố p50/p95/p99. [Reports](https://tsung.readthedocs.io/en/latest/reports.html) (truy cập 2026-07-14). **[DOC]**

CLI và XML phù hợp version control/automation; command chờ test hoàn tất và logs nằm trong thư mục run. Tuy nhiên CI cần boot/health-check SUT, pin DTD/version, thu artifact, parse metric và áp SLA gate riêng. `abort_test` có thể dừng theo nội dung match, nhưng không thay thế gate hiệu năng tổng hợp. [Running Tsung](https://tsung.readthedocs.io/en/latest/installation.html#running), [Reports](https://tsung.readthedocs.io/en/latest/reports.html), [Advanced features](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

Repository chính thức không trình bày Docker image như kênh phát hành cốt lõi; container hóa tùy chỉnh/third-party phải pin source và dependency, không gắn nhãn first-party nếu chưa có provenance. Local single-node vẫn chạy offline sau cài đặt, nhưng Erlang/tool report làm setup nặng hơn binary benchmark. [Repository](https://github.com/processone/tsung), [Installation](https://tsung.readthedocs.io/en/latest/installation.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

Distributed trở nên cần thiết khi một generator không đạt target load hoặc chạm CPU, memory, network, file/socket limits, hoặc khi quy mô/mô hình địa lý là mục tiêu nghiên cứu. Tsung được thiết kế để phân tải trên cluster và cấu hình nhiều client host/maxusers/weights. Với EShop chạy local và smoke lớp học nhỏ, thêm SSH, Erlang node naming/cookies, host resolution, clock/network và hợp nhất evidence tạo nhiều biến nhiễu hơn giá trị; single-node `use_controller_vm='true'` đúng phạm vi hơn. [Introduction](https://tsung.readthedocs.io/en/latest/introduction.html), [Client/server configuration](https://tsung.readthedocs.io/en/latest/conf-client-server.html), [Installation](https://tsung.readthedocs.io/en/latest/installation.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

AI có tiềm năng lớn để scaffold XML, CSV data, extractor/match, stage và parser report. Rủi ro cũng lớn: DTD/version skew, XML escaping, regex/JSONPath giới hạn, transaction naming, secret/correlation và arrival semantics phải được người có chuyên môn review; chỉ một smoke nhỏ mới xác nhận config do AI sinh tương thích binary đã pin. [Advanced features](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html), [Load configuration](https://tsung.readthedocs.io/en/latest/conf-load.html), [manual version](https://tsung.readthedocs.io/en/latest/) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 6.4. Chấm 12 tiêu chí

| Tiêu chí (trọng số) | Điểm | Bằng chứng và lý do |
|---|---:|---|
| Chi phí & truy cập (8%) | 5 | GPLv2, source công khai. [Introduction](https://tsung.readthedocs.io/en/latest/introduction.html), [COPYING](https://github.com/processone/tsung/blob/develop/COPYING) (truy cập 2026-07-14). **[DOC]** |
| Độ dễ học (8%) | 2 | XML/DTD, Erlang, report dependencies và distributed concepts tạo learning curve cao. [Installation](https://tsung.readthedocs.io/en/latest/installation.html), [Configuration](https://tsung.readthedocs.io/en/latest/configuration.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Phù hợp EShop (15%) | 5 | HTTP session, cookie, dynamic data/correlation/match phù hợp flow thương mại điện tử. [Features](https://tsung.readthedocs.io/en/latest/features.html), [Advanced features](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html) (truy cập 2026-07-14). **[DOC]** |
| Hành trình nhiều bước (12%) | 5 | Session tuần tự, transaction, think time, loop/if/foreach và extraction. [Sessions](https://tsung.readthedocs.io/en/latest/conf-sessions.html), [Advanced features](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html) (truy cập 2026-07-14). **[DOC]** |
| Điều khiển workload (10%) | 5 | Arrival phases/rates/interarrival/max users, session mix và distributed clients. [Load](https://tsung.readthedocs.io/en/latest/conf-load.html), [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html) (truy cập 2026-07-14). **[DOC]** |
| Assertion/check (8%) | 4 | Response match có nhiều action và counters; aggregate performance SLA gate vẫn cần lớp ngoài. [Advanced features](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html#checking-the-server-s-response) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Reporting (8%) | 4 | Stats/JSON, live web và HTML graphs tốt; raw samples/percentile của đúng version cần kiểm chứng. [Reports](https://tsung.readthedocs.io/en/latest/reports.html) (truy cập 2026-07-14). **[DOC]** |
| CI/CD (7%) | 3 | CLI/XML Git-friendly; setup/report/gate và distributed lifecycle phức tạp. [Installation](https://tsung.readthedocs.io/en/latest/installation.html), [Reports](https://tsung.readthedocs.io/en/latest/reports.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Tái lập (7%) | 4 | XML/data/source pin được; DTD/version skew, node/network và randomness cần khóa. [`vsn.mk`](https://github.com/processone/tsung/blob/develop/vsn.mk), [manual](https://tsung.readthedocs.io/en/latest/) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Local/offline (5%) | 4 | Có single-node local/offline, nhưng Erlang/report dependencies nặng hơn binary đơn. [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html), [Installation](https://tsung.readthedocs.io/en/latest/installation.html) (truy cập 2026-07-14). **[DOC]** |
| Hỗ trợ bằng AI (7%) | 3 | AI hữu ích cho XML/extractor nhưng DTD/correlation/escaping cần audit và smoke. [Advanced features](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |
| Phù hợp lớp học (5%) | 2 | Năng lực minh họa cao nhưng setup/learning curve không hợp slot ngắn nếu chưa chuẩn bị image/lab. [Installation](https://tsung.readthedocs.io/en/latest/installation.html), [Configuration](https://tsung.readthedocs.io/en/latest/configuration.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]** |

**Tổng:** 81.0/100.  
**Điểm mạnh:** session/correlation/assertion, workload phase/mix, protocol breadth, scale-out thật, dashboard/HTML.  
**Giới hạn:** XML/Erlang và distributed operations khó học; hosted docs lệch version source; raw percentile/gate cần xác minh/automation thêm.  
**Phân loại:** **Survey-only** cho bài EShop local hiện tại; có thể là shortlist cho dự án dài ngày cần journey + distributed scale.

### 6.5. Smoke Test Plan đầy đủ

> **[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN]** Cấu hình dưới đây là skeleton, chưa được validate bằng binary/DTD.

1. **Mục tiêu:** xác nhận single-node Tsung đọc XML, gửi một HTTP GET nhỏ và sinh log/report, không kích hoạt distributed cluster.
2. **Điều kiện tiên quyết:** xác minh `[VERIFIED_HOST]`, `[VERIFIED_PORT]`, `[VERIFIED_PRODUCT_PATH]` và protocol/TLS; pin tag/commit + DTD đúng version; cài Erlang và report dependencies. **[GIẢ ĐỊNH CẦN XÁC MINH]**
3. **Cài đặt/setup:** build/cài theo [Installation](https://tsung.readthedocs.io/en/latest/installation.html) (truy cập 2026-07-14); lưu `tsung -v`, Erlang/OTP version, source commit và dependency versions.
4. **Một request:** GET `[VERIFIED_PRODUCT_PATH]` tới server đã xác minh. Base skeleton chưa có body match; chỉ thêm match đã review sau khi pin binary/DTD và stable marker.
5. **Cấu hình/lệnh mẫu:** tạo `smoke.xml` theo skeleton sau, validate với DTD của binary rồi chạy `tsung -f smoke.xml -l ./tsung-logs start`; sau run, vào `[GENERATED_LOG_DIR]` và chạy `tsung_stats.pl`. Cú pháp dựa trên [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html), [Load](https://tsung.readthedocs.io/en/latest/conf-load.html), [Sessions](https://tsung.readthedocs.io/en/latest/conf-sessions.html) và [Reports](https://tsung.readthedocs.io/en/latest/reports.html) (truy cập 2026-07-14).

```xml
<?xml version='1.0'?>
<!DOCTYPE tsung SYSTEM '/path/to/pinned/tsung-1.0.dtd'>
<tsung loglevel='notice' version='1.0'>
  <clients><client host='localhost' use_controller_vm='true'/></clients>
  <servers><server host='[VERIFIED_HOST]' port='[VERIFIED_PORT]' type='tcp'/></servers>
  <load><arrivalphase phase='1' duration='10' unit='second'>
    <users interarrival='1' unit='second'/>
  </arrivalphase></load>
  <sessions><session name='smoke' probability='100' type='ts_http'>
    <request><http url='[VERIFIED_PRODUCT_PATH]' method='GET' version='1.1'/></request>
  </session></sessions>
</tsung>
```

6. **Kết quả mong đợi:** XML/DTD hợp lệ, node local start/stop sạch, request/transport đúng contract, thư mục log và report sinh được. Base smoke chưa claim body match; không dự đoán RPS/latency.
7. **Evidence:** XML + hash; DTD/source commit; Tsung/Erlang versions; exact command; stdout/stderr/exit code; run log/JSON/HTML; EShop commit; timestamp/timezone; client/SUT resources; redaction chứng minh không lộ secret.
8. **Lỗi có thể gặp:** XML/DTD mismatch; hostname/Erlang node/cookie; port/TLS type; dependency report thiếu; path log; placeholder chưa thay; match/regex/escaping sai; generator/SUT clock; vô tình cấu hình remote client/SSH; log chứa token.
9. **Tiêu chí thành công:** single-node hoàn tất, request/transport đúng, không Erlang/transport error, log/report đầy đủ và rerun được. Chỉ claim body match nếu XML thật có match, pinned validation và negative control. Chưa bật distributed/SLA gate.

### 6.6. Câu hỏi phản biện và trả lời

1. **“Điểm 81 cao nhất, sao chỉ Survey-only?”** Điểm phản ánh năng lực; quyết định còn chịu timebox/risk. Journey/distributed mạnh nhưng XML/Erlang/report setup và version skew làm demo local ngắn có rủi ro cao. [Installation](https://tsung.readthedocs.io/en/latest/installation.html), [manual](https://tsung.readthedocs.io/en/latest/) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
2. **“Khi nào distributed thực sự cần?”** Khi một generator không đạt load hoặc bão hòa tài nguyên, hoặc nghiên cứu yêu cầu scale/geography. Local smoke có client trên controller VM và không cần SSH cluster. [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html), [Introduction](https://tsung.readthedocs.io/en/latest/introduction.html) (truy cập 2026-07-14). **[DOC]**
3. **“Vì sao không gắn tiền tố của ASF?”** Repository, license và docs chính thức thuộc dự án Tsung/ProcessOne, không có bằng chứng dự án thuộc ASF. Tên chính xác trong hồ sơ là **Tsung**. [Repository](https://github.com/processone/tsung), [Introduction](https://tsung.readthedocs.io/en/latest/introduction.html) (truy cập 2026-07-14). **[DOC]**
4. **“XML có làm giảm khả năng tái lập không?”** XML/data rất dễ version-control; rủi ro đến từ DTD/version, randomness, node/network và dependency không pin, chứ không phải cú pháp XML tự thân. [`vsn.mk`](https://github.com/processone/tsung/blob/develop/vsn.mk), [Configuration](https://tsung.readthedocs.io/en/latest/configuration.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

---

## 7. Khuyến nghị sử dụng trong EShop và lớp học

1. **Nếu cần một benchmark phụ có artifact tốt:** ưu tiên Vegeta cho một hoặc vài API endpoint độc lập; lưu `results.bin` + JSON + HTML plot. Đây là recommendation từ scoring và feature docs, chưa được EXP xác nhận trên EShop. [Usage](https://github.com/tsenart/vegeta#usage), [Encode](https://github.com/tsenart/vegeta#encode-command) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
2. **Nếu chỉ cần baseline tối giản:** ApacheBench có time-to-first-result thấp nhất; `wrk` phù hợp khi cần endpoint load cao và có người review Lua; Siege phù hợp bài giảng trực quan về client/delay/URL list. Các lựa chọn này phải giới hạn claim ở endpoint/page sequence tĩnh. [ApacheBench](https://httpd.apache.org/docs/current/en/programs/ab.html), [wrk](https://github.com/wg/wrk), [Siege](https://www.joedog.org/siege/manual) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
3. **Nếu nghiên cứu dài ngày cần journey và scale-out:** Tsung xứng đáng một spike riêng vì có session, correlation, match và distributed clients. Không nên đưa distributed cluster vào smoke EShop local khi chưa chứng minh generator bottleneck. [Advanced features](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html), [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
4. **Không trộn semantics:** concurrency, connection, worker, arrival rate và simulated user không phải các đại lượng hoán đổi. Một so sánh công bằng phải ghi model, warm-up, duration, keep-alive, target mix, machine/network, sample count, status/check contract và generator headroom. Các interface khác nhau được mô tả trong [ApacheBench](https://httpd.apache.org/docs/current/en/programs/ab.html), [wrk](https://github.com/wg/wrk#command-line-options), [Siege](https://www.joedog.org/siege/manual), [Vegeta](https://github.com/tsenart/vegeta#attack-command) và [Tsung load configuration](https://tsung.readthedocs.io/en/latest/conf-load.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### Thứ tự smoke đề xuất

`Vegeta → ApacheBench → Siege → wrk → Tsung single-node`. Thứ tự này tối ưu giá trị evidence sớm và tăng dần setup risk; nó **không** phải bảng xếp hạng năng lực tuyệt đối. Mỗi smoke chỉ bắt đầu sau khi endpoint contract được xác minh, và mọi kết quả sau này phải chuyển tag từ **[KẾ HOẠCH]** sang **[EXP]** kèm raw artifacts thực tế.

## 8. AI Usage Declaration

AI (Codex, họ mô hình GPT-5) đã được dùng để: cấu trúc desk research; đối chiếu và tóm tắt nguồn chính thức; xây ma trận điểm có trọng số; đề xuất lệnh/cấu hình smoke **chưa chạy**; và soạn câu hỏi phản biện. AI **không cài công cụ, không chạy tải, không quan sát EShop, không tạo log và không cung cấp số đo thực nghiệm** trong hồ sơ này.

Người thực hiện phải tự kiểm tra lại URL, license, tag/commit, DTD, option, platform, endpoint EShop, secret handling, command quoting và mọi nhận định trước khi nộp; sau đó chạy smoke trong môi trường được phép, lưu raw evidence và công bố sai khác. Đặc biệt, các nhận định **[DOC + ASSUMPTION]** và toàn bộ **[KẾ HOẠCH – CHƯA THỰC NGHIỆM]** không được đổi nhãn thành kết quả.

> **[NHÓM CẦN TÙY CHỈNH TRƯỚC KHI NỘP]** Ghi chính xác công cụ AI/model/version nếu biết, prompt hoặc loại tác vụ đã giao, thành viên đã review, những claim/command đã sửa, các nguồn đã mở lại, và artifact thực nghiệm thật. Tuyên bố này là scaffold minh bạch, không thay thế disclosure do nhóm tự xác nhận theo chính sách môn học.
