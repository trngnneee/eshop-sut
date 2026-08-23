# Postman features đã dùng → ở đâu (HW06 · MSSV 23127438)

> Bảng đối chiếu để dán vào report. Collection: `EShop-HW06.postman_collection.json` (v2.1.0) ·
> Environment: `EShop-Local.postman_environment.json` · Data: `postman/data/*.csv`.
> Tổng: **231 request** trong suite chính + 3 request data-driven + 1 request mock. SUT: `http://localhost:3000`.

| # | Feature | Đã dùng ở đâu (cụ thể) |
|---|---------|------------------------|
| 1 | **Workspace** | Toàn bộ artifact nằm trong 1 workspace; import 2 file (collection + environment) và thư mục `data/`. Chọn environment **EShop-Local** ở góc phải trước khi chạy. |
| 2 | **Nested folders** (cây phân cấp) | 7 folder gốc: `00-Setup`, `01-API1-Products-Read`, `02-API2-Order-Cancel`, `03-API3-Product-Manage`, `04-DataDriven-CSV`, `05-Mock-Spec`, `99-Teardown`. Mỗi API có **sub-folder** theo nhóm kỹ thuật (Positive-Boundary / Negative / Security / Schema · Fixtures / State-Transitions / Auth-IDOR / Schema · Create-Validation / Update-Validation / Auth-Escalation / Schema). |
| 3 | **Environment variables** | `EShop-Local`: `baseUrl`, `studentId`, `adminToken`, `userToken`, `productId`, `orderId`, các biến state đơn `ordPending/ordConfirmed/ordShipping/ordDelivered/ordCanceled`, và token forge `forgedVictim/forgedAdminRole/forgedExpired/tokenWrongSecret`, `jwtSecret`. Token để `type: secret`. |
| 4 | **Collection variables** | 5 JSON schema nhúng dạng string: `productSchema`, `productListSchema`, `messageSchema`, `errorSchema`, `createdSchema` (tab **Variables** của collection). Test script `JSON.parse(...)` rồi gọi `jsonSchema`. |
| 5 | **Pre-request script (cấp collection)** | Tab **Scripts** của collection: `pm.request.headers.upsert({key:'X-Student-Id', value:...})` + `console.log('[HW06] X-Student-Id = ...')`. Chèn header MSSV cho MỌI request, request không hardcode. |
| 6 | **Pre-request script (cấp request)** | Order-builder dựng đơn theo state (`02` State-Transitions/Schema, `DD-3`); sinh chuỗi 1000 ký tự (`TC-P1-019/033`); sinh name 255/256/300 ký tự (`TC-P3-002/006/007`); dựng product target sạch (`03` PUT/DELETE); gỡ header `X-Student-Id` (`TC-P1-082`, `TC-O2-056`, `TC-P3-073`); cảnh báo token forge rỗng. |
| 7 | **pm.test + assertions** (chai) | Tất cả request. `pm.response.to.have.status`, `pm.expect(...).to.eql/be.a/include/be.at.least`, `pm.expect.fail(...)` cho case cố ý FAIL (bug). |
| 8 | **pm.response.to.have.jsonSchema** | Các sub-folder **Schema** của cả 3 API + DD-1/DD-2. Bắt BUG-01 (price string), thiếu/thừa field, sai loại response (`{message}` vs `{error}`). |
| 9 | **Chaining (set/get biến từ response)** | `00-Setup` set `adminToken/userToken/productId/orderId`; `02/Fixtures` set `ord*`; `TC-P1-021` list→detail; `03` chain create id → GET; `05-Mock` gọi lại. |
| 10 | **Dynamic variables** | `{{$randomProductName}}` + `{{$timestamp}}` ở `SETUP-03` (tên product mẫu không trùng) và `TC-P3-075` (test trùng tên). |
| 11 | **Collection Runner + CSV (data-driven)** | Folder `04-DataDriven-CSV`: DD-1 (`product-ids.csv`), DD-2 (`products.csv`), DD-3 (`cancel-states.csv`). Chạy Runner → chọn request → Data → chọn CSV → Iterations theo số dòng. |
| 12 | **Bearer auth inherit (auth cấp folder)** | `02` sub-folder Fixtures/State-Transitions/Schema inherit `{{userToken}}`; `03` Create/Update/Schema inherit `{{adminToken}}`. Các sub-folder auth-test (`Auth-IDOR`, `Auth-Escalation`) để **noauth** để mỗi case tự khai báo (tránh token inherit làm case "không token" pass giả). |
| 13 | **pm.sendRequest** (request phụ trong script) | Hậu kiểm state đơn qua `GET /api/orders/:id`; order-builder (checkout → admin đẩy state); cross-endpoint `TC-P1-021`; double-cancel lần 2 `TC-O2-021`; teardown xoá id>5 `TD-2`; hậu kiểm product sau PUT/DELETE. |
| 14 | **Mock Server + examples** | Folder `05-Mock-Spec`: request `GET /api/products/:id` mang **2 examples** (200 price NUMBER, 404 not-found) → tạo Mock Server để đối chiếu spec-đúng vs SUT-sai (BUG-01/02). Cách setup ghi trong description request. |
| 15 | **Examples** | 2 saved example ở `05-Mock-Spec` (nguồn cho mock). |
| 16 | **Monitor** | *(Tùy chọn — chưa dựng trong file.)* Cách setup: collection → **⋯ → Monitor collection** → đặt lịch (vd mỗi giờ) + chọn environment → Postman chạy tự động và gửi mail khi có test đỏ. Lưu ý: monitor chạy trên cloud Postman nên **không** gọi được `localhost` — chỉ dùng khi SUT có URL public (hoặc dùng Postman Agent). Ghi làm hướng mở rộng trong report. |
| 17 | **Newman + htmlextra** | Chạy CLI ngoài Postman (Bước 6). Lệnh ở dưới. |

## Lệnh Newman (Bước 6)

```bash
# cài 1 lần
npm i -g newman newman-reporter-htmlextra

# chạy toàn suite (bỏ qua folder mock/data-driven cần CSV riêng)
newman run postman/EShop-HW06.postman_collection.json \
  -e postman/EShop-Local.postman_environment.json \
  -r cli,htmlextra \
  --reporter-htmlextra-export newman/report.html

# chạy 1 request data-driven với CSV
newman run postman/EShop-HW06.postman_collection.json \
  -e postman/EShop-Local.postman_environment.json \
  --folder "04-DataDriven-CSV" \
  -d postman/data/product-ids.csv \
  -r cli,htmlextra --reporter-htmlextra-export newman/report-dd1.html
```

> ⚠ Trước mỗi lần chạy lại: **restart `node server.js`** (database.js DROP + reseed) để về đúng seed
> (categories 1..3, products 1..5, orders rỗng), vì folder 03 có case DELETE destructive (TC-P3-054/055).
> Chạy `00-Setup` đầu tiên để nạp token/id.

## Ghi chú "cố ý FAIL = bắt bug"

Suite được thiết kế để **một số test CỐ Ý đỏ** — đó là bằng chứng bug, không phải lỗi test:
BUG-01 (price string, id chẵn) · BUG-02 (404→200 {}) · BUG-03 (SQLi search) · BUG-04 (500 HTML leak) ·
BUG-05 (shipping→cancel) · BUG-07 (CRUD thiếu auth) · BUG-08/09/10 (POST không validate) ·
BUG-11 (PUT null hóa) · BUG-12 (PUT/DELETE not-found no-op) · BUG-13 (JWT forge) · BUG-14 (id không canonical) ·
BUG-15 (lỗi HTML thay vì JSON) · BUG-16 (unicode search) · BUG-17 (wildcard bypass) · BUG-18 (param lặp) ·
BUG-20 (UNION lộ credential) · BUG-21 (thiếu nosniff) · TC-O2-058 (IDOR đọc đơn).
