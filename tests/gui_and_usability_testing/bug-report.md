# EShop — Bug Report

- Tổng hợp từ 57 checklist item **Failed** (66 item, 9 Passed), gộp theo nguyên nhân gốc thành **48 bug**.
- Sắp theo mức độ nghiêm trọng.
- Screenshot tương ứng nằm trong `test-cases/screenshots/<checklist-id>.png`.

| Bug | Mức độ | Issue | Tiêu đề | Checklist liên quan |
|---|---|---|---|---|
| BUG-01 | Blocker | [194](https://github.com/trngnneee/eshop-sut/issues/194) | XSS: từ khoá tìm kiếm và tên người dùng render bằng dangerouslySetInnerHTML | GUI-IA04-13 |
| BUG-02 | Blocker | [195](https://github.com/trngnneee/eshop-sut/issues/195) | Tổng tiền thanh toán là input sửa được và gửi thẳng lên API | GUI-IA02-10 |
| BUG-03 | Major | [196](https://github.com/trngnneee/eshop-sut/issues/196) | Ô mật khẩu trang Đăng nhập dùng type=text (không che ký tự) | GUI-IA02-03 |
| BUG-04 | Major | [197](https://github.com/trngnneee/eshop-sut/issues/197) | Lộ lỗi SQL kỹ thuật của backend ra giao diện | GUI-IA04-14 |
| BUG-05 | Major | [198](https://github.com/trngnneee/eshop-sut/issues/198) | Form Đăng nhập dùng tiếng Anh: "Username", "Sign In" | GUI-IA01-01, GUI-IA01-02 |
| BUG-06 | Major | [199](https://github.com/trngnneee/eshop-sut/issues/199) | Heading trang Đăng nhập ghi sai thành "Đăng Ký" | GUI-IA01-11 |
| BUG-07 | Major | [200](https://github.com/trngnneee/eshop-sut/issues/200) | Nút hành động tích cực không dùng màu xanh dương theo spec | GUI-IA01-03, GUI-IA01-04 |
| BUG-08 | Major | [201](https://github.com/trngnneee/eshop-sut/issues/201) | tabindex=1 trên nút Đăng nhập phá thứ tự Tab | GUI-IA01-13 |
| BUG-09 | Major | [202](https://github.com/trngnneee/eshop-sut/issues/202) | Nút "Thêm vào giỏ hàng" lệch khỏi khung ở mobile ≤640px | GUI-IA01-14 |
| BUG-10 | Major | [203](https://github.com/trngnneee/eshop-sut/issues/203) | Field Email dùng type=text trên các form | GUI-IA02-02 |
| BUG-11 | Major | [204](https://github.com/trngnneee/eshop-sut/issues/204) | Regex số điện thoại từ chối số VN bắt đầu bằng 0 | GUI-IA02-06 |
| BUG-12 | Major | [205](https://github.com/trngnneee/eshop-sut/issues/205) | Regex mật khẩu mâu thuẫn với hint (đòi khoảng trắng, cấm ký tự đặc biệt) | GUI-IA02-07 |
| BUG-13 | Major | [206](https://github.com/trngnneee/eshop-sut/issues/206) | Không có route guard cho /checkout | GUI-IA03-12 |
| BUG-14 | Major | [207](https://github.com/trngnneee/eshop-sut/issues/207) | Nút đăng xuất ghi "Thoát" thay vì "Đăng xuất" | GUI-IA03-03 |
| BUG-15 | Major | [208](https://github.com/trngnneee/eshop-sut/issues/208) | Không có trang 404 / xử lý not-found thân thiện | GUI-IA03-05, GUI-IA03-06 |
| BUG-16 | Major | [209](https://github.com/trngnneee/eshop-sut/issues/209) | Link "Giỏ hàng" thiếu badge số lượng và không có feedback khi thêm giỏ | GUI-IA03-02, GUI-IA04-01 |
| BUG-17 | Major | [210](https://github.com/trngnneee/eshop-sut/issues/210) | Click "Thêm vào giỏ hàng" lần đầu bị bỏ qua | GUI-IA04-02 |
| BUG-18 | Major | [211](https://github.com/trngnneee/eshop-sut/issues/211) | Hành động phá huỷ (Xóa giỏ, Hủy đơn) không có dialog xác nhận | GUI-IA04-03, GUI-IA04-04 |
| BUG-19 | Major | [212](https://github.com/trngnneee/eshop-sut/issues/212) | Thiếu loading/error state khi tải dữ liệu | GUI-IA04-08, GUI-IA04-09, GUI-IA04-16 |
| BUG-20 | Major | [213](https://github.com/trngnneee/eshop-sut/issues/213) | Giỏ hàng không được reset sau khi thanh toán thành công | GUI-IA04-15 |
| BUG-21 | Major | [214](https://github.com/trngnneee/eshop-sut/issues/214) | Giỏ hàng mất toàn bộ khi refresh trang | GUI-GAP-01 |
| BUG-22 | Major | [215](https://github.com/trngnneee/eshop-sut/issues/215) | Label không gắn với input (thiếu htmlFor/id) | GUI-GAP-04 |
| BUG-23 | Minor | [216](https://github.com/trngnneee/eshop-sut/issues/216) | Cấu trúc thẻ `<h1>` sai trên nhiều trang | GUI-IA01-09, GUI-IA01-10 |
| BUG-24 | Minor | [217](https://github.com/trngnneee/eshop-sut/issues/217) | Field bắt buộc không có dấu * cạnh nhãn | GUI-IA02-01 |
| BUG-25 | Minor | [218](https://github.com/trngnneee/eshop-sut/issues/218) | Đơn vị tiền "VND" không nhất quán với ký hiệu ₫ | GUI-IA01-06 |
| BUG-26 | Minor | [219](https://github.com/trngnneee/eshop-sut/issues/219) | Nút phụ "← Quay lại" trùng style nút chính | GUI-IA01-05 |
| BUG-27 | Minor | [220](https://github.com/trngnneee/eshop-sut/issues/220) | Title tab trình duyệt cố định "frontend-web" | GUI-IA01-12 |
| BUG-28 | Minor | [221](https://github.com/trngnneee/eshop-sut/issues/221) | Tên sản phẩm bị cắt (truncate) không có tooltip xem đầy đủ | GUI-IA01-16 |
| BUG-29 | Minor | [222](https://github.com/trngnneee/eshop-sut/issues/222) | Quên mật khẩu 2 bước thiếu Step Indicator | GUI-IA02-05 |
| BUG-30 | Minor | [223](https://github.com/trngnneee/eshop-sut/issues/223) | Ô OTP không giới hạn 4 chữ số | GUI-IA02-08 |
| BUG-31 | Minor | [224](https://github.com/trngnneee/eshop-sut/issues/224) | Input số lượng không có ràng buộc min | GUI-IA02-09 |
| BUG-32 | Minor | [225](https://github.com/trngnneee/eshop-sut/issues/225) | Đăng ký thiếu field "Xác nhận mật khẩu" | GUI-IA02-13 |
| BUG-33 | Minor | [226](https://github.com/trngnneee/eshop-sut/issues/226) | Thông báo bắt buộc nhập hiển thị tiếng Anh (HTML5 native) | GUI-IA02-14 |
| BUG-34 | Minor | [227](https://github.com/trngnneee/eshop-sut/issues/227) | Lỗi form đăng nhập đặt DƯỚI nút submit (ngược FR-22) | GUI-IA02-04 |
| BUG-35 | Minor | [228](https://github.com/trngnneee/eshop-sut/issues/228) | Navbar không highlight trang đang chọn | GUI-IA03-01 |
| BUG-36 | Minor | [229](https://github.com/trngnneee/eshop-sut/issues/229) | Thiếu breadcrumb ở các trang con | GUI-IA03-04 |
| BUG-37 | Minor | [230](https://github.com/trngnneee/eshop-sut/issues/230) | Link "Quên mật khẩu?" reload toàn trang | GUI-IA03-07 |
| BUG-38 | Minor | [231](https://github.com/trngnneee/eshop-sut/issues/231) | Trang thanh toán thiếu đường quay lại Giỏ hàng | GUI-IA03-08 |
| BUG-39 | Minor | [232](https://github.com/trngnneee/eshop-sut/issues/232) | Sau khi buộc đăng nhập từ checkout, mất ngữ cảnh (về trang chủ) | GUI-IA03-09 |
| BUG-40 | Minor | [233](https://github.com/trngnneee/eshop-sut/issues/233) | Back ở bước 2 Quên mật khẩu làm mất tiến trình | GUI-IA03-11 |
| BUG-41 | Minor | [234](https://github.com/trngnneee/eshop-sut/issues/234) | /profile khi chưa đăng nhập là ngõ cụt | GUI-IA03-13 |
| BUG-42 | Minor | [235](https://github.com/trngnneee/eshop-sut/issues/235) | Empty state thiếu icon/minh hoạ; tìm kiếm 0 kết quả không có empty state | GUI-IA04-05, GUI-IA04-06 |
| BUG-43 | Minor | [236](https://github.com/trngnneee/eshop-sut/issues/236) | Ảnh sản phẩm có alt rỗng | GUI-IA04-07 |
| BUG-44 | Minor | [237](https://github.com/trngnneee/eshop-sut/issues/237) | Feedback thành công/lỗi dùng alert() native khắp nơi | GUI-IA04-10 |
| BUG-45 | Minor | [238](https://github.com/trngnneee/eshop-sut/issues/238) | Message khoá tài khoản không phân biệt với sai mật khẩu | GUI-IA04-11 |
| BUG-46 | Minor | [239](https://github.com/trngnneee/eshop-sut/issues/239) | Đăng ký thành công không có thông báo xác nhận | GUI-IA04-17 |
| BUG-47 | Minor | [240](https://github.com/trngnneee/eshop-sut/issues/240) | Giỏ hàng không gộp sản phẩm trùng | GUI-GAP-02 |
| BUG-48 | Minor | [241](https://github.com/trngnneee/eshop-sut/issues/241) | Thẻ <html> khai báo lang="en" trong khi UI tiếng Việt | GUI-GAP-03 |

**Phân bố:** Blocker: 2 · Major: 20 · Minor: 26

---

### BUG-01

## Title

[Blocker] XSS: từ khoá tìm kiếm và tên người dùng render bằng dangerouslySetInnerHTML

## Description

Từ khoá tìm kiếm (Home.jsx:62-67) và tên user trên header (App.jsx:26-28) được render qua `dangerouslySetInnerHTML`, không thoát HTML. Payload chứa mã JS sẽ được thực thi.

## Steps to Reproduce

1. Mở trang chủ `localhost:5173/`.
2. Nhập vào ô tìm kiếm: `<img src=x onerror=window.__xss=1>` rồi bấm Tìm.
3. Mở Console kiểm tra biến `window.__xss`.

## Expected Result

Từ khoá hiển thị dạng text thuần, không thực thi JS (`window.__xss` không được đặt).

## Actual Result

- (GUI-IA04-13) Từ khoá tìm kiếm được render bằng dangerouslySetInnerHTML: payload "<img onerror>" THỰC THI JS (window.__xss=1) — lỗ hổng XSS. Tên user ở header cũng render tương tự.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA04-13

## Requirement

FR-24 + README mục 1 (safe rendering)

## Severity

Blocker — Cho phép thực thi JS tuỳ ý trong trình duyệt nạn nhân — lỗ hổng bảo mật nghiêm trọng nhất.

## Screenshot

![GUI-IA04-13](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965772/eshop-hw03/gui-checklist/GUI-IA04-13.png)

---

### BUG-02

## Title

[Blocker] Tổng tiền thanh toán là input sửa được và gửi thẳng lên API

## Description

Ô "Tổng tiền thanh toán" là `input type=number` sửa được (Checkout.jsx:94-103); giá trị sửa tay được gửi thẳng vào `POST /api/checkout` (dòng 44-48) không kiểm tra lại phía server.

## Steps to Reproduce

1. Thêm sản phẩm vào giỏ, đăng nhập, mở `/checkout`.
2. Sửa ô "Tổng tiền thanh toán" thành `1000`.
3. Bấm "Xác Nhận Thanh Toán", xem payload ở Network tab.

## Expected Result

Tổng tiền là giá trị chỉ đọc; số tiền gửi lên server không thể bị sửa từ UI.

## Actual Result

- (GUI-IA02-10) Ô "Tổng tiền thanh toán" là input number sửa được: đổi thành "1000" thành công → số tiền do người dùng nhập được gửi thẳng lên API /api/checkout (lỗi nghiêm trọng).

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA02-10

## Requirement

Heuristic (input constraint)

## Severity

Blocker — Người dùng tự đặt số tiền phải trả → thất thoát doanh thu, lỗi nghiệp vụ nghiêm trọng.

## Screenshot

![GUI-IA02-10](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965726/eshop-hw03/gui-checklist/GUI-IA02-10.png)

---

### BUG-03

## Title

[Major] Ô mật khẩu trang Đăng nhập dùng type=text (không che ký tự)

## Description

Ô Mật khẩu ở form Đăng nhập dùng `type="text"` (Login.jsx:39-45) nên ký tự hiển thị rõ.

## Steps to Reproduce

1. Mở `/login`.
2. Gõ vào ô Mật khẩu.
3. Quan sát ký tự hiển thị.

## Expected Result

Ký tự mật khẩu hiển thị dạng chấm tròn (`type="password"`).

## Actual Result

- (GUI-IA02-03) Ô Mật khẩu trên form Đăng nhập có type="text" → ký tự mật khẩu hiển thị rõ, không được che.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA02-03

## Requirement

FR-22 (password masking)

## Severity

Major — Mật khẩu hiển thị rõ trên màn hình — rủi ro lộ thông tin đăng nhập.

## Screenshot

![GUI-IA02-03](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965713/eshop-hw03/gui-checklist/GUI-IA02-03.png)

---

### BUG-04

## Title

[Major] Lộ lỗi SQL kỹ thuật của backend ra giao diện

## Description

Tìm kiếm với ký tự đặc biệt khiến backend trả về nguyên khối HTML lỗi và frontend render trực tiếp (Home.jsx:69-73).

## Steps to Reproduce

1. Mở `/`.
2. Tìm với từ khoá `'` (một dấu nháy đơn).

## Expected Result

Hiển thị thông báo thân thiện ("Có lỗi xảy ra, thử lại sau"), không lộ SQL/stack.

## Actual Result

- (GUI-IA04-14) Tìm với từ khoá "'" hiển thị nguyên khối lỗi kỹ thuật "Database Error / SQLITE_ERROR" ra UI — lộ chi tiết backend thay vì thông báo thân thiện.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA04-14

## Requirement

Heuristic (error feedback)

## Severity

Major — Lộ thông tin nội bộ (SQLITE_ERROR) hỗ trợ tấn công; trải nghiệm kém.

## Screenshot

![GUI-IA04-14](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965773/eshop-hw03/gui-checklist/GUI-IA04-14.png)

---

### BUG-05

## Title

[Major] Form Đăng nhập dùng tiếng Anh: "Username", "Sign In"

## Description

Nhãn ô nhập là "Username" và nút submit là "Sign In" (Login.jsx:28,58), lẫn tiếng Anh giữa UI tiếng Việt.

## Steps to Reproduce

1. Mở `/login`.
2. Đọc nhãn field và nút submit.

## Expected Result

Nhãn tiếng Việt ("Email"/"Tên đăng nhập"), nút "Đăng nhập".

## Actual Result

- (GUI-IA01-01) Nhãn field: "Username | Mật khẩu"; nút submit: "Sign In". Màn đăng nhập vẫn dùng chuỗi tiếng Anh ("Username", "Sign In") thay vì tiếng Việt.
- (GUI-IA01-02) Còn chuỗi tiếng Anh không phải thuật ngữ chuẩn trên UI: Username, Sign In (màn Đăng nhập).

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA01-01, GUI-IA01-02

## Requirement

FR-21 (nhất quán ngôn ngữ)

## Severity

Major — Vi phạm quy tắc nhất quán ngôn ngữ FR-21 trên màn hình chính.

## Screenshot

![GUI-IA01-01](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965687/eshop-hw03/gui-checklist/GUI-IA01-01.png) ![GUI-IA01-02](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965688/eshop-hw03/gui-checklist/GUI-IA01-02.png)

---

### BUG-06

## Title

[Major] Heading trang Đăng nhập ghi sai thành "Đăng Ký"

## Description

Trang `/login` hiển thị heading "Đăng Ký" (Login.jsx:24) sai với chức năng.

## Steps to Reproduce

1. Mở `/login`.
2. Đọc heading đầu form.

## Expected Result

Heading là "Đăng Nhập".

## Actual Result

- (GUI-IA01-11) Heading trang /login là "Đăng Ký" — sai chức năng (ghi "Đăng Ký" trên trang Đăng nhập).

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA01-11

## Requirement

FR-21 (tiêu đề trang)

## Severity

Major — Gây nhầm lẫn chức năng trang.

## Screenshot

![GUI-IA01-11](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965701/eshop-hw03/gui-checklist/GUI-IA01-11.png)

---

### BUG-07

## Title

[Major] Nút hành động tích cực không dùng màu xanh dương theo spec

## Description

Nút "Đăng Ký" nền đỏ (Register.jsx:71-76); các nút tích cực khác (thêm giỏ/thanh toán xanh lá, áp mã cam) — không nút nào dùng xanh dương như spec.

## Steps to Reproduce

1. Mở lần lượt Đăng ký, Chi tiết SP, Giỏ hàng, Thanh toán.
2. Quan sát màu nền các nút hành động tích cực.

## Expected Result

Tất cả nút hành động tích cực đồng nhất màu xanh dương.

## Actual Result

- (GUI-IA01-03) Nút "Đăng Ký" có màu nền rgb(239, 68, 68) (đỏ, bg-red-500) — dùng màu cảnh báo cho hành động tích cực thay vì xanh dương.
- (GUI-IA01-04) Nút "Thêm vào giỏ hàng" (Chi tiết SP) màu rgb(22, 163, 74) — xanh lá, không phải xanh dương. Các nút tích cực khác (thanh toán xanh lá, áp mã cam) cũng lệch spec.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA01-03, GUI-IA01-04

## Requirement

FR-21 (nhất quán màu sắc)

## Severity

Major — Vi phạm quy tắc màu FR-21 trên nhiều nút mua hàng/đăng ký.

## Screenshot

![GUI-IA01-03](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965690/eshop-hw03/gui-checklist/GUI-IA01-03.png) ![GUI-IA01-04](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965691/eshop-hw03/gui-checklist/GUI-IA01-04.png)

---

### BUG-08

## Title

[Major] tabindex=1 trên nút Đăng nhập phá thứ tự Tab

## Description

Nút submit form Đăng nhập có `tabIndex={1}` (Login.jsx:56) nên được focus trước các input.

## Steps to Reproduce

1. Mở `/login`.
2. Nhấn Tab liên tục từ đầu trang, ghi lại thứ tự focus.

## Expected Result

Tab đi lần lượt các ô nhập rồi mới tới nút submit.

## Actual Result

- (GUI-IA01-13) Nút submit form Đăng nhập có tabindex="1" → được focus TRƯỚC các ô input, phá thứ tự Tab tự nhiên.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA01-13

## Requirement

FR-21 (tab order)

## Severity

Major — Bàn phím focus vào nút submit trước các ô nhập — cản trở thao tác keyboard/accessibility.

## Screenshot

![GUI-IA01-13](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965704/eshop-hw03/gui-checklist/GUI-IA01-13.png)

---

### BUG-09

## Title

[Major] Nút "Thêm vào giỏ hàng" lệch khỏi khung ở mobile ≤640px

## Description

Class `bug-mobile-hidden` áp `margin-right:-100px` ở ≤640px (index.css:10-14) đẩy nút lệch/tràn khỏi khung.

## Steps to Reproduce

1. Mở `/product/1`.
2. Bật DevTools device toolbar, đặt viewport 375px.
3. Quan sát vị trí nút "Thêm vào giỏ hàng".

## Expected Result

Nút nằm trọn trong khung, bấm được ở 375px.

## Actual Result

- (GUI-IA01-14) Ở viewport 375px, nút "Thêm vào giỏ hàng" có margin-right -100px (class bug-mobile-hidden) → bị đẩy lệch/tràn khỏi khung.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA01-14

## Requirement

Heuristic (responsive)

## Severity

Major — Chức năng chính không dùng được trên mobile.

## Screenshot

![GUI-IA01-14](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965705/eshop-hw03/gui-checklist/GUI-IA01-14.png)

---

### BUG-10

## Title

[Major] Field Email dùng type=text trên các form

## Description

Cả 3 form dùng `type="text"` cho ô email.

## Steps to Reproduce

1. Mở `/register`.
2. Nhập `abc` vào ô email và submit.

## Expected Result

Ô email dùng `type="email"`, chặn định dạng sai.

## Actual Result

- (GUI-IA02-02) Field email dùng type: {"/register":"text","/login":"text","/forgot-password":"text"} — đang là "text" thay vì "email", không chặn định dạng sai ở tầng trình duyệt.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA02-02

## Requirement

FR-22 (input type)

## Severity

Major — Không validate định dạng email phía client; bàn phím mobile không tối ưu.

## Screenshot

![GUI-IA02-02](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965711/eshop-hw03/gui-checklist/GUI-IA02-02.png)

---

### BUG-11

## Title

[Major] Regex số điện thoại từ chối số VN bắt đầu bằng 0

## Description

Regex `/^[1-9][0-9]{8,9}$/` (Profile.jsx:44) loại số bắt đầu bằng 0, mâu thuẫn chính placeholder "0912345678".

## Steps to Reproduce

1. Đăng nhập, mở `/profile`.
2. Nhập `0912345678` vào ô SĐT, bấm Cập nhật.

## Expected Result

Số `0912345678` được chấp nhận.

## Actual Result

- (GUI-IA02-06) Nhập SĐT hợp lệ "0912345678" bị từ chối: "Số điện thoại không hợp lệ. Vui lòng nhập đúng 9-10 chữ số." — regex yêu cầu số đầu 1-9 nên loại số VN bắt đầu bằng 0, mâu thuẫn với placeholder.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA02-06

## Requirement

FR-22 (format constraints: phone)

## Severity

Major — Người dùng nhập SĐT hợp lệ vẫn bị chặn — không cập nhật được hồ sơ.

## Screenshot

![GUI-IA02-06](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965717/eshop-hw03/gui-checklist/GUI-IA02-06.png)

---

### BUG-12

## Title

[Major] Regex mật khẩu mâu thuẫn với hint (đòi khoảng trắng, cấm ký tự đặc biệt)

## Description

Regex yêu cầu có khoảng trắng và chỉ cho phép `[A-Za-z\d\s]` (Register.jsx:16-19) trong khi hint ghi cần "ký tự đặc biệt".

## Steps to Reproduce

1. Mở `/register`.
2. Nhập mật khẩu `Abcdef1!` (đủ điều kiện theo hint) và submit.

## Expected Result

Mật khẩu đúng như hint được chấp nhận; validate và hint không mâu thuẫn.

## Actual Result

- (GUI-IA02-07) Mật khẩu "Abcdef1!" (đủ hoa/thường/số/ký tự đặc biệt như hint) bị từ chối: "Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT." — regex thực tế bắt buộc có khoảng trắng và cấm ký tự đặc biệt, mâu thuẫn với hint.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA02-07

## Requirement

FR-22 (validation)

## Severity

Major — Mật khẩu đúng như hướng dẫn vẫn bị từ chối — chặn đăng ký/đổi mật khẩu.

## Screenshot

![GUI-IA02-07](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965719/eshop-hw03/gui-checklist/GUI-IA02-07.png)

---

### BUG-13

## Title

[Major] Không có route guard cho /checkout

## Description

Truy cập thẳng `/checkout` khi giỏ trống và chưa đăng nhập vẫn hiển thị form (tổng 0 ₫), không redirect.

## Steps to Reproduce

1. Đăng xuất, giỏ trống.
2. Truy cập thẳng `localhost:5173/checkout`.

## Expected Result

Giỏ trống → về giỏ hàng; chưa login → về đăng nhập.

## Actual Result

- (GUI-IA03-12) Vào thẳng /checkout khi giỏ trống & chưa đăng nhập vẫn hiển thị form thanh toán (tổng 0 ₫), không bị redirect — thiếu route guard.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA03-12

## Requirement

Heuristic (route guarding)

## Severity

Major — Vào thẳng thanh toán khi giỏ trống/chưa đăng nhập — luồng nghiệp vụ sai.

## Screenshot

![GUI-IA03-12](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965749/eshop-hw03/gui-checklist/GUI-IA03-12.png)

---

### BUG-14

## Title

[Major] Nút đăng xuất ghi "Thoát" thay vì "Đăng xuất"

## Description

Nút đăng xuất trên header ghi "Thoát" (App.jsx:29).

## Steps to Reproduce

1. Đăng nhập.
2. Đọc nhãn nút đăng xuất trên header.

## Expected Result

Nhãn đúng "Đăng xuất".

## Actual Result

- (GUI-IA03-03) Nút đăng xuất trên header ghi "Thoát" thay vì đúng nhãn "Đăng xuất" theo FR-23.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA03-03

## Requirement

FR-23 (exact label wording)

## Severity

Major — Sai nhãn theo yêu cầu FR-23.

## Screenshot

![GUI-IA03-03](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965735/eshop-hw03/gui-checklist/GUI-IA03-03.png)

---

### BUG-15

## Title

[Major] Không có trang 404 / xử lý not-found thân thiện

## Description

Không có route catch-all (App.jsx:50-59) → `/abc` render vùng trống; `/product/999` hiện text "Lỗi trắng trang do data rỗng" không có link về.

## Steps to Reproduce

1. Truy cập `/abc-khong-ton-tai`.
2. Truy cập `/product/999`.

## Expected Result

Hiển thị trang 404/not-found thân thiện có link về trang chủ.

## Actual Result

- (GUI-IA03-05) URL không tồn tại /abc-khong-ton-tai render vùng nội dung trống ("") — không có route catch-all, không có trang 404 thân thiện.
- (GUI-IA03-06) /product/999 hiển thị text kỹ thuật "Sản phẩm không tồn tại (Lỗi trắng trang do data rỗng)" và không có link quay về — không thân thiện, không lối thoát.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA03-05, GUI-IA03-06

## Requirement

Heuristic (invalid-URL/404)

## Severity

Major — URL sai hoặc sản phẩm không tồn tại cho trang trắng / text kỹ thuật, không lối thoát.

## Screenshot

![GUI-IA03-05](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965739/eshop-hw03/gui-checklist/GUI-IA03-05.png) ![GUI-IA03-06](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965740/eshop-hw03/gui-checklist/GUI-IA03-06.png)

---

### BUG-16

## Title

[Major] Link "Giỏ hàng" thiếu badge số lượng và không có feedback khi thêm giỏ

## Description

Link "Giỏ hàng" là link trần không badge (App.jsx:23); bấm "Thêm vào giỏ" ở trang chủ không có toast/badge nào (Home.jsx:98-103).

## Steps to Reproduce

1. Mở `/`.
2. Bấm "Thêm vào giỏ" một sản phẩm.
3. Quan sát header và vùng thao tác.

## Expected Result

Header có badge số lượng cập nhật tức thì; có phản hồi trực quan khi thêm giỏ.

## Actual Result

- (GUI-IA03-02) Link "Giỏ hàng" là link trần, không có badge số lượng; sau khi thêm 1 SP header vẫn không hiển thị counter. Header: "EShop Giỏ hàng Đăng nhập Đăng ký".
- (GUI-IA04-01) Bấm "Thêm vào giỏ" ở trang chủ không có phản hồi trực quan nào (không toast, không badge cập nhật trên header).

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA03-02, GUI-IA04-01

## Requirement

FR-23 (badge) + FR-24 (feedback)

## Severity

Major — Người dùng không biết đã thêm thành công hay giỏ có bao nhiêu món.

## Screenshot

![GUI-IA03-02](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965733/eshop-hw03/gui-checklist/GUI-IA03-02.png) ![GUI-IA04-01](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965753/eshop-hw03/gui-checklist/GUI-IA04-01.png)

---

### BUG-17

## Title

[Major] Click "Thêm vào giỏ hàng" lần đầu bị bỏ qua

## Description

Biến `clickCount` nuốt lần bấm đầu tiên (ProductDetail.jsx:22-32); phải bấm lần 2 mới có tác dụng.

## Steps to Reproduce

1. Mở `/product/1`.
2. Bấm "Thêm vào giỏ hàng" đúng 1 lần.
3. Mở giỏ kiểm tra.

## Expected Result

Bấm 1 lần → sản phẩm vào giỏ ngay + hiện "Đã thêm".

## Actual Result

- (GUI-IA04-02) Click "Thêm vào giỏ hàng" lần đầu bị "nuốt" (clickCount): không có feedback "Đã thêm" và giỏ vẫn trống (0 dòng) — mất 1 lần thao tác.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA04-02

## Requirement

FR-24 (add-to-cart feedback)

## Severity

Major — Mất thao tác người dùng; sản phẩm không vào giỏ ở lần bấm đầu.

## Screenshot

![GUI-IA04-02](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965754/eshop-hw03/gui-checklist/GUI-IA04-02.png)

---

### BUG-18

## Title

[Major] Hành động phá huỷ (Xóa giỏ, Hủy đơn) không có dialog xác nhận

## Description

Bấm "Xóa" (Cart.jsx:50-55) và "Hủy đơn" (Profile.jsx:200-208) thực hiện ngay, không hỏi xác nhận.

## Steps to Reproduce

1. Mở `/cart` có hàng, bấm "Xóa".
2. Mở `/profile`, bấm "Hủy đơn" một đơn chưa giao.

## Expected Result

Có dialog xác nhận trước khi xoá/huỷ; chọn Hủy → giữ nguyên.

## Actual Result

- (GUI-IA04-03) Bấm "Xóa" item xoá ngay (dòng giỏ 1→0) không có dialog xác nhận — thao tác phá huỷ không có bước chặn.
- (GUI-IA04-04) Bấm "Hủy đơn" huỷ ngay, không có dialog xác nhận trước hành động không hoàn tác (chỉ có alert "Hủy đơn thành công" sau khi đã huỷ).

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA04-03, GUI-IA04-04

## Requirement

FR-24 (confirmation dialog)

## Severity

Major — Dễ mất dữ liệu do bấm nhầm, không hoàn tác được.

## Screenshot

![GUI-IA04-03](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965756/eshop-hw03/gui-checklist/GUI-IA04-03.png) ![GUI-IA04-04](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965757/eshop-hw03/gui-checklist/GUI-IA04-04.png)

---

### BUG-19

## Title

[Major] Thiếu loading/error state khi tải dữ liệu

## Description

Home fetch không loading (Home.jsx:13-30); Chi tiết SP kẹt "Đang tải..." khi lỗi (ProductDetail.jsx:15-20); lỗi tải đơn bị nuốt thành "chưa có đơn" (Profile.jsx:26-29).

## Steps to Reproduce

1. Bật Network Slow 3G, mở `/`.
2. Tắt backend, mở `/product/1`.
3. Làm lỗi `/api/orders/my-orders`, mở `/profile`.

## Expected Result

Có spinner/skeleton khi chờ; lỗi có error state riêng, phân biệt với empty.

## Actual Result

- (GUI-IA04-08) Khi API bị làm chậm, trang chủ không hiển thị spinner/skeleton nào (số phần tử loading: 0) — người dùng thấy trang trống trong lúc chờ.
- (GUI-IA04-09) Khi API sản phẩm lỗi, trang kẹt ở "Đang tải..." (không có error state / nút thử lại) — chỉ log console, kẹt "Đang tải..." vô hạn.
- (GUI-IA04-16) Lỗi API tải đơn bị "nuốt" (catch → setOrders([])) nên hiển thị "Bạn chưa có đơn hàng nào" giống hệt trạng thái trống — không phân biệt lỗi với empty.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA04-08, GUI-IA04-09, GUI-IA04-16

## Requirement

Heuristic (loading/error state)

## Severity

Major — Trang trống hoặc kẹt "Đang tải...", lỗi API bị nhầm thành trạng thái trống.

## Screenshot

![GUI-IA04-08](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965764/eshop-hw03/gui-checklist/GUI-IA04-08.png) ![GUI-IA04-09](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965766/eshop-hw03/gui-checklist/GUI-IA04-09.png) ![GUI-IA04-16](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965777/eshop-hw03/gui-checklist/GUI-IA04-16.png)

---

### BUG-20

## Title

[Major] Giỏ hàng không được reset sau khi thanh toán thành công

## Description

`clearCart` được import nhưng không bao giờ gọi (Checkout.jsx:9,62).

## Steps to Reproduce

1. Thêm SP, đăng nhập, hoàn tất thanh toán.
2. Mở lại `/cart`.

## Expected Result

Giỏ trống sau khi đặt hàng thành công.

## Actual Result

- (GUI-IA04-15) Sau thanh toán thành công, giỏ hàng vẫn còn 1 sản phẩm cũ (clearCart không được gọi) — trạng thái giỏ không được reset.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA04-15

## Requirement

Heuristic (state consistency)

## Severity

Major — Giỏ còn hàng cũ sau khi đặt, dễ đặt trùng.

## Screenshot

![GUI-IA04-15](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965775/eshop-hw03/gui-checklist/GUI-IA04-15.png)

---

### BUG-21

## Title

[Major] Giỏ hàng mất toàn bộ khi refresh trang

## Description

Giỏ chỉ nằm trong React state (CartContext.jsx:6), không lưu localStorage (trong khi token thì có).

## Steps to Reproduce

1. Thêm SP vào giỏ.
2. Nhấn F5.
3. Mở `/cart`.

## Expected Result

Giỏ giữ nguyên sản phẩm sau reload.

## Actual Result

- (GUI-GAP-01) Thêm SP vào giỏ rồi F5 (reload) → giỏ trống (0 dòng). Giỏ chỉ nằm trong React state, không lưu localStorage (trong khi token thì có).

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-GAP-01

## Requirement

Heuristic (state persistence)

## Severity

Major — Reload là mất giỏ — trải nghiệm mua sắm gãy.

## Screenshot

![GUI-GAP-01](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965680/eshop-hw03/gui-checklist/GUI-GAP-01.png)

---

### BUG-22

## Title

[Major] Label không gắn với input (thiếu htmlFor/id)

## Description

Không `<label>` nào trên 4 form có `htmlFor` gắn với `id` input.

## Steps to Reproduce

1. Mở một form bất kỳ.
2. Click vào chữ nhãn (vd "Mật khẩu").

## Expected Result

Click nhãn → focus vào ô input tương ứng.

## Actual Result

- (GUI-GAP-04) Không label nào trên các form (Đăng nhập/Đăng ký/Quên MK/Hồ sơ) có thuộc tính htmlFor/for gắn với input — click nhãn không focus vào ô, screen reader không đọc được tên field (WCAG 1.3.1, 4.1.2).

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-GAP-04

## Requirement

Heuristic / WCAG (label association)

## Severity

Major — Click nhãn không focus ô nhập; screen reader không đọc được tên field (WCAG 1.3.1/4.1.2).

## Screenshot

![GUI-GAP-04](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965685/eshop-hw03/gui-checklist/GUI-GAP-04.png)

---

### BUG-23

## Title

[Minor] Cấu trúc thẻ <h1> sai trên nhiều trang

## Description

Trang chủ có 2 `<h1>` (Home.jsx:44,110); 6 trang (login/register/forgot/cart/checkout/profile) không có `<h1>` nào.

## Steps to Reproduce

1. Mở từng trang, chạy `document.querySelectorAll('h1').length`.

## Expected Result

Mỗi trang có đúng 1 `<h1>` mô tả nội dung.

## Actual Result

- (GUI-IA01-09) Trang chủ có 2 thẻ <h1> (tiêu đề "Danh sách sản phẩm" và dòng đếm "Hiển thị N sản phẩm" đều là h1) — vượt quá 1.
- (GUI-IA01-10) Số thẻ <h1> mỗi trang: /login=0, /register=0, /forgot-password=0, /cart=0, /checkout=0, /profile=0 — các trang này chỉ có <h2>, thiếu <h1> mô tả nội dung.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA01-09, GUI-IA01-10

## Requirement

FR-21 (tiêu đề trang)

## Severity

Minor — Ảnh hưởng SEO và screen reader (đọc cấu trúc trang).

## Screenshot

![GUI-IA01-09](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965698/eshop-hw03/gui-checklist/GUI-IA01-09.png) ![GUI-IA01-10](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965699/eshop-hw03/gui-checklist/GUI-IA01-10.png)

---

### BUG-24

## Title

[Minor] Field bắt buộc không có dấu * cạnh nhãn

## Description

Không field `required` nào hiển thị dấu `*`.

## Steps to Reproduce

1. Mở các form, đối chiếu field required với dấu *.

## Expected Result

Mỗi field bắt buộc có dấu `*` cạnh nhãn.

## Actual Result

- (GUI-IA02-01) Không field bắt buộc nào có dấu "*" cạnh nhãn trên các form (Đăng ký, Đăng nhập, Quên MK, Hồ sơ).

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA02-01

## Requirement

FR-22 (required indicator)

## Severity

Minor — Người dùng không biết field nào bắt buộc.

## Screenshot

![GUI-IA02-01](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965709/eshop-hw03/gui-checklist/GUI-IA02-01.png)

---

### BUG-25

## Title

[Minor] Đơn vị tiền "VND" không nhất quán với ký hiệu ₫

## Description

Card trang chủ hiển thị "30,000,000 VND" (Home.jsx:87-89) trong khi các màn khác dùng ₫.

## Steps to Reproduce

1. Mở `/`, quan sát đơn vị tiền trên card.

## Expected Result

Dùng ký hiệu ₫ thống nhất toàn app.

## Actual Result

- (GUI-IA01-06) Giá trên card trang chủ hiển thị "30,000,000 VND" dùng "VND", trong khi các màn khác dùng ký hiệu ₫ — không nhất quán.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA01-06

## Requirement

FR-21 (đơn vị tiền)

## Severity

Minor — Không nhất quán đơn vị tiền theo FR-21.

## Screenshot

![GUI-IA01-06](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965695/eshop-hw03/gui-checklist/GUI-IA01-06.png)

---

### BUG-26

## Title

[Minor] Nút phụ "← Quay lại" trùng style nút chính

## Description

Nút "Đặt lại mật khẩu" và "← Quay lại" cùng nền xanh lá, full-width (ForgotPassword.jsx:91-96).

## Steps to Reproduce

1. Vào bước 2 của `/forgot-password`.
2. Quan sát 2 nút.

## Expected Result

Nút phụ có style thứ cấp, phân biệt rõ với nút submit.

## Actual Result

- (GUI-IA01-05) Nút chính "Đặt lại mật khẩu" (rgb(22, 163, 74)) và nút phụ "← Quay lại" (rgb(22, 163, 74)) cùng nền xanh lá, full-width — không phân biệt được thị giác.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA01-05

## Requirement

Heuristic (visual hierarchy)

## Severity

Minor — Dễ bấm nhầm nút hành động chính.

## Screenshot

![GUI-IA01-05](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965693/eshop-hw03/gui-checklist/GUI-IA01-05.png)

---

### BUG-27

## Title

[Minor] Title tab trình duyệt cố định "frontend-web"

## Description

Title cố định "frontend-web" (index.html:7), không đổi theo trang.

## Steps to Reproduce

1. Mở các trang khác nhau, quan sát tiêu đề tab.

## Expected Result

Title dạng "EShop — <tên trang>", đổi theo trang.

## Actual Result

- (GUI-IA01-12) Title tab cố định "frontend-web" ở trang chủ và "frontend-web" ở /login — không đổi theo trang, không mô tả nội dung.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA01-12

## Requirement

Heuristic (page title)

## Severity

Minor — Không mô tả trang, khó phân biệt tab.

## Screenshot

![GUI-IA01-12](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965702/eshop-hw03/gui-checklist/GUI-IA01-12.png)

---

### BUG-28

## Title

[Minor] Tên sản phẩm bị cắt (truncate) không có tooltip xem đầy đủ

## Description

Class `truncate` (Home.jsx:86) cắt tên nhưng không có thuộc tính `title`.

## Steps to Reproduce

1. Seed sản phẩm tên dài, mở `/`, rê chuột lên tên.

## Expected Result

Có tooltip/title hiển thị tên đầy đủ.

## Actual Result

- (GUI-IA01-16) Tên sản phẩm dùng class "truncate" để cắt gọn nhưng KHÔNG có thuộc tính title/tooltip → không có cách xem đầy đủ tên khi bị cắt.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA01-16

## Requirement

Heuristic (text overflow)

## Severity

Minor — Không xem được tên đầy đủ khi bị cắt.

## Screenshot

![GUI-IA01-16](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965707/eshop-hw03/gui-checklist/GUI-IA01-16.png)

---

### BUG-29

## Title

[Minor] Quên mật khẩu 2 bước thiếu Step Indicator

## Description

Luồng 2 bước không có chỉ dẫn bước (ForgotPassword.jsx:46-98).

## Steps to Reproduce

1. Đi qua bước 1 → bước 2, tìm chỉ dẫn bước.

## Expected Result

Hiển thị "Bước 1/2", "Bước 2/2" hoặc tương đương.

## Actual Result

- (GUI-IA02-05) Luồng Quên mật khẩu 2 bước không có Step Indicator ở cả bước 1 lẫn bước 2 (không có chỉ dẫn "Bước 1/2", "Bước 2/2").

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA02-05

## Requirement

FR-22 (step indicator)

## Severity

Minor — Người dùng không biết đang ở bước nào.

## Screenshot

![GUI-IA02-05](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965716/eshop-hw03/gui-checklist/GUI-IA02-05.png)

---

### BUG-30

## Title

[Minor] Ô OTP không giới hạn 4 chữ số

## Description

Ô OTP nhận "123456abcd" — không có maxLength/pattern (ForgotPassword.jsx:71-77).

## Steps to Reproduce

1. Vào bước 2, nhập `123456abcd` vào ô OTP.

## Expected Result

Chỉ nhận tối đa 4 chữ số.

## Actual Result

- (GUI-IA02-08) Ô OTP (nhãn "4 số") nhận giá trị "123456abcd" (dài 10, cả chữ) — không có maxLength/pattern giới hạn 4 chữ số.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA02-08

## Requirement

FR-22 (format constraints)

## Severity

Minor — Nhận input sai định dạng so với nhãn "4 số".

## Screenshot

![GUI-IA02-08](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965722/eshop-hw03/gui-checklist/GUI-IA02-08.png)

---

### BUG-31

## Title

[Minor] Input số lượng không có ràng buộc min

## Description

Input số lượng không có `min` (ProductDetail.jsx:57-62), nhập được `-1`.

## Steps to Reproduce

1. Mở `/product/1`, đặt số lượng `-1` rồi thêm vào giỏ.

## Expected Result

Số lượng <1 bị chặn/chuẩn hoá về 1.

## Actual Result

- (GUI-IA02-09) Input số lượng không có ràng buộc min (min=null); nhập được giá trị "-1" (<1) — cho phép số lượng vô lý.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA02-09

## Requirement

FR-22 (format constraints: quantity)

## Severity

Minor — Cho phép số lượng ≤0 hoặc vô lý vào giỏ.

## Screenshot

![GUI-IA02-09](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965724/eshop-hw03/gui-checklist/GUI-IA02-09.png)

---

### BUG-32

## Title

[Minor] Đăng ký thiếu field "Xác nhận mật khẩu"

## Description

Form không có field xác nhận mật khẩu (Register.jsx:35-81).

## Steps to Reproduce

1. Mở `/register`, tìm field xác nhận mật khẩu.

## Expected Result

Có field xác nhận và kiểm tra khớp.

## Actual Result

- (GUI-IA02-13) Form đăng ký KHÔNG có field "Xác nhận mật khẩu" — thiếu cơ chế kiểm tra khớp mật khẩu.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA02-13

## Requirement

Heuristic (confirmation field)

## Severity

Minor — Không phát hiện lỗi gõ mật khẩu.

## Screenshot

![GUI-IA02-13](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965728/eshop-hw03/gui-checklist/GUI-IA02-13.png)

---

### BUG-33

## Title

[Minor] Thông báo bắt buộc nhập hiển thị tiếng Anh (HTML5 native)

## Description

Dựa vào `required` native → tooltip "Please fill out this field." theo ngôn ngữ trình duyệt.

## Steps to Reproduce

1. Submit form khi để trống field bắt buộc.

## Expected Result

Thông báo required bằng tiếng Việt, cùng style lỗi khác.

## Actual Result

- (GUI-IA02-14) Thông báo required dựa vào HTML5 native → hiển thị theo ngôn ngữ trình duyệt: "Please fill out this field." (tiếng Anh), không nhất quán tiếng Việt với các lỗi khác của app.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA02-14

## Requirement

Heuristic (validation consistency)

## Severity

Minor — Không nhất quán ngôn ngữ.

## Screenshot

![GUI-IA02-14](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965730/eshop-hw03/gui-checklist/GUI-IA02-14.png)

---

### BUG-34

## Title

[Minor] Lỗi form đăng nhập đặt DƯỚI nút submit (ngược FR-22)

## Description

Lỗi đăng nhập render dưới nút submit (Login.jsx:66); Quên MK/Hồ sơ còn dùng alert().

## Steps to Reproduce

1. Mở `/login`, nhập sai và submit, quan sát vị trí lỗi so với nút.

## Expected Result

Lỗi hiển thị trong trang, phía TRÊN nút submit.

## Actual Result

- (GUI-IA02-04) Thông báo lỗi đăng nhập nằm DƯỚI nút submit (errY=517, btnY=425) — ngược yêu cầu FR-22 (lỗi phải phía TRÊN nút submit). Quên MK/Hồ sơ còn dùng alert() native.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA02-04

## Requirement

FR-22 (message placement)

## Severity

Minor — Vi phạm quy tắc đặt lỗi phía trên nút submit.

## Screenshot

![GUI-IA02-04](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965714/eshop-hw03/gui-checklist/GUI-IA02-04.png)

---

### BUG-35

## Title

[Minor] Navbar không highlight trang đang chọn

## Description

Link navbar chỉ có `hover:underline`, không có active state (App.jsx:22-37).

## Steps to Reproduce

1. Điều hướng tới `/cart`, quan sát link "Giỏ hàng".

## Expected Result

Link trang hiện tại có style active.

## Actual Result

- (GUI-IA03-01) Ở /cart, link "Giỏ hàng" trên navbar chỉ có class "hover:underline" (chỉ hover:underline), không có active-state (aria-current/đậm/đổi màu) để chỉ mục đang chọn.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA03-01

## Requirement

FR-23 (active highlight)

## Severity

Minor — Người dùng không biết đang ở mục nào.

## Screenshot

![GUI-IA03-01](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965731/eshop-hw03/gui-checklist/GUI-IA03-01.png)

---

### BUG-36

## Title

[Minor] Thiếu breadcrumb ở các trang con

## Description

3 trang con không có breadcrumb.

## Steps to Reproduce

1. Mở Chi tiết SP / Giỏ hàng / Thanh toán, tìm breadcrumb.

## Expected Result

Có breadcrumb đúng cấp, click được.

## Actual Result

- (GUI-IA03-04) Các trang con thiếu breadcrumb: /product/1, /cart, /checkout — không có chỉ dẫn cấp điều hướng ("Trang chủ > ...").

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA03-04

## Requirement

FR-23 (breadcrumb)

## Severity

Minor — Thiếu chỉ dẫn cấp điều hướng.

## Screenshot

![GUI-IA03-04](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965737/eshop-hw03/gui-checklist/GUI-IA03-04.png)

---

### BUG-37

## Title

[Minor] Link "Quên mật khẩu?" reload toàn trang

## Description

Dùng thẻ `<a href>` (Login.jsx:49-51) gây full page load.

## Steps to Reproduce

1. Mở `/login`, bấm "Quên mật khẩu?", quan sát Network tab.

## Expected Result

Điều hướng SPA, không reload toàn trang.

## Actual Result

- (GUI-IA03-07) Link "Quên mật khẩu?" dùng <a href> gây tải lại toàn trang (cờ SPA đặt trước khi click đã mất) — không điều hướng kiểu SPA như các link khác.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA03-07

## Requirement

Heuristic (navigation consistency)

## Severity

Minor — Không điều hướng SPA như các link khác.

## Screenshot

![GUI-IA03-07](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965742/eshop-hw03/gui-checklist/GUI-IA03-07.png)

---

### BUG-38

## Title

[Minor] Trang thanh toán thiếu đường quay lại Giỏ hàng

## Description

Không có link/nút quay lại giỏ (Checkout.jsx:79-150).

## Steps to Reproduce

1. Mở `/checkout`, tìm nút quay lại giỏ.

## Expected Result

Có link/nút quay lại giỏ hàng không mất dữ liệu.

## Actual Result

- (GUI-IA03-08) Trang thanh toán không có link/nút quay lại Giỏ hàng trước khi xác nhận — người dùng bị cụt đường về để sửa giỏ.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA03-08

## Requirement

Heuristic (back/continue links)

## Severity

Minor — Người dùng cụt đường về để sửa giỏ.

## Screenshot

![GUI-IA03-08](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965744/eshop-hw03/gui-checklist/GUI-IA03-08.png)

---

### BUG-39

## Title

[Minor] Sau khi buộc đăng nhập từ checkout, mất ngữ cảnh (về trang chủ)

## Description

Login luôn về `/` (Login.jsx:16) thay vì quay lại giỏ/checkout.

## Steps to Reproduce

1. Chưa login, từ giỏ bấm thanh toán → bị chuyển login → đăng nhập.

## Expected Result

Quay lại giỏ/checkout sau khi đăng nhập.

## Actual Result

- (GUI-IA03-09) Sau khi buộc đăng nhập từ luồng checkout, người dùng bị đưa về "http://localhost:5173/" (trang chủ) thay vì quay lại giỏ/checkout — mất ngữ cảnh.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA03-09

## Requirement

Heuristic (redirect flow)

## Severity

Minor — Người dùng phải tự tìm lại giỏ/checkout.

## Screenshot

![GUI-IA03-09](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965745/eshop-hw03/gui-checklist/GUI-IA03-09.png)

---

### BUG-40

## Title

[Minor] Back ở bước 2 Quên mật khẩu làm mất tiến trình

## Description

Bước là state không gắn URL (ForgotPassword.jsx:8) → Back rời trang.

## Steps to Reproduce

1. Vào bước 2, bấm Back của trình duyệt.

## Expected Result

Back quay về bước 1 hoặc giữ tiến trình.

## Actual Result

- (GUI-IA03-11) Ở bước 2, bấm Back trình duyệt rời hẳn trang Quên mật khẩu (URL: "about:blank") — step là state không gắn URL nên mất toàn bộ tiến trình OTP.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA03-11

## Requirement

Heuristic (browser back-button)

## Severity

Minor — Bấm Back rời hẳn trang, mất OTP đã lấy.

## Screenshot

![GUI-IA03-11](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965747/eshop-hw03/gui-checklist/GUI-IA03-11.png)

---

### BUG-41

## Title

[Minor] /profile khi chưa đăng nhập là ngõ cụt

## Description

Chỉ hiển thị text "Vui lòng đăng nhập" (Profile.jsx:109), không link/redirect.

## Steps to Reproduce

1. Đăng xuất, truy cập `/profile`.

## Expected Result

Có link "Đăng nhập" hoặc tự redirect.

## Actual Result

- (GUI-IA03-13) /profile khi chưa đăng nhập chỉ hiển thị text trần "Vui lòng đăng nhập", không có link tới trang đăng nhập và không tự redirect — ngõ cụt điều hướng.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA03-13

## Requirement

Heuristic (dead-end navigation)

## Severity

Minor — Chỉ có text, không có đường tới đăng nhập.

## Screenshot

![GUI-IA03-13](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965750/eshop-hw03/gui-checklist/GUI-IA03-13.png)

---

### BUG-42

## Title

[Minor] Empty state thiếu icon/minh hoạ; tìm kiếm 0 kết quả không có empty state

## Description

Empty state giỏ/đơn chỉ có text (Cart.jsx:20-27, Profile.jsx:169-170); tìm 0 kết quả cho grid trống hoàn toàn (Home.jsx:75-114).

## Steps to Reproduce

1. Mở `/cart` trống.
2. Tìm từ khoá `zzzzzzzz` ở `/`.

## Expected Result

Empty state có icon/hình + message thân thiện + CTA.

## Actual Result

- (GUI-IA04-05) Empty state Giỏ hàng chỉ có text + link, không có icon/hình minh hoạ (số ảnh/SVG trong main: 0). Lịch sử ĐH trống cũng chỉ là text trần.
- (GUI-IA04-06) Tìm từ khoá không tồn tại ("zzzzzzzz") cho grid trống hoàn toàn, không có empty-state ("Không tìm thấy sản phẩm...").

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA04-05, GUI-IA04-06

## Requirement

FR-24 (empty-state visuals)

## Severity

Minor — Trạng thái trống sơ sài / trống trơn gây bối rối.

## Screenshot

![GUI-IA04-05](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965759/eshop-hw03/gui-checklist/GUI-IA04-05.png) ![GUI-IA04-06](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965761/eshop-hw03/gui-checklist/GUI-IA04-06.png)

---

### BUG-43

## Title

[Minor] Ảnh sản phẩm có alt rỗng

## Description

Ảnh card dùng `alt=""` (Home.jsx:81-85).

## Steps to Reproduce

1. Mở `/`, kiểm tra thuộc tính alt của ảnh card (DevTools).

## Expected Result

Ảnh có alt = tên sản phẩm, không rỗng.

## Actual Result

- (GUI-IA04-07) Ảnh sản phẩm trên trang chủ có alt="" (rỗng) — thiếu văn bản thay thế mô tả.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA04-07

## Requirement

FR-24 (image alt-text)

## Severity

Minor — Screen reader không mô tả được ảnh (FR-24).

## Screenshot

![GUI-IA04-07](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965763/eshop-hw03/gui-checklist/GUI-IA04-07.png)

---

### BUG-44

## Title

[Minor] Feedback thành công/lỗi dùng alert() native khắp nơi

## Description

Dùng `alert()` native cho feedback (ForgotPassword/Profile/Cart/Checkout).

## Steps to Reproduce

1. Thực hiện các thao tác có feedback, quan sát alert() native.

## Expected Result

Feedback dùng một pattern in-page thống nhất.

## Actual Result

- (GUI-IA04-10) Feedback cập nhật hồ sơ dùng alert() native (đã bắt được dialog alert) thay vì toast/thông báo trong trang — không nhất quán, còn 8+ chỗ dùng alert.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA04-10

## Requirement

Heuristic (feedback consistency)

## Severity

Minor — Không nhất quán, trải nghiệm kém (8+ chỗ).

## Screenshot

![GUI-IA04-10](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965768/eshop-hw03/gui-checklist/GUI-IA04-10.png)

---

### BUG-45

## Title

[Minor] Message khoá tài khoản không phân biệt với sai mật khẩu

## Description

Sau 3 lần sai, UI vẫn hiện "Đăng nhập thất bại. Vui lòng kiểm tra lại." (Login.jsx:17-19).

## Steps to Reproduce

1. Đăng nhập sai 3 lần, thử lần 4, quan sát thông báo.

## Expected Result

Message phân biệt "sai mật khẩu" và "tài khoản đang khoá" (kèm thời gian).

## Actual Result

- (GUI-IA04-11) Sau 3 lần đăng nhập sai (tài khoản đã bị backend khoá), UI vẫn hiện message chung "Đăng nhập thất bại. Vui lòng kiểm tra lại." — không phân biệt "sai mật khẩu" với "đang bị khoá", không nói thời gian mở khoá.

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA04-11

## Requirement

FR-24 + FR-02 (lockout messaging)

## Severity

Minor — Người dùng không biết tài khoản đang bị khoá 30s.

## Screenshot

![GUI-IA04-11](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965770/eshop-hw03/gui-checklist/GUI-IA04-11.png)

---

### BUG-46

## Title

[Minor] Đăng ký thành công không có thông báo xác nhận

## Description

Đăng ký thành công navigate thẳng `/login` không message (Register.jsx:25).

## Steps to Reproduce

1. Đăng ký hợp lệ, quan sát có thông báo trước khi sang login.

## Expected Result

Có toast/message "Đăng ký thành công, mời đăng nhập".

## Actual Result

- (GUI-IA04-17) Đăng ký thành công điều hướng thẳng sang /login không có thông báo xác nhận ("Đăng ký thành công, mời đăng nhập").

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-IA04-17

## Requirement

Heuristic (action feedback)

## Severity

Minor — Chuyển trang đột ngột, người dùng không chắc đã thành công.

## Screenshot

![GUI-IA04-17](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965779/eshop-hw03/gui-checklist/GUI-IA04-17.png)

---

### BUG-47

## Title

[Minor] Giỏ hàng không gộp sản phẩm trùng

## Description

`addToCart` luôn push entry mới (CartContext.jsx:8-10).

## Steps to Reproduce

1. Thêm cùng 1 SP 2 lần, mở `/cart`.

## Expected Result

Gộp thành 1 dòng với số lượng cộng dồn.

## Actual Result

- (GUI-GAP-02) Thêm cùng 1 sản phẩm 2 lần tạo 2 dòng riêng trong giỏ thay vì gộp thành 1 dòng số lượng 2 (addToCart luôn push entry mới).

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-GAP-02

## Requirement

Heuristic (cart merge)

## Severity

Minor — Thêm cùng SP nhiều lần tạo nhiều dòng, khó quản lý số lượng.

## Screenshot

![GUI-GAP-02](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965681/eshop-hw03/gui-checklist/GUI-GAP-02.png)

---

### BUG-48

## Title

[Minor] Thẻ <html> khai báo lang="en" trong khi UI tiếng Việt

## Description

`index.html:2` khai báo `lang="en"`.

## Steps to Reproduce

1. Mở app, kiểm tra thuộc tính `lang` của `<html>` (DevTools).

## Expected Result

`<html lang="vi">`.

## Actual Result

- (GUI-GAP-03) Thẻ <html> khai báo lang="en" trong khi toàn bộ UI là tiếng Việt — sai ngôn ngữ nội dung (WCAG 3.1.1).

## Environment

Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)

GUI-GAP-03

## Requirement

Heuristic / WCAG 3.1.1

## Severity

Minor — Sai ngôn ngữ nội dung (WCAG 3.1.1), screen reader đọc sai giọng.

## Screenshot

![GUI-GAP-03](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965683/eshop-hw03/gui-checklist/GUI-GAP-03.png)
