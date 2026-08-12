# 07 — HUMAN REVIEW TEMPLATE

> Khung cho `deliverables/03_human-review-fixes.md`.
> Đề §6 Task 1: *"Critically review the AI-generated test plans and correct them. Report what the AI got wrong or missed — and explain **why** it missed them (prompt quality, model limitations, or characteristics of the endpoint). You are fully responsible for the final test plans."*

---

## 1. Cách chấm phần này

Người chấm tìm ba thứ:

1. **Cụ thể** — chỉ ra được element/tham số nào sai, không nói chung chung "AI thiếu chi tiết".
2. **Có bằng chứng** — dẫn được dòng code SUT hoặc số liệu chứng minh cái sai.
3. **Giải thích được `why`** — đây là phần dễ mất điểm nhất. Phải quy được nguyên nhân về **một trong ba nhóm** mà đề nêu:

| Nhóm nguyên nhân | Nghĩa là gì |
| :--- | :--- |
| **Prompt quality** | Mình hỏi thiếu ngữ cảnh, AI không thể biết |
| **Model limitations** | AI có đủ ngữ cảnh nhưng vẫn suy luận sai, hoặc bịa |
| **Endpoint characteristics** | Đặc thù của SUT trái với quy ước phổ biến, nên "kiến thức chung" của AI phản tác dụng |

> Nhóm thứ ba là nhóm đáng giá nhất. Nó cho thấy mình hiểu **vì sao** kiến thức tổng quát lại sai trên hệ thống cụ thể này.

---

## 2. Bảng chính — dán vào `03_human-review-fixes.md`

| # | AI đề xuất | Sai ở đâu | Bằng chứng | Mình sửa thành | Vì sao AI sai |
| :--: | :--- | :--- | :--- | :--- | :--- |
| 1 | ... | ... | ... | ... | ... |

Dưới đây là **6 mục đã biết chắc sẽ xảy ra** trên SUT này, kèm luận cứ viết sẵn. Khi chạy phiên sinh test plan bằng AI (`08_AI_ANALYSIS_PROMPTS.md` §2), đối chiếu output thật với 6 mục này — cái nào AI mắc thì giữ, cái nào không mắc thì **xóa đi**, và bổ sung lỗi mới nếu có.

> ⚠️ **Không copy nguyên 6 mục nếu AI không thực sự mắc.** Báo cáo phải phản ánh phiên làm việc thật. Nếu AI chỉ mắc 3/6, viết 3 và nói rõ "AI không mắc lỗi X vì prompt bước N đã cung cấp ngữ cảnh Y" — điều đó còn ghi điểm hơn.

---

### Mục 1 — Lockout: AI tin spec, không tin code

| Mục | Nội dung |
| :--- | :--- |
| **AI đề xuất** | "Sau 3 lần đăng nhập sai, tài khoản bị khóa 30 giây. Test plan nên chờ 30 giây rồi thử lại." |
| **Sai ở đâu** | Cả hai con số đều sai so với hệ thống thật |
| **Bằng chứng** | `backend/server.js:54` → `const newAttempts = user.login_attempts + 2;` — bộ đếm tăng **2**, nên **2 lần sai** đã đạt ngưỡng `>= 3`.<br>`backend/server.js:57` → `new Date(Date.now() + 180000)` — khóa **180 giây**, không phải 30 |
| **Mình sửa thành** | Thiết kế theo hành vi thật: coi ngưỡng khóa là **2 lần sai**, thời hạn **180 s**. Nghỉ ≥ 3 phút giữa các run và chạy `reset_lockout.js` trước mỗi run (`05_EXECUTION_RUNBOOK.md` §4) |
| **Vì sao AI sai** | **Endpoint characteristics.** `README.md` (bản đặc tả yêu cầu) ghi "3 lần / 30 giây", và AI ưu tiên tài liệu đặc tả — đó là hành vi hợp lý trong đa số dự án. Nhưng SUT này **cố ý** cài đặt lệch spec để sinh viên tìm bug. AI không có cách nào biết điều đó nếu không được yêu cầu đọc `server.js`. Đây là bài học: **khi test một hệ thống có bug cố ý, spec là giả thuyết chứ không phải sự thật** |

---

### Mục 2 — Think time bằng 0 / ramp-up quá nhanh

| Mục | Nội dung |
| :--- | :--- |
| **AI đề xuất** | Thread Group `50 threads, ramp-up 1s`, không có Timer nào |
| **Sai ở đâu** | Không có think time thì 50 VU sẽ bắn request liên tục hết công suất — đó là **stress test**, không phải load test. Ramp-up 1 s trộn chi phí khởi tạo thread vào số đo |
| **Bằng chứng** | Không cần bằng chứng từ SUT; đây là sai về **phương pháp**. Hệ quả đo được: nếu chạy không timer, RPS vọt lên gấp nhiều lần mức người dùng thật sinh ra, và p95 phản ánh giới hạn công cụ chứ không phải trải nghiệm người dùng |
| **Mình sửa thành** | Uniform Random Timer trong từng sampler: 1–2 / **2–4** / 1–2 / 1 s (`03_TEST_DESIGN.md` §1.2). Ramp-up 60 s cho Load. Riêng Spike **cố ý** giữ ramp-up 5 s vì đó là bản chất của kịch bản sốc |
| **Vì sao AI sai** | **Prompt quality.** Prompt đầu chỉ nói "tạo test plan JMeter cho workflow này với 50 VU" mà không mô tả **hồ sơ người dùng**. AI mặc định tối đa hóa thông lượng vì đó là dạng ví dụ phổ biến nhất trên mạng. Sau khi bổ sung prompt "mô phỏng người dùng thật đang duyệt catalog, ước lượng think time từng bước", AI đưa ra khoảng hợp lý |

---

### Mục 3 — Assertion chỉ kiểm status code

| Mục | Nội dung |
| :--- | :--- |
| **AI đề xuất** | Mỗi sampler một Response Assertion: `Response Code Equals 200` |
| **Sai ở đâu** | Trên SUT này, `200` **không** đảm bảo request thành công |
| **Bằng chứng** | `backend/server.js:161` → `if (!row) return res.status(200).json({});` — id không tồn tại vẫn trả `200` với body rỗng. Nếu JSON Extractor `$..id` ở bước 2 lỗi và `pid` rơi về giá trị mặc định không hợp lệ, bước 3 vẫn "xanh" trong khi thực chất không lấy được sản phẩm nào |
| **Mình sửa thành** | Thêm JSON Assertion kiểm `$.name` và `$.price` tồn tại ở bước 3; Response Assertion regex `^\s*\[[\s\S]*\]\s*$` ở bước 2 để chắc chắn body là array; Contains `Added to cart` ở bước 4; JSON Assertion `$.orderId` ở bước 5 |
| **Vì sao AI sai** | **Endpoint characteristics.** Quy ước REST chuẩn là `404` cho tài nguyên không tồn tại, nên AI giả định đúng theo chuẩn. SUT vi phạm chuẩn một cách cố ý. AI chỉ phát hiện được nếu prompt yêu cầu nó đọc mã nguồn của endpoint |

---

### Mục 4 — CSV Data Set Config sai `Sharing mode`

| Mục | Nội dung |
| :--- | :--- |
| **AI đề xuất** | CSV Data Set Config với `Sharing mode = Current thread group` (hoặc bỏ trống, JMeter mặc định `All threads` nhưng AI ghi rõ giá trị khác), `Recycle on EOF = false` |
| **Sai ở đâu** | `Current thread` / `Current thread group` khiến **mỗi thread đọc lại file từ đầu** → hàng trăm thread cùng đăng nhập bằng `khoa001@eshop.com`.<br>`Recycle = false` + test chạy theo thời lượng → hết 400 dòng là thread bắt đầu nhận giá trị rỗng, tải sụt giữa chừng |
| **Bằng chứng** | Hậu quả đo được: tỉ lệ `403` ở `01_Login` tăng vọt, và trong `.jtl` mọi `threadName` khác nhau lại cùng một email. Kiểm bằng:<br>`Import-Csv <jtl> \| Where-Object label -eq '01_Login' \| Group-Object responseCode` |
| **Mình sửa thành** | `Sharing mode = All threads`, `Recycle on EOF = true`, `Stop thread on EOF = false`, `Allow quoted data = true` (`04_JMX_BUILD_SPEC.md` §2) |
| **Vì sao AI sai** | **Model limitations.** Đây là chi tiết cấu hình tinh vi của JMeter mà hậu quả chỉ lộ ra khi chạy ở tải cao **và** khi backend có cơ chế khóa tài khoản. AI biết từng mảnh kiến thức riêng lẻ nhưng không tự nối được chuỗi nhân quả "sharing mode → trùng credential → lockout → hỏng số đo". Con người phát hiện được vì đã đọc `server.js:40-44` và biết trước hậu quả |

---

### Mục 5 — Bỏ sót đặc tính giỏ hàng in-memory

| Mục | Nội dung |
| :--- | :--- |
| **AI đề xuất** | "Chạy soak test 15 phút để kiểm tra tính ổn định." Không đề cập theo dõi bộ nhớ, không giải thích tại sao soak lại quan trọng với SUT này |
| **Sai ở đâu** | Thiếu chứ không sai. Nhưng bỏ sót đúng thứ khiến kịch bản endurance có ý nghĩa trên hệ thống này |
| **Bằng chứng** | `backend/server.js:14` → `const userCarts = {};`<br>`:293` → `userCarts[userId].push(req.body);` — chỉ thêm, không bao giờ xóa<br>`:297-309` — `/api/checkout` ghi đơn hàng vào DB nhưng **không** dọn `userCarts[userId]`<br>→ Mỗi iteration của mỗi VU thêm vĩnh viễn một phần tử vào heap |
| **Mình sửa thành** | Bổ sung `monitor_backend.ps1` lấy mẫu `PrivateMemorySize64` mỗi 2 s, và đưa "trần bộ nhớ + tốc độ tăng MB/phút" thành **kết quả bắt buộc** của kịch bản Endurance (`06_ANALYSIS_SPEC.md` §6.2) |
| **Vì sao AI sai** | **Prompt quality.** Prompt chỉ mô tả workflow theo góc nhìn HTTP (endpoint, payload, assertion) mà không cung cấp mã nguồn xử lý. AI không thể suy ra trạng thái lưu ở đâu chỉ từ mô tả API. Sau khi bổ sung prompt "đây là mã nguồn `/api/cart` và `/api/checkout`, hãy chỉ ra rủi ro hiệu năng", AI phát hiện ngay |

---

### Mục 6 — Tự ý thêm `?search=` vào bước duyệt sản phẩm

| Mục | Nội dung |
| :--- | :--- |
| **AI đề xuất** | Bước 2 là `GET /api/products?search=${keyword}` kèm một cột `search` trong CSV |
| **Sai ở đâu** | **Vi phạm phân chia scope của nhóm.** Endpoint search thuộc về Trâm, Nguyên và Thịnh. Workflow của mình là **Browse-to-buy**, bước 2 phải là `GET /api/products` trần |
| **Bằng chứng** | `00_GROUP_SCOPE.md` §3 (ma trận endpoint) và §4.2. Đề §5 yêu cầu *"no two members may test the same workflow"* |
| **Mình sửa thành** | Xóa query string; bước 2 gọi `/api/products` không tham số. Bổ sung kiểm tra tự động trước khi commit:<br>`Select-String -Path "test-plans\*.jmx" -Pattern "search=\|apply-coupon\|my-orders"` phải rỗng |
| **Vì sao AI sai** | **Prompt quality** kết hợp **model limitations.** Ràng buộc "không trùng workflow với thành viên khác" là **ngữ cảnh tổ chức**, không nằm trong mã nguồn hay tài liệu API — AI không thể biết nếu không được nói. Đồng thời, "search rồi mua" là mẫu e-commerce phổ biến hơn nhiều so với "duyệt toàn bộ rồi mua", nên xu hướng của mô hình kéo về mẫu quen thuộc ngay cả khi đã được dặn. Bài học: **ràng buộc âm (đừng làm X) phải được nhắc lại ở mỗi bước, không chỉ nói một lần ở đầu phiên** |

---

## 3. Phần "Nhận trách nhiệm" — bắt buộc

Đề ghi rõ: *"You are fully responsible for the final test plans."* Kết `03_human-review-fixes.md` bằng một đoạn như sau (viết lại bằng lời của mình, đừng chép nguyên):

> Tôi đã tự tay kiểm tra lại toàn bộ 4 test plan sau khi AI sinh bản đầu. Cụ thể, tôi mở từng `.jmx` bằng JMeter GUI, chạy thử ở chế độ 1 thread × 1 loop và xác nhận cả 5 sampler trả về đúng dữ liệu mong đợi trước khi chạy tải thật (`04_JMX_BUILD_SPEC.md` §9.4). Tôi đã đối chiếu từng giả định của AI với mã nguồn `backend/server.js` và sửa `<<N>>` điểm nêu ở bảng trên. Mọi tham số tải, think time và assertion trong bản cuối là lựa chọn của tôi và tôi chịu trách nhiệm về tính đúng đắn của chúng.

Thay `<<N>>` bằng số mục thật sự đã sửa.

---

## 4. Bảng phân loại nguyên nhân — thêm vào cuối báo cáo

Giúp người chấm thấy mình đã suy nghĩ có hệ thống chứ không liệt kê rời rạc:

| Nhóm nguyên nhân | Số lỗi | Các mục | Rút ra được gì |
| :--- | :---: | :--- | :--- |
| Prompt quality | `<<FILL>>` | `<<FILL>>` | Thiếu ngữ cảnh nào thì AI sai kiểu nào — và ngữ cảnh đó lẽ ra phải cung cấp ở bước prompt nào |
| Model limitations | `<<FILL>>` | `<<FILL>>` | AI biết từng mảnh kiến thức nhưng không tự nối chuỗi nhân quả nhiều bước |
| Endpoint characteristics | `<<FILL>>` | `<<FILL>>` | Khi hệ thống lệch chuẩn, "kiến thức chung" của AI trở thành nguồn lỗi thay vì nguồn trợ giúp |

---

## 5. Checklist

- [ ] Chỉ giữ lại những mục AI **thực sự** mắc trong phiên làm việc thật
- [ ] Mỗi mục có đủ 5 cột: đề xuất / sai ở đâu / bằng chứng / sửa thành / vì sao
- [ ] Mỗi "bằng chứng" dẫn được **dòng code cụ thể** hoặc **số liệu từ `.jtl`**
- [ ] Mỗi "vì sao" quy về **một trong ba nhóm** nguyên nhân đề nêu
- [ ] Có bảng phân loại nguyên nhân §4
- [ ] Có đoạn nhận trách nhiệm §3, viết bằng lời của mình
- [ ] Nếu AI **không** mắc lỗi nào đó trong danh sách, ghi rõ vì sao nó tránh được
