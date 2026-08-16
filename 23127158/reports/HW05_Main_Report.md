# HW05 Performance Testing Report

## 1. Introduction

Báo cáo được thực hiện cho bài tập HW05 Performance Testing với thông tin sinh viên như sau:

| Mục | Thông tin |
|---|---|
| Họ tên | `Nguyễn Thanh Gia Bảo` |
| Mã số sinh viên | `23127158` |
| GitHub repository | `<Điền link GitHub repository của bài nộp>` |

Báo cáo này trình bày quá trình thiết kế kiểm thử hiệu năng cho hệ thống EShop, một ứng dụng thương mại điện tử demo gồm backend API Node.js/Express, cơ sở dữ liệu SQLite và các frontend web/admin/mobile. Phạm vi HW05 tập trung vào backend REST API tại `http://localhost:3000`, với mục tiêu thiết kế và thực thi các kịch bản Load, Stress và Spike bằng JMeter.

Workflow được chọn cho cả ba scenario là `Buy-then-history`:

`Login -> browse product list -> view product detail -> add to cart -> checkout -> read My Orders`

Workflow này được chọn vì nó mô phỏng một luồng mua hàng hoàn chỉnh và bao phủ đủ ba nhóm endpoint chính theo yêu cầu HW05:

| Nhóm endpoint | Endpoint trong workflow | Vai trò trong test |
|---|---|---|
| Auth-heavy | `POST /api/login` | Xác thực người dùng, lấy JWT token và kiểm tra rủi ro account lockout nếu dữ liệu đăng nhập sai. |
| Read-heavy | `GET /api/products`, `GET /api/products/:id` | Đọc danh sách sản phẩm, tìm kiếm/đọc chi tiết sản phẩm. |
| Transactional | `POST /api/cart`, `POST /api/checkout`, `GET /api/orders/my-orders` | Tạo trạng thái giỏ hàng, tạo đơn hàng và xác nhận đơn mới trong lịch sử đơn hàng. |

Quá trình làm bài áp dụng AI-first strategy: AI được dùng để đề xuất thiết kế, sinh JMeter test plan, chỉnh sửa cấu hình sau human review và ghi lại audit log. Tuy nhiên, các test plan cuối cùng không được xem là output thô của AI; chúng đã được review và chỉnh sửa thủ công để phù hợp hơn với giới hạn máy local, semantics của JMeter Ultimate Thread Group, dữ liệu đăng nhập theo từng scenario và yêu cầu evidence của HW05.

Student ID sử dụng trong tên test plan là `23127158`. Các test plan hiện tại gồm:

| Scenario | Test plan | Listener/report view |
|---|---|---|
| Load | `test-plans/23127158_Load_20260815.jmx` | Summary Report |
| Stress | `test-plans/23127158_Stress_20260816.jmx` | Aggregate Report |
| Spike | `test-plans/23127158_Spike_20260816.jmx` | View Results Tree |

## 2. Test Environment

Phần cứng và hệ điều hành được ghi nhận từ ảnh chụp DirectX Diagnostic Tool (`dxdiag`) trên máy local dùng để chạy SUT và JMeter.

| Mục | Thông tin |
|---|---|
| Evidence source | ![(nh chụp DirectX Diagnostic Tool, tab System](../screenshots/hardware-report.png) |
| Current date/time trong ảnh | Sunday, August 16, 2026, 10:03:54 PM |
| Computer name | `DESKTOP-8PSPNF6` |
| Operating system | Windows 11 Pro 64-bit, version 10.0, build 26200 |
| Language / regional setting | English / English |
| System manufacturer | LENOVO |
| System model | 83EG |
| BIOS | PJCN15WW |
| Processor | AMD Ryzen 7 7840H with Radeon 780M Graphics |
| CPU logical processors | 16 CPUs |
| Approximate CPU clock | ~3.8 GHz |
| Memory | 16384 MB RAM |
| Page file | 19547 MB used, 18537 MB available |
| DirectX version | DirectX 12 |

Môi trường kiểm thử là máy local Windows, chạy backend EShop tại `http://localhost:3000` và dùng Apache JMeter để phát tải vào REST API. Vì JMeter, Java runtime và resource-monitor version không hiển thị trong ảnh DxDiag, các thông tin đó sẽ được bổ sung sau khi chụp evidence chạy test hoặc xuất cấu hình công cụ.

| Thành phần | Cấu hình dùng trong bài |
|---|---|
| SUT backend | Node.js + Express + SQLite |
| Backend base URL | `http://localhost:3000` |
| Performance test tool | Apache JMeter |
| Test plan format | `.jmx` |
| Raw result format | `.jtl` |
| HTML report folders | `reports/html/load/`, `reports/html/stress/`, `reports/html/spike/` |
| Resource monitor evidence | Sẽ bổ sung bằng screenshot JMeter cùng Task Manager/resource monitor khi chạy từng scenario |

## 3. Test Design

### 3.1 Load

Load Test đo khả năng duy trì workflow `Buy-then-history` ở mức tải ổn định. Profile cuối cùng sử dụng 50 users, think time thực tế và cùng dữ liệu CSV/correlation như các scenario còn lại.

| Thuộc tính | Cấu hình |
|---|---|
| Tool | Apache JMeter |
| Thread group | Ultimate Thread Group |
| Workload profile | 50 users |
| Startup / ramp-up | 60 giây |
| Hold load | 360 giây |
| Shutdown | 60 giây |
| Think time | Uniform random 750-1750 ms |
| Auth CSV | `data/load_auth_users.csv` |
| Product CSV | `data/product_inputs.csv` |
| Checkout CSV | `data/checkout_inputs.csv` |
| Listener | Summary Report |
| Test plan | `test-plans/23127158_Load_20260815.jmx` |

Workflow gồm 6 request theo thứ tự: login, browse product list, view product detail, add to cart, checkout và read My Orders để verify order mới. Test plan dùng JWT `${token}` sau login và `${orderId}` sau checkout để kiểm tra đúng business flow.

### 3.2 Stress

Stress Test dùng cùng workflow nhưng tăng tải theo bậc để quan sát degradation hoặc breakpoint. Các row trong Ultimate Thread Group được cấu hình cộng dồn để tải tăng liên tục đến 500 users.

| Thuộc tính | Cấu hình |
|---|---|
| Tool | Apache JMeter |
| Thread group | Ultimate Thread Group |
| Workload profile | 50 -> 150 -> 300 -> 500 users |
| Schedule row 1 | +50 users, delay 0 giây, startup 60 giây, hold 420 giây, shutdown 60 giây |
| Schedule row 2 | +100 users, delay 120 giây, startup 60 giây, hold 360 giây, shutdown 60 giây |
| Schedule row 3 | +150 users, delay 240 giây, startup 60 giây, hold 240 giây, shutdown 60 giây |
| Schedule row 4 | +200 users, delay 360 giây, startup 60 giây, hold 60 giây, shutdown 60 giây |
| Think time | Uniform random 750-1750 ms |
| Auth CSV | `data/stress_auth_users.csv` |
| Product CSV | `data/product_inputs.csv` |
| Checkout CSV | `data/checkout_inputs.csv` |
| Listener | Aggregate Report |
| Test plan | `test-plans/23127158_Stress_20260816.jmx` |

Stress giữ cùng request sequence, CSV product/checkout, JWT/orderId correlation và assertions với Load Test. Điểm khác biệt chính là workload profile tăng dần và listener Aggregate Report.

### 3.3 Spike

Spike Test dùng cùng workflow để kiểm tra phản ứng khi tải tăng đột ngột rồi giảm về baseline. Profile cuối cùng dùng baseline 50 users, spike lên peak 500 users và có recovery window sau peak.

| Thuộc tính | Cấu hình |
|---|---|
| Tool | Apache JMeter |
| Thread group | Ultimate Thread Group |
| Workload profile | Baseline 50 users, spike lên peak 500 users |
| Baseline row | 50 users, delay 0 giây, startup 30 giây, hold 390 giây, shutdown 60 giây |
| Spike row | +450 users, delay 120 giây, startup 30 giây, hold 90 giây, shutdown 90 giây |
| Think time | Uniform random 500-1500 ms |
| Auth CSV | `data/spike_auth_users.csv` |
| Product CSV | `data/product_inputs.csv` |
| Checkout CSV | `data/checkout_inputs.csv` |
| Listener | View Results Tree |
| Test plan | `test-plans/23127158_Spike_20260816.jmx` |

Spike giữ cùng request sequence, CSV product/checkout, JWT/orderId correlation và assertions với Load/Stress. Listener View Results Tree được dùng để đảm bảo ba scenario có ba report/listener view khác nhau.

## 4. Test Execution and Results

### 4.1 Load

Nguồn kết quả chính thức: JMeter HTML report `reports/html-report/load-profile/index.html`, dữ liệu trong `reports/html-report/load-profile/statistics.json`.

| Metric | Value |
|---|---:|
| Sample count | 16.714 |
| Error count | 0 |
| Error rate | 0,0% |
| Mean response time | 2,671 ms |
| Median response time | 2,0 ms |
| Min response time | 0,0 ms |
| Max response time | 44,0 ms |
| 90th percentile | 5,0 ms |
| 95th percentile | 6,0 ms |
| 99th percentile | 9,0 ms |
| Throughput | 35,061 req/s |
| Received throughput | 39,599 KB/s |
| Sent throughput | 10,696 KB/s |

| Sampler / endpoint | Samples | Error % | Avg ms | p90 ms | p95 ms | p99 ms | Throughput req/s |
|---|---:|---:|---:|---:|---:|---:|---:|
| 01 Login | 2.805 | 0,0% | 3,040 | 4,0 | 5,0 | 9,940 | 5,895 |
| 02 Browse Product List | 2.801 | 0,0% | 1,568 | 2,0 | 3,0 | 6,980 | 5,891 |
| 03 View Product Detail | 2.789 | 0,0% | 1,573 | 2,0 | 3,0 | 7,0 | 5,897 |
| 04 Add To Cart | 2.779 | 0,0% | 1,740 | 2,0 | 3,0 | 3,0 | 5,929 |
| 05 Checkout | 2.775 | 0,0% | 5,730 | 8,0 | 9,0 | 11,0 | 5,914 |
| 06 My Orders Verify New Order | 2.765 | 0,0% | 2,388 | 3,0 | 4,0 | 7,0 | 5,892 |

### 4.2 Stress

_Tạm thời để trống._

### 4.3 Spike

_Tạm thời để trống._

## 5. Endurance / Soak Test

_Tạm thời để trống._

## 6. AI Analysis of Raw JTL Logs

### 6.1 Load

#### Objective Metrics From Raw JTL

| Metric | Value | Source |
|---|---:|---|
| Total samples | 16.714 | `results/load_result.jtl`, computed by `analyze_jtl.py` |
| Failures | 0 | `results/load_result.jtl`, computed by `analyze_jtl.py` |
| Error rate | 0,0% | `results/load_result.jtl`, computed by `analyze_jtl.py` |
| Duration | 476,709 s | `results/load_result.jtl`, computed by `analyze_jtl.py` |
| Throughput | 35,061 req/s | `results/load_result.jtl`, computed by `analyze_jtl.py` |
| Avg response time | 2,671 ms | `results/load_result.jtl`, computed by `analyze_jtl.py` |
| Median response time | 2,0 ms | `results/load_result.jtl`, computed by `analyze_jtl.py` |
| p90 response time | 5,0 ms | `results/load_result.jtl`, computed by `analyze_jtl.py` |
| p95 response time | 6,0 ms | `results/load_result.jtl`, computed by `analyze_jtl.py` |
| p99 response time | 9,0 ms | `results/load_result.jtl`, computed by `analyze_jtl.py` |
| Max response time | 44,0 ms | `results/load_result.jtl`, computed by `analyze_jtl.py` |
| Response codes | HTTP 200: 16.714 | `results/load_result.jtl`, computed by `analyze_jtl.py` |

#### Per-Sampler Metrics From Raw JTL

| Sampler / endpoint | Samples | Error % | Avg ms | p95 ms | p99 ms | Throughput req/s |
|---|---:|---:|---:|---:|---:|---:|
| 01 Login | 2.805 | 0,0% | 3,040 | 5,0 | 9,0 | 5,895 |
| 02 Browse Product List | 2.801 | 0,0% | 1,568 | 3,0 | 6,0 | 5,891 |
| 03 View Product Detail | 2.789 | 0,0% | 1,573 | 3,0 | 6,120 | 5,897 |
| 04 Add To Cart | 2.779 | 0,0% | 1,740 | 3,0 | 3,0 | 5,929 |
| 05 Checkout | 2.775 | 0,0% | 5,730 | 9,0 | 11,0 | 5,914 |
| 06 My Orders Verify New Order | 2.765 | 0,0% | 2,388 | 4,0 | 7,0 | 5,892 |

#### AI Interpretation

Raw JTL cho thấy Load Test 50 users chạy ổn định trong khoảng 476,709 giây với 16.714 request và không có lỗi. Error rate 0,0% và toàn bộ response code HTTP 200 cho thấy workflow `Buy-then-history` hoàn tất thành công ở mức tải steady-load này.

Overall latency rất thấp: avg 2,671 ms, p95 6,0 ms, p99 9,0 ms và max 44,0 ms. Điều này cho thấy trong môi trường local hiện tại, SUT chưa có dấu hiệu saturation ở profile Load 50 VU. Tuy nhiên, vì đây là môi trường local Node.js/Express + SQLite và không có APM/backend profiling đi kèm trong raw JTL, không nên suy luận rằng hệ thống sẽ giữ cùng mức latency khi deploy thật hoặc khi dữ liệu lớn hơn.

Sampler chậm nhất là `05 Checkout` với avg 5,730 ms, p95 9,0 ms, p99 11,0 ms và max 22,0 ms. Đây là kết quả hợp lý vì checkout là bước transactional có ghi dữ liệu, tạo order và cập nhật trạng thái liên quan. Các bước read-heavy như product list và product detail có p95 3,0 ms, thấp hơn checkout. `01 Login` có max 44,0 ms nhưng p95 chỉ 5,0 ms, nên đây là outlier nhỏ, chưa phải bằng chứng của degradation kéo dài.

#### AI-Proposed Thresholds

| Threshold | Proposed value | Rationale | Raw metric used |
|---|---:|---|---|
| Load p95 response-time threshold | <= 15 ms | Cao hơn 2,5 lần overall p95 hiện tại để có biên an toàn cho dao động local nhưng vẫn phát hiện regression rõ ràng. | Overall p95 = 6,0 ms |
| Load p99 response-time threshold | <= 25 ms | Cao hơn p99 hiện tại nhưng thấp hơn nhiều so với mức có thể làm người dùng cảm nhận chậm trong API local. | Overall p99 = 9,0 ms |
| Load error-rate threshold | <= 1,0% | Run hiện tại 0 lỗi; 1,0% là ngưỡng cảnh báo sớm cho workflow có login, cart và checkout. | Error rate = 0,0% |
| Load request-throughput target | >= 30 req/s | Run hiện tại đạt 35,061 req/s; đặt ngưỡng thấp hơn một chút để tránh fail do nhiễu nhỏ nhưng vẫn bắt được regression throughput. | Throughput = 35,061 req/s |
| Checkout p95 threshold | <= 20 ms | Checkout là bước transactional chậm nhất; ngưỡng này cao hơn p95 hiện tại nhưng vẫn đủ nhạy để bắt tail latency tăng. | Checkout p95 = 9,0 ms |

#### AI-Proposed Optimizations

| Recommendation | Evidence category | Metric / observation used | Expected effect |
|---|---|---|---|
| Giữ nguyên implementation hiện tại cho workload Load 50 VU, chưa tối ưu nóng khi chưa có regression. | Supported by raw evidence | 16.714 samples, 0 failures, p95 6,0 ms, throughput 35,061 req/s. | Tránh thay đổi không cần thiết khi hệ thống đang ổn định ở baseline Load. |
| Ưu tiên quan sát checkout trong Stress/Spike/Endurance trước khi tối ưu write path. | Plausible but not proven | Checkout là sampler chậm nhất trong Load: avg 5,730 ms, p95 9,0 ms. | Nếu các scenario mạnh hơn cho thấy checkout tail latency tăng, có thể tối ưu transaction/order write path đúng trọng tâm hơn. |
| Cân nhắc pagination hoặc giới hạn số bản ghi cho `My Orders` khi dữ liệu order của mỗi user tăng lớn. | Plausible but not proven | `My Orders` hiện p95 4,0 ms, chưa chậm trong Load; rủi ro chủ yếu đến từ dữ liệu tăng theo thời gian. | Giảm latency đọc lịch sử đơn hàng khi số lượng order/user tăng trong endurance hoặc dữ liệu lâu dài. |
| Cân nhắc composite index cho truy vấn order-history theo `user_id` và thời gian tạo nếu Stress/Spike/Endurance cho thấy `My Orders` tăng latency. | Plausible but not proven | Load hiện chưa chứng minh bottleneck; `My Orders` p95 4,0 ms. | Tăng tốc truy vấn lịch sử đơn hàng trong dữ liệu lớn, giảm p95/p99 cho read-after-checkout. |
| Chỉ bật/tinh chỉnh SQLite WAL hoặc busy timeout nếu các run tải cao hơn xuất hiện lock contention hoặc lỗi ghi. | Plausible but not proven | Load hiện 0 lỗi, Checkout p95 9,0 ms, không có bằng chứng lock từ JTL. | Giảm lỗi/độ trễ do lock SQLite nếu stress/spike thật sự tạo contention ghi. |

Kết luận sau review: Load Test 50 VU được xem là ổn định trong môi trường local. HTML report xác nhận 16.714 samples, 0 lỗi, error rate 0,0%, throughput 35,061 req/s, overall p95 6,0 ms và p99 9,0 ms. Các correction nhỏ ở p99 per-sampler đã được ghi ở mục 8.2 và không làm thay đổi kết luận chính của Load Test.

### 6.2 Stress

_Tạm thời để trống._

### 6.3 Spike

_Tạm thời để trống._

## 7. Cross-Scenario Analysis and Final Thresholds

_Tạm thời để trống._

## 8. AI Misinterpretation Hunt

### 8.1 Task 1 - AI Test Plan Review

Phần này ghi lại các điểm AI-generated test plan hoặc thiết kế ban đầu cần được human review chỉnh lại trước khi dùng làm bản cuối.

| Scenario | AI output / issue | Human correction | Final decision |
|---|---|---|---|
| Load | Profile ban đầu quá nhẹ, chưa tạo baseline đủ mạnh cho môi trường local. | Chỉnh Load profile thành 50 users, ramp-up 60 giây, hold 360 giây, shutdown 60 giây. | Đã hiệu chỉnh |
| Load | Cần tránh nhiều virtual users dùng chung credential. | Mở rộng `data/load_auth_users.csv` và seed data để có 50 tài khoản Load. | Đã hiệu chỉnh |
| Load | Test plan cần dùng workload profile rõ ràng và ổn định. | Dùng Ultimate Thread Group cho Load plan cuối cùng. | Đã hiệu chỉnh |
| Stress | Thiết kế ban đầu chưa đủ mạnh để quan sát breakpoint rõ ràng. | Chỉnh profile thành 50 -> 150 -> 300 -> 500 users. | Đã hiệu chỉnh |
| Stress | Có nguy cơ hiểu sai Ultimate Thread Group như các mức tải độc lập, làm tải rơi giữa các level. | Cấu hình các row cộng dồn để tải tăng liên tục đến peak 500 users. | Đã hiệu chỉnh |
| Stress | Dữ liệu đăng nhập ban đầu không đủ cho peak workload. | Mở rộng `data/stress_auth_users.csv` và seed data lên 500 tài khoản Stress. | Đã hiệu chỉnh |
| Spike | Profile 50 -> 1000 users quá aggressive cho máy local, có thể đo giới hạn JMeter/thiết bị thay vì SUT. | Loại bỏ kết quả Spike cũ và thiết kế lại workload. | Bị từ chối |
| Spike | Profile 20 -> 200 users sau đó chưa đủ mạnh so với mục tiêu spike. | Chỉnh profile cuối thành baseline 50 users, spike lên peak 500 users, có recovery window. | Đã hiệu chỉnh |
| Spike | Dữ liệu auth cần đủ cho peak 500 users. | Dùng `data/spike_auth_users.csv` với số lượng tài khoản đủ cho peak workload. | Đã hiệu chỉnh |

### 8.2 Task 2 - Load HTML Report Cross-Check

Nguồn đối chiếu là JMeter HTML dashboard tại `reports/html-report/load-profile/index.html`, đọc qua file dữ liệu `reports/html-report/load-profile/statistics.json`. Mục tiêu là kiểm tra lại phần AI analysis ở mục 6.1 so với số liệu do JMeter HTML report sinh ra.

| AI claim or recommendation | Raw evidence / correct value | Human decision | Reason |
|---|---|---|---|
| Total samples của Load Test là 16.714. | HTML report `Total.sampleCount = 16714`. | Đúng | Khớp với cả `statistics.json` và kết quả `analyze_jtl.py`. |
| Error rate là 0,0% và toàn bộ request không lỗi. | HTML report `Total.errorCount = 0`, `Total.errorPct = 0.0`. | Đúng | Không có sai khác giữa HTML report và raw JTL analysis. |
| Overall throughput là 35,061 req/s. | HTML report `Total.throughput = 35.06114828721864 req/s`. | Đúng | Giá trị AI làm tròn thành 35,061 req/s là đúng. |
| Overall avg/p95/p99/max lần lượt là 2,671 ms / 6,0 ms / 9,0 ms / 44,0 ms. | HTML report `meanResTime = 2.6711140361373675`, `pct2ResTime = 6.0`, `pct3ResTime = 9.0`, `maxResTime = 44.0`. | Đúng | Các metric tổng quan khớp với HTML dashboard. |
| `05 Checkout` là sampler chậm nhất với avg 5,730 ms, p95 9,0 ms, p99 11,0 ms. | HTML report cho Checkout: `meanResTime = 5.730450450450459`, `pct2ResTime = 9.0`, `pct3ResTime = 11.0`. | Đúng | Checkout có mean cao nhất trong các sampler và các percentile chính khớp HTML report. |
| `01 Login` p99 là 9,0 ms. | HTML report cho Login: `pct3ResTime = 9.940000000000055 ms`; custom analyzer trả 9,0 ms. | Đã hiệu chỉnh | Sai khác do cách tính/làm tròn percentile giữa JMeter HTML dashboard và script custom. Khi viết kết luận cuối, dùng p99 Login xấp xỉ 9,94 ms theo HTML report. |
| `02 Browse Product List` p99 là 6,0 ms. | HTML report cho Browse Product List: `pct3ResTime = 6.980000000000018 ms`; custom analyzer trả 6,0 ms. | Đã hiệu chỉnh | Sai khác do cách tính/làm tròn percentile giữa JMeter HTML dashboard và script custom. Khi viết kết luận cuối, dùng p99 Browse xấp xỉ 6,98 ms theo HTML report. |
| `03 View Product Detail` p99 là 6,120 ms. | HTML report cho View Product Detail: `pct3ResTime = 7.0 ms`; custom analyzer trả 6,120 ms. | Đã hiệu chỉnh | Sai khác percentile nhỏ giữa hai nguồn tính toán. Kết luận không đổi vì p99 vẫn rất thấp và không có lỗi. |
| Đề xuất giữ implementation hiện tại cho Load baseline. | HTML report xác nhận 16.714 samples, 0 lỗi, overall p95 6,0 ms, p99 9,0 ms. | Khả thi | Đề xuất có cơ sở từ raw evidence và HTML report; chưa cần tối ưu nóng cho riêng Load baseline. |
| Đề xuất pagination/index/WAL chỉ nên cân nhắc khi Stress/Spike/Endurance có bằng chứng thêm. | HTML report Load không cho thấy lỗi, lock contention hoặc My Orders bottleneck; My Orders p95 = 4,0 ms, p99 = 7,0 ms. | Có cơ sở nhưng chưa chứng minh | Đây là nhận định phòng ngừa, không phải kết luận bottleneck từ Load run. Cần scenario tải cao hoặc dữ liệu lớn hơn để chứng minh. |

Kết luận review cho Load Phase 4: phần AI analysis ở mục 6.1 không có sai lệch lớn về tổng quan. Các số liệu tổng như samples, error rate, throughput, overall p95/p99 và Checkout metrics khớp HTML report. Sai khác cần ghi nhận nằm ở một số p99 per-sampler (`Login`, `Browse Product List`, `View Product Detail`) vì JMeter HTML dashboard và script custom dùng cách tính percentile/làm tròn khác nhau. Các sai khác này không làm thay đổi kết luận rằng Load 50 VU đang ổn định, nhưng khi viết kết luận cuối nên ưu tiên số percentile từ HTML report cho các sampler bị lệch.

## 9. Optimization Recommendations

_Tạm thời để trống._

## 10. Performance Issues / Bugs

_Tạm thời để trống._

## 11. Continuous Performance Testing Proposal

_Tạm thời để trống._
