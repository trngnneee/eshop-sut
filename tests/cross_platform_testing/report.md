# HW03 — Task 3: Báo cáo Cross-Browser / Cross-Platform

**Sinh viên:** Đặng Trường Nguyên

**MSSV**: 23127438

**SUT:** EShop (`frontend-web` tại `http://localhost:5173`, backend tại `http://localhost:3000`)

**Ngày thực thi:** 28/07/2026 · **Máy:** MacBook Pro (Apple Silicon), macOS 15.5 (24F74)

---

## 1. Đã làm gì

Đề yêu cầu *"Perform Task 1 across at least three (3) platforms"*. Task 1 là checklist **66 item** (IA-01 17 · IA-02 15 · IA-03 15 · IA-04 19). Task 3 vì thế là **198 lượt thực thi** (66 × 3), tất cả đều được chạy thật, không lấy mẫu, không suy diễn từ platform khác.

| | Giá trị |
|---|---|
| Số platform | 3 (Chromium/Blink · Firefox/Gecko · WebKit) — chi tiết version/OS/device ở [platform-matrix.md](platform-matrix.md) |
| Số item mỗi platform | 66/66 (không item nào bị bỏ) |
| Tổng lượt thực thi | **198** |
| Kết quả | P1 **7 Pass / 59 Fail** · P2 **6 Pass / 60 Fail** · P3 **6 Pass / 60 Fail** — 0 Blocked, 0 lỗi harness |
| Ảnh bằng chứng | **179 ảnh viewport** (mọi item Fail, mọi platform) + **18 ảnh cửa sổ thật** (6 màn × 3 platform) |
| Khác biệt giữa platform | **1** item đổi hẳn Pass/Fail · **28** item cùng kết quả nhưng giá trị hiển thị khác nhau · 6 item khác nhau chỉ vì dữ liệu chạy (đã tách riêng, không tính là phát hiện) |
| Sai lệch so với kết luận Task 1 | **4** item (3 item Task 1 chấm Pass thực ra Fail; 1 item Task 1 chấm Fail nhưng Pass trên Chromium) |

> **Đọc nhãn platform cho đúng.** "Chrome / Firefox / Safari" trong mọi bảng và trong overlay ảnh là **vai trò theo đề**, không phải tên bundle đã chạy. Cả ba là browser build do Playwright quản lý, chạy headed trên máy thật: P1 là *Google Chrome for Testing* (Blink), P2 là Firefox bundle `Nightly.app` (Gecko), P3 là **WebKit build của Playwright — không phải `Safari.app`** (cùng engine `AppleWebKit/605.1.15` · `Version/26.5`, tức cùng lớp render/JS/CSS/validation với Safari, nhưng vỏ ứng dụng khác). Vì vậy trong 18 ảnh cửa sổ thật, menu bar macOS hiện tên **"Playwright"** chứ không phải "Safari" — đó là hệ quả đã biết và đã khai, không phải ảnh sai platform. Khai báo đầy đủ: [platform-matrix.md](platform-matrix.md) §4.

Cách chạy lại toàn bộ:

```bash
cd eshop-sut/backend      && node server.js      # :3000 (drop + seed DB mỗi lần start)
cd eshop-sut/frontend-web && npm run dev         # :5173
cd eshop-sut/tests/cross_platform_testing/harness
./run-all-platforms.sh                 # 66 item × 3 platform, reseed DB trước mỗi platform
node scripts/build-matrix.js           # sinh results-matrix.md + divergences.md
node scripts/capture-platform-proof.js # 6 ảnh cửa sổ thật mỗi platform
node scripts/verify-evidence.js        # cổng kiểm tra bằng chứng (exit 1 nếu thiếu)
```

## 2. Vì sao tự động hoá, và tự động hoá không làm mất tính "thực thi thật"

198 lượt kiểm tay trong 10 giờ là không khả thi; tệ hơn, kiểm tay lần 2–3 trên cùng một checklist mình vừa viết gần như chắc chắn sẽ *nhìn thấy điều mình mong đợi*. Harness giải quyết đúng hai điểm đó:

- Mỗi check **đọc trạng thái thật của app đang chạy** (DOM, computed style, `input.validationMessage`, `validity`, hình học phần tử, dialog native, console) rồi mới kết luận. Contract cấm hard-code kết quả Task 1 (`harness/checks/README.md`, rule 1) — và đúng 4 item đã cho kết quả khác Task 1, bằng chứng là cấm đó có hiệu lực.
- Mỗi check ghi lại **giá trị thô** vào `metrics`. Pass/Fail giống nhau giữa 3 engine không có nghĩa là UI giống nhau — 28/29 khác biệt tìm được thuộc đúng loại này và chỉ lộ ra khi diff giá trị thô.
- Mỗi check chạy trong **browser context mới** (giỏ hàng rỗng, `localStorage` rỗng) đúng như phần Preconditions của test case Task 1; và **DB được seed lại trước mỗi platform** để 3 platform xuất phát từ cùng một trạng thái.

## 3. Phát hiện A — item ĐỔI kết quả giữa các platform (nghiêm trọng nhất)

### XP-01 · `GUI-IA02-14` — Thông báo "bắt buộc nhập" phụ thuộc trình duyệt, không phụ thuộc app

Cùng một build, cùng một DOM, ba kết quả khác nhau khi submit form với field `required` để trống:

| Platform | `navigator.language` | Chuỗi engine hiện ra | Kết quả |
|---|---|---|---|
| P1 Chromium 151 | `vi-VN` | "Vui lòng điền vào trường này." | ✅ Pass |
| P2 Firefox 153 | `en-US` | "Please fill out this field." | ❌ Fail |
| P3 WebKit 26.5 | `vi-VN` | "Fill out this field" | ❌ Fail |

Điểm đắt giá: **WebKit báo locale là `vi-VN` mà vẫn hiện tiếng Anh** — nghĩa là không thể "sửa bằng cách đặt locale". SUT dựa hoàn toàn vào bong bóng validate mặc định của HTML5 `required`, nên yêu cầu "message tiếng Việt nhất quán" bị quyết định bởi *trình duyệt của người dùng*, không phải bởi app. Task 1 chấm Fail (Chrome bản đó hiện tiếng Anh); bản Chromium ở đây hiện tiếng Việt nên Pass — chính sự lật kết quả này là lý do đề bắt phải test nhiều platform.

Bằng chứng: [P1](results/P1-chromium-macos/screenshots/) (Pass, không có ảnh vì Pass) · [P2](results/P2-firefox-macos/screenshots/GUI-IA02-14.png) · [P3](results/P3-webkit-macos/screenshots/GUI-IA02-14.png) · chi tiết `metrics`: [divergences.md §A](divergences.md).

## 4. Phát hiện B — cùng kết quả, hiển thị/hành vi khác nhau (28 item)

Bốn nhóm nguyên nhân, xếp theo mức ảnh hưởng tới người dùng thật:

### XP-02 · Tiền tệ đổi dấu phân cách theo engine — ảnh hưởng 13 item, mọi màn có giá

`toLocaleString()` gọi **không tham số** (Home.jsx:88, ProductDetail.jsx:50, Cart.jsx:57–60, Checkout.jsx) nên kết quả phụ thuộc locale mà engine tự resolve:

| | Trang chủ | Chi tiết SP | Giỏ hàng | Coupon (SAVE10) |
|---|---|---|---|---|
| Chromium (`vi`) | `30.000.000 VND` | `30.000.000 ₫` | `30.000.000 ₫` | `Tiết kiệm: -270.000.000 ₫` |
| **Firefox (`en-US`)** | **`30,000,000 VND`** | **`30,000,000 ₫`** | **`30,000,000 ₫`** | **`Tiết kiệm: -270,000,000 ₫`** |
| WebKit (`vi-VN`) | `30.000.000 VND` | `30.000.000 ₫` | `30.000.000 ₫` | `Tiết kiệm: -270.000.000 ₫` |

Với người mua Việt Nam, `30,000,000` đọc là "ba mươi phẩy..." — sai nghiêm trọng về ngữ nghĩa tiền tệ, và nó chỉ xuất hiện trên Firefox. Ảnh cửa sổ thật cho thấy rõ: [Firefox](results/P2-firefox-macos/platform-proof/01-home.png) vs [Chromium](results/P1-chromium-macos/platform-proof/01-home.png).

13 item có giá trị `metrics` khác nhau đúng vì nguyên nhân này (đếm bằng script trên `results/raw/*.json`): `GUI-IA01-06/07/08`, `GUI-IA02-09/10/11`, `GUI-IA03-04/08/09/10`, `GUI-IA04-12/15`, `GUI-GAP-02`.

### XP-03 · WebKit loại `<button>`/`<a>` khỏi Tab order → 3 nút submit không thể tới bằng bàn phím

`GUI-IA01-13` metric `unreachableControls`:

| Platform | `nativeButtonsInTabOrder` | Control không tới được bằng Tab |
|---|---|---|
| Chromium | `true` | — |
| Firefox | `true` | — |
| **WebKit** | `false` | `/register` "Đăng Ký", `/forgot-password` "Lấy mã OTP", `/checkout` "Xác Nhận Thanh Toán" |

Đây là **hành vi hợp lệ của WebKit/Safari trên macOS** (mặc định "Tab chỉ di chuyển giữa các field"), nhưng hệ quả là người dùng bàn phím trên Safari không tới được nút submit của 3 form. Trên `/login` nút vẫn tới được — vì có `tabIndex={1}`, chính là lỗi khiến item này Fail ở mọi engine (focus vào nút TRƯỚC input).

### XP-04 · `input[type=number]` nhận chữ: hai chế độ hỏng khác nhau

`GUI-IA02-09` — gõ `abc` vào ô Số lượng:

| Platform | `value` sau khi gõ | `validity.badInput` | `validationMessage` | Hệ quả cho app |
|---|---|---|---|---|
| Chromium | `""` | `false` | `""` | `parseInt("")` → **NaN** vào giỏ, app không hề biết |
| **Firefox** | `""` | **`true`** | **"Please enter a number."** | engine chặn, nhưng bằng tiếng Anh |
| WebKit | `""` | `false` | `""` | như Chromium |

Cùng lúc, gõ `-1` được nhận trên **cả 3 engine** (không có `min`) → giỏ hàng hiện `-1` và `-30.000.000 ₫`. Đây là lỗi SUT; engine chỉ khác nhau ở chỗ có tố giác hay không.

### XP-05 · Chẩn đoán lỗi API: Firefox che mất status code

`GUI-IA04-09/16` — chặn `/api/products/1` trả 500:

| Platform | Console |
|---|---|
| Chromium | 4 lỗi, có `"Failed to load resource: … status of 500 (Internal Server Error)"` + `AxiosError` kèm stack |
| WebKit | 4 lỗi, đúng nội dung như Chromium nhưng không kèm stack |
| **Firefox** | 2 lỗi, chỉ `"Error"` / `"Lỗi lấy đơn hàng: Error"` — **không có status code, không có dòng resource** |

Không phải bug của SUT, nhưng là rủi ro vận hành: UI đã không hiện gì (item Fail ở mọi engine), mà trên Firefox console cũng không cho dev biết request nào chết.

## 5. Phát hiện C — 3 item Task 1 chấm Pass nhưng thực đo là Fail

Task 3 không chỉ so sánh platform; chạy lại bằng máy đã lộ 3 chỗ Task 1 kết luận sai (tất cả đều Fail đồng nhất trên **cả 3** platform, nên không phải hiện tượng platform):

| ID | Task 1 | Thực đo | Vì sao Task 1 bỏ sót |
|---|---|---|---|
| `GUI-IA01-08` | Passed | Fail | Task 1 chỉ thử với dữ liệu seed hợp lệ. Khi stub `/api/products/1` trả `price:"ba mươi triệu"`, màn hình render **`NaN ₫`** — đúng điều item yêu cầu không được xảy ra. |
| `GUI-IA01-15` | Passed | Fail | Ở đúng 768px, breakpoint `md:` của Tailwind (`min-width:768px`) đã kích hoạt → grid **3 cột** trong khi item yêu cầu 2. Mắt thường ở 768px rất dễ chấm Pass. |
| `GUI-IA04-12` | Passed | Fail | Item đòi "cả 2 nhánh đúng **và số tiền tính đúng**". Hai nhánh feedback có thật, nhưng coupon `SAVE10` (10%) trên đơn 30.000.000 ₫ hiện **`Tiết kiệm: -270.000.000 ₫`** và **`Thành tiền: 300.000.000 ₫`** (đúng phải là 3.000.000 và 27.000.000) — backend tính `discount = total × (1 − 10)`. Task 1 chỉ kiểm sự hiện diện của 2 nhánh. |

`GUI-IA04-12` là bug **chức năng** nặng nhất tìm được trong Task 3 — không phải bug cross-platform, và được báo cáo đúng bản chất đó (XP-07).

## 6. Bug report

| ID | Tiêu đề | Loại | Severity | Platform bị ảnh hưởng | File |
|---|---|---|---|---|---|
| XP-01 | Message "bắt buộc nhập" là chuỗi của engine, không phải của app | SUT bug — biểu hiện phụ thuộc platform | Major | Firefox, WebKit (Chromium ẩn lỗi) | [issues/XP-01.md](issues/XP-01.md) |
| XP-02 | `toLocaleString()` không locale → tiền tệ VN sai dấu phân cách | SUT bug — biểu hiện phụ thuộc platform | Major | Firefox | [issues/XP-02.md](issues/XP-02.md) |
| XP-03 | 3 nút submit không tới được bằng Tab trên WebKit/Safari | Hành vi engine + khuyết accessibility của SUT | Major | WebKit/Safari | [issues/XP-03.md](issues/XP-03.md) |
| XP-04 | Ô Số lượng nhận `-1`/chữ; chế độ hỏng khác nhau theo engine | SUT bug | Major | cả 3 (biểu hiện khác nhau) | [issues/XP-04.md](issues/XP-04.md) |
| XP-05 | Firefox không log status code khi API 500 (UI cũng không báo) | Rủi ro chẩn đoán | Minor | Firefox | [issues/XP-05.md](issues/XP-05.md) |
| XP-06 | Tràn ngang 24px ở 375px trên Gecko (Home search row) | SUT bug — chỉ lộ trên 1 engine | Minor | Firefox (WebKit 3px) | [issues/XP-06.md](issues/XP-06.md) |
| XP-07 | Coupon `SAVE10` tính ngược: tiết kiệm −270 triệu, thành tiền 300 triệu | SUT bug chức năng (không liên quan platform) | **Blocker** | cả 3 | [issues/XP-07.md](issues/XP-07.md) |

## 7. Giới hạn của lần đo này

1. **Không dùng BrowserStack/LambdaTest** (không còn trial). Thay bằng 3 engine thật chạy headed trên máy thật — đề cho phép phương án thay thế nếu ảnh thể hiện rõ browser/OS/device + URL localhost, và mọi ảnh ở đây đều có. Chi tiết: [platform-matrix.md §4](platform-matrix.md).
2. **P3 là WebKit build của Playwright, không phải `Safari.app`.** Cùng engine (`AppleWebKit/605.1.15`, `Version/26.5`) nên hành vi render/JS/CSS/validation là của Safari, nhưng menu bar hiện "Playwright". Muốn khoá tuyệt đối tiêu chí "Safari": bật `safaridriver` (xem [platform-matrix.md §5](platform-matrix.md)).
3. **P1 là "Google Chrome for Testing"** (cùng Blink, cùng dòng version), không phải Chrome bản người dùng.
4. **Không có platform mobile trong bộ bằng chứng.** Hai profile emulation (iPhone 14, Pixel 7) từng có trong kế hoạch nhưng đã bị **xoá khỏi `harness/lib/platforms.js`**, không phải chỉ ẩn đi: `PLATFORMS` hiện đúng 3 entry (P1/P2/P3) nên `--platforms all` cũng chỉ trả về 3 — không có cờ nào chạy lại được mobile. Lý do xoá: emulation không phải máy thật nên không thoả §6, và giữ lại chỉ làm bộ bằng chứng loãng. Nếu cần platform thứ 4 hợp lệ thì phải chạy `frontend-mobile` bằng Expo Go trên điện thoại thật (đề cho phép, và đó là cách duy nhất còn lại).
5. **`GUI-IA03-15` chỉ quan sát được với 5 sản phẩm seed** — metric `observationLimit` ghi rõ điều này; Pass ở đây không có nghĩa "đã kiểm chứng với danh sách dài".
6. **Kết quả automation phản ánh đúng những gì đo được, không thay thế phán đoán thị giác.** Ví dụ `GUI-IA01-14`: computed `margin-right:-100px` chỉ dành 86px layout cho nút rộng 186px (Fail), nhưng nút vẫn nằm trong container và click được ở 375×812 — cả hai sự thật đều ghi trong `evidence`/`metrics` để người đọc tự đánh giá.

## 8. AI Critique

Ở Task 3, AI sai và thiếu ở đúng một chỗ: lớp bằng chứng, chứ không phải lớp đo. Thiết kế đầu tiên của nó chụp ảnh bằng `page.screenshot()` — mà API này không bao giờ chụp được browser chrome, nên yêu cầu "ảnh phải hiện URL localhost" của đề là không thể thoả; AI không nhận ra vì nó tối ưu cho việc chụp được ảnh, không đối chiếu lại điều kiện chấm điểm. Thanh overlay đầu tiên còn che mất header của SUT — đúng phần mà 15 item IA-03 cần soi. Quy trình chạy đầu tiên thì không seed lại database giữa các platform, tức sẽ làm nhiễu chính phép so sánh mà nó vừa dựng: metric `orderRows` trôi 7/3/5/9/11 theo thứ tự chạy vì các check đặt đơn thật. Lần chụp cửa sổ đầu tiên còn chụp nhầm cửa sổ ứng dụng khác, vì không kiểm tra app nào đang ở tiền cảnh. Bốn lỗi này cùng một bản chất: AI rất giỏi thực hiện phép đo nhưng không tự hỏi "bằng chứng này có chứng minh được điều cần chứng minh không".

Ngược lại, chỗ AI mạnh vượt em là kỷ luật ghi lại giá trị thô của từng lần quan sát. Chính việc bắt mỗi check trả về `metrics` đã biến cảm giác "ba trình duyệt trông như nhau" thành 29 khác biệt đo được, và lôi ra bug coupon tính ngược mà Task 1 em chấm Passed.

Nguyên tắc em rút ra: để AI dựng dụng cụ đo và đọc số, nhưng người phải định nghĩa thế nào là bằng chứng hợp lệ, và luôn hỏi "nếu kết quả này sai thì nó sẽ trông như thế nào" trước khi tin.
