# 03 — Human Review & AI Mistakes Fixes Log

> **Học phần:** Kiểm thử Phần mềm (HW05)  
> **Sinh viên:** Khoa (MSSV: **23127207**) · **SUT:** EShop  
> **Mục tiêu năng lực:** Bloom-AI **G9.3 (Evaluate)** & **G9.4 (Correct)**  

---

## 1. Tổng quan Đánh giá Chất lượng Test Plan do AI sinh ra

Trong quá trình khởi tạo test plan ban đầu, AI đã mắc phải **6 lỗi kỹ thuật nghiêm trọng** (khiếm khuyết kiến trúc JMeter và hiểu sai hành vi SUT). Nếu không có kỹ sư con người can thiệp rà soát mã nguồn SUT (`backend/server.js`) và cấu trúc XML của JMeter, các bài test sẽ fail 100% hoặc cho ra số liệu sai lệch hoàn toàn.

---

## 2. Bảng Phân loại 6 Lỗi và Biện pháp Khắc phục

| STT | Lỗi do AI sinh ra | Triệu chứng / Hậu quả | Nguyên nhân gốc rễ | Biện pháp sửa đổi của Con người | Phân loại lỗi (Taxonomy) |
|:---:|:---|:---|:---|:---|:---|
| **1** | Bỏ sót `quotedData=true` trong CSV Data Set Config | JMeter đọc sai cột địa chỉ `123 Le Loi, Q1`, tách nhầm dấu phẩy trong chuỗi thành 2 cột, làm payload Checkout hỏng | AI dùng cấu hình mặc định của JMeter (`quotedData=false`), không tuân thủ chuẩn RFC 4180 | Bật `<boolProp name="quotedData">true</boolProp>` trong mọi CSV Data Set | **Data / Parser Format** |
| **2** | Nhầm lẫn logic Token JWT: Trích xuất `token` nhưng dùng sai tên biến `${jwt}` ở Header Manager | 100% request `04_AddToCart` và `05_Checkout` bị trả về `401 Unauthorized` | AI không đồng bộ tên biến giữa JSON PostProcessor (`referenceNames=token`) và Header (`Bearer ${jwt}`) | Chuẩn hóa toàn bộ tên biến là `${token}` và gán Header Manager cục bộ dưới từng Sampler yêu cầu Auth | **Variable Correlation** |
| **3** | Không trích xuất động `product_id` từ `02_BrowseProducts` | Tất cả 50 VU đều mua cùng 1 sản phẩm hard-coded `id=1`, không phản ánh đúng hành vi người dùng thật | AI viết sampler độc lập, thiếu PostProcessor gom danh sách `$..id` với `match_number=0` | Thêm JSON PostProcessor `extract_pid` với match number 0 (chọn ngẫu nhiên 1 ID từ catalog 505 sản phẩm) | **Dynamic Extraction** |
| **4** | Lập lịch Stress Test dùng `Constant Throughput Timer` sai mục đích | Thread Group cố gắng ép tải ảo, gây nghẽn tại client thay vì tăng tải bậc thang thực tế | AI không phân biệt được Stepped Concurrency Thread Group và CTT | Tái cấu trúc thành **Test Fragment (`FRAG_BrowseToBuy`)** kết hợp **4 Thread Group bậc thang (25 $\to$ 50 $\to$ 100 $\to$ 200 VU)** qua `ModuleController` | **Concurrency Architecture** |
| **5** | Đặt Assertion kiểm tra `response_data` chứa `error` một cách ngây thơ | Gặp sản phẩm có mô tả chứa từ `"error"` hoặc chuỗi vô hại thì bị đánh trượt giả (False Positive) | AI dùng substring assertion đơn giản không dựa trên JSON schema chuẩn | Thay bằng Response Assertion mã trạng thái HTTP `200` và `JSONPathAssertion` kiểm tra sự tồn tại của trường nghiệp vụ (`$.token`, `$.orderId`) | **Assertion Robustness** |
| **6** | Lỗi cú pháp import trong script Agent Skill (`from xml.dom import minidmin`) | Script `generate_jmx.py` crash ngay khi gọi `--help`, không thể sinh file test plan tự động | AI gõ sai chính tả thư viện chuẩn `minidom` | Sửa lại `from xml.dom import minidom`, bổ sung `sys.stdout.reconfigure(encoding="utf-8")` trên Windows và kiểm thử thực thi sinh ra 2 file JMX thật | **Syntax & Toolchain Integrity** |

---

## 3. Bài học Rút ra (Lessons Learned)

1. **AI không có ngữ cảnh mã nguồn nếu không được cung cấp trực tiếp:** Cần bắt buộc AI đọc các dòng code cốt lõi của backend trước khi thiết kế test plan.
2. **Kiểm thử hiệu năng đòi hỏi tính toàn vẹn của dữ liệu (Data Integrity):** Một lỗi nhỏ về format CSV (dấu phẩy trong ngoặc kép) có thể phá hủy toàn bộ kịch bản tải.
3. **Correlation (Liên kết biến động) là điểm yếu phổ biến của AI:** Luôn phải rà soát thủ công luồng dữ liệu từ Response của request trước sang Request Body/Header của request sau.
4. **Mọi script do AI sinh ra phải được chạy thử thực tế:** Không bao giờ chấp nhận script mà chưa kiểm tra exit code và console output.
