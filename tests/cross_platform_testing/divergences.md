# Task 3 — Khác biệt giữa các platform

> Sinh tự động từ `results/raw/*.json`. Mỗi mục dưới đây là bằng chứng cho thấy cùng một item checklist cho ra kết quả hoặc giá trị hiển thị **khác nhau** giữa các engine — đây chính là nội dung của Task 3.

## A. Khác biệt về KẾT QUẢ Pass/Fail (nghiêm trọng nhất)

### GUI-IA02-14 — Thông báo "bắt buộc nhập" nhất quán tiếng Việt (hiện dùng tooltip native)

* Aspect: IA-02 · Screen(s): Đăng ký, Đăng nhập, Quên MK · Task 1: Failed

| Platform | Kết quả | Quan sát |
|---|---|---|
| P1 Chrome / Chromium — macOS | ✅ Pass | Required messages are Vietnamese on all 3 forms: "Vui lòng điền vào trường này.", "Vui lòng điền vào trường này.", "Vui lòng điền vào trường này." |
| P2 Firefox — macOS | ❌ Fail | Required feedback is the engine's own bubble, not Vietnamese app text: /register "Họ Tên" → "Please fill out this field." ; /login "Username" → "Please fill out this field." ; /forgot-password "Nhập Email của bạn" → "Please fill out this field." (navigator.language=en-US, <html lang>=en) |
| P3 Safari / WebKit — macOS | ❌ Fail | Required feedback is the engine's own bubble, not Vietnamese app text: /register "Họ Tên" → "Fill out this field" ; /login "Username" → "Fill out this field" ; /forgot-password "Nhập Email của bạn" → "Fill out this field" (navigator.language=vi-VN, <html lang>=en) |

Giá trị thô khác nhau:

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `perForm` | `{"/register":{"field":"Họ Tên","requiredAttr":true,"validationMessage":"Vui lòng điền vào trường này.","valueMissing":true,"willValidate":true,"formValid":false` | `{"/register":{"field":"Họ Tên","requiredAttr":true,"validationMessage":"Please fill out this field.","valueMissing":true,"willValidate":true,"formValid":false,"` | `{"/register":{"field":"Họ Tên","requiredAttr":true,"validationMessage":"Fill out this field","valueMissing":true,"willValidate":true,"formValid":false,"mechanis` |
| `navigatorLanguage` | `"vi-VN"` | `"en-US"` | `"vi-VN"` |
| `navigatorLanguages` | `"vi-VN,vi,fr-FR,fr,en-US,en"` | `"en-US,en"` | `"vi-VN"` |

Screenshot: [P2](results/P2-firefox-macos/screenshots/GUI-IA02-14.png) · [P3](results/P3-webkit-macos/screenshots/GUI-IA02-14.png)

## B. Cùng kết quả nhưng GIÁ TRỊ HIỂN THỊ khác nhau

### GUI-IA01-06 — Giá trên card sản phẩm dùng ký hiệu ₫ (Home hiện dùng "VND")

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `homeCardPrice` | `"30.000.000 VND"` | `"30,000,000 VND"` | `"30.000.000 VND"` |
| `productDetailPrice` | `"30.000.000 ₫"` | `"30,000,000 ₫"` | `"30.000.000 ₫"` |

### GUI-IA01-07 — Phân cách hàng nghìn nhất quán (toLocaleString() không tham số → phụ thuộc locale engine)

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `prices` | `{"/":"30.000.000 VND","/product/1":"30.000.000 ₫","/cart":"30.000.000 ₫"}` | `{"/":"30,000,000 VND","/product/1":"30,000,000 ₫","/cart":"30,000,000 ₫"}` | `{"/":"30.000.000 VND","/product/1":"30.000.000 ₫","/cart":"30.000.000 ₫"}` |
| `separatorPerScreen` | `{"/":".","/product/1":".","/cart":"."}` | `{"/":",","/product/1":",","/cart":","}` | `{"/":".","/product/1":".","/cart":"."}` |
| `distinctSeparators` | `["."]` | `[","]` | `["."]` |
| `navigatorLanguage` | `"vi-VN"` | `"en-US"` | `"vi-VN"` |
| `navigatorLanguages` | `"vi-VN,vi,fr-FR,fr,en-US,en"` | `"en-US,en"` | `"vi-VN"` |
| `resolvedLocale` | `"vi"` | `"en-US"` | `"vi-VN"` |
| `defaultFormat` | `"30.000.000"` | `"30,000,000"` | `"30.000.000"` |
| `localePinnedByApp` | `true` | `false` | `true` |

### GUI-IA01-08 — Giá luôn render là số có định dạng kể cả khi backend trả price sai kiểu (không bao giờ "NaN ₫")

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `validPrice` | `"30.000.000 ₫"` | `"30,000,000 ₫"` | `"30.000.000 ₫"` |

### GUI-IA01-13 — Tab order mọi form đi trên-xuống, submit cuối (Đăng nhập có tabIndex={1} trên nút → focus nút TRƯỚC input)

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `rawFocusSequence` | `{"/login":"#2:button[submit] → (outside:a EShop) → (outside:a Giỏ hàng) → (outside:a Chào, Test User) → (outside:button Thoát) → #0:input[text] → #1:input[text]` | `{"/login":"#2:button[submit] → (outside:a EShop) → (outside:a Giỏ hàng) → (outside:a Chào, Test User) → (outside:button Thoát) → #0:input[text] → #1:input[text]` | `{"/login":"#2:button[submit] → #0:input[text] → #1:input[text] → (outside:body EShop Giỏ hàng Chào, T) → #2:button[submit]","/register":"#0:input[text] → #1:inp` |
| `unreachableControls` | `{}` | `{}` | `{"/register":["#3 button[submit] \"Đăng Ký\""],"/forgot-password":["#1 button[submit] \"Lấy mã OTP\""],"/checkout":["#2 button[submit] \"Xác Nhận Thanh Toán\""]` |
| `nativeButtonsInTabOrder` | `true` | `true` | `false` |

### GUI-IA01-14 — Viewport ≤640px: nút "Thêm vào giỏ hàng" hiển thị đầy đủ (class bug-mobile-hidden áp margin-right:-100px)

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `rect` | `{"left":41,"right":227,"width":186}` | `{"left":41,"right":228,"width":187}` | `{"left":41,"right":227,"width":186}` |
| `layoutWidthReserved` | `86` | `87` | `86` |

### GUI-IA01-15 — Grid sản phẩm 1/2/3 cột theo breakpoint, không horizontal scroll ở 375/768/1280px

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `gridTemplateByViewport` | `{"375":"343px","768":"229.328px 229.336px 229.328px","1280":"314.664px 314.664px 314.664px"}` | `{"375":"343px","768":"229.333px 229.333px 229.333px","1280":"314.667px 314.667px 314.667px"}` | `{"375":"343px","768":"229.328125px 229.328125px 229.34375px","1280":"314.65625px 314.671875px 314.671875px"}` |
| `horizontalOverflowByViewport` | `{"375":false,"768":false,"1280":false}` | `{"375":true,"768":false,"1280":false}` | `{"375":true,"768":false,"1280":false}` |
| `overflowDetail` | `{}` | `{"375":"24px (scrollWidth 399 vs clientWidth 375) from [\"form.flex.gap-2 right=398\",\"button.bg-blue-600.text-white right=398\"]"}` | `{"375":"3px (scrollWidth 378 vs clientWidth 375) from [\"form.flex.gap-2 right=378\",\"button.bg-blue-600.text-white right=378\"]"}` |

### GUI-IA01-16 — Tên sản phẩm dài bị truncate vẫn xem được đầy đủ, không phá layout

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `byViewport` | `{"375":{"viewport":{"requested":375,"applied":375,"resized":true},"renderedText":"Tai nghe không dây chống ồn chủ động bản đặc biệt phiên bản giới hạn 2026 màu ` | `{"375":{"viewport":{"requested":375,"applied":375,"resized":true},"renderedText":"Tai nghe không dây chống ồn chủ động bản đặc biệt phiên bản giới hạn 2026 màu ` | `{"375":{"viewport":{"requested":375,"applied":375,"resized":true},"renderedText":"Tai nghe không dây chống ồn chủ động bản đặc biệt phiên bản giới hạn 2026 màu ` |

### GUI-GAP-03 — Thẻ <html> khai báo đúng ngôn ngữ nội dung (hiện lang="en" trong khi UI tiếng Việt)

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `navigatorLanguage` | `"vi-VN"` | `"en-US"` | `"vi-VN"` |

### GUI-IA02-02 — Field Email dùng type="email" và chặn định dạng sai ("abc")

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `navigatorLanguage` | `"vi-VN"` | `"en-US"` | `"vi-VN"` |
| `navigatorLanguages` | `"vi-VN,vi,fr-FR,fr,en-US,en"` | `"en-US,en"` | `"vi-VN"` |

### GUI-IA02-03 — Field Mật khẩu che ký tự khi gõ

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `fontFamily` | `"ui-sans-serif, system-ui, sans-serif, \"Apple Color Emoji\", \"Segoe UI Emoji\", \"Segoe UI Symbol\", \"Noto Color Emoji\""` | `"ui-sans-serif, system-ui, sans-serif, \"Apple Color Emoji\", \"Segoe UI Emoji\", \"Segoe UI Symbol\", \"Noto Color Emoji\""` | `"ui-sans-serif, system-ui, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol, Noto Color Emoji"` |
| `widthOf60i` | `380` | `364` | `380` |
| `widthOf60W` | `927` | `910` | `928` |
| `clientWidth` | `380` | `364` | `380` |

### GUI-IA02-04 — Lỗi form hiển thị trong trang, phía TRÊN nút submit (không alert native)

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `perForm` | `{"/login":{"mechanism":"in-page","errorText":"Đăng nhập thất bại. Vui lòng kiểm tra lại.","errorY":517,"submitY":425,"aboveSubmit":false},"/register":{"mechanis` | `{"/login":{"mechanism":"in-page","errorText":"Đăng nhập thất bại. Vui lòng kiểm tra lại.","errorY":517,"submitY":425,"aboveSubmit":false},"/register":{"mechanis` | `{"/login":{"mechanism":"in-page","errorText":"Đăng nhập thất bại. Vui lòng kiểm tra lại.","errorY":517,"submitY":425,"aboveSubmit":false},"/register":{"mechanis` |

### GUI-IA02-05 — Luồng 2 bước có Step Indicator rõ ràng ("Bước 1/2", "Bước 2/2")

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `step2Text` | `"EShop Giỏ hàng Đăng nhập Đăng ký Quên Mật Khẩu Mã OTP của bạn là: 5822 Mã OTP (4 số) Mật khẩu mới Đặt lại mật khẩu← Quay lại © 2026 EShop SUT. Dành cho mục đíc` | `"EShop Giỏ hàng Đăng nhập Đăng ký Quên Mật Khẩu Mã OTP của bạn là: 9925 Mã OTP (4 số) Mật khẩu mới Đặt lại mật khẩu← Quay lại © 2026 EShop SUT. Dành cho mục đíc` | `"EShop Giỏ hàng Đăng nhập Đăng ký Quên Mật Khẩu Mã OTP của bạn là: 1770 Mã OTP (4 số) Mật khẩu mới Đặt lại mật khẩu← Quay lại © 2026 EShop SUT. Dành cho mục đíc` |

### GUI-IA02-07 — Validate mật khẩu khớp hint — "Abcdef1!" phải được chấp nhận

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `registerWithWhitespacePassword` | `{"password":"Abc defg1","email":"xp-1785244739453-3446@t.local","hint":"Yêu cầu: Tối thiểu 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt.","error":null,` | `{"password":"Abc defg1","email":"xp-1785245127104-8326@t.local","hint":"Yêu cầu: Tối thiểu 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt.","error":null,` | `{"password":"Abc defg1","email":"xp-1785245520089-3057@t.local","hint":"Yêu cầu: Tối thiểu 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt.","error":null,` |

### GUI-IA02-09 — Input Số lượng có ràng buộc min/max, không cho giá trị vô lý

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `probes` | `{"-1":{"keystrokes":"-1","valueAfter":"-1","validationMessage":"","badInput":false,"rangeUnderflow":false,"valueMissing":false,"valid":true},"abc":{"keystrokes"` | `{"-1":{"keystrokes":"-1","valueAfter":"-1","validationMessage":"","badInput":false,"rangeUnderflow":false,"valueMissing":false,"valid":true},"abc":{"keystrokes"` | `{"-1":{"keystrokes":"-1","valueAfter":"-1","validationMessage":"","badInput":false,"rangeUnderflow":false,"valueMissing":false,"valid":true},"abc":{"keystrokes"` |
| `cartLine` | `"iPhone 15 Pro Max 30.000.000 ₫ -1 -30.000.000 ₫ Xóa"` | `"iPhone 15 Pro Max 30,000,000 ₫ -1 -30,000,000 ₫ Xóa"` | `"iPhone 15 Pro Max 30.000.000 ₫ -1 -30.000.000 ₫ Xóa"` |

### GUI-IA02-10 — Tổng tiền thanh toán là giá trị chỉ đọc, không sửa được

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `summaryLine` | `"Tổng thanh toán: 1.000 ₫"` | `"Tổng thanh toán: 1,000 ₫"` | `"Tổng thanh toán: 1.000 ₫"` |

### GUI-IA02-11 — Mã giảm giá chuẩn hoá hoa/thường ("save10" xử lý như "SAVE10")

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `lowerCase` | `{"typedValue":"save10","success":"✅ Áp dụng thành công! Giảm 10% Tiết kiệm: -270.000.000 ₫ Thành tiền: 300.000.000 ₫","error":null,"applied":true}` | `{"typedValue":"save10","success":"✅ Áp dụng thành công! Giảm 10% Tiết kiệm: -270,000,000 ₫ Thành tiền: 300,000,000 ₫","error":null,"applied":true}` | `{"typedValue":"save10","success":"✅ Áp dụng thành công! Giảm 10% Tiết kiệm: -270.000.000 ₫ Thành tiền: 300.000.000 ₫","error":null,"applied":true}` |
| `upperCase` | `{"typedValue":"SAVE10","success":"✅ Áp dụng thành công! Giảm 10% Tiết kiệm: -270.000.000 ₫ Thành tiền: 300.000.000 ₫","error":null,"applied":true}` | `{"typedValue":"SAVE10","success":"✅ Áp dụng thành công! Giảm 10% Tiết kiệm: -270,000,000 ₫ Thành tiền: 300,000,000 ₫","error":null,"applied":true}` | `{"typedValue":"SAVE10","success":"✅ Áp dụng thành công! Giảm 10% Tiết kiệm: -270.000.000 ₫ Thành tiền: 300.000.000 ₫","error":null,"applied":true}` |

### GUI-IA03-04 — Có breadcrumb ở 3 trang con theo spec (hiện không có)

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `breadcrumbs` | `{"/product/1":{"count":0,"sample":"","mainHead":"iPhone 15 Pro Max 30.000.000 ₫ Điện thoại cao cấp của Apple Số lượng: Thêm vào g"},"/cart":{"count":0,"sample":` | `{"/product/1":{"count":0,"sample":"","mainHead":"iPhone 15 Pro Max 30,000,000 ₫ Điện thoại cao cấp của Apple Số lượng: Thêm vào g"},"/cart":{"count":0,"sample":` | `{"/product/1":{"count":0,"sample":"","mainHead":"iPhone 15 Pro Max 30.000.000 ₫ Điện thoại cao cấp của Apple Số lượng: Thêm vào g"},"/cart":{"count":0,"sample":` |

### GUI-IA03-07 — Link "Quên mật khẩu?" điều hướng SPA không reload trang (hiện dùng <a href> — Login.jsx:49-51)

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `totalLoadEvents` | `2` | `3` | `2` |

### GUI-IA03-08 — Có link/nút quay lại Giỏ hàng trước khi xác nhận (hiện không có — Checkout.jsx:79-150)

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `mainText` | `"Xác Nhận Đơn Hàng Sản phẩm: iPhone 15 Pro Max x 1 — 30.000.000 ₫ Tổng tiền thanh toán (VND): Mã Giảm Giá Áp dụng Tổng thanh toán: 30.000.000 ₫ Xác Nhận Thanh T` | `"Xác Nhận Đơn Hàng Sản phẩm: iPhone 15 Pro Max x 1 — 30,000,000 ₫ Tổng tiền thanh toán (VND): Mã Giảm Giá Áp dụng Tổng thanh toán: 30,000,000 ₫ Xác Nhận Thanh T` | `"Xác Nhận Đơn Hàng Sản phẩm: iPhone 15 Pro Max x 1 — 30.000.000 ₫ Tổng tiền thanh toán (VND): Mã Giảm Giá Áp dụng Tổng thanh toán: 30.000.000 ₫ Xác Nhận Thanh T` |

### GUI-IA03-09 — Bị chặn checkout vì chưa login → đăng nhập xong quay lại giỏ/checkout (hiện luôn về / — Login.jsx:16)

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `atCart` | `{"label":"cart (guest)","url":"http://localhost:5173/cart","route":"/cart","heading":"Giỏ Hàng","mainText":"Giỏ Hàng Sản phẩm Giá Số lượng Thành tiền Thao tác i` | `{"label":"cart (guest)","url":"http://localhost:5173/cart","route":"/cart","heading":"Giỏ Hàng","mainText":"Giỏ Hàng Sản phẩm Giá Số lượng Thành tiền Thao tác i` | `{"label":"cart (guest)","url":"http://localhost:5173/cart","route":"/cart","heading":"Giỏ Hàng","mainText":"Giỏ Hàng Sản phẩm Giá Số lượng Thành tiền Thao tác i` |
| `afterLogin` | `{"label":"after login","url":"http://localhost:5173/","route":"/","heading":"Danh sách sản phẩm","mainText":"Danh sách sản phẩm Tìm iPhone 15 Pro Max 30.000.000` | `{"label":"after login","url":"http://localhost:5173/","route":"/","heading":"Danh sách sản phẩm","mainText":"Danh sách sản phẩm Tìm iPhone 15 Pro Max 30,000,000` | `{"label":"after login","url":"http://localhost:5173/","route":"/","heading":"Danh sách sản phẩm","mainText":"Danh sách sản phẩm Tìm iPhone 15 Pro Max 30.000.000` |

### GUI-IA03-10 — Sau thanh toán thành công, Back trình duyệt không quay lại form có thể re-submit (Checkout.jsx:69-77)

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `afterBack` | `{"label":"after goBack","url":"http://localhost:5173/cart","route":"/cart","heading":"Giỏ Hàng","mainText":"Giỏ Hàng Sản phẩm Giá Số lượng Thành tiền Thao tác i` | `{"label":"after goBack","url":"http://localhost:5173/cart","route":"/cart","heading":"Giỏ Hàng","mainText":"Giỏ Hàng Sản phẩm Giá Số lượng Thành tiền Thao tác i` | `{"label":"after goBack","url":"http://localhost:5173/cart","route":"/cart","heading":"Giỏ Hàng","mainText":"Giỏ Hàng Sản phẩm Giá Số lượng Thành tiền Thao tác i` |
| `afterForward` | `{"label":"after goForward","url":"http://localhost:5173/checkout","route":"/checkout","heading":"Xác Nhận Đơn Hàng","mainText":"Xác Nhận Đơn Hàng Sản phẩm: iPho` | `{"label":"after goForward","url":"http://localhost:5173/checkout","route":"/checkout","heading":"Xác Nhận Đơn Hàng","mainText":"Xác Nhận Đơn Hàng Sản phẩm: iPho` | `{"label":"after goForward","url":"http://localhost:5173/checkout","route":"/checkout","heading":"Xác Nhận Đơn Hàng","mainText":"Xác Nhận Đơn Hàng Sản phẩm: iPho` |

### GUI-IA03-11 — Ở bước 2 bấm Back trình duyệt: không mất tiến trình (step là state, không gắn URL — ForgotPassword.jsx:8)

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `before` | `{"label":"step 2","url":"http://localhost:5173/forgot-password","route":"/forgot-password","heading":"Quên Mật Khẩu","mainText":"Quên Mật Khẩu Mã OTP của bạn là` | `{"label":"step 2","url":"http://localhost:5173/forgot-password","route":"/forgot-password","heading":"Quên Mật Khẩu","mainText":"Quên Mật Khẩu Mã OTP của bạn là` | `{"label":"step 2","url":"http://localhost:5173/forgot-password","route":"/forgot-password","heading":"Quên Mật Khẩu","mainText":"Quên Mật Khẩu Mã OTP của bạn là` |

### GUI-IA03-15 — Danh sách dài có phân trang/lazy-load hoặc không vỡ layout (render toàn bộ — Home.jsx:75, Profile.jsx:172-213)

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `gridTemplateColumns` | `"314.664px 314.664px 314.664px"` | `"314.667px 314.667px 314.667px"` | `"314.65625px 314.671875px 314.671875px"` |

### GUI-IA04-09 — API lỗi → error state, không kẹt "Đang tải..." vô hạn

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `consoleErrorCount` | `4` | `2` | `4` |
| `consoleErrorSample` | `["Failed to load resource: the server responded with a status of 500 (Internal Server Error)","AxiosError: Request failed with status code 500\n    at settle (h` | `["Error","Error"]` | `["Failed to load resource: the server responded with a status of 500 (Internal Server Error)","AxiosError: Request failed with status code 500"]` |

### GUI-IA04-12 — Feedback coupon đủ 2 nhánh (hợp lệ → message + tiết kiệm + thành tiền; sai → lỗi đỏ) và số tiền tính đúng

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `successBlockText` | `"✅ Áp dụng thành công! Giảm 10% Tiết kiệm: -270.000.000 ₫ Thành tiền: 300.000.000 ₫"` | `"✅ Áp dụng thành công! Giảm 10% Tiết kiệm: -270,000,000 ₫ Thành tiền: 300,000,000 ₫"` | `"✅ Áp dụng thành công! Giảm 10% Tiết kiệm: -270.000.000 ₫ Thành tiền: 300.000.000 ₫"` |
| `savedRendered` | `"-270.000.000"` | `"-270,000,000"` | `"-270.000.000"` |
| `finalRendered` | `"300.000.000"` | `"300,000,000"` | `"300.000.000"` |
| `grandTotalLine` | `"Tổng thanh toán: 300.000.000 ₫"` | `"Tổng thanh toán: 300,000,000 ₫"` | `"Tổng thanh toán: 300.000.000 ₫"` |
| `thousandsSeparator` | `"."` | `","` | `"."` |

### GUI-IA04-15 — Sau thanh toán thành công giỏ hàng được reset (clearCart không bao giờ được gọi)

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `rowsAfterDetail` | `[{"name":"iPhone 15 Pro Max","price":"30.000.000 ₫","qty":"1","total":"30.000.000 ₫"}]` | `[{"name":"iPhone 15 Pro Max","price":"30,000,000 ₫","qty":"1","total":"30,000,000 ₫"}]` | `[{"name":"iPhone 15 Pro Max","price":"30.000.000 ₫","qty":"1","total":"30.000.000 ₫"}]` |
| `cartTextAfterOrder` | `"Giỏ Hàng Sản phẩm Giá Số lượng Thành tiền Thao tác iPhone 15 Pro Max 30.000.000 ₫ 1 30.000.000 ₫ Xóa Tổng tạm tính: 30.000.000 ₫ ← Mua tiếp Tiến hành thanh toá` | `"Giỏ Hàng Sản phẩm Giá Số lượng Thành tiền Thao tác iPhone 15 Pro Max 30,000,000 ₫ 1 30,000,000 ₫ Xóa Tổng tạm tính: 30,000,000 ₫ ← Mua tiếp Tiến hành thanh toá` | `"Giỏ Hàng Sản phẩm Giá Số lượng Thành tiền Thao tác iPhone 15 Pro Max 30.000.000 ₫ 1 30.000.000 ₫ Xóa Tổng tạm tính: 30.000.000 ₫ ← Mua tiếp Tiến hành thanh toá` |

### GUI-IA04-16 — Lỗi API tải đơn hiển thị khác empty state (lỗi bị nuốt → hiện "chưa có đơn")

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `consoleErrorSample` | `["Failed to load resource: the server responded with a status of 500 (Internal Server Error)","Lỗi lấy đơn hàng: AxiosError: Request failed with status code 500` | `["Lỗi lấy đơn hàng: Error","Lỗi lấy đơn hàng: Error"]` | `["Failed to load resource: the server responded with a status of 500 (Internal Server Error)","Lỗi lấy đơn hàng: AxiosError: Request failed with status code 500` |

### GUI-GAP-02 — Thêm cùng 1 SP nhiều lần → gộp 1 dòng, số lượng cộng dồn (hiện append dòng riêng)

| metric | P1 | P2 | P3 |
|---|---|---|---|
| `rows` | `[{"name":"iPhone 15 Pro Max","price":"30.000.000 ₫","qty":"1","total":"30.000.000 ₫"},{"name":"iPhone 15 Pro Max","price":"30.000.000 ₫","qty":"1","total":"30.0` | `[{"name":"iPhone 15 Pro Max","price":"30,000,000 ₫","qty":"1","total":"30,000,000 ₫"},{"name":"iPhone 15 Pro Max","price":"30,000,000 ₫","qty":"1","total":"30,0` | `[{"name":"iPhone 15 Pro Max","price":"30.000.000 ₫","qty":"1","total":"30.000.000 ₫"},{"name":"iPhone 15 Pro Max","price":"30.000.000 ₫","qty":"1","total":"30.0` |
| `cartTotalRendered` | `"60.000.000 ₫"` | `"60,000,000 ₫"` | `"60.000.000 ₫"` |

## C. Khác biệt CHỈ do dữ liệu của lần chạy — KHÔNG phải khác biệt platform

Liệt kê để minh bạch: các item dưới đây có giá trị `metrics` khác nhau, nhưng mọi khoá khác nhau đều là dữ liệu sinh theo từng lần chạy (email throwaway do check tự đăng ký, mã OTP ngẫu nhiên của SUT, id đơn hàng, thời gian). Chạy lại 2 lần trên **cùng một** engine cũng cho giá trị khác nhau, nên đây không phải phát hiện cross-platform.

| ID | Khoá chỉ khác do dữ liệu chạy |
|---|---|
| GUI-IA04-04 | `account` |
| GUI-IA04-05 | `account` |
| GUI-IA04-10 | `account` |
| GUI-IA04-11 | `account` |
| GUI-IA04-13 | `account` |
| GUI-IA04-17 | `account` |

