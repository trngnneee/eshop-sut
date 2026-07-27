# Khảo sát 15 công cụ Performance Testing cho EShop — Seminar T05

> **Trạng thái tài liệu:** Bản Desk Research; nguồn công cụ được truy cập ngày **2026-07-14**, source SUT được kiểm tra ngày **2026-07-15**.  
> **Evidence level tổng quát:** `[CHỈ KẾT LUẬN TỪ DESK RESEARCH]`.  
> **Cảnh báo:** Nhóm chưa cung cấp log cài đặt, log thực thi, raw result, metrics hoặc screenshot. Mọi nội dung Smoke Test và EShop Fit Test trong tài liệu này là kế hoạch, không phải kết quả. Không dùng điểm số provisional như bằng chứng rằng một công cụ đã chạy thành công trên EShop.

## Phạm vi và kết luận điều hành

Tài liệu khảo sát 15 công cụ theo cùng 12 tiêu chí, sau đó áp dụng điều kiện sàng lọc theo phạm vi Seminar T05. Việc chấm điểm nhằm hỗ trợ quyết định trong bối cảnh **EShop local, thời gian học và classroom activity tối đa 25 phút, Reproducibility, cùng yêu cầu ghép một cách tiếp cận traditional với một cách tiếp cận AI-augmented**; điểm số không phải xếp hạng chất lượng tuyệt đối của sản phẩm.

Kết luận chọn Apache JMeter và k6 trong tài liệu là **provisional** cho đến khi hai công cụ này và ít nhất một ứng viên đối chứng hoàn tất cùng Smoke Test và EShop Fit Test. Các công cụ thương mại hoặc cloud không được hạ điểm chỉ vì nhóm chưa cài; mức access, local/offline và Reproducibility chỉ được đánh giá từ điều khoản/tài liệu chính thức, đồng thời giới hạn evidence được ghi rõ.

---

# 5. System Under Test và phạm vi kiểm thử

> **Evidence status:** `[DOC — SOURCE CODE INSPECTION]`. Nội dung dưới đây được đối chiếu trên branch `seminar`, commit `609b6e6821cd3241363d0087d859576674d47e1b`, ngày 2026-07-15. Việc đọc source xác nhận cấu trúc, route và cấu hình mặc định; nó **không** chứng minh service đã khởi động hoặc endpoint đã trả response thành công. Tại thời điểm kiểm tra, các port `3000`, `5173` và `5174` đều không lắng nghe.

## 5.1. Mô tả SUT

| Thành phần | Thông tin đã xác minh | Evidence và giới hạn |
|---|---|---|
| Repository | [trngnneee/eshop-sut](https://github.com/trngnneee/eshop-sut), branch `seminar`, commit `609b6e6821cd3241363d0087d859576674d47e1b` | `git remote -v`, `git rev-parse HEAD`; snapshot local ngày 2026-07-15. |
| Frontend khách hàng | React `^19.2.6`, React Router `^7.15.0`, Vite `^8.0.12`; source tại `frontend-web/` | [package.json](../../frontend-web/package.json), [App routes](../../frontend-web/src/App.jsx). Vite config không override port; `http://localhost:5173` là URL dev dự kiến và phải xác nhận bằng log `npm run dev`. |
| Frontend quản trị | React `^19.2.6` + Vite `^8.0.12`; port `5174` với `strictPort: true` | [package.json](../../frontend-admin/package.json), [vite.config.js](../../frontend-admin/vite.config.js). Chưa khởi động trong lần kiểm tra này. |
| Frontend mobile | Expo `~54.0.33`, React Native `0.81.5`; source tại `frontend-mobile/` | [package.json](../../frontend-mobile/package.json). `App.js` đang hard-code một IP LAN cũ; phải chuyển thành biến môi trường/IP hiện tại trước khi dùng, không coi IP đó là Base URL portable. |
| Backend | Node.js CommonJS; `engines.node: 20.x`; Express `^5.2.1`; JSON REST API; JWT Bearer authentication; port mặc định `3000` | [backend/package.json](../../backend/package.json), [backend/server.js](../../backend/server.js). Máy hiện có Node `v24.10.0`, khác major version đã khai báo; cần dùng Node 20.x hoặc ghi evidence compatibility trước khi test. |
| Database | **SQLite**, package `sqlite3 ^6.0.1`, file `backend/database.sqlite` | [backend/database.js](../../backend/database.js). Đây **không phải PostgreSQL**. File snapshot hiện tại là `36,864` byte (`36 KiB`); kích thước sau chạy phải đo lại. Initializer xóa và seed lại các bảng mỗi lần backend khởi động. |
| API Base URL | `http://localhost:3000` | Được định nghĩa bởi backend port mặc định và `frontend-web/src/config.js`; chưa có reverse proxy nào trong repository để biến `http://localhost` thành URL hoàn chỉnh. |
| Web/Admin URL | Web dự kiến `http://localhost:5173`; Admin `http://localhost:5174` | Admin port được cấu hình trực tiếp; web port phải xác nhận từ Vite startup log. Hai URL này chỉ dùng cho UI, còn JMeter/k6 protocol tests nên target API `:3000`. |
| Môi trường | **Local source workspace** trên Windows; staging chưa có evidence | Không có Dockerfile/Compose hoặc staging deployment config trong snapshot đã kiểm. Service status ngày 2026-07-15: `3000`, `5173`, `5174` đều `NOT_LISTENING`. |

**Sai lệch đã sửa so với thông tin ban đầu:** repository hiện dùng SQLite, không dùng PostgreSQL. Nếu nhóm có một branch/deployment staging dùng PostgreSQL thì phải cung cấp commit hoặc deployment evidence riêng; không được gán cấu hình staging đó cho snapshot local này.

## 5.2. Business flows đã đối chiếu với source

| Business flow | UI route | API thật | Auth và request data | Ghi chú kiểm thử |
|---|---|---|---|---|
| Product Listing | `/` | `GET /api/products` | Public; không có request body | Read-only, phù hợp làm smoke đầu tiên. Response dự kiến là JSON array nhưng vẫn phải xác nhận khi service chạy. |
| Product Search | `/` | `GET /api/products?search={query}` | Public; query parameter `search` | Chỉ dùng chuỗi tìm kiếm benign, URL-encoded và có allow-list. Source ghép search string vào SQL nên security testing/fuzzing không được trộn với baseline performance run. |
| Product Detail | `/product/:id` | `GET /api/products/:id` | Public; `id` phải lấy từ Product Listing hoặc seed data đã xác minh | Read-only. Không hard-code ID trước khi kiểm tra dataset của lần chạy. |
| Login | `/login` | `POST /api/login` | JSON gồm `email`, `password`; response thành công trả JWT `token`; các request sau dùng `Authorization: Bearer [JWT_FROM_LOGIN]` | Dùng test account riêng cho từng VU hoặc partition rõ ràng. Không commit password/token vào `.jmx`, script k6, log hoặc report. |
| Add to Cart | `/cart` | Backend có `POST /api/cart` và `GET /api/cart` | JWT bắt buộc; POST body tối thiểu cần product `id` và `quantity` đã xác minh | **Khác biệt cần lưu ý:** web frontend hiện giữ cart trong React `CartContext` và không gọi API cart. Nếu test trực tiếp `/api/cart`, phải ghi đây là API journey, không tuyên bố nó tái hiện đúng network flow của web UI hiện tại. |
| Checkout | `/checkout` | `POST /api/checkout` | JWT bắt buộc; frontend gửi `items`, `total_amount`, `shipping_address`; backend hiện chỉ đọc `total_amount` và `shipping_address` | Đây là write flow tạo row trong `orders`. Chỉ chạy bằng test account/data riêng, tải thấp ban đầu, có snapshot/cleanup và không restart backend giữa run. |

Nguồn route và payload: [backend/server.js](../../backend/server.js), [frontend web routes](../../frontend-web/src/App.jsx), [CartContext](../../frontend-web/src/context/CartContext.jsx), [Checkout.jsx](../../frontend-web/src/pages/Checkout.jsx) và [API config](../../frontend-web/src/config.js).

Request skeleton dùng để audit script, **không chứa credential thật**:

```http
POST http://localhost:3000/api/login
Content-Type: application/json

{"email":"[VERIFIED_TEST_EMAIL]","password":"[SECRET_FROM_ENV]"}
```

```http
POST http://localhost:3000/api/cart
Authorization: Bearer [JWT_FROM_LOGIN]
Content-Type: application/json

{"id":[VERIFIED_PRODUCT_ID],"quantity":1}
```

```http
POST http://localhost:3000/api/checkout
Authorization: Bearer [JWT_FROM_LOGIN]
Content-Type: application/json

{"items":[{"id":[VERIFIED_PRODUCT_ID],"quantity":1}],"total_amount":[COMPUTED_CART_TOTAL],"shipping_address":"[TEST_ADDRESS]"}
```

Các skeleton trên chỉ mô tả contract đọc từ source. Trước khi biến thành test script, nhóm phải chạy một functional contract check tải tối thiểu, xác nhận status/body thực tế và redaction của token/password.

## 5.3. In Scope

- Response time và p50/p95/p99 của các API đã xác minh: Product Listing, Search, Detail, Login, API Cart và Checkout.
- Throughput, request count, iteration count và error rate theo cùng một success contract; không coi mọi HTTP response là thành công nếu status/body sai.
- Concurrent workload và hành vi dưới baseline, load, spike và stress sau khi positive smoke, negative control và stop conditions đã đạt.
- JWT authentication, token correlation và dữ liệu test tách theo VU đối với Login, Cart và Checkout.
- So sánh JMeter và k6 trên cùng commit SUT, dataset, business steps, pacing, workload shape, duration, success criteria và generator/SUT monitoring.
- Theo dõi CPU, RAM và process của backend/load generator để phát hiện generator bottleneck hoặc contention do chạy cùng máy.

## 5.4. Out of Scope

- Kết luận về năng lực production, SLA production hoặc capacity planning chính thức từ kết quả local.
- Browser rendering, Core Web Vitals và frontend JavaScript execution; JMeter/k6 ở đây được dùng ở protocol/API layer.
- Third-party image, payment hoặc email service không do nhóm kiểm soát.
- Mobile network/device performance.
- Distributed load generation nếu nhóm không triển khai và lưu topology evidence.
- Admin CRUD/import/delete endpoints, password reset và destructive/security fuzzing trong cùng performance run; chỉ đưa vào một test plan cô lập nếu có phê duyệt và cleanup riêng.
- So sánh hai tool khi chúng không dùng cùng workload contract hoặc khi load generator đã bão hòa.

## 5.5. Test Environment

| Thuộc tính | Giá trị đã kiểm tra ngày 2026-07-15 | Trạng thái/việc còn làm |
|---|---|---|
| SUT commit | `609b6e6821cd3241363d0087d859576674d47e1b` trên branch `seminar` | Pin commit này trong mọi evidence bundle; nếu đổi commit phải ghi lại. |
| Máy chạy SUT | Windows 11 Home 64-bit, version `10.0.26200` build `26200`; Intel Core i7-1260P, 12 cores/16 logical processors; RAM `15.72 GiB` | Thông số host đã đọc từ Windows. Chưa có SUT runtime metrics vì service chưa chạy. |
| Máy phát tải | **Dự kiến cùng máy với SUT**, cùng thông số trên | Đây là hạn chế lớn: phải monitor cả generator và SUT; không suy rộng kết quả thành capacity production. Nếu chuyển sang máy khác, thay dòng này bằng thông số thật. |
| Backend runtime | Source yêu cầu Node `20.x`; máy hiện có Node `v24.10.0`, npm `11.6.1` | **Version mismatch.** Khuyến nghị dùng Node 20.x đã pin trước test hoặc lưu log chứng minh Node 24 tương thích. |
| JMeter version | `NOT_FOUND` trên `PATH`; chưa cài hoặc chưa expose command | Sau khi cài, lưu output thật của `jmeter --version`, package/checksum và đường dẫn binary. |
| Java version | Eclipse Temurin OpenJDK `25.0.2+10-LTS`, 64-bit | Đây chỉ là runtime hiện có; phải xác nhận với JMeter version được chọn bằng smoke test. |
| k6 version | `NOT_FOUND` trên `PATH`; chưa cài hoặc chưa expose command | Sau khi cài, lưu output thật của `k6 version`, package/checksum hoặc image digest. |
| Docker | Docker client `29.2.1` có trên máy; Docker Desktop Linux daemon không chạy | Repository không có Compose/Dockerfile; không ghi Docker là execution environment nếu chưa tạo và review cấu hình. |
| Network | Planned local loopback: API `localhost:3000`, web `localhost:5173`, admin `localhost:5174` | Các port đều không lắng nghe tại thời điểm kiểm tra. Nếu tách load generator, ghi LAN topology, IP, latency nền và firewall/proxy. |
| Database | SQLite file `backend/database.sqlite`, snapshot `36 KiB` | `database.js` drop/re-seed khi backend start; phải copy/restore dataset kiểm soát và đo lại file size/row counts trước–sau từng run. |
| Monitoring | Chưa có Prometheus/Grafana hoặc monitoring config trong repository | Tối thiểu dùng Windows Task Manager/Resource Monitor hoặc Performance Monitor cho Node/SUT và load generator; lưu timestamped CPU/RAM/network evidence. `docker stats` chỉ dùng nếu SUT thật sự chạy trong container. |
| Service status | API, web và admin đều `NOT_LISTENING` trong lần kiểm tra | Không tuyên bố environment ready cho tới khi có startup log, functional contract check và positive/negative smoke evidence. |

**Environment gate trước khi chạy tải:** pin Node/tool versions; khởi động SUT; xác nhận ba URL cần dùng; chụp dataset snapshot; tạo test accounts riêng; chạy một request positive và một negative assertion; sau đó mới tăng workload. Do initializer xóa dữ liệu khi backend khởi động, không restart backend giữa các lần đo cần so sánh nếu chưa khôi phục cùng một snapshot.

---

# 6. Phương pháp khảo sát công cụ

## 6.1. Danh sách khảo sát

| STT | Công cụ | Nhóm chức năng dùng khi so sánh |
|---:|---|---|
| 1 | Apache JMeter | GUI/Test Plan; open-source Performance Testing |
| 2 | Silk Performer | Enterprise Performance Testing |
| 3 | Artillery | Developer-oriented/Test-as-Code |
| 4 | k6 | Developer-oriented/Test-as-Code |
| 5 | Locust | Developer-oriented/Test-as-Code |
| 6 | Gatling | Developer-oriented/Test-as-Code |
| 7 | Loader.io | Cloud-Based Service |
| 8 | Siege | Lightweight HTTP Benchmark |
| 9 | Vegeta | Lightweight HTTP Benchmark |
| 10 | wrk | Lightweight HTTP Benchmark |
| 11 | NeoLoad | Enterprise Performance Testing |
| 12 | ApacheBench | Lightweight HTTP Benchmark |
| 13 | OpenText LoadRunner Professional | Enterprise Performance Testing |
| 14 | Tsung | Distributed Load Testing |
| 15 | Taurus | Orchestration/Automation Framework |

Phân nhóm là bước kiểm soát tính công bằng: một Lightweight HTTP Benchmark có thể rất phù hợp để đo nhanh một endpoint nhưng không bị kỳ vọng phải có cùng workflow, correlation hoặc enterprise analytics như một full Performance Testing platform. Tương tự, Taurus được đánh giá như một orchestration layer, không phải load generator độc lập khi nó gọi JMeter hoặc executor khác.

## 6.2. Tiêu chí đánh giá

| Tiêu chí | Câu hỏi vận hành khi chấm điểm | Evidence tối thiểu để cho điểm |
|---|---|---|
| Cost & access | Sinh viên và audience có thể cài/sử dụng mà không bị cản bởi licence, trial hoặc tài khoản không? | Official licence/pricing/access page |
| Learning curve | Có thể hiểu workflow, chuẩn bị và thực hiện activity trong thời lượng seminar không? | Official getting-started + độ phức tạp cấu hình quan sát được từ docs; cần EXP để xác nhận thời gian |
| EShop fit | Có hỗ trợ HTTP API, auth/session, token/cookie, data parameterization và local target không? | Official protocol/scripting/session docs |
| Multi-step journey | Có biểu diễn tuần tự login → browse → product → cart → checkout và truyền dữ liệu động giữa bước không? | Official scenario/correlation/extraction docs |
| Workload control | Có concurrency/VU, arrival rate, ramp-up/ramp-down, duration và nhiều scenario không? | Official workload/execution docs |
| Assertions/checks | Có kiểm tra HTTP status, body và business condition; có thể đưa ra automated pass/fail không? | Official assertion/check/threshold docs |
| Reporting | Có percentiles, Throughput, Error Rate, raw output và report/integration không? | Official metrics/report/output docs |
| CI/CD | Có CLI, non-interactive execution, exit code/pass-fail và pipeline guidance không? | Official automation/CI docs |
| Reproducibility | Script/config, test data và output có thể lưu trong Git và chạy lại có kiểm soát không? | Official file/config/output docs; EXP cần xác nhận end-to-end |
| Local/offline | Sau setup, load generator có thể gọi EShop local mà không lệ thuộc cloud/Internet không? | Official architecture/deployment docs |
| AI-assisted potential | AI có thể hỗ trợ draft/audit artefact dễ đọc hay không, với human review bắt buộc? | Cấu trúc artefact chính thức + quy trình AI Audit do nhóm định nghĩa; không coi đây là native AI nếu docs không nói vậy |
| Classroom suitability | Audience có thể hoàn tất một activity có ý nghĩa trong tối đa 25 phút không? | Tổng hợp access, setup và workflow; bắt buộc EXP để xác nhận thời lượng |

`Community` là tiêu chí bắt buộc của Stage S1 nhưng không xuất hiện trong bảng 12 trọng số do nhóm cung cấp. Vì vậy mỗi hồ sơ vẫn chấm `Community` 1–5 với citation, nhưng ghi **0% — không tham gia Weighted Score**. Cách xử lý này giữ nguyên tổng trọng số 100% thay vì tự ý thay rubric đề xuất. Community được hiểu qua độ hiện hành của official docs, kênh support/forum/repository và khả năng tìm tài liệu học; số sao GitHub hoặc mức độ nổi tiếng không được dùng một mình để suy ra chất lượng.

### Quy tắc đánh giá AI-assisted potential

Tiêu chí này không hỏi “tool có phải AI tool không”. Nó hỏi liệu artefact của tool có thể được AI hỗ trợ tạo bản nháp, giải thích, chuyển đổi hoặc audit một cách minh bạch hay không. Điểm cao cần đồng thời có: artefact dạng text có thể review; đường biên assumption rõ; Checks/Thresholds có thể audit; và human reviewer có thể đối chiếu endpoint, auth, test data, think time, Workload Model cùng Failure Mode. Mọi AI-generated script đều là bản nháp cho đến khi được source review, dry validation và thực nghiệm.

## 6.3. Trọng số và thang điểm

> Đây là **trọng số do nhóm đề xuất**, không phải rubric chính thức của môn học.

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
| Community | 0% (đánh giá định tính bắt buộc; không tham gia công thức) |
| **Tổng** | **100%** |

```text
Weighted Score = Σ (Criterion Score / 5 × Criterion Weight)
```

Điểm cuối thuộc khoảng 0–100. Mỗi tiêu chí dùng thang 1–5:

| Điểm | Ý nghĩa chung |
|---:|---|
| 1 | Không đáp ứng hoặc rất hạn chế đối với phạm vi T05 |
| 2 | Đáp ứng yếu; cần workaround đáng kể |
| 3 | Đáp ứng cơ bản; có giới hạn cần quản lý |
| 4 | Đáp ứng tốt cho phần lớn nhu cầu T05 |
| 5 | Đáp ứng rất tốt và có evidence chính thức rõ cho phạm vi T05 |

### Scoring anchors để giảm thiên vị

Điểm 2 và 4 là mức trung gian giữa các anchor sau:

| Tiêu chí | Anchor 1 | Anchor 3 | Anchor 5 |
|---|---|---|---|
| Cost & access | Bị chặn bởi licence/account/trial cho activity | Có bản dùng được nhưng có điều kiện hoặc setup đáng kể | Miễn phí/local, audience dễ tái tạo |
| Learning curve | Không khả thi trong seminar nếu chưa có đào tạo riêng | Getting-started khả thi nhưng workflow cần hướng dẫn | First meaningful test ngắn, artefact dễ giải thích |
| EShop fit | Không phù hợp HTTP API/session flow | HTTP API cơ bản; state/data cần workaround | Hỗ trợ rõ multi-step auth, data và local API |
| Multi-step journey | Chủ yếu one-shot endpoint | Chuỗi bước khả thi nhưng biểu đạt/correlation hạn chế | Flow, state và dynamic extraction là first-class |
| Workload control | Chỉ concurrency/rate tối thiểu | Có duration/ramp hoặc nhiều profile cơ bản | VU + arrival-rate/open/closed + nhiều scenario/ramp |
| Assertions/checks | Không có business validation thực dụng | Status/body validation cơ bản | Business Checks + policy pass/fail rõ |
| Reporting | Chỉ số tổng hợp tối thiểu, khó lưu raw | Có core metrics và export cơ bản | Percentiles/Throughput/Error Rate + raw/integration/report |
| CI/CD | Manual/GUI hoặc cloud-only khó tự động | Có CLI nhưng pass/fail/report cần glue | Headless CLI + exit policy + official CI guidance |
| Reproducibility | Artefact khó lưu/chạy lại hoặc phụ thuộc account | Có config/script nhưng môi trường còn thủ công | Text/config + data + command + raw output dễ version control |
| Local/offline | Không gọi được localhost/private target | Local được nhưng một số bước cần Internet/account | Chạy local hoàn toàn sau setup |
| AI-assisted potential | Artefact binary/opaque; khó audit | Text/config có thể draft nhưng logic phân tán | Text-as-code rõ, dễ diff, test và human audit |
| Classroom suitability | Activity 25 phút không khả thi theo docs/access | Khả thi nếu pre-install/preconfigure | Audience có thể tạo/chạy/đọc kết quả trong activity ngắn |

### Cách đọc điểm provisional

- Mọi điểm trong bản này có Evidence `DOC` hoặc `ASSUMPTION`; chưa có điểm nào là `EXP`.
- `DOC` xác minh tính năng được nhà cung cấp/tổ chức mô tả, không xác minh usability hoặc performance trên máy nhóm.
- Các lý do rút gọn trong bảng điểm §7 là synthesis, không phải evidence độc lập: phải trace về citation tại các mục 2–13 của chính profile đó và hai Evidence ID `*-DOC-01/02` trong Appendix B.
- Learning curve, AI-assisted potential và Classroom suitability luôn chứa phần phán đoán ngữ cảnh. Dù citation là `DOC`, kết luận “phù hợp trong 25 phút” vẫn cần `[CẦN THỰC NGHIỆM]`.
- Không diễn giải chênh lệch nhỏ 1–3 điểm phần trăm như khác biệt có ý nghĩa trước khi hoàn tất calibration và thực nghiệm.

## 6.4. Quy trình đánh giá

### Vòng 1 — Desk Research

1. Dùng official documentation, product page, official repository và official licence/pricing page.
2. Ghi claim ở mức hẹp, đặt citation ngay sau claim và ghi ngày truy cập.
3. Gán Evidence ID và một trong ba mức: `DOC`, `EXP`, `ASSUMPTION`.
4. Hai reviewer nên chấm độc lập bằng scoring anchors, sau đó thảo luận ô lệch từ 2 điểm trở lên. `[CẦN THỰC NGHIỆM QUY TRÌNH REVIEW]`

### Vòng 2 — Smoke Test

Thực hiện cùng mục tiêu tối thiểu cho từng tool có thể truy cập: gửi một HTTP GET đến `[VERIFIED_BASE_URL][VERIFIED_PRODUCT_ENDPOINT]`, kiểm tra protocol result, lưu command/config, version, console output và raw result nếu tool hỗ trợ. Tất cả kế hoạch hiện tại mang nhãn `[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN]`.

### Vòng 3 — EShop Fit Test

Chỉ deep-test các ứng viên còn lại sau vòng 1–2 nhưng dùng cùng một Workload Model và cùng dataset. Flow chuẩn:

```text
POST [VERIFIED_LOGIN_ENDPOINT]
  → extract token/cookie
GET  [VERIFIED_PRODUCT_ENDPOINT]
  → extract/parameterize product
POST [VERIFIED_CART_ENDPOINT]
POST [VERIFIED_CHECKOUT_ENDPOINT]
  → assert business outcome without reusing destructive data
```

Thu p50, p95, p99, Throughput và Error Rate; lưu raw result; theo dõi CPU/RAM của load generator lẫn SUT. Tách warm-up khỏi measurement window; cố định data, version, duration và môi trường; không so raw throughput nếu hai script không tạo cùng logical workload.

### Vòng 4 — Shortlist và Pair Selection

Quyết định dùng bốn lớp evidence:

1. Weighted Score provisional.
2. Điều kiện loại trực tiếp trong phạm vi seminar.
3. Chất lượng và độ phủ evidence.
4. Complementarity so với learning objectives traditional + AI-augmented.

Pair selection không mặc định lấy hai điểm cao nhất. Nếu hai tool gần như cùng workflow và learning value, một tool có điểm thấp hơn đôi chút nhưng bổ sung một cách tiếp cận khác có thể tạo cặp seminar tốt hơn; trade-off phải được nêu rõ.

## 6.5. Quy tắc evidence

| Mức | Ý nghĩa | Được phép kết luận | Không được phép suy rộng |
|---|---|---|---|
| `DOC` | Verified from official documentation/product/repository | Tính năng, licence, command hoặc kiến trúc được tài liệu mô tả | Tool đã cài/chạy thành công trên máy nhóm; metrics thực tế |
| `EXP-PLAN` | Ô/ID dành trước cho thí nghiệm chưa chạy | Chỉ được mô tả setup, expected evidence, failure modes và success criteria | Đã quan sát, pass/fail, metric hoặc evidence thực nghiệm |
| `EXP` | Verified by actual experiment với artefact truy nguyên được | Kết quả đúng trong version, SUT, workload và môi trường đã ghi | Kết quả phổ quát cho version/môi trường khác |
| `ASSUMPTION` | Chưa xác minh hoặc là phán đoán theo context | Giả thuyết/kế hoạch cần kiểm tra | Fact hoặc basis duy nhất của kết luận cuối |

Mỗi evidence thực nghiệm phải có tối thiểu: tool/version; OS/runtime; timestamp; Git commit EShop; command; config/script; anonymized test data; raw output; log SUT; CPU/RAM context; expected-versus-observed; người thực hiện. Screenshot chỉ là bằng chứng phụ, không thay raw result hoặc script.

Thông tin pricing/trial có tính thời điểm. Tài liệu này ghi ngày truy cập 2026-07-14; nhóm phải re-check ngay trước ngày nộp nếu ngày nộp khác đáng kể.

## 6.6. Điều kiện sàng lọc

Một tool có thể không được deep-test trong **phạm vi seminar hiện tại** nếu gặp một hoặc nhiều điều kiện sau; đây không phải kết luận tool “kém”:

1. Không thể nhắm EShop local/private target.
2. Live activity phụ thuộc Internet hoặc external service không kiểm soát được.
3. Licence/trial/account khiến audience không thể tái tạo.
4. Full EShop flow cần workaround session/token/correlation quá lớn so với thời lượng.
5. Không lưu được script/config và raw evidence đủ cho Reproducibility.
6. First meaningful activity không khả thi trong 25 phút, kể cả khi pre-install hợp lý.
7. Vai trò bị trùng với ứng viên đã shortlist nhưng không bổ sung learning objective cần thiết.
8. Công cụ là orchestration layer nhưng đang bị chấm nhầm như engine tạo tải.
9. Claim quyết định không có evidence đủ tin cậy.

Điều kiện sàng lọc được áp dụng sau khi ghi nhận điểm mạnh của tool. Commercial platform không bị loại vì “nhiều tính năng”; vấn đề là access, scope và khả năng tái tạo trong lớp. Lightweight benchmark không bị loại vì “ít tính năng”; nó được giữ ở vai trò supporting benchmark nếu phù hợp one-endpoint diagnostics.

## 6.7. Câu hỏi phản biện

<details>
<summary><strong>Câu hỏi phản biện</strong></summary>

### Câu 1. Làm sao bảo đảm cùng một tiêu chí được dùng cho cả 15 công cụ có mục đích khác nhau?

**Trả lời:** Cả 15 tool dùng cùng 12 tiêu chí và cùng scoring anchors, nhưng kết quả được diễn giải trong nhóm chức năng. Điểm thấp ở Multi-step journey của một benchmark tool mô tả mismatch với EShop journey, không phủ nhận giá trị benchmark endpoint của nó.

### Câu 2. Điểm tổng có thể che giấu điều gì?

**Trả lời:** Điểm tổng có thể bù trừ một blocker — ví dụ điểm reporting cao không khắc phục việc không gọi được EShop local. Vì vậy quyết định còn dùng điều kiện loại trực tiếp, evidence quality và complementarity.

### Câu 3. Có công bằng khi chưa cài được commercial tool không?

**Trả lời:** Công bằng ở vòng Desk Research nếu chỉ chấm claim đã có official evidence và đánh dấu chưa có EXP. Không công bằng nếu biến “nhóm chưa cài” thành “tool không làm được”. Kết luận access/classroom chỉ là provisional và ghi rõ trial/account constraint.

### Câu 4. Làm sao tránh thiên vị do mỗi thành viên phụ trách một tool?

**Trả lời:** Dùng anchor chung, yêu cầu citation trên từng ô, chấm độc lập chéo và review các chênh lệch lớn. Tên tool nên được ẩn trong một lượt calibration nếu nhóm có thể chuẩn hóa mô tả capability.

### Câu 5. Vì sao tài liệu có điểm số khi chưa thực nghiệm?

**Trả lời:** Điểm số hiện là decision hypothesis dựa trên DOC, giúp xác định test nào có giá trị thông tin cao nhất. Chúng không phải empirical ranking và phải được cập nhật sau Smoke Test/EShop Fit Test.

</details>

---

# 7. Khảo sát 15 công cụ Performance Testing

## 7.1. Apache JMeter

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
| Cost & access | 8% | 5 | Apache 2.0, không account/VU fee | DOC; **Trace:** JM-DOC-01, JM-DOC-02. |
| Learning curve | 8% | 3 | GUI tốt; correlation/thread model cần học | ASSUMPTION từ DOC; **Trace:** JM-DOC-01, JM-DOC-02. |
| EShop fit | 15% | 5 | HTTP/state/data/assertion/local | DOC + ASSUMPTION; **Trace:** JM-DOC-01, JM-DOC-02. |
| Multi-step journey & state | 12% | 5 | Cookie, extractor, CSV, controllers | DOC; **Trace:** JM-DOC-01, JM-DOC-02. |
| Workload model & scalability | 10% | 5 | Thread/ramp/timers/open/remote | DOC; **Trace:** JM-DOC-01, JM-DOC-02. |
| Assertions & business validation | 8% | 5 | Response/JSON/XPath | DOC; **Trace:** JM-DOC-01, JM-DOC-02. |
| Metrics & reporting | 8% | 5 | JTL, percentile, throughput, HTML/APDEX | DOC; **Trace:** JM-DOC-01, JM-DOC-02. |
| CI/CD & automation | 7% | 4 | Headless; threshold gate cần wrapper | DOC + ASSUMPTION; **Trace:** JM-DOC-01, JM-DOC-02. |
| Reproducibility | 7% | 4 | `.jmx`/CSV/CLI; phải pin plugin/version | DOC + ASSUMPTION; **Trace:** JM-DOC-01, JM-DOC-02. |
| Local/offline | 5% | 5 | Runner/report local | DOC; **Trace:** JM-DOC-01, JM-DOC-02. |
| AI-assisted potential | 7% | 3 | Draft được, XML khó audit, không native | ASSUMPTION; **Trace:** JM-DOC-01, JM-DOC-02. |
| Classroom suitability | 5% | 4 | Free/GUI nếu pre-install | ASSUMPTION; **Trace:** JM-DOC-01, JM-DOC-02. |
| Community | 0% | 5 | Manual, source, mailing lists ([Mailing lists](https://jmeter.apache.org/mail.html) — truy cập 2026-07-14) | DOC; không tính; **Trace:** JM-DOC-01, JM-DOC-02. |

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

## 7.2. Silk Performer

### 1. Tổng quan

Silk Performer là bộ performance/load testing thương mại của OpenText, mô phỏng VU cho web, database, distributed application và middleware, kèm Workbench/analysis ([OpenText Marketplace](https://marketplace.opentext.com/appdelivery/content/silk-performer) — truy cập 2026-07-14). Evidence: `DOC`.

### 2. Cost và licence

Installation Guide 21.0 mô tả Evaluation 45 ngày, giới hạn 10 VU; Workbench Help lại có đoạn nói 30 ngày. Giá commercial không công khai trong nguồn kiểm tra: `[CẦN BÁO GIÁ]`; entitlement thực phải xác minh, không tự hoà giải mâu thuẫn ([Installation Guide](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-installationguide-en.pdf), [Workbench Help](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-workbenchhelp-en.pdf) — truy cập 2026-07-14). Evidence: `DOC`.

### 3. Installation và platform support

Workbench/Controller 21.0 là Windows-centric, cần quyền admin; guide nêu khoảng 2,5 GB cho controller và 1 GB cho agent. Có silent installation và remote agents; container support không được xác nhận ([Installation Guide](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-installationguide-en.pdf), [Silent install](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-7DA0F053-INSTALLINGSILENTMODE-TSK.html) — truy cập 2026-07-14). Evidence: `DOC`; container: `ASSUMPTION`.

### 4. Scripting hoặc configuration model

Workbench record/generate Benchmark Description Language (BDL); có Java framework và HAR import. Project/script/workload lưu được, nhưng tooling/version/license làm Git reproducibility nặng hơn plain text tool ([Java framework](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-E71FE522-JAVAFM-CON.html), [Release Notes 19.5](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-releasenotes-en.pdf) — truy cập 2026-07-14). Evidence: `DOC` + `ASSUMPTION`.

### 5. Workload capabilities

Increasing, Steady State, Dynamic, All Day, Queuing arrival-rate và Verification models; warm-up/measurement/close-down, runtime adjustment và agent distribution. Parsing/context functions, per-VU cookies/cache, sequential/random multi-column data hỗ trợ correlation/session/parameterization ([Workload models](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-webhelp-en/SILKPERF-390794D9-WORKLOADMODELS-CON.html), [Parsing](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-0A2D472E-PARSINGFUNCTIONS-CON.html), [Agent assignment](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-webhelp-en/SILKPERF-0A0FF53D-WORKLOADCONFIGURATIONDIALOG-AGENTASSIGNMENT-REF.html) — truy cập 2026-07-14). Evidence: `DOC`.

### 6. Assertions và validation

Web verification kiểm tra response content/HTML/XML/data; baseline/performance threshold hỗ trợ pass/fail evaluation ([Web tutorial](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webloadtestingtutorial-en.pdf), [Baselines](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-B176837E-CONFIRMINGTESTBASELINES-CON.html) — truy cập 2026-07-14). Protocol-specific depth: `[CẦN THỰC NGHIỆM]`. Evidence: `DOC`.

### 7. Metrics và reporting

Real-time monitoring, browser HTML results, VU output/log và `.tsd` time-series; percentile function có accuracy/memory setting, nên p50/p95/p99 phải ghi cấu hình ([Real-time monitoring](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/GUID-626CEE1A-9989-4E61-B54D-7C6A1CCC387B.html), [Results](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-7CBD1FDA-VIEWINGRESULTSINWEBBROWSER-CON.html), [Percentile](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-webhelp-en/GUID-271C001F-FE5E-4B28-AA37-1B087F916493.html) — truy cập 2026-07-14). Evidence: `DOC`.

### 8. CI/CD và automation

`performer project.ltp /Automation 5 /WL:Workload /Resultsdir:<path>`; Jenkins integration có success conditions/performance levels. Public docs chưa cho contract exit code đủ rõ; cần positive/negative lab và Event Viewer/output audit ([CLI automation](https://www.microfocus.com/documentation/silk-performer/205/en/silkperformer-205-webhelp-en/GUID-BE43A9E4-6B4C-46CB-BCA9-6A3E7CE51F36.html), [Release Notes](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-releasenotes-en.pdf) — truy cập 2026-07-14). Evidence: `DOC`; exit semantics: `[CẦN THỰC NGHIỆM]`.

### 9. EShop suitability

Web/API flow, independent VU state, parser/correlation, data và multi-phase workload phù hợp login → catalog → cart → checkout. Access/license/Windows làm giảm fit trong seminar, không phủ nhận enterprise capability ([Web settings](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webhelp-en/SILKPERF-790881A8-WEBSETTINGS-CON.html) — truy cập 2026-07-14). Evidence: `DOC` + fit `ASSUMPTION`.

### 10. AI-assisted potential

HAR + BDL/Java cho phép AI draft/audit, nhưng không tìm thấy native AI current trong docs 21.0. Human phải replay, audit parser/correlation, data/secret và workload. Evidence: `ASSUMPTION`.

### 11. Classroom suitability

Workbench trực quan nhưng Windows/admin/trial 10 VU và tài liệu 30/45 ngày mâu thuẫn cản trở activity 25 phút; chỉ khả thi nếu pre-install/pre-license, vẫn `[CẦN THỰC NGHIỆM]`. Evidence: `DOC` + `ASSUMPTION`.

### 12. Điểm mạnh trong phạm vi seminar

Workload doanh nghiệp đa dạng; correlation/parser; distributed agents; verification; real-time/percentile/baseline reporting ([Documentation 21.0](https://www.microfocus.com/documentation/silk-performer/) — truy cập 2026-07-14). Evidence: `DOC`.

### 13. Hạn chế trong phạm vi seminar

Commercial price không public; trial docs mâu thuẫn; Windows-heavy; public docs latest tìm thấy là 21.0; container và direct exit semantics chưa xác nhận. Các điểm này là scope/access limits, không phải kết luận tool “kém”. Evidence: `DOC`/`ASSUMPTION` đã đánh dấu.

### 14. Smoke Test Plan

**[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN]**

- **Mục tiêu:** 1 GET, content verification, 1 VU và result/report.
- **Prerequisites:** Windows/admin, installer checksum, Evaluation/licensed entitlement, `[VERIFIED_BASE_URL]`, quyền test.
- **Installation/setup:** cài 21.0; ghi OS/version/license; Workbench tạo Web project + Verification workload 1 VU/1 iteration.
- **Request:** `GET [VERIFIED_BASE_URL]/[VERIFIED_READ_ONLY_PATH]` với status/content verification.
- **Command/config:** `performer C:\lab\silk-smoke\silk-smoke.ltp /Automation 5 /WL:Verification /Resultsdir:C:\lab\artifacts\silk-smoke` ([CLI](https://www.microfocus.com/documentation/silk-performer/205/en/silkperformer-205-webhelp-en/GUID-BE43A9E4-6B4C-46CB-BCA9-6A3E7CE51F36.html) — truy cập 2026-07-14).
- **Kết quả mong đợi:** verification pass, output/result/report sinh; chưa quan sát.
- **Evidence:** version/license redacted, project/BDL/workload, command, stdout/stderr/exit, Event Viewer, VU output, report.
- **Lỗi có thể gặp:** trial hết/10 VU, admin/runtime, TLS/proxy, parser/marker, agent unavailable, results path.
- **Tiêu chí thành công:** đúng request/verification, không automation error, đủ artefact; marker sai phải chứng minh failure propagation.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Lý do | Evidence |
|---|---:|---:|---|---|
| Cost & access | 8% | 2 | Trial 10 VU; commercial/price cần xác minh | DOC; **Trace:** SP-DOC-01, SP-DOC-02. |
| Learning curve | 8% | 2 | Workbench + BDL/agents/workloads | ASSUMPTION từ DOC; **Trace:** SP-DOC-01, SP-DOC-02. |
| EShop fit | 15% | 4 | Web state/data/verification tốt, access friction | DOC + ASSUMPTION; **Trace:** SP-DOC-01, SP-DOC-02. |
| Multi-step journey & state | 12% | 5 | Cookie/parser/correlation/data | DOC; **Trace:** SP-DOC-01, SP-DOC-02. |
| Workload model & scalability | 10% | 5 | Arrival/concurrency/dynamic/distributed | DOC; **Trace:** SP-DOC-01, SP-DOC-02. |
| Assertions & business validation | 8% | 4 | Content verification/thresholds | DOC; **Trace:** SP-DOC-01, SP-DOC-02. |
| Metrics & reporting | 8% | 5 | Real-time/raw/log/HTML/percentile | DOC; **Trace:** SP-DOC-01, SP-DOC-02. |
| CI/CD & automation | 7% | 4 | CLI/Jenkins; exit cần lab | DOC + ASSUMPTION; **Trace:** SP-DOC-01, SP-DOC-02. |
| Reproducibility | 7% | 3 | Project lưu được; Windows/license/agents nặng | ASSUMPTION; **Trace:** SP-DOC-01, SP-DOC-02. |
| Local/offline | 5% | 4 | On-prem runner; activation/air-gap cần xác minh | DOC + ASSUMPTION; **Trace:** SP-DOC-01, SP-DOC-02. |
| AI-assisted potential | 7% | 3 | HAR/BDL draft được, không native AI xác nhận | ASSUMPTION; **Trace:** SP-DOC-01, SP-DOC-02. |
| Classroom suitability | 5% | 2 | Trial/admin/Windows khó nhân rộng | ASSUMPTION; **Trace:** SP-DOC-01, SP-DOC-02. |
| Community | 0% | 3 | Official catalog/marketplace có, nhưng public docs hiện hành hạn chế ([docs](https://www.microfocus.com/documentation/silk-performer/) — truy cập 2026-07-14) | DOC; không tính; **Trace:** SP-DOC-01, SP-DOC-02. |

**Weighted Score provisional: 74,8/100; 0 EXP.**

### 16. Kết luận sơ bộ

**Survey-only.** Ghi nhận enterprise workload/analysis; không chọn live activity cho đến khi access, version và 25-minute workflow được chứng minh.

### 17. Câu hỏi phản biện

<details>
<summary><strong>Câu hỏi phản biện Silk Performer</strong></summary>

1. **Trial 30 hay 45 ngày?** Official docs mâu thuẫn; entitlement tài khoản thực mới quyết định ([Install Guide](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-installationguide-en.pdf) — truy cập 2026-07-14).
2. **10 VU chứng minh scalability?** Không; chỉ đủ smoke/learning, không đủ capacity conclusion.
3. **Report đẹp có đủ thay JMeter?** Không; access, reproducibility, local/classroom và role complementarity vẫn phải chấm.
4. **CLI tự fail build khi threshold fail?** Chưa được chứng minh; cần positive/negative run và process/report evidence.

</details>

## 7.3. Artillery

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
| Cost & access (8%) | 4/5 | OSS local, nhưng Azure licence nuance/Cloud limits. **DOC** ([repo](https://github.com/artilleryio/artillery), [pricing](https://www.artillery.io/pricing) — truy cập 2026-07-14); **Trace:** AR-DOC-01, AR-DOC-02. |
| Learning curve (8%) | 4/5 | YAML dễ bắt đầu; plugin/processor cần hướng dẫn. **DOC + ASSUMPTION** ([scripts](https://www.artillery.io/docs/reference/test-script) — truy cập 2026-07-14); **Trace:** AR-DOC-01, AR-DOC-02. |
| EShop fit (15%) | 5/5 | Cookie/capture/data/HTTP flow. **DOC + ASSUMPTION** ([HTTP engine](https://www.artillery.io/docs/reference/engines/http) — truy cập 2026-07-14); **Trace:** AR-DOC-01, AR-DOC-02. |
| Multi-step journey (12%) | 4/5 | Flow/capture/hooks tốt; logic phức tạp sang processor. **DOC + ASSUMPTION** ([HTTP engine](https://www.artillery.io/docs/reference/engines/http) — truy cập 2026-07-14); **Trace:** AR-DOC-01, AR-DOC-02. |
| Workload control (10%) | 4/5 | Arrival/ramp/count/cap mạnh; closed model hạn chế. **DOC + ASSUMPTION** ([phases](https://www.artillery.io/docs/reference/test-script) — truy cập 2026-07-14); **Trace:** AR-DOC-01, AR-DOC-02. |
| Assertions/checks (8%) | 4/5 | expect + ensure, nhưng là hai lớp và có caveat. **DOC** ([Expect](https://www.artillery.io/docs/reference/extensions/expect), [Ensure](https://www.artillery.io/docs/reference/extensions/ensure) — truy cập 2026-07-14); **Trace:** AR-DOC-01, AR-DOC-02. |
| Reporting (8%) | 4/5 | Rich console/JSON; local HTML removed. **DOC** ([metrics](https://www.artillery.io/docs/reference/reported-metrics), [report](https://www.artillery.io/docs/reference/cli/report) — truy cập 2026-07-14); **Trace:** AR-DOC-01, AR-DOC-02. |
| CI/CD (7%) | 5/5 | Official CI/Docker và non-zero ensure gate. **DOC** ([CI/CD](https://www.artillery.io/docs/cicd) — truy cập 2026-07-14); **Trace:** AR-DOC-01, AR-DOC-02. |
| Reproducibility (7%) | 5/5 | Text config + lock/image + raw JSON. **DOC + ASSUMPTION** ([run](https://www.artillery.io/docs/reference/cli/run) — truy cập 2026-07-14); **Trace:** AR-DOC-01, AR-DOC-02. |
| Local/offline (5%) | 4/5 | Local CLI/JSON; strict offline cần cache, no local HTML. **DOC + ASSUMPTION** ([install](https://www.artillery.io/docs/get-started/get-artillery), [report](https://www.artillery.io/docs/reference/cli/report) — truy cập 2026-07-14); **Trace:** AR-DOC-01, AR-DOC-02. |
| AI-assisted potential (7%) | 4/5 | Text/agent-friendly, nhưng tool không AI và cần audit. **ASSUMPTION** ([homepage](https://www.artillery.io/) — truy cập 2026-07-14); **Trace:** AR-DOC-01, AR-DOC-02. |
| Classroom suitability (5%) | 5/5 | YAML activity ngắn nếu pre-install; thời gian cần EXP. **ASSUMPTION**; **Trace:** AR-DOC-01, AR-DOC-02. |
| Community (0%) | 4/5 | Official docs, repo và Discussions hiện hành; không vào Weighted Score. **DOC** ([docs](https://www.artillery.io/docs), [repo](https://github.com/artilleryio/artillery) — truy cập 2026-07-14); **Trace:** AR-DOC-01, AR-DOC-02. |

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

## 7.4. k6

**1. Tổng quan.** **[DOC]** k6 là developer-oriented performance-testing tool do Grafana Labs duy trì, dùng test-as-code cho protocol load và có browser module/Studio bổ sung. ([k6 repository](https://github.com/grafana/k6), [k6 documentation](https://grafana.com/docs/k6/latest/) — truy cập 2026-07-14)

**2. Cost và licence.** **[DOC]** Repository hiện cấp phép **AGPL-3.0**; local OSS CLI không đòi Cloud account. Grafana Cloud k6 là tùy chọn; pricing hiện có Free 0 USD với 500 VUh/tháng và paid usage theo trang giá, vì vậy con số phải re-check trước nộp. ([k6 repository/licence](https://github.com/grafana/k6), [Grafana pricing](https://grafana.com/pricing/) — truy cập 2026-07-14) **[ASSUMPTION]** Local seminar access cao; legal implications nếu sửa/nhúng/phân phối cần chuyên gia, không suy từ activity CLI.

**3. Installation và platform support.** **[DOC]** Official install bao phủ Linux, macOS, Windows, standalone binary và image Docker **grafana/k6**; k6 Studio có desktop build cho Windows/macOS/Linux. ([Install k6](https://grafana.com/docs/k6/latest/set-up/install-k6/), [k6 Studio](https://grafana.com/docs/k6/latest/k6-studio/) — truy cập 2026-07-14) **[ASSUMPTION]** Setup ngắn nếu pin binary/image; strict offline cần cache trước.

**4. Scripting hoặc configuration model.** **[DOC]** Test viết bằng JavaScript nhưng chạy trên k6 runtime riêng, **không phải Node.js và không phải browser runtime**; Node built-ins không mặc định có, package npm cần đánh giá/bundle tương thích. Script/module/options là text dễ Git diff/review. ([First test](https://grafana.com/docs/k6/latest/get-started/write-your-first-test/), [Modules](https://grafana.com/docs/k6/latest/using-k6/modules/) — truy cập 2026-07-14) k6 Studio có thể record flow/HAR; **har-to-k6** tạo script khởi đầu nhưng docs yêu cầu chỉnh correlation, data và load profile. Browser-recorder extension cũ đã deprecated. ([k6 Studio](https://grafana.com/docs/k6/latest/k6-studio/), [HAR converter](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-har-converter/), [Recorder status](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-browser-recorder/) — truy cập 2026-07-14)

**5. Workload capabilities.** **[DOC]** Scenarios có shared/per-VU iterations, constant/ramping VUs và constant/ramping arrival rate; từng scenario có start time, function, environment và tags. ([Scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/) — truy cập 2026-07-14) Cookie jar là per-VU; response body/JSON dùng cho token/ID correlation; variables/JSON/SharedArray hỗ trợ test data. ([Cookies](https://grafana.com/docs/k6/latest/using-k6/cookies/), [HTTP Response](https://grafana.com/docs/k6/latest/javascript-api/k6-http/response/), [Data parameterization](https://grafana.com/docs/k6/latest/examples/data-parameterization/) — truy cập 2026-07-14) Arrival-rate executors cần đủ pre-allocated/max VUs và theo dõi dropped iterations. ([Executors](https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/) — truy cập 2026-07-14)

**6. Assertions và validation.** **[DOC]** Checks kiểm Boolean status/body/business condition và tạo rate metric, nhưng check fail **không tự làm process fail**. Thresholds là acceptance criteria trên trend/rate/counter/gauge, hỗ trợ percentile/abortOnFail và trả non-zero khi fail. ([Checks](https://grafana.com/docs/k6/latest/using-k6/checks/), [Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) — truy cập 2026-07-14) Pipeline phải đặt threshold trên checks/http_req_failed/latency thay vì chỉ viết check.

**7. Metrics và reporting.** **[DOC]** k6 có end-of-test summary, custom metrics, granular points, JSON/CSV, external outputs và custom summary HTML/JSON/XML. Built-in web dashboard hiển thị realtime và export self-contained HTML. ([Results output](https://grafana.com/docs/k6/latest/get-started/results-output/), [Web dashboard](https://grafana.com/docs/k6/latest/results-output/web-dashboard/) — truy cập 2026-07-14) Core HTTP metrics bao phủ request duration/failure/rate; custom tags hỗ trợ endpoint/journey breakdown. ([Built-in metrics](https://grafana.com/docs/k6/latest/using-k6/metrics/reference/) — truy cập 2026-07-14)

**8. CI/CD và automation.** **[DOC]** CLI chính là **k6 run**; threshold failure tạo error exit. Official integrations liệt kê GitHub Actions, GitLab, Jenkins, Azure Pipelines và AWS CodeBuild; Docker image hỗ trợ pipeline/container. ([Integrations](https://grafana.com/docs/k6/latest/reference/integrations/), [Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/), [Install/Docker](https://grafana.com/docs/k6/latest/set-up/install-k6/) — truy cập 2026-07-14)

**9. EShop suitability.** **[ASSUMPTION dựa trên DOC]** HTTP, per-VU cookie, JSON/token extraction, SharedArray, multiple scenarios và open/closed-style executors phù hợp login → product → cart → checkout trên local EShop. Exact routes, refresh token, destructive checkout data và cleanup là **[CẦN THỰC NGHIỆM]**. Browser module có thể đo một số frontend/Web Vitals nhưng không nên thay toàn bộ backend protocol load; browser-VU capacity cần đo. ([Browser tests](https://grafana.com/docs/k6/latest/using-k6-browser/running-browser-tests/) — truy cập 2026-07-14)

**10. AI-assisted potential.** k6 **không phải AI tool**. **[ASSUMPTION]** JavaScript/HAR/text output phù hợp để AI draft scenario/check/threshold, gợi ý correlation và tóm tắt result; nhưng generated script không chứng minh đúng workload/business semantics. Human audit bắt buộc cho endpoints, secrets, data, correlation, think time, scenario mix, executor/VU capacity, tags, checks, SLO thresholds và Failure Modes. HAR docs xác nhận generated script vẫn phải chỉnh. ([HAR converter](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-har-converter/) — truy cập 2026-07-14)

**11. Classroom suitability.** **[ASSUMPTION]** Một file JavaScript, binary CLI và local HTML/raw output phù hợp activity ≤25 phút nếu pre-install. Ba khái niệm phải dạy rõ: runtime không phải Node, check khác threshold, browser VU khác protocol VU. Actual activity time là **[CẦN THỰC NGHIỆM]**.

**12. Điểm mạnh trong phạm vi seminar.**

- **[DOC]** Workload executors rộng, script/version-control rõ. ([Scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/) — truy cập 2026-07-14)
- **[DOC]** Checks + thresholds + exit code tạo audit/CI path minh bạch. ([Checks](https://grafana.com/docs/k6/latest/using-k6/checks/), [Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) — truy cập 2026-07-14)
- **[DOC]** Raw JSON/CSV, custom output và self-contained HTML tốt cho evidence. ([Results](https://grafana.com/docs/k6/latest/get-started/results-output/), [Dashboard](https://grafana.com/docs/k6/latest/results-output/web-dashboard/) — truy cập 2026-07-14)
- **[DOC]** HAR/Studio/browser bổ sung authoring/frontend path mà không bắt buộc Cloud. ([Studio](https://grafana.com/docs/k6/latest/k6-studio/) — truy cập 2026-07-14)

**13. Hạn chế trong phạm vi seminar.**

- **[DOC]** Runtime riêng khiến Node/npm assumption dễ sai. ([Modules](https://grafana.com/docs/k6/latest/using-k6/modules/) — truy cập 2026-07-14)
- **[DOC]** Check fail không tự fail CI; thiếu threshold tạo false pass. ([Checks](https://grafana.com/docs/k6/latest/using-k6/checks/) — truy cập 2026-07-14)
- **[DOC]** HAR/recorded script chưa tự giải quyết correlation/data/workload. ([HAR converter](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-har-converter/) — truy cập 2026-07-14)
- **[ASSUMPTION]** Coding requirement và workload correctness vẫn cần reviewer; browser VU/resource ceiling cần EXP.

**14. Smoke Test Plan.** **[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN; 0 EXP]**

- **Mục tiêu:** xác nhận install, một GET idempotent, check, threshold, raw JSON và exit.
- **Prerequisites:** authorized target; thay **[VERIFIED_BASE_URL]** và **[VERIFIED_PRODUCT_ENDPOINT]**; pin k6; tạo artifacts directory.
- **Installation/setup:** official package/binary hoặc pinned image; ghi k6 version, OS/CPU/RAM, Git commit.
- **Request/config mẫu:**

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
  const response = http.get(
    "[VERIFIED_BASE_URL][VERIFIED_PRODUCT_ENDPOINT]"
  );
  check(response, {
    "status is 200": (r) => r.status === 200,
  });
}
~~~

- **Command:** **k6 run --out json=artifacts/k6-smoke.json smoke.js**.
- **Kết quả mong đợi:** đúng một iteration, checks/thresholds pass, exit 0, JSON + summary được tạo; chưa quan sát. ([Checks](https://grafana.com/docs/k6/latest/using-k6/checks/), [Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) — truy cập 2026-07-14)
- **Evidence cần thu:** version/command; script/hash; stdout/stderr; exit; raw JSON; summary/HTML nếu bật; timestamps; machine/SUT metadata; Git commit.
- **Lỗi có thể gặp:** DNS/TLS/proxy, auth/redirect, write permission/container volume, threshold syntax, remote module/npm assumption.
- **Tiêu chí thành công:** đúng one-iteration raw record, status/check/threshold đạt, exit 0, artifacts đầy đủ và target trong scope.

**15. Điểm đánh giá provisional.** Mọi điểm là **DOC + ASSUMPTION**, **không có EXP**.

| Tiêu chí | Điểm | Lý do, evidence và nguồn |
|---|---:|---|
| Cost & access (8%) | 5/5 | AGPL OSS local; Cloud optional. **DOC** ([repo](https://github.com/grafana/k6), [pricing](https://grafana.com/pricing/) — truy cập 2026-07-14); **Trace:** K6-DOC-01, K6-DOC-02. |
| Learning curve (8%) | 4/5 | JavaScript dễ, runtime riêng cần học. **DOC + ASSUMPTION** ([modules](https://grafana.com/docs/k6/latest/using-k6/modules/) — truy cập 2026-07-14); **Trace:** K6-DOC-01, K6-DOC-02. |
| EShop fit (15%) | 5/5 | HTTP/cookie/JSON/data/tag. **DOC + ASSUMPTION** ([cookies](https://grafana.com/docs/k6/latest/using-k6/cookies/), [data](https://grafana.com/docs/k6/latest/examples/data-parameterization/) — truy cập 2026-07-14); **Trace:** K6-DOC-01, K6-DOC-02. |
| Multi-step journey (12%) | 5/5 | Per-VU state và multiple scenarios. **DOC + ASSUMPTION** ([scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/) — truy cập 2026-07-14); **Trace:** K6-DOC-01, K6-DOC-02. |
| Workload control (10%) | 5/5 | Iteration, VU và arrival-rate executors. **DOC** ([scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/) — truy cập 2026-07-14); **Trace:** K6-DOC-01, K6-DOC-02. |
| Assertions/checks (8%) | 5/5 | Business checks + threshold/exit gate. **DOC** ([checks](https://grafana.com/docs/k6/latest/using-k6/checks/), [thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) — truy cập 2026-07-14); **Trace:** K6-DOC-01, K6-DOC-02. |
| Reporting (8%) | 5/5 | Summary, raw output, stream và local HTML. **DOC** ([results](https://grafana.com/docs/k6/latest/get-started/results-output/), [dashboard](https://grafana.com/docs/k6/latest/results-output/web-dashboard/) — truy cập 2026-07-14); **Trace:** K6-DOC-01, K6-DOC-02. |
| CI/CD (7%) | 5/5 | CLI/non-zero threshold exit/official integrations. **DOC** ([integrations](https://grafana.com/docs/k6/latest/reference/integrations/) — truy cập 2026-07-14); **Trace:** K6-DOC-01, K6-DOC-02. |
| Reproducibility (7%) | 5/5 | Text script + pin binary/image + raw evidence. **DOC + ASSUMPTION** ([install](https://grafana.com/docs/k6/latest/set-up/install-k6/) — truy cập 2026-07-14); **Trace:** K6-DOC-01, K6-DOC-02. |
| Local/offline (5%) | 5/5 | Local binary/output/report; cache trước. **DOC + ASSUMPTION** ([install](https://grafana.com/docs/k6/latest/set-up/install-k6/) — truy cập 2026-07-14); **Trace:** K6-DOC-01, K6-DOC-02. |
| AI-assisted potential (7%) | 5/5 | JS/HAR dễ draft/diff/audit; tool không AI. **ASSUMPTION** ([HAR](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-har-converter/) — truy cập 2026-07-14); **Trace:** K6-DOC-01, K6-DOC-02. |
| Classroom suitability (5%) | 4/5 | Activity ngắn nếu pre-install; runtime/check/threshold caveat. **ASSUMPTION**; **Trace:** K6-DOC-01, K6-DOC-02. |
| Community (0%) | 5/5 | Official docs, active public repo/issues/community; không vào Weighted Score. **DOC** ([docs](https://grafana.com/docs/k6/latest/), [repo](https://github.com/grafana/k6) — truy cập 2026-07-14); **Trace:** K6-DOC-01, K6-DOC-02. |

**Weighted Score provisional: 97.4/100.** Đây không phải empirical ranking.

**16. Kết luận sơ bộ.** **Main candidate.** k6 phù hợp code-first/AI-assisted-draft + human-audit learning objective và EShop protocol flow, nhưng selection vẫn provisional cho đến khi k6 và counterfactual tool chạy cùng workload/evidence protocol.

**17. Câu hỏi phản biện.**

<details>
<summary><strong>Câu hỏi phản biện</strong></summary>

### Câu 1. k6 có phải AI tool không?

**Trả lời:** Không. AI chỉ hỗ trợ draft/audit text artefact; k6 là deterministic load-testing engine.

### Câu 2. Checks đều có thì tại sao còn cần thresholds?

**Trả lời:** Check failure không tự làm process fail; threshold mới định nghĩa acceptance/exit gate. ([Checks](https://grafana.com/docs/k6/latest/using-k6/checks/), [Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) — truy cập 2026-07-14)

### Câu 3. JavaScript nghĩa là dùng mọi npm package?

**Trả lời:** Không; k6 không chạy Node.js runtime và package compatibility phải được kiểm tra. ([Modules](https://grafana.com/docs/k6/latest/using-k6/modules/) — truy cập 2026-07-14)

### Câu 4. Vì sao không gọi k6 là “tốt nhất” khi điểm cao nhất?

**Trả lời:** Điểm chỉ dựa DOC/ASSUMPTION và có thể che blocker/workload error; chưa có EXP, calibration hay comparison trên cùng logical EShop workload.

### Câu 5. Có browser module thì nên phát toàn bộ tải bằng browser?

**Trả lời:** Không thể suy ra; browser và protocol VU phục vụ mục tiêu/footprint khác, capacity cần đo. **[CẦN THỰC NGHIỆM]**

</details>

## 7.5. Locust

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
| Cost & access (8%) | 5/5 | MIT/local OSS, account không bắt buộc. **DOC** ([repo](https://github.com/locustio/locust) — truy cập 2026-07-14); **Trace:** LO-DOC-01, LO-DOC-02. |
| Learning curve (8%) | 4/5 | Dễ với Python; lifecycle/gevent/distributed cần học. **DOC + ASSUMPTION** ([locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14); **Trace:** LO-DOC-01, LO-DOC-02. |
| EShop fit (15%) | 5/5 | HttpSession/cookie/state/Python correlation. **DOC + ASSUMPTION** ([locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14); **Trace:** LO-DOC-01, LO-DOC-02. |
| Multi-step journey (12%) | 5/5 | Sequential task/lifecycle/per-user state. **DOC** ([locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14); **Trace:** LO-DOC-01, LO-DOC-02. |
| Workload control (10%) | 4/5 | Users/spawn/custom shape; open-rate caveat. **DOC + ASSUMPTION** ([shapes](https://docs.locust.io/en/stable/configuration.html#custom-load-shapes) — truy cập 2026-07-14); **Trace:** LO-DOC-01, LO-DOC-02. |
| Assertions/checks (8%) | 4/5 | catch_response mạnh, SLO gate cần hook. **DOC** ([validation](https://docs.locust.io/en/stable/writing-a-locustfile.html#validating-responses), [headless](https://docs.locust.io/en/stable/running-without-web-ui.html) — truy cập 2026-07-14); **Trace:** LO-DOC-01, LO-DOC-02. |
| Reporting (8%) | 4/5 | Live UI + multi-file CSV; local polished HTML không là core path. **DOC** ([configuration](https://docs.locust.io/en/stable/configuration.html) — truy cập 2026-07-14); **Trace:** LO-DOC-01, LO-DOC-02. |
| CI/CD (7%) | 4/5 | Headless/exit/Actions; custom threshold glue. **DOC** ([headless](https://docs.locust.io/en/stable/running-without-web-ui.html) — truy cập 2026-07-14); **Trace:** LO-DOC-01, LO-DOC-02. |
| Reproducibility (7%) | 5/5 | Python/lock/config/CSV dễ version; pin workers/deps. **DOC + ASSUMPTION**; **Trace:** LO-DOC-01, LO-DOC-02. |
| Local/offline (5%) | 5/5 | Runner/UI/workers local; cache dependencies. **DOC + ASSUMPTION** ([docs](https://docs.locust.io/en/stable/) — truy cập 2026-07-14); **Trace:** LO-DOC-01, LO-DOC-02. |
| AI-assisted potential (7%) | 5/5 | Python/HAR dễ draft/audit; tool không AI. **ASSUMPTION** ([locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) — truy cập 2026-07-14); **Trace:** LO-DOC-01, LO-DOC-02. |
| Classroom suitability (5%) | 4/5 | UI/Python tốt; process/custom gate cần thời gian. **ASSUMPTION**; **Trace:** LO-DOC-01, LO-DOC-02. |
| Community (0%) | 5/5 | Current official docs, active repo, Discussions/Discord; không vào Weighted Score. **DOC** ([repo](https://github.com/locustio/locust), [docs](https://docs.locust.io/en/stable/) — truy cập 2026-07-14); **Trace:** LO-DOC-01, LO-DOC-02. |

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

## 7.6. Gatling

**1. Tổng quan.** **[DOC]** Gatling là performance-testing engine/platform do Gatling Corp duy trì. Community engine hỗ trợ Java, JavaScript, TypeScript, Kotlin và Scala; không còn đúng nếu mô tả Gatling “chỉ có Scala”. ([Gatling repository](https://github.com/gatling/gatling), [Gatling documentation](https://docs.gatling.io/) — truy cập 2026-07-14)

**2. Cost và licence.** **[DOC]** Main open-source project dùng Apache-2.0, nhưng bundled Highcharts report module có licence riêng với phạm vi dùng/sửa giới hạn; Enterprise components có điều khoản riêng. Community chạy local miễn phí. Current Enterprise pricing niêm yết Basic từ 89 EUR/tháng khi annual hoặc 99 EUR monthly, Team từ 356/396 EUR và custom Enterprise; giá phải re-check trước nộp. ([Project licences](https://docs.gatling.io/project/licenses/project-licenses/), [Gatling pricing](https://gatling.io/pricing) — truy cập 2026-07-14) Trial self-service là 14 ngày với hạn mức chính thức. ([Trial plan](https://docs.gatling.io/evaluate-enterprise/trial-plan/) — truy cập 2026-07-14)

**3. Installation và platform support.** **[DOC]** Gatling chạy trên JVM; JVM SDK hỗ trợ Java/Kotlin/Scala và build tools Maven/Gradle/sbt. Current install docs hỗ trợ OpenJDK LTS 11–25. Current JS/TS route yêu cầu Node.js 24+ LTS và npm 11+. Official docs đang có **documentation conflict**: trang install vẫn nói JavaScript SDK chỉ bao phủ HTTP, trong khi current official guides/reference đã minh họa JS/TS cho gRPC, SSE và MQTT qua các protocol modules. Vì vậy không suy ra protocol parity từ một trang; phải pin Gatling version, package/module và edition của lab. npm, build-tool project và standalone bundle đều được tài liệu hóa; bundle phù hợp offline/firewall. ([Install local](https://docs.gatling.io/reference/deploy/install-local/), [gRPC JS/TS guide](https://docs.gatling.io/guides/use-cases/grpc-js/), [SSE reference](https://docs.gatling.io/reference/script/sse/), [MQTT reference](https://docs.gatling.io/reference/script/mqtt/protocol/) — truy cập 2026-07-14)

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

- **[DOC]** Official install page và current protocol guides không nhất quán về phạm vi JS/TS; protocol/module/edition parity phải được pin và smoke-test, không được ghi categorical “HTTP-only”. ([Install](https://docs.gatling.io/reference/deploy/install-local/), [gRPC JS/TS](https://docs.gatling.io/guides/use-cases/grpc-js/), [SSE](https://docs.gatling.io/reference/script/sse/), [MQTT](https://docs.gatling.io/reference/script/mqtt/protocol/) — truy cập 2026-07-14)
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
| Cost & access (8%) | 4/5 | Free Community, nhưng Highcharts nuance/Enterprise cost. **DOC** ([licences](https://docs.gatling.io/project/licenses/project-licenses/), [pricing](https://gatling.io/pricing) — truy cập 2026-07-14); **Trace:** GA-DOC-01, GA-DOC-02. |
| Learning curve (8%) | 3/5 | JVM/npm/build + typed DSL. **DOC + ASSUMPTION** ([install](https://docs.gatling.io/reference/deploy/install-local/) — truy cập 2026-07-14); **Trace:** GA-DOC-01, GA-DOC-02. |
| EShop fit (15%) | 5/5 | HTTP/session/feeders/checks. **DOC + ASSUMPTION** ([session](https://docs.gatling.io/concepts/session/api/), [feeders](https://docs.gatling.io/concepts/session/feeders/) — truy cập 2026-07-14); **Trace:** GA-DOC-01, GA-DOC-02. |
| Multi-step journey (12%) | 5/5 | saveAs/session/reusable chains. **DOC** ([checks](https://docs.gatling.io/concepts/checks/) — truy cập 2026-07-14); **Trace:** GA-DOC-01, GA-DOC-02. |
| Workload control (10%) | 5/5 | Rich explicit open/closed profiles. **DOC** ([injection](https://docs.gatling.io/concepts/injection/) — truy cập 2026-07-14); **Trace:** GA-DOC-01, GA-DOC-02. |
| Assertions/checks (8%) | 5/5 | Request checks + global/detail assertions/error exit. **DOC** ([assertions](https://docs.gatling.io/concepts/assertions/) — truy cập 2026-07-14); **Trace:** GA-DOC-01, GA-DOC-02. |
| Reporting (8%) | 4/5 | Strong static HTML; raw log not stable contract. **DOC** ([reports](https://docs.gatling.io/reference/stats/reports/oss/), [FAQ](https://docs.gatling.io/tutorials/faq/) — truy cập 2026-07-14); **Trace:** GA-DOC-01, GA-DOC-02. |
| CI/CD (7%) | 5/5 | Build-tool/npm CLI + assertion gate. **DOC** ([JS CLI](https://docs.gatling.io/integrations/build-tools/js-cli/) — truy cập 2026-07-14); **Trace:** GA-DOC-01, GA-DOC-02. |
| Reproducibility (7%) | 5/5 | Typed code/build lock/static report. **DOC + ASSUMPTION**; **Trace:** GA-DOC-01, GA-DOC-02. |
| Local/offline (5%) | 5/5 | Community local/standalone offline path. **DOC** ([install](https://docs.gatling.io/reference/deploy/install-local/) — truy cập 2026-07-14); **Trace:** GA-DOC-01, GA-DOC-02. |
| AI-assisted potential (7%) | 4/5 | Code + official Enterprise AI/MCP, gated và human-reviewed. **DOC + ASSUMPTION** ([AI](https://docs.gatling.io/ai/), [MCP](https://gatling.io/product/mcp) — truy cập 2026-07-14); **Trace:** GA-DOC-01, GA-DOC-02. |
| Classroom suitability (5%) | 3/5 | Learning value cao nhưng setup/DSL nặng hơn. **ASSUMPTION**; **Trace:** GA-DOC-01, GA-DOC-02. |
| Community (0%) | 5/5 | Current official docs, repo và forum; không vào Weighted Score. **DOC** ([docs](https://docs.gatling.io/), [repo](https://github.com/gatling/gatling) — truy cập 2026-07-14); **Trace:** GA-DOC-01, GA-DOC-02. |

**Weighted Score provisional: 90.2/100.** Chưa hiệu chỉnh bằng EXP.

**16. Kết luận sơ bộ.** **Shortlist.** Gatling có workload/assertion capability rất mạnh và là đối chứng quan trọng; chưa chọn pair chính vì typed/build learning path có thể giảm classroom throughput và vai trò code-first trùng k6. Không kết luận Gatling yếu hơn tuyệt đối.

**17. Câu hỏi phản biện.**

<details>
<summary><strong>Câu hỏi phản biện</strong></summary>

### Câu 1. Vì sao không chọn Gatling?

**Trả lời:** Không phải do capability; pair ưu tiên complementarity và activity time. Cần measured 25-minute trial trước khi loại khỏi final shortlist.

### Câu 2. Gatling hiện chỉ viết Scala phải không?

**Trả lời:** Không; official docs hỗ trợ Java, Kotlin, Scala, JavaScript và TypeScript. Protocol parity phải đọc theo pinned version/module/edition vì install page nói JS chỉ HTTP nhưng current official gRPC/SSE/MQTT pages lại có JS/TS examples; tài liệu này ghi nhận conflict thay vì chọn một claim categorical. ([Install](https://docs.gatling.io/reference/deploy/install-local/), [gRPC JS/TS](https://docs.gatling.io/guides/use-cases/grpc-js/), [SSE](https://docs.gatling.io/reference/script/sse/), [MQTT](https://docs.gatling.io/reference/script/mqtt/protocol/) — truy cập 2026-07-14)

### Câu 3. Có thể parse simulation.log làm raw integration ổn định?

**Trả lời:** Không; official FAQ gọi nó là undocumented implementation detail có thể đổi. ([FAQ](https://docs.gatling.io/tutorials/faq/) — truy cập 2026-07-14)

### Câu 4. Toàn bộ Gatling có Apache-2.0 không?

**Trả lời:** Không; main project là Apache-2.0 nhưng Highcharts report module và Enterprise components có licence riêng. ([Licences](https://docs.gatling.io/project/licenses/project-licenses/) — truy cập 2026-07-14)

</details>

## 7.7. Loader.io

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
| Cost & access | 8% | 3 | Free plan có quota công khai, nhưng bắt buộc account và verified public host nên access có điều kiện | DOC + ASSUMPTION; **Trace:** LI-DOC-01, LI-DOC-02. |
| Learning curve | 8% | 5 | Web/API workflow ngắn | ASSUMPTION từ DOC; **Trace:** LI-DOC-01, LI-DOC-02. |
| EShop fit | 15% | 3 | Public HTTP tốt; local/assertion hạn chế | DOC + ASSUMPTION; **Trace:** LI-DOC-01, LI-DOC-02. |
| Multi-step journey & state | 12% | 3 | URL/cookie/header variable; Free 2 URL | DOC; **Trace:** LI-DOC-01, LI-DOC-02. |
| Workload model & scalability | 10% | 4 | Per-test/per-second/maintain cloud | DOC; **Trace:** LI-DOC-01, LI-DOC-02. |
| Assertions & business validation | 8% | 2 | Status/error/timeout, không body check | DOC; **Trace:** LI-DOC-01, LI-DOC-02. |
| Metrics & reporting | 8% | 3 | Avg/min/max/errors; no documented percentile/raw | DOC + ASSUMPTION; **Trace:** LI-DOC-01, LI-DOC-02. |
| CI/CD & automation | 7% | 4 | API/webhooks; custom gate/docs cũ | DOC + ASSUMPTION; **Trace:** LI-DOC-01, LI-DOC-02. |
| Reproducibility | 7% | 3 | JSON lưu được; SaaS/IP/state biến động | DOC + ASSUMPTION; **Trace:** LI-DOC-01, LI-DOC-02. |
| Local/offline | 5% | 1 | AWS generators cần public target | DOC; **Trace:** LI-DOC-01, LI-DOC-02. |
| AI-assisted potential | 7% | 3 | JSON dễ draft; không native/capability mỏng | ASSUMPTION; **Trace:** LI-DOC-01, LI-DOC-02. |
| Classroom suitability | 5% | 4 | Free/easy; public host governance | ASSUMPTION; **Trace:** LI-DOC-01, LI-DOC-02. |
| Community | 0% | 3 | API/docs public nhưng nhiều Help articles cũ ([Docs](https://support.loader.io/collection/3-loaderio-docs) — truy cập 2026-07-14) | DOC; không tính; **Trace:** LI-DOC-01, LI-DOC-02. |

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

## 7.8. Siege

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
- **Command:** đặt `logfile = [ARTIFACT_PATH]` trong isolated `.siegerc` nếu cần custom path, rồi chạy `siege -l -c 2 -r 5 -b "[VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]"`. `-l/--log` chỉ bật logging, không nhận path argument. ([Manual](https://www.joedog.org/siege/manual), [official `siegerc.in`](https://github.com/JoeDog/siege/blob/master/doc/siegerc.in) — truy cập 2026-07-14)
- **Expected result:** dự kiến 10 transactions, status theo contract, không transport/failure ở smoke load; chưa có latency giả định.
- **Evidence:** version/provenance, `.siegerc`, command, stdout/stderr/exit, log/hash, cookie isolation, EShop commit, time/timezone, client/SUT resources.
- **Possible errors:** native Windows; container routing; TLS/OpenSSL; stale cookie; 3xx false-success; HTTP/1.1 limitation; file descriptor; encoding; client saturation.
- **Success criteria:** count/status đúng, không transport error, cookie sạch, generator headroom, artifacts đủ rerun; không đặt p95 vì standard report không có.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Evidence |
|---|---:|---:|---|
| Cost & access | 8% | 5 | GPL/source mở. **[DOC]**; **Trace:** SI-DOC-01, SI-DOC-02. |
| Learning curve | 8% | 4 | CLI/URL file dễ; POSIX setup. **[DOC]**; **Trace:** SI-DOC-01, SI-DOC-02. |
| EShop fit | 15% | 3 | POST/cookie/URLs, thiếu correlation. **[DOC + ASSUMPTION]**; **Trace:** SI-DOC-01, SI-DOC-02. |
| Multi-step journey | 12% | 2 | Sequence tĩnh. **[DOC + ASSUMPTION]**; **Trace:** SI-DOC-01, SI-DOC-02. |
| Workload control | 10% | 3 | Users/duration/delay/random, không stage. **[DOC]**; **Trace:** SI-DOC-01, SI-DOC-02. |
| Assertions/checks | 8% | 2 | `<400`, không business check. **[DOC + ASSUMPTION]**; **Trace:** SI-DOC-01, SI-DOC-02. |
| Reporting | 8% | 2 | Aggregate, thiếu percentile/raw. **[DOC]**; **Trace:** SI-DOC-01, SI-DOC-02. |
| CI/CD | 7% | 2 | Wrapper/gate/cookie isolation. **[DOC + ASSUMPTION]**; **Trace:** SI-DOC-01, SI-DOC-02. |
| Reproducibility | 7% | 4 | Config pin được; kiểm soát cookies. **[DOC]**; **Trace:** SI-DOC-01, SI-DOC-02. |
| Local/offline | 5% | 5 | Không SaaS/Dockerfile. **[DOC]**; **Trace:** SI-DOC-01, SI-DOC-02. |
| AI-assisted potential | 7% | 3 | Hữu ích cho config/parser; audit semantics. **[DOC + ASSUMPTION]**; **Trace:** SI-DOC-01, SI-DOC-02. |
| Classroom suitability | 5% | 4 | Trực quan nếu setup sẵn. **[DOC + ASSUMPTION]**; **Trace:** SI-DOC-01, SI-DOC-02. |
| Community | 0% | 3 | Manual/FAQ/repo công khai; không ảnh hưởng tổng. [Repository](https://github.com/JoeDog/siege) (truy cập 2026-07-14). **[DOC]**; **Trace:** SI-DOC-01, SI-DOC-02. |

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

## 7.9. Vegeta

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
| Cost & access | 8% | 5 | MIT/source/releases mở. **[DOC]**; **Trace:** VE-DOC-01, VE-DOC-02. |
| Learning curve | 8% | 4 | CLI rõ; Go chỉ cho nâng cao. **[DOC]**; **Trace:** VE-DOC-01, VE-DOC-02. |
| EShop fit | 15% | 3 | API tốt, session yếu. **[DOC + ASSUMPTION]**; **Trace:** VE-DOC-01, VE-DOC-02. |
| Multi-step journey | 12% | 1 | Targets độc lập. **[DOC + ASSUMPTION]**; **Trace:** VE-DOC-01, VE-DOC-02. |
| Workload control | 10% | 4 | Rate/workers + Go Pacers. **[DOC]**; **Trace:** VE-DOC-01, VE-DOC-02. |
| Assertions/checks | 8% | 1 | Protocol success, không body check. **[DOC + ASSUMPTION]**; **Trace:** VE-DOC-01, VE-DOC-02. |
| Reporting | 8% | 5 | Raw/JSON/CSV/hist/HTML/Prometheus. **[DOC]**; **Trace:** VE-DOC-01, VE-DOC-02. |
| CI/CD | 7% | 3 | Pipeline tốt, gate ngoài. **[DOC + ASSUMPTION]**; **Trace:** VE-DOC-01, VE-DOC-02. |
| Reproducibility | 7% | 5 | Version/target/rate/raw pin được. **[DOC]**; **Trace:** VE-DOC-01, VE-DOC-02. |
| Local/offline | 5% | 5 | Binary/Dockerfile, không SaaS. **[DOC]**; **Trace:** VE-DOC-01, VE-DOC-02. |
| AI-assisted potential | 7% | 4 | Target/policy/report dễ hỗ trợ. **[DOC + ASSUMPTION]**; **Trace:** VE-DOC-01, VE-DOC-02. |
| Classroom suitability | 5% | 5 | Artifact pipeline trực quan. **[DOC + ASSUMPTION]**; **Trace:** VE-DOC-01, VE-DOC-02. |
| Community | 0% | 4 | Repo/docs/releases công khai; không ảnh hưởng tổng. [Repository](https://github.com/tsenart/vegeta) (truy cập 2026-07-14). **[DOC]**; **Trace:** VE-DOC-01, VE-DOC-02. |

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

## 7.10. wrk

> **Trạng thái bằng chứng:** chỉ **[DOC]**, **[DOC + ASSUMPTION]**, **[ASSUMPTION]** và kế hoạch chưa chạy; ngày chốt 2026-07-14.

### 1. Tổng quan

`wrk` là HTTP benchmarking CLI do Will Glozer (`wg`) duy trì, tối ưu tạo tải trên máy đa lõi bằng epoll/kqueue và mở rộng request/response qua Lua. [Repository/README](https://github.com/wg/wrk), [maintainer](https://github.com/wg) (truy cập 2026-07-14). **[DOC]**

### 2. Cost và licence

Source mở theo **Modified Apache 2.0 License Version 2.0.1 (February 2015)**, không cần tài khoản/trial; cần giữ đúng qualifier license. [LICENSE](https://raw.githubusercontent.com/wg/wrk/master/LICENSE) (truy cập 2026-07-14). **[DOC]**

### 3. Installation và platform support

Hỗ trợ phần lớn hệ kiểu UNIX; build bằng GNU make (`gmake` trên BSD), LuaJIT và OpenSSL, có dependency bundle/system option. INSTALL không tuyên bố native Windows, nên lớp Windows cần WSL/VM/container tự pin. [INSTALL](https://github.com/wg/wrk/blob/master/INSTALL) (truy cập 2026-07-14). **[DOC]**

### 4. Scripting hoặc configuration model

CLI điều khiển workload; file Lua có hooks `setup/init/delay/request/response/done`, dễ version-control. Mỗi thread có một Lua environment; response callback làm giảm khả năng phát tải. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC]**

### 5. Workload capabilities

`-t` threads, `-c` connections, `-d` duration, timeout, header, latency và Lua delay/request. Mô hình chính là fixed connections trong duration; không có staged arrival/ramp, weighted multi-scenario hay distributed controller trong CLI. State Lua per-thread không tương ứng VU/connection khi một thread quản lý nhiều connections, nên correlation login/cart dễ trộn session. [README options](https://github.com/wg/wrk#command-line-options), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 6. Assertions và validation

Lua `response(status, headers, body)` cho phép đếm/ghi custom check, nhưng không có assertion DSL/SLA threshold contract native. Business pass/fail và CI exit cần script/wrapper được review. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 7. Metrics và reporting

Console có latency/Req-Sec average, stdev, max, total, RPS, transfer/sec; `--latency` thêm distribution. Hook `done` đọc percentile tùy ý, histogram value/count và connect/read/write/status/timeout errors; artifact machine-readable chuẩn phải tự xây. [README](https://github.com/wg/wrk), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC]**

### 8. CI/CD và automation

CLI/Lua hợp pipeline và chạy local/offline; threshold, stable JSON/CSV, exit policy và custom container cần nhóm cung cấp/pin. Trang Releases không công bố package release, nên phải lưu commit/tag/binary provenance. [Releases](https://github.com/wg/wrk/releases), [INSTALL](https://github.com/wg/wrk/blob/master/INSTALL) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 9. EShop suitability

Tốt cho product/catalog API cô lập và header/auth tĩnh. Lua có thể biến đổi request/đọc response nhưng session state per-thread không an toàn để mặc định mô hình login→cart→checkout ở concurrency cao. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 10. AI-assisted potential

AI có thể sinh Lua, parser, workload matrix và Failure Mode checks; phải audit thread-vs-connection state, callback overhead, secret, HTTP formatting và exit policy. Script AI chưa audit không được coi là đúng. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 11. Classroom suitability

CLI cơ bản có thể demo trong 25 phút nếu đã build sẵn; build Windows/WSL và Lua state model khiến buổi tự cài+tạo journey khó vừa timebox. [INSTALL](https://github.com/wg/wrk/blob/master/INSTALL), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 12. Điểm mạnh trong phạm vi seminar

Tạo tải endpoint hiệu quả, latency distribution/histogram API tốt, Lua linh hoạt cho request-level instrumentation. [README](https://github.com/wg/wrk), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC]**

### 13. Hạn chế trong phạm vi seminar

Không có business-VU/session model, staged rate, SLA gate hoặc report artifact chuẩn; response processing giảm load capacity. Đây là ranh giới endpoint benchmark, không phải nhận xét tuyệt đối về chất lượng. [README](https://github.com/wg/wrk), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 14. Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

- **Mục tiêu:** phát GET nhỏ, thu latency distribution và quan sát HTTP status bằng một Lua response callback đã review, trong khi client chưa bão hòa.
- **Prerequisites:** `[VERIFIED_BASE_URL]`, `[VERIFIED_PRODUCT_PATH]`, `[EXPECTED_STATUS]`, WSL/Linux/container và monitoring đã xác minh. **[ASSUMPTION]**
- **Installation/setup:** build theo [INSTALL](https://github.com/wg/wrk/blob/master/INSTALL); lưu commit, compiler, LuaJIT/OpenSSL provenance và version. Tạo/version-control `status_check.lua` dùng official `response(status, headers, body)` callback và `setup`/thread handles để aggregate expected/unexpected status; human-review aggregation trước khi chạy. `response()` làm giảm load capacity nên chỉ dùng ở smoke này, không dùng để suy ra generator ceiling. ([SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) — truy cập 2026-07-14)
- **Một request:** `GET [VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]`.
- **Command:** `wrk -t2 -c4 -d10s --latency -s status_check.lua "[VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]"` theo [README](https://github.com/wg/wrk) và [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14).
- **Expected result:** duration 10s, có RPS/latency distribution, status counters và không socket error ở smoke load; không dự đoán số đo.
- **Evidence:** binary hash/commit, `status_check.lua` + hash/review record, command, stdout/stderr/exit, aggregated status counters, EShop commit, timestamp/timezone và CPU/RAM/network client/SUT.
- **Possible errors:** build/OpenSSL/LuaJIT; WSL routing; TLS/timeout/file descriptor; CPU saturation; nhầm threads với VU; Lua aggregation sai; response callback overhead; wrapper không biến unexpected status thành failed gate.
- **Success criteria:** duration/connections đúng, `unexpected_status=0`, socket error bằng 0, client còn headroom và evidence đủ rerun. Vì wrk không có native SLA exit contract, negative status phải làm reviewed wrapper/parser fail trước khi claim CI gate.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Evidence |
|---|---:|---:|---|
| Cost & access | 8% | 5 | Source/license mở. **[DOC]**; **Trace:** WR-DOC-01, WR-DOC-02. |
| Learning curve | 8% | 3 | CLI dễ, build/Lua trung bình. **[DOC]**; **Trace:** WR-DOC-01, WR-DOC-02. |
| EShop fit | 15% | 2 | Endpoint tốt, journey yếu. **[DOC + ASSUMPTION]**; **Trace:** WR-DOC-01, WR-DOC-02. |
| Multi-step journey | 12% | 2 | Lua nhưng state per-thread. **[DOC + ASSUMPTION]**; **Trace:** WR-DOC-01, WR-DOC-02. |
| Workload control | 10% | 3 | Threads/connections/duration/delay. **[DOC]**; **Trace:** WR-DOC-01, WR-DOC-02. |
| Assertions/checks | 8% | 2 | Custom Lua, không contract native. **[DOC + ASSUMPTION]**; **Trace:** WR-DOC-01, WR-DOC-02. |
| Reporting | 8% | 3 | Console/percentile/histogram API. **[DOC]**; **Trace:** WR-DOC-01, WR-DOC-02. |
| CI/CD | 7% | 2 | Wrapper/gate/artifact tự xây. **[DOC + ASSUMPTION]**; **Trace:** WR-DOC-01, WR-DOC-02. |
| Reproducibility | 7% | 4 | Lệnh/Lua pin được; pin build. **[DOC]**; **Trace:** WR-DOC-01, WR-DOC-02. |
| Local/offline | 5% | 5 | Không SaaS. **[DOC]**; **Trace:** WR-DOC-01, WR-DOC-02. |
| AI-assisted potential | 7% | 3 | Lua hữu ích nhưng audit sâu. **[DOC + ASSUMPTION]**; **Trace:** WR-DOC-01, WR-DOC-02. |
| Classroom suitability | 5% | 3 | Demo CLI được, setup/Lua tốn thời gian. **[DOC + ASSUMPTION]**; **Trace:** WR-DOC-01, WR-DOC-02. |
| Community | 0% | 4 | Repo/issues và docs công khai; không ảnh hưởng tổng. [Repository](https://github.com/wg/wrk) (truy cập 2026-07-14). **[DOC]**; **Trace:** WR-DOC-01, WR-DOC-02. |

**Tổng có trọng số: 58.2/100**; Community 0% không tham gia công thức.

### 16. Kết luận sơ bộ

**Supporting benchmark tool.** Dùng đo endpoint khi cần generator hiệu quả/Lua nhỏ, không thay công cụ journey.

### 17. Câu hỏi phản biện

<details>
<summary>Phản biện và trả lời</summary>

1. **Có Lua là đủ login–cart–checkout?** Không: state per-thread, một thread có nhiều connection nên correlation per-user không được bảo đảm. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
2. **RPS cao hơn chứng minh SUT tốt hơn?** Không nếu callback/client CPU/network bão hòa hoặc workload khác; phải quan sát generator. [README](https://github.com/wg/wrk), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC]**
3. **CI xanh nghĩa là SLA đạt?** Không; CLI không có threshold contract mặc định, cần parser/policy exit. [README options](https://github.com/wg/wrk#command-line-options) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

</details>

## 7.11. NeoLoad

### 1. Tổng quan

NeoLoad là commercial performance platform của Tricentis, có protocol + RealBrowser, no-code/as-code, desktop/Web, CLI/API và cloud/on-prem execution ([NeoLoad](https://www.tricentis.com/products/performance-testing-neoload) — truy cập 2026-07-14). Evidence: `DOC`.

### 2. Cost và licence

Giá niêm yết từ 20.000 USD/năm, gồm 300 VU; có “Try for free” và Free Edition. Không-key mode chỉ design/analyze, không launch; exact current Free run cap không rõ trong public docs: `[CẦN XÁC MINH ENTITLEMENT]` ([Pricing](https://www.tricentis.com/products/performance-testing-neoload/pricing), [Manage licenses](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/manage_licenses.htm), [Quick Start](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/quick_start_guide.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 3. Installation và platform support

Controller/components hỗ trợ Windows/Linux/macOS theo matrix và Java 21; có built-in Load Generator/Monitoring Agent, remote agents, official container/Kubernetes deployment ([System requirements](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/system_requirements.htm), [Install Controller](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/install_the_controller.htm), [Deployment](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/deployment_considerations.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 4. Scripting hoặc configuration model

Record/import API → User Paths → Populations → Scenarios. User Path có Init/Actions/End; YAML/JSON as-code trộn với `.nlp`; JavaScript Action mở rộng logic. Git-friendly nhất khi commit YAML/data schema/environment overrides, không commit secret ([Get started](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/get_started.htm), [As-code](https://docs.tricentis.com/neoload-2026.1/en-us/content/user_guides.htm/neoload_as_code/executing_yaml_based_projects.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 5. Workload capabilities

Populations trộn User Paths theo %, có pacing; policies Constant/Ramp-up/Peaks/Custom và distributed agents/infrastructure override. Variables hỗ trợ CSV, unique/sequential/random; extractors/automatic dynamic-parameter handling làm correlation/session. Public section được kiểm tra chưa chứng minh open arrival-rate executor tương đương: `[CẦN XÁC MINH]` ([Populations](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/create_populations.htm), [Load policy](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/load_variation_policy.htm), [Variables](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/variables_and_fuctions.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 6. Assertions và validation

Validation kiểm tra duration, content length/body, XPath, JSONPath; SLA profiles đặt threshold và test status ([Validation](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/validation.htm), [SLA profiles](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/service_level_agreement_sla_profiles.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 7. Metrics và reporting

Test Summary có request/s, error rate, min/avg/max, stddev, throughput và ba percentile cấu hình 0,1–99,9. CLI xuất raw transactions, HTML/PDF/XML và SLA JUnit XML ([Test Summary](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/test_summary.htm), [Controller CLI](https://docs.tricentis.com/neoload-2026.1/en-us/content/get_started/start_the_controller.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 8. CI/CD và automation

`NeoLoadCmd -project ... -launch ... -noGUI -report ... -exportRaw ...`; exit `0=PASSED`, `1=FAILED` do SLA, `2=ERROR`; `-exitCodeFailIgnore` có thể ép 0 nên pipeline phải cấm nếu không được review. Có Jenkins và APIs ([Controller CLI](https://docs.tricentis.com/neoload-2026.1/en-us/content/get_started/start_the_controller.htm), [Jenkins](https://docs.tricentis.com/neoload-latest/en-us/content/user_guides.htm/integrate_with_third_party_tools/jenkins/jenkins.htm), [APIs](https://docs.tricentis.com/neoload-latest/en-us/content/apis/api_overview.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 9. EShop suitability

Rất mạnh cho Web/API journey, login/token, data, population mix, validation/SLA, report và CI; local agents có thể gọi EShop private. Cost/entitlement làm giảm seminar fit, không giảm enterprise capability. Evidence: `DOC` + fit `ASSUMPTION`.

### 10. AI-assisted potential

Product page công bố Agentic Performance Testing, AI Chat/MCP và Augmented Analysis. YAML/JS thuận lợi human audit; availability theo plan/data residency và correctness vẫn cần xác minh. Nghiên cứu không gọi NeoLoad AI ([NeoLoad](https://www.tricentis.com/products/performance-testing-neoload) — truy cập 2026-07-14). Evidence: `DOC` + governance `ASSUMPTION`.

### 11. Classroom suitability

GUI/no-code dễ trình diễn, nhưng entry price, entitlement, Java/resources và account làm khó tái lập toàn lớp trong 25 phút; cần pre-install/license. `[CẦN THỰC NGHIỆM]`. Evidence: `ASSUMPTION` từ DOC.

### 12. Điểm mạnh trong phạm vi seminar

GUI + as-code; validation/SLA; explicit CI exit codes; configurable percentiles/raw export; agents/container; native AI ([NeoLoad docs](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/get_started.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 13. Hạn chế trong phạm vi seminar

Giá từ 20.000 USD/năm; Free cap chưa rõ; environment/license nặng; arrival equivalence cần xác minh; AI/cloud tăng governance/data dependency. Evidence: `DOC`/`ASSUMPTION` đã đánh dấu.

### 14. Smoke Test Plan

**[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN]**

- **Mục tiêu:** 1 GET, validation/SLA, raw/HTML/JUnit và exit code.
- **Prerequisites:** supported OS/Java, installer checksum, Free/trial entitlement screenshot redacted, `[VERIFIED_BASE_URL]`, quyền test.
- **Installation/setup:** cài Controller; User Path GET + validation; Population 1; Scenario `Smoke`, 1 VU/1 iteration; SLA rõ.
- **Request:** `GET [VERIFIED_BASE_URL]/[VERIFIED_READ_ONLY_PATH]`.
- **Command/config:** `NeoLoadCmd -project ...\smoke.nlp -launch Smoke -noGUI -report ...\smoke.html -exportRaw ...\raw.csv -SLAJUnitReport ...\junit.xml` ([CLI](https://docs.tricentis.com/neoload-2026.1/en-us/content/get_started/start_the_controller.htm) — truy cập 2026-07-14).
- **Kết quả mong đợi:** exit 0, validation/SLA pass và ba artefact; chưa quan sát.
- **Evidence:** version/entitlement, `.nlp`/YAML, command/env, stdout/stderr/exit, HTML/raw/JUnit.
- **Lỗi có thể gặp:** no license (exit 2), Java/resource, agent certificate, TLS/proxy, wrong extraction/validation, report path.
- **Tiêu chí thành công:** request + validation/SLA + artefacts đạt; marker/SLA sai phải cho exit 1; không dùng `-exitCodeFailIgnore`.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Lý do | Evidence |
|---|---:|---:|---|---|
| Cost & access | 8% | 2 | 20k USD/year; free cap cần xác minh | DOC; **Trace:** NL-DOC-01, NL-DOC-02. |
| Learning curve | 8% | 4 | GUI/no-code + as-code; infra vẫn phức tạp | ASSUMPTION từ DOC; **Trace:** NL-DOC-01, NL-DOC-02. |
| EShop fit | 15% | 5 | Full journey/state/data/SLA | DOC + ASSUMPTION; **Trace:** NL-DOC-01, NL-DOC-02. |
| Multi-step journey & state | 12% | 5 | Init/Actions/End/extractor/data | DOC; **Trace:** NL-DOC-01, NL-DOC-02. |
| Workload model & scalability | 10% | 4 | Policies/agents; arrival gap | DOC + ASSUMPTION; **Trace:** NL-DOC-01, NL-DOC-02. |
| Assertions & business validation | 8% | 5 | Body/XPath/JSONPath/SLA | DOC; **Trace:** NL-DOC-01, NL-DOC-02. |
| Metrics & reporting | 8% | 5 | Percentiles/raw/multi-format | DOC; **Trace:** NL-DOC-01, NL-DOC-02. |
| CI/CD & automation | 7% | 5 | Headless/JUnit/Jenkins/API/exit 0-1-2 | DOC; **Trace:** NL-DOC-01, NL-DOC-02. |
| Reproducibility | 7% | 5 | YAML/JSON/Git/CLI overrides | DOC; **Trace:** NL-DOC-01, NL-DOC-02. |
| Local/offline | 5% | 4 | On-prem agents/offline lease; cloud features ngoài | DOC + ASSUMPTION; **Trace:** NL-DOC-01, NL-DOC-02. |
| AI-assisted potential | 7% | 5 | Native agentic/AI/augmented + text artefacts | DOC + ASSUMPTION; **Trace:** NL-DOC-01, NL-DOC-02. |
| Classroom suitability | 5% | 2 | Cost/license/resource khó nhân rộng | ASSUMPTION; **Trace:** NL-DOC-01, NL-DOC-02. |
| Community | 0% | 4 | Current 2026 docs/API/support ecosystem ([Docs](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/get_started.htm) — truy cập 2026-07-14) | DOC; không tính; **Trace:** NL-DOC-01, NL-DOC-02. |

**Weighted Score provisional: 87,6/100; 0 EXP.**

### 16. Kết luận sơ bộ

**Survey-only** / enterprise alternative. Capability mạnh nhưng không vượt access/reproducibility blocker của live seminar.

### 17. Câu hỏi phản biện

<details>
<summary><strong>Câu hỏi phản biện NeoLoad</strong></summary>

1. **Free có bao nhiêu VU?** Current public docs không cho cap đủ chắc; phải dùng entitlement screenshot, không số từ version cũ.
2. **Giá cao mà điểm gần JMeter có thiên vị?** Ma trận tách capability khỏi cost/classroom; classification vẫn Survey-only.
3. **Ramp 100 VU/phút = 100 arrivals/phút?** Không được đồng nhất; concurrency ramp khác arrival, cần experiment.
4. **Native AI làm script đúng?** Không; vẫn phải audit extraction, workload, SLA và raw results.

</details>

## 7.12. ApacheBench

> **Trạng thái bằng chứng:** chỉ **[DOC]**, **[DOC + ASSUMPTION]**, **[ASSUMPTION]** và kế hoạch chưa chạy; ngày chốt 2026-07-14.

### 1. Tổng quan

ApacheBench (`ab`) là CLI benchmark một HTTP endpoint, đi cùng Apache HTTP Server do Apache Software Foundation/PMC duy trì. Mục tiêu chính thức là cho biết số request/giây một HTTP server có thể phục vụ; đây là endpoint benchmark, không phải engine mô phỏng business journey. [Manual `ab`](https://httpd.apache.org/docs/current/en/programs/ab.html), [About HTTP Server](https://httpd.apache.org/ABOUT_APACHE.html) (truy cập 2026-07-14). **[DOC]**

### 2. Cost và licence

Source mở theo Apache License 2.0, không cần tài khoản/trial và sinh viên có thể truy cập tự do. [LICENSE](https://github.com/apache/httpd/blob/trunk/LICENSE), [download](https://httpd.apache.org/download.cgi) (truy cập 2026-07-14). **[DOC]**

### 3. Installation và platform support

`ab` thuộc bộ chương trình HTTP Server. ASF phát source; trang tải nói binary Windows do bên thứ ba cung cấp. Build source có APR/APR-util, PCRE và toolchain tùy cấu hình, nên phải ghi provenance/version của package hoặc binary. [Programs](https://httpd.apache.org/docs/2.4/en/programs/), [Install](https://httpd.apache.org/docs/2.4/install.html), [download](https://httpd.apache.org/download.cgi) (truy cập 2026-07-14). **[DOC]**

### 4. Scripting hoặc configuration model

Cấu hình qua command line và file body POST/PUT; header, cookie và auth có option tĩnh. Lệnh/file dễ version-control nhưng không có module/scenario DSL. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC]**

### 5. Workload capabilities

`-n` tổng request, `-c` concurrency, `-t` duration, `-k` keep-alive, `-s` timeout; một invocation nhắm một URL. Không có arrival-rate phase, scenario mix, VU session, response extractor/correlation hay distributed controller được tài liệu hóa. Shell-chaining nhiều lệnh không tạo journey/session native. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 6. Assertions và validation

Báo failed requests và non-2xx nhưng không có response-body/business assertion hoặc SLA threshold. HTTP 200 không tự chứng minh dữ liệu sản phẩm/checkout đúng. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 7. Metrics và reporting

Console có complete/failed, RPS, time/request, transfer rate và lỗi connect/read/length/exception; `-e` xuất percentile CSV, `-g` TSV measurement, `-w` bảng HTML. Tài liệu cảnh báo `ab` có thể thành bottleneck và không triển khai đầy đủ HTTP/1.x. [Manual/Bugs](https://httpd.apache.org/docs/current/en/programs/ab.html#bugs) (truy cập 2026-07-14). **[DOC]**

### 8. CI/CD và automation

CLI dễ gọi trong pipeline và chạy local/offline, nhưng performance gate/exit policy cần wrapper parse output; không có container release first-party dành riêng cho `ab` trong kênh phát hành chương trình. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html), [download](https://httpd.apache.org/download.cgi) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 9. EShop suitability

Phù hợp GET product/catalog hoặc một API cô lập. Login/session, cart/checkout, data động và multi-step correlation vượt ranh giới native; chỉ có thể replay header/cookie/body tĩnh. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 10. AI-assisted potential

AI có thể soạn lệnh, ma trận `n/c`, parser CSV và checklist Failure Modes; phải audit URL/secret, hai biến thể time/request, sample size và generator saturation. AI không bổ sung session/assertion native. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 11. Classroom suitability

Mental model nhỏ, chạy offline và có thể demo trong 25 phút nếu binary/endpoint đã chuẩn bị; Windows cần package provenance rõ. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html), [download](https://httpd.apache.org/download.cgi) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 12. Điểm mạnh trong phạm vi seminar

Time-to-first-baseline rất ngắn; command/artifact gọn; minh họa rõ concurrency, throughput, latency và client bottleneck. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 13. Hạn chế trong phạm vi seminar

Không phù hợp làm công cụ chính cho journey EShop; thiếu business check/SLA gate; protocol/client bottleneck đe dọa validity. Đây là ranh giới công cụ endpoint benchmark, không phải kết luận công cụ “kém”. [Bugs](https://httpd.apache.org/docs/current/en/programs/ab.html#bugs) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 14. Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

- **Mục tiêu:** xác nhận một GET EShop nhỏ và percentile artifact.
- **Prerequisites:** `[VERIFIED_BASE_URL]`, `[VERIFIED_PRODUCT_PATH]`, `[EXPECTED_STATUS]`, TLS/proxy và resource monitoring đã xác minh. **[ASSUMPTION]**
- **Installation/setup:** cài/build theo [hướng dẫn chính thức](https://httpd.apache.org/docs/2.4/install.html) (truy cập 2026-07-14); lưu `ab -V`, source/package/checksum.
- **Một request:** `GET [VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]`.
- **Command:** `ab -n 20 -c 2 -e ab-percentiles.csv "[VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]"` theo [manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14).
- **Expected result:** 20 complete, status theo contract, không connect/read/exception, CSV parse được; chưa dự đoán latency/RPS.
- **Evidence:** version/provenance, command redacted, stdout/stderr, exit code, CSV/hash, EShop commit, timestamp/timezone, CPU/RAM/network client và SUT.
- **Possible errors:** DNS/TLS/refused; response-length biến đổi; file descriptor; Windows provenance; secret leak; client saturation.
- **Success criteria:** count/status đúng, transport error bằng 0 ở smoke load, generator còn headroom, artifacts đủ để rerun; chỉ thêm SLA sau baseline được duyệt.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Evidence |
|---|---:|---:|---|
| Cost & access | 8% | 5 | Apache-2.0/source mở. **[DOC]**; **Trace:** AB-DOC-01, AB-DOC-02. |
| Learning curve | 8% | 5 | CLI nhỏ. **[DOC]**; **Trace:** AB-DOC-01, AB-DOC-02. |
| EShop fit | 15% | 2 | Endpoint đơn. **[DOC + ASSUMPTION]**; **Trace:** AB-DOC-01, AB-DOC-02. |
| Multi-step journey | 12% | 1 | Không session/extractor. **[DOC + ASSUMPTION]**; **Trace:** AB-DOC-01, AB-DOC-02. |
| Workload control | 10% | 2 | Count/concurrency/duration, không phase. **[DOC]**; **Trace:** AB-DOC-01, AB-DOC-02. |
| Assertions/checks | 8% | 1 | Protocol failure, không business check. **[DOC + ASSUMPTION]**; **Trace:** AB-DOC-01, AB-DOC-02. |
| Reporting | 8% | 3 | Console + percentile CSV/TSV. **[DOC]**; **Trace:** AB-DOC-01, AB-DOC-02. |
| CI/CD | 7% | 2 | Cần wrapper/gate. **[DOC + ASSUMPTION]**; **Trace:** AB-DOC-01, AB-DOC-02. |
| Reproducibility | 7% | 4 | Lệnh pin được; client bottleneck. **[DOC]**; **Trace:** AB-DOC-01, AB-DOC-02. |
| Local/offline | 5% | 5 | Không SaaS. **[DOC]**; **Trace:** AB-DOC-01, AB-DOC-02. |
| AI-assisted potential | 7% | 2 | Hữu ích quanh CLI, không đổi semantics. **[DOC + ASSUMPTION]**; **Trace:** AB-DOC-01, AB-DOC-02. |
| Classroom suitability | 5% | 5 | Demo nhanh. **[DOC + ASSUMPTION]**; **Trace:** AB-DOC-01, AB-DOC-02. |
| Community | 0% | 5 | ASF docs/support/mailing list; không ảnh hưởng tổng. [Support](https://httpd.apache.org/userslist.html) (truy cập 2026-07-14). **[DOC]**; **Trace:** AB-DOC-01, AB-DOC-02. |

**Tổng có trọng số: 56.0/100**; Community 0% không tham gia công thức.

### 16. Kết luận sơ bộ

**Supporting benchmark tool.** Dùng làm endpoint baseline phụ, không dùng để tuyên bố hành trình EShop thành công.

### 17. Câu hỏi phản biện

<details>
<summary>Phản biện và trả lời</summary>

1. **Không có journey thì còn giá trị gì?** Cô lập route để có baseline latency/RPS nhanh; claim dừng ở endpoint. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
2. **Có `-e` là p95 đã đáng tin?** Có percentile artifact, nhưng sample size, warm-up và client bottleneck vẫn quyết định validity. [Manual/Bugs](https://httpd.apache.org/docs/current/en/programs/ab.html#bugs) (truy cập 2026-07-14). **[DOC]**
3. **HTTP 200 chứng minh business đúng?** Không; `ab` không có body/business assertion native. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

</details>

## 7.13. OpenText LoadRunner Professional

### 1. Tổng quan

Tên hiện hành là **OpenText Professional Performance Engineering (LoadRunner Professional)**, bộ enterprise on-prem performance testing cho co-located teams. Ba thành phần chính: VuGen tạo script, Controller điều phối/monitor scenario, Analysis phân tích result ([Product](https://www.opentext.com/products/professional-performance-engineering), [Get started 26.1](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/WelcomeContent/c_Welcome.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 2. Cost và licence

Community license 26.1 tự cài, miễn phí 50 Vuser cho các protocol, gồm JMeter/Gatling, trừ COM/DCOM, Templates và GUI bundles. Scale/bundle khác dùng evaluation/permanent/VUFD/commercial; giá public chưa tìm thấy: `[CẦN BÁO GIÁ]`. Trial được request không cần card, entitlement/duration phải xác minh ([License Utility](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/License/R_License_Utility.htm), [Trial](https://www.opentext.com/en-gb/products/professional-performance-engineering/trial) — truy cập 2026-07-14). Evidence: `DOC`.

### 3. Installation và platform support

VuGen/Controller/Analysis full stack là Windows-centric; standalone OneLG có Windows/Linux tùy protocol. Official Docker images chỉ cho load generators Ubuntu/RHEL/Windows, có firewall/protocol limitations; không đồng nghĩa full stack container ([Install](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Install/About-install.htm), [Docker LG](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/dockerized_load_generator.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 4. Scripting hoặc configuration model

VuGen record client-server traffic; recorded scripts chủ yếu C, một số protocol dùng C#/VB.NET/Java/JavaScript; init/action/end tách login/business/logout. Có HAR/offline generation, file/generated parameters, Correlation Studio và automatic correlation ([Vuser scripts](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/100050_c_vugen_overview.htm), [Recording](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/tocs/103100_toc_recording.htm), [Correlation](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/tocs/109650_toc_correlation_studio.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 5. Workload capabilities

Manual Scenario ghép scripts/groups, VU số lượng/tỷ lệ, load generators và SLA; schedule theo scenario/group có ramp/duration/stop. Goal-oriented targets VUs/pages/min/hits/s/transactions/s và tự điều chỉnh VU; nhiều on-prem/cloud/container LG phân tán tải ([Manual scenarios](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_manual_scenarios.htm), [Schedules](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_schedules_overview.htm), [Goal-oriented](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_goal_oriented_scenarios.htm) — truy cập 2026-07-14). Goal throughput không tự động tương đương fixed open-arrival executor (`ASSUMPTION`).

### 6. Assertions và validation

VuGen Web text/image checks xác minh đúng page/object; transactions và Controller/Analysis SLA cho pass/fail/APDEX. API flow vẫn cần status/body/business invariant cụ thể ([Web checks](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/c_web_text_and_image_verification.htm), [SLAs](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/toc_SLAs_main.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 7. Metrics và reporting

Analysis có transaction/TPS, throughput/web resources, errors/monitoring, HTML/Excel, raw result/export JSON/InfluxDB; Summary có HTTP status, pass/fail, APDEX và configurable percentile. Known Issues 26.1 ghi một Transaction Response Time percentile graph có thể sai, nên cross-check raw/export và patch ([Analysis](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/c_analysis_workflow.htm), [Summary](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/116850_ui_summary_report.htm), [Known issues](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/tl_Analysis.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 8. CI/CD và automation

`CLIControllerApp.exe` chạy `.lrs`/XML, Run/Collate/CollateAndAnalyze, result path/LG override/`-SilentMode`; chỉ một Controller, args case-sensitive và có overwrite risk. Direct CLI không công bố universal “SLA fail = exit N”; Jenkins OpenText plugin chạy scenarios có SLA để xác định pass/fail ([CLI](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/scenario-run-cli.htm), [Jenkins](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_jenkins.htm) — truy cập 2026-07-14). Evidence: `DOC`; direct exit: `[CẦN THỰC NGHIỆM]`.

### 9. EShop suitability

Web/API, recorder, data, token/session correlation, user mix, scheduling, SLA và monitoring rất phù hợp enterprise EShop. Nhiều protocol (>180 technologies theo product claim) hữu ích khi có legacy/packaged systems, nhưng HTTP EShop không tự động cần breadth đó ([Product](https://www.opentext.com/products/professional-performance-engineering), [Supported Protocols 26.1](https://admhelp.microfocus.com/documents/lre/Supported_Protocols/26.1/LR_Protocols.htm) — truy cập 2026-07-14). Evidence: `DOC` + fit `ASSUMPTION`.

### 10. AI-assisted potential

VuGen 26.1 có paid cloud **Aviator for Scripting**: protocol selection, coding help, error analysis, optimization, summary; AI analysis thuộc Core Performance Engineering Analysis. Không mặc định free/offline; output vẫn phải replay/audit ([VuGen What's New 26.1](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/WelcomeContent/c_WhatsNew.htm) — truy cập 2026-07-14). Evidence: `DOC` + governance `ASSUMPTION`; nghiên cứu không gọi Aviator.

### 11. Classroom suitability

Community 50 VU cho demo, nhưng Windows/admin, ba-component workflow, protocol concepts và artefact nặng khó hoàn tất trong 25 phút nếu không pre-install/prebuild; `[CẦN THỰC NGHIỆM]`. Evidence: `DOC` + `ASSUMPTION`.

### 12. Điểm mạnh trong phạm vi seminar

Enterprise protocol breadth; mature recording/correlation; Controller scheduling/distribution; Analysis/SLA; Community 50 VU; Jenkins/Docker LG; native AI ([Get started](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/WelcomeContent/c_Welcome.htm) — truy cập 2026-07-14). Evidence: `DOC`.

### 13. Hạn chế trong phạm vi seminar

Windows-heavy; commercial price không public; nhiều component/license/patch làm reproducibility nặng; direct CLI SLA exit cần test; documented percentile issue; Aviator paid/cloud. So với JMeter, LoadRunner có lifecycle/protocol enterprise tích hợp hơn, còn JMeter dễ access/local/version-control hơn; không kết luận công cụ nào mạnh tuyệt đối ([JMeter](https://jmeter.apache.org/), [LoadRunner product](https://www.opentext.com/products/professional-performance-engineering) — truy cập 2026-07-14). Evidence: `DOC` + contextual `ASSUMPTION`.

### 14. Smoke Test Plan

**[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN]**

- **Mục tiêu:** VuGen GET/check → Controller 1 VU → collate/Analysis/SLA; không đo capacity.
- **Prerequisites:** supported Windows/admin, installer checksum/patch, Community license, `[VERIFIED_BASE_URL]`, quyền test.
- **Installation/setup:** cài VuGen/Controller/Analysis; ghi License Utility; Web HTTP/HTML script + text check; manual `.lrs`, 1 VU/local LG/1 iteration + SLA.
- **Request:** `GET [VERIFIED_BASE_URL]/[VERIFIED_READ_ONLY_PATH]` bằng `web_url`, đăng ký text check trước request.
- **Command/config:** `CLIControllerApp.exe -TestPath C:\lab\lr-smoke\lr-smoke.lrs -CollateAndAnalyze -ResultName C:\lab\artifacts\lr-smoke -SilentMode` ([CLI](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/scenario-run-cli.htm) — truy cập 2026-07-14).
- **Kết quả mong đợi:** Vuser/check/SLA pass, collated result + Analysis report; chưa quan sát.
- **Evidence:** version/license redacted, VuGen source/data/runtime, `.lrs`/SLA/schedule/LG, command/stdout/stderr/exit, raw result/report.
- **Lỗi có thể gặp:** license/protocol, Windows privilege, recording/TLS/correlation, LG down, only-one-Controller, result overwrite/path, Analysis issue.
- **Tiêu chí thành công:** đúng request/check/SLA, collate/report đủ; marker/SLA sai phải chứng minh plugin/direct-CLI failure propagation.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Lý do | Evidence |
|---|---:|---:|---|---|
| Cost & access | 8% | 4 | Community 50 VU; ngoài đó commercial | DOC; **Trace:** LR-DOC-01, LR-DOC-02. |
| Learning curve | 8% | 2 | VuGen–Controller–Analysis/protocol depth | ASSUMPTION từ DOC; **Trace:** LR-DOC-01, LR-DOC-02. |
| EShop fit | 15% | 5 | Full Web/API state/data/SLA | DOC + ASSUMPTION; **Trace:** LR-DOC-01, LR-DOC-02. |
| Multi-step journey & state | 12% | 5 | init/action/end/parameter/correlation | DOC; **Trace:** LR-DOC-01, LR-DOC-02. |
| Workload model & scalability | 10% | 5 | Manual/goal/ramp/multi-LG/cloud | DOC; **Trace:** LR-DOC-01, LR-DOC-02. |
| Assertions & business validation | 8% | 5 | Checks/transactions/SLA | DOC; **Trace:** LR-DOC-01, LR-DOC-02. |
| Metrics & reporting | 8% | 5 | Analysis/raw/export/SLA/APDEX | DOC; **Trace:** LR-DOC-01, LR-DOC-02. |
| CI/CD & automation | 7% | 4 | CLI/Jenkins; direct exit needs lab | DOC + ASSUMPTION; **Trace:** LR-DOC-01, LR-DOC-02. |
| Reproducibility | 7% | 3 | Assets saveable; multi-component/license/OS | ASSUMPTION; **Trace:** LR-DOC-01, LR-DOC-02. |
| Local/offline | 5% | 5 | Full on-prem runner/analysis/help | DOC; **Trace:** LR-DOC-01, LR-DOC-02. |
| AI-assisted potential | 7% | 4 | Native Aviator, paid cloud dependency | DOC + ASSUMPTION; **Trace:** LR-DOC-01, LR-DOC-02. |
| Classroom suitability | 5% | 2 | 50 VU helps; setup/workflow difficult | ASSUMPTION; **Trace:** LR-DOC-01, LR-DOC-02. |
| Community | 0% | 4 | Current 26.1 Help Center, plugin/support ecosystem ([Help](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/WelcomeContent/c_Welcome.htm) — truy cập 2026-07-14) | DOC; không tính; **Trace:** LR-DOC-01, LR-DOC-02. |

**Weighted Score provisional: 85,0/100; 0 EXP.**

### 16. Kết luận sơ bộ

**Backup** / enterprise reference. Community tier cho phép demo, nhưng không phải lựa chọn live mặc định khi JMeter/k6 tái lập gọn hơn cho EShop seminar.

### 17. Câu hỏi phản biện

<details>
<summary><strong>Câu hỏi phản biện LoadRunner Professional</strong></summary>

1. **Có thật sự miễn phí?** Community miễn phí đến 50 VU với exclusions; scale/bundle khác commercial ([License](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/License/R_License_Utility.htm) — truy cập 2026-07-14).
2. **180+ protocol làm nó tốt hơn JMeter cho EShop?** Không tự động; HTTP EShop còn phụ thuộc access, script clarity, CI và reproducibility.
3. **Docker nghĩa full LoadRunner container?** Không; source ở đây xác nhận Dockerized **load generators**, không full Controller/VuGen/Analysis ([Docker LG](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/dockerized_load_generator.htm) — truy cập 2026-07-14).
4. **Aviator tự sửa correlation chính xác?** Không; assistance phải qua replay, request snapshot, business assertions và raw evidence.
5. **Analysis percentile là ground truth?** Cần đúng patch/settings và raw cross-check vì có known issue ([Known issues](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/tl_Analysis.htm) — truy cập 2026-07-14).

</details>

## 7.14. Tsung

> **Trạng thái bằng chứng:** chỉ **[DOC]**, **[DOC + ASSUMPTION]**, **[ASSUMPTION]** và kế hoạch chưa chạy; ngày chốt 2026-07-14.

### 1. Tổng quan

Tsung là framework load test distributed/multi-protocol, repository chính thức thuộc ProcessOne; tài liệu ghi tác giả ban đầu Nicolas Niclausse. Source `develop` khai báo 1.8.0, trong khi hosted manual mang nhãn 1.7.0, nên phải pin tag/DTD và ghi version skew. [Repository](https://github.com/processone/tsung), [`vsn.mk`](https://github.com/processone/tsung/blob/develop/vsn.mk), [manual](https://tsung.readthedocs.io/en/latest/) (truy cập 2026-07-14). **[DOC]**

### 2. Cost và licence

Source mở GPL v2, không cần tài khoản/trial. [Introduction](https://tsung.readthedocs.io/en/latest/introduction.html), [COPYING](https://github.com/processone/tsung/blob/develop/COPYING) (truy cập 2026-07-14). **[DOC]**

### 3. Installation và platform support

Manual nêu Linux/FreeBSD/Solaris và MacPorts, về nguyên tắc trên hệ Erlang hỗ trợ. Dependency gồm Erlang/OTP, build tools; report có thể cần gnuplot, Perl/Template Toolkit hoặc Python/matplotlib. Build `./configure; make; make install`; distributed cần host resolution/Erlang nodes và passwordless SSH. Các minimum-version trong manual 1.7.0 không được tự coi là recommendation năm 2026. [Installation](https://tsung.readthedocs.io/en/latest/installation.html) (truy cập 2026-07-14). **[DOC]**

### 4. Scripting hoặc configuration model

XML/DTD định nghĩa clients, servers, load, sessions, request/transaction/think time; CSV data và config dễ version-control/modularize ở mức file. Local có `use_controller_vm='true'`; cấu hình nâng cao dùng dynvars/loops/conditions. [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html), [Sessions](https://tsung.readthedocs.io/en/latest/conf-sessions.html), [Advanced](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html) (truy cập 2026-07-14). **[DOC]**

### 5. Workload capabilities

Nhiều arrival phases có duration, interarrival/arrival rate/max users; weighted/probabilistic sessions, think time và distributed client hosts/maxusers/weights. Automatic cookies, CSV sequential/random, regex/XPath/limited JSONPath extraction, substitution, random/unique data, loop/if/foreach hỗ trợ session/correlation thật. [Load](https://tsung.readthedocs.io/en/latest/conf-load.html), [Features](https://tsung.readthedocs.io/en/latest/features.html), [Advanced](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html) (truy cập 2026-07-14). **[DOC]**

README hiện hành liệt kê HTTP, WebDAV, SOAP, PostgreSQL, MySQL, LDAP, MQTT, AMQP và Jabber/XMPP. Manual 1.7.0 mô tả thêm WebSocket RFC6455, AMQP 0.9.1, MQTT v3.1 là experimental; phải xác minh tag 1.8.0 trước khi claim production support. [README](https://github.com/processone/tsung), [Features](https://tsung.readthedocs.io/en/latest/features.html) (truy cập 2026-07-14). **[DOC]**

### 6. Assertions và validation

`match` kiểm tra response và có action continue/log/abort session/abort test/restart/loop/dump cùng counters match/nomatch. Đây là content/business validation mạnh; aggregate SLA p95/error-budget vẫn cần policy ngoài. [Response checks](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html#checking-the-server-s-response) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 7. Metrics và reporting

Statistics log hoặc JSON backend theo dõi request/page/connect/session/users/status/traffic; live web dashboard và `tsung_stats.pl` tạo HTML/graphs. Engine chuẩn tính mean/stdev theo interval thay vì mặc định giữ mọi sample, nên raw per-request/p50/p95/p99 phải xác minh theo backend/fullstats của đúng version. [Reports](https://tsung.readthedocs.io/en/latest/reports.html) (truy cập 2026-07-14). **[DOC]**

### 8. CI/CD và automation

CLI `tsung -f config.xml start`, XML/data Git-friendly và local/offline; CI phải pin DTD/version, quản lý node/SUT lifecycle, collect log/report và áp SLA gate. `abort_test` theo match không thay aggregate performance gate. Repository không trình bày first-party container image như kênh phát hành cốt lõi. [Installation/Running](https://tsung.readthedocs.io/en/latest/installation.html#running), [Reports](https://tsung.readthedocs.io/en/latest/reports.html), [Repository](https://github.com/processone/tsung) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 9. EShop suitability

HTTP cookies, dynamic data, correlation, transactions, think time và match có thể biểu diễn login→product→cart→checkout tốt nếu endpoint contract được xác minh. Local single-node phù hợp hơn cluster cho smoke EShop nhỏ. [Features](https://tsung.readthedocs.io/en/latest/features.html), [Advanced](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 10. AI-assisted potential

AI có thể scaffold XML/CSV/extractor/match/phases và phân tích report; phải audit DTD/version, XML escaping, regex/JSONPath giới hạn, secret, correlation, arrival semantics và Failure Modes. Config AI chưa smoke không được coi là đúng. [Advanced](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html), [Load](https://tsung.readthedocs.io/en/latest/conf-load.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 11. Classroom suitability

Năng lực minh họa cao nhưng Erlang/XML/DTD/report/distributed concepts khó vừa 25 phút nếu chưa chuẩn bị lab. Single-node prebuilt có thể demo offline; tự cài cluster trong lớp là over-scope. [Installation](https://tsung.readthedocs.io/en/latest/installation.html), [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 12. Điểm mạnh trong phạm vi seminar

Session/correlation/assertion, workload phases/mix, protocol breadth, scale-out thật và HTML/dashboard. [Features](https://tsung.readthedocs.io/en/latest/features.html), [Load](https://tsung.readthedocs.io/en/latest/conf-load.html), [Reports](https://tsung.readthedocs.io/en/latest/reports.html) (truy cập 2026-07-14). **[DOC]**

### 13. Hạn chế trong phạm vi seminar

Learning/setup cao; hosted docs lệch source version; raw percentile/gate cần xác minh thêm. Distributed chỉ cần khi một generator bão hòa CPU/memory/network/socket hoặc mục tiêu yêu cầu scale/geography; với local EShop nó thêm SSH, Erlang naming/cookies, clock/network và biến nhiễu. [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html), [Installation](https://tsung.readthedocs.io/en/latest/installation.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 14. Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

- **Mục tiêu:** single-node đọc XML, gửi một GET và sinh log/report; không bật cluster.
- **Prerequisites:** `[VERIFIED_HOST]`, `[VERIFIED_PORT]`, `[VERIFIED_PRODUCT_PATH]`, protocol/TLS và pinned tag/DTD/dependencies. **[ASSUMPTION]**
- **Installation/setup:** theo [Installation](https://tsung.readthedocs.io/en/latest/installation.html) (truy cập 2026-07-14); lưu Tsung/Erlang versions, source commit và dependency versions.
- **Một request:** GET path đã xác minh. Skeleton base bên dưới cố ý chưa có body `match`; chỉ thêm một match đã review sau khi pin binary/DTD và xác minh stable marker.
- **Config/command:** validate skeleton dưới bằng DTD của binary; chạy `tsung -f smoke.xml -l ./tsung-logs start`, rồi `tsung_stats.pl` trong `[GENERATED_LOG_DIR]`. [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html), [Load](https://tsung.readthedocs.io/en/latest/conf-load.html), [Reports](https://tsung.readthedocs.io/en/latest/reports.html) (truy cập 2026-07-14).

```xml
<?xml version='1.0'?>
<!DOCTYPE tsung SYSTEM '/path/to/pinned/tsung-1.0.dtd'>
<tsung loglevel='notice' version='1.0'>
 <clients><client host='localhost' use_controller_vm='true'/></clients>
 <servers><server host='[VERIFIED_HOST]' port='[VERIFIED_PORT]' type='tcp'/></servers>
 <load><arrivalphase phase='1' duration='10' unit='second'><users interarrival='1' unit='second'/></arrivalphase></load>
 <sessions><session name='smoke' probability='100' type='ts_http'><request><http url='[VERIFIED_PRODUCT_PATH]' method='GET' version='1.1'/></request></session></sessions>
</tsung>
```

- **Expected result:** XML/DTD hợp lệ, local node start/stop sạch, request/transport đúng contract và log/report sinh được; base smoke chưa tuyên bố business/body check và chưa dự đoán metric.
- **Evidence:** XML/DTD/hash, Tsung/Erlang/source versions, command, stdout/stderr/exit, log/JSON/HTML, EShop commit, time/timezone, resources, redaction.
- **Possible errors:** DTD mismatch; Erlang hostname/node/cookie; port/TLS; report dependency; placeholder; match/escaping; clock; vô tình remote client/SSH; secret trong log.
- **Success criteria:** single-node hoàn tất, request/transport đúng và artifacts đủ/rerun được; body match chỉ được tính khi đã thêm vào XML, validate bằng pinned DTD/binary và chạy negative control. Chưa bật distributed/SLA gate.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Evidence |
|---|---:|---:|---|
| Cost & access | 8% | 5 | GPLv2/source mở. **[DOC]**; **Trace:** TS-DOC-01, TS-DOC-02. |
| Learning curve | 8% | 2 | XML/Erlang/distributed/report. **[DOC + ASSUMPTION]**; **Trace:** TS-DOC-01, TS-DOC-02. |
| EShop fit | 15% | 5 | Session/correlation/check. **[DOC]**; **Trace:** TS-DOC-01, TS-DOC-02. |
| Multi-step journey | 12% | 5 | Transactions/dynvars/loops. **[DOC]**; **Trace:** TS-DOC-01, TS-DOC-02. |
| Workload control | 10% | 5 | Phases/rates/session mix/clients. **[DOC]**; **Trace:** TS-DOC-01, TS-DOC-02. |
| Assertions/checks | 8% | 4 | `match` mạnh; SLA ngoài. **[DOC + ASSUMPTION]**; **Trace:** TS-DOC-01, TS-DOC-02. |
| Reporting | 8% | 4 | Stats/JSON/live/HTML; raw cần xác minh. **[DOC]**; **Trace:** TS-DOC-01, TS-DOC-02. |
| CI/CD | 7% | 3 | CLI/XML tốt, lifecycle/gate phức tạp. **[DOC + ASSUMPTION]**; **Trace:** TS-DOC-01, TS-DOC-02. |
| Reproducibility | 7% | 4 | XML pin được; version/node/randomness. **[DOC + ASSUMPTION]**; **Trace:** TS-DOC-01, TS-DOC-02. |
| Local/offline | 5% | 4 | Single-node được; dependencies nặng. **[DOC]**; **Trace:** TS-DOC-01, TS-DOC-02. |
| AI-assisted potential | 7% | 3 | Scaffold tốt, audit DTD/correlation. **[DOC + ASSUMPTION]**; **Trace:** TS-DOC-01, TS-DOC-02. |
| Classroom suitability | 5% | 2 | Khó trong timebox ngắn. **[DOC + ASSUMPTION]**; **Trace:** TS-DOC-01, TS-DOC-02. |
| Community | 0% | 3 | Repo/manual/issues có, nhưng docs skew; không ảnh hưởng tổng. [Repository](https://github.com/processone/tsung), [manual](https://tsung.readthedocs.io/en/latest/) (truy cập 2026-07-14). **[DOC]**; **Trace:** TS-DOC-01, TS-DOC-02. |

**Tổng có trọng số: 81.0/100**; Community 0% không tham gia công thức.

### 16. Kết luận sơ bộ

**Survey-only** cho seminar EShop local/timebox hiện tại; cân nhắc shortlist trong dự án dài ngày cần journey + distributed scale.

### 17. Câu hỏi phản biện

<details>
<summary>Phản biện và trả lời</summary>

1. **Điểm cao nhất sao chỉ Survey-only?** Điểm đo năng lực; XML/Erlang/version skew và distributed operations làm risk/timebox không phù hợp demo ngắn. [Installation](https://tsung.readthedocs.io/en/latest/installation.html), [manual](https://tsung.readthedocs.io/en/latest/) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
2. **Khi nào distributed thực sự cần?** Khi generator đơn không đạt load/bão hòa tài nguyên hoặc nghiên cứu scale/geography; smoke local có controller VM. [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
3. **Vì sao không gắn tiền tố của ASF?** Repo/docs thuộc dự án Tsung/ProcessOne, không có bằng chứng liên hệ ASF; tên đúng là **Tsung**. [Repository](https://github.com/processone/tsung), [Introduction](https://tsung.readthedocs.io/en/latest/introduction.html) (truy cập 2026-07-14). **[DOC]**
4. **XML làm giảm tái lập?** Không tự thân; XML/data pin tốt. Rủi ro là DTD/version, randomness, node/network và dependency chưa khóa. [`vsn.mk`](https://github.com/processone/tsung/blob/develop/vsn.mk), [Configuration](https://tsung.readthedocs.io/en/latest/configuration.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

</details>

## 7.15. Taurus

**1. Tổng quan.** **[DOC]** Taurus, CLI tên **bzt**, là automation-friendly orchestration/convenience framework: nó thống nhất config, gọi executor và tổng hợp/report kết quả; **không phải load generator độc lập ngang hàng k6, Locust, Gatling hoặc Artillery**. Repository do tổ chức BlazeMeter duy trì; supported executors hiện gồm JMeter, Gatling, Locust, k6, Selenium, Playwright, Apiritif và nhiều tool khác. ([Taurus repository](https://github.com/Blazemeter/taurus), [Execution settings/executors](https://gettaurus.org/docs/ExecutionSettings/) — truy cập 2026-07-14)

**2. Cost và licence.** **[DOC]** Taurus dùng Apache-2.0 và local OSS không cần account. BlazeMeter report/cloud là tùy chọn có Free Starter và paid plans; Cloud provisioning cần API key. Repository hiện hiển thị release 1.16.51 ngày 2026-06-15, là tín hiệu activity chứ không phải bằng chứng chất lượng runtime. ([Taurus repository](https://github.com/Blazemeter/taurus), [BlazeMeter pricing](https://www.blazemeter.com/pricing), [Cloud provisioning](https://gettaurus.org/docs/Cloud/) — truy cập 2026-07-14)

**3. Installation và platform support.** **[DOC]** Official install dùng **pip install bzt**, có hướng dẫn Linux/macOS/Windows và image **blazemeter/taurus**. Docs nêu Python 3.7+; executor có dependency riêng, ví dụ Java/JMeter. ([Installation](https://gettaurus.org/docs/Installation/), [Docker installation](https://gettaurus.org/install/Installation/) — truy cập 2026-07-14) **[ASSUMPTION]** “Cài Taurus” chưa đồng nghĩa toàn stack sẵn sàng; reproducible setup phải pin Python, bzt, executor, runtime và plugins.

**4. Scripting hoặc configuration model.** **[DOC]** bzt nhận YAML/JSON, merge nhiều config, hỗ trợ CLI overrides và sinh merged/effective configs; text artefact phù hợp Git. Default executor là **jmeter**. ([Command line](https://gettaurus.org/docs/CommandLine/), [Config syntax](https://gettaurus.org/docs/ConfigSyntax/), [Execution settings](https://gettaurus.org/docs/ExecutionSettings/) — truy cập 2026-07-14)

**5. Workload capabilities.** **[DOC]** Common execution profile có concurrency, ramp-up, hold-for, iterations, throughput, steps và multiple executions. Support/semantics phụ thuộc executor. ([Execution settings/load profile](https://gettaurus.org/docs/ExecutionSettings/) — truy cập 2026-07-14) Khi chọn hoặc mặc định **executor: jmeter**, Taurus generate/modify/orchestrate plan nhưng **Apache JMeter là engine thực thi request và phát tải**; Taurus có thể auto-download JMeter/plugins nếu thiếu. Existing JMX/thread groups và YAML load settings có override/proportional rules riêng. ([JMeter executor](https://gettaurus.org/docs/JMeter/) — truy cập 2026-07-14)

**Abstraction cost — [ASSUMPTION dựa trên DOC]:** YAML ngắn che bớt engine complexity, nhưng feature parity và exact semantics khác giữa executors; debug phải đọc cả bzt log, executor log và generated script. Merged/effective config + generated JMX là evidence bắt buộc để biết test thực chạy. ([Artifacts](https://gettaurus.org/docs/ArtifactsDir/) — truy cập 2026-07-14)

**6. Assertions và validation.** **[DOC]** Với JMeter executor, request YAML hỗ trợ status/body/header, JSONPath/XPath assertions và extractors regex/boundary/JSONPath/CSS/XPath. Taurus **passfail** module đặt criteria trên failure/success, response code, average response time, percentiles và timeframe; có stop/continue, global/per-execution/per-scenario criteria. ([JMeter request/assertions](https://gettaurus.org/docs/JMeter/), [Pass/fail criteria](https://gettaurus.org/docs/PassFail/) — truy cập 2026-07-14)

**7. Metrics và reporting.** **[DOC]** Default console/final-stats có sample/failure, average, latency/connect và percentiles; optional JUnit XML, CSV/XML dump, InfluxDB và BlazeMeter online report. Artifacts chứa bzt.log, original/merged/effective config, executor stdout/stderr/log, JTL/LDJSON và generated executor scripts. ([Reporting](https://gettaurus.org/docs/Reporting/), [Artifacts directory](https://gettaurus.org/docs/ArtifactsDir/) — truy cập 2026-07-14)

**8. CI/CD và automation.** **[DOC]** bzt exit codes: 0 no problem, 1 generic error, 2 manual shutdown, 3 automatic shutdown như pass/fail hoặc Cloud failure. JUnit XML có thể dùng pass-fail data source; official knowledge base có Jenkins integration, Docker image nhận config/mount artifacts. ([Command-line exit codes](https://gettaurus.org/docs/CommandLine/), [Reporting/JUnit](https://gettaurus.org/docs/Reporting/), [Jenkins](https://gettaurus.org/kb/Jenkins/), [Docker](https://gettaurus.org/install/Installation/) — truy cập 2026-07-14)

**9. EShop suitability.** **[DOC]** Request YAML có method/body/headers/think-time, data sources, extractors, assertions và include-scenario composition; option availability khác theo executor. ([JMeter executor](https://gettaurus.org/docs/JMeter/), [Data sources](https://gettaurus.org/docs/DataSources/), [Include scenario example](https://gettaurus.org/docs/Gatling/) — truy cập 2026-07-14) **[ASSUMPTION]** Với explicit JMeter executor, EShop journey khả thi, nhưng cookie/session/correlation thật do JMeter/generated plan xử lý; phải inspect JMX, không giả định Taurus có independent cookie engine.

**10. AI-assisted potential.** Taurus **không phải AI tool**. **[ASSUMPTION]** Unified YAML dễ cho AI draft/review và compare executors; repository có CLAUDE.md mô tả contributor architecture cho coding agent, nhưng không chứng minh end-user test tự đúng. ([Taurus CLAUDE.md](https://github.com/Blazemeter/taurus/blob/master/CLAUDE.md) — truy cập 2026-07-14) Human audit bắt buộc: executor/version, supported fields, generated JMX, plugins/JVM, auto-download, data/secrets, passfail placement, artifacts và Cloud upload.

**11. Classroom suitability.** **[ASSUMPTION]** YAML ngắn rất tốt để dạy orchestration/abstraction, nhưng dễ che JMeter semantics và thêm Python + Java + executor setup. Activity ≤25 phút chỉ khả thi nếu stack pre-pinned; cần **[CẦN THỰC NGHIỆM]**. Default provisioning là local; Cloud/account không cần cho local activity. ([Cloud/local provisioning](https://gettaurus.org/docs/Cloud/) — truy cập 2026-07-14)

**12. Điểm mạnh trong phạm vi seminar.**

- **[DOC]** Unified YAML cho nhiều executors và existing scripts. ([Execution settings](https://gettaurus.org/docs/ExecutionSettings/) — truy cập 2026-07-14)
- **[DOC]** Common passfail/reporting/exit/JUnit tạo automation layer rõ. ([PassFail](https://gettaurus.org/docs/PassFail/), [Reporting](https://gettaurus.org/docs/Reporting/), [CLI](https://gettaurus.org/docs/CommandLine/) — truy cập 2026-07-14)
- **[DOC]** Merged/effective config và generated artefacts hỗ trợ audit nếu được giữ đầy đủ. ([Artifacts](https://gettaurus.org/docs/ArtifactsDir/) — truy cập 2026-07-14)
- **[ASSUMPTION]** Có giá trị giảng dạy để minh họa abstraction benefit/cost và orchestration CI.

**13. Hạn chế trong phạm vi seminar.**

- **[DOC]** Capability/semantics phụ thuộc executor; Taurus không phải engine phát tải. ([Execution settings](https://gettaurus.org/docs/ExecutionSettings/), [JMeter executor](https://gettaurus.org/docs/JMeter/) — truy cập 2026-07-14)
- **[DOC]** Auto-download JMeter/plugins có thể gây version/network drift. ([JMeter executor](https://gettaurus.org/docs/JMeter/) — truy cập 2026-07-14)
- **[ASSUMPTION]** Debug complexity tăng vì phải đọc YAML → effective config → generated plan → engine log.
- **[DOC]** Strict offline cần preinstall/cache; **TAURUS_DISABLE_DOWNLOADS** làm Taurus error thay vì tải tool. ([Config syntax](https://gettaurus.org/docs/ConfigSyntax/) — truy cập 2026-07-14)
- **[ASSUMPTION]** Không được dùng score/throughput của Taurus mà không ghi executor/version/plugins/JVM.

**14. Smoke Test Plan — explicit JMeter executor.** **[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN; 0 EXP]**

- **Mục tiêu:** chứng minh Taurus orchestrate **JMeter**, 1 VU/1 iteration, request assertion, passfail, JUnit, artifacts và exit.
- **Prerequisites:** authorized target; pin Python/bzt/Java/JMeter/plugins; pre-cache; tạo writable artifacts; thay placeholders.
- **Installation/setup:** venv/pinned image; explicit **executor: jmeter**; trong offline run đặt TAURUS_DISABLE_DOWNLOADS; lưu all versions.
- **Request/config mẫu:**

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

- **Command:** **bzt smoke.yml**.
- **Kết quả mong đợi:** Taurus generates/prepares JMX, JMeter executes one iteration, assertion/passfail pass, exit 0; JMX/JTL/log/merged/effective/JUnit artifacts exist. Nếu passfail automatic shutdown xảy ra, documented exit class là 3. ([JMeter](https://gettaurus.org/docs/JMeter/), [PassFail](https://gettaurus.org/docs/PassFail/), [Exit codes](https://gettaurus.org/docs/CommandLine/) — truy cập 2026-07-14)
- **Evidence cần thu:** Python/bzt/Java/JMeter/plugin/image versions; original YAML/hash; exact command/env; bzt.log; merged/effective YAML+JSON; generated/modified JMX; JMeter log/JTL; executor stdout/stderr; xunit.xml; exit; timestamps; machine/SUT metadata.
- **Lỗi có thể gặp:** Python/Java/JMeter mismatch, hidden auto-download/plugin resolution, YAML translation/override, assertion subject, reporter order/path, TLS/auth/permission.
- **Tiêu chí thành công:** evidence chứng minh JMeter executor, đúng one iteration/sample, assertion/passfail pass, exit 0 và không có unapproved download.

**15. Điểm đánh giá provisional — conditional on JMeter executor.** Mọi điểm là **DOC + ASSUMPTION**, **không có EXP**.

| Tiêu chí | Điểm | Lý do, evidence và nguồn |
|---|---:|---|
| Cost & access (8%) | 5/5 | Apache-2.0 local; Cloud optional. **DOC** ([repo](https://github.com/Blazemeter/taurus), [pricing](https://www.blazemeter.com/pricing) — truy cập 2026-07-14); **Trace:** TA-DOC-01, TA-DOC-02. |
| Learning curve (8%) | 4/5 | YAML ngắn, nhưng phải hiểu executor/generated plan. **DOC + ASSUMPTION** ([execution](https://gettaurus.org/docs/ExecutionSettings/) — truy cập 2026-07-14); **Trace:** TA-DOC-01, TA-DOC-02. |
| EShop fit (15%) | 4/5 | JMeter-backed request/extractor/data; executor-dependent. **DOC + ASSUMPTION** ([JMeter](https://gettaurus.org/docs/JMeter/) — truy cập 2026-07-14); **Trace:** TA-DOC-01, TA-DOC-02. |
| Multi-step journey (12%) | 4/5 | Requests/include/extractors tốt; parity cost. **DOC + ASSUMPTION** ([JMeter](https://gettaurus.org/docs/JMeter/), [data](https://gettaurus.org/docs/DataSources/) — truy cập 2026-07-14); **Trace:** TA-DOC-01, TA-DOC-02. |
| Workload control (10%) | 4/5 | Unified profile; exact semantics vary executor. **DOC** ([execution](https://gettaurus.org/docs/ExecutionSettings/) — truy cập 2026-07-14); **Trace:** TA-DOC-01, TA-DOC-02. |
| Assertions/checks (8%) | 4/5 | Request assertions + passfail; generated-engine semantics. **DOC** ([PassFail](https://gettaurus.org/docs/PassFail/) — truy cập 2026-07-14); **Trace:** TA-DOC-01, TA-DOC-02. |
| Reporting (8%) | 4/5 | Console/final/JUnit/CSV/XML/online, executor-dependent. **DOC** ([reporting](https://gettaurus.org/docs/Reporting/) — truy cập 2026-07-14); **Trace:** TA-DOC-01, TA-DOC-02. |
| CI/CD (7%) | 5/5 | bzt exit classes, JUnit, Docker/Jenkins. **DOC** ([CLI](https://gettaurus.org/docs/CommandLine/), [reporting](https://gettaurus.org/docs/Reporting/) — truy cập 2026-07-14); **Trace:** TA-DOC-01, TA-DOC-02. |
| Reproducibility (7%) | 5/5 | merged/effective config + generated scripts/artifacts. **DOC** ([artifacts](https://gettaurus.org/docs/ArtifactsDir/) — truy cập 2026-07-14); **Trace:** TA-DOC-01, TA-DOC-02. |
| Local/offline (5%) | 4/5 | Local default/disable downloads; pre-cache stack. **DOC + ASSUMPTION** ([Cloud](https://gettaurus.org/docs/Cloud/), [config](https://gettaurus.org/docs/ConfigSyntax/) — truy cập 2026-07-14); **Trace:** TA-DOC-01, TA-DOC-02. |
| AI-assisted potential (7%) | 4/5 | YAML/agent guidance; tool không AI, generated plan needs review. **ASSUMPTION** ([CLAUDE.md](https://github.com/Blazemeter/taurus/blob/master/CLAUDE.md) — truy cập 2026-07-14); **Trace:** TA-DOC-01, TA-DOC-02. |
| Classroom suitability (5%) | 3/5 | Orchestration lesson tốt; dễ che JMeter/setup semantics. **ASSUMPTION**; **Trace:** TA-DOC-01, TA-DOC-02. |
| Community (0%) | 4/5 | Current docs/repo/support forum/release activity; không vào Weighted Score. **DOC** ([docs](https://gettaurus.org/docs/Index/), [repo](https://github.com/Blazemeter/taurus) — truy cập 2026-07-14); **Trace:** TA-DOC-01, TA-DOC-02. |

**Weighted Score provisional: 83.4/100, conditional on JMeter executor.** Không diễn giải là Taurus phát tải tốt hơn/kém hơn engine độc lập.

**16. Kết luận sơ bộ.** **Orchestration framework.** Giữ Taurus để minh họa unified YAML, pass/fail/reporting và CI orchestration; không chọn như load generator thứ hai. Nếu dùng JMeter executor, mọi claim execution/capacity phải ghi **Taurus + JMeter + version/plugins/JVM**.

**17. Câu hỏi phản biện.**

<details>
<summary><strong>Câu hỏi phản biện</strong></summary>

### Câu 1. Taurus có phải load generator không?

**Trả lời:** Không trong cách phân loại này; Taurus orchestrate executor. Với executor JMeter, JMeter mới thực thi request/phát tải. ([JMeter executor](https://gettaurus.org/docs/JMeter/) — truy cập 2026-07-14)

### Câu 2. Có thể so raw throughput Taurus trực tiếp với k6 không?

**Trả lời:** Không công bằng nếu không ghi underlying executor/version/plugins và không đo abstraction overhead; phải so tổ hợp Taurus+engine trên cùng logical workload.

### Câu 3. Một YAML có semantics giống nhau trên mọi executor không?

**Trả lời:** Không; supported settings/data/assertions và translation phụ thuộc executor. ([Execution settings](https://gettaurus.org/docs/ExecutionSettings/), [Data sources](https://gettaurus.org/docs/DataSources/) — truy cập 2026-07-14)

### Câu 4. Taurus có tự chạy offline sau pip install không?

**Trả lời:** Không bảo đảm; nó có thể auto-download JMeter/plugins. Cần pre-cache/pin và TAURUS_DISABLE_DOWNLOADS để phát hiện download. ([JMeter](https://gettaurus.org/docs/JMeter/), [Config syntax](https://gettaurus.org/docs/ConfigSyntax/) — truy cập 2026-07-14)

### Câu 5. Chỉ giữ smoke.yml có đủ reproducibility không?

**Trả lời:** Không; cần merged/effective config, generated JMX, engine/plugin versions, logs/JTL, exit và environment metadata. ([Artifacts](https://gettaurus.org/docs/ArtifactsDir/) — truy cập 2026-07-14)

</details>

---

# 8. Phân loại và sàng lọc

## 8.1. Phân nhóm theo vai trò

| Nhóm công cụ | Công cụ | Vai trò phù hợp trong khảo sát | Quyết định vòng đầu | Lý do theo phạm vi T05 |
|---|---|---|---|---|
| GUI/Test Plan và Enterprise Performance Testing | Apache JMeter | Traditional, visual Test Plan; chạy tải bằng CLI | **Main candidate** | Local, open-source, flow/state/assertion/report đủ sâu và có giá trị giảng dạy GUI → CLI. |
| GUI/Test Plan và Enterprise Performance Testing | Silk Performer | Enterprise modelling và analysis | **Survey-only** | Capability đáng ghi nhận; public access, Windows-centric setup và evidence hiện hành cần xác minh thêm trước activity. |
| GUI/Test Plan và Enterprise Performance Testing | NeoLoad | Enterprise no-code/as-code, analytics và AI-related workflow | **Survey-only / enterprise alternative** | Current platform có capability rộng; licence/account và classroom Reproducibility khác đáng kể open-source CLI. |
| GUI/Test Plan và Enterprise Performance Testing | OpenText Professional Performance Engineering (LoadRunner Professional) | Enterprise protocol breadth; VuGen–Controller–Analysis | **Backup / enterprise reference** | Phù hợp enterprise use case nhưng setup/access/scope lớn cho activity ngắn; tên hiện hành phải được trình bày cùng tên quen dùng LoadRunner Professional. |
| Developer-oriented/Test-as-Code | k6 | JavaScript protocol test, Checks/Thresholds, CI/CD | **Main candidate** | Text-as-code, local, workload executors rõ và thuận lợi cho AI-generated draft + human AI Audit. |
| Developer-oriented/Test-as-Code | Locust | Python user behaviour và distributed run | **Shortlist** | EShop fit cao và dễ mở rộng; vai trò code-first trùng phần lớn với k6 trong pair hai tool. |
| Developer-oriented/Test-as-Code | Gatling | Multi-language DSL; open/closed Workload Model | **Shortlist** | Capability và Reproducibility cao; build/DSL learning path cần đối chứng trong 25 phút. Không dùng nhận định lỗi thời “chỉ có Scala”. |
| Developer-oriented/Test-as-Code | Artillery | YAML/JavaScript, arrival-oriented scenarios | **Shortlist** | Activity nhanh, CI tốt; workflow code/config-first trùng mục tiêu chính với k6, dù vẫn là đối chứng mạnh. |
| Cloud-Based Service | Loader.io | Tạo load cloud nhanh vào verified public host | **Survey-only / cloud supporting tool** | Free plan có ích cho demo cloud nhưng service chạy từ cloud và yêu cầu host verification, nên không phù hợp EShop chỉ ở localhost/private network. |
| Lightweight HTTP Benchmark | ApacheBench | One-endpoint concurrency benchmark | **Supporting benchmark tool** | Lệnh rất ngắn và có output percentile/requests-per-second; không biểu diễn full stateful journey. |
| Lightweight HTTP Benchmark | wrk | High-throughput HTTP benchmark; Lua extension | **Supporting benchmark tool** | Hữu ích kiểm tra endpoint/load-generator ceiling; native workload/session/assertion không tương đương full tool. |
| Lightweight HTTP Benchmark | Siege | HTTP stress/regression với URL list | **Supporting benchmark tool** | Nhiều URL, delay và cookie có ích cho quick exercise; không phải lựa chọn chính cho correlation/business gate. |
| Lightweight HTTP Benchmark | Vegeta | Constant-rate HTTP attack và raw result pipeline | **Supporting benchmark tool** | Rất tốt cho rate-controlled endpoint experiment; user journey/state cần orchestration ngoài. |
| Distributed Load Testing | Tsung | Erlang/XML distributed multi-protocol load | **Survey-only** | Distributed architecture có giá trị khi một generator là bottleneck; có thể vượt nhu cầu EShop local và tăng setup/learning cost. |
| Orchestration/Automation Framework | Taurus | YAML orchestration, executor abstraction, pass/fail/reporting | **Orchestration framework** | Có thể bao JMeter/k6/Gatling và các executor khác; engine bên dưới mới tạo tải, nên không chọn như một load generator độc lập thứ hai. |

Các quyết định này là `[CHỈ KẾT LUẬN TỪ DESK RESEARCH]`. Ví dụ, official docs mô tả Taurus dùng executor và mặc định có thể dùng JMeter; vì vậy khi cấu hình `executor: jmeter`, JMeter mới là engine thực thi request ([Taurus Execution Settings](https://gettaurus.org/docs/ExecutionSettings/) — truy cập 2026-07-14). Loader.io yêu cầu đăng ký/xác minh target host và hiện chạy test từ Amazon US-east, nên localhost không phải target trực tiếp của cloud service ([Loader.io target verification](https://support.loader.io/article/20-verifying-an-app), [Loader.io pricing FAQ](https://loader.io/pricing) — truy cập 2026-07-14).

## 8.2. Áp dụng điều kiện loại trực tiếp

| Điều kiện | Tool bị ảnh hưởng trong bối cảnh hiện tại | Hệ quả có giới hạn |
|---|---|---|
| Không nhắm trực tiếp EShop local/private | Loader.io | Không deep-test nếu nhóm không có public staging host được phép và verification token. |
| Account/licence/trial làm audience khó tái tạo | Silk Performer, NeoLoad, LoadRunner Professional; Loader.io ở mức account | Giữ trong Desk Research/enterprise comparison; chỉ thực nghiệm nếu entitlement thật được lưu evidence. |
| Mismatch với multi-step stateful journey | ApacheBench, wrk, Vegeta; Siege ở mức một phần | Giữ làm supporting benchmark cho endpoint, không dùng thay full EShop Fit Test. |
| Setup/distributed scope vượt nhu cầu local | Tsung | Chỉ deep-test nếu generator ceiling hoặc learning objective phân tán được chứng minh. |
| Là orchestration layer, không phải engine độc lập trong cấu hình khảo sát | Taurus | Có thể dùng ở giai đoạn CI orchestration; không tính như một pair ngang hàng với k6. |
| Vai trò code-first bị trùng trong pair chỉ có hai tool | Locust, Gatling, Artillery | Giữ shortlist và chọn ít nhất một tool làm counterfactual Smoke Test; không gọi các tool này “yếu”. |

### Vì sao benchmark tool không phù hợp full EShop journey nhưng vẫn đáng giữ?

ApacheBench tập trung benchmark một URL với request count/concurrency và xuất bảng percentile/CSV ([ApacheBench manual](https://httpd.apache.org/docs/current/en/programs/ab.html) — truy cập 2026-07-14). wrk tập trung threads/connections/duration và có Lua callback để mở rộng ([wrk repository](https://github.com/wg/wrk) — truy cập 2026-07-14). Vegeta tối ưu constant request rate và raw result/report pipeline ([Vegeta repository](https://github.com/tsenart/vegeta) — truy cập 2026-07-14). Siege hỗ trợ nhiều URL, concurrency và random delay nhưng chính tài liệu cảnh báo simulated user không đồng nghĩa session người thật ([Siege README](https://www.joedog.org/siege/readme) — truy cập 2026-07-14). Các đặc điểm này phù hợp endpoint diagnostics; full login/cart/checkout cần state, correlation, unique data và business Checks nhất quán hơn.

## 8.3. Chất lượng evidence sau vòng 1

| Lớp evidence | Hiện có | Chưa có | Ảnh hưởng quyết định |
|---|---|---|---|
| Licence/access | Official pages/repositories cho phần lớn tool; một số enterprise entitlement không công khai đầy đủ | Trial approval, account screenshots, licence file thực tế | Không khẳng định audience chắc chắn truy cập được commercial tool. |
| Capability | Official reference/user manuals | Xác nhận feature hoạt động với version/máy nhóm | Có thể chấm DOC provisional, chưa kết luận usability. |
| EShop fit | Source-level Workload Model và placeholder flow | Validated routes, auth contract, test data, execution logs | Mọi EShop fit vẫn cần EXP. |
| Classroom | Getting-started/setup docs | Measured setup/activity time trên máy audience | Điểm Classroom suitability là ASSUMPTION có citation nền. |
| Performance | Không có | p50/p95/p99, Throughput, Error Rate, CPU/RAM | Không có cơ sở nói tool nào nhanh hoặc nhẹ hơn trong EShop. |

## 8.4. Câu hỏi phản biện

<details>
<summary><strong>Câu hỏi phản biện</strong></summary>

### Câu 1. Vì sao khảo sát 15 tool nhưng chỉ deep-test hai tool?

**Trả lời:** Desk Research trả lời breadth; deep-test trả lời validity với nguồn lực hữu hạn. Hai tool chính cùng một counterfactual shortlist tool phải chạy cùng Smoke Test để kiểm tra selection bias. Các tool không truy cập được vẫn được đánh giá DOC, không bị gán kết quả EXP giả.

### Câu 2. Commercial tool nhiều tính năng hơn có phải tốt hơn không?

**Trả lời:** Có thể tốt hơn cho enterprise protocol, governance hoặc analytics, nhưng “phù hợp nhất” phụ thuộc EShop, access, Reproducibility và 25-minute activity. Feature breadth không tự động thắng contextual fit.

### Câu 3. Tsung có cần thiết cho EShop local không?

**Trả lời:** Chưa có evidence cho thấy một generator không đủ. Tsung trở nên đáng deep-test khi load-generator CPU/network là bottleneck hoặc mục tiêu học là distributed testing; trước đó distributed XML/SSH là scope bổ sung.

### Câu 4. Taurus có phải load generator không?

**Trả lời:** Trong cấu hình dùng JMeter executor, không: Taurus orchestration/config/report/pass-fail, còn JMeter tạo request. Taurus có nhiều executor, nên phải ghi engine thật cho từng run.

</details>
---

# 9. Shortlist Comparison

## 9.1. Shortlist đề xuất

Shortlist sau vòng Desk Research gồm **Apache JMeter, k6, Locust, Gatling và Artillery**. Cả năm đều có thể mô hình HTTP user journey có state/data và chạy local; sự khác nhau quan trọng nằm ở authoring workflow, cách biểu diễn Workload Model, pass/fail semantics và learning value. Không công cụ nào trong shortlist đã được xác nhận bằng EXP trong tài liệu này.

| Công cụ | Workflow | Multi-step journey | Workload control | Assertions/Checks | Reporting | CI/CD | Reproducibility | Learning curve | AI-assisted potential | Classroom suitability | Weighted score | Evidence quality |
|---|---|---|---|---|---|---|---|---|---|---|---:|---|
| Apache JMeter | GUI component tree → `.jmx`; CLI cho load run ([official getting started](https://jmeter.apache.org/usermanual/get-started.html)) | Cookie manager, extractor, CSV, controller | Thread/ramp/timer; open model có phần experimental | Nhiều Assertion; CI gate cần thiết kế rõ | JTL/CSV + HTML dashboard | Headless CLI; threshold gate cần wrapper/post-processing đã audit | Tốt nếu pin Java/plugin/data; XML diff khó review hơn code | Trung bình | Trung bình: có thể hỗ trợ draft Groovy/XML nhưng audit khó hơn | Tốt nếu pre-install | **90,2/100** | DOC rộng; 0 EXP |
| k6 | JavaScript test-as-code ([official docs](https://grafana.com/docs/k6/latest/using-k6/)) | JS state, cookie jar, JSON extraction, SharedArray | VU/iteration/constant và ramping arrival rate ([scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/)) | Checks + Thresholds; threshold điều khiển exit | Summary, JSON/CSV/output, local dashboard | CLI + nonzero threshold exit + official integrations | Rất tốt khi pin binary/image/module/data | Thấp–trung bình với người biết JavaScript | Cao cho text draft/diff/AI Audit; k6 không phải AI tool | Tốt nếu dạy check ≠ threshold | **97,4/100** | DOC rộng; 0 EXP |
| Locust | Python classes/tasks; web UI hoặc headless ([official docs](https://docs.locust.io/en/stable/)) | Python control flow, per-user client/session | User count/spawn rate, custom shape, distributed | Python validation/catch-response; exit policy cấu hình | Web stats + CSV/history | Headless/config/exit controls | Rất tốt với Python environment pin | Thấp–trung bình với người biết Python | Cao cho readable Python; human audit bắt buộc | Tốt, web UI dễ quan sát | **90,8/100** | DOC rộng; 0 EXP |
| Gatling | Java/JavaScript/TypeScript/Kotlin/Scala DSL; không đánh giá theo stereotype Scala-only ([official repository](https://github.com/gatling/gatling)) | Session/feeders/checks và scenario DSL | Open/closed injection, ramp/rate/stress peak ([injection docs](https://docs.gatling.io/concepts/injection/)) | Checks + global assertions | Local report/output theo edition | Build-tool/CLI integrations | Rất tốt với project/dependency pin | Trung bình do DSL/project setup | Cao với text DSL, nhưng generated code vẫn cần audit | Cần đo activity time | **90,2/100** | DOC rộng; 0 EXP |
| Artillery | YAML test definition + JavaScript extension ([core concepts](https://www.artillery.io/docs/get-started/core-concepts)) | Scenario flow, capture, variables/cookies | Arrival phases, ramp, fixed arrival count, cap VUs ([test script](https://www.artillery.io/docs/reference/test-script)) | `expect` request checks + `ensure` metric policy ([expect](https://www.artillery.io/docs/reference/extensions/expect), [ensure](https://www.artillery.io/docs/reference/extensions/ensure)) | Console/metrics; export/cloud options theo cấu hình | CLI; `ensure` có nonzero exit | Tốt khi pin Node/package lock/plugins | Thấp–trung bình | Cao cho YAML/JS draft; logic có thể bị phân tán giữa config/hooks | Tốt nếu dependency cache sẵn | **86,8/100** | DOC rộng; 0 EXP |

> Điểm trên được tính từ 12 tiêu chí và hiện chỉ dựa trên DOC/ASSUMPTION. Chênh lệch nhỏ không được diễn giải là khác biệt empirical trước EXP; Community là 0% theo quy ước §6.2.

## 9.2. Vì sao không chọn từng ứng viên vào pair chính?

### Vì sao chưa chọn Locust?

Locust là ứng viên mạnh: Python mô tả behaviour, `HttpUser` giữ session, có headless/distributed execution và CSV stats ([Locust documentation](https://docs.locust.io/en/stable/) — truy cập 2026-07-14). Trong pair chỉ có hai tool, nó trùng vai trò test-as-code/local/CI với k6. k6 được ưu tiên provisional vì Scenarios, Checks và Thresholds tạo câu chuyện trực tiếp hơn cho AI-generated JavaScript draft → human audit → pipeline gate. Nếu nhóm/audience thành thạo Python hơn JavaScript hoặc cần extension bằng Python library, Locust có thể thay k6 sau EXP; đây không phải kết luận Locust kém.

### Vì sao chưa chọn Gatling?

Gatling có workload modelling rất mạnh, phân biệt open/closed model và hiện hỗ trợ nhiều SDK gồm JavaScript/TypeScript, Java, Kotlin và Scala ([Gatling repository](https://github.com/gatling/gatling), [workload models](https://docs.gatling.io/testing-concepts/workload-models/) — truy cập 2026-07-14). Nó trùng vai trò code-first với k6; project/DSL/build setup và activity time cần EXP. Không được loại Gatling bằng lý do lỗi thời “chỉ dùng Scala”. Nếu Smoke Test cho thấy audience hoàn thành Gatling nhanh và report/DSL mang learning value tốt hơn, shortlist decision phải mở lại.

### Vì sao chưa chọn Artillery?

Artillery có YAML scenario, arrival phases, HTTP capture và plugin `expect`/`ensure`, nên rất phù hợp làm counterfactual classroom tool ([Artillery test script](https://www.artillery.io/docs/reference/test-script), [HTTP engine](https://www.artillery.io/docs/reference/engines/http) — truy cập 2026-07-14). Nó không được chọn provisional vì vai trò YAML/JavaScript developer workflow chồng lấn với k6, trong khi pair cần tương phản rõ với JMeter. Trade-off cần test là Artillery có thể nhanh hơn cho YAML activity nhưng logic phức tạp có thể tách qua YAML, processor/hooks và plugin. Nhóm nên Smoke Test Artillery cùng JMeter/k6 để tránh hợp thức hóa quyết định sẵn có.

### Vì sao chưa chọn LoadRunner Professional?

Tên hiện hành trên docs là **OpenText Professional Performance Engineering**, với VuGen để phát triển script, Controller để tổ chức/chạy/monitor scenario và Analysis để phân tích ([OpenText 26.1 help](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/WelcomeContent/c_Welcome.htm) — truy cập 2026-07-14). Protocol breadth và enterprise workflow là điểm mạnh. Tuy nhiên gated access/licence, Windows-heavy full setup, nhiều component và scope lớn làm Reproducibility trong lớp khác JMeter; official product page yêu cầu contact/trial ([product page](https://www.opentext.com/products/professional-performance-engineering) — truy cập 2026-07-14). Vì mục tiêu là EShop HTTP seminar, feature breadth không tự động bù access và activity time. Nếu trường có licence/lab image chuẩn, quyết định có thể thay đổi.

### Vì sao chưa chọn Taurus?

Taurus giải quyết abstraction/orchestration: YAML, executor selection, artefact collection và pass/fail. Official docs liệt kê JMeter, Gatling, Locust, Siege, ApacheBench, Tsung, k6 cùng các executor khác; default là JMeter ([Execution Settings](https://gettaurus.org/docs/ExecutionSettings/) — truy cập 2026-07-14). Vì vậy Taurus không tương đương hoàn toàn với k6 như một engine. Nó có thể là **lớp thứ ba hỗ trợ CI** sau khi chọn JMeter/k6, nhưng nếu đưa Taurus vào pair hai “load generators” sẽ trộn abstraction layer với executor và đếm trùng capability engine.

### Vì sao chưa chọn Tsung?

Tsung là distributed tool viết bằng Erlang, mô tả session trong XML và hỗ trợ nhiều protocol; distributed mode cần Erlang nodes/SSH và đồng bộ setup ([Tsung introduction](https://tsung.readthedocs.io/en/latest/introduction.html), [installation](https://tsung.readthedocs.io/en/latest/installation.html) — truy cập 2026-07-14). Chưa có evidence rằng EShop local cần nhiều generator. Vì thế distributed capability có thể vượt scope, còn XML/Erlang/SSH tăng learning/setup cost. Nếu JMeter/k6 generator saturate trước SUT hoặc seminar đặt mục tiêu distributed testing, Tsung phải được đánh giá lại.

### Vì sao chưa chọn NeoLoad?

NeoLoad hiện là enterprise platform có design/run/analyze, local/cloud architecture, CLI/CI và AI-related capabilities trong dòng 2026; official docs yêu cầu licence mode hoặc free/trial entitlement tương ứng ([NeoLoad current documentation](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/get_started.htm), [licence modes](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/manage_licenses.htm) — truy cập 2026-07-14). Tool có thể phù hợp enterprise hơn cặp open-source, nhưng classroom access và khả năng mọi audience tái tạo cần EXP/entitlement evidence. Do đó hiện giữ làm enterprise alternative, không hạ thấp capability.

## 9.3. EShop Fit Test Plan chung cho shortlist

**[KẾ HOẠCH THỰC NGHIỆM – CHƯA XÁC NHẬN]**

### A. Preconditions và guardrails

- Repository/commit: `[VERIFIED_ESHOP_REPOSITORY]` / `[VERIFIED_ESHOP_COMMIT]`.
- Target: `[VERIFIED_BASE_URL]`; chỉ staging/local environment được chủ hệ thống cho phép.
- Routes: `[VERIFIED_LOGIN_ENDPOINT]`, `[VERIFIED_PRODUCT_ENDPOINT]`, `[VERIFIED_CART_ENDPOINT]`, `[VERIFIED_CHECKOUT_ENDPOINT]`.
- Auth: `[VERIFIED_AUTH_MECHANISM]`; secret chỉ truyền qua environment/secret store, không commit.
- Data: account riêng cho mỗi Virtual User hoặc partition rõ; seeded product; idempotent/cleanup strategy; tuyệt đối không tạo order thật trên production.
- SLO/acceptance criteria: `[APPROVED_CHECK_POLICY]`, `[APPROVED_P95_MS]`, `[APPROVED_P99_MS]`, `[APPROVED_ERROR_RATE]`. Không tự đặt số rồi gọi là yêu cầu hệ thống.
- Environment: pin tool/runtime/dependency; ghi CPU/RAM/OS/network; không chạy SUT và generator cùng máy nếu muốn kết luận capacity, hoặc phải công bố interference và monitor cả hai.

### B. Logical journey dùng chung

1. Login bằng row dữ liệu riêng; assert protocol và business marker; extract token/cookie.
2. Browse/search product; assert danh sách đúng schema; chọn product ID hợp lệ.
3. View product; assert ID/field nghiệp vụ cần thiết.
4. Add cart với auth/session; assert cart mutation cho đúng user.
5. Checkout chỉ với dataset/cleanup được phê duyệt; extract order ID; assert business result.
6. Think time, pacing và retry policy lấy từ `[VERIFIED_ANALYTICS_OR_WORKLOAD_ASSUMPTION]`; không để tool tự retry khác nhau mà không công bố.

Tỷ lệ browse/detail/cart/checkout hiện có trong `Workload_Model.md` phải được coi là hypothesis cho đến khi có analytics/access-log hoặc stakeholder approval. Không dùng 60/25/10/5 như fact chỉ vì nó đã xuất hiện trong draft.

### C. Test profiles

| Profile | Workload placeholder | Mục tiêu | Dữ liệu phải thu |
|---|---|---|---|
| Smoke Test | 1 Virtual User, 1 iteration | Xác nhận script, correlation, Checks và evidence path | Per-step result, raw output, logs |
| Baseline/Load Testing | `[APPROVED_BASELINE_MODEL]` | Đo reference trong steady state | p50/p95/p99, Throughput, Error Rate, generator/SUT CPU-RAM |
| Spike Testing | `[APPROVED_SPIKE_MODEL]` | Quan sát phản ứng với arrival jump đã được phê duyệt | Recovery, dropped/failed work, resource timeline |
| Stress Testing | `[APPROVED_STRESS_MODEL_AND_STOP_RULE]` | Tìm giới hạn an toàn, có abort guard | Saturation signal, errors, queue/resource behaviour |
| Soak Testing | `[APPROVED_SOAK_DURATION]` | Tìm degradation/leak theo thời gian | Time series, memory/connection/db growth, errors |

### D. Ánh xạ implementation cho năm shortlist tool

| Tool | State/data | Workload | Checks/pass-fail | Raw evidence |
|---|---|---|---|---|
| JMeter | HTTP Cookie Manager, JSON extractor, CSV Data Set | Thread Group/timer hoặc open model đã ghi rõ; CLI run | Assertion; policy CI post-process được audit | `.jmx`, `.jtl`, `jmeter.log`, HTML report |
| k6 | Cookie jar, `Response.json()`, SharedArray/env | Scenarios với VU hoặc arrival-rate executor | `check()` + Thresholds | JS, raw JSON/CSV, stdout, dashboard export |
| Locust | `HttpUser.client`, Python state/test data | users/spawn rate/custom shape | `catch_response`/events + agreed exit policy | `locustfile.py`, CSV/history, logs |
| Gatling | Session, checks/save, feeders | `injectOpen`/`injectClosed` profile | Checks + assertions | Simulation source, dependency lock, results/report |
| Artillery | capture/variables/cookie + payload data | phases/scenario weights | `expect` + `ensure` | YAML/JS, package lock, JSON/report/logs |

### E. Fairness controls

1. Cùng logical transaction mix, data partitions, think time distribution, warm-up và measurement window.
2. Cùng open/closed semantics; không so “50 concurrent VUs” với “50 arrivals/s” như một tải.
3. Cùng timeout, redirect, keep-alive, TLS verification, response-body handling và retry policy hoặc ghi rõ khác biệt bắt buộc.
4. Chạy thứ tự được xoay/randomize nếu có nhiều lượt; lưu timestamp và background load.
5. Theo dõi generator saturation; nếu generator saturate thì kết quả là inconclusive cho SUT capacity.
6. Lặp lại đủ để đánh giá variability theo kế hoạch nhóm; không cherry-pick run đẹp nhất.
7. Report both protocol failures và business failures; HTTP 200 không tự động là checkout thành công.

### F. Tiêu chí ra quyết định sau EXP

- Script thể hiện đúng logical workload và auth/data correlation.
- Không có endpoint/assumption do AI tự tạo mà chưa xác minh.
- Raw artefact đủ tái chạy; pass/fail semantics được chứng minh bằng cả positive và deliberate-negative smoke case.
- Audience hoàn tất activity time-box 25 phút trên lab image.
- Kết luận pair được mở lại nếu Artillery/Locust/Gatling cho evidence tốt hơn rõ ràng hoặc JMeter/k6 gặp blocker.

## 9.4. Câu hỏi phản biện

<details>
<summary><strong>Câu hỏi phản biện</strong></summary>

### Câu 1. Vì sao không chọn đúng hai tool có Weighted Score cao nhất?

**Trả lời:** Weighted Score không đo complementarity và có thể che blocker. Pair seminar cần hai cách tiếp cận tạo learning contrast; điểm vẫn là input nhưng không phải thuật toán quyết định duy nhất.

### Câu 2. Vì sao complementarity quan trọng?

**Trả lời:** Nó cho phép cùng Workload Model được triển khai bằng visual/Test Plan và code-first, từ đó dạy rõ model quan trọng hơn syntax/tool và tạo một AI Audit đối chiếu được.

### Câu 3. Có thiên vị khi chọn Artillery làm counterfactual thay vì chạy cả năm tool không?

**Trả lời:** Có rủi ro; vì vậy lý do chọn counterfactual phải công bố (gần classroom/code-first nhất và đã có ownership trong nhóm). Nếu thời gian cho phép, chạy cùng one-request Smoke Test cho cả năm; chỉ full EShop Fit Test mới giới hạn.

### Câu 4. k6 có phải AI tool không?

**Trả lời:** Không. AI chỉ draft/analyze/audit text; k6 là deterministic load-testing engine. Endpoint, auth, Workload Model, Checks và Thresholds phải được con người xác minh.

</details>

---

# 10. Lý do chọn Apache JMeter và k6

## 10.1. Kết luận có giới hạn

Trong bối cảnh **Seminar T05, EShop HTTP/API, classroom activity tối đa 25 phút, local Reproducibility và mục tiêu traditional + AI-augmented**, evidence DOC hiện tại dẫn đến cặp **Apache JMeter + k6** như một lựa chọn **provisional**. Kết luận không có nghĩa đây là hai tool tốt nhất cho mọi dự án, cũng không chứng minh tool nào tạo tải “nhanh hơn”. Quyết định phải mở lại nếu EXP cho thấy blocker, workload semantics không tương đương hoặc một shortlist alternative tạo evidence/learning value tốt hơn.

## 10.2. Apache JMeter — đại diện GUI/Test Plan

1. **Visual/Test Plan:** GUI biểu diễn Thread Group, Sampler, Timer, Config Element, Post-Processor và Assertion thành một cây có thể dùng để giảng mối quan hệ giữa workload, request, correlation và validation ([JMeter Component Reference](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14).
2. **Đúng workflow vận hành:** Apache hướng dẫn dùng GUI để build/debug và CLI mode để chạy Load Testing; lệnh CLI có thể ghi JTL/CSV và tạo HTML report ([Getting Started](https://jmeter.apache.org/usermanual/get-started.html), [Dashboard report](https://jmeter.apache.org/usermanual/generating-dashboard.html) — truy cập 2026-07-14).
3. **EShop primitives:** HTTP Request, Cookie Manager, CSV Data Set, JSON/extractor và Assertions đủ để mô hình login → product → cart → checkout ở protocol level ([Component Reference](https://jmeter.apache.org/usermanual/component_reference.html) — truy cập 2026-07-14).
4. **Giá trị evidence:** `.jmx`, `.jtl`, `jmeter.log` và HTML report có thể lưu cùng Git commit/config để tái kiểm toán.
5. **Giới hạn phải dạy:** `.jmx` là XML verbose nên code review/diff khó hơn source code; GUI/listener tiêu thụ tài nguyên và không nên dùng cho load run lớn; Thread Group concurrency không mặc nhiên là arrival rate; core CLI cần một policy rõ để biến sample failures/SLO thành pipeline gate. Các điểm cuối là lý do chấm có điều kiện, không phải phủ nhận JMeter.

## 10.3. k6 — đại diện test-as-code và AI Audit

1. **Code-first:** k6 dùng JavaScript runtime riêng và script text phù hợp Git/code review; runtime không phải Node.js nên module/npm assumption phải kiểm tra ([k6 modules](https://grafana.com/docs/k6/latest/using-k6/modules/) — truy cập 2026-07-14).
2. **Workload Model rõ:** Scenarios/executors tách VU/iteration và constant/ramping arrival rate, giúp biểu diễn open/closed intent thay vì chỉ đặt concurrency ([k6 Scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/) — truy cập 2026-07-14).
3. **Checks và Thresholds:** Checks ghi nhận business/protocol conditions nhưng không tự fail process; Thresholds định nghĩa pass/fail và nonzero exit cho CI/CD ([Checks](https://grafana.com/docs/k6/latest/using-k6/checks/), [Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/) — truy cập 2026-07-14).
4. **Evidence và automation:** local CLI, raw JSON/CSV, outputs và dashboard/custom summary tạo đường pipeline/review gọn ([Results output](https://grafana.com/docs/k6/latest/get-started/results-output/) — truy cập 2026-07-14).
5. **AI-assisted workflow:** JavaScript/HAR-derived draft dễ đọc và diff; nhưng HAR converter chỉ là điểm bắt đầu, còn endpoint, token, data, think time, scenario distribution và Thresholds phải human audit ([HAR converter](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-har-converter/) — truy cập 2026-07-14). k6 **không phải AI tool**.
6. **Giới hạn phải dạy:** yêu cầu coding; JavaScript runtime khác Node.js; generated script có thể syntactically valid nhưng sai Workload Model; Checks không thay Thresholds; browser VU và protocol VU có footprint/mục tiêu khác nhau.

## 10.4. Giá trị bổ sung của cặp công cụ

| Learning objective | Apache JMeter | k6 | Giá trị khi đặt cạnh nhau |
|---|---|---|---|
| Authoring | GUI component/Test Plan; XML artefact | JavaScript test-as-code | Audience thấy cùng journey có thể được biểu diễn trực quan hoặc bằng code. |
| Load execution | GUI để debug, CLI để load | CLI-first | Tách authoring UX khỏi nguyên tắc chạy headless có kiểm soát. |
| State/data | Manager/extractor/CSV/variables | Cookie jar/JSON/SharedArray/JS state | So sánh correlation theo component với correlation theo code. |
| Validation | Assertions làm sample pass/fail; CI gate cần policy thêm | Checks + Thresholds tách functional signal khỏi acceptance policy | Dạy rõ HTTP 200, business success và performance SLO là ba lớp khác nhau. |
| Reporting | JTL/CSV + generated HTML | Summary/raw output/dashboard/integration | Cùng metrics nhưng artefact và pipeline khác nhau. |
| Reproducibility | Pin Java/JMeter/plugin/JMX/data | Pin k6/image/module/JS/data | Cho thấy file có trong Git chưa đủ; runtime và environment cũng phải pin. |
| AI usage | AI có thể giải thích/draft element/Groovy nhưng XML cần audit chặt | AI draft JavaScript/HAR conversion dễ diff | Tạo AI Audit có đối chứng; không dùng output AI làm ground truth. |
| Teaching | Traditional visual decomposition | Automation/code review | Bao phủ classroom learning và CI/CD mà không giả định một workflow đúng tuyệt đối. |

Hai tool phải triển khai **cùng logical Workload Model**, không tự tạo hai workload khác nhau rồi so metrics. Nếu JMeter dùng closed concurrency còn k6 dùng arrival rate, đó là hai experiment khác; pair chỉ có giá trị khi semantics được chuẩn hóa hoặc khác biệt được cố ý nghiên cứu.

## 10.5. Ba lý do ngắn dùng trực tiếp trong proposal/slide

- **Best fit for EShop:** Cả Apache JMeter và k6 đều có primitive cho HTTP/API, session/token, parameterization, multi-step journey, validation và local execution; mức fit cuối cùng vẫn cần EShop Fit Test.
- **Complementary approaches:** JMeter đại diện visual/Test Plan và k6 đại diện test-as-code/CI, giúp trình bày cùng Workload Model qua hai workflow bổ sung thay vì hai tool gần như trùng vai trò.
- **Clear AI-assisted workflow:** AI có thể draft k6 JavaScript/HAR conversion, sau đó con người audit endpoint, correlation, think time, data, Checks, Thresholds và đối chiếu với JMeter Test Plan; không gọi k6 là AI tool.

## 10.6. AI-generated draft → human audit → execution evidence

```text
Verified EShop contract + approved Workload Model
        ↓
AI tạo bản nháp k6 (không có quyền tự xác nhận)
        ↓
Static AI Audit: endpoint, secret, auth, token, data, think time,
scenario weights, executor, Checks, Thresholds, retry, destructive action
        ↓
Human sửa và code review; đối chiếu JMeter logical Test Plan
        ↓
1-VU Smoke Test + deliberate-negative Checks/Thresholds
        ↓
Approved Load Test với guardrails
        ↓
Raw results + SUT/generator telemetry + limitations
```

### AI Audit Failure Modes bắt buộc

| Failure Mode | Dấu hiệu | Cách phát hiện trước load | Mitigation |
|---|---|---|---|
| Hallucinated endpoint/method | 404/405 hoặc request sai nghiệp vụ | Diff với verified route/API contract | Chỉ dùng `[VERIFIED_*]`; source/API-owner review |
| Hard-coded token/cookie | 401/403, cross-user state, secret leak | Secret scan; inspect per-VU state | Correlate tại runtime; env/secret store; redact artefact |
| Missing think time/pacing | Throughput phi thực tế, generator/SUT saturation sớm | Review sleep/pacing và iteration duration | Dùng distribution đã được phê duyệt; báo cả achieved rate |
| Sai open/closed model | Arrival rate tụt khi Response Time tăng hoặc concurrency phình ngoài ý định | Review executor/Thread Group semantics | Chọn model theo hệ thống; ghi target và achieved workload |
| Missing business Checks | HTTP 200 nhưng body/order/cart sai | Deliberate-negative case; inspect business marker | Check protocol + schema + business condition |
| Threshold không gắn SLO | Build pass/fail tùy tiện | Trace mỗi threshold về requirement/baseline approval | Dùng `[APPROVED_*]`; version SLO cùng test |
| Dùng chung account/product state | Duplicate cart/order, lock/race giả | Review data partition và cleanup | Unique/partitioned data; idempotency/cleanup |
| Unbounded destructive checkout | Tạo nhiều order thật | Threat/safety review trước run | Staging only, cap/abort rule, seeded cleanup |
| Chỉ báo average | Tail Latency bị che | Kiểm tra p50/p95/p99 và distribution | Báo percentile + time series + error cohorts |
| Generator bottleneck bị gán cho SUT | CPU/RAM generator cao, dropped iterations | Monitor generator và achieved load | Tách máy/giảm load/phân tán rồi chạy lại |

## 10.7. Counterfactual check và trạng thái quyết định

> **Câu hỏi bắt buộc:** “Nếu bỏ tên JMeter và k6 khỏi quyết định ban đầu, evidence hiện có có thật sự dẫn đến việc chọn lại đúng cặp công cụ này không?”

**Trả lời hiện tại:** DOC cho thấy đây là một cặp hợp lý vì JMeter có visual/Test Plan/local depth còn k6 có code-first/Scenarios/Checks/Thresholds/CI và AI Audit rõ. Tuy nhiên câu trả lời **chưa chắc chắn**, vì chưa có EXP về setup time, EShop correlation, classroom completion, generator footprint và counterfactual Artillery/Locust/Gatling. Do đó:

- Quyết định là **provisional**, không phải “best tools”.
- Bắt buộc chạy cùng one-request Smoke Test cho ít nhất JMeter, k6 và Artillery (hoặc shortlist alternative được nhóm biện minh).
- Bắt buộc chạy cùng EShop logical journey cho JMeter và k6; nếu có blocker, mở rộng cho counterfactual.
- Re-score các ô Learning curve, Reproducibility và Classroom suitability bằng EXP; giữ DOC/EXP riêng, không ghi đè lịch sử.
- Chỉ finalize pair sau khi evidence register có raw artefact và review sign-off.

## 10.8. Câu hỏi phản biện

<details>
<summary><strong>Câu hỏi phản biện</strong></summary>

### Câu 1. Vì sao JMeter và k6 được chọn nhưng không được gọi là tốt nhất?

**Trả lời:** “Tốt nhất” cần một tập dự án/môi trường rộng hơn. Khảo sát chỉ tối ưu cho T05, EShop, access, 25 phút, Reproducibility và learning contrast; decision còn provisional vì 0 EXP.

### Câu 2. Nếu k6 có điểm cao hơn JMeter, tại sao vẫn cần JMeter?

**Trả lời:** Điểm cao không thay visual/Test Plan learning objective. JMeter tạo contrast truyền thống và cho phép audience thấy component/correlation/report workflow khác code-first; pair value không bằng tổng hai score độc lập.

### Câu 3. AI capability được chấm thế nào mà không gọi k6 là AI tool?

**Trả lời:** Điểm đo mức artefact dễ draft/diff/audit và khả năng áp human control, không đo một native AI engine. AI-assisted potential là contextual inference, luôn cần audit và EXP.

### Câu 4. Làm sao chứng minh hai tool chạy cùng workload?

**Trả lời:** Lập tool-neutral transaction model, chuẩn hóa open/closed semantics, data, think time, retry, timeout và measurement window; sau run so target với achieved workload trước khi so Response Time/Throughput/Error Rate.

### Câu 5. Evidence nào có thể đảo quyết định?

**Trả lời:** Không hoàn tất correlation, CI gate không tái lập, activity vượt 25 phút, generator saturation, access blocker hoặc counterfactual tạo evidence/learning value tốt hơn là các lý do hợp lệ để re-open selection.

</details>

---

# Appendix A — Full Scoring Matrix

## A.1. Cách đọc ma trận

Ma trận dưới đây là bản tổng hợp số học của 15 bảng điểm tại §7. Thứ tự hàng giữ nguyên danh sách công cụ trong đề bài, **không phải bảng xếp hạng tuyệt đối**. Tất cả điểm hiện là provisional từ `DOC` và, với các tiêu chí mang tính bối cảnh như Learning curve, AI-assisted potential và Classroom suitability, có thêm `ASSUMPTION`; chưa có ô nào được nâng thành `EXP`.

Các ký hiệu tiêu chí và trọng số:

| Mã | Tiêu chí | Trọng số |
|---|---|---:|
| C1 | Cost | 8% |
| C2 | Learning curve | 8% |
| C3 | EShop fit | 15% |
| C4 | Multi-step user journey | 12% |
| C5 | Workload modelling | 10% |
| C6 | Assertions/Checks | 8% |
| C7 | Reporting/raw output | 8% |
| C8 | CI/CD | 7% |
| C9 | Reproducibility | 7% |
| C10 | Local/offline suitability | 5% |
| C11 | AI-assisted potential | 7% |
| C12 | Classroom suitability | 5% |
| Q | Community/documentation maturity, chỉ dùng định tính | 0% |

Mỗi `C1…C12` dùng thang 1–5 theo anchor tại §6.3. Công thức chuẩn hóa:

\[
\text{Weighted Score}=\sum_{i=1}^{12}\left(\frac{\text{score}_i}{5}\times\text{weight}_i\right)
\]

Tổng trọng số là 100%; kết quả làm tròn một chữ số thập phân. `Q` được giữ để phục vụ Stage S1 nhưng không đi vào công thức vì đề bài không cấp trọng số Community.

## A.2. Full Scoring Matrix

| # | Công cụ | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | Q (0%) | Weighted Score /100 |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Apache JMeter | 5 | 3 | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 5 | 3 | 4 | 5 | **90,2** |
| 2 | Silk Performer | 2 | 2 | 4 | 5 | 5 | 4 | 5 | 4 | 3 | 4 | 3 | 2 | 3 | **74,8** |
| 3 | Artillery | 4 | 4 | 5 | 4 | 4 | 4 | 4 | 5 | 5 | 4 | 4 | 5 | 4 | **86,8** |
| 4 | k6 | 5 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 5 | **97,4** |
| 5 | Locust | 5 | 4 | 5 | 5 | 4 | 4 | 4 | 4 | 5 | 5 | 5 | 4 | 5 | **90,8** |
| 6 | Gatling | 4 | 3 | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 4 | 3 | 5 | **90,2** |
| 7 | Loader.io | 3 | 5 | 3 | 3 | 4 | 2 | 3 | 4 | 3 | 1 | 3 | 4 | 3 | **64,0** |
| 8 | Siege | 5 | 4 | 3 | 2 | 3 | 2 | 2 | 2 | 4 | 5 | 3 | 4 | 3 | **62,2** |
| 9 | Vegeta | 5 | 4 | 3 | 1 | 4 | 1 | 5 | 3 | 5 | 5 | 4 | 5 | 4 | **70,2** |
| 10 | wrk | 5 | 3 | 2 | 2 | 3 | 2 | 3 | 2 | 4 | 5 | 3 | 3 | 4 | **58,2** |
| 11 | NeoLoad | 2 | 4 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 4 | 5 | 2 | 4 | **87,6** |
| 12 | ApacheBench | 5 | 5 | 2 | 1 | 2 | 1 | 3 | 2 | 4 | 5 | 2 | 5 | 5 | **56,0** |
| 13 | OpenText LoadRunner Professional | 4 | 2 | 5 | 5 | 5 | 5 | 5 | 4 | 3 | 5 | 4 | 2 | 4 | **85,0** |
| 14 | Tsung | 5 | 2 | 5 | 5 | 5 | 4 | 4 | 3 | 4 | 4 | 3 | 2 | 3 | **81,0** |
| 15 | Taurus | 5 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 5 | 4 | 4 | 3 | 4 | **83,4** |

## A.3. Kiểm tra chéo và giới hạn diễn giải

- Các vector và phép tính đã được recompute độc lập từ cùng bộ trọng số; tổng tại đây phải khớp bảng chi tiết của từng profile tại §7.
- Điểm cao không vô hiệu hóa điều kiện loại trực tiếp ở §8.2. Ví dụ, NeoLoad có capability rộng nhưng entitlement/classroom access vẫn chưa được chứng minh; Taurus có điểm orchestration tốt nhưng không được tính như một load engine độc lập; benchmark tools không được dùng thay full stateful EShop journey.
- Không dùng chênh lệch vài điểm thập phân để suy ra khác biệt performance runtime. Tài liệu chưa có kết quả p95/p99, Throughput, Error Rate hay CPU/RAM cho bất kỳ tool nào.
- Pair selection ở §10 xét thêm role complementarity, access, evidence quality và learning objective; vì vậy không đơn giản lấy hai Weighted Score cao nhất.
- Sau Smoke Test/EShop Fit Test, mọi thay đổi điểm phải ghi evidence ID, scorer, ngày, before/after và lý do theo quy tắc Appendix D.5.

## A.4. Trạng thái sàng lọc theo bối cảnh T05

| Công cụ/nhóm | Trạng thái sau Desk Research | Điều kiện để thay đổi trạng thái |
|---|---|---|
| Apache JMeter, k6 | Main candidates; pair provisional | Hoàn tất Smoke Test, same-journey Fit Test và negative controls với evidence có thể audit. |
| Locust, Gatling, Artillery | Shortlist/counterfactuals | Ít nhất một tool chạy cùng Smoke/Fit criteria; mở lại pair nếu evidence hoặc audience fit tốt hơn. |
| Silk Performer, NeoLoad, LoadRunner Professional | Enterprise references/survey-only trong lab hiện tại | Có entitlement/version/máy lab thật và hoàn thành Smoke Test tương đương. |
| Loader.io | Cloud supporting/survey-only | Có public staging target được phép, host verification và kiểm soát test window/load ceiling. |
| Siege, Vegeta, wrk, ApacheBench | Supporting endpoint benchmarks | Dùng cho endpoint/generator diagnostics; không nâng thành full-journey tool nếu chưa bổ sung state/correlation/business gates. |
| Tsung | Distributed survey-only | Chứng minh single-generator bottleneck hoặc distributed testing là learning objective. |
| Taurus | Orchestration framework | Ghi rõ executor/engine thật; đánh giá giá trị pipeline riêng, không double-count capability của engine. |


---

# Appendix B — Evidence Register

> **Phạm vi của register.** `Verified` chỉ có nghĩa nguồn official/primary được truy cập ngày 2026-07-14 trực tiếp hỗ trợ claim ở mức **Desk Research**. Nó không xác nhận khả năng chạy trên EShop, không thay thế kiểm tra entitlement tại thời điểm dùng, và không phải bằng chứng performance. `Partially verified` được dùng khi nguồn xác nhận phần chính nhưng còn pricing/licence entitlement, version skew, platform packaging hoặc exit semantics chưa khép kín. Các ID hậu tố `-EXP-01` bên dưới hiện có Type `EXP-PLAN`: đây chỉ là ô dành trước cho thí nghiệm, chưa phải `EXP` evidence.

## B.1. Evidence items theo công cụ

| ID | Công cụ | Claim/evidence item | Loại | Nguồn official/primary | Ngày truy cập | Trạng thái và giới hạn |
|---|---|---|---|---|---|---|
| JM-DOC-01 | Apache JMeter | JMeter là tool Java mã nguồn mở theo Apache License 2.0; yêu cầu Java 8+ và khuyến nghị GUI cho design/debug, non-GUI CLI cho load execution. | DOC | [Apache JMeter](https://jmeter.apache.org/); [Apache licences](https://www.apache.org/licenses/); [Getting Started](https://jmeter.apache.org/usermanual/get-started.html) | 2026-07-14 | **Verified** cho identity/licence/runtime path; official Docker image chưa được xác nhận trong nguồn đã kiểm. |
| JM-DOC-02 | Apache JMeter | Thread Group/timers/remote engines, assertions, JTL và HTML dashboard là các interface được tài liệu hóa; core CLI chưa cung cấp performance-threshold exit contract rõ trong nguồn đã kiểm. | DOC | [Component Reference](https://jmeter.apache.org/usermanual/component_reference.html); [Remote Testing](https://jmeter.apache.org/usermanual/remote-test.html); [Dashboard](https://jmeter.apache.org/usermanual/generating-dashboard.html) | 2026-07-14 | **Partially verified**: execution/reporting được xác nhận; CI threshold propagation còn cần negative experiment. |
| JM-EXP-01 | Apache JMeter | Smoke một GET read-only với status/body assertion, JTL, HTML report và một negative marker để quan sát failure propagation. | EXP-PLAN | Smoke Test Plan `§7.1`; Appendix C | — | **Not executed — [CẦN THỰC NGHIỆM]**; chưa có JTL, HTML, stdout/stderr hoặc exit code quan sát được. |
| SP-DOC-01 | Silk Performer | Silk Performer là suite thương mại của OpenText; tài liệu 21.0 mô tả Windows-centric Workbench/Controller và Evaluation 10 VU, nhưng hai tài liệu public mâu thuẫn 30/45 ngày và giá không công khai. | DOC | [OpenText Marketplace](https://marketplace.opentext.com/appdelivery/content/silk-performer); [Installation Guide 21.0](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-installationguide-en.pdf); [Workbench Help 21.0](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-workbenchhelp-en.pdf) | 2026-07-14 | **Partially verified**: product/platform/10 VU được ghi nhận; duration, entitlement hiện hành và commercial price phải xác minh trực tiếp. |
| SP-DOC-02 | Silk Performer | Workload models, per-VU state/parsing, Web verification, result monitoring và CLI automation được tài liệu hóa; public exit-code contract chưa đủ rõ. | DOC | [Workload models](https://www.microfocus.com/documentation/silk-performer/195/en/silkperformer-195-webhelp-en/SILKPERF-390794D9-WORKLOADMODELS-CON.html); [Web verification tutorial](https://www.microfocus.com/documentation/silk-performer/210/en/silkperformer-210-webloadtestingtutorial-en.pdf); [CLI automation](https://www.microfocus.com/documentation/silk-performer/205/en/silkperformer-205-webhelp-en/GUID-BE43A9E4-6B4C-46CB-BCA9-6A3E7CE51F36.html) | 2026-07-14 | **Partially verified**: feature set được xác nhận từ official docs nhiều version; failure/exit propagation và protocol depth phải lab-test. |
| SP-EXP-01 | Silk Performer | Smoke Workbench/BDL một GET, content verification, Verification workload 1 VU/1 iteration và automation result folder. | EXP-PLAN | Smoke Test Plan `§7.2`; Appendix C | — | **Not executed — [CẦN THỰC NGHIỆM]**; chưa xác nhận installer, licence, report hoặc exit semantics. |
| AR-DOC-01 | Artillery | Local Artillery CLI là open-source, hỗ trợ Windows/macOS/Linux và official Docker image; repository có MPL-2.0 cùng licence nuance cho một số Azure modules. | DOC | [Artillery repository/licence notice](https://github.com/artilleryio/artillery); [Get Artillery](https://www.artillery.io/docs/get-started/get-artillery); [Docker](https://www.artillery.io/docs/docker) | 2026-07-14 | **Partially verified**: local access/platform được xác nhận; Azure-specific production/commercial licence phải được legal review theo deployment thật. |
| AR-DOC-02 | Artillery | Phases/scenarios, HTTP cookies/capture, `expect`, `ensure`, JSON output và CI guides được tài liệu hóa; local `artillery report` HTML đã bị loại khỏi current v2 path. | DOC | [Test scripts](https://www.artillery.io/docs/reference/test-script); [Expect](https://www.artillery.io/docs/reference/extensions/expect); [Ensure](https://www.artillery.io/docs/reference/extensions/ensure); [Run/output](https://www.artillery.io/docs/reference/cli/run); [Report command](https://www.artillery.io/docs/reference/cli/report) | 2026-07-14 | **Verified** cho documented execution/gate/output; Cloud report/account là đường riêng. |
| AR-EXP-01 | Artillery | Smoke một `arrivalCount: 1` GET với `expect`, strict `ensure`, raw JSON và exit code. | EXP-PLAN | Smoke Test Plan `§7.3`; Appendix C | — | **Not executed — [CẦN THỰC NGHIỆM]**; chưa quan sát plugin compatibility, result count hay exit code. |
| K6-DOC-01 | k6 | k6 local CLI dùng AGPL-3.0, có install path cho Linux/macOS/Windows, standalone binary và official `grafana/k6` image; Cloud là tùy chọn. | DOC | [k6 repository/licence](https://github.com/grafana/k6); [Install k6](https://grafana.com/docs/k6/latest/set-up/install-k6/); [Grafana pricing](https://grafana.com/pricing/) | 2026-07-14 | **Verified** cho local licence/platform/install; current Cloud allowance phải re-check trước khi dùng và không ảnh hưởng local smoke. |
| K6-DOC-02 | k6 | Scenarios cung cấp iteration/VU/arrival-rate executors; checks và thresholds tách biệt, threshold failure tạo non-zero exit; JSON/CSV và local web dashboard được tài liệu hóa. | DOC | [Scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/); [Checks](https://grafana.com/docs/k6/latest/using-k6/checks/); [Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/); [Results output](https://grafana.com/docs/k6/latest/get-started/results-output/); [Web dashboard](https://grafana.com/docs/k6/latest/results-output/web-dashboard/) | 2026-07-14 | **Verified** cho documented semantics; EShop correlation/data/workload correctness vẫn chưa được thực nghiệm. |
| K6-EXP-01 | k6 | Smoke `shared-iterations`, 1 VU/1 iteration, một GET, status check, thresholds và raw JSON. | EXP-PLAN | Smoke Test Plan `§7.4`; Appendix C | — | **Not executed — [CẦN THỰC NGHIỆM]**; chưa có raw record, summary hoặc exit code. |
| LO-DOC-01 | Locust | Locust là OSS MIT, cài bằng pip/uvx, có Windows troubleshooting và official `locustio/locust` Docker/Compose path; local/distributed OSS không cần SaaS account. | DOC | [Locust repository/licence](https://github.com/locustio/locust); [Installation](https://docs.locust.io/en/stable/installation.html); [Docker](https://docs.locust.io/en/stable/running-in-docker.html) | 2026-07-14 | **Verified** cho licence/install/platform path; reproducibility vẫn cần pin Python/dependencies/image digest. |
| LO-DOC-02 | Locust | `HttpUser`, validation bằng `catch_response`, headless execution, CSV artifacts, exit policy hooks, LoadTestShape và master/worker được tài liệu hóa. | DOC | [Writing a locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html); [Headless/CI](https://docs.locust.io/en/stable/running-without-web-ui.html); [Configuration/CSV](https://docs.locust.io/en/stable/configuration.html); [Distributed load](https://docs.locust.io/en/stable/running-distributed.html) | 2026-07-14 | **Verified** cho interface; p95/custom SLO gate và distributed data uniqueness cần code review/experiment. |
| LO-EXP-01 | Locust | Smoke một `HttpUser`/GET idempotent với `catch_response`, 1 user, short headless run, CSV và exit code. | EXP-PLAN | Smoke Test Plan `§7.5`; Appendix C | — | **Not executed — [CẦN THỰC NGHIỆM]**; loop 5 giây có thể phát hơn một request, nên chưa claim exactly-one-request. |
| GA-DOC-01 | Gatling | Gatling Community hỗ trợ Java/JavaScript/TypeScript/Kotlin/Scala; main project Apache-2.0 nhưng bundled Highcharts report module có licence riêng; JVM và current JS/npm routes có requirements khác nhau. Official install page và current JS/TS protocol guides hiện không nhất quán về protocol scope. | DOC | [Gatling repository](https://github.com/gatling/gatling); [Project licences](https://docs.gatling.io/project/licenses/project-licenses/); [Install local](https://docs.gatling.io/reference/deploy/install-local/); [gRPC JS/TS guide](https://docs.gatling.io/guides/use-cases/grpc-js/); [SSE reference](https://docs.gatling.io/reference/script/sse/); [MQTT reference](https://docs.gatling.io/reference/script/mqtt/protocol/) | 2026-07-14 | **Partially verified**: languages/platform/licence split được xác nhận; protocol/module/edition parity phải đối chiếu theo pinned setup thật. |
| GA-DOC-02 | Gatling | Open/closed injection, per-VU Session/feeders/checks, global assertions và static Community HTML report được tài liệu hóa; `simulation.log` không phải stable integration API. | DOC | [Injection](https://docs.gatling.io/concepts/injection/); [Session](https://docs.gatling.io/concepts/session/api/); [Assertions](https://docs.gatling.io/concepts/assertions/); [Community reports](https://docs.gatling.io/reference/stats/reports/oss/); [FAQ](https://docs.gatling.io/tutorials/faq/) | 2026-07-14 | **Verified** cho documented capability và limitation; EShop flow/current JS SDK phải smoke-test. |
| GA-EXP-01 | Gatling | Smoke current JavaScript SDK với `atOnceUsers(1)`, một GET, status check, global failed-request assertion, local HTML và exit code. | EXP-PLAN | Smoke Test Plan `§7.6`; Appendix C | — | **Not executed — [CẦN THỰC NGHIỆM]**; chưa xác nhận starter/Node compatibility, exact request count hoặc report path. |
| LI-DOC-01 | Loader.io | Loader.io là SaaS; Free/Pro limits được công bố, host phải verify và AWS generators không gọi trực tiếp localhost/private service. | DOC | [Loader.io pricing](https://loader.io/pricing); [Verify an app](https://support.loader.io/article/20-verifying-an-app); [Local services FAQ](https://support.loader.io/article/80-can-i-test-the-local-services-hosted-on-local-machine) | 2026-07-14 | **Verified** tại ngày truy cập; plan limits là temporally unstable và target ownership/public exposure phải re-check. |
| LI-DOC-02 | Loader.io | API v2 hỗ trợ create/run/stop/poll, ba test types và result summaries; documented error threshold dựa protocol, còn native CLI/exit gate và body assertion không được xác nhận. | DOC | [API v2](https://loader.io/docs/v2/); [Test types](https://support.loader.io/article/16-test-types); [Test results](https://support.loader.io/article/19-test-results); [Webhooks](https://support.loader.io/article/23-webhook) | 2026-07-14 | **Partially verified**: service/API behavior được mô tả; CI mapping, percentile/raw timing và negative-path behavior cần experiment. |
| LI-EXP-01 | Loader.io | Smoke host public đã được ủy quyền: verify token, một GET, `per-test`, total 15, duration 60 giây, poll result và kiểm error/timeout/network. | EXP-PLAN | Smoke Test Plan `§7.7`; Appendix C | — | **Not executed — [CẦN THỰC NGHIỆM]**; không có public target/authorization, result JSON hay cost/WAF observation. |
| SI-DOC-01 | Siege | Siege là OSS GPL-3.0 cho POSIX/UNIX; FAQ không hỗ trợ native Windows, còn repository có guide để tự build Docker image. | DOC | [Siege repository](https://github.com/JoeDog/siege); [COPYING](https://github.com/JoeDog/siege/blob/master/COPYING); [FAQ](https://www.joedog.org/siege/faq); [Dockerfile guide](https://github.com/JoeDog/siege/blob/master/Dockerfile.md) | 2026-07-14 | **Verified** cho licence/platform path; image tự build phải pin source/dependencies, không được gọi là registry release first-party. |
| SI-DOC-02 | Siege | CLI hỗ trợ concurrency/duration/repetition/delay, URL list, cookies, GET/POST và aggregate log; success là status dưới 400 và standard report không cung cấp business assertion/percentile dashboard. | DOC | [Siege manual](https://www.joedog.org/siege/manual); [Siege FAQ](https://www.joedog.org/siege/faq) | 2026-07-14 | **Verified** cho documented interface/semantics; CI gate/cookie isolation là wrapper responsibility. |
| SI-EXP-01 | Siege | Smoke 2 clients × 5 repetitions trên một GET với aggregate log, isolated HOME/cookie file và generator resource capture. | EXP-PLAN | Smoke Test Plan `§7.8`; Appendix C | — | **Not executed — [CẦN THỰC NGHIỆM]**; chưa xác nhận native/WSL/container route, transaction count hoặc errors. |
| VE-DOC-01 | Vegeta | Vegeta là OSS MIT; repository cung cấp release assets, install instructions và Dockerfile để tự build image; local binary không cần SaaS. | DOC | [Vegeta repository](https://github.com/tsenart/vegeta); [LICENSE](https://github.com/tsenart/vegeta/blob/master/LICENSE); [Install](https://github.com/tsenart/vegeta#install); [Dockerfile](https://github.com/tsenart/vegeta/blob/master/Dockerfile) | 2026-07-14 | **Verified**; binary/image provenance và checksum vẫn phải được lưu cho mỗi run. |
| VE-DOC-02 | Vegeta | `attack` hỗ trợ rate/duration/worker/connection controls; `report`, raw binary/JSON/CSV encoding và HTML plot tạo artifact chain; success là protocol 200–399, không phải business assertion/SLA gate. | DOC | [Attack](https://github.com/tsenart/vegeta#attack-command); [Report](https://github.com/tsenart/vegeta#report-command); [Encode](https://github.com/tsenart/vegeta#encode-command); [Plot](https://github.com/tsenart/vegeta#plot-command) | 2026-07-14 | **Verified** cho endpoint benchmark/report semantics; journey/correlation không được suy ra từ multiple targets. |
| VE-EXP-01 | Vegeta | Smoke target file một GET ở 2 request/s trong 10 giây, lưu `results.bin`, JSON report, optional HTML plot và exit của từng command. | EXP-PLAN | Smoke Test Plan `§7.9`; Appendix C | — | **Not executed — [CẦN THỰC NGHIỆM]**; “khoảng 20” chỉ là workload intent, chưa phải observed count. |
| WR-DOC-01 | wrk | `wrk` là OSS theo Modified Apache 2.0 License 2.0.1; build nhắm phần lớn hệ UNIX với GNU make/LuaJIT/OpenSSL, không có native Windows claim trong INSTALL. | DOC | [wrk repository](https://github.com/wg/wrk); [LICENSE](https://raw.githubusercontent.com/wg/wrk/master/LICENSE); [INSTALL](https://github.com/wg/wrk/blob/master/INSTALL) | 2026-07-14 | **Verified** cho source/licence/build path; Windows classroom path cần WSL/VM/custom container được pin. |
| WR-DOC-02 | wrk | CLI điều khiển threads/connections/duration/latency; Lua hooks đọc response và histogram nhưng state là per-thread, response parsing giảm load capacity và không có native threshold contract. | DOC | [wrk README](https://github.com/wg/wrk); [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) | 2026-07-14 | **Verified** cho documented capability/limitations; custom business gate và machine-readable output phải review/experiment. |
| WR-EXP-01 | wrk | Smoke `-t2 -c4 -d10s --latency` trên một GET, capture console/errors và client/SUT headroom. | EXP-PLAN | Smoke Test Plan `§7.10`; Appendix C | — | **Not executed — [CẦN THỰC NGHIỆM]**; chưa có latency distribution, socket-error count hoặc saturation evidence. |
| NL-DOC-01 | NeoLoad | NeoLoad là commercial Tricentis platform; Controller hỗ trợ Windows/Linux/macOS theo matrix và có agents/container deployment. Public pricing bắt đầu từ 20.000 USD/năm, nhưng exact Free run entitlement chưa rõ. | DOC | [NeoLoad product](https://www.tricentis.com/products/performance-testing-neoload); [Pricing](https://www.tricentis.com/products/performance-testing-neoload/pricing); [System requirements](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/system_requirements.htm); [Manage licences](https://docs.tricentis.com/neoload-latest/en-us/content/get_started/manage_licenses.htm) | 2026-07-14 | **Partially verified**: platform/list price được xác nhận; Free/trial entitlement tại tài khoản thật phải kiểm tra. |
| NL-DOC-02 | NeoLoad | User Paths/populations, validation/SLA, configurable percentiles/raw export và `NeoLoadCmd` exit 0/1/2 cùng JUnit/Jenkins/API path được tài liệu hóa. | DOC | [Validation](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/validation.htm); [SLA profiles](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/service_level_agreement_sla_profiles.htm); [Controller CLI](https://docs.tricentis.com/neoload-2026.1/en-us/content/get_started/start_the_controller.htm); [Test Summary](https://docs.tricentis.com/neoload-latest/en-us/content/reference_guide/test_summary.htm) | 2026-07-14 | **Verified** cho documented workflow; chosen entitlement, agent connectivity và EShop journey vẫn chưa chạy. |
| NL-EXP-01 | NeoLoad | Smoke 1 VU/1 iteration, GET + validation/SLA, headless CLI, HTML/raw/JUnit artifacts và positive/negative exit. | EXP-PLAN | Smoke Test Plan `§7.11`; Appendix C | — | **Not executed — [CẦN THỰC NGHIỆM]**; chưa có licence screenshot, project, raw export, report hoặc exit evidence. |
| AB-DOC-01 | ApacheBench | `ab` đi cùng Apache HTTP Server, source dùng Apache License 2.0; ASF phân phối source còn Windows binaries trên download page là third-party builds. | DOC | [ApacheBench manual](https://httpd.apache.org/docs/current/en/programs/ab.html); [Apache HTTP Server LICENSE](https://github.com/apache/httpd/blob/trunk/LICENSE); [Download](https://httpd.apache.org/download.cgi); [Install](https://httpd.apache.org/docs/2.4/install.html) | 2026-07-14 | **Verified**; package/binary provenance trên Windows phải được ghi, không gắn nhãn binary ASF. |
| AB-DOC-02 | ApacheBench | `-n/-c/-t/-k` điều khiển single-URL benchmark; console và `-e` percentile CSV có sẵn, nhưng body assertion/SLA gate không được tài liệu hóa và manual cảnh báo client có thể thành bottleneck. | DOC | [ApacheBench manual và Bugs](https://httpd.apache.org/docs/current/en/programs/ab.html#bugs) | 2026-07-14 | **Verified** cho documented endpoint scope/report/limitation; CI policy cần wrapper. |
| AB-EXP-01 | ApacheBench | Smoke 20 requests, concurrency 2, một GET và `-e` percentile CSV; capture transport errors và generator headroom. | EXP-PLAN | Smoke Test Plan `§7.12`; Appendix C | — | **Not executed — [CẦN THỰC NGHIỆM]**; chưa có `ab -V`, stdout/stderr, CSV hoặc request/error count. |
| LR-DOC-01 | OpenText LoadRunner Professional | Tên hiện hành là OpenText Professional Performance Engineering (LoadRunner Professional); Community licence 26.1 cho 50 Vuser theo documented exclusions. Full VuGen/Controller/Analysis stack là Windows-centric; giá commercial không công khai. | DOC | [Product](https://www.opentext.com/products/professional-performance-engineering); [Licence Utility 26.1](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/License/R_License_Utility.htm); [Install](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Install/About-install.htm); [Trial](https://www.opentext.com/en-gb/products/professional-performance-engineering/trial) | 2026-07-14 | **Partially verified**: Community entitlement/platform được documented; trial duration và commercial quote phải xác minh. |
| LR-DOC-02 | OpenText LoadRunner Professional | VuGen scripts/correlation, Controller schedules/SLA, Analysis/raw export và CLI scenario execution được tài liệu hóa; direct CLI universal “SLA fail → exit N” chưa được tìm thấy, còn Jenkins plugin có SLA pass/fail path. | DOC | [VuGen overview](https://admhelp.microfocus.com/vugen/en/26.1/help/WebHelp/Content/VuGen/100050_c_vugen_overview.htm); [Schedules](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_schedules_overview.htm); [Analysis](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Analysis/c_analysis_workflow.htm); [CLI](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/scenario-run-cli.htm); [Jenkins](https://admhelp.microfocus.com/lr/en/26.1/help/WebHelp/Content/Controller/c_jenkins.htm) | 2026-07-14 | **Partially verified**: execution/reporting/SLA confirmed; direct exit propagation và known percentile issue require lab/patch review. |
| LR-EXP-01 | OpenText LoadRunner Professional | Smoke VuGen GET/text check → Controller 1 VU/1 iteration → collate/Analysis/SLA, cộng negative check/SLA propagation. | EXP-PLAN | Smoke Test Plan `§7.13`; Appendix C | — | **Not executed — [CẦN THỰC NGHIỆM]**; chưa có installer/licence, `.lrs`, raw result, Analysis report hoặc exit observation. |
| TS-DOC-01 | Tsung | Tsung là GPLv2 project của ProcessOne, build trên Erlang; hosted manual mang nhãn 1.7.0 trong khi source `develop` khai báo 1.8.0, nên tag/DTD/dependencies phải pin. | DOC | [Tsung repository](https://github.com/processone/tsung); [COPYING](https://github.com/processone/tsung/blob/develop/COPYING); [Installation](https://tsung.readthedocs.io/en/latest/installation.html); [`vsn.mk`](https://github.com/processone/tsung/blob/develop/vsn.mk); [Manual](https://tsung.readthedocs.io/en/latest/) | 2026-07-14 | **Partially verified**: identity/licence/install path rõ; source/manual version skew chưa được binary validation. |
| TS-DOC-02 | Tsung | XML hỗ trợ arrival phases, weighted sessions, cookies, dynamic variables/extraction/match và single-node/distributed clients; logs/live view/HTML reports được tài liệu hóa. | DOC | [Load configuration](https://tsung.readthedocs.io/en/latest/conf-load.html); [Sessions](https://tsung.readthedocs.io/en/latest/conf-sessions.html); [Advanced features](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html); [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html); [Reports](https://tsung.readthedocs.io/en/latest/reports.html) | 2026-07-14 | **Partially verified**: documented capability mạnh, nhưng exact DTD, percentile/raw backend và CI gate của pinned binary phải kiểm chứng. |
| TS-EXP-01 | Tsung | Smoke single-node `use_controller_vm='true'`, một HTTP GET nhỏ, optional body `match`, run log và `tsung_stats.pl` report. | EXP-PLAN | Smoke Test Plan `§7.14`; Appendix C | — | **Not executed — [CẦN THỰC NGHIỆM]**; skeleton XML chưa validate bằng DTD/binary và không có log/report. |
| TA-DOC-01 | Taurus | Taurus/bzt là OSS Apache-2.0 orchestration framework, cài qua pip trên Linux/macOS/Windows và có official `blazemeter/taurus` image; executor có runtime/dependency riêng. | DOC | [Taurus repository](https://github.com/Blazemeter/taurus); [Installation](https://gettaurus.org/docs/Installation/); [Docker installation](https://gettaurus.org/install/Installation/) | 2026-07-14 | **Verified** cho Taurus layer; không đồng nghĩa JMeter/Java/plugins đã sẵn hoặc cùng version. |
| TA-DOC-02 | Taurus | YAML/JSON common profile gọi executor; khi `executor: jmeter`, JMeter thực thi/phát tải. Pass/fail, JUnit, exit codes và merged/effective/generated artifacts được tài liệu hóa. | DOC | [Execution settings](https://gettaurus.org/docs/ExecutionSettings/); [JMeter executor](https://gettaurus.org/docs/JMeter/); [Pass/fail](https://gettaurus.org/docs/PassFail/); [Reporting](https://gettaurus.org/docs/Reporting/); [Command line](https://gettaurus.org/docs/CommandLine/); [Artifacts](https://gettaurus.org/docs/ArtifactsDir/) | 2026-07-14 | **Verified** cho orchestration semantics; cross-executor parity không được giả định và generated plan phải audit. |
| TA-EXP-01 | Taurus | Smoke explicit JMeter executor, 1 VU/1 iteration, request assertion, passfail, JUnit, generated JMX/JTL/effective config và exit code. | EXP-PLAN | Smoke Test Plan `§7.15`; Appendix C | — | **Not executed — [CẦN THỰC NGHIỆM]**; chưa quan sát auto-download/offline behavior, generated plan, engine result hoặc exit. |

## B.2. Quy tắc nâng trạng thái evidence

- Chỉ đổi Type của một hàng từ `EXP-PLAN` sang `EXP` và status sang `Executed/Observed` khi có đủ: tool/runtime version, provenance/checksum hoặc image digest, exact command/config đã redaction, target/EShop commit, timestamp/timezone, stdout/stderr, exit code, raw artifact/report và metadata tài nguyên load generator/SUT.
- Một output “đẹp” không đủ để gọi smoke thành công. Negative control phải làm hỏng status/body marker hoặc threshold một cách có chủ đích và chứng minh failure đi tới process/pipeline theo đúng policy.
- Pricing, hosted limits, trial/community entitlement, SaaS region và licence conditions phải được kiểm lại sát ngày trình bày; register này chỉ chốt trạng thái ngày 2026-07-14.
- Không nâng claim endpoint benchmark thành claim journey: ApacheBench, wrk, Siege và Vegeta cần giữ đúng role boundary trừ khi có harness riêng được review và evidence mới.
- Taurus luôn phải ghi executor/version/plugins/JVM; một result do JMeter executor phát tải không được gán nhầm cho “Taurus engine”.

---

# Appendix C — Smoke Test Plans

> **Toàn bộ nội dung Appendix C là kế hoạch, không phải kết quả.** Mỗi smoke phải giữ tải tối thiểu, chỉ gọi endpoint read-only/idempotent đã được chủ hệ thống cho phép, thay toàn bộ placeholder `[VERIFIED_*]`, và dừng nếu target, data ownership, WAF/cost guard hoặc cleanup chưa được xác minh. Không có latency, throughput, percentile, error rate hay capacity value nào dưới đây đã được quan sát.

## C.1. Evidence bundle tối thiểu dùng chung

Trước khi chuyển bất kỳ `EXP-PLAN` nào thành `EXP`, nhóm phải lưu cùng một evidence bundle:

1. Tool/runtime/OS versions; package source, checksum hoặc image digest; lockfile/plugin versions khi có.
2. EShop commit SHA, sanitized config/script và hash; exact command/procedure; target contract và written authorization.
3. Start/end timestamp kèm timezone; stdout, stderr, process exit code và mọi raw/result/report artifact.
4. Load-generator và SUT CPU/RAM/network snapshot; proxy/TLS/container topology; redaction proof cho secrets và personal data.
5. Một positive control và một **negative control** nhỏ: cố ý làm sai marker/status/threshold trên test-only target để chứng minh assertion/gate thực sự lan tới exit/pipeline.

## C.2. Consolidated Smoke Test Plan index

| Ref / công cụ | Setup và prerequisites | Request, workload và command/procedure | Expected evidence — chưa quan sát | Typical failure modes cần bắt | Success criteria của smoke |
|---|---|---|---|---|---|
| `§7.1` **Apache JMeter** | Pin Java `>=8` và Apache binary/checksum; ghi `java -version`, `jmeter -v`; tạo writable artifact directories. Trong GUI chỉ design/debug một plan gồm 1 Thread, 1 loop, HTTP Request, Response Assertion và Simple Data Writer. Xác minh `[VERIFIED_BASE_URL]`, `[VERIFIED_READ_ONLY_PATH]`, status/body marker và quyền test. | Một `GET [VERIFIED_BASE_URL]/[VERIFIED_READ_ONLY_PATH]`; chạy load ở non-GUI mode: `jmeter -n -t jmeter-smoke.jmx -l artifacts/jmeter-smoke.jtl -e -o artifacts/jmeter-report`. Không thêm listener nặng cho load test. | `.jmx`, command, stdout/stderr/exit, `jmeter.log`, JTL và `artifacts/jmeter-report/index.html`; config percentile/report properties và timestamps. Expected intent: một sample có `success=true` và assertion pass. | Java mismatch; DNS/TLS/proxy; 401/404; bad cookie/marker; output folder không rỗng; plugin/version drift; GUI accidentally used as load runner; threshold wrapper không nhận assertion failure. | Exactly one planned sample đúng status/body, zero transport/assertion errors và đủ artifact để rerun. Negative marker phải làm sample/gate fail theo CI policy trước khi claim automation. **[CẦN THỰC NGHIỆM]** |
| `§7.2` **Silk Performer** | Windows/admin và supported installer; ghi OS, Silk version, installer checksum, redacted Evaluation/licence entitlement. Workbench tạo Web project/BDL, content verification và `Verification` workload 1 VU/1 iteration; xác minh target read-only. | Một GET tới `[VERIFIED_BASE_URL]/[VERIFIED_READ_ONLY_PATH]` với status/content verification. Chạy `performer C:\lab\silk-smoke\silk-smoke.ltp /Automation 5 /WL:Verification /Resultsdir:C:\lab\artifacts\silk-smoke`. | Project/BDL/workload, command, stdout/stderr/exit, Event Viewer, VU output/log, `.tsd`/result và browser report. Expected intent: verification pass và result folder sinh được. | Trial expired/10-VU cap; admin/runtime failure; TLS/proxy; parser/marker sai; agent unavailable; results path/permissions; public docs/version khác installed build; exit semantics không lan tới pipeline. | Request và content verification đúng, không automation/runtime error, artifact đầy đủ; negative marker phải chứng minh failure propagation. Không suy ra scalability từ 1 VU. **[CẦN THỰC NGHIỆM]** |
| `§7.3` **Artillery** | Pin Node LTS, Artillery package + lockfile hoặc official image digest; cache package/image nếu offline; tạo artifacts directory. Xác minh target/endpoint và plugin versions. | YAML có `duration: 1`, `arrivalCount: 1`, một HTTP GET tới `[VERIFIED_PRODUCT_ENDPOINT]`, `expect statusCode: 200`, strict `ensure` với `plugins.expect.failed == 0`. Chạy `artillery run --output artifacts/artillery-smoke.json smoke.yml`. | YAML/hash, Node/Artillery versions, command/stdout/stderr/exit, raw JSON và metric names. Expected intent: một arrival, zero expect failures, ensure pass và exit 0. Không trông đợi local HTML vì current `artillery report` path đã bị loại. | Node/PowerShell/npm/cache; plugin/metric-version mismatch; TLS/auth/proxy; target/path concatenation; output permission; 5xx/timeout không làm build fail nếu thiếu strict expect/ensure; Cloud upload ngoài ý muốn. | Raw JSON xác nhận planned arrival/request; status expectation và strict ensure pass; exit 0; negative status/condition phải non-zero; không vượt authorized scope. **[CẦN THỰC NGHIỆM]** |
| `§7.4` **k6** | Pin k6 binary/package hoặc `grafana/k6` image digest; ghi version, OS/CPU/RAM, EShop commit; tạo artifacts directory. Không giả định runtime là Node.js. | Script dùng `shared-iterations`, `vus: 1`, `iterations: 1`; một `http.get`, status check và thresholds `checks: rate==1`, `http_req_failed: rate==0`. Chạy `k6 run --out json=artifacts/k6-smoke.json smoke.js`. | Script/hash, version, command/stdout/stderr/exit, raw JSON và end-of-test summary; optional local HTML nếu đã bật dashboard/export. Expected intent: một iteration, checks/thresholds pass, exit 0. | DNS/TLS/proxy; auth/redirect; threshold syntax; output/container volume permission; incompatible remote/npm module; check fail nhưng process vẫn 0 khi quên threshold; secret leak. | Raw output có đúng planned iteration/request, status/check/threshold đều đạt, exit 0 và artifacts đầy đủ. Negative check/threshold phải tạo non-zero exit. **[CẦN THỰC NGHIỆM]** |
| `§7.5` **Locust** | Pin Python/Locust với locked venv hoặc official image digest; ghi versions/OS; tạo artifact path. `HttpUser` dùng per-user client và `catch_response=True`; target/endpoint phải read-only. | Một task GET `[VERIFIED_PRODUCT_ENDPOINT]`; nếu status khác expected thì `response.failure(...)`. Chạy `locust -f locustfile.py --headless --users 1 --spawn-rate 1 --run-time 5s --host [VERIFIED_BASE_URL] --csv artifacts/locust-smoke`. | Locustfile/hash, lock/image, command/stdout/stderr/exit và toàn bộ `locust-smoke*.csv`; observed request count, failures/exceptions và timestamps. Expected intent: 1 user, ít nhất một valid sample, zero failure. | venv/PATH/import; TLS/auth/proxy; host/path ghép sai; CSV permission; run quá ngắn không có sample; repeated side effect do user loop; custom exit hook sai; Windows/distributed process assumption. | Có ít nhất một in-scope sample, failure/exception 0, expected exit và đủ CSV/log. Không gọi đây là exactly-one-request vì 5-second user loop có thể lặp; muốn exact one phải thêm stop logic rồi kiểm riêng. **[CẦN THỰC NGHIỆM]** |
| `§7.6` **Gatling** | Dùng current JavaScript starter đã pin; Node 24+ LTS/npm 11+ theo profile, lockfile và Gatling versions được ghi. Xác minh package cache, script location/name và target. | Simulation JS có `atOnceUsers(1)`, một HTTP GET, `status().is(200)` và `global().failedRequests().count().is(0)`. Chạy `npx gatling run --simulation smokeSimulation`. | Script/hash, Node/npm/Gatling versions, build log, stdout/stderr/exit và toàn bộ portable HTML report folder. Expected intent: one VU/request, check/assertion pass và exit 0. | Node/npm version; dependency network/cache; file naming/location; current SDK import/syntax; TLS/auth; report permission; feeder/session issue; parse `simulation.log` như stable API. | Report xác nhận planned request, check/global assertion pass, exit 0 và complete HTML/log/config evidence. Negative status/assertion phải fail process/build. **[CẦN THỰC NGHIỆM]** |
| `§7.7` **Loader.io** | Chỉ dùng `[AUTHORIZED_PUBLIC_HOST]`; lưu written authorization, Free/paid plan snapshot, WAF/cost guard, API key trong secret store. Verify host bằng HTTP token và ghi loader IP list; private/localhost không thuộc scope. | API JSON: một GET read-only, `test_type=per-test`, `total=15`, `duration=60`, `timeout=10000`, `error_threshold=1`; POST `/v2/tests`, lưu sanitized request/response rồi poll result đến terminal state. | Redacted API JSON/responses, host verification/plan evidence, result JSON/report URL, webhook/poll logs, server logs, loader IPs, timestamps. Expected intent: completed run, `success>0`, zero error/timeout/network; không đặt p95 gate khi schema chưa chứng minh percentile. | Host verification/DNS; target không public; TLS/WAF/429; threshold abort; API key leak; unexpected cloud/hosting cost; API/webhook article/version drift; redirect được tính success; body error dưới HTTP 200. | Verification và terminal completion thành công; zero protocol/timeout/network error theo smoke contract; artifacts đầy đủ. Test-only 404/timeout phải làm wrapper/CI fail trước khi automation claim. **[CẦN THỰC NGHIỆM]** |
| `§7.8` **Siege** | Pin Linux/WSL/custom image/source; ghi Siege version/provenance, isolated `.siegerc`; cô lập `$HOME` và cookie file. Xác minh target/status; đặt `logfile = [ARTIFACT_PATH]` trong `.siegerc`. | Một GET; chạy `siege -l -c 2 -r 5 -b "[VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]"`; `-l` chỉ bật log, không nhận path. Planned count 2 × 5 phải xác nhận từ output. | Command, version/config, stdout/stderr/exit, configured log/hash, cookie isolation proof, EShop commit và client/SUT resources. | Không có native Windows; routing/TLS; stale cookie; 3xx false-success; file descriptors; client saturation; `.siegerc`/log path sai. | Transaction/status count khớp contract, zero transport error, isolated cookies, generator headroom và artifacts đủ rerun; không đặt p95. **[CẦN THỰC NGHIỆM]** |
| `§7.9` **Vegeta** | Pin official release asset hoặc source-built binary/Dockerfile result; lưu version/checksum/digest. Xác minh target, status contract, synchronized clock và resource monitoring. | `targets.txt` chứa một dòng `GET [VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]`. Chạy tuần tự, capture exit từng bước: `vegeta attack -targets=targets.txt -rate=2/s -duration=10s -output=results.bin`; `vegeta report -type=json results.bin > report.json`; optional `vegeta plot results.bin > plot.html`. | Target/hash, commands/exits, version/provenance, `results.bin`, `report.json`, optional `plot.html`, stdout/stderr và resource metadata. Workload intent xấp xỉ 20 arrivals nếu client theo kịp; đây không phải observed result. | Quoting/redirection; JSON body chưa base64; raw artifact lộ secret; TLS/timeout; rate vượt client capacity; 3xx tính protocol success; shell pipeline che exit; wrong report format/version; container clock/network. | Artifact chain parse được, observed request/status/error khớp contract, từng command exit đúng và generator có headroom. Chỉ bật CI policy sau khi SLA/parser được review; multiple targets không được gọi là journey. **[CẦN THỰC NGHIỆM]** |
| `§7.10` **wrk** | Build/pin source/compiler/LuaJIT/OpenSSL và binary hash. Version-control `status_check.lua` dùng official `response(status, headers, body)` + thread aggregation; review script và monitoring. Callback overhead chỉ chấp nhận ở smoke. | Một GET; chạy `wrk -t2 -c4 -d10s --latency -s status_check.lua "[VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]"`. | Command, binary/script hashes, review record, stdout/stderr/exit, status counters, latency/RPS/error counters và resource snapshots. | Build/routing/TLS/file descriptor; client saturation; nhầm threads/VU; Lua aggregation sai; callback overhead; wrapper che failure. | `unexpected_status=0`, zero transport errors, client headroom và evidence đủ rerun; negative status phải làm wrapper fail. **[CẦN THỰC NGHIỆM]** |
| `§7.11` **NeoLoad** | Cài supported Controller/Java; ghi version, checksum và redacted Free/trial/commercial entitlement. Tạo User Path GET + validation, Population 1, Scenario `Smoke` 1 VU/1 iteration và explicit SLA. | Chạy `NeoLoadCmd -project ...\smoke.nlp -launch Smoke -noGUI -report ...\smoke.html -exportRaw ...\raw.csv -SLAJUnitReport ...\junit.xml`; không dùng `-exitCodeFailIgnore`. | `.nlp`/YAML, environment overrides, command/stdout/stderr/exit, HTML, raw CSV, SLA JUnit và entitlement/version metadata. Expected intent: validation/SLA pass và exit 0. | No/expired licence (documented error class), Java/resource, agent certificate/connectivity, TLS/proxy, extraction/validation mismatch, report path, hidden `-exitCodeFailIgnore`. | Request/validation/SLA đạt; HTML/raw/JUnit tồn tại; expected positive exit. Negative marker/SLA phải cho documented failure exit, không bị option ignore che. **[CẦN THỰC NGHIỆM]** |
| `§7.12` **ApacheBench (`ab`)** | Lấy binary/package có provenance hoặc build Apache HTTP Server; lưu `ab -V`, checksum/package source. Xác minh base URL/path/status, TLS/proxy và resource monitoring. | Một GET; chạy `ab -n 20 -c 2 -e ab-percentiles.csv "[VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]"`. Static auth header nếu thật sự cần phải inject từ secret store, không commit. | Command redacted, `ab -V`, stdout/stderr/exit, `ab-percentiles.csv`/hash, EShop commit, timestamps và client/SUT resource snapshots. Expected intent: 20 complete requests và parseable CSV; không dự đoán latency/RPS. | DNS/refused/TLS; URL thiếu `/`; response length thay đổi bị tính failed; file descriptor; unprovenanced Windows binary; header leak; `ab` tự thành bottleneck; non-2xx/body error diễn giải sai. | Complete/status count đúng contract, zero connect/read/exception ở smoke load, CSV parse được, generator còn headroom và đủ artifact. Không claim business correctness vì `ab` thiếu body assertion. **[CẦN THỰC NGHIỆM]** |
| `§7.13` **OpenText LoadRunner Professional** | Supported Windows/admin; pin installer/patch, ghi redacted Community/trial licence. Cài VuGen, Controller, Analysis; tạo Web HTTP/HTML script, text check, manual `.lrs`, local LG, 1 VU/1 iteration và SLA. | `web_reg_find`/text check phải đăng ký trước `web_url` GET tới verified path. Chạy `CLIControllerApp.exe -TestPath C:\lab\lr-smoke\lr-smoke.lrs -CollateAndAnalyze -ResultName C:\lab\artifacts\lr-smoke -SilentMode`. | VuGen source/data/runtime, `.lrs`, schedule/LG/SLA, command/stdout/stderr/exit, Controller/raw result, collated Analysis report, installed build/licence. Expected intent: Vuser/check/SLA pass và result collate/analyze. | Licence/protocol restriction; Windows privilege; recording/TLS/correlation; LG down; only-one-Controller restriction; result overwrite/path/case-sensitive args; Analysis issue; known percentile graph issue; direct exit không phản ánh SLA. | Correct request/text check/SLA, collate/report đầy đủ và no runtime error. Deliberately wrong marker/SLA must prove failure via chosen direct CLI/plugin path before pipeline claim. **[CẦN THỰC NGHIỆM]** |
| `§7.14` **Tsung** | Pin source tag/commit, DTD, Erlang/OTP/report dependencies; xác minh host/port/path/protocol/TLS. Base skeleton chưa có body match; optional marker chỉ thêm sau review. Chỉ single-node `use_controller_vm='true'`. | Validate XML với DTD; one 10-second phase, one session, one GET; chạy `tsung ... start`, rồi `tsung_stats.pl`. | XML/DTD/hashes, versions, commands/exits, run log, HTML/graphs và resources; không dự đoán metrics. | Version mismatch; Erlang node/cookie; TLS; report/log; placeholder; optional match escaping; unintended SSH; token leak. | Single-node sạch, request/transport đúng, complete report. Chỉ claim body match nếu XML thật có match và negative control. **[CẦN THỰC NGHIỆM]** |
| `§7.15` **Taurus — explicit JMeter executor** | Pin Python/bzt, Java, JMeter và plugins; cache trước và đặt `TAURUS_DISABLE_DOWNLOADS` cho strict offline run. YAML phải ghi rõ `executor: jmeter`; lưu mọi version và writable artifacts directory. | YAML: concurrency 1, iterations 1, one GET; HTTP-code assertion, `passfail` criterion `fail>0%`, JUnit reporter. Chạy `bzt smoke.yml`. JMeter — không phải Taurus — là engine phát request. | Original/merged/effective config, generated JMX, bzt/JMeter logs, JTL/LDJSON, final stats, `xunit.xml`, stdout/stderr/exit, versions/plugins/JVM. Expected intent: 1 iteration, assertion/passfail pass và exit 0. | Python/Java/JMeter/plugin mismatch; auto-download/network drift; downloads disabled nhưng dependency thiếu; unsupported YAML field/executor parity; bad generated JMX; TLS/auth; passfail placement; artifacts/cloud upload misconfiguration. | Generated plan phản ánh đúng request/workload; JMeter executes one iteration; assertion/passfail/JUnit đạt; expected exit và complete artifacts. Negative assertion/passfail phải tạo automatic-shutdown/failure exit theo policy. **[CẦN THỰC NGHIỆM]** |

## C.3. Thứ tự chạy và stop conditions đề xuất

1. Chạy một `curl`/manual contract check ngoài load tool để xác nhận endpoint, status và body marker; bước này không được tính là performance evidence.
2. Chạy positive smoke ở tải tối thiểu; nếu artifact thiếu, exit semantics mơ hồ hoặc load generator bão hòa thì dừng, không tăng tải.
3. Chạy negative control trên test-only endpoint/marker; nếu pipeline vẫn xanh thì dừng và sửa gate trước mọi benchmark.
4. Chỉ sau hai control mới thiết kế EShop Fit Test với account/product data riêng, cleanup, warm-up, duration và workload model thống nhất.
5. Dừng ngay khi xuất hiện target ngoài allow-list, destructive checkout ngoài sandbox, WAF/rate-limit không được phê duyệt, secret/PII trong artifact, chi phí cloud bất ngờ hoặc SUT/load generator thiếu monitoring.

---

# Appendix D — Các thông tin cần thực nghiệm bổ sung

## D.1. Thông tin EShop phải khóa trước khi chạy

```md
# THÔNG TIN ESHOP THỰC TẾ

- Repository: https://github.com/trngnneee/eshop-sut
- Branch/Commit: seminar / 609b6e6821cd3241363d0087d859576674d47e1b
- API Base URL: http://localhost:3000 [SOURCE-CONFIRMED; RUNTIME CHƯA KHỞI ĐỘNG]
- Web URL: http://localhost:5173 [VITE DEFAULT DỰ KIẾN; CẦN STARTUP LOG]
- Admin URL: http://localhost:5174 [SOURCE-CONFIRMED; RUNTIME CHƯA KHỞI ĐỘNG]
- Login endpoint: POST /api/login
- Product endpoints: GET /api/products; GET /api/products?search={query}; GET /api/products/:id
- Cart endpoints: GET /api/cart; POST /api/cart
- Checkout endpoint: POST /api/checkout
- Authentication mechanism: JWT Bearer token lấy từ response login
- Backend technology: Node.js CommonJS, engines 20.x; Express ^5.2.1
- Database: SQLite, backend/database.sqlite; initializer drop/re-seed on backend start
- Operating system: Windows 11 Home 64-bit, build 26200
- Available CPU/RAM: Intel Core i7-1260P, 12 cores/16 logical processors; 15.72 GiB RAM
- Load-generator topology: Dự kiến cùng máy với SUT [CẦN XÁC NHẬN KHI CHẠY]
- JMeter: NOT_FOUND trên PATH ngày 2026-07-15
- k6: NOT_FOUND trên PATH ngày 2026-07-15
- Audience operating system: [CẦN NHÓM ĐIỀN]
- Internet availability during seminar: [CẦN NHÓM ĐIỀN CÓ/KHÔNG]
- Test environment owner/approval: [CẦN OWNER SIGN-OFF]
- Allowed load ceiling và abort rule: [CẦN OWNER PHÊ DUYỆT]
- Approved SLO/Thresholds: [CẦN PRODUCT/SEMINAR OWNER PHÊ DUYỆT]
- Test-data seed/cleanup procedure: [CẦN CHỐT SNAPSHOT/ACCOUNT/CLEANUP; KHÔNG RESTART BACKEND GIỮA RUN]
```

Workspace hiện có source EShop, nhưng source inspection không chứng minh URL runtime, seed data, auth behaviour, environment capacity hoặc permission to load. Vì vậy các script vẫn phải dùng `[VERIFIED_*]` cho đến khi nhóm điền bảng trên, review route contract và lưu evidence. Không đưa secret từ source/config vào tài liệu hoặc raw result.

## D.2. Evidence gap theo mức ưu tiên

| Ưu tiên | Evidence còn thiếu | Cách thu | Tiêu chí hoàn tất | Quyết định bị ảnh hưởng |
|---:|---|---|---|---|
| P0 | Permission, target và safety ceiling | Owner sign-off + environment record | Target/staging, max load, abort, window được duyệt | Có được phép chạy hay không |
| P0 | Verified routes/auth/data contract | Source/API-owner review + 1-user manual request | Method/path/payload/token/business marker được xác nhận | EShop fit và script correctness |
| P0 | Tool version/install evidence | Version command, checksum, OS/runtime | Artefact truy nguyên cho từng tool đã chạy | Cost/access, Reproducibility |
| P0 | One-request Smoke Test JMeter/k6/counterfactual | Thực hiện Appendix C | Raw output + deliberate negative + exact command | Shortlist validity |
| P1 | Same-journey EShop Fit Test | Chạy logical model chuẩn | Correlation/data/Checks hoạt động; raw results đủ | Pair selection |
| P1 | Classroom time | Người không viết script thử trên lab image | Setup + activity ≤25 phút hoặc có mitigation rõ | Classroom suitability |
| P1 | Generator/SUT telemetry | OS/container/APM monitoring | CPU/RAM/network/dropped work đồng bộ timestamp | Diễn giải metrics |
| P1 | Counterfactual Artillery/Locust/Gatling | Ít nhất Smoke Test cùng tiêu chí | Evidence chất lượng ngang nhau | Bias/complementarity |
| P2 | Commercial trial/access | Trial request/licence terms/account evidence | Entitlement/version/limit/expiry được ghi | Enterprise candidate fairness |
| P2 | Distributed need | Single-generator capacity check | Chứng minh generator bottleneck trước Tsung/remote mode | Distributed scope |
| P2 | Soak/Spike/Stress profiles | Safety-reviewed test run | Profile, abort, recovery và telemetry đủ | Advanced demonstration |

## D.3. Experiment record tối thiểu

Mỗi run cần một manifest tương đương:

```yaml
experiment_id: [EXP-ID]
timestamp_timezone: [ISO-8601 + timezone]
operator: [NAME/ID]
approval: [LINK_OR_RECORD]
eshop_repository: [URL]
eshop_commit: [SHA]
tool: [NAME]
tool_version: [EXACT]
runtime_and_dependencies: [EXACT]
generator_os_cpu_ram: [EXACT]
sut_os_cpu_ram: [EXACT]
network_topology: [EXACT]
workload_model: [VERSIONED_FILE]
profile: [SMOKE/LOAD/STRESS/SPIKE/SOAK]
target_and_achieved_load: [RAW_REFERENCE]
test_data_and_cleanup: [VERSIONED_REFERENCE]
command: [EXACT]
raw_results: [PATH]
generator_telemetry: [PATH]
sut_telemetry: [PATH]
stdout_stderr_logs: [PATH]
screenshots_optional: [PATH]
outcome: [PASS/FAIL/INCONCLUSIVE]
limitations: [TEXT]
```

## D.4. Thực nghiệm negative-control bắt buộc

Để chứng minh Assertions/Checks/Thresholds thực sự hoạt động, không chỉ chạy happy path:

1. Một endpoint/path cố ý sai trong safe environment phải làm protocol Check/Assertion thất bại.
2. Một business marker cố ý sai phải làm business Check/Assertion thất bại dù HTTP status có thể là 200.
3. Một Threshold kiểm chứng với policy test-only phải tạo nonzero CI outcome hoặc artefact failure như tài liệu thiết kế.
4. Sau đó hoàn nguyên cấu hình; không đưa negative-control vào Load Test thật.

## D.5. Quy tắc cập nhật điểm sau thực nghiệm

- Không sửa `DOC` thành `EXP`; thêm một evidence record mới và link cả hai.
- Nếu EXP mâu thuẫn DOC, kiểm tra version/config trước; ghi `Inconclusive` nếu chưa giải thích được.
- Chỉ cập nhật các ô liên quan; không “đẩy điểm” để giữ pair mong muốn.
- Ghi scorer, ngày, lý do và before/after score.
- Recompute Weighted Score tự động và review điều kiện loại trực tiếp riêng.

---

# Appendix E — Bộ câu hỏi phản biện và đáp án bảo vệ

| # | Câu hỏi phản biện | Trả lời bảo vệ ngắn |
|---:|---|---|
| 1 | Vì sao khảo sát 15 công cụ nhưng chỉ deep-test hai? | Breadth được xử lý bằng Desk Research; depth dùng nguồn lực hữu hạn. Pair chỉ finalize sau Smoke Test JMeter/k6 và ít nhất một counterfactual. |
| 2 | Có công bằng khi không cài được commercial tool? | Có ở mức DOC nếu không biến thiếu access thành thiếu capability. EXP được ghi `Not executed`; access/classroom conclusion giữ provisional. |
| 3 | Vì sao JMeter và k6 được chọn nhưng không gọi là tốt nhất? | Quyết định chỉ tối ưu cho T05/EShop/access/25 phút/complementarity; không có phạm vi hay EXP để kết luận toàn cục. |
| 4 | Vì sao không chọn hai điểm cao nhất? | Weighted Score không đo role overlap, blocker và complementarity. Pair selection dùng thêm evidence quality và learning objectives. |
| 5 | Vì sao complementarity quan trọng? | Pair phải dạy hai cách tiếp cận khác nhau với cùng Workload Model, không chỉ lặp lại hai syntax code-first. |
| 6 | Vì sao chưa chọn Locust? | Locust mạnh và giữ shortlist; Python code-first trùng vai trò k6. Có thể thay k6 nếu EXP/audience skill nghiêng về Python. |
| 7 | Vì sao chưa chọn Gatling? | Capability cao, current SDK không chỉ Scala; project/DSL/activity cost cần EXP và vai trò code-first trùng k6. |
| 8 | Vì sao chưa chọn Artillery? | YAML/JS rất phù hợp và là counterfactual ưu tiên; hiện chưa tạo learning contrast bằng JMeter+k6 và logic có thể phân tán config/hooks. |
| 9 | Vì sao chưa chọn LoadRunner Professional? | Enterprise protocol/components mạnh nhưng gated licence, setup/component scope và classroom Reproducibility khác mục tiêu local seminar. |
| 10 | Tsung có cần cho EShop local? | Chỉ khi chứng minh một generator là bottleneck hoặc distributed testing là learning objective. Hiện chưa có evidence đó. |
| 11 | Taurus có phải load generator? | Không nên gọi như vậy khi nó dùng executor. Với `executor: jmeter`, JMeter là engine; Taurus orchestration/pass-fail/reporting. |
| 12 | k6 có phải AI tool? | Không. k6 thực thi script/metrics; AI chỉ hỗ trợ draft/audit và không có quyền xác nhận endpoint/workload/result. |
| 13 | AI capability được đánh giá thế nào? | Qua mức artefact dễ draft/diff/audit, trace assumption và áp human control; đây là contextual inference, không phải native-AI claim. |
| 14 | Điểm nào chỉ dựa trên documentation? | Hiện tất cả điểm capability/licence đều DOC; Learning curve, AI potential và Classroom suitability có thêm ASSUMPTION; chưa có EXP. |
| 15 | Làm sao tránh thiên vị thành viên phụ trách tool? | Anchor chung, citation trên mỗi ô, cross-review độc lập, reconcile chênh lệch và chạy counterfactual cùng test. |
| 16 | Làm sao bảo đảm cùng tiêu chí cho 15 tool? | Dùng cùng 12 weighted criteria + Community qualitative; diễn giải trong role group và không đổi anchor theo tên tool. |
| 17 | Vì sao benchmark tool không phù hợp full journey? | Nó tối ưu one/multi-URL request generation và endpoint metrics, thường thiếu per-user state/correlation/business gate tích hợp. Vẫn hữu ích supporting benchmark. |
| 18 | Commercial tool nhiều feature hơn có tốt hơn? | Có thể tốt hơn cho enterprise use case nhưng không tự động phù hợp access, local EShop, Reproducibility hay 25-minute activity. |
| 19 | Điểm tổng có thể che gì? | Hard blocker, evidence yếu, role overlap và một tiêu chí trọng yếu thấp có thể bị điểm khác bù. Vì vậy dùng điều kiện loại riêng. |
| 20 | Evidence nào còn thiếu trước kết luận cuối? | Permission, routes/auth/data, tool versions, raw smoke/fit results, CPU/RAM, classroom time, counterfactual và commercial entitlement. |
| 21 | HTTP 200 có đủ chứng minh checkout thành công? | Không. Cần schema/business Check và state/order confirmation phù hợp, không chỉ protocol status. |
| 22 | Cùng số VU có phải cùng workload? | Không. VU closed model khác arrival-rate open model; phải so target/achieved arrival, pacing, journey mix và duration. |
| 23 | Vì sao cần raw result nếu đã có screenshot? | Screenshot không đủ tái tính percentile, lọc errors hoặc audit config. Raw result + script + manifest là evidence chính. |
| 24 | Làm sao biết generator chứ không phải SUT là bottleneck? | Đồng bộ telemetry generator/SUT, theo dõi achieved load/dropped work; nếu generator saturate thì capacity conclusion là inconclusive. |
| 25 | Nếu EXP đảo thứ hạng thì sao? | Cập nhật evidence/score minh bạch và mở lại pair. Phương pháp có giá trị hơn việc giữ quyết định ban đầu. |

---

# Self-Audit trước khi kết thúc

## Factual Audit

- [x] Mọi external factual claim trong phạm vi Desk Research có official/primary citation ngay sau claim hoặc trỏ đến Evidence ID; inference được gắn `ASSUMPTION` hoặc giới hạn diễn giải.
- [x] Licence/pricing/trial/access đã được kiểm tra theo snapshot ngày 2026-07-14; entitlement, quote và điều kiện account chưa khép kín được giữ ở trạng thái `Partially verified` hoặc chuyển thành EXP.
- [x] Không gọi Taurus là load generator độc lập khi đang dùng executor khác.
- [x] Chỉ dùng tên sản phẩm **Tsung**, không tự gắn thêm tiền tố dự án khác.
- [x] Không gọi k6 là AI tool.
- [x] Dùng tên hiện hành OpenText Professional Performance Engineering và giải thích tên LoadRunner Professional.
- [x] Đã link-audit snapshot công cụ: baseline 230 URL duy nhất có 223 phản hồi HTTP 200, một URL Locust 404 đã được thay, sáu URL Loader.io/OpenText được mở thủ công do TLS/timeout/anti-bot; tài liệu hiện có 234 URL HTTP(S) duy nhất sau delta và bổ sung repository SUT. Các URL Gatling/Siege/wrk mới trả 200, anchor Locust stable được xác nhận qua chỉ mục official dù lần kiểm trực tiếp cuối bị HTTP 429, còn URL SUT được đối chiếu bằng `git remote` và checkout local tại commit đã ghi.

## Methodology Audit

- [x] Dùng cùng 12 weighted criteria; Community được đánh giá định tính 0% vì prompt không cấp trọng số.
- [x] Phân nhóm tool theo role trước khi diễn giải score.
- [x] Giải thích DOC/EXP-PLAN/EXP/ASSUMPTION và gắn phần chưa chạy.
- [x] Tách Weighted Score, direct exclusion, evidence quality và complementarity.
- [x] Đã calibration/recompute chéo toàn bộ 15 bảng điểm; 12 trọng số cộng 100%, 15 vector và tổng đều khớp Appendix A.

## Bias Audit

- [x] Ghi điểm mạnh của commercial, benchmark, distributed và orchestration tools.
- [x] Không dùng “nhóm chưa quen” làm bằng chứng tool không tốt.
- [x] Có counterfactual test và câu hỏi bỏ tên JMeter/k6.
- [ ] Chạy ít nhất một shortlist alternative với cùng Smoke Test trước final selection.
- [ ] Re-score bằng EXP mà không ép kết quả về pair ban đầu.

## Submission Readiness Audit

- [x] Không còn assembly marker hoặc template token chưa thay; các placeholder `[VERIFIED_*]`, `[ARTIFACT_PATH]` và `[CẦN THỰC NGHIỆM]` còn lại là guard có chủ ý cho `EXP-PLAN`/thực nghiệm chưa chạy.
- [x] Full Scoring Matrix đã recompute và khớp từng profile.
- [x] Evidence Register có 45 ID duy nhất: 30 DOC và 15 `EXP-PLAN`; không có `EXP` đã thực thi. Mỗi plan ghi rõ `Not executed` và artefact/evidence path dự kiến.
- [x] Appendix C có đủ 15 Smoke Test Plans, đều nêu setup, request/workload, expected evidence, failure modes và success criteria.
- [x] Shortlist, selection rationale, limitations và rebuttal set đã có cấu trúc.
- [ ] Nhóm đã tùy chỉnh AI Usage Declaration đúng công cụ/hành động thật.

**Trạng thái chốt Desk Research ngày 2026-07-14:** cấu trúc, nguồn, bảng điểm, Evidence Register và Smoke Plan đã qua self-audit. Tài liệu **chưa đủ để tuyên bố lựa chọn thực nghiệm hoặc performance result** vì có 0 EXP, các trường EShop target/auth/data vẫn cần xác minh và AI Usage Declaration phải được nhóm tùy chỉnh trước khi nộp.

---

# AI Usage Declaration

> **[NHÓM PHẢI TÙY CHỈNH TRƯỚC KHI NỘP]** Hãy thay phần này bằng đúng AI tools mà từng thành viên thực sự dùng (ví dụ OpenAI Codex/ChatGPT, Claude hoặc Gemini), prompt/artefact được tạo và hành động human audit thực tế. Không giữ tên một tool nếu nhóm không dùng tool đó.

Tài liệu draft này có sử dụng **OpenAI Codex** để: đọc yêu cầu; tổ chức phương pháp và cấu trúc Markdown; hỗ trợ Desk Research trên official documentation/product/repository/pricing pages; đọc source/config/routes của EShop tại commit đã ghi để lập bản nháp Section 5; kiểm tra version command và thông số host; tạo bản nháp bảng so sánh, Smoke Test Plans, Evidence Register và câu hỏi phản biện; đồng thời rà soát dấu hiệu fabricated evidence.

**Human review bắt buộc:** Thành viên nhóm phải mở lại từng citation; xác minh version/licence/pricing; kiểm tra scoring anchors và tính nhất quán; xác minh EShop routes/auth/data; review mọi command/config; chạy Smoke Test và EShop Fit Test trong phạm vi được phép; lưu raw artefacts; và sửa mọi claim không khớp evidence. AI-generated text hoặc script không phải technical source và không được tự xem là verified.

**Data integrity:** AI không được dùng để tạo log, screenshot, Jira/Drive link, attendance, p50/p95/p99, Throughput, Error Rate, CPU/RAM hoặc kết quả pass/fail giả. Bản này không tuyên bố đã cài tool hoặc chạy Performance Testing. Mọi empirical field còn thiếu được đánh dấu `[CẦN THỰC NGHIỆM]`, `[ĐIỀN]` hoặc `Not executed`.
