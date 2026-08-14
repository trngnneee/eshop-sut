# 06 — AI Analysis Critique & Misinterpretation Hunt (Task 2)

> **Học phần:** Kiểm thử Phần mềm (HW05)  
> **Nhiệm vụ:** Task 2 — Phân tích Kết quả bằng AI & Săn tìm Lỗi Hiểu sai (Misinterpretation Hunt)  
> **Sinh viên:** Khoa (MSSV: **23127207**) · **SUT:** EShop  
> **Mục tiêu năng lực:** Bloom-AI **G9.3 (Evaluate)** & **G9.5 (Meta-Evaluate)**  
> **Công cụ AI thực hiện:** `Gemini 2.5 Pro (via Antigravity Engine)` · **Timestamp:** `2026-08-14T22:30:00+07:00`  

---

## 1. Nhật ký Chuỗi 4 Lần Tương tác Phân tích với AI (Guided Dialogue Sequence)

### 1.1 Lần 1 — Khám phá Không Gợi ý (Discovery Prompt)
- **Kỹ sư Con người (Prompt nguyên văn):**
  > "Hãy đọc toàn bộ dữ liệu tóm tắt từ 4 file `summary.json` của kịch bản Load, Stress, Spike, Endurance của sinh viên 23127207 (kịch bản Browse-to-buy). Hãy chỉ ra đâu là nút thắt cổ chai (bottleneck) lớn nhất của hệ thống và đề xuất 3 giải pháp cải tiến kiến trúc."

- **AI — Gemini 2.5 Pro (Output thô ban đầu):**
  > *"Dựa trên dữ liệu 4 kịch bản kiểm thử hiệu năng, tôi phân tích các vấn đề chính như sau:*
  > *1. Nút thắt cổ chai lớn nhất là cơ sở dữ liệu SQLite bị nghẽn do thiếu Index trên bảng `products` khi người dùng gọi `GET /api/products`.*
  > *2. Khuyến nghị cấu hình Connection Pool `max: 10, min: 2` cho SQLite để tăng khả năng xử lý truy vấn đồng thời.*
  > *3. Trong kịch bản Spike, khi bị lỗi kết nối hoặc thời gian phản hồi tăng cao, nguyên nhân là do hệ thống bị sập vì quá tải CPU.*
  > *4. Trong kịch bản Endurance, RAM tăng liên tục do kết nối cơ sở dữ liệu SQLite không được đóng sau mỗi request (Database Connection Leak)."*

---

### 1.2 Lần 2 — Kỹ sư Con người Chất vấn & Phản biện (Challenge Prompt)
- **Kỹ sư Con người (Prompt phản biện nguyên văn):**
  > "Phân tích của bạn có 4 điểm mâu thuẫn trực tiếp với mã nguồn backend/server.js và dữ liệu log thực tế:
  > 1. `GET /api/products` thực thi câu lệnh `SELECT * FROM products` lấy toàn bộ bảng không có mệnh đề `WHERE`. Tại sao bạn lại đề xuất thêm Index?
  > 2. SQLite là cơ sở dữ liệu nhúng đơn tệp (file-based, single-writer lock), thư viện `sqlite3` trong Node.js không có khái niệm Client-Server Connection Pool. Tại sao lại cấu hình Pool?
  > 3. Xem log Spike: CPU chỉ đạt đỉnh 5.33%, tại sao lại khẳng định 'sập vì CPU'? Khi có lỗi kết nối, bạn đã kiểm tra xem tiến trình backend có bị xung đột cổng mạng hoặc crash do unhandled error hay chưa?
  > 4. Kiểm tra `server.js:14,293`: Mảng `userCarts[userId].push(req.body)` không hề được giải phóng sau checkout. Đây là memory leak in-memory hay connection leak?"

- **AI — Gemini 2.5 Pro (Output đính chính sau chất vấn):**
  > *"Tôi xin đính chính toàn bộ 4 điểm trên sau khi đối chiếu mã nguồn thực tế:*
  > *1. Đúng, truy vấn quét toàn bộ bảng (Full Table Scan) không dùng Index; giải pháp đúng phải là áp dụng phân trang `LIMIT / OFFSET` để giảm kích thước payload 154KB.*
  > *2. SQLite không hỗ trợ Connection Pool; giải pháp đúng là chuyển sang cơ sở dữ liệu Client-Server như PostgreSQL nếu cần ghi đồng thời.*
  > *3. Về Spike Test, CPU rất thấp (5.33%), nguyên nhân nghẽn là do hàng đợi sự kiện Node.js bị dồn ứ khi có 300 kết nối đồng thời, hoặc lỗi xung đột cổng mạng/process, không phải do kiệt quệ CPU phần cứng.*
  > *4. Rò rỉ bộ nhớ thực chất nằm ở biến toàn cục `userCarts` trong heap của Node.js (`server.js:14,293`), không liên quan đến SQLite connection."*

---

### 1.3 Lần 3 — Đào sâu Phân tích Định lượng (Deep-dive Prompt)
- **Kỹ sư Con người (Prompt nguyên văn):**
  > "Dựa trên số liệu Endurance: RAM bắt đầu 60.30 MB, kết thúc 137.39 MB sau 11.95 phút, hãy tính độ dốc rò rỉ (MB/phút) và dự báo thời gian OOM trên container 512MB và 1024MB."

- **AI — Gemini 2.5 Pro (Output tính toán):**
  > *"Độ dốc rò rỉ bộ nhớ thực tế:*
  > $$\text{Leak Rate} = \frac{137.39 - 60.30}{11.95} = 6.45\text{ MB/phút} \approx 387.0\text{ MB/giờ}$$
  > *Dự báo thời gian sập do cạn kiệt bộ nhớ (Time to Out-of-Memory):*
  > *- Container 512MB: $\frac{512 - 60.30}{6.45} \approx \mathbf{70\text{ phút}}$ (~1.17 giờ).*
  > *- Container 1024MB: $\frac{1024 - 60.30}{6.45} \approx \mathbf{149\text{ phút}}$ (~2.49 giờ).*
  > *- Node.js Heap 2048MB: $\frac{2048 - 60.30}{6.45} \approx \mathbf{308\text{ phút}}$ (~5.14 giờ)."*

---

### 1.4 Lần 4 — Đánh giá Năng lực Tự phản biện (Meta-Evaluation Prompt)
- **Kỹ sư Con người (Prompt nguyên văn):**
  > "Hãy tự tổng kết lại tại sao bạn đưa ra các nhận định sai ở Lần 1 và bài học cốt lõi khi dùng AI trong phân tích kiểm thử hiệu năng là gì?"

- **AI — Gemini 2.5 Pro (Output tự phê bình):**
  > *"Nguyên nhân gốc rễ là do tôi đã suy diễn dựa trên các mẫu kiến thức tổng quát (generic mental models) mà không đọc chi tiết mã nguồn triển khai thực tế. Khi thấy độ trễ tăng, tôi tự động gợi ý 'Index' và 'Connection Pool' — vốn là giải pháp cho RDBMS truyền thống nhưng hoàn toàn vô nghĩa với SQLite và câu truy vấn quét toàn bảng."*

---

## 2. Bảng Săn tìm 5 Lỗi Hiểu sai Nguy hiểm của AI (Misinterpretation Hunt Matrix)

| STT | Lỗi Hiểu sai của AI (AI Misinterpretation) | Thực tế Kỹ thuật & Mã nguồn SUT | Tác hại nếu áp dụng vào Thực tế | Phân loại Lỗi |
|:---:|:---|:---|:---|:---|
| **1** | **Nhầm lẫn In-memory Leak thành DB Connection Leak** | Rò rỉ xảy ra tại mảng toàn cục `userCarts` trong heap V8 (`server.js:14,293`), không hề có rò rỉ kết nối SQLite | Đội ngũ Dev sẽ mất hàng tuần tối ưu SQLite mà bỏ qua dòng code rò rỉ bộ nhớ thực sự | **Domain Incompetence** |
| **2** | **Đề xuất Index cho truy vấn không có WHERE** | `GET /api/products` chạy `SELECT * FROM products` lấy toàn bộ 505 sản phẩm | Tạo thêm index làm chậm thao tác INSERT/UPDATE mà không cải thiện được 1ms đọc nào | **Hallucinated Optimization** |
| **3** | **Đề xuất Connection Pool cho SQLite** | SQLite hoạt động theo cơ chế file lock đơn luồng ghi; driver `sqlite3` serialize truy vấn | Gây lỗi cấu hình runtime khi cố gắng truyền tham số pool không được hỗ trợ | **Architectural Ignorance** |
| **4** | **Đổ lỗi cho 'Quá tải CPU' khi độ trễ tăng** | CPU chỉ đạt đỉnh 5.33%; độ trễ tăng là do hàng đợi sự kiện Node.js và GC Pauses khi heap phình to | Bỏ sót lỗi phần mềm nghiêm trọng, quy sai trách nhiệm sang hạ tầng phần cứng | **Causal Fallacy** |
| **5** | **Tính Percentile sai chuẩn toán học** | AI dùng công thức nội suy tuyến tính `(N-1)*p`, làm lệch số p95 so với JMeter HTML report | Làm sai lệch báo cáo nghiệm thu SLO, gây tranh cãi giữa QA và Khách hàng | **Math Method Mismatch** |

---

## 3. Kết luận & Khuyến nghị Thực hành (Key Takeaways)

1. **AI là công cụ hỗ trợ tổng hợp, không phải trọng tài kỹ thuật:** Mọi kết luận của AI về nguyên nhân nghẽn (bottleneck) đều phải được kiểm chứng chéo với mã nguồn backend và log phần cứng.
2. **Kỹ sư kiểm thử cần nắm vững bản chất công nghệ:** Hiểu rõ giới hạn của SQLite, cơ chế quản lý bộ nhớ của V8, và chuẩn toán học ISO 80000-2 là vũ khí quan trọng nhất để vạch trần các ảo giác (hallucinations) của AI.
