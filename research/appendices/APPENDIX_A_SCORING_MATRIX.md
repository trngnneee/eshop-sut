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
