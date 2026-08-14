# 07 — Continuous Performance Testing Proposal (Task 3)

> **Học phần:** Kiểm thử Phần mềm (HW05)  
> **Nhiệm vụ:** Task 3 — Đề xuất Mô hình Kiểm thử Hiệu năng Liên tục (Continuous Performance Testing - CPT)  
> **Sinh viên:** Khoa (MSSV: **23127207**) · **SUT:** EShop  
> **Mục tiêu năng lực:** Bloom-AI **G9.6 (Disrupt)**  

---

## 1. Vấn đề của Kiểm thử Hiệu năng Thủ công

Kiểm thử hiệu năng định kỳ thủ công như HW05 có 3 hạn chế lớn:
1. **Chạy đơn lẻ (Point-in-time):** Kết quả chỉ có giá trị tại thời điểm đo. Một commit mới sửa logic route có thể làm suy giảm p95 mà không ai biết.
2. **Chi phí thời gian lớn (~40 phút chạy + nhiều giờ phân tích):** Đội ngũ kỹ thuật không thể lặp lại quy trình này thường xuyên.
3. **Phát hiện muộn:** Lỗi hiệu năng (regression) chỉ được phát hiện khi đã lên môi trường Production, làm chi phí khắc phục tăng gấp 10–50 lần.

**Mục tiêu của đề xuất:** Tự động giám sát commit, kích hoạt kiểm thử hiệu năng có chọn lọc, bắt regression p95 trong vòng **15 phút** với chi phí CI thấp và tỉ lệ báo động giả (false alarms) dưới kiểm soát.

---

## 2. Ba Nguyên tắc Cốt lõi của Mô hình

1. **Không chạy kiểm thử trên mọi commit:** Chỉ kích hoạt khi thay đổi thực sự chạm vào mã nguồn backend (`backend/**`, queries, middleware, config). Sửa docs hoặc CSS không thể làm chậm API.
2. **So sánh Tương đối so với Baseline (Relative Delta):** Runner CI đám mây (GitHub Actions) dùng chung CPU, hiệu năng biến thiên 15–30%. Ngưỡng tuyệt đối (ví dụ `p95 < 500ms`) sẽ tạo báo động giả liên tục. Đo `delta_p95 = (p95_current / p95_baseline) - 1` trên cùng loại runner loại bỏ được nhiễu phần cứng nền.
3. **Chặn Merge chỉ khi Bằng chứng Đủ mạnh:** Một lần chạy chậm có thể do máy chủ CI bận. Mô hình sử dụng **Median của 3 lần chạy lặp lại** (3 runs median) trước khi kết luận và chặn PR.

---

## 3. Quy trình Thực thi (Flowchart)

```mermaid
flowchart TD
    A[Commit / Pull Request] --> B{Thay đổi có thuộc<br/>backend/** ?}
    B -- Không --> Z1[Bỏ qua CI Perf<br/>Log: perf-skip: path]
    B -- Có --> C{Có nhãn [skip perf]<br/>hoặc perf-skip ?}
    C -- Có --> Z2[Bỏ qua CI Perf<br/>Log: perf-skip: manual]
    C -- Không --> D{Phân loại thay đổi}

    D -- "Chỉ docs / comment" --> Z3[Bỏ qua]
    D -- "Route / SQL / Middleware" --> E[Khởi tạo môi trường CI]

    E --> F[Seed dữ liệu chuẩn:<br/>400 users, 505 products]
    F --> G[Chạy Smoke JMeter 15 VU x 2 phút<br/>Workflow Browse-to-buy 5 bước]
    G --> H[analyze_jtl.py -> summary.json]

    H --> I{Số lần lặp lại?}
    I -- "< 3" --> G
    I -- "= 3" --> J[Lấy MEDIAN p95 của 3 lần<br/>theo từng Label]

    J --> K[Đọc baseline.json từ nhánh main]
    K --> L{delta_p95 = p95_test / p95_baseline - 1}

    L -- "delta <= +10%" --> M[PASS: Báo cáo xanh]
    L -- "+10% < delta <= +20%" --> N[WARN: Comment cảnh báo vào PR<br/>Không chặn merge]
    L -- "delta > +20% HOẶC Err > 1%" --> O[FAIL: Chặn Merge<br/>Post bảng so sánh chi tiết]

    M --> P{Nhánh hiện tại là main?}
    P -- Có --> Q[Tự động cập nhật baseline.json]
    P -- Không --> R[Kết thúc]
    N --> R
    O --> R
    Q --> R

    S[Nightly Cron 02:00] --> T[Chạy bộ 4 kịch bản đầy đủ:<br/>Load + Stress + Spike + Endurance]
    T --> U[Lưu trữ Dashboard & Trend 30 ngày]
    U --> V{Xu hướng xấu dần > 15% / 7 ngày?}
    V -- Có --> W[Tự động tạo GitHub Issue giao Dev Backend]
    V -- Không --> X[Kết thúc]
```

---

## 4. Kiến trúc 4 Tầng Giám sát (T1 - T4)

| Tầng | Thời điểm kích hoạt | Thời lượng | Mô hình tải | Mục đích chính |
|:---|:---|:---:|:---|:---|
| **T1 — Filter Gate** | Mọi commit / push | < 5 giây | — | Lọc nhanh đường dẫn thay đổi bằng Git diff |
| **T2 — Smoke Perf Gate** | Pull Request vào `main` | ~8 phút | 15 VU $\times$ 2 phút $\times$ 3 lần lặp | Bắt regression thuật toán và n+1 query trước merge |
| **T3 — Nightly Full Suite** | Cron `02:00` hàng ngày | ~40 phút | Đầy đủ Load (50VU), Stress (200VU), Spike, Soak | Cập nhật baseline chuẩn, theo dõi suy thoái dài hạn |
| **T4 — Release Gate** | Gắn Release Tag (vX.Y) | ~90 phút | Full Suite + Soak 60 phút | Đánh giá tổng thể trước khi đưa lên Production |

---

## 5. Phân tích Đánh đổi (Trade-offs)

### 5.1 Đánh đổi về Chi phí Hạ tầng (Cost Analysis)
- **Thời lượng CI hàng tháng:**
  - T2 Smoke PRs: 8 phút $\times$ ~15 PRs/tuần = ~2 giờ CI/tuần (~8 giờ/tháng).
  - T3 Nightly: 40 phút $\times$ 30 ngày = ~20 giờ CI/tháng.
  - T4 Release: ~2 giờ/tháng.
  - **Tổng cộng:** ~30 giờ runner CI mỗi tháng (hoàn toàn nằm trong hạn mức miễn phí của GitHub Actions cho public/private repo).
- **Chi phí Lưu trữ & Dữ liệu:** File `.jtl` và HTML dashboard sinh ra ~50MB mỗi lần chạy đầy đủ. Thiết lập chính sách lưu trữ: lưu raw `.jtl` trong 14 ngày, chỉ giữ file `summary.json` vĩnh viễn trong kho lịch sử.

### 5.2 Kiểm soát và Giảm thiểu Báo động Giả (False Alarms Mitigation)
1. **Runner chia sẻ tài nguyên (Noisy Neighbors):** Đây là nguyên nhân lớn nhất gây lệch số đo. Mô hình giải quyết bằng cách lấy **Median của 3 lần lặp** và đặt ngưỡng chặn `FAIL` ở mức **`+20%`**.
2. **Khởi động nguội (Cold Start / JIT Warmup):** Bỏ qua 30 giây đầu tiên của mỗi run 2 phút để Node.js V8 JIT compiler tối ưu hóa bytecode và cache bộ nhớ ổn định.
3. **Tính nhất quán của Dữ liệu:** Database luôn được reset và seed cố định 400 user + 505 product bằng script tự động trước khi đo.
4. **Chỉ số Sức khỏe CPT:** Theo dõi tỉ lệ cảnh báo đúng (True Positive Rate). Nếu tỉ lệ cảnh báo được dev xác nhận là regression thực tế tụt dưới 50%, hệ thống tự động nới lỏng ngưỡng `WARN/FAIL` để tránh tình trạng "báo động quá nhiều dẫn đến bị phớt lờ".
