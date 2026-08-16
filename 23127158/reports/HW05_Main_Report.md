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

## 3. AI-Assisted Test Design

### 3.1 Load

Load Test dùng cùng workflow `Buy-then-history` để đo mức tải ổn định có kiểm soát. Thiết kế ban đầu của AI quá an toàn ở mức 10 VU, nên sau review và chạy thử, profile được chỉnh thành 50 concurrent users để tạo baseline mạnh hơn nhưng vẫn không biến thành Stress Test. Mục tiêu của Load Test là kiểm tra hệ thống có duy trì được luồng mua hàng hoàn chỉnh ở tải ổn định, error rate thấp và latency p95 không tăng bất thường hay không.

| Thuộc tính | Thiết kế cuối cùng |
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

AI hỗ trợ tạo cấu trúc JMeter gồm HTTP Request Defaults, CSV Data Set Config, JSON headers, sampler sequence, JSON extractor và response assertions. Human review đã phát hiện và sửa các điểm chính: dùng Ultimate Thread Group thay vì standard Thread Group, mở rộng dữ liệu đăng nhập Load lên 50 tài khoản để tránh nhiều VU dùng chung user, và giữ think time đủ thực tế để request không chạy thành vòng lặp quá gắt.

Các assertion quan trọng gồm kiểm tra HTTP 200 cho từng bước, kiểm tra token sau login, kiểm tra product response chứa dữ liệu đúng, kiểm tra checkout thành công và kiểm tra My Orders chứa order mới thông qua `${orderId}` được trích xuất từ response checkout.

### 3.2 Stress

Stress Test dùng cùng workflow nhưng tăng tải theo bậc để tìm dấu hiệu breakpoint hoặc degradation. AI ban đầu tạo profile quá nhẹ và từng có lỗi diễn giải Ultimate Thread Group như các mức độc lập, có nguy cơ làm tải rơi giữa các level. Sau human review, profile được chỉnh thành các row cộng dồn trong Ultimate Thread Group để tải tăng liên tục đến 500 users.

| Thuộc tính | Thiết kế cuối cùng |
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

Thiết kế Stress nhấn mạnh quan sát p95/p99, throughput, error rate, max latency outlier và resource usage khi tải tăng. Human review đã yêu cầu tăng workload vì profile cũ chỉ đến 50 VU chưa đủ để tìm breakpoint rõ ràng. Dữ liệu đăng nhập Stress cũng được mở rộng lên 500 tài khoản để peak 500 VU không bị thiếu credential hoặc nhiễu bởi tài khoản dùng chung.

Các bước request, correlation và assertion vẫn giữ giống Load Test để kết quả giữa các scenario có thể so sánh được. Điểm khác biệt chính của Stress nằm ở workload profile và listener Aggregate Report.

### 3.3 Spike

Spike Test dùng cùng workflow để kiểm tra phản ứng của hệ thống khi tải tăng đột ngột rồi giảm về baseline. AI từng đề xuất spike 50 -> 1000 VU, nhưng profile này bị human review đánh giá là quá aggressive cho máy local vì có thể đo giới hạn JMeter/thiết bị thay vì SUT. Sau đó profile 20 -> 200 VU lại bị xem là chưa đủ mạnh, nên bản cuối cùng được cân bằng ở baseline 50 users và peak 500 users.

| Thuộc tính | Thiết kế cuối cùng |
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

Thiết kế này có baseline trước spike, giai đoạn tăng tải nhanh trong 30 giây, hold peak ngắn để quan sát phản ứng dưới cú sốc tải, và recovery/shutdown để xem hệ thống có phục hồi sau spike hay không. Human review giữ lại peak 500 VU vì nó đủ mạnh hơn Load/Stress ban đầu nhưng vẫn hợp lý hơn profile 1000 VU trên môi trường local.

Spike dùng `data/spike_auth_users.csv`, hiện có đủ dữ liệu cho peak 500 VU. Listener View Results Tree được dùng cho Spike để đáp ứng yêu cầu ba scenario có ba report/listener view khác nhau: Load dùng Summary Report, Stress dùng Aggregate Report, Spike dùng View Results Tree.

## 4. Test Execution and Results

### 4.1 Load

_Tạm thời để trống._

### 4.2 Stress

_Tạm thời để trống._

### 4.3 Spike

_Tạm thời để trống._

## 5. Endurance / Soak Test

_Tạm thời để trống._

## 6. AI Analysis of Raw JTL Logs

### 6.1 Load

_Tạm thời để trống._

### 6.2 Stress

_Tạm thời để trống._

### 6.3 Spike

_Tạm thời để trống._

## 7. Cross-Scenario Analysis and Final Thresholds

_Tạm thời để trống._

## 8. AI Misinterpretation Hunt

_Tạm thời để trống._

## 9. Optimization Recommendations

_Tạm thời để trống._

## 10. Performance Issues / Bugs

_Tạm thời để trống._

## 11. Continuous Performance Testing Proposal

_Tạm thời để trống._
