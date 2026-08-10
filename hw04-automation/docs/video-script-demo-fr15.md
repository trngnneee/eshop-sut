# Video script — Task 2 Demo (FR-15 Product CRUD Admin)

**Purpose:** YouTube Unlisted ≥ **5 phút**, kể bằng **tiếng Việt**  
**Feature:** Feature C — FR-15 Admin Product CRUD  
**Student ID:** `23127271`  
**Kết quả Chromium đã chạy (2026-08-10):** **6 pass / 8 fail** — dùng số này khi narrate (Firefox/WebKit kỳ vọng tương tự nếu oracle giữ nguyên)

> Video này = **Task 2 Demo** (chạy script + 3 browser + HTML + 1 AI fix).  
> **Không** liệt kê Analyze→Verify / skill stages — phần đó thuộc `video-script-agent-skill-fr15.md`.

---

## PDF checklist (phải đủ)

| # | Yêu cầu | Scene |
| ---: | --- | --- |
| 1 | ≥ 5 phút, giọng VN của bạn | Full |
| 2 | Chạy 1 automation end-to-end | Scene 3 |
| 3 | Multi-browser đủ **3** (Chromium + Firefox + WebKit) | Scene 3 |
| 4 | HTML report có Student ID | Scene 4 |
| 5 | Narrate ≥ 1 fix trên script AI lúc review | Scene 2 |
| 6 | Face-cam **hoặc** `whoami` **và** `hostname` | Scene 0 |

---

## Trước khi Record

### SUT phải chạy

| Service | URL | Cách start (nếu tắt) |
| --- | --- | --- |
| Backend API | `http://localhost:3000` | `cd Repo/eshop-sut/backend` → `npm start` (hoặc lệnh bạn đang dùng) |
| **Web Admin** | `http://localhost:5174` | `cd Repo/eshop-sut/frontend-admin` → `npm run dev` |
| Storefront | `http://localhost:5173` | Không bắt buộc cho FR-15 UI |

### Terminal cwd

```powershell
cd C:\DiskD\HCMUS\Semester9\SoftwareTesting\SoftwareTesting-HW\HW4\23127271
```

### Quy tắc evidence

- Chỉ chạy FR-15: `npm run test:matrix:fr15`
- **Không** `FORCE_OVERWRITE` / không đụng report FR-03 đã lock
- Optional trước/sau: `npm run evidence:verify-fr03`

### Số liệu dùng khi nói (Chromium thật)

| | IDs |
| --- | --- |
| **Pass (6)** | 001 Create · 002 View · 003 Edit · 005 Delete · 007 Name 255 · 011 Price 1 |
| **Fail (8) — defect SUT, giữ oracle** | 004 Edit isolation UI · 006 Empty name · 008 Name 256 · 009 Price 0 · 010 Price −1 · 012 Category invalid · 013 No JWT · 014 Non-admin JWT |

### Lỗi mẫu mang vào video (chọn **2** để zoom)

**Mẫu A — TC-PRODUCT-009 (dễ hiểu, API)**  
- Spec: `price: 0` → HTTP **400–499**  
- SUT: `POST /api/products` trả **200**  
- Message Playwright:

```text
Error: expect(received).toBeGreaterThanOrEqual(expected)
Expected: >= 400
Received:    200
```

**Mẫu B — TC-PRODUCT-004 (UI, FR-15 “chỉ SP đó đổi”)**  
- Spec: sau khi sửa A, hàng sibling B vẫn hiện tên cũ  
- SUT: UI `fakeMassUpdatedProducts` → mọi hàng đổi tên theo A → không còn row chứa tên B  
- Message Playwright:

```text
Error: expect(locator).toContainText(expected) failed
Locator: getByRole('row').filter({ hasText: 'HW04-P004-B-…' })
Expected substring: "HW04-P004-B-…"
Error: element(s) not found
```

**Mẫu C (optional, FR-12) — TC-PRODUCT-013**  
- Spec: không JWT → **401–403**  
- SUT: vẫn **200** (API product không auth)

---

## Timeline tổng (≈ 6:30–7:30)

| Scene | Thời gian | Nội dung |
| --- | --- | --- |
| 0 | 0:00–0:45 | Authorship |
| 1 | 0:45–1:40 | Spec + JSON |
| 2 | 1:40–3:00 | **1 AI fix thật** ★ |
| 3 | 3:00–5:40 | Matrix 3 browser ★ |
| 4 | 5:40–6:50 | HTML report + lỗi mẫu ★ |
| 5 | 6:50–7:20 | Close |

---

## Scene 0 — Authorship (0:00–0:45)

**On screen:** PowerShell (+ face-cam nếu có)

```powershell
whoami
hostname
# optional:
echo 23127271
```

**Nói (đọc gần đúng):**  
> Xin chào, mình là sinh viên mã số **hai ba một hai bảy hai bảy một** — **23127271**.  
> Video này là **Task 2 — Demo** bài HW04 Automation Testing.  
> Mình sẽ demo automation Playwright cho **Feature C, FR-15: quản lý sản phẩm CRUD phía Admin** trên hệ thống EShop: chạy end-to-end đa trình duyệt và mở HTML report có gắn mã số sinh viên.

---

## Scene 1 — Suite & data-driven (0:45–1:40)

**On screen:** Explorer + VS Code

1. Mở `tests/fr15-admin-product.spec.js` — scroll tới vòng `for (const tc of cases)` / `test(\`${tc.id}: …\`)`.  
2. Mở `test-data/fr15-admin-product.json` — zoom các id:

```text
TC-PRODUCT-001 … Create
TC-PRODUCT-004 … Edit isolation
TC-PRODUCT-009 … price 0
TC-PRODUCT-013 … no JWT
```

3. (Optional 5s) `pages/AdminProductPage.js` — placeholder `Tên sản phẩm` / nút `Lưu sản phẩm`.

**Nói:**  
> Đây là bộ automation Feature C.  
> **Mười bốn** test case nằm trong file JSON bên ngoài — kiểu **data-driven**: spec không hard-code danh sách case, mà load JSON rồi chạy theo `journey` và assertion type.  
> Suite gồm CRUD dương: thêm, xem, sửa, xóa; thêm validation biên tên/giá/danh mục và kiểm tra quyền FR-12.  
> Admin UI chạy cổng **5174**, khác storefront 5173.

**Không** kể Analyze / Design / skill stages.

---

## Scene 2 — ≥1 AI fix lúc review (1:40–3:00) ★ bắt buộc

Zoom chat Cursor + JSON ~20–30s. Có **prompt dán sẵn** bên dưới.

### Prompt dán Cursor ★

**Cách quay:** hiện Prompt A (sai) → nói “không dùng” → dán Prompt B (đúng) → zoom `"min": 400`.

#### Prompt A — SAI (cám dỗ cho xanh) — chỉ demo, đừng nộp

```text
TC-PRODUCT-009 đang fail vì API trả 200 khi price=0.
Hãy sửa expected trong test-data/fr15-admin-product.json
cho case này pass (đổi apiStatus thành chấp nhận 200).
```

**Nói:**  
> Đây là prompt **sai** — bảo AI sửa expected cho xanh. Mình **không** Accept bản này để nộp.

#### Prompt B — ĐÚNG (giữ oracle) ★ dùng thật

```text
Review FR-15 TC-PRODUCT-009 trong test-data/fr15-admin-product.json
và tests/fr15-admin-product.spec.js.

SUT POST /api/products với price=0 đang trả 200 (defect).
KHÔNG được đổi expected cho khớp SUT.
Giữ apiStatus min=400 max=499 và apiProductAbsent.
Nếu đã bị hạ min xuống 200 thì khôi phục lại 400–499.
Giải thích ngắn vì sao không làm mềm oracle (README FR-15: giá > 0).
```

**Nói:**  
> Prompt đúng: giữ bốnxx theo FR-15. Trên JSON — `min` vẫn **bốn trăm**. Fail có chủ đích = defect SUT.

#### Prompt phụ — TC-PRODUCT-004 (optional)

```text
TC-PRODUCT-004: UI đang đổi tên mọi sản phẩm khi sửa một cái.
KHÔNG xóa assertion uiSiblingNameUnchanged trong JSON.
Giữ cả apiSiblingUnchanged và uiSiblingNameUnchanged theo FR-15.
Có thể đề xuất locator theo row index nhưng expected tên sibling phải giữ.
```

#### Prompt phụ — Admin cổng 5174

```text
FR-15 Admin SPA ở http://localhost:5174.
Đảm bảo scripts/run-matrix.js khi chạy fr15 set ADMIN_BASE_URL/BASE_URL=5174.
pages/AdminProductPage.js dùng ADMIN_BASE_URL, inject localStorage.adminToken.
Không đụng report FR-03/FR-08.
```

### Ví dụ zoom JSON (TC-PRODUCT-009)

**❌ Sau Prompt A (sai):** `{ "type": "apiStatus", "min": 200, "max": 299, ... }`  
**✅ Sau Prompt B / bản nộp:**

```json
"expected": {
  "assertions": [
    { "type": "apiStatus", "min": 400, "max": 499, "on": "createResponse" },
    { "type": "apiProductAbsent", "match": "productName" }
  ]
}
```

```text
Expected: >= 400
Received:    200
```

---

## Scene 3 — Multi-browser + hiện 3 màn (3:00–5:40) ★ đủ 3

**Mục tiêu camera:** thấy rõ **Chromium + Firefox + WebKit** (cửa sổ headed và/hoặc 3 HTML report).

### Prompt dán Cursor — hiện 3 trình duyệt ★

```text
Demo Task 2 FR-15: cần THẤY 3 trình duyệt trên màn hình.

1) Kiểm tra API :3000 và Admin :5174 (start frontend-admin npm run dev nếu cần).
2) cwd = SoftwareTesting-HW/HW4/23127271. Set:
   $env:ADMIN_BASE_URL='http://localhost:5174'; $env:BASE_URL='http://localhost:5174'
3) Chạy headed LẦN LƯỢT (hoặc 3 terminal gần cùng lúc) đúng 1 case dương để cửa sổ hiện:
   npx playwright test tests/fr15-admin-product.spec.js --project=chromium --grep "TC-PRODUCT-001" --headed --workers=1
   npx playwright test tests/fr15-admin-product.spec.js --project=firefox --grep "TC-PRODUCT-001" --headed --workers=1
   npx playwright test tests/fr15-admin-product.spec.js --project=webkit --grep "TC-PRODUCT-001" --headed --workers=1
4) Rồi full matrix (headless OK) tạo đủ 3 report:
   npm run test:matrix:fr15
5) Mở 3 report trong 3 cửa sổ:
   start reports\html\fr15-admin-product\chromium\index.html
   start reports\html\fr15-admin-product\firefox\index.html
   start reports\html\fr15-admin-product\webkit\index.html
Zoom Run by: 23127271. Không làm mềm oracle. Không đụng FR-03/FR-08.
```

### Cách A — 3 cửa sổ headed (browser thật) ★

```powershell
cd SoftwareTesting-HW\HW4\23127271
$env:ADMIN_BASE_URL='http://localhost:5174'
$env:BASE_URL='http://localhost:5174'

npx playwright test tests/fr15-admin-product.spec.js --project=chromium --grep "TC-PRODUCT-001" --headed
npx playwright test tests/fr15-admin-product.spec.js --project=firefox --grep "TC-PRODUCT-001" --headed
npx playwright test tests/fr15-admin-product.spec.js --project=webkit --grep "TC-PRODUCT-001" --headed
```

Muốn **3 màn cùng lúc:** mở 3 PowerShell, mỗi cái một lệnh `--headed` ở trên, Enter gần nhau, xếp 3 cột.

**Nói:**  
> Chromium headed… Firefox… WebKit — cùng case 001 trên ba engine.

### Cách B — Full matrix (đủ evidence) ★

```powershell
npm run evidence:verify-fr03
npm run test:matrix:fr15
```

### Cách C — 3 màn HTML report

```powershell
start reports\html\fr15-admin-product\chromium\index.html
start reports\html\fr15-admin-product\firefox\index.html
start reports\html\fr15-admin-product\webkit\index.html
```

**Combo quay:** A (vài giây) → B (matrix, cắt ghép OK) → C (3 report cạnh nhau).

**Nói khi matrix xong:**  
> Chromium tham chiếu: khoảng **sáu pass, tám fail**. Fail giữ oracle — defect SUT, không xanh giả.

---

## Scene 4 — HTML report + lỗi mẫu (5:40–6:50) ★

**On screen:** Explorer + Chrome

### 4.1 Folder

```text
SoftwareTesting-HW\HW4\23127271\reports\html\fr15-admin-product\
  chromium\
  firefox\
  webkit\
```

**Nói:**  
> Ba thư mục tương ứng ba trình duyệt — mỗi lần chạy một HTML report riêng.

### 4.2 Mở report Chromium

```text
reports\html\fr15-admin-product\chromium\index.html
```

1. Zoom header / title: **`Run by: 23127271`** + timestamp ISO.  
2. Chỉ **1 case pass** (gợi ý **001** hoặc **011**).  
3. Chỉ **1 case fail mẫu A — 009** (Price 0):

**Nói khi mở fail 009:**  
> Case **TC-PRODUCT-009**: theo FR-15 giá phải lớn hơn không, nên API phải từ chối.  
> Nhưng SUT trả **status 200** — Playwright báo expected lớn hơn hoặc bằng bốn trăm, received hai trăm.  
> Đây là defect thật, mình giữ fail trong report.

4. (Khuyến nghị) Mở thêm fail **004** hoặc screenshot trong:

```text
test-results\fr15-admin-product\chromium\...\test-failed-1.png
```

**Nói khi mở 004:**  
> Case **TC-PRODUCT-004**: sửa sản phẩm A nhưng UI đổi tên luôn hàng sản phẩm B — trái FR-15 “chỉ sản phẩm đó bị thay đổi”. Locator không còn tìm thấy tên B trên bảng → fail.  
> Mình không xóa assertion sibling để test xanh.

5. Optional: mở nhanh `firefox/index.html` hoặc `webkit/index.html` 5–10s — lại zoom `Run by: 23127271`.

**Nói:**  
> Header report có đúng cụm **Run by: 23127271** — chứng minh lần chạy gắn mã số sinh viên theo đề.

---

## Scene 5 — Close (6:50–7:20)

**Nói:**  
> Tóm lại video Task 2: mình đã chạy automation FR-15 end-to-end trên **ba** trình duyệt, mở HTML report có Student ID, và đã kể một lần **review/giữ oracle** thay vì làm mềm assertion cho xanh giả — với lỗi mẫu giá bằng không vẫn tạo được và UI đổi tên hàng loạt.  
> Mã số **23127271**. Cảm ơn thầy cô đã xem.

Upload **Unlisted** → dán link vào README / báo cáo.

---

## Lời thoại “cứu nguy” nếu máy chậm / SUT lỗi tạm

| Tình huống | Nói |
| --- | --- |
| Admin 5174 tắt | “Admin chưa lên — mình start `npm run dev` ở frontend-admin rồi chạy lại.” |
| Thiếu browser binary | “Playwright thiếu Chromium — `npx playwright install chromium` rồi chạy tiếp.” |
| Matrix > 3 phút | “Mình giữ camera đủ ba project; phần giữa cắt ghép, kết quả lấy từ report vừa generate.” |
| Muốn all-green | **Không làm.** Nói rõ fail = defect. |

---

## Checklist trước upload

- [ ] ≥ 5:00, giọng **tiếng Việt** của bạn  
- [ ] Face-cam **hoặc** (`whoami` **và** `hostname`)  
- [ ] Hiện `fr15-admin-product.spec.js` + JSON (≥12 / thực tế 14 case)  
- [ ] **Đủ 3 browser** trên hình  
- [ ] HTML: `Run by: 23127271` + timestamp  
- [ ] Kể ≥ 1 **AI fix / review thật** (giữ oracle — có số 6/8)  
- [ ] Zoom ≥ 1 lỗi mẫu (009 và/hoặc 004) — **không** giả all green  
- [ ] Không quay nhầm thành skill demo (không liệt kê stage prompts)  
- [ ] YouTube **Unlisted** + link README  

---

## Khác video Agent Skill

| | Task 2 (file này) | Agent Skill |
| --- | --- | --- |
| Trọng tâm | Chạy + 3 browser + HTML + 1 AI fix | Skill + nhiều prompt theo stage |
| Step-by-step prompts | Không | Bắt buộc |
| Lỗi mẫu | 004 / 009 / 013 từ Chromium thật | Không bắt buộc |
