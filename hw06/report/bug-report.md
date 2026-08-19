# HW06 bug report

> Mỗi defect giữ đúng ID trong `docs/hw06/02-sut-defect-catalog.md`. Evidence Newman là report JSON thật; các dòng manual follow-up được đánh dấu rõ, không bịa screenshot/issue.

| Bug ID | Severity | Title | Found by Test Case | Expected | Actual | Evidence | GitHub Issue | Screenshot |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D-LOGIN-01 | Critical | Sai password làm tăng counter hai lần; lock quá sớm | `TC-API-LOGIN-018` | 200 sau hai lần sai (theo đặc tả) | 403 sau hai lần sai trong canary/full; xem `00-canary-suite.json` | Newman | Chưa tạo — HUMAN | Chưa có — HUMAN |
| D-LOGIN-02 | Major | Thời gian khóa 180s thay vì 30s | `TC-API-LOGIN-019` | Khóa 30s | SUT defect catalog ghi nhận 180s; smoke collection chưa chờ đủ 180s | Catalog + manual follow-up | Chưa tạo — HUMAN | Chưa có — HUMAN |
| D-LOGIN-03 | Critical | Response trả password plaintext | `TC-API-LOGIN-028` | Không có password | Full strict assertion bắt được password `Test1234!` | `00-full-suite.json` | Chưa tạo — HUMAN | Chưa có — HUMAN |
| D-LOGIN-05 | Major | JWT hard-code/không hết hạn | `TC-API-LOGIN-030` | JWT có exp và secret quản lý an toàn | Endpoint phát token không có exp; cần decode token xác nhận đầy đủ | Catalog + manual follow-up | Chưa tạo — HUMAN | Chưa có — HUMAN |
| D-LOGIN-06 | Major | Counter không reset sau khi hết khóa | `TC-API-LOGIN-020` | Counter reset khi hết thời gian khóa | Catalog ghi nhận counter giữ nguyên; cần probe chờ timer | Catalog + manual follow-up | Chưa tạo — HUMAN | Chưa có — HUMAN |
| D-CHK-01 | Critical | Tin total_amount từ client | `TC-API-CHECKOUT-037` | Tính lại total từ cart | Checkout nhận client total `1` và tạo order thành công | `00-full-suite.json` / test table | Chưa tạo — HUMAN | Chưa có — HUMAN |
| D-CHK-02 | Major | Chấp nhận total âm/0 | `TC-API-CHECKOUT-005` | 400 validation | Zero total trả 200 trong full strict | `00-full-suite.json` | Chưa tạo — HUMAN | Chưa có — HUMAN |
| D-CHK-03 | Major | Không xóa cart sau checkout | `TC-API-CHECKOUT-020` | Cart rỗng | Post-condition strict fail; cart vẫn còn item | `00-full-suite.json` | Chưa tạo — HUMAN | Chưa có — HUMAN |
| D-CHK-04 | Major | Checkout với cart rỗng | `TC-API-CHECKOUT-021` | 400 | Catalog ghi nhận checkout rỗng vẫn tạo order; cần probe độc lập | Catalog + manual follow-up | Chưa tạo — HUMAN | Chưa có — HUMAN |
| D-CHK-07 | Critical | IDOR GET /api/orders/:id | `TC-API-CHECKOUT-031` | 401/403 nếu không có auth | Anonymous/order detail probe trả 200 | `00-full-suite.json` | Chưa tạo — HUMAN | Chưa có — HUMAN |
| D-ADM-01 | Critical | User thường đổi trạng thái qua API admin | `TC-API-ORDER-STATUS-033` | 403 | User token trả 200 trong full strict | `00-full-suite.json` | Chưa tạo — HUMAN | Chưa có — HUMAN |
| D-ADM-02 | Critical | canceled → delivered được phép | `TC-API-ORDER-STATUS-024` | 400 | Trả 200 trong full strict và matrix DDT | `00-full-suite.json`, `03-ddt-order-status.json` | Chưa tạo — HUMAN | Chưa có — HUMAN |
| D-ADM-03 | Major | Admin không hủy được shipping | `TC-API-ORDER-STATUS-015` | 200 | Catalog ghi nhận 400; cần stateful probe độc lập | Catalog + manual follow-up | Chưa tạo — HUMAN | Chưa có — HUMAN |
| D-ADM-04 | Major | Bỏ qua lỗi UPDATE, trả 200 | `TC-API-ORDER-STATUS-041` | 4xx/5xx khi update lỗi | Callback bỏ qua err theo catalog; cần tạo orderId không tồn tại | Catalog + manual follow-up | Chưa tạo — HUMAN | Chưa có — HUMAN |
| D-ADM-08 | Major | User hủy order shipping | `TC-API-ORDER-STATUS-042` | 400 | Catalog ghi nhận user cancel shipping được 200; cần stateful probe | Catalog + manual follow-up | Chưa tạo — HUMAN | Chưa có — HUMAN |

## Quy ước reproducing

- Chạy backend reset DB rồi `powershell -ExecutionPolicy Bypass -File hw06/newman/run-newman.ps1 -Mode full -BaseUrl http://127.0.0.1:3001`.
- Dùng `-DataDriven` để chạy 16/18/25 rows; status matrix cần precondition state đúng theo `from_status`.
- GitHub Issues và screenshot là artifact external/human-only, nên không được thay bằng số issue hoặc ảnh giả.
