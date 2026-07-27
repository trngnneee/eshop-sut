# BÁO CÁO SEMINAR PERFORMANCE TESTING TOOLS

> **Môn học:** Software Testing  
> **Chủ đề:** Performance Testing tools  
> **Hệ thống được kiểm thử:** EShop  
> **Nhóm:** Nhóm 7 

---

# Mục lục

1. Tóm tắt báo cáo  
2. Thông tin nhóm và phân công  
3. Giới thiệu  
4. Cơ sở lý thuyết Performance Testing  
5. Hệ thống EShop và phạm vi kiểm thử  
6. Phương pháp khảo sát công cụ  
7. Khảo sát 15 công cụ Performance Testing  
8. Sàng lọc và lập danh sách rút gọn  
9. Lý do lựa chọn Apache JMeter và k6  
10. Workload Model cho EShop  
11. Phương pháp thực nghiệm  
12. Triển khai bằng Apache JMeter  
13. Triển khai bằng k6  
14. AI-Augmented Performance Testing và AI Audit  
15. Kịch bản demo  
16. Kết quả thực nghiệm và phân tích  
17. So sánh JMeter và k6  
18. Troubleshooting  
19. Failure Modes  
20. Giới hạn nghiên cứu  
21. Kết luận và khuyến nghị  
22. AI Usage Declaration  
23. Tài liệu tham khảo  

---

# 1. Tóm tắt báo cáo

Performance Testing được sử dụng để đánh giá tốc độ phản hồi, khả năng xử lý tải, độ ổn định và hành vi suy giảm của hệ thống khi số người dùng hoặc số request tăng. Trong seminar T05, nhóm khảo sát 15 công cụ gồm Apache JMeter, Silk Performer, Artillery, k6, Locust, Gatling, Loader.io, Siege, Vegeta, wrk, NeoLoad, ApacheBench, OpenText LoadRunner Professional, Tsung và Taurus.

Quá trình lựa chọn không dựa trên nhận định “công cụ nào mạnh nhất”, vì không có một công cụ tối ưu cho mọi bối cảnh. Nhóm đánh giá các công cụ theo mức độ phù hợp với EShop, khả năng mô phỏng user journey nhiều bước, chi phí tiếp cận, learning curve, khả năng tái tạo, reporting, CI/CD, hoạt động trong lớp học và khả năng kết hợp với AI.

Sau hai vòng sàng lọc, nhóm chọn **Apache JMeter** và **k6** làm hai công cụ chính. JMeter đại diện cho cách tiếp cận trực quan dựa trên Test Plan, trong đó người dùng xây dựng Thread Group, Sampler, Timer, Assertion và các thành phần cấu hình qua GUI; khi chạy tải chính thức, JMeter được thực thi bằng CLI. k6 đại diện cho cách tiếp cận test-as-code, sử dụng JavaScript để định nghĩa scenarios, executors, checks và thresholds. Hai công cụ bổ sung cho nhau và cho phép nhóm so sánh hai phương pháp xây dựng Performance Test thay vì chọn hai công cụ có cách sử dụng gần như giống nhau.

Báo cáo thiết kế các kịch bản baseline, normal load, spike và stress cho EShop. Tài liệu T05 yêu cầu nhóm có khả năng triển khai workload bằng JMeter và k6, chạy baseline 50 VU và spike 50 lên 500 VU trong 30 giây, đồng thời thu thập p50, p95, p99 và error rate. 

---

# 2. Thông tin nhóm và phân công

## 2.1. Thành viên

| MSSV | Họ và tên | Công cụ khảo sát | Trách nhiệm thực nghiệm |
|---|---|---|---|
| 23127271 | Võ Ngọc Bích Trâm | JMeter, Silk Performer, Artillery | `[CẦN ĐIỀN]` |
| 23127207 | Đặng Đăng Khoa | k6, Locust, Gatling | Xây dựng tiêu chí lựa chọn; tổng hợp khảo sát; thiết kế Workload Model; viết k6 script; AI Audit; so sánh JMeter–k6 |
| 23127458 | Phan Quốc Thịnh | Loader.io, Siege, Vegeta | `[CẦN ĐIỀN]` |
| 23127158 | Nguyễn Thanh Gia Bảo | wrk, NeoLoad, ApacheBench | `[CẦN ĐIỀN]` |
| 23127438 | Đặng Trường Nguyên | OpenText LoadRunner Professional, Tsung, Taurus | Khảo sát ba hướng enterprise, distributed và orchestration; thực hiện smoke test trong phạm vi licence/môi trường; tổng hợp hạn chế và lý do không chọn vào cặp demo chính |

---

# 3. Giới thiệu

## 3.1. Bối cảnh

Functional Testing trả lời câu hỏi hệ thống có thực hiện đúng chức năng hay không. Tuy nhiên, một chức năng có thể trả về dữ liệu chính xác nhưng phản hồi quá chậm, thất bại khi số user tăng hoặc không phục hồi sau spike. Vì vậy, chất lượng của hệ thống còn phụ thuộc vào hiệu năng và độ ổn định dưới tải.

Đối với hệ thống thương mại điện tử, hành vi người dùng thường gồm nhiều bước: xem danh sách sản phẩm, tìm kiếm, xem chi tiết, đăng nhập, thêm giỏ hàng và checkout. Tỷ lệ xuất hiện của các hành vi này không giống nhau. Một workload chỉ lặp lại một endpoint với tốc độ rất cao có thể hữu ích để benchmark endpoint đó, nhưng không đủ để đại diện cho hành vi của người dùng EShop.

## 3.2. Vấn đề nghiên cứu

Báo cáo tập trung trả lời bốn vấn đề:

1. Trong 15 công cụ đã khảo sát, công cụ nào phù hợp để mô hình hóa và chạy workload EShop?
2. Vì sao chọn JMeter và k6 thay vì chọn theo độ phổ biến hoặc cảm tính?
3. Trên cùng workload, hai cách tiếp cận GUI-oriented và test-as-code khác nhau như thế nào?
4. AI giúp xây dựng Performance Test ở đâu, và AI có thể tạo ra những lỗi gì?

## 3.3. Mục tiêu

- Trình bày đúng các khái niệm cốt lõi của Performance Testing.
- Khảo sát 15 công cụ bằng một phương pháp nhất quán.
- Sàng lọc công cụ theo đặc điểm và giới hạn thực tế.
- Chọn JMeter và k6 bằng lập luận có thể kiểm chứng.
- Xây dựng Workload Model phản ánh hành vi EShop.
- Thực thi cùng workload trên JMeter và k6.
- Thu thập p50, p95, p99, throughput và error rate.
- Audit script do AI tạo thay vì sử dụng trực tiếp.
- Ghi nhận Troubleshooting và Failure Modes.

---

# 4. Cơ sở lý thuyết Performance Testing

Hiểu rõ các khái niệm cơ bản và phân loại trong kiểm thử hiệu năng là bước đầu tiên để xây dựng một chiến lược kiểm thử chính xác. Dưới đây là các định nghĩa, mục tiêu và phân loại chi tiết của Performance Testing.

## 4.1. Performance Testing là gì?

**Performance Testing** là một loại kiểm thử phi chức năng (non-functional testing), nhằm đánh giá hành vi và phản ứng của hệ thống dưới một khối lượng công việc hoặc lượt truy cập cụ thể. Mục tiêu cốt lõi không phải là kiểm tra xem hệ thống có *hoạt động đúng tính năng* hay không, mà là đo lường xem hệ thống hoạt động *nhanh đến mức nào*, *ổn định ra sao*, và *chịu tải được bao nhiêu*.

## 4.2. Mục tiêu của Performance Testing

Dựa trên định nghĩa về kiểm thử hiệu năng, hoạt động này hướng đến các mục tiêu kỹ thuật và trải nghiệm cụ thể sau:

* **Đo lường thời gian phản hồi:** Xác định hệ thống mất bao lâu để xử lý và hoàn thành một yêu cầu từ người dùng.
* **Đánh giá thông lượng:** Đo số lượng giao dịch hoặc yêu cầu mà hệ thống xử lý thành công trong một đơn vị thời gian.
* **Xác định giới hạn tải:** Tìm ra ngưỡng tải tối đa mà tại đó hệ thống bắt đầu suy giảm hiệu năng hoặc gặp lỗi.
* **Phát hiện nút thắt cổ chai:** Nhận diện các thành phần gây chậm trễ trong toàn bộ kiến trúc hệ thống (CPU, bộ nhớ, cơ sở dữ liệu, băng thông mạng, v.v.).
* **Xác nhận khả năng đáp ứng SLA:** Kiểm tra xem hệ thống có đáp ứng được các cam kết về mức độ dịch vụ (Service Level Agreement) đã thỏa thuận hay không.
* **Đảm bảo trải nghiệm người dùng:** Xác minh rằng thời gian chờ đợi của người dùng cuối luôn nằm trong ngưỡng chấp nhận được.

## 4.3. Các loại Performance Testing

Để đạt được những mục tiêu trên, người ta không dùng một phương pháp duy nhất mà chia thành nhiều loại kiểm thử con. Mỗi loại được thiết kế để kiểm tra một khía cạnh cơ học riêng biệt của hệ thống dưới các mô hình tải khác nhau.

### 4.3.1. Load Testing 

**Định nghĩa:** Load testing là quá trình mô phỏng lượng tải dự kiến áp lên hệ thống để đánh giá hành vi của nó dưới điều kiện làm việc bình thường và lúc cao điểm. Đây là loại hình phổ biến nhất và thường là bước khởi đầu trong quy trình kiểm thử hiệu năng.

**Mục tiêu:** 
- Xác nhận hệ thống đáp ứng được yêu cầu hiệu năng ở mức tải kỳ vọng.

* Phát hiện các vấn đề hiệu năng xuất hiện khi số lượng người dùng tăng dần.
* Xác định mối quan hệ tuyến tính hoặc phi tuyến giữa mức độ tải và thời gian phản hồi.

---

### 4.3.2. Stress Testing 

**Định nghĩa:** Stress testing đánh giá hành vi của hệ thống khi bị đẩy **vượt quá** giới hạn thiết kế thông thường. Mục đích không phải để chứng minh hệ thống hoạt động tốt dưới tải, mà là để tìm ra điểm gãy (breaking point) và quan sát cách hệ thống tự phục hồi.

**Mục tiêu:** 
- Xác định điểm giới hạn tối đa mà hệ thống sụp đổ hoàn toàn.

* Đánh giá khả năng tự phục hồi (recovery) sau khi áp lực tải giảm xuống.
* Xác định các lỗi nghiêm trọng chỉ xảy ra dưới áp lực cao (rò rỉ bộ nhớ, deadlock, timeout, v.v.).
* Đánh giá hệ thống xử lý lỗi một cách êm ái (graceful degradation) hay crash đột ngột làm mất dữ liệu.

---

### 4.3.3. Spike Testing 

**Định nghĩa:** Spike testing là một dạng đặc biệt của stress testing, trong đó lượng tải tăng **đột ngột** và **mạnh** trong khoảng thời gian rất ngắn, rồi giảm xuống ngay sau đó. Loại kiểm thử này mô phỏng các tình huống đột biến trong thực tế như sự kiện Flash Sale hoặc lỗi hệ thống mạng khiến request bị dồn ứ lại.

**Mục tiêu:** 
- Đánh giá khả năng xử lý các đỉnh tải đột biến bất ngờ mà không làm gián đoạn dịch vụ.

* Kiểm tra cơ chế tự động mở rộng quy mô (auto-scaling) có phản ứng kịp thời và chính xác không.
* Đánh giá hệ thống có nhanh chóng quay lại trạng thái ổn định sau khi đỉnh tải qua đi hay không.

---

### 4.3.4. Endurance Testing / Soak Testing 

**Định nghĩa:** Endurance testing (hay soak testing) đánh giá hệ thống khi chạy dưới **mức tải tiêu chuẩn** nhưng duy trì trong **thời gian dài** liên tục (nhiều giờ, nhiều ngày hoặc thậm chí hàng tuần). Mục đích là phát hiện các lỗi tích tụ theo thời gian.

**Mục tiêu:** - Phát hiện tình trạng rò rỉ bộ nhớ (memory leak) - bộ nhớ tăng dần theo thời gian mà không được bộ thu gom rác giải phóng.

* Phát hiện rò rỉ kết nối cơ sở dữ liệu (database connection leak) - các kết nối mở ra nhưng không được đóng lại cho đến khi cạn kiệt resource pool.
* Đánh giá sự suy giảm hiệu năng dần dần do các file log quá lớn hoặc phân mảnh dữ liệu.
* Kiểm tra tính ổn định lâu dài của các thành phần bên thứ ba hoặc các tầng đệm (cache, message queue).

---

### 4.3.5. Volume Testing 

**Định nghĩa:** Volume testing (còn gọi là flood testing) tập trung đánh giá hành vi của hệ thống khi phải xử lý và lưu trữ một **khối lượng dữ liệu cực lớn**. Trọng tâm ở đây không nằm ở số lượng người dùng đồng thời, mà nằm ở kích thước tệp tin hoặc số lượng bản ghi trong cơ sở dữ liệu.

**Mục tiêu:** - Xác định xem hệ thống có bị suy giảm hiệu năng truy vấn, tìm kiếm hoặc kết xuất báo cáo khi dữ liệu phình to hay không.

* Phát hiện các lỗi tràn bộ đệm hoặc giới hạn lưu trữ vật lý của hệ thống.
* Đánh giá tính ổn định khi thực hiện migration (dịch chuyển) dữ liệu lớn từ hệ thống cũ sang mới.

---

### 4.3.6. Scalability Testing 

**Định nghĩa:** Scalability testing đánh giá năng lực của hệ thống trong việc mở rộng quy mô phần cứng nhằm đáp ứng lượng tải lớn hơn. Việc mở rộng bao gồm cả chiều dọc (vertical scaling - nâng cấp CPU, RAM của server hiện tại) và chiều ngang (horizontal scaling - bổ sung thêm nhiều server vào cụm cluster).

**Mục tiêu:** - Xác định xem hiệu năng hệ thống có tăng trưởng tuyến tính với tài nguyên bổ sung hay không (ví dụ: nhân đôi cấu hình thì năng lực chịu tải có tăng gấp đôi không).

* Tìm ra điểm nghẽn kiến trúc khiến việc thêm tài nguyên phần cứng không còn mang lại hiệu quả cải thiện hiệu năng.
* Cung cấp dữ liệu thực tế để lập chiến lược tối ưu chi phí hạ tầng.

---

## 4.4. Các chỉ số đánh giá hiệu năng 

Để định lượng chính xác kết quả từ các loại kiểm thử hiệu năng phía trên, các kỹ sư cần dựa vào các chỉ số đo lường chuẩn hóa. Các chỉ số này phản ánh cả góc nhìn từ phía người dùng (thời gian) lẫn góc nhìn từ phía hệ thống (tài nguyên).

### 4.4.1. Response Time 

**Định nghĩa:** Response time là tổng thời gian tính từ khi client gửi một yêu cầu (request) đi cho đến khi nhận được phản hồi hoàn chỉnh (response) trả về từ phía server. Đây là chỉ số quan trọng nhất quyết định trải nghiệm người dùng cuối.

**Công thức tính toán:** 

$$\text{Response Time} = \text{Network Latency (Go)} + \text{Server Processing Time} + \text{Network Latency (Return)}$$

**Tầm quan trọng:** Phản ánh trực tiếp độ trễ mà người dùng phải chịu đựng. Một hệ thống xử lý nội bộ rất nhanh nhưng mạng chậm thì response time vẫn lớn, khiến trải nghiệm người dùng bị giảm sút.

---

### 4.4.2. Latency 

**Định nghĩa:** Latency là khoảng thời gian trễ trước khi quá trình truyền dữ liệu thực sự bắt đầu. Trong ngữ cảnh web, nó thường được hiểu là thời gian để byte dữ liệu đầu tiên (TTFB) truyền từ server quay trở lại đến client sau khi nhận request.

**Tầm quan trọng:** Biến số này giúp cô lập vấn đề xem sự chậm trễ nằm ở đường truyền vật lý hay ở khâu xử lý logic của máy chủ. Nó cực kỳ quan trọng đối với các ứng dụng thời gian thực như video call, giao dịch chứng khoán hoặc game online.

---

### 4.4.3. Throughput 

**Định nghĩa:** Throughput là số lượng đơn vị công việc mà hệ thống tiếp nhận và xử lý thành công trong một đơn vị thời gian cố định. Nó đại diện cho năng lực tải và sức chứa tổng thể của toàn bộ kiến trúc.

**Đơn vị đo phổ biến:**
- Requests per second (req/s): Số yêu cầu trên mỗi giây.

* Transactions per second (TPS): Số giao dịch nghiệp vụ hoàn thành trên mỗi giây.
* Megabytes per second (MB/s): Tốc độ truyền tải băng thông dữ liệu.

**Tầm quan trọng:** Giúp xác định năng lực phục vụ số đông. Khi throughput đạt ngưỡng trần (saturation point), các request mới sẽ bị đẩy vào hàng đợi (queue), kéo theo response time tăng vọt một cách đột ngột.

---

### 4.4.4. Error Rate (Tỷ lệ lỗi)

**Định nghĩa:** Error rate là tỷ lệ phần trăm các yêu cầu bị lỗi (như lỗi kết nối, lỗi phản hồi HTTP 5xx) so với tổng số lượng yêu cầu được gửi lên hệ thống trong suốt phiên kiểm thử.

**Công thức tính toán:** 

$$\text{Error Rate (%)} = \left( \frac{\text{Số request bị lỗi}}{\text{Tổng số request gửi đi}} \right) \times 100$$

**Tầm quan trọng:** Định lượng độ tin cậy của phần mềm dưới áp lực tải. Nếu hệ thống phản hồi cực nhanh nhưng tỷ lệ lỗi lên tới 30%, điều đó chứng tỏ hệ thống đang từ chối phục vụ hoặc bị sụp đổ cục bộ bên trong cấu trúc logic.

---

### 4.4.5. Concurrent Users (Người dùng đồng thời)

**Định nghĩa:** Concurrent users là số lượng người dùng (hoặc các Virtual Users - VU trong script) đang thực hiện các tương tác tích cực và gửi yêu cầu đến hệ thống tại cùng một thời điểm.

**Phân biệt khái niệm:** Cần phân biệt rõ với *Simultaneous Users* (người dùng kết nối đồng thời nhưng có thể đang trong trạng thái nghỉ/đọc thông tin mà không gửi request) và *Active Sessions* (phiên làm việc còn hiệu lực trong bộ nhớ server nhưng không phát sinh traffic). Concurrent users là tham số đầu vào cốt lõi để thiết kế kịch bản tải.

---

### 4.4.6. Resource Utilization (Mức sử dụng tài nguyên)

**Định nghĩa:** Resource Utilization đo lường mức độ tiêu thụ các tài nguyên phần cứng vật lý hoặc ảo hóa của các máy chủ thành phần (Web Server, App Server, Database Server) khi bài test hiệu năng diễn ra.

**Các chỉ số thành phần chính cần theo dõi:** - **CPU Utilization (%):** Tỷ lệ phần trăm năng lực xử lý của vi xử lý đang bị chiếm dụng. Mức an toàn thường dưới 75-80%.

* **Memory Utilization / RAM Usage:** Lượng bộ nhớ RAM bị chiếm giữ. Nếu đồ thị RAM tăng liên tục không giảm, đó là dấu hiệu của memory leak.
* **Disk I/O (Input/Output):** Tốc độ đọc và ghi dữ liệu lên ổ đĩa. Đây thường là nút thắt cổ chai lớn nhất ở các máy chủ database do tốc độ ghi đĩa vật lý có giới hạn.
* **Network I/O:** Lượng băng thông mạng tiêu thụ ở các cổng inbound/outbound.

**Tầm quan trọng:** Chỉ số này chỉ ra nguyên nhân gốc rễ (Root Cause Analysis) của các vấn đề hiệu năng. Nó giúp đội ngũ hạ tầng biết chính xác thành phần nào đang bị vắt kiệt sức để đưa ra phương án tối ưu phần mềm hoặc nâng cấp phần cứng phù hợp.

---

### 4.4.7. Percentile (Phân vị: p50, p90, p95, p99)

**Định nghĩa:** Percentile là phương pháp thống kê toán học dùng để mô tả sự phân bố của chỉ số thời gian phản hồi, giúp loại bỏ sự sai lệch của các giá trị trung bình đơn thuần. Giá trị phân vị thứ $N$ (ký hiệu p$N$) nghĩa là có $N\%$ số lượng request có thời gian phản hồi thấp hơn hoặc bằng giá trị đó.

* **p50 (Median):** Giá trị trung vị, phản ánh thời gian phản hồi của một người dùng ở mức trung bình của hệ thống.
* **p90:** 90% số request có thời gian phản hồi bằng hoặc nhanh hơn giá trị này. Phản ánh trải nghiệm của đại đa số người dùng.
* **p95:** Ngưỡng tiêu chuẩn phổ biến nhất khi ký kết các văn bản SLA kỹ thuật.
* **p99:** Biểu thị nhóm 1% khách hàng phải chịu đựng thời gian phản hồi chậm nhất (tail latency).

**Tầm quan trọng:** Percentile phản ánh chân thực hơn nhiều so với giá trị trung bình (average). Nếu một hệ thống có 99 request phản hồi trong 10ms và 1 request phản hồi trong 10,000ms, thời gian trung bình sẽ là ~110ms. Con số này che giấu việc có 1% khách hàng phải đợi tới 10 giây. Chỉ số Percentile sẽ bộc lộ rõ ràng điểm yếu chí mạng này.

---

## 4.5. Quy trình kiểm thử Performance Testing chuẩn

Để thu thập các chỉ số đo lường trên một cách chính xác và có thể lặp lại, quy trình thực hiện kiểm thử hiệu năng cần tuân thủ theo các bước kỹ thuật chặt chẽ, từ khâu lập kế hoạch cho đến phân tích báo cáo.

### Bước 1: Xác định môi trường kiểm thử (Identify the Test Environment)

Trước khi bắt đầu, kiểm thử viên cần nắm rõ kiến trúc vật lý, kiến trúc mạng và cấu hình phần cứng của hệ thống được kiểm thử (SUT - System Under Test) cũng như công cụ tạo tải. Môi trường kiểm thử hiệu năng nên được tách biệt hoàn toàn với môi trường phát triển (Dev) hoặc kiểm thử chức năng (QC/Staging) thông thường để tránh nhiễu số liệu, và lý tưởng nhất là cấu hình phải tương đương hoặc tiệm cận với môi trường Production.

### Bước 2: Xác định các tiêu chí đánh giá hiệu năng (Identify Performance Acceptance Criteria)

Ở bước này, đội ngũ kiểm thử phải làm việc với các bên liên quan (Product Owner, Architecture, Business Analyst) để xác định các mục tiêu cụ thể hoặc các chỉ số SLA mong muốn. Các tiêu chí này bao gồm giới hạn tối đa chấp nhận được của thời gian phản hồi (Response Time), thông lượng mục tiêu (Throughput), tỷ lệ lỗi tối đa (Error Rate) và ngưỡng giới hạn tiêu thụ tài nguyên phần cứng (CPU, RAM).

### Bước 3: Lập kế hoạch và thiết kế kịch bản (Plan & Design Performance Tests)

Giai đoạn này bao gồm việc xác định các kịch bản nghiệp vụ chính mà người dùng thực tế thường xuyên thao tác (ví dụ: đăng nhập, tìm kiếm sản phẩm, thêm vào giỏ hàng, thanh toán). Từ đó, kiểm thử viên định hình mô hình tải (Workload Model), xác định số lượng người dùng ảo (VU), thiết lập tốc độ tăng tải (Ramp-up), thời gian duy trì tải tối đa (Duration) và tốc độ giảm tải (Ramp-down).

### Bước 4: Cấu hình môi trường và chuẩn bị dữ liệu (Configure the Test Environment & Data)

Chuẩn bị các công cụ tạo tải (như JMeter, Locust, K6) đặt trên các máy tạo tải (Load Generators). Đồng thời, đây là bước cực kỳ quan trọng để chuẩn bị dữ liệu kiểm thử (Test Data). Dữ liệu này cần đủ lớn và đa dạng (ví dụ: hàng vạn tài khoản khác nhau, danh mục sản phẩm phong phú) nhằm tránh các tác động tích cực giả tạo do cơ chế lưu bộ đệm (cache) của hệ thống tạo ra.

### Bước 5: Triển khai thiết kế kịch bản kiểm thử (Implement the Test Design)

Kiểm thử viên tiến hành viết mã hoặc cấu hình các kịch bản kiểm thử tự động (Test Scripts) trên công cụ đã chọn. Trong bước này, cần chèn các tham số hóa dữ liệu (Parameterization), xử lý các giá trị động được trả về từ máy chủ (Correlation như Token, Session ID) và thiết lập các điểm kiểm tra logic (Assertions) để xác định một request là thành công hay thất bại.

### Bước 6: Thực thi kiểm thử (Execute the Tests)

Chạy các kịch bản kiểm thử hiệu năng đã lập trình sẵn. Trong quá trình chạy, các kỹ sư không chỉ vận hành công cụ tạo tải mà còn phải kết hợp sử dụng các công cụ giám sát (Monitoring Tools như Prometheus, Grafana, New Relic, Datadog) để theo dõi liên tục trạng thái sức khỏe tài nguyên phần cứng, ghi nhận các hiện tượng bất thường và đảm bảo máy tạo tải không bị quá tải cục bộ.

### Bước 7: Phân tích kết quả, báo cáo và tinh chỉnh (Analyze, Tune and Retest)

Sau khi thu thập đầy đủ dữ liệu từ bài test, tiến hành hợp nhất các số liệu, đối chiếu trực tiếp với các tiêu chí chấp nhận đã đặt ra ở Bước 2 để rút ra kết luận hệ thống đạt hay không đạt. Tìm kiếm các nút thắt cổ chai, chuyển thông tin phân tích chi tiết cho đội ngũ lập trình để tối ưu hóa mã nguồn hoặc đội ngũ hệ thống cấu hình lại hạ tầng. Sau khi tinh chỉnh (Tuning), bài test hiệu năng bắt buộc phải được thực thi lại (Retest) để xác minh xem việc sửa đổi có thực sự cải thiện hiệu năng hay không.

---

## 4.6. Workload Model 

Nền tảng để thực hiện chính xác Bước 3 trong quy trình trên chính là việc xây dựng một Mô hình khối lượng công việc chuẩn xác. **Workload Model** là một tài liệu hoặc cấu hình kịch bản mô phỏng chi tiết hành vi, tần suất tương tác và phân bổ luồng đi của người dùng thực tế lên hệ thống phần mềm tại một thời điểm cụ thể.

### Các thành phần cấu tạo nên một Workload Model:

* **User Distribution (Phân bổ tính năng):** Xác định tỷ lệ phần trăm người dùng thực hiện các tính năng khác nhau. Trong thực tế, không bao giờ có chuyện 100% người dùng vào hệ thống đều thực hiện chức năng thanh toán. Một mô hình thực tế sẽ phân bổ ví dụ: 60% người dùng chỉ lướt xem tin tức, 30% thực hiện tìm kiếm, và chỉ có 10% thực hiện giao dịch mua bán.
* **Load Profile (Biểu đồ phân phối tải):** Xác định hình thái tăng giảm của lượng tải theo thời gian, bao gồm:
    * **User Load:** Số lượng người dùng ảo truy cập vào hệ thống.
    * **Ramp-up period:** Thời gian tải tăng dần, đưa VU vào hệ thống từ từ để tránh gây shock hệ thống đột ngột.
    * **Steady-state period:** Thời gian duy trì tải đỉnh ổn định để quan sát hệ thống ở trạng thái bão hòa.
    * **Ramp-down period:** Thời gian tắt dần các VU khi bài test kết thúc.

### Phương pháp thu thập dữ liệu xây dựng Workload Model:

1. **Dựa trên dữ liệu lịch sử (Historical Data):** Trích xuất thông tin từ các công cụ phân tích log hệ thống, Google Analytics, hoặc chỉ số APM trên Production để tính toán số lượng request/giây cao nhất ở quá khứ.
2. **Dựa trên dự báo kinh doanh (Business Forecasts):** Đối với các hệ thống mới hoàn toàn chưa có dữ liệu lịch sử, đội ngũ kiểm thử phải dựa trên dự kiến tăng trưởng của bộ phận kinh doanh (ví dụ: hệ thống dự kiến đạt 50,000 người dùng đăng ký trong tháng đầu tiên, tỷ lệ hoạt động giờ cao điểm là 5%).

---

## 4.7. Các nguyên tắc khi thiết kế Performance Test

Việc xây dựng quy trình và mô hình tải ở trên nếu không tuân thủ các nguyên tắc thiết kế thực tế dưới đây sẽ dễ dẫn đến tình trạng sai lệch số liệu, tạo ra các kết quả kiểm thử lạc quan giả tạo hoặc bi quan quá mức.

### 4.7.1. Sử dụng workload thực tế (Realistic Workload)

**Nguyên tắc:** Mô hình tải (Workload model) phải phản ánh chính xác hành vi sử dụng thực tế của tập khách hàng, bao gồm tỷ lệ phân bổ giữa các hành động nghiệp vụ, thời gian suy nghĩ (think time) hợp lý, và nhịp độ kiểm soát (pacing).

**Tại sao quan trọng:** Xây dựng một workload sai lệch sẽ dẫn đến kết quả test vô giá trị. Nếu trong thực tế hệ thống nhận 80% traffic là các truy vấn đọc dữ liệu (GET) nhưng kịch bản test lại cấu hình 80% traffic là thao tác ghi dữ liệu (POST), kết quả thu được sẽ phản ánh sai hoàn toàn khả năng chịu tải thực tiễn của cơ sở dữ liệu.

---

### 4.7.2. Sử dụng dữ liệu kiểm thử đại diện (Representative Test Data)

**Nguyên tắc:** Toàn bộ dữ liệu đầu vào sử dụng trong quá trình kiểm thử (tài khoản đăng nhập, từ khóa tìm kiếm, ID sản phẩm) phải đủ lớn, đa dạng và được thay đổi liên tục cho mỗi VU, không sử dụng lặp đi lặp lại một tập dữ liệu nhỏ hẹp.

**Tại sao quan trọng:** Nếu tất cả các VU chạy đồng thời đều truy vấn cùng một từ khóa hoặc xem chung một mã sản phẩm, hệ thống máy chủ sẽ trả ngay kết quả từ tầng bộ đệm (Cache Hit) mà không cần thực hiện các tính toán logic hay truy vấn xuống ổ đĩa vật lý của Database (Cache Miss). Điều này tạo ra một kết quả kiểm thử đẹp đẽ nhưng giả tạo.

---

### 4.7.3. Đảm bảo phiên người dùng độc lập (Independent User Sessions)

**Nguyên tắc:** Mỗi người dùng ảo (VU) khi tham gia vào bài test phải được cấp phát một phiên làm việc (Session) hoàn toàn riêng biệt, sở hữu Cookie, Token nhận dạng, và ngữ cảnh dữ liệu độc lập.

**Tại sao quan trọng:** Khi nhiều VU dùng chung một tài khoản hoặc chia sẻ chung trạng thái, các hành động nghiệp vụ sẽ triệt tiêu hoặc xung đột lẫn nhau (ví dụ: VU này vừa thêm hàng vào giỏ thì VU kia bấm xóa sạch giỏ hàng). Điều này gây ra một tỷ lệ lỗi logic giả, đồng thời làm mất đi khả năng kiểm thử cơ chế quản lý session (Session Management) ở phía server dưới tải lớn.

---

### 4.7.4. Khởi động hệ thống (Warm-up) trước khi đo lường

**Nguyên tắc:** Luôn thiết lập một khoảng thời gian chạy khởi động hệ thống (Warm-up phase) trước khi bắt đầu ghi nhận số liệu chính thức để phân tích. Toàn bộ dữ liệu nhiễu sinh ra trong giai đoạn khởi động này phải được loại bỏ khỏi báo cáo cuối cùng.

**Tại sao quan trọng:** Kiến trúc phần mềm hiện đại phụ thuộc nhiều vào các cơ chế tối ưu động theo thời gian như biên dịch JIT (Just-In-Time Compilation), khởi tạo các bể kết nối (Connection Pooling initialization), và nạp dữ liệu nền lên cache. Nếu tính cả thời gian hệ thống đang "khởi động máy" này vào báo cáo, chỉ số response time trong vài phút đầu sẽ bị đẩy lên rất cao, dẫn tới những kết luận thiếu chính xác.

---

### 4.7.5. Đảm bảo khả năng lặp lại (Repeatability)

**Nguyên tắc:** Một bài test hiệu năng khi được thực thi nhiều lần trên cùng một môi trường, cùng một cấu hình kịch bản và cùng một tập dữ liệu đầu vào phải cho ra các kết quả tương đồng nhau (nằm trong biên độ dao động sai số thống kê cho phép, thông thường dưới 5%).

**Tại sao quan trọng:** Nếu kết quả kiểm thử biến động quá mạnh giữa các lần chạy (lần đầu response time ra 200ms, lần sau vọt lên 3000ms), số liệu đó hoàn toàn không đáng tin cậy. Nguyên nhân thường do môi trường kiểm thử bị chia sẻ với các đội ngũ khác, dữ liệu kiểm thử bị thay đổi trạng thái sau lần chạy đầu mà không được reset, hoặc do các tiến trình chạy ngầm (background cronjobs) của hệ điều hành gây nhiễu. Mỗi bài kiểm thử tiêu chuẩn nên được chạy lặp lại ít nhất 3 lần để khẳng định tính nhất quán.

---

### 4.7.6. Tránh nghẽn cổ chai phía máy tạo tải (Avoid Client-Side Bottlenecks)

**Nguyên tắc:** Máy tạo tải (Load Generator) phải được đảm bảo cấu hình phần cứng đủ mạnh để vận hành số lượng VU mong muốn mà không tự rơi vào trạng thái quá tải tài nguyên (CPU/RAM của máy test không vượt quá 80%).

**Tại sao quan trọng:** Đây là sai lầm kinh điển của các kiểm thử viên mới: cố gắng ép một chiếc laptop cấu hình yếu tạo ra 5,000 VU đồng thời. Khi máy tạo tải bị hết tài nguyên hoặc cạn kiệt cổng mạng (port exhaustion), bản thân nó không thể gửi request đi đúng tiến độ quy định trong script. Kết quả là biểu đồ response time trả về tăng vọt, nhưng nguyên nhân không phải hệ thống SUT chậm mà do máy tạo tải đang bị nghẽn. Giải pháp cho trường hợp này là áp dụng kiến trúc tạo tải phân tán (Distributed Load Generation) trên nhiều máy.

---

### 4.7.7. Nhất quán cấu hình môi trường (Environment Consistency)

**Nguyên tắc:** Giữ nguyên trạng thái cấu hình của toàn bộ hệ thống bao gồm mã nguồn, tham số cấu hình web server, phiên bản hệ quản trị cơ sở dữ liệu, và kiến trúc đường truyền mạng trong suốt các lượt chạy kiểm thử so sánh. Nếu có bất kỳ sự thay đổi nào để tối ưu, phải ghi nhận thành một phiên bản kiểm thử mới độc lập.

**Tại sao quan trọng:** Việc so sánh kết quả kiểm thử hiệu năng giữa hai lần chạy có cấu hình phần cứng khác nhau hoặc các tham số cấu hình phần mềm khác nhau để kết luận xem đoạn code nào tối ưu hơn là hoàn toàn vô nghĩa. Mọi sự so sánh chỉ có giá trị khi được đặt trên cùng một hệ quy chiếu nền tảng vững chắc.

---

### 4.7.8. Đo lường đa chỉ số, không chỉ dựa vào giá trị trung bình (Measure Multiple Metrics, Not Just Averages)

**Nguyên tắc:** Tuyệt đối không bao giờ sử dụng một con số trung bình duy nhất (Average/Mean) để đại diện cho hiệu năng của toàn bộ hệ thống. Bắt buộc phải thu thập và báo cáo đầy đủ dải phân vị thống kê (p50, p90, p95, p99) cùng với giá trị lớn nhất (Max) và nhỏ nhất (Min).

**Tại sao quan trọng:** Giá trị trung bình toán học có xu hướng làm mịn và che giấu đi các điểm dị biệt nghiêm trọng. Hãy xem xét ví dụ cụ thể sau:

| Chỉ số đo lường | Kịch bản A | Kịch bản B |
| --- | --- | --- |
| Số lượng Request thực hiện | 100 requests | 100 requests |
| Phân bố thời gian phản hồi thực tế | Tất cả 100 request đều phản hồi ổn định ở mức **100 ms**. | 99 request phản hồi cực nhanh ở mức **50 ms**; duy nhất 1 request bị treo mất **5,050 ms**. |
| **Giá trị Trung bình (Average)** | **100 ms** | **100 ms** |
| **Giá trị Phân vị thứ 99 (p99)** | **100 ms** | **5,050 ms** |

Nhìn vào bảng so sánh, nếu chỉ báo cáo con số trung bình, cả hai kịch bản đều cho ra kết quả lý tưởng là **100 ms**. Tuy nhiên, trải nghiệm thực tế ở Kịch bản B rất tệ khi có 1% khách hàng phải chờ đợi hơn 5 giây. Chỉ có việc đo lường đa chỉ số (đặc biệt là p95 và p99) mới có thể bộc lộ chính xác các nút thắt cổ chai cục bộ này của hệ thống.
# 5. Hệ thống EShop và phạm vi kiểm thử

## 5.1. Mô tả SUT

| Thành phần | Giá trị đã xác minh |
|---|---|
| Repository | `https://github.com/trngnneee/eshop-sut` |
| Branch | `seminar` |
| Commit | `609b6e6821cd3241363d0087d859576674d47e1b` |
| Customer frontend | React `^19.2.6`, React Router `^7.15.0`, Vite `^8.0.12` |
| Admin frontend | React `^19.2.6`, Vite `^8.0.12`, port `5174` |
| Mobile frontend | Expo `~54.0.33`, React Native `0.81.5` |
| Backend | Node.js CommonJS, yêu cầu Node `20.x`, Express `^5.2.1`, JWT Bearer |
| Database | **SQLite**, `backend/database.sqlite`, snapshot hiện tại `36 KiB` |
| API Base URL | `http://localhost:3000` |
| Web URL | `http://localhost:5173` |
| Admin URL | `http://localhost:5174` |
| Environment | Local source workspace; chưa có staging evidence |
| Service status | Port `3000`, `5173`, `5174` đều chưa lắng nghe khi kiểm tra |

## 5.2. Business flows

1. Product Listing.
2. Product Search.
3. Product Detail.
4. Login.
5. Add to Cart.
6. Checkout.

Endpoint và request body phải được lấy từ network log, API documentation hoặc source code thật. Báo cáo không tự tạo endpoint.

## 5.3. In Scope

- Response time và percentiles của API được chọn.
- Throughput.
- Error rate.
- Concurrent workload.
- Hành vi dưới baseline, load, spike và stress.
- Session/authentication nếu flow yêu cầu.
- So sánh JMeter và k6 trên workload tương đương.

## 5.4. Out of Scope

- Kết luận về năng lực production nếu chỉ chạy local.
- Third-party payment hoặc email service nếu không được kiểm soát.
- Mobile network performance.
- Distributed load generation nếu nhóm không triển khai.
- Capacity planning chính thức nếu không có production topology và traffic data.

## 5.5. Test Environment

| Thuộc tính | Giá trị thực tế |
|---|---|
| OS | Windows 11 Home 64-bit, build `26200` |
| CPU | Intel Core i7-1260P, 12 cores/16 logical processors |
| RAM | `15.72 GiB` |
| Máy phát tải | Cùng máy với SUT |
| Node hiện cài | `v24.10.0` |
| Node backend yêu cầu | `20.x` |
| npm | `11.6.1` |
| Java | Eclipse Temurin OpenJDK `25.0.2+10-LTS`, 64-bit |
| JMeter | `NOT_FOUND` trên `PATH` khi kiểm tra ngày 2026-07-15; cần cài và lưu `jmeter --version` trước thực nghiệm |
| k6 | `NOT_FOUND` trên `PATH` khi kiểm tra ngày 2026-07-15; cần cài và lưu `k6 version` trước thực nghiệm |
| Docker | Client `29.2.1`; Docker Desktop Linux daemon không chạy |
| Database size | `36 KiB` tại snapshot hiện tại |

---

# 6. Phương pháp khảo sát công cụ

## 6.1. Danh sách khảo sát

Nhóm khảo sát 15 công cụ đã được phân công trong tài liệu nhóm:

1. Apache JMeter
2. Silk Performer
3. Artillery
4. k6
5. Locust
6. Gatling
7. Loader.io
8. Siege
9. Vegeta
10. wrk
11. NeoLoad
12. ApacheBench
13. OpenText LoadRunner Professional
14. Tsung
15. Taurus

## 6.2. Tiêu chí bắt buộc từ Seminar Guide

Stage S1 yêu cầu đánh giá tối thiểu:

- Cost/licence.
- Learning curve.
- EShop fit.
- AI capability.
- Community.

## 6.3. Tiêu chí mở rộng của nhóm

| Tiêu chí | Câu hỏi đánh giá |
|---|---|
| Cost & access | Cả nhóm và audience có thể cài/chạy không? Có phụ thuộc trial không? |
| Learning curve | Có thể học và demo trong thời gian seminar không? |
| EShop fit | Có hỗ trợ API, session, token và data parameterization không? |
| Multi-step journey | Có mô hình hóa flow nhiều bước rõ ràng không? |
| Workload control | Có VU/arrival-rate/ramp-up/scenario phù hợp không? |
| Assertions/checks | Có phát hiện protocol và business failure không? |
| Reporting | Có percentiles, throughput, errors và raw result không? |
| CI/CD | Có CLI và automated pass/fail không? |
| Reproducibility | Script/config có thể lưu Git và chạy lại không? |
| Local/offline | Có chạy được khi EShop local hoặc lớp mất mạng không? |
| AI-assisted potential | AI output có thể được tạo, audit và minh họa rõ không? |
| Classroom suitability | Audience có thể hoàn thành activity trong 25 phút không? |

## 6.4. Quy trình đánh giá

### Vòng 1 – Desk Research

- Đọc tài liệu chính thức.
- Xác định cách cài đặt, scripting model, reporting và licence/access.
- Không sử dụng blog làm nguồn duy nhất cho claim quan trọng.

### Vòng 2 – Smoke Test

Mỗi công cụ cần tối thiểu:

- Cài đặt hoặc xác minh dịch vụ.
- Chạy official “hello world” hoặc request đơn giản.
- Ghi setup time.
- Lưu command, screenshot và lỗi.

### Vòng 3 – EShop Fit Test

Với ứng viên mạnh:

- Gọi endpoint EShop thật.
- Thực hiện một flow có data/session nếu có.
- Xác minh metrics và errors.

### Vòng 4 – Shortlist và Pair Selection

Chọn hai công cụ không chỉ có điểm cao mà còn:

- Bổ sung cho nhau.
- Phù hợp learning objectives T05.
- Cho phép so sánh công bằng.
- Có AI angle rõ ràng.

## 6.5. Quy tắc chấm điểm

Nếu nhóm sử dụng điểm số 1–5, mỗi điểm phải có evidence. Không được ghi 5/5 chỉ vì công cụ “nổi tiếng”. Báo cáo này sử dụng phân loại định tính ở vòng đầu và yêu cầu nhóm bổ sung bảng điểm thực nghiệm trong Appendix.

---

# 7. Khảo sát 15 công cụ Performance Testing

Dựa trên cơ sở lý thuyết về các loại kiểm thử, các chỉ số đo lường hiệu năng và nguyên tắc thiết kế kịch bản tải đã nêu, dưới đây là phần khảo sát chi tiết 15 công cụ Performance Testing phổ biến. Mỗi công cụ sẽ được phân tích sâu về vai trò kỹ thuật, điểm phù hợp, hạn chế và kết luận sơ bộ phục vụ cho bài toán EShop.

## 7.1. Apache JMeter

Apache JMeter là công cụ của Apache dùng để xây dựng và chạy Test Plan. Tài liệu chính thức khuyến nghị dùng GUI để xây dựng/debug Test Plan và dùng CLI mode để chạy load test. CLI có thể ghi raw results và tạo HTML report. JMeter hỗ trợ nhiều loại sampler và cấu hình như HTTP Request, Header Manager, Cookie Manager, Timer, Assertion và CSV Data Set Config.

**Vai trò kỹ thuật trong hệ thống lý thuyết:**

* **Loại kiểm thử đáp ứng:** Load Testing, Stress Testing, Spike Testing, Endurance Testing và Volume Testing.
* **Áp dụng lý thuyết:** Cung cấp giao diện trực quan trực tiếp để thiết kế **Workload Model** thông qua *Thread Group* (cấu hình Ramp-up, Duration). Hỗ trợ đắc lực nguyên tắc **Sử dụng dữ liệu đại diện** nhờ *CSV Data Set Config* và **Đảm bảo phiên độc lập** nhờ *Cookie/Header Manager*. Cơ chế sinh HTML Report tự động cung cấp đầy đủ các góc nhìn dữ liệu từ **Response Time, Throughput, Error Rate** cho đến biểu đồ **Percentile (p50, p90, p95, p99)** chi tiết, giúp kiểm thử viên dễ dàng đối chiếu với tiêu chí SLA trong *Quy trình kiểm thử*.

**Điểm phù hợp với EShop**

* Mô hình hóa flow nhiều bước.
* Xử lý header, cookie, token và data parameterization.
* GUI dễ minh họa cho audience.
* CLI phù hợp với lần chạy chính thức.
* HTML report hỗ trợ phân tích sau test.

**Hạn chế**

* File `.jmx` dạng XML khó review hơn script thuần code.
* GUI và listener nặng có thể ảnh hưởng load generator.
* Test Plan lớn có thể khó bảo trì nếu không tổ chức tốt.

**Kết luận sơ bộ:** Ứng viên mạnh cho công cụ chính và đại diện hướng visual/Test Plan.

---

## 7.2. Silk Performer

Silk Performer là giải pháp Performance Testing hướng doanh nghiệp. Công cụ cung cấp hệ sinh thái thiết kế workload và phân tích cho nhiều môi trường, nhưng khả năng tiếp cận của nhóm phụ thuộc licence, trial và điều kiện cài đặt.

**Vai trò kỹ thuật trong hệ thống lý thuyết:**

* **Loại kiểm thử đáp ứng:** Load Testing, Stress Testing, Endurance Testing và Scalability Testing.
* **Áp dụng lý thuyết:** Đóng vai trò là một nền tảng quản lý hiệu năng ở quy mô Enterprise. Công cụ hỗ trợ thiết kế **Workload Model** phức tạp và tích hợp khả năng giám sát các chỉ số **Resource Utilization (CPU, RAM, Disk I/O)** trong những môi trường được cấu hình phù hợp. Quy mô VU thực tế, protocol entitlement và overhead của load generator vẫn phải được xác minh bằng version/licence và thực nghiệm cụ thể.

**Điểm phù hợp**

* Hướng đến workload và reporting doanh nghiệp.
* Có giá trị khảo sát để so sánh với công cụ miễn phí.

**Hạn chế trong seminar**

* Access/licence có thể làm giảm reproducibility.
* Audience khó bảo đảm có cùng môi trường.
* Phạm vi tính năng lớn hơn nhu cầu demo EShop ngắn.

**Kết luận sơ bộ:** Có năng lực mạnh nhưng không tối ưu cho activity cần mọi nhóm tái tạo dễ dàng.

---

## 7.3. Artillery

Artillery là công cụ Performance Testing theo hướng cấu hình/script, thường sử dụng YAML hoặc JavaScript để định nghĩa phases, scenarios và flow. Công cụ phù hợp với API và hệ sinh thái developer, có thể chạy từ CLI và tích hợp automation.

**Vai trò kỹ thuật trong hệ thống lý thuyết:**

* **Loại kiểm thử đáp ứng:** Load Testing, Stress Testing và Spike Testing (phù hợp nhất cho HTTP API/endpoints).
* **Áp dụng lý thuyết:** Công cụ này hiện thực hóa cấu trúc **Workload Model** thông qua file cấu hình YAML tường minh (định nghĩa các `phases` gồm `arrivalRate` và `duration`). Phục vụ tốt các chỉ số cốt lõi như **Response Time, Throughput, Error Rate** hiển thị trực tiếp trên CLI. Do cấu hình dạng khai báo văn bản, nó hỗ trợ tốt nguyên tắc **Nhất quán cấu hình môi trường** khi quản lý mã nguồn kiểm thử qua Git.

**Điểm phù hợp**

* Cấu hình tương đối dễ đọc.
* Tốt cho API và flow web.
* Thân thiện với CI/CD.
* AI có thể tạo bản nháp YAML/JavaScript.

**Hạn chế trong quyết định cặp công cụ**

* Vai trò gần với k6: đều là code/config-first, CLI và automation-friendly.
* Chọn Artillery cùng k6 tạo ít sự tương phản hơn JMeter–k6.

**Kết luận sơ bộ:** Ứng viên tốt và là backup phù hợp cho k6.

---

## 7.4. k6

k6 là công cụ Performance Testing theo hướng test-as-code. Test được viết bằng JavaScript và có thể định nghĩa scenarios, executors, checks, custom metrics và thresholds. Thresholds cho phép thể hiện tiêu chí pass/fail ở cấp tự động.

**Vai trò kỹ thuật trong hệ thống lý thuyết:**

* **Loại kiểm thử đáp ứng:** Load Testing, Stress Testing, Spike Testing, Endurance Testing và Scalability Testing.
* **Áp dụng lý thuyết:** Thể hiện tư duy *Test-as-Code* trong *Quy trình kiểm thử*. k6 hiện thực hóa **Workload Model** thông qua các *Executors* như `ramping-arrival-rate` và `constant-vus`. Tính năng *Thresholds* cho phép định nghĩa acceptance criteria ngay trong code, ví dụ `http_req_duration: ['p(95)<200']`. Đây chỉ là ví dụ cú pháp; ngưỡng `200 ms` không phải SLO đã được phê duyệt cho EShop. Script vẫn phải quản lý dữ liệu và state theo VU để **đảm bảo phiên người dùng độc lập**.

**Điểm phù hợp với EShop**

* Script lưu Git và review được.
* JavaScript quen thuộc với nhóm phát triển web.
* Scenarios và executors giúp mô hình hóa workload.
* Checks phát hiện lỗi và thresholds tự động đánh giá.
* Phù hợp CI/CD.
* Rất phù hợp để minh họa AI-generated draft và human audit.

**Hạn chế**

* Yêu cầu kỹ năng lập trình.
* Không có GUI thiết kế cây như JMeter.
* Script chạy thành công không chứng minh workload đúng business behavior.

**Kết luận sơ bộ:** Ứng viên mạnh cho công cụ chính và đại diện test-as-code.

---

## 7.5. Locust

Locust cho phép mô tả user behavior bằng Python. Tài liệu chính thức nhấn mạnh khả năng viết scenario bằng code, theo dõi bằng web UI hoặc chạy headless, và có thể scale theo mô hình distributed.

**Vai trò kỹ thuật trong hệ thống lý thuyết:**

* **Loại kiểm thử đáp ứng:** Load Testing, Stress Testing, Endurance Testing và Scalability Testing.
* **Áp dụng lý thuyết:** Hỗ trợ xây dựng **Workload Model** dựa trên tư duy hướng đối tượng, nơi hành vi của người dùng được viết thành các hàm Python (`@task`), giúp mô phỏng chính xác nguyên tắc **Sử dụng workload thực tế** và **Think Time** phân phối ngẫu nhiên. Công cụ cung cấp giao diện Web UI thời gian thực để theo dõi biểu đồ tăng trưởng của **Throughput (RPS)**, **Error Rate**, và các dải **Percentile**, phục vụ tốt cho bước *Thực thi kiểm thử* và *Phân tích kết quả*.

**Điểm phù hợp**

* Python dễ đọc với người biết ngôn ngữ này.
* Mô tả user behavior tự nhiên.
* Có web UI và distributed mode.
* Phù hợp user journey EShop.

**Lý do không chọn trong cặp cuối**

* Cùng nhóm code-first với k6.
* k6 phù hợp hơn với mục tiêu dùng JavaScript và AI-generated script của T05.
* Không phải vì Locust yếu, mà vì mức bổ sung cho JMeter thấp hơn k6 trong phạm vi này.

**Kết luận sơ bộ:** Shortlist; backup mạnh.

---

## 7.6. Gatling

Gatling theo hướng test-as-code và cung cấp concepts về simulation, scenario, protocol, injection profile và assertions. Công cụ phù hợp với mô hình workload phức tạp và automation.

**Vai trò kỹ thuật trong hệ thống lý thuyết:**

* **Loại kiểm thử đáp ứng:** Load Testing, Stress Testing, Spike Testing và Endurance Testing.
* **Áp dụng lý thuyết:** Mô hình thực thi bất đồng bộ và DSL của Gatling hỗ trợ định nghĩa *Injection Profile* cho **Workload Model** và đặt *Assertions* trên các chỉ số như **Response Time** và **Error Rate**. Thiết kế này có thể giảm overhead so với mô hình một thread hệ điều hành cho mỗi user, nhưng số user mà một load generator thực sự duy trì được vẫn phải đo cùng CPU/RAM/network telemetry; không được suy ra capacity chỉ từ kiến trúc.

**Điểm phù hợp**

* DSL có cấu trúc.
* Hỗ trợ scenario và injection profile.
* Reporting và automation tốt.
* Phù hợp performance engineering dài hạn.

**Lý do không chọn trong cặp cuối**

* Learning curve và môi trường runtime có thể nặng hơn cho audience trong seminar ngắn.
* Vai trò code-first trùng với k6.
* k6 trực tiếp phù hợp learning objectives T05 và AI scripting workflow của nhóm.

**Kết luận sơ bộ:** Shortlist; phù hợp nhóm quen hệ sinh thái của Gatling.

---

## 7.7. Loader.io

Loader.io là dịch vụ cloud load testing cho web application/API endpoints. Điểm mạnh là giảm công việc thiết lập load generator local.

**Vai trò kỹ thuật trong hệ thống lý thuyết:**

* **Loại kiểm thử đáp ứng:** Load Testing và Stress Testing trên môi trường Public Internet.
* **Áp dụng lý thuyết:** Đóng vai trò giải phóng hoàn toàn gánh nặng của nguyên tắc **Tránh bottleneck phía client** bằng cách chuyển hạ tầng phát tải lên đám mây (Cloud-based Load Generation). Công cụ này tập trung đo lường các chỉ số hiệu năng cơ bản phía người dùng như **Response Time, Throughput** và **Error Rate** dưới dạng biểu đồ trực quan, giúp đẩy nhanh Bước 6 (*Thực thi*) và Bước 7 (*Phân tích*) trong *Quy trình kiểm thử*.

**Điểm phù hợp**

* Bắt đầu nhanh với endpoint có thể truy cập từ Internet.
* Hữu ích để kiểm tra nhanh dịch vụ public.

**Hạn chế với EShop seminar**

* EShop local có thể không truy cập được từ cloud.
* Phụ thuộc Internet và dịch vụ bên ngoài.
* Activity phải có phương án chạy khi mất mạng sau setup.
* Kiểm soát môi trường load generator ít trực tiếp hơn local tools.

**Kết luận sơ bộ:** Không chọn làm tool chính cho EShop local; có thể là công cụ khảo sát cloud-based.

---

## 7.8. Siege

Siege là công cụ HTTP load testing/benchmarking qua command line. Nó có thể tạo concurrent HTTP traffic và chạy danh sách URL.

**Vai trò kỹ thuật trong hệ thống lý thuyết:**

* **Loại kiểm thử đáp ứng:** Bản chất là một công cụ Benchmarking nhanh, đáp ứng cơ bản cho Load Testing ở mức thô.
* **Áp dụng lý thuyết:** Đóng vai trò thu thập nhanh chỉ số baseline trong *Quy trình kiểm thử* ở giai đoạn đầu. Nó đo lường thô các chỉ số **Throughput (trans/sec)**, **Response Time**, **Error Rate (tổng số lỗi HTTP)** và mức độ xử lý **Concurrent Users** tối đa mà không đi sâu vào việc xây dựng cấu trúc **Workload Model** đa bước phức tạp hay tính toán sâu các dải phân vị **Percentile**.

**Điểm phù hợp**

* Nhẹ và dễ chạy cho benchmark HTTP.
* Hữu ích cho smoke benchmark hoặc endpoint-level test.

**Hạn chế**

* Không tối ưu để giảng dạy và duy trì user journey phức tạp có session, correlation và business assertions.
* Reporting và cấu trúc scenario không sâu bằng full performance testing tools.

**Kết luận sơ bộ:** Công cụ benchmark phụ; không chọn làm công cụ seminar chính.

---

## 7.9. Vegeta

Vegeta là HTTP load testing tool và Go library, được thiết kế mạnh cho workload theo constant request rate. Nó có CLI và reporting.

**Vai trò kỹ thuật trong hệ thống lý thuyết:**

* **Loại kiểm thử đáp ứng:** Load Testing và Stress Testing (chuyên biệt cho mô hình kiểm thử hướng tốc độ yêu cầu cố định).
* **Áp dụng lý thuyết:** Phù hợp với **Workload Model** dạng *Constant Request Rate*, trong đó target request rate được cấu hình độc lập với response time trong giới hạn capacity của generator. Raw result và report có thể hỗ trợ quan sát **Throughput**, **Latency/Response Time** và phân vị. Điểm bão hòa chỉ được kết luận khi request rate thực đạt target, generator còn headroom và SUT telemetry được đồng bộ.

**Điểm phù hợp**

* Kiểm soát request rate rõ.
* Binary/CLI thuận tiện.
* Hữu ích để benchmark HTTP service.

**Hạn chế**

* Không phải lựa chọn trực tiếp nhất cho user journey mua sắm nhiều bước và stateful.
* Cần thêm thiết kế nếu muốn mô phỏng nhiều flow có dependency.

**Kết luận sơ bộ:** Tốt cho rate-based HTTP testing; không được chọn vì mục tiêu của nhóm ưu tiên business journey và so sánh GUI–code.

---

## 7.10. wrk

wrk là HTTP benchmarking tool có khả năng tạo tải lớn trên một máy đa lõi. Công cụ sử dụng mô hình multi-threaded và hỗ trợ LuaJIT scripting cho request generation/response processing.

**Vai trò kỹ thuật trong hệ thống lý thuyết:**

* **Loại kiểm thử đáp ứng:** High-velocity Load Testing và Benchmarking cho các Single Endpoints.
* **Áp dụng lý thuyết:** Thiết kế multi-threaded giúp wrk tận dụng CPU đa lõi và phù hợp để nghiên cứu nguyên tắc **tránh bottleneck phía client** khi benchmark một endpoint. Công cụ báo request rate, latency statistics và errors ở mức HTTP/socket. Tuy nhiên, throughput tối đa quan sát được có thể bị giới hạn bởi chính generator, network hoặc script Lua, nên phải kèm telemetry và không được tự đồng nhất với capacity của SUT.

**Điểm phù hợp**

* Nhẹ và tạo raw HTTP load hiệu quả.
* Hữu ích khi benchmark một endpoint hoặc server HTTP.

**Hạn chế**

* Scripting và response processing có thể làm giảm mức tải phát được.
* Không trực quan cho audience và không tối ưu cho full business transaction reporting.
* Cần cẩn thận để load generator không trở thành bottleneck.

**Kết luận sơ bộ:** Tốt cho HTTP benchmark; không phải công cụ chính cho scenario EShop nhiều bước.

---

## 7.11. NeoLoad

NeoLoad là giải pháp Performance Testing thương mại hướng doanh nghiệp, tập trung vào thiết kế, chạy và phân tích load tests.

**Vai trò kỹ thuật trong hệ thống lý thuyết:**

* **Loại kiểm thử đáp ứng:** Toàn diện từ Load, Stress, Spike cho đến Endurance và Scalability Testing.
* **Áp dụng lý thuyết:** NeoLoad hỗ trợ nhiều hoạt động trong *Quy trình kiểm thử Performance*, từ thiết kế workload đến execution, result analysis và monitoring integration. Công cụ có thể liên kết chỉ số phía người dùng như **Response Time, Throughput, Percentile** với **Resource Utilization** khi monitor/agent và licence tương ứng được cấu hình. Mức độ quan sát thực tế phải được xác minh trên environment cụ thể.

**Điểm phù hợp**

* Hỗ trợ workflow enterprise và reporting.
* Có giá trị so sánh với open-source tooling.

**Hạn chế trong seminar**

* Licence/access và môi trường dùng thử có thể ảnh hưởng reproducibility.
* Audience khó bảo đảm cùng quyền truy cập.
* Không phù hợp bằng công cụ local miễn phí cho hands-on 25 phút.

**Kết luận sơ bộ:** Công cụ enterprise mạnh; không chọn vì constraints của seminar, không phải vì thiếu tính năng.

---

## 7.12. ApacheBench

ApacheBench (`ab`) là công cụ command-line để benchmark HTTP server. Nó phù hợp với việc gửi nhiều request đến một URL và đo các thống kê cơ bản.

**Vai trò kỹ thuật trong hệ thống lý thuyết:**

* **Loại kiểm thử đáp ứng:** Baseline Load Testing và Smoke Testing (kiểm thử nhanh).
* **Áp dụng lý thuyết:** Phục vụ cho bước đầu tiên trong khâu *Thực thi kiểm thử* nhằm đo lường nhanh năng lực thô của máy chủ web trước khi tiến hành tối ưu. Công cụ này tính toán trực tiếp chỉ số **Throughput (Requests per second)** và **Response Time (ms)** ở các mức phân vị cơ bản một cách nhanh chóng, giúp thiết lập một thước đo ban đầu (Baseline) để làm hệ quy chiếu cho nguyên tắc **Nhất quán môi trường** về sau.

**Điểm phù hợp**

* Cài đặt và lệnh chạy đơn giản.
* Hữu ích để tạo baseline nhanh cho một endpoint.

**Hạn chế**

* Mô hình chủ yếu hướng single endpoint benchmark.
* Không phù hợp nhất để mô tả user journey nhiều bước, session và transaction mix EShop.

**Kết luận sơ bộ:** Dùng làm benchmark phụ hoặc sanity check; không chọn làm công cụ chính.

---

## 7.13. OpenText LoadRunner Professional

OpenText LoadRunner Professional là nền tảng Performance Testing thương mại hướng doanh nghiệp. Workflow thường gồm tạo Vuser script, thiết kế scenario trong Controller, phân phối tải qua load generators, theo dõi hệ thống và phân tích kết quả bằng Analysis. Giá trị khảo sát của công cụ nằm ở khả năng hỗ trợ nhiều loại giao thức và quy trình performance engineering quy mô lớn.

**Vai trò kỹ thuật trong hệ thống lý thuyết:**

* **Loại kiểm thử đáp ứng:** Có thể hỗ trợ Load, Stress, Spike, Endurance, Volume và Scalability Testing tùy protocol, licence, scenario và load-generator topology được triển khai.
* **Áp dụng lý thuyết:** Công cụ này chia nhỏ quy trình thành các module chuyên biệt tương ứng chặt chẽ với các bước lý thuyết: *Virtual User Generator (VuGen)* phục vụ thiết kế **Workload Model** chi tiết (xử lý nghiêm ngặt nguyên tắc **Dữ liệu đại diện, Phiên người dùng độc lập** và cấu hình **Think Time**); *Controller* điều phối khâu *Thực thi kiểm thử* chuyên nghiệp; và *Analysis* hiện thực hóa nguyên tắc **Đo lường đa chỉ số**, tổng hợp sâu các thông số từ **Response Time, Throughput, Error Rate** đến **Resource Utilization** để xác định chính xác vị trí *Nút thắt cổ chai*.

**Điểm phù hợp**

* Mô hình hóa business flow và transaction ở cấp enterprise.
* Có Controller, load generators, monitoring và analysis trong một hệ sinh thái.
* Hữu ích khi hệ thống cần protocol support hoặc governance rộng hơn HTTP API testing cơ bản.

**Hạn chế trong seminar**

* Là sản phẩm proprietary/commercial; licence, trial và quyền truy cập phải được xác minh tại thời điểm thực hiện.
* Installation và onboarding nặng hơn nhu cầu demo EShop ngắn.
* Audience khó bảo đảm có cùng licence và môi trường để tái tạo activity.
* Nếu nhóm chỉ đọc tài liệu mà chưa có quyền chạy đầy đủ, không được chấm điểm thực nghiệm ngang với công cụ đã smoke-test.

**Kết luận sơ bộ:** Đại diện tốt cho enterprise performance platform, nhưng không tối ưu cho tiêu chí access, reproducibility và hands-on trong lớp.

---

## 7.14. Tsung

Tsung là công cụ distributed load testing mã nguồn mở, được phát triển bằng Erlang. Tài liệu chính thức mô tả Tsung có thể stress nhiều giao thức, phân phối simulated users trên cluster và định nghĩa session bằng cấu hình XML. Công cụ có giá trị khi mục tiêu là tạo tải lớn hoặc nghiên cứu distributed load generation.

**Vai trò kỹ thuật trong hệ thống lý thuyết:**

* **Loại kiểm thử đáp ứng:** High-scale Load Testing, Stress Testing và Scalability Testing.
* **Áp dụng lý thuyết:** Hỗ trợ đắc lực cho nguyên tắc **Tránh bottleneck phía client** thông qua cơ chế phân tán tải (Distributed Load Generation) chạy trên cụm Cluster nhờ sức mạnh xử lý đồng thời (Concurrency) của ngôn ngữ Erlang. Về mặt kịch bản, cấu hình XML của Tsung cho phép hiện thực hóa cấu trúc **Workload Model** với các thuật toán phân phối mô phỏng sự xuất hiện của người dùng thực tế (*User Arrival Rate*), hỗ trợ đo đạc đầy đủ các chỉ số **Response Time, Latency** và **Throughput**.

**Điểm phù hợp**

* Có distributed architecture và hỗ trợ nhiều protocol.
* Có thể mô hình hóa dynamic session, think time và user-arrival behavior.
* Phù hợp để thảo luận sự khác nhau giữa single-generator và clustered load testing.

**Hạn chế trong seminar**

* XML configuration và hệ sinh thái Erlang có learning curve cao hơn JavaScript/YAML với audience hiện tại.
* Distributed capability có thể vượt quá phạm vi EShop chạy local.
* Setup cluster làm tăng rủi ro demo và thời gian chuẩn bị.
* Không tạo sự đối lập giảng dạy rõ bằng cặp JMeter GUI và k6 test-as-code.

**Kết luận sơ bộ:** Mạnh cho distributed, high-load và multi-protocol testing; không chọn làm tool chính vì scope, onboarding và classroom feasibility.

---

## 7.15. Taurus

Taurus là một automation-friendly testing framework sử dụng YAML để mô tả execution, reporting và pass/fail criteria, sau đó điều phối các executor được hỗ trợ. Taurus cần được đánh giá đúng vai trò: nó là lớp orchestration/abstraction, không phải lúc nào cũng là load generator độc lập. Vì vậy, khi Taurus chạy JMeter hoặc executor khác, năng lực phát tải cốt lõi vẫn phụ thuộc underlying engine.

**Vai trò kỹ thuật trong hệ thống lý thuyết:**

* **Loại kiểm thử đáp ứng:** Điều phối (Orchestration) tất cả các loại kiểm thử hiệu năng phụ thuộc vào Engine chạy bên dưới (như Load, Stress, Spike thông qua JMeter/Gatling).
* **Áp dụng lý thuyết:** Đóng vai trò chuẩn hóa và tự động hóa khâu *Lập kế hoạch, thiết kế kịch bản* (Bước 3) và khâu *Thực thi kiểm thử* (Bước 6) trong *Quy trình kiểm thử Performance*. Bằng cách chuyển đổi các Test Plan phức tạp thành cấu hình YAML đơn giản, Taurus giúp duy trì nguyên tắc **Nhất quán cấu hình môi trường** khi chạy tích hợp CI/CD. Nó chịu trách nhiệm định nghĩa các tiêu chí chấp nhận SLA thông qua module *Pass/Fail Criteria*, tự động giám sát chỉ số **Error Rate** hay **Response Time Percentile** để đưa ra quyết định dừng bài test khi hệ thống đạt ngưỡng sụp đổ.

**Điểm phù hợp**

* YAML giúp chuẩn hóa cấu hình và giảm độ phức tạp của command line.
* Có giá trị cho CI/CD, reusable configuration và orchestration.
* Có thể giúp nhóm quản lý execution/reporting thống nhất trên các engine được tài liệu chính thức hỗ trợ.

**Hạn chế trong seminar**

* Không nên tính Taurus như một load engine hoàn toàn độc lập khi so sánh raw performance.
* Kết quả và metric phụ thuộc executor bên dưới.
* Thêm một abstraction layer có thể làm audience khó phân biệt lỗi của Taurus, executor và SUT.
* Phải xác minh executor support theo phiên bản tài liệu hiện tại; không được tự khẳng định Taurus hỗ trợ k6 nếu chưa có official evidence.

**Kết luận sơ bộ:** Hữu ích cho orchestration và pipeline automation, nhưng không được chọn làm một trong hai load-testing engines chính.

---

# 8. Sàng lọc và lập danh sách rút gọn

## 8.1. Nguyên tắc sàng lọc

Việc sàng lọc không nhằm kết luận công cụ nào “tốt nhất tuyệt đối”. Mỗi công cụ được đặt đúng vai trò, sau đó đánh giá theo bối cảnh EShop và seminar T05 dựa trên các câu hỏi sau:

- Có thể cài đặt hoặc truy cập hợp pháp, lặp lại được trong môi trường lớp học hay không?
- Có mô hình hóa được EShop journey nhiều bước, session/token, think time và test data hay không?
- Có assertion/check để phân biệt HTTP success với business success hay không?
- Có cung cấp raw result, percentiles, throughput và error information để phân tích hay không?
- Có CLI/automation và lưu cấu hình trong Git hay không?
- Có tạo ra learning value khác biệt khi ghép với một công cụ thứ hai hay không?

Một công cụ bị loại khỏi cặp demo chính không có nghĩa công cụ đó yếu. Loader.io, enterprise platforms, distributed tools, endpoint benchmarks và orchestration frameworks giải quyết các bài toán khác với full EShop journey chạy local.

## 8.2. Kết quả phân nhóm sau Desk Research

| Nhóm | Công cụ | Trạng thái trong seminar | Lý do chính |
|---|---|---|---|
| Main candidates | Apache JMeter, k6 | Chọn vào cặp triển khai chính, có điều kiện | Cùng đáp ứng EShop journey nhưng đại diện hai workflow khác nhau: visual Test Plan và test-as-code. |
| Shortlist/counterfactual | Artillery, Locust, Gatling | Giữ làm ứng viên đối chứng hoặc backup | Có khả năng scenario/workload tốt, nhưng vai trò code-first trùng nhiều hơn với k6. |
| Enterprise references | Silk Performer, NeoLoad, LoadRunner Professional | Survey/deep-dive nếu có licence và lab phù hợp | Năng lực rộng nhưng access, onboarding và reproducibility trong lớp chưa được chứng minh. |
| Cloud service | Loader.io | Supporting/survey-only cho SUT hiện tại | EShop local không trực tiếp phù hợp với cloud generator và host verification. |
| Endpoint benchmarks | Siege, Vegeta, wrk, ApacheBench | Dùng cho sanity check hoặc single-endpoint benchmark | Không thay thế stateful business journey nếu chưa có harness, correlation và business checks. |
| Distributed testing | Tsung | Survey-only trong phạm vi hiện tại | Distributed generation chỉ cần thiết khi single generator được chứng minh là bottleneck. |
| Orchestration | Taurus | Supporting framework | Phải ghi rõ executor; không tính Taurus như một load engine độc lập khi nó gọi JMeter/Gatling. |

## 8.3. Shortlist và quyết định chuyển vòng

| Công cụ | EShop journey | Local/reproducible | Assertion/gate | Learning value | Quyết định |
|---|---|---|---|---|---|
| Apache JMeter | Phù hợp | Phù hợp | Phù hợp; CI gate cần thiết kế rõ | Visual/Test Plan | **Main candidate** |
| k6 | Phù hợp | Phù hợp | Checks + thresholds | Test-as-code/AI audit | **Main candidate** |
| Artillery | Phù hợp | Phù hợp | Expect/ensure | Config-as-code | Counterfactual/backup |
| Locust | Phù hợp | Phù hợp | Cần code policy rõ | Python user behavior | Counterfactual/backup |
| Gatling | Phù hợp | Phù hợp khi pin SDK/runtime | Checks/assertions | Structured DSL | Counterfactual/backup |

**Quyết định Desk Research:** chọn Apache JMeter và k6 làm cặp triển khai **provisional**. Quyết định chỉ được xác nhận sau khi hai công cụ chạy cùng functional contract, Workload Model và evidence requirements; ít nhất một shortlist alternative nên hoàn thành smoke test để kiểm soát selection bias.

---

# 9. Lý do lựa chọn Apache JMeter và k6

Phần lựa chọn được rút gọn thành **hai lý do chính**, tránh lặp lại kết luận “công cụ phổ biến” mà không gắn với mục tiêu seminar.

## 9.1. Lý do 1 — Phù hợp trực tiếp với EShop và mục tiêu T05

Topic brief T05 yêu cầu nhóm thiết kế Workload Model, triển khai bằng JMeter `.jmx` và k6 JavaScript, thu thập percentiles/error rate và minh họa AI-generated scenario được human-audit. Cả JMeter lẫn k6 đều có thể biểu diễn cùng endpoint, transaction mix, think time, duration, test data, success contract và threshold policy của EShop. Đây là điều kiện để so sánh có ý nghĩa và không quy nhầm khác biệt workload thành khác biệt công cụ.

Hai công cụ chỉ được xác nhận là phù hợp sau khi:

- Cùng vượt qua positive và negative functional controls.
- Cùng thực thi workload tương đương trên một SUT commit và dataset.
- Raw results, process exit, generator/SUT telemetry và cấu hình đều được lưu.
- Metric được đối chiếu theo cùng request/transaction name và cùng success policy.

## 9.2. Lý do 2 — Hai workflow bổ sung nhau và tạo giá trị AI audit

JMeter và k6 cùng có thể triển khai EShop workload, nhưng giúp người đọc quan sát hai cách tiếp cận khác nhau. JMeter đại diện traditional visual/Test Plan; k6 đại diện test-as-code, Git workflow và automation. Sự tương phản này phù hợp với mục tiêu seminar hơn việc chọn hai công cụ code-first gần giống nhau.

| Apache JMeter | k6 |
|---|---|
| GUI để xây dựng/debug Test Plan | JavaScript test-as-code |
| Cấu trúc cây trực quan | Script thuận tiện cho Git/code review |
| Thành phần Sampler/Timer/Assertion | Scenarios/Executors/Checks/Thresholds |
| HTML report sau CLI run | CLI output và automated thresholds |
| Tốt để dạy cấu trúc test | Tốt cho automation/CI/CD |
| File `.jmx` XML | File `.js` dễ audit bởi người và AI |

JMeter plan do nhóm xây dựng và giải thích thủ công đóng vai trò implementation đối chiếu. Với k6, requirement/HAR/log đã sanitize có thể được dùng để tạo JavaScript draft, sau đó con người phải kiểm tra endpoint, token correlation, data uniqueness, think time, checks, thresholds và stop conditions trước khi chạy. Vì vậy, AI được dùng để tăng tốc soạn thảo và review, không thay thế tester và không tạo ra số liệu performance.

---

# 10. Workload Model cho EShop

## 10.1. Objective

Mục tiêu của Workload Model là mô phỏng hành vi người dùng trên hệ thống EShop để đánh giá hiệu năng của ứng dụng dưới các mức tải khác nhau. Các bài kiểm thử được sử dụng để đo thời gian phản hồi (Response Time), thông lượng (Throughput), tỷ lệ lỗi (Error Rate) và khả năng duy trì ổn định của hệ thống trong điều kiện tải thông thường cũng như khi xảy ra lưu lượng truy cập đột biến.

## 10.2. Transaction Distribution

Workload được xây dựng dựa trên hành vi phổ biến của người dùng trên một hệ thống thương mại điện tử, trong đó phần lớn lưu lượng tập trung vào các thao tác xem và tìm kiếm sản phẩm, còn các thao tác giao dịch chiếm tỷ lệ nhỏ hơn.

| Transaction | Tỷ lệ |
|--------------|-------:|
| Browse/Search Products | 60% |
| View Product Details | 25% |
| Add to Cart | 10% |
| Checkout Flow | 5% |
| **Tổng** | **100%** |

### Lý do lựa chọn

- Người dùng chủ yếu truy cập để tìm kiếm hoặc duyệt sản phẩm.
- Một phần người dùng sẽ xem chi tiết sản phẩm trước khi quyết định mua.
- Chỉ một tỷ lệ nhỏ người dùng thêm sản phẩm vào giỏ hàng.
- Checkout là bước cuối của quy trình mua hàng nên có tần suất thấp nhất.
- Phân bố này giúp mô phỏng tương đối sát hành vi của người dùng trên một website thương mại điện tử và tránh tạo quá nhiều yêu cầu giao dịch không thực tế.

## 10.3. Think Time

Trong các bài kiểm thử Baseline, Virtual Users sử dụng Think Time ngẫu nhiên giữa các thao tác để mô phỏng hành vi người dùng thực tế.

| Transaction | Think Time |
|--------------|-----------:|
| Browse/Search Products | 1–3 giây |
| View Product Details | 2–5 giây |
| Add to Cart | 1–2 giây |
| Checkout Flow | 2–4 giây |

Đối với bài kiểm thử Spike, Think Time được đặt bằng **0 giây** nhằm tạo lượng yêu cầu tăng đột ngột lên hệ thống. Cấu hình này giúp mô phỏng tình huống lưu lượng truy cập tăng nhanh trong thời gian ngắn và đánh giá khả năng chịu tải cũng như tính ổn định của hệ thống.

## 10.4. Test Data

Dữ liệu kiểm thử được chuẩn bị theo flow và phải có manifest/cleanup rõ ràng:

- Browse/Search/Detail dùng Product ID lấy từ `GET /api/products` của đúng dataset trước run.
- Login/Cart/Checkout ưu tiên **test account riêng theo VU** hoặc partition account không giao nhau qua CSV/data file.
- Mỗi VU tự đăng nhập để nhận JWT và không chia sẻ token qua global mutable state.
- Checkout dùng address/order marker dành riêng cho test; không dùng dữ liệu cá nhân thật.
- Ghi database snapshot, row count trước–sau và cleanup procedure cho mọi write flow.

### Quy tắc về shared account

Source inspection cho thấy web frontend giữ cart trong React state, nhưng backend `/api/cart` lại lưu cart theo `userId`, còn `/api/checkout` tạo order trong SQLite. Vì vậy, hai browser có cart UI độc lập **không chứng minh** nhiều API VU dùng chung một account sẽ độc lập. Shared account có thể làm nhiễu cart state, order ownership và error rate.

Chỉ dùng một account chung cho flow authenticated khi có experiment riêng chứng minh không tạo state conflict đối với chính endpoint đang test. Nếu chưa có evidence đó, sử dụng account riêng theo VU; nếu không đủ account, giới hạn authenticated concurrency hoặc chỉ chạy read-only workload. Không trình bày tính độc lập của shared account như một empirical conclusion nếu chưa có raw request log, database evidence và run manifest.

## 10.5. Test Profiles

### Baseline Test (Load Test)

- **Concurrent Users:** 50 Virtual Users (VUs).
- **Ramp-up:** 1 phút.
- **Steady State:** 3 phút.
- **Ramp-down:** 1 phút.

**Mục tiêu**

- Thiết lập mức hiệu năng cơ sở của hệ thống.
- Đo Response Time (p50, p95, p99).
- Thu thập Throughput và Error Rate.
- Quan sát mức sử dụng tài nguyên hệ thống trong điều kiện tải bình thường.

### Spike Test

- **Concurrent Users:** tăng từ 50 lên 500 Virtual Users.
- **Ramp-up:** 30 giây.
- **Steady State:** 1 phút.
- **Ramp-down:** 30 giây.

**Mục tiêu**

- Đánh giá khả năng chịu tải khi lượng truy cập tăng đột ngột.
- Kiểm tra hệ thống có xảy ra lỗi, nghẽn cơ sở dữ liệu hoặc mất khả năng phục vụ hay không.
- Quan sát khả năng phục hồi của hệ thống sau khi lưu lượng giảm.

## 10.6. Performance Metrics

Trong mỗi lần thực thi kiểm thử sẽ thu thập các chỉ số sau:

- **Response Time:** Average, Median (p50), p95 và p99.
- **Throughput:** Requests per Second (RPS).
- **Error Rate:** Tỷ lệ các request thất bại (HTTP 4xx, HTTP 5xx hoặc timeout).

## 10.7. Workload Rationale

Workload được xây dựng theo mô hình điển hình của một hệ thống thương mại điện tử, trong đó phần lớn lưu lượng là các thao tác đọc (browsing và view detail), còn các thao tác ghi (Add to Cart và Checkout) chiếm tỷ lệ nhỏ hơn.

Việc phân bố như vậy giúp:

- Mô phỏng hành vi người dùng gần với thực tế.
- Tránh tạo quá nhiều yêu cầu Checkout không cần thiết.
- Đánh giá hiệu năng của hệ thống dưới điều kiện tải đại diện cho môi trường vận hành thông thường.

---

# 11. Phương pháp thực nghiệm

## 11.1. Nguyên tắc công bằng

JMeter và k6 phải dùng:

- Cùng Base URL.
- Cùng endpoint và HTTP method.
- Cùng test data.
- Cùng workload model
- Cùng duration/ramp-up.
- Cùng threshold definition.
- Chạy trên môi trường ổn định.

## 11.2. Quy trình chạy

1. Checkout đúng commit EShop.
2. Ghi cấu hình máy và tool version.
3. Khởi động SUT.
4. Xác minh health/manual flow.
5. Reset dữ liệu.
6. Warm-up ngắn.
7. Chạy baseline.
8. Chờ hệ thống ổn định/reset.
9. Chạy normal load.
10. Chạy spike.
11. Chạy stress nếu môi trường cho phép.
12. Lưu raw results và logs.
13. Lặp lại mỗi scenario tối thiểu 3 lần nếu thời gian cho phép.
14. So sánh median/xu hướng thay vì chọn lần chạy đẹp nhất.

## 11.3. Thresholds

> **[GIẢ ĐỊNH THỬ NGHIỆM]** Topic brief gợi ý SLO như p95 < 500 ms và error rate < 1%. Nếu không phải yêu cầu chính thức của EShop, báo cáo phải ghi đây là threshold của seminar.

| Metric | Threshold đề xuất |
|---|---|
| p95 | < 500 ms |
| Error rate | < 1% |
| HTTP 5xx | 0 hoặc giải thích rõ |
| Recovery after spike | Quay về gần baseline sau thời gian quan sát |

## 11.4. Monitoring

Tối thiểu theo dõi:

- CPU load generator.
- RAM load generator.
- CPU/RAM SUT.
- Database errors/locks.
- Application logs.
- Network errors/timeouts.

## 11.5. Kiểm soát sai lệch

- Không chạy JMeter load test bằng GUI.
- Tắt listener nặng trong lần chạy chính thức.
- Không mở nhiều ứng dụng nặng trên máy.
- Không thay đổi data hoặc code giữa hai tool runs.
- Random hóa thứ tự chạy nếu có thể để giảm bias do cache/warm state.
- Lưu timestamp và commit.

---

# 12. Triển khai bằng Apache JMeter

## 12.1. Cấu trúc Test Plan đề xuất

```text
Test Plan
├── User Defined Variables
├── HTTP Request Defaults
├── HTTP Header Manager
├── HTTP Cookie Manager
├── CSV Data Set Config
├── Setup Thread Group (nếu cần login/setup)
├── Main Thread Group
│   ├── Transaction Controller - Product Listing
│   ├── Transaction Controller - Search
│   ├── Transaction Controller - Product Detail
│   ├── Transaction Controller - Add to Cart
│   ├── Transaction Controller - Checkout
│   ├── JSON Extractor / Correlation
│   ├── Assertions
│   └── Timers
└── Minimal result writers / Backend Listener
```

## 12.2. Các thành phần quan trọng

- **Thread Group:** số thread/VU, ramp-up, loop/duration.
- **HTTP Request Defaults:** Base URL chung.
- **Header Manager:** content type, authorization.
- **Cookie Manager:** duy trì session.
- **CSV Data Set Config:** account, product và input data.
- **JSON Extractor:** lấy token/ID từ response.
- **Timer:** think time/pacing.
- **Response Assertion:** status và response content.
- **Transaction Controller:** gom request theo business transaction.

## 12.3. Lệnh chạy chính thức

```bash
jmeter -n \
  -t scripts/jmeter/eshop-performance.jmx \
  -l results/jmeter/run-01.jtl \
  -j results/jmeter/run-01.log \
  -e \
  -o results/jmeter/html-run-01
```

## 12.4. Quy tắc chạy

- GUI chỉ dùng để build/debug.
- CLI dùng cho load execution.
- Thư mục HTML output phải rỗng hoặc chưa tồn tại.
- Không ghi quá nhiều response body khi tải lớn.
- Theo dõi heap và CPU load generator.

## 12.5. Evidence cần nộp

- File `.jmx`.
- File `.jtl`.
- JMeter log.
- HTML report.
- Screenshot Test Plan.
- Command history.
- Tool version.
- Lỗi thật và cách sửa.

---

# 13. Triển khai bằng k6

## 13.1. Cấu trúc project đề xuất

```text
scripts/k6/
├── config.js
├── data/
│   ├── accounts.json
│   └── products.json
├── flows/
│   ├── browse.js
│   ├── login.js
│   ├── cart.js
│   └── checkout.js
├── tests/
│   ├── baseline.js
│   ├── load.js
│   ├── spike.js
│   └── stress.js
└── utils/
    ├── checks.js
    └── auth.js
```

## 13.2. Skeleton script

> Endpoint dưới đây là placeholder; phải thay bằng endpoint EShop đã xác minh.

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL;

if (!BASE_URL) {
  throw new Error('BASE_URL is required');
}

export const options = {
  stages: [
    { duration: '30s', target: 50 },
    { duration: '5m', target: 50 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
  },
};

export default function () {
  const response = http.get(`${BASE_URL}/[VERIFIED_PRODUCT_ENDPOINT]`);

  check(response, {
    'HTTP status is successful': (r) => r.status >= 200 && r.status < 300,
    'response body is not empty': (r) => Boolean(r.body && r.body.length > 0),
  });

  sleep(1 + Math.random() * 2);
}
```

## 13.3. Thành phần quan trọng

- `options`: workload và thresholds.
- `scenarios`: nhiều workload profile.
- `setup()`: lấy token hoặc chuẩn bị data dùng chung.
- `check()`: functional/business validation.
- `sleep()`: think time.
- Environment variables: Base URL và non-secret configuration.
- Custom metrics: business transaction time nếu cần.

## 13.4. Lệnh chạy

```bash
k6 run \
  -e BASE_URL=http://localhost:[PORT] \
  scripts/k6/tests/load.js
```

Xuất raw result theo phương án nhóm chọn:

```bash
k6 run --summary-export results/k6/summary-run-01.json \
  -e BASE_URL=http://localhost:[PORT] \
  scripts/k6/tests/load.js
```

## 13.5. Evidence cần nộp

- Script trước AI.
- AI-generated draft.
- Diff sau human correction.
- Terminal output.
- Summary JSON/raw metrics.
- Tool version.
- Screenshots.
- Errors và fixes.

---

# 14. AI-Augmented Performance Testing và AI Audit

## 14.1. Vai trò của AI

AI được phép hỗ trợ:

- Chuyển requirement thành script draft.
- Chuyển HTTP log/HAR thành flow draft.
- Đề xuất data parameterization.
- Đề xuất checks và thresholds.
- Phân tích log và tóm tắt anomalies.
- Audit một script theo checklist.

AI không được xem là nguồn xác nhận cuối cùng về endpoint, workload realism hoặc threshold.

## 14.2. Workflow

```text
Verified requirements / HAR / HTTP log
                    ↓
                  Prompt
                    ↓
          AI-generated k6 draft
                    ↓
       Syntax + endpoint verification
                    ↓
       Authentication/session audit
                    ↓
        Workload and think-time audit
                    ↓
          Checks/thresholds audit
                    ↓
             Corrected script
                    ↓
              Real execution
                    ↓
        Compare against server evidence
```

## 14.3. Prompt mẫu

```text
You are assisting with a performance test for the EShop SUT.
Use only the verified endpoints and request samples below.
Create a k6 draft for a 50-VU, 5-minute load test.

Requirements:
1. Preserve authentication and dynamic IDs.
2. Add realistic think time.
3. Add checks for HTTP status and business success.
4. Add thresholds: p95 < 500 ms and error rate < 1%.
5. Do not invent endpoints or fields.
6. Mark every assumption explicitly.

Verified inputs:
[PASTE HAR/LOG/REQUESTS AFTER REMOVING SECRETS]
```

## 14.4. AI Audit Checklist

| Hạng mục | Câu hỏi audit |
|---|---|
| Endpoint | Có tồn tại trong EShop commit không? |
| Method | GET/POST/PUT/DELETE có đúng không? |
| Payload | Field và type có đúng requirement không? |
| Authentication | Token/cookie được lấy và tái sử dụng đúng không? |
| Correlation | ID động có được extract không? |
| Data | Có dùng chung account gây conflict không? |
| Think time | Có phản ánh hành vi user không? |
| Mix | Tỷ lệ browse/search/cart/checkout có căn cứ không? |
| Checks | Có kiểm tra business success không? |
| Thresholds | Có căn cứ và đúng metric không? |
| Secrets | Có lộ password/token không? |
| Load safety | Có gây tải vượt khả năng môi trường không? |

## 14.5. Các lỗi AI thường cần tìm

1. Tự tạo endpoint không tồn tại.
2. Dùng sai HTTP method.
3. Hard-code token.
4. Không correlation product/cart/order ID.
5. Không có think time.
6. Chỉ check HTTP 200.
7. Checkout quá nhiều so với browse.
8. Dùng một account cho mọi VU.
9. Threshold không có căn cứ.
10. Trộn closed model và open model nhưng không giải thích.

## 14.6. Evidence AI bắt buộc

- Tên AI tool.
- Ngày giờ.
- Prompt đầy đủ hoặc prompt summary theo template môn học.
- Output gốc.
- Danh sách lỗi phát hiện.
- Diff trước/sau.
- Người review.
- Nguồn dùng để cross-check.

---

# 15. Kịch bản demo

> **Trạng thái:** `[KẾ HOẠCH — CHƯA THỰC THI]`. Chỉ thay trạng thái này khi có script/Test Plan, command, raw result, screenshot và log SUT tương ứng.

## 15.1. Trình tự demo đề xuất

1. Giới thiệu EShop commit, API Base URL, test data và workload contract dùng chung.
2. Mở JMeter GUI ở tải tối thiểu để giải thích Thread Group, HTTP Request, Header/Cookie Manager, Timer và Assertion; không dùng GUI để chạy tải chính thức.
3. Mở k6 JavaScript tương đương để giải thích scenarios/executors, checks, thresholds và environment variables.
4. Chạy positive smoke và negative control của từng công cụ; chỉ tiếp tục nếu failure propagation hoạt động đúng.
5. Chạy cùng một profile đã được phê duyệt bằng JMeter CLI và k6 CLI; lưu raw artefact và generator/SUT telemetry.
6. Điền bảng §16 và §17 từ evidence, sau đó trình bày khác biệt workflow thay vì tuyên bố tool nào luôn nhanh hơn.

## 15.2. Evidence tối thiểu cho demo

- JMeter `.jmx`, k6 `.js`, test-data/config files và commit/hash.
- Exact command, tool/runtime version, stdout/stderr và process exit code.
- JMeter JTL/HTML report; k6 raw output/summary; assertion/check/threshold results.
- Positive và negative control evidence.
- Timestamped CPU/RAM/network context của SUT và load generator.
- AI prompt/draft/diff và human-audit notes nếu dùng AI để scaffold k6 script.

# 16. Kết quả thực nghiệm và phân tích

> **[CẦN ĐIỀN EVIDENCE]** Không được tự tạo số liệu. Mỗi dòng phải liên kết tới raw result tương ứng.

## 16.1. Baseline

| Run | Tool | VU | Duration | Requests | p50 | p95 | p99 | Throughput | Error rate | Evidence |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | JMeter | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[link]` |
| 1 | k6 | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[link]` |

## 16.2. Normal Load – 50 VU/5 phút

| Run | Tool | p50 | p95 | p99 | Throughput | Error rate | CPU SUT | CPU Generator | Pass/Fail |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | JMeter | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 1 | k6 | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 2 | JMeter | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 2 | k6 | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 3 | JMeter | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| 3 | k6 | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |

## 16.3. Spike – 50→500 VU/30 giây

| Tool | Peak VU | Peak throughput | Peak error rate | Worst p95/p99 | Recovery time | Generator bottleneck? | Evidence |
|---|---:|---:|---:|---:|---:|---|---|
| JMeter | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[link]` |
| k6 | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[link]` |

## 16.4. Stress Test

| Load step | Duration | p95 | Throughput | Error rate | SUT CPU/RAM | Observed failure |
|---:|---:|---:|---:|---:|---|---|
| `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |

## 16.5. Cách viết phân tích

Mỗi scenario phải trả lời:

- Threshold có đạt không?
- Khi tải tăng, metric nào xấu đi trước?
- Throughput còn tăng hay plateau?
- Error là transport, HTTP hay business error?
- Load generator có cạn CPU/RAM không?
- Database/app log cho thấy gì?
- Hệ thống có phục hồi sau spike không?
- Hai implementation có thực sự tương đương không?

## 16.6. Câu mẫu hợp lệ

> “Trong run 02, p95 vượt threshold 500 ms từ giai đoạn `[X]`, đồng thời CPU SUT đạt `[Y]%`. Đây là tương quan quan sát được, chưa đủ để kết luận CPU là nguyên nhân duy nhất. Application log cho thấy `[EVIDENCE]`, vì vậy nhóm nghi ngờ `[HYPOTHESIS]` và cần thêm profiling để xác nhận.”

## 16.7. Câu không hợp lệ

> “Server chậm vì CPU cao.”

Câu này thiếu bằng chứng nguyên nhân và bỏ qua database, I/O, lock, load generator hoặc lỗi script.

---

# 17. So sánh JMeter và k6

## 17.1. So sánh workflow

| Khía cạnh | JMeter | k6 |
|---|---|---|
| Thiết kế ban đầu | GUI/Test Plan dễ quan sát | JavaScript cần coding |
| Review thay đổi | XML diff có thể khó đọc | Code diff rõ hơn |
| Debug | GUI, View Results Tree ở tải thấp | Console/log/checks |
| Load execution | CLI | CLI |
| Pass/fail tự động | Cần cấu hình/assertions/plugins/pipeline | Thresholds tích hợp rõ |
| Reporting | HTML dashboard và raw JTL | Summary/raw output/integrations |
| CI/CD | Có thể tích hợp | Developer-oriented, thuận tiện |
| AI generation | XML khó audit hơn | JavaScript thuận tiện hơn |
| Giá trị giảng dạy | Cấu trúc test trực quan | Minh họa test-as-code |

## 17.2. Ma trận trực quan về mức độ phù hợp

> **Cách đọc:** `●●●` = rất phù hợp trong bối cảnh seminar; `●●○` = phù hợp nhưng cần cấu hình hoặc có trade-off; `●○○` = không phải thế mạnh chính. Đây là **đánh giá Desk Research về fit**, không phải benchmark runtime và không thay thế dữ liệu thực nghiệm.

| Tiêu chí quyết định | JMeter | k6 | Cơ sở diễn giải |
|---|:---:|:---:|---|
| Chạy local, không phụ thuộc SaaS | ●●● | ●●● | Cả hai có local CLI và phù hợp API Base URL của EShop. |
| Multi-step journey, session và token | ●●● | ●●● | JMeter dùng Test Plan/config elements; k6 dùng JavaScript, per-VU state và request flow. |
| Workload control: VU, ramp, duration, scenario | ●●● | ●●● | Cả hai biểu diễn được baseline/load/spike khi dùng cùng workload contract. |
| Protocol và business validation | ●●● | ●●● | JMeter dùng Assertions; k6 dùng Checks và Thresholds. Cả hai vẫn cần negative control. |
| Percentiles, throughput, error information và raw artefact | ●●● | ●●● | JMeter có JTL/HTML dashboard; k6 có summary/raw outputs và integrations. |
| Trực quan hóa cấu trúc test cho audience | ●●● | ●●○ | Tree Test Plan của JMeter dễ trình bày; k6 cần đọc code. |
| Test-as-code, Git diff và modularization | ●●○ | ●●● | `.jmx` có thể version-control nhưng XML diff khó hơn JavaScript. |
| CI/CD và automated quality gate | ●●○ | ●●● | JMeter cần thiết kế assertion/result parser/pipeline; k6 có Thresholds trực tiếp. |
| AI-generated draft và human audit | ●●○ | ●●● | AI có thể hỗ trợ cả hai, nhưng JavaScript k6 dễ review hơn JMX/XML. |
| Khả năng chạy cùng một EShop workload để đối chiếu | ●●● | ●●● | Cùng endpoint, data, pacing, duration và success contract có thể được triển khai ở cả hai. |

Ma trận cho thấy hai công cụ **cùng mạnh ở các tiêu chí cốt lõi của EShop**, trong khi các ô khác biệt tập trung đúng vào learning objective: JMeter mạnh về visual/Test Plan, k6 mạnh về test-as-code, CI/CD và AI audit. Đây là lý do chọn một **cặp bổ sung**, không phải tuyên bố k6 hoặc JMeter luôn thắng mọi công cụ khác.

## 17.3. Bảng metric thực nghiệm cần điền

> **Trạng thái:** chưa có execution evidence. Chỉ điền số sau khi cả hai implementation vượt qua functional validity gate và chạy cùng SUT commit, dataset, transaction mix, pacing, duration và load profile. Không dùng số ví dụ hoặc số do AI tạo.

| Metric đánh giá | Đơn vị/cách tính | JMeter | k6 | Quy tắc diễn giải |
|---|---|---:|---:|---|
| Positive functional control | `PASS/FAIL` | `[CHƯA CHẠY]` | `[CHƯA CHẠY]` | Status, body marker, token và business check phải đúng trước khi đo latency. |
| Negative control propagation | `PASS/FAIL` | `[CHƯA CHẠY]` | `[CHƯA CHẠY]` | Marker/threshold cố ý sai phải làm assertion/gate và pipeline fail. |
| Achieved request/iteration count | Count + transaction mix | `[CHƯA CHẠY]` | `[CHƯA CHẠY]` | Hai run chỉ so sánh khi lượng công việc và mix thực tế tương đương. |
| Setup time | Phút; timestamp bắt đầu–kết thúc | `[CHƯA ĐO]` | `[CHƯA ĐO]` | Tách download time, configuration time và troubleshooting time. |
| Script/Test Plan creation time | Phút; commit/timestamp evidence | `[CHƯA ĐO]` | `[CHƯA ĐO]` | Dùng cùng requirements và cùng người/skill baseline nếu có thể. |
| Debug time | Phút đến khi positive + negative control đạt | `[CHƯA ĐO]` | `[CHƯA ĐO]` | Không chỉ tính thời gian đến khi command exit 0. |
| Response time p50 | Millisecond | `[CHƯA CHẠY]` | `[CHƯA CHẠY]` | Báo theo cùng transaction; không trộn request name khác nhau. |
| Response time p95 | Millisecond | `[CHƯA CHẠY]` | `[CHƯA CHẠY]` | Chỉ diễn giải sau warm-up và kiểm tra sample count. |
| Response time p99 | Millisecond | `[CHƯA CHẠY]` | `[CHƯA CHẠY]` | Ghi rõ sample size; p99 nhỏ không có ý nghĩa nếu run quá ngắn. |
| Throughput | Requests/second và business transactions/second | `[CHƯA CHẠY]` | `[CHƯA CHẠY]` | Phân biệt raw HTTP request với completed business transaction. |
| Error rate | `% = failed / total × 100` | `[CHƯA CHẠY]` | `[CHƯA CHẠY]` | Bao gồm transport, unexpected status và business-check failure theo cùng policy. |
| Load-generator CPU | Average/peak `%` | `[CHƯA ĐO]` | `[CHƯA ĐO]` | Nếu generator bão hòa, kết quả phải ghi `INCONCLUSIVE`. |
| Load-generator RAM | Average/peak MiB | `[CHƯA ĐO]` | `[CHƯA ĐO]` | Đo process và host context; không chỉ chụp một thời điểm. |
| SUT CPU/RAM | Average/peak `%` và MiB | `[CHƯA ĐO]` | `[CHƯA ĐO]` | Đồng bộ timestamp với raw result để tránh quy kết nguyên nhân sai. |
| Run-to-run variability | Ít nhất 3 run; range/CV | `[CHƯA CHẠY]` | `[CHƯA CHẠY]` | Không kết luận từ một lần chạy duy nhất. |
| Artefact completeness | `% mục evidence bắt buộc có đủ` | `[CHƯA ĐÁNH GIÁ]` | `[CHƯA ĐÁNH GIÁ]` | Version, script/config, command, raw result, log, exit và telemetry. |
| Maintainability | Rubric 1–5 + review notes | `[CHƯA ĐÁNH GIÁ]` | `[CHƯA ĐÁNH GIÁ]` | Chấm theo readability, modularity, diff quality, data/config separation và onboarding. |

## 17.4. Khuyến nghị theo bối cảnh

### Dùng JMeter khi

- Nhóm cần GUI để xây dựng và giải thích Test Plan.
- Người học cần nhìn rõ thành phần sampler, timer và assertion.
- Cần HTML report và hệ sinh thái JMeter.
- Team đã có `.jmx` hoặc kinh nghiệm JMeter.

### Dùng k6 khi

- Team muốn test-as-code và Git workflow.
- Developer quen JavaScript.
- Cần thresholds cho CI/CD.
- Muốn AI tạo draft script dễ review.
- Cần modular hóa flow bằng code.

### Không nên kết luận

- JMeter luôn chậm hơn k6.
- k6 luôn dễ hơn JMeter.
- Một tool có p95 thấp hơn nghĩa SUT nhanh hơn; có thể workload khác.

## 17.5. Bảng kết luận trực quan

| Câu hỏi quyết định | Apache JMeter | k6 | Kết luận ở cấp cặp công cụ |
|---|---|---|---|
| Có test được EShop API journey không? | Có: Test Plan, sampler, config elements, assertions | Có: JavaScript flow, per-VU state, checks | **Cả hai đủ điều kiện để chạy cùng workload.** |
| Có hỗ trợ đọc kết quả theo percentile/throughput/error không? | Có: JTL và HTML dashboard | Có: summary/raw outputs/integrations | **Có thể dùng cùng metric contract để phân tích.** |
| Có phù hợp traditional workflow không? | **Rất phù hợp** | Phù hợp ở CLI/code | **JMeter đảm nhiệm vai trò traditional/visual.** |
| Có phù hợp test-as-code và CI/CD không? | Có nhưng XML/pipeline cần tổ chức kỹ | **Rất phù hợp** với JavaScript và Thresholds | **k6 đảm nhiệm vai trò developer-centric.** |
| Có phù hợp AI-assisted workflow không? | AI hỗ trợ được nhưng JMX khó audit hơn | **Phù hợp rõ** cho draft JavaScript + human audit | **k6 tạo AI angle; JMeter tạo implementation đối chiếu.** |
| Có thể kết luận tool nào nhanh hơn ngay bây giờ không? | Không | Không | **Chưa có EXP; phải điền bảng §17.3 từ raw evidence.** |
| Vì sao chọn cả hai? | Trực quan hóa cấu trúc và traditional Test Plan | Reproducible test-as-code, automated gate và AI audit | **Hai công cụ vừa có nền tảng chung để so sánh, vừa bổ sung nhau về learning value.** |

---

# 18. Troubleshooting

> Chỉ giữ các lỗi nhóm thực sự gặp. Mỗi lỗi cần screenshot/log.

## 18.1. Connection Refused

- **Symptom:** request không kết nối được.
- **Nguyên nhân khả dĩ:** SUT chưa chạy, sai port/Base URL, firewall hoặc container mapping.
- **Cách xác minh:** dùng browser/curl, kiểm tra port và application log.
- **Fix:** sửa Base URL, khởi động service, cập nhật mapping.

## 18.2. Authentication Failed/Token Expired

- **Symptom:** HTTP 401/403 hoặc business unauthorized.
- **Nguyên nhân:** token hard-code, token hết hạn, flow login sai.
- **Cách xác minh:** so sánh manual request và script; xem response body.
- **Fix:** login trong setup/flow, extract token, dùng test accounts riêng.

## 18.3. JMeter GUI/Listener tiêu thụ nhiều tài nguyên

- **Symptom:** load generator CPU/RAM cao, throughput thấp bất thường.
- **Fix:** chạy CLI, tắt listener nặng, chỉ ghi dữ liệu cần thiết.

## 18.4. Missing k6 Environment Variable

- **Symptom:** URL `undefined` hoặc script fail.
- **Fix:** validate `BASE_URL`, dùng command `-e` hoặc environment an toàn.

## 18.5. Database Lock/Write Conflict

- **Symptom:** request ghi thất bại, latency tăng, log báo lock/conflict.
- **Nguyên nhân:** nhiều VU dùng cùng data hoặc giới hạn database.
- **Fix:** tách account/data, giảm write ratio, reset database và ghi limitation.

## 18.6. Load Generator Bottleneck

- **Symptom:** CPU generator đạt giới hạn, throughput plateau dù SUT còn tài nguyên.
- **Fix:** giảm overhead, tắt logging nặng, tách máy hoặc distributed load nếu cần.

---

# 19. Failure Modes

## 19.1. HTTP 200 nhưng business failure

- **Trigger:** script chỉ dùng protocol status.
- **Symptom:** công cụ ghi success nhưng body báo lỗi.
- **Detection:** assertion/check response schema và business field.
- **Mitigation:** định nghĩa business checks; ghi check failure vào error analysis.

## 19.2. Load generator trở thành bottleneck

- **Trigger:** listener/logging nặng, CPU/RAM thấp, quá nhiều VU.
- **Symptom:** throughput plateau; generator CPU 100%; SUT chưa dùng hết tài nguyên.
- **Detection:** monitor cả generator và SUT.
- **Mitigation:** CLI/headless, giảm logging, tăng/tách generator.

## 19.3. AI-generated workload không thực tế

- **Trigger:** prompt thiếu production behavior hoặc transaction mix.
- **Symptom:** quá nhiều checkout, không think time, mọi VU giống nhau.
- **Detection:** business review và so với log/requirement.
- **Mitigation:** bắt AI đánh dấu assumptions; human chỉnh workload.

## 19.4. Average che giấu tail latency

- **Trigger:** chỉ xem average.
- **Symptom:** average đạt nhưng một nhóm user rất chậm.
- **Detection:** p95/p99 và distribution.
- **Mitigation:** threshold trên percentiles và phân tích theo transaction.

## 19.5. Cache làm kết quả quá lạc quan

- **Trigger:** lặp lại cùng request/data.
- **Symptom:** response nhanh dần nhưng không đại diện traffic đa dạng.
- **Detection:** so sánh cold/warm cache, randomize data.
- **Mitigation:** ghi rõ cache condition; dùng data đa dạng.

## 19.6. Shared test account gây conflict

- **Trigger:** mọi VU dùng cùng account/cart.
- **Symptom:** race condition, overwrite, lock hoặc business failure.
- **Detection:** log account/order IDs.
- **Mitigation:** account pool, unique data, cleanup strategy.

## 19.7. Hai tool chạy workload không tương đương

- **Trigger:** khác think time, connection reuse, number of iterations hoặc checks.
- **Symptom:** metrics khác lớn nhưng nguyên nhân là implementation.
- **Detection:** compare request count, server logs và timeline.
- **Mitigation:** workload contract và validation trước comparison.

---

# 20. Giới hạn nghiên cứu

1. Workload có thể dựa một phần trên giả định, không phải production logs.
2. Local environment không đại diện production topology.
3. Database và dataset có thể nhỏ.
4. SUT và load generator có thể dùng chung máy.
5. 15 công cụ không được deep-test ở mức độ giống nhau; vòng đầu là survey/smoke test.
6. Commercial/cloud tools chịu constraints access.
7. JMeter và k6 dùng execution models có thể không hoàn toàn giống nhau.
8. Kết quả bị ảnh hưởng bởi cache, OS, runtime và background process.
9. Chưa có distributed load nếu nhóm không triển khai.
10. AI output phụ thuộc chất lượng input và model tại thời điểm sử dụng.

---

# 21. Kết luận và khuyến nghị

Nhóm khảo sát 15 công cụ thuộc nhiều nhóm khác nhau: enterprise platforms, cloud services, lightweight HTTP benchmarks, distributed load tools, orchestration frameworks và full performance testing/test-as-code tools. Kết quả sàng lọc cho thấy không thể đánh giá mọi công cụ bằng một tiêu chí duy nhất. wrk, Vegeta, Siege và ApacheBench phù hợp benchmark HTTP; Loader.io phù hợp endpoint public qua cloud; Silk Performer, NeoLoad và LoadRunner Professional hướng enterprise; Tsung đại diện distributed load generation; Taurus đại diện orchestration/automation; còn JMeter, k6, Locust, Gatling và Artillery phù hợp hơn với multi-step EShop workload được deep-test trực tiếp.

JMeter và k6 được chọn vì **hai lý do chính**. Thứ nhất, chúng đại diện cho hai workflow bổ sung và cùng bám sát learning objectives T05: JMeter visual/Test Plan và k6 test-as-code. Thứ hai, cả hai có thể triển khai cùng EShop workload để so sánh công bằng, trong khi k6 JavaScript tạo điều kiện minh họa quy trình AI-generated draft và human audit với JMeter làm implementation đối chiếu.

Nhóm không kết luận một công cụ tốt hơn tuyệt đối. JMeter phù hợp khi cần GUI, cấu trúc Test Plan trực quan và hệ sinh thái quen thuộc. k6 phù hợp khi team ưu tiên Git, code review, CI/CD và thresholds. Kết luận về performance của EShop chỉ được đưa ra sau khi bảng kết quả được điền từ raw evidence và kiểm tra load generator bottleneck.

Khuyến nghị cuối cùng:

- Dùng JMeter để trình bày traditional workflow và giúp audience hiểu cấu trúc Performance Test.
- Dùng k6 để trình bày test-as-code, thresholds và AI audit.
- Giữ Artillery hoặc Locust làm backup nếu môi trường k6 gặp vấn đề.
- Dùng LoadRunner Professional, Tsung và Taurus để mở rộng phần khảo sát theo ba hướng enterprise, distributed và orchestration; không trình bày chúng như ba lựa chọn tương đương trực tiếp với JMeter/k6 nếu chưa có cùng mức evidence.
- Dùng benchmark tools như wrk/Vegeta/ApacheBench cho endpoint sanity check, không thay thế full journey test.
- Không sử dụng AI output trực tiếp nếu chưa audit.

---

# 22. AI Usage Declaration

| AI Tool | Ngày giờ | Mục đích | Input | Output | Human verification |
|---|---|---|---|---|---|
| OpenAI Codex | 2026-07-15 | Hợp nhất hai attachment thành một báo cáo Markdown; bổ sung Section 8; rút Section 9 còn đúng hai lý do; tạo ma trận fit và bảng metric ở Section 17; rà fabricated-evidence wording | Hai pasted-text attachment, source EShop local và báo cáo Desk Research đã audit | `Bao_Cao_Seminar_Performance_Testing_Tools.md` | Kiểm tra số mục 1–23, 15 tool đúng thứ tự, official references, placeholder EXP và Markdown structure; nhóm phải review lại trước khi nộp |
| `[AI TOOL]` | `[ ]` | Sinh k6 draft | Sanitized HAR/log | k6 script | Verify endpoint, session, data, checks, thresholds |
| `[AI TOOL]` | `[ ]` | Audit script | Script + checklist | Issues list | Review bằng test run và server logs |

## Cam kết

- Không đưa secret/token/password thật vào AI.
- Không trích dẫn AI thay tài liệu chính thức.
- Không copy AI output chưa chỉnh sửa.
- Lưu prompt, output và correction evidence.
- Không dùng AI để tạo số liệu performance, screenshot hoặc audience feedback giả.

---

# 23. Tài liệu tham khảo

## 23.1. Tài liệu môn học

1. `Seminar_Guide.docx` – Master Guide và rubric.
2. `Seminar_Workflow_Briefing.pdf` – 8 stages, demo, AI Audit và pitfalls.
3. `T05_Performance_Testing.docx` – Topic brief T05.
4. `T05_Performance_Testing_InClass.pptx` – Workload Model Bake-off.

## 23.2. Tài liệu chính thức Performance Testing

1. International Software Testing Qualifications Board (ISTQB). (2022). *Standard glossary of terms used in software testing* (Version 3.7). [https://www.ctqb.org/en/downloads/istqb.html?cid=33119&file=files%2Fcontent%2Fctqb%2Fdownloads%2Fistqb%2FGlossary-terms-version-3.7.pdf](https://www.ctqb.org/en/downloads/istqb.html?cid=33119&file=files%2Fcontent%2Fctqb%2Fdownloads%2Fistqb%2FGlossary-terms-version-3.7.pdf)

2. Meier, J. D., Farre, C., Bansode, P., Barber, S., & Rea, D. (2007). *Performance Testing Guidance for Web Applications*. Microsoft patterns & practices. [https://learn.microsoft.com/en-us/previous-versions/msp-n-p/bb924356(v=pandp.10)](https://learn.microsoft.com/en-us/previous-versions/msp-n-p/bb924356(v=pandp.10))
## 23.3. Tài liệu chính thức của công cụ

1. Apache JMeter – Getting Started: <https://jmeter.apache.org/usermanual/get-started.html>
2. Apache JMeter – Best Practices: <https://jmeter.apache.org/usermanual/best-practices.html>
3. Grafana k6 – Scenarios: <https://grafana.com/docs/k6/latest/using-k6/scenarios/>
4. Grafana k6 – Checks: <https://grafana.com/docs/k6/latest/using-k6/checks/>
5. Grafana k6 – Thresholds: <https://grafana.com/docs/k6/latest/using-k6/thresholds/>
6. Locust Documentation: <https://docs.locust.io/en/stable/what-is-locust.html>
7. Gatling Concepts: <https://docs.gatling.io/concepts/>
8. Artillery Documentation: <https://www.artillery.io/docs>
9. Silk Performer Documentation: <https://www.microfocus.com/documentation/silk-performer/>
10. Tricentis NeoLoad: <https://www.tricentis.com/products/performance-testing-neoload>
11. Loader.io: <https://loader.io/>
12. wrk Repository: <https://github.com/wg/wrk>
13. Vegeta Repository: <https://github.com/tsenart/vegeta>
14. Siege: <https://www.joedog.org/siege-home/>
15. ApacheBench: <https://httpd.apache.org/docs/2.4/programs/ab.html>
16. OpenText LoadRunner Professional: <https://www.opentext.com/products/loadrunner-professional>
17. Tsung Documentation: <https://tsung.readthedocs.io/en/latest/>
18. Taurus Documentation: <https://gettaurus.org/docs/Index/>

---
