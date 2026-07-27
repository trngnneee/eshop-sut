# Hồ sơ nghiên cứu nhóm Developer-centric và Orchestration

**Mốc thông tin:** 2026-07-14 (Asia/Bangkok)  
**Phạm vi:** k6, Locust, Gatling, Artillery và Taurus  
**Đối tượng minh họa:** EShop có hành trình nhiều bước như đăng nhập → duyệt/tìm sản phẩm → xem chi tiết → thêm giỏ → thanh toán  
**Trạng thái thực nghiệm:** **Chưa chạy công cụ nào trong hồ sơ này.** Mọi lệnh, cấu hình và kết quả mong đợi bên dưới là kế hoạch kiểm chứng, không phải kết quả thực tế.

## 0. Quy ước bằng chứng, an toàn và cách chấm

- **DOC**: thông tin được đối chiếu với tài liệu sản phẩm, kho mã nguồn, trang giấy phép hoặc trang giá chính thức; đường dẫn được đặt ngay sau phát biểu tương ứng.
- **EXP**: kết quả đo hoặc quan sát trực tiếp. Hồ sơ này **không có bằng chứng EXP**; vị trí cần chạy được ghi **[CẦN THỰC NGHIỆM]** hoặc **[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**.
- **ASSUMPTION**: suy luận kỹ thuật, ví dụ mức phù hợp với bài EShop hay khả năng AI hỗ trợ. Đây không phải tuyên bố của nhà cung cấp.
- Chỉ chạy tải trên hệ thống mà nhóm có quyền kiểm thử; khóa URL, tài khoản thử nghiệm, tốc độ và thời lượng trước khi chạy. Không dùng các URL ví dụ công cộng trong tài liệu của nhà cung cấp làm mục tiêu benchmark.
- Điểm 1–5 là **đề xuất của nhóm nghiên cứu**, không phải điểm do nhà cung cấp hay môn học công bố. Công thức: **điểm quy đổi = tổng(điểm tiêu chí / 5 × trọng số)**, thang 0–100.

| # | Tiêu chí | Trọng số |
|---:|---|---:|
| 1 | Cost & access | 8% |
| 2 | Learning curve | 8% |
| 3 | EShop fit | 15% |
| 4 | Multi-step journey | 12% |
| 5 | Workload control | 10% |
| 6 | Assertions/checks | 8% |
| 7 | Reporting | 8% |
| 8 | CI/CD | 7% |
| 9 | Reproducibility | 7% |
| 10 | Local/offline | 5% |
| 11 | AI-assisted potential | 7% |
| 12 | Classroom suitability | 5% |

> **Cảnh báo so sánh:** Taurus là lớp orchestration/abstraction gọi các executor bên dưới. Điểm Taurus mô tả trải nghiệm dùng **Taurus + executor được chọn**; không được đọc như phép đo một load generator độc lập ngang hàng với k6, Locust, Gatling hoặc Artillery.

---

# 1. k6

## 1.1 Tổng quan và maintainer

k6 là công cụ kiểm thử hiệu năng mã nguồn mở do Grafana Labs duy trì, tập trung vào test-as-code, tải ở tầng giao thức và có thêm mô-đun browser để kiểm thử bằng Chromium. Kho chính thức mô tả k6 là công cụ load testing hiện đại, hướng lập trình viên và do Grafana phát triển. **(DOC; [Grafana k6 repository](https://github.com/grafana/k6), truy cập 2026-07-14; [k6 documentation](https://grafana.com/docs/k6/latest/), truy cập 2026-07-14)**

**Phân loại tạm thời:** **Main candidate** cho bài EShop API/backend. Browser VU chỉ nên là lớp bổ sung nhỏ để đo frontend/Web Vitals, không phải cách mặc định để phát toàn bộ tải backend. Việc chọn này là **ASSUMPTION** dựa trên khả năng workload, checks, thresholds, kết quả cục bộ và CI được tài liệu hóa dưới đây.

## 1.2 Giấy phép, chi phí và quyền truy cập

- Kho k6 hiện công bố giấy phép **AGPL-3.0**. Bản CLI mã nguồn mở có thể chạy cục bộ mà không cần tạo tài khoản Grafana Cloud. **(DOC; [k6 repository and license](https://github.com/grafana/k6), truy cập 2026-07-14)**
- Grafana Cloud k6 là dịch vụ tùy chọn. Trang giá hiện có gói Free 0 USD với hạn mức 500 VUh/tháng; các gói trả phí tính theo VUh và mức dịch vụ. Giá/hạn mức là dữ liệu dễ thay đổi, vì vậy phải chụp lại trang giá ở thời điểm nộp bài nếu dùng con số này trong slide. **(DOC; [Grafana pricing](https://grafana.com/pricing/), truy cập 2026-07-14)**
- Hệ quả lớp học: có thể hoàn thành smoke test, version-control script và xuất dữ liệu tại máy mà không phụ thuộc tài khoản cloud; cloud chỉ cần khi muốn phân tán/quản trị tập trung. **(ASSUMPTION, dựa trên DOC về CLI cục bộ và pricing)**

## 1.3 Cài đặt và nền tảng

- Tài liệu chính thức cung cấp gói/cách cài cho Linux, macOS và Windows, binary độc lập, cùng image Docker **grafana/k6**; Windows có installer chính thức, còn một số manifest/package manager được ghi là do cộng đồng duy trì. **(DOC; [Install k6](https://grafana.com/docs/k6/latest/set-up/install-k6/), truy cập 2026-07-14)**
- k6 Studio là ứng dụng desktop cho Windows, macOS và Linux để ghi browser flow/HAR, sinh và debug test; đây là công cụ authoring bổ sung, không bắt buộc để chạy CLI. **(DOC; [k6 Studio](https://grafana.com/docs/k6/latest/k6-studio/), truy cập 2026-07-14)**
- Để tái lập trong lớp, nên pin phiên bản binary hoặc tag image, lưu checksum/lock thông tin image digest, và ghi kết quả của lệnh version. Đây là **ASSUMPTION/thực hành đề xuất**, cần kiểm chứng trên máy lớp học.

## 1.4 Ngôn ngữ script, runtime và cấu hình

- Test k6 viết bằng JavaScript. k6 dùng JavaScript runtime riêng, **không phải Node.js và không phải browser runtime**; do đó không có sẵn Node built-ins và mức tương thích package npm phải được kiểm tra hoặc bundle phù hợp. **(DOC; [Write your first k6 test](https://grafana.com/docs/k6/latest/get-started/write-your-first-test/), truy cập 2026-07-14; [k6 modules](https://grafana.com/docs/k6/latest/using-k6/modules/), truy cập 2026-07-14)**
- Script có thể tách module, dùng biến môi trường, options và scenario; điều này phù hợp với Git review và tái sử dụng journey. **(DOC; [k6 modules](https://grafana.com/docs/k6/latest/using-k6/modules/), truy cập 2026-07-14; [k6 scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/), truy cập 2026-07-14)**
- HAR có thể chuyển thành script bằng **har-to-k6**, nhưng tài liệu yêu cầu chỉnh lại script sinh ra cho correlation, dữ liệu và load profile; browser recorder extension cũ đã bị deprecate và Grafana hướng người dùng sang k6 Studio. **(DOC; [HAR converter](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-har-converter/), truy cập 2026-07-14; [deprecated browser recorder](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-browser-recorder/), truy cập 2026-07-14)**

## 1.5 Workload model và điều khiển tải

- Scenarios hỗ trợ nhiều executor: shared/per-VU iterations, constant/ramping VUs và constant/ramping arrival rate; mỗi scenario có thể có thời điểm bắt đầu, hàm thực thi, biến môi trường và tag riêng. **(DOC; [k6 scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/), truy cập 2026-07-14)**
- Nhờ có cả mô hình VU đóng và arrival-rate mở, nhóm có thể tách browse, cart và checkout thành các population khác nhau thay vì dùng một vòng lặp đồng nhất. **(ASSUMPTION, dựa trên DOC về scenarios/executors)**
- Cần hiệu chuẩn pre-allocated/max VUs cho arrival-rate scenario và theo dõi dropped iterations; nếu không, tải phát ra có thể không đạt target. **(DOC; [k6 executors](https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/), truy cập 2026-07-14)**

## 1.6 Session, cookie, correlation và dữ liệu

- Mỗi VU có cookie jar; cookie từ phản hồi **Set-Cookie** được lưu và tự gửi ở request phù hợp, đồng thời API cho phép thao tác cookie jar riêng. **(DOC; [k6 cookies](https://grafana.com/docs/k6/latest/using-k6/cookies/), truy cập 2026-07-14)**
- Response cho phép đọc body và parse JSON, nên token/ID động có thể được trích rồi truyền vào bước sau. **(DOC; [k6 HTTP Response](https://grafana.com/docs/k6/latest/javascript-api/k6-http/response/), truy cập 2026-07-14; [Response.json](https://grafana.com/docs/k6/latest/javascript-api/k6-http/response/response-json/), truy cập 2026-07-14)**
- Dữ liệu có thể parameterize bằng biến, JSON và **SharedArray**, giúp tránh mỗi VU nạp lại toàn bộ bộ dữ liệu. **(DOC; [Data parameterization](https://grafana.com/docs/k6/latest/examples/data-parameterization/), truy cập 2026-07-14)**
- Với EShop phải kiểm tra thực tế CSRF, access/refresh token, product ID, cart ID, order ID, dữ liệu người dùng duy nhất và cleanup. **[CẦN THỰC NGHIỆM]**

## 1.7 Assertions/checks và tiêu chí pass/fail

- **Checks** đánh giá điều kiện Boolean như status/body và tạo metric rate. Check thất bại **không tự dừng test và không tự làm process thất bại**; muốn gate CI phải đặt threshold trên metric checks hoặc metric liên quan. **(DOC; [k6 checks](https://grafana.com/docs/k6/latest/using-k6/checks/), truy cập 2026-07-14)**
- **Thresholds** là tiêu chí pass/fail cho trend/rate/counter/gauge, hỗ trợ percentile tùy chọn và **abortOnFail**; threshold thất bại làm k6 trả mã thoát khác 0. **(DOC; [k6 thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/), truy cập 2026-07-14)**
- Khuyến nghị EShop: check nghiệp vụ ở từng bước và threshold tối thiểu cho **checks**, **http_req_failed**, p95/p99 theo endpoint/tag. Đây là **ASSUMPTION/thiết kế đề xuất**, ngưỡng số cụ thể phải lấy từ SLO hoặc baseline, không tự đặt như “kết quả”.

## 1.8 Metrics, report và dữ liệu thô

- k6 in end-of-test summary, tạo metric points theo thời gian, hỗ trợ custom metrics, xuất JSON/CSV, stream sang hệ thống ngoài và tùy biến summary thành JSON/HTML/XML qua **handleSummary**. **(DOC; [k6 results output](https://grafana.com/docs/k6/latest/get-started/results-output/), truy cập 2026-07-14)**
- Web dashboard tích hợp có thể hiển thị realtime và xuất một file HTML tự chứa. **(DOC; [k6 web dashboard](https://grafana.com/docs/k6/latest/results-output/web-dashboard/), truy cập 2026-07-14)**
- Khi báo cáo, phải giữ raw JSON/CSV, stdout/stderr, summary, HTML, script, input data đã khử bí mật, Git commit và metadata máy; chỉ giữ ảnh dashboard là chưa đủ để tái kiểm toán. **(ASSUMPTION/thực hành đề xuất)**

## 1.9 CLI, CI/CD, container, threshold và exit code

- Lệnh lõi là **k6 run**; tài liệu integration chính thức liệt kê GitHub Actions, GitLab, Jenkins, Azure Pipelines, AWS CodeBuild và các output/integration liên quan. **(DOC; [k6 integrations](https://grafana.com/docs/k6/latest/reference/integrations/), truy cập 2026-07-14)**
- Threshold thất bại tạo exit code khác 0, nên pipeline có thể dùng trực tiếp làm quality gate; checks đơn lẻ thì không đủ. **(DOC; [k6 thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/), truy cập 2026-07-14; [k6 checks](https://grafana.com/docs/k6/latest/using-k6/checks/), truy cập 2026-07-14)**
- Image Docker chính thức cho phép đóng gói môi trường chạy; browser test dùng image/browser dependencies tương ứng và tiêu tốn tài nguyên cao hơn protocol test. **(DOC; [Install k6 with Docker](https://grafana.com/docs/k6/latest/set-up/install-k6/), truy cập 2026-07-14; [Run browser tests](https://grafana.com/docs/k6/latest/using-k6-browser/running-browser-tests/), truy cập 2026-07-14)**

## 1.10 Local/offline

- CLI, summary, JSON/CSV và web dashboard có thể chạy tại máy; tài khoản Cloud không bắt buộc cho đường chạy này. **(DOC; [Install k6](https://grafana.com/docs/k6/latest/set-up/install-k6/), truy cập 2026-07-14; [k6 results output](https://grafana.com/docs/k6/latest/get-started/results-output/), truy cập 2026-07-14)**
- “Offline tuyệt đối” vẫn cần chuẩn bị trước binary/image, module và dependency; ngoài kết nối tới SUT, không được để script import tài nguyên từ xa. Mức hoạt động trong mạng lớp học chưa được xác nhận. **[CẦN THỰC NGHIỆM]**

## 1.11 Tài liệu và cộng đồng

Tài liệu chính thức có cấu trúc rõ cho authoring, execution, results và integrations; kho GitHub công khai issues/releases và liên kết cộng đồng Grafana. **(DOC; [k6 documentation](https://grafana.com/docs/k6/latest/), truy cập 2026-07-14; [k6 repository](https://github.com/grafana/k6), truy cập 2026-07-14)**

## 1.12 AI-assisted potential

k6 **không phải công cụ AI**; engine phát tải, thu metric và áp threshold theo cách xác định. AI có thể hỗ trợ dựng skeleton JavaScript từ OpenAPI/HAR, sinh dữ liệu giả, gợi ý correlation, review scenario/threshold và tóm tắt raw result. Đây là **ASSUMPTION về quy trình**, không phải bằng chứng k6 tự hiểu nghiệp vụ. HAR converter và k6 Studio chỉ cung cấp điểm khởi đầu cho authoring, và tài liệu vẫn yêu cầu người dùng chỉnh script sau khi chuyển đổi. **(DOC; [HAR converter](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-har-converter/), truy cập 2026-07-14; [k6 Studio](https://grafana.com/docs/k6/latest/k6-studio/), truy cập 2026-07-14)**

**Bắt buộc human audit:** URL/method/payload; bí mật; token/CSRF/correlation; uniqueness và cleanup dữ liệu; think time; tỉ lệ journey; executor và capacity VU; tag cardinality; check nghiệp vụ; threshold gắn SLO; rủi ro tạo tải ngoài phạm vi.

## 1.13 Độ phù hợp EShop và lớp học

- EShop fit cao vì HTTP API, cookie, JSON extraction, data parameterization, multi-scenario và arrival-rate đều có API chính thức. **(ASSUMPTION, dựa trên DOC các mục 1.5–1.7)**
- JavaScript và file đơn giúp demo nhanh; điểm cần dạy rõ là runtime không phải Node.js, check khác threshold, và browser VU khác protocol VU. **(ASSUMPTION, dựa trên DOC các mục 1.4, 1.7 và 1.9)**

## 1.14 Điểm mạnh

1. Test-as-code gọn, review tốt; có workload model mở và đóng.
2. Checks + thresholds + exit code tạo đường CI rõ.
3. Local raw output và self-contained HTML tốt cho hồ sơ bằng chứng.
4. Cookie, JSON extraction và SharedArray đủ cho journey EShop.
5. Có đường authoring bằng HAR/k6 Studio và đường browser bổ sung.

## 1.15 Hạn chế

1. JavaScript runtime riêng gây nhầm với Node.js; không thể mặc định dùng mọi npm package. **(DOC; [k6 modules](https://grafana.com/docs/k6/latest/using-k6/modules/), truy cập 2026-07-14)**
2. Check thất bại không tự fail build; thiếu threshold là lỗi cấu hình CI phổ biến. **(DOC; [k6 checks](https://grafana.com/docs/k6/latest/using-k6/checks/), truy cập 2026-07-14)**
3. HAR/script sinh tự động chưa giải quyết correlation, data và load model. **(DOC; [HAR converter](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-har-converter/), truy cập 2026-07-14)**
4. Browser VU nặng hơn protocol VU và chỉ nên dùng có chủ đích; cần đo capacity load generator. **[CẦN THỰC NGHIỆM]**
5. AGPL-3.0 cần được bộ phận pháp lý xem xét nếu nhúng/sửa/phân phối theo mô hình sản phẩm; bài học chạy CLI độc lập thường không đồng nghĩa với tư vấn pháp lý. **(DOC về giấy phép; [k6 repository](https://github.com/grafana/k6), truy cập 2026-07-14; diễn giải pháp lý cần chuyên gia)**

## 1.16 Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

- **Mục tiêu:** xác nhận cài đặt, một HTTP GET được phép, check status, threshold, raw JSON và mã thoát.
- **Tiền điều kiện:** chủ hệ thống xác nhận phạm vi; thay **[VERIFIED_BASE_URL]** và **[VERIFIED_PRODUCT_ENDPOINT]**; endpoint idempotent; pin phiên bản k6; đồng bộ giờ máy; không dùng production nếu chưa được phép.
- **Cài đặt/setup:** cài theo tài liệu chính thức hoặc dùng image đã pin; ghi lại OS, CPU/RAM, lệnh version, đường mạng và Git commit. **(DOC; [Install k6](https://grafana.com/docs/k6/latest/set-up/install-k6/), truy cập 2026-07-14)**
- **Script đề xuất – smoke.js:**

~~~javascript
import http from "k6/http";
import { check } from "k6";

export const options = {
  scenarios: {
    smoke: {
      executor: "shared-iterations",
      vus: 1,
      iterations: 1,
    },
  },
  thresholds: {
    checks: ["rate==1"],
    http_req_failed: ["rate==0"],
  },
};

export default function () {
  const response = http.get(
    "[VERIFIED_BASE_URL][VERIFIED_PRODUCT_ENDPOINT]",
    { tags: { journey: "smoke", endpoint: "product" } }
  );
  check(response, {
    "status is 200": (r) => r.status === 200,
  });
}
~~~

- **Lệnh:** **k6 run --out json=artifacts/k6-smoke.json smoke.js**
- **Kết quả mong đợi:** đúng một iteration được lập lịch; status check đạt; thresholds đạt; process trả 0; JSON và summary được tạo. Đây là điều kiện chấp nhận, **không phải kết quả đã quan sát**.
- **Bằng chứng cần thu:** lệnh/version; script + SHA-256; stdout/stderr; exit code; raw JSON; summary/HTML nếu bật dashboard; timestamps; metadata máy; network/SUT version; Git commit; ảnh màn hình chỉ là phụ.
- **Lỗi có thể gặp:** URL/DNS/TLS; endpoint yêu cầu auth; 301/401/403/404; quyền ghi artifacts; threshold syntax; proxy; timestamp; container volume; nhầm Node.js package với k6 module.
- **Tiêu chí thành công:** mọi bằng chứng trên có mặt, request trong phạm vi cho phép, exit code 0 và raw data cho thấy check/threshold đạt. Nếu khác, ghi **EXP failed/inconclusive**, không sửa số liệu.

## 1.17 Bảng điểm đề xuất

| Tiêu chí | Điểm | Lý do ngắn và bằng chứng |
|---|---:|---|
| Cost & access | 5 | OSS AGPL-3.0 chạy local không cần account; cloud tùy chọn. **(DOC; [repo](https://github.com/grafana/k6), [pricing](https://grafana.com/pricing/), truy cập 2026-07-14)** |
| Learning curve | 4 | JavaScript dễ tiếp cận nhưng runtime không phải Node.js. **(DOC; [modules](https://grafana.com/docs/k6/latest/using-k6/modules/), truy cập 2026-07-14)** |
| EShop fit | 5 | HTTP, cookie, JSON, data và tagging phù hợp API commerce. **(DOC; [cookies](https://grafana.com/docs/k6/latest/using-k6/cookies/), [parameterization](https://grafana.com/docs/k6/latest/examples/data-parameterization/), truy cập 2026-07-14)** |
| Multi-step journey | 5 | JS flow, per-VU state và nhiều scenario. **(DOC; [scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/), truy cập 2026-07-14)** |
| Workload control | 5 | VU, iteration và arrival-rate executors. **(DOC; [scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/), truy cập 2026-07-14)** |
| Assertions/checks | 5 | Check nghiệp vụ + threshold/abort/exit; phải cấu hình cả hai đúng. **(DOC; [checks](https://grafana.com/docs/k6/latest/using-k6/checks/), [thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/), truy cập 2026-07-14)** |
| Reporting | 5 | Summary, raw JSON/CSV, stream, custom summary và local HTML dashboard. **(DOC; [results](https://grafana.com/docs/k6/latest/get-started/results-output/), [dashboard](https://grafana.com/docs/k6/latest/results-output/web-dashboard/), truy cập 2026-07-14)** |
| CI/CD | 5 | CLI, nonzero threshold exit và nhiều CI integration chính thức. **(DOC; [integrations](https://grafana.com/docs/k6/latest/reference/integrations/), truy cập 2026-07-14)** |
| Reproducibility | 5 | Script/config/raw output dễ pin và version-control; điểm này vẫn cần EXP xác nhận môi trường lớp. **(DOC; [install](https://grafana.com/docs/k6/latest/set-up/install-k6/), [results](https://grafana.com/docs/k6/latest/get-started/results-output/), truy cập 2026-07-14)** |
| Local/offline | 5 | Binary/Docker và output/report local; offline tuyệt đối cần cache trước. **(DOC; [install](https://grafana.com/docs/k6/latest/set-up/install-k6/), truy cập 2026-07-14)** |
| AI-assisted potential | 5 | Text JS + HAR/Studio tạo điểm vào tốt cho AI hỗ trợ; **ASSUMPTION**, tool không phải AI. **(DOC nền; [HAR](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-har-converter/), truy cập 2026-07-14)** |
| Classroom suitability | 4 | Demo gọn và evidence tốt; phải dạy runtime/check-vs-threshold/browser caveat. **(DOC nền như trên; đánh giá ASSUMPTION)** |

**Điểm quy đổi đề xuất: 97.4/100.** Đây là điểm hồ sơ tài liệu, chưa được hiệu chỉnh bằng EXP.

## 1.18 Câu hỏi phản biện và trả lời

1. **Nếu checks đều đúng thì tại sao còn cần thresholds?**  
   Vì tài liệu k6 nói check thất bại không tự làm test dừng hay trả lỗi; threshold mới là acceptance criterion điều khiển pass/fail/exit code. **(DOC; [checks](https://grafana.com/docs/k6/latest/using-k6/checks/), [thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/), truy cập 2026-07-14)**

2. **JavaScript nghĩa là có thể dùng mọi package npm phải không?**  
   Không. k6 chạy runtime riêng, không phải Node.js; Node built-ins không mặc định tồn tại và package phải được đánh giá/bundle tương thích. **(DOC; [k6 modules](https://grafana.com/docs/k6/latest/using-k6/modules/), truy cập 2026-07-14)**

3. **Có browser module thì nên chạy toàn bộ 1.000 browser VU để “thực tế” hơn?**  
   Không thể kết luận như vậy. Browser VU và protocol VU phục vụ mục tiêu khác nhau và có footprint khác; cần dùng một lượng browser nhỏ cho frontend signal, còn backend capacity thường dùng protocol load. Capacity cụ thể phải đo. **[CẦN THỰC NGHIỆM]**

4. **HAR/k6 Studio có làm script production-ready tự động không?**  
   Không. Tài liệu HAR converter yêu cầu chỉnh script sinh ra cho workload/correlation; nhóm vẫn phải audit dữ liệu, token, think time, assertions và threshold. **(DOC; [HAR converter](https://grafana.com/docs/k6/latest/using-k6/test-authoring/create-tests-from-recordings/using-the-har-converter/), truy cập 2026-07-14)**

