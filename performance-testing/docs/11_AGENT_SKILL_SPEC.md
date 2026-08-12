# 11 — AGENT SKILL SPEC

> Nguồn để xây `.agents/skills/performance_testing/`. **10 điểm.**
> Đề §7: *"build an Agent Skill that applies this performance-testing and log-analysis workflow, so that it can be **reused on additional endpoints** in future testing tasks. Submit the skill together with a demonstration video."*

---

## 1. Tiêu chí "tái sử dụng được"

Điểm mấu chốt là chữ **reused on additional endpoints**. Một skill chỉ chạy được đúng workflow Browse-to-buy là **hard-code**, không phải skill.

| Tiêu chí | Cách đạt |
| :--- | :--- |
| Không hard-code endpoint | Workflow mô tả bằng **file config JSON**, skill đọc config để sinh `.jmx` |
| Không hard-code tham số tải | Kịch bản Load/Stress/Spike/Endurance là **profile** trong config |
| Dùng lại được cho thành viên khác | Kèm sẵn config mẫu cho **hai** workflow khác nhau, chứng minh tính tổng quát |
| Phân tích không phụ thuộc workflow | `analyze_jtl.py` gom nhóm theo `label`, không biết gì về ngữ nghĩa endpoint |

**Phép thử:** đưa skill cho bạn Thịnh (workflow Coupon checkout, có bước `apply-coupon`), bạn ấy chỉ cần sửa file JSON, không sửa dòng code nào. Nếu phải sửa code thì skill chưa đạt.

---

## 2. Cấu trúc thư mục

Theo đúng khuôn của skill đã có trong repo (`.agents/skills/domain_and_boundary_testing/`):

```
.agents/skills/performance_testing/
├── SKILL.md
├── scripts/
│   ├── generate_jmx.py        # config JSON -> .jmx
│   ├── analyze_jtl.py         # .jtl -> summary.json + summary.md  (dùng chung với 06_ANALYSIS_SPEC)
│   └── compare_runs.py        # so 2 summary.json, phát hiện regression
├── examples/
│   ├── browse_to_buy_config.json      # workflow của Khoa
│   └── coupon_checkout_config.json    # workflow khác — chứng minh tính tái dùng
└── templates/
    └── report_template.md
```

---

## 3. `SKILL.md`

### 3.1 Frontmatter — bắt buộc, khớp khuôn skill hiện có

```markdown
---
name: Performance Testing and Log Analysis Skill
description: Kỹ năng hỗ trợ thiết kế, sinh và phân tích kiểm thử hiệu năng (Load / Stress / Spike / Endurance) cho các nhóm endpoint REST API bằng Apache JMeter, từ file cấu hình JSON mô tả workflow, kèm phân tích log .jtl và sinh báo cáo.
---
```

### 3.2 Bố cục nội dung

| Mục | Nội dung |
| :--- | :--- |
| **1. Quy trình 6 bước** | §4 dưới đây — phần cốt lõi |
| **2. Cấu trúc file config** | §5 |
| **3. Quy ước đặt tên và thư mục** | `{StudentID}_{ScenarioType}_{YYYYMMDD}`, cây thư mục `results/` |
| **4. Hướng dẫn dùng script** | Lệnh cụ thể cho `generate_jmx.py`, `analyze_jtl.py`, `compare_runs.py` |
| **5. Template báo cáo** | `templates/report_template.md` |
| **6. Hướng dẫn tương tác cho Agent** | §6 dưới đây |
| **7. Cạm bẫy đã biết** | §7 dưới đây — phần giá trị nhất |

---

## 4. Quy trình 6 bước (viết vào `SKILL.md` mục 1)

### Bước 1 — Xác định nhóm endpoint và chốt workflow

- Phân loại từng endpoint vào ba nhóm: **auth-heavy**, **read-heavy**, **transactional**.
- Chọn một chuỗi end-to-end phủ đủ ba nhóm.
- **Kiểm tra ràng buộc loại trừ**: nếu có nhiều người cùng test một hệ thống, xác nhận workflow không trùng. Ghi danh sách endpoint **bị cấm** vào trường `excluded_endpoints` của config.

### Bước 2 — Đọc mã nguồn để tìm đặc thù cài đặt

**Không được bỏ qua bước này.** Tài liệu đặc tả có thể lệch với cài đặt thật.

Cần trả lời:
- Có cơ chế khóa tài khoản / giới hạn tần suất không? Ngưỡng và thời hạn **thật** là bao nhiêu?
- Endpoint nào trả `200` nhưng thực chất không thành công?
- Trạng thái (giỏ hàng, phiên) lưu ở đâu — bộ nhớ tiến trình hay cơ sở dữ liệu?
- Truy vấn nào không có `WHERE`, không có `LIMIT`?
- Có ghi đồng thời vào cùng một tài nguyên không?

Ghi phát hiện vào `sut_characteristics` trong config để các bước sau dùng.

### Bước 3 — Sinh dữ liệu và file CSV

- Ước lượng số tài khoản cần: **≥ số VU cao nhất** trong mọi kịch bản.
- Nếu hệ có khóa tài khoản: mỗi VU **phải** có tài khoản riêng.
- Dữ liệu đọc phải đủ lớn để endpoint danh sách lộ chi phí thật.
- CSV: UTF-8 không BOM, bọc `"` cho trường chứa dấu phẩy, không dòng trống cuối.

### Bước 4 — Sinh test plan từ config

```powershell
python .agents\skills\performance_testing\scripts\generate_jmx.py `
  --config examples\browse_to_buy_config.json `
  --scenario Load `
  --out test-plans\23127207_Load_20260812.jmx
```

Bốn kịch bản dùng **chung một `workflow`**, chỉ khác khối `load_profiles`.

### Bước 5 — Chạy và giám sát

- JMeter **non-GUI** bắt buộc.
- Giám sát tài nguyên tiến trình backend song song, ghi ra CSV.
- Reset trạng thái (khóa tài khoản, dữ liệu) trước mỗi lần chạy, **ghi lại timestamp**.
- Thu: raw `.jtl`, HTML dashboard, CSV tài nguyên, ảnh chụp màn hình.

### Bước 6 — Phân tích và báo cáo

```powershell
python .agents\skills\performance_testing\scripts\analyze_jtl.py `
  --jtl results\load\run.jtl --out-dir results\load --slice-sec 60
```

- **Bắt buộc đối chiếu** `summary.json` với HTML dashboard của JMeter trước khi trích dẫn.
- Cắt lát thời gian để tìm điểm gãy và độ trôi.
- Sinh báo cáo từ `templates/report_template.md`.

---

## 5. Cấu trúc file config

### 5.1 `examples/browse_to_buy_config.json`

```json
{
  "meta": {
    "student_id": "23127207",
    "workflow_name": "browse_to_buy",
    "description": "Login -> duyệt toàn bộ catalog -> xem chi tiết -> thêm giỏ -> thanh toán",
    "excluded_endpoints": [
      "/api/products?search=",
      "/api/categories",
      "/api/apply-coupon",
      "/api/orders/my-orders"
    ]
  },

  "target": {
    "protocol": "http",
    "host": "localhost",
    "port": 3000
  },

  "sut_characteristics": {
    "auth_lockout": {
      "enabled": true,
      "spec_threshold": 3,
      "actual_threshold": 2,
      "spec_duration_sec": 30,
      "actual_duration_sec": 180,
      "source": "backend/server.js:54,57",
      "note": "Bộ đếm tăng 2 mỗi lần sai -> khóa sau 2 lần. Cần tài khoản riêng cho mỗi VU."
    },
    "returns_200_on_missing": ["/api/products/{id}"],
    "in_memory_state": ["userCarts (server.js:14) — không bao giờ giải phóng"],
    "unbounded_queries": ["SELECT * FROM products (server.js:153)"]
  },

  "data": {
    "csv_file": "khoa_users.csv",
    "columns": ["email","password","product_id","quantity","price","total_amount","shipping_address"],
    "sharing_mode": "All threads",
    "recycle_on_eof": true,
    "stop_thread_on_eof": false,
    "allow_quoted_data": true
  },

  "workflow": [
    {
      "label": "01_Login",
      "group": "auth-heavy",
      "method": "POST",
      "path": "/api/login",
      "body": "{\"email\":\"${email}\",\"password\":\"${password}\"}",
      "extract": [
        { "var": "token",   "jsonpath": "$.token",   "default": "TOKEN_NOT_FOUND" },
        { "var": "user_id", "jsonpath": "$.user.id", "default": "-1" }
      ],
      "assertions": [
        { "type": "response_code", "value": "200" },
        { "type": "jsonpath_exists", "value": "$.token" }
      ],
      "think_time_ms": { "base": 1000, "random": 1000 }
    },
    {
      "label": "02_BrowseProducts",
      "group": "read-heavy",
      "method": "GET",
      "path": "/api/products",
      "extract": [
        { "var": "pid", "jsonpath": "$..id", "match_no": 0, "default": "${product_id}" }
      ],
      "assertions": [
        { "type": "response_code", "value": "200" },
        { "type": "regex_matches", "value": "^\\s*\\[[\\s\\S]*\\]\\s*$" }
      ],
      "think_time_ms": { "base": 2000, "random": 2000 }
    },
    {
      "label": "03_ProductDetail",
      "group": "read-heavy",
      "method": "GET",
      "path": "/api/products/${pid}",
      "assertions": [
        { "type": "response_code", "value": "200" },
        { "type": "jsonpath_exists", "value": "$.name" },
        { "type": "jsonpath_exists", "value": "$.price" }
      ],
      "think_time_ms": { "base": 1000, "random": 1000 }
    },
    {
      "label": "04_AddToCart",
      "group": "transactional",
      "method": "POST",
      "path": "/api/cart",
      "headers": { "Authorization": "Bearer ${token}" },
      "body": "{\"product_id\":${pid},\"quantity\":${quantity},\"name\":\"PERF item ${pid}\",\"price\":${price}}",
      "assertions": [
        { "type": "response_code", "value": "200" },
        { "type": "contains", "value": "Added to cart" }
      ],
      "think_time_ms": { "base": 1000, "random": 500 }
    },
    {
      "label": "05_Checkout",
      "group": "transactional",
      "method": "POST",
      "path": "/api/checkout",
      "headers": { "Authorization": "Bearer ${token}" },
      "body": "{\"total_amount\":${total_amount},\"shipping_address\":\"${shipping_address}\"}",
      "extract": [
        { "var": "order_id", "jsonpath": "$.orderId", "default": "-1" }
      ],
      "assertions": [
        { "type": "response_code", "value": "200" },
        { "type": "jsonpath_exists", "value": "$.orderId" }
      ],
      "think_time_ms": null
    }
  ],

  "load_profiles": {
    "Load": {
      "listener": "AggregateReport",
      "thread_groups": [
        { "name": "TG_Load_50VU", "threads": 50, "ramp_up_sec": 60, "duration_sec": 300, "startup_delay_sec": 0 }
      ]
    },
    "Stress": {
      "listener": "SummaryReport",
      "thread_groups": [
        { "name": "TG_Stress_Step1_25VU",  "threads": 25,  "ramp_up_sec": 30, "duration_sec": 480, "startup_delay_sec": 0   },
        { "name": "TG_Stress_Step2_25VU",  "threads": 25,  "ramp_up_sec": 30, "duration_sec": 360, "startup_delay_sec": 120 },
        { "name": "TG_Stress_Step3_50VU",  "threads": 50,  "ramp_up_sec": 30, "duration_sec": 240, "startup_delay_sec": 240 },
        { "name": "TG_Stress_Step4_100VU", "threads": 100, "ramp_up_sec": 30, "duration_sec": 120, "startup_delay_sec": 360 }
      ]
    },
    "Spike": {
      "listener": "ViewResultsTree",
      "listener_options": { "errors_only": true },
      "thread_groups": [
        { "name": "TG_Spike_Baseline_10VU", "threads": 10,  "ramp_up_sec": 30, "duration_sec": 360, "startup_delay_sec": 0   },
        { "name": "TG_Spike_Burst1_300VU",  "threads": 300, "ramp_up_sec": 5,  "duration_sec": 30,  "startup_delay_sec": 60  },
        { "name": "TG_Spike_Burst2_300VU",  "threads": 300, "ramp_up_sec": 5,  "duration_sec": 30,  "startup_delay_sec": 240 }
      ]
    },
    "Endurance": {
      "listener": "AggregateReport",
      "thread_groups": [
        { "name": "TG_Endurance_30VU", "threads": 30, "ramp_up_sec": 60, "duration_sec": 720, "startup_delay_sec": 0 }
      ]
    }
  }
}
```

### 5.2 `examples/coupon_checkout_config.json` — chứng minh tính tái dùng

Cùng schema, khác `workflow`: 6 bước có thêm `05_ApplyCoupon` (`POST /api/apply-coupon`) chèn giữa cart và checkout, và `excluded_endpoints` liệt kê những endpoint thuộc người khác.

Đây là **bằng chứng thuyết phục nhất** cho phần chấm điểm skill: cùng một script, hai workflow khác nhau, không sửa dòng code nào.

> Trong `SKILL.md` ghi rõ: *"Để áp dụng cho một nhóm endpoint mới, chỉ cần tạo một file config theo schema ở mục 2; không cần sửa script."*

---

## 6. `generate_jmx.py`

| Mục | Yêu cầu |
| :--- | :--- |
| Đầu vào | `--config <json>`, `--scenario <Load\|Stress\|Spike\|Endurance>`, `--out <path.jmx>` |
| Đầu ra | File `.jmx` hợp lệ JMeter 5.6.3, mở được bằng GUI |
| Thư viện | Chỉ standard library (`json`, `xml.etree.ElementTree` hoặc dựng chuỗi từ template) |
| Ràng buộc | **Chỉ dùng element JMeter core**, không plugin bên thứ ba |
| Kiểm tra scope | Nếu `path` của bất kỳ bước nào khớp một mục trong `meta.excluded_endpoints` → **báo lỗi và dừng**, không sinh file |
| Ánh xạ element | `assertions[].type` → `response_code`: ResponseAssertion trên Response Code · `contains`: ResponseAssertion trên Text Response · `regex_matches`: ResponseAssertion chế độ Matches · `jsonpath_exists`: JSONPathAssertion |
| Nhiều Thread Group | Khi `load_profiles[scenario].thread_groups` có > 1 phần tử, sinh **Test Fragment + Module Controller** để 5 sampler chỉ định nghĩa một lần |

Kiểm tra scope tự động ở dòng "Ràng buộc" là tính năng đáng giá nhất của skill này: nó biến ràng buộc tổ chức (không trùng workflow trong nhóm) thành một **cổng kiểm tra máy chạy được**, thay vì trông chờ vào trí nhớ con người.

---

## 7. Mục 7 của `SKILL.md` — Cạm bẫy đã biết

Đây là phần chuyển kinh nghiệm HW05 thành tri thức tái dùng. Viết dạng bảng:

| Cạm bẫy | Dấu hiệu | Cách tránh |
| :--- | :--- | :--- |
| CSV `Sharing mode` sai | Nhiều thread cùng dùng một tài khoản → khóa dây chuyền, `403` hàng loạt | Luôn đặt `All threads` |
| Think time = 0 | RPS cao bất thường, Load test thực chất là stress test | Luôn có Uniform Random Timer mỗi bước |
| Assert chỉ status code | Test xanh trong khi dữ liệu rỗng | Assert cả nội dung response |
| Tin spec thay vì code | Ngưỡng khóa, mã lỗi, quy tắc nghiệp vụ lệch thực tế | Bước 2 của quy trình là bắt buộc |
| Nhầm `Latency` với response time | Kết luận sai về nút thắt cổ chai | `elapsed` mới là response time; `elapsed − Latency` là chi phí truyền payload |
| Trần bộ nhớ đọc từ WorkingSet | Số dao động theo áp lực bộ nhớ toàn hệ thống | Dùng `PrivateMemorySize64` |
| Thread Group xếp chồng đọc sai | Báo "bậc cuối 100 VU" trong khi thực tế 200 | Đọc `max(allThreads)` từ `.jtl`, không suy từ cấu hình |
| Chạy JMeter chế độ GUI ở tải cao | Chính công cụ đo thành nút cổ chai | Luôn `-n` |
| Không reset trạng thái giữa các run | Rác của run trước làm sai lệch run sau | Reset + ghi timestamp |
| Percentile tính bằng nội suy | Lệch với HTML dashboard vài ms, phá vỡ luận điểm đối chiếu | Dùng nearest-rank |

---

## 8. Video demo skill — NGƯỜI thực hiện

Đề §7: *"Submit the skill together with a demonstration video (YouTube link) that shows, **end to end**, how you used the skill on a complete endpoint group."*

Video riêng, khác video ở `05_EXECUTION_RUNBOOK.md` §7. Độ dài khuyến nghị **4–6 phút**.

| Đoạn | Nội dung |
| :--- | :--- |
| 1 | Mở `SKILL.md`, giới thiệu quy trình 6 bước |
| 2 | Mở `browse_to_buy_config.json`, giải thích schema — nhấn vào `sut_characteristics` và `excluded_endpoints` |
| 3 | Chạy `generate_jmx.py`, mở file `.jmx` vừa sinh bằng JMeter GUI để chứng minh nó hợp lệ |
| 4 | **Chứng minh tính tái dùng:** mở `coupon_checkout_config.json`, chạy lại **cùng script**, sinh ra `.jmx` cho workflow khác. Nhấn mạnh: *"không sửa một dòng code nào"* |
| 5 | **Chứng minh cổng kiểm tra scope:** cố tình thêm `/api/products?search=` vào một workflow rồi chạy script → script báo lỗi và từ chối sinh file |
| 6 | Chạy `analyze_jtl.py` trên một `.jtl` có sẵn, mở `summary.md` |

Đoạn 4 và 5 là hai đoạn ăn điểm. Đừng bỏ.

---

## 9. Checklist

- [ ] `SKILL.md` có frontmatter `name` + `description`, khớp khuôn skill đã có trong repo
- [ ] Quy trình 6 bước đầy đủ, bước 2 (đọc mã nguồn) được nêu là **bắt buộc**
- [ ] `generate_jmx.py` sinh được `.jmx` mở bằng JMeter GUI không lỗi
- [ ] `generate_jmx.py` **từ chối** sinh file khi workflow chạm `excluded_endpoints`
- [ ] Có **hai** file config mẫu cho **hai** workflow khác nhau
- [ ] Chứng minh được: đổi config, không đổi code, ra `.jmx` mới
- [ ] `analyze_jtl.py` dùng chung với `06_ANALYSIS_SPEC.md`, không viết trùng
- [ ] Có mục "Cạm bẫy đã biết" ≥ 8 dòng
- [ ] Video demo có đoạn 4 (tái dùng) và đoạn 5 (cổng kiểm tra scope)
- [ ] Link video dán vào `performance-testing/README.md`
- [ ] Commit: `feat(skill): add performance_testing agent skill`
