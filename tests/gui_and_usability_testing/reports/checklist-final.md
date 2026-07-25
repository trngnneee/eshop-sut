# EShop — GUI Checklist cuối

- **Input:** 65 item AI (IA-01: 16, IA-02: 16, IA-03: 15, IA-04: 18) + 4 item bổ sung thủ công (GUI-GAP, từ gap analysis Phần B).
- **Dedup:** 3 cặp near-duplicate được gộp (log cuối file). Item GUI-GAP giữ nguyên mã để truy vết nguồn gốc AI vs thủ công.
- **Tổng: 66 item** — IA-01: 16 · IA-02: 14 · IA-03: 15 · IA-04: 17 · GAP: 4

| ID | Interface Aspect | Screen(s) | Checklist Item | Expected Result |
|---|---|---|---|---|
| GUI-IA01-01 | IA-01 General UI | Đăng nhập | Nhãn field và nút hiển thị tiếng Việt (hiện là "Username", "Sign In" — Login.jsx:28,58) | Nhãn "Email", nút "Đăng nhập" — không còn chữ tiếng Anh |
| GUI-IA01-02 | IA-01 General UI | Tất cả 8 màn hình | Toàn bộ text UI tĩnh (nhãn, nút, placeholder, heading, thông báo) bằng tiếng Việt, trừ thuật ngữ chuẩn (Email, OTP) | 100% text UI tiếng Việt |
| GUI-IA01-03 | IA-01 General UI | Đăng ký | Nút submit "Đăng Ký" dùng màu hành động tích cực (hiện nền đỏ bg-red-500 — Register.jsx:71-76) | Nút xanh dương; đỏ chỉ dành cho hành động nguy hiểm/hủy |
| GUI-IA01-04 | IA-01 General UI | Chi tiết SP, Giỏ hàng, Thanh toán, Quên MK | Các nút tích cực ("Thêm vào giỏ hàng", "Tiến hành thanh toán", "Xác Nhận Thanh Toán", "Áp dụng", "Đặt lại mật khẩu" — hiện xanh lá/cam) dùng màu xanh dương theo spec | Tất cả nút hành động tích cực đồng nhất xanh dương |
| GUI-IA01-05 | IA-01 General UI | Quên mật khẩu | Nút phụ "← Quay lại" (bước 2) phân biệt thị giác với nút chính "Đặt lại mật khẩu" (hiện cùng bg-green-600, full-width — ForgotPassword.jsx:91-96) | Nút phụ style thứ cấp, không nhầm với submit |
| GUI-IA01-06 | IA-01 General UI | Trang chủ | Giá trên card dùng ký hiệu `₫` (hiện là "VND" — Home.jsx:87-89; các màn khác dùng ₫) | Mọi giá dạng `30.000.000 ₫`, thống nhất toàn app |
| GUI-IA01-07 | IA-01 General UI | Trang chủ, Chi tiết SP, Giỏ hàng, Thanh toán, Lịch sử ĐH | Phân cách hàng nghìn nhất quán (toLocaleString() không tham số → phụ thuộc locale trình duyệt) | Một kiểu phân cách duy nhất mọi màn hình/trình duyệt |
| GUI-IA01-08 | IA-01 General UI | Chi tiết SP | Giá luôn render là số có định dạng kể cả khi backend trả price sai kiểu (ProductDetail.jsx:49-52) | Không bao giờ hiển thị "NaN ₫" |
| GUI-IA01-09 | IA-01 General UI | Trang chủ | Trang có đúng 1 thẻ h1 (hiện có 2: Home.jsx:44 và dòng đếm :110-114) | Đúng 1 h1; dòng đếm dùng thẻ phi-heading |
| GUI-IA01-10 | IA-01 General UI | Đăng nhập, Đăng ký, Quên MK, Giỏ hàng, Thanh toán, Hồ sơ/ĐH | Mỗi trang có đúng 1 h1 mô tả nội dung (6 trang này chỉ có h2, không có h1) | Mỗi trang đúng 1 h1 mô tả đúng nội dung |
| GUI-IA01-11 | IA-01 General UI | Đăng nhập | Heading mô tả đúng chức năng trang (trang Đăng nhập nhưng heading ghi "Đăng Ký" — Login.jsx:24) | Heading là "Đăng Nhập" |
| GUI-IA01-12 | IA-01 General UI | Tất cả 8 màn hình | Title tab trình duyệt mô tả trang (hiện cố định "frontend-web" — index.html:7) | Title dạng "EShop — Đăng nhập", đổi theo trang |
| GUI-IA01-13 | IA-01 General UI | Đăng nhập, Đăng ký, Quên MK, Thanh toán, Hồ sơ | Tab order mọi form đi trên-xuống, field đầu → nút submit cuối, không có tabIndex phá thứ tự (Đăng nhập hiện có tabIndex={1} trên nút — Login.jsx:56 → focus nút TRƯỚC input) | Tab tuần tự đúng thứ tự thị giác trên cả 5 form |
| GUI-IA01-14 | IA-01 General UI | Chi tiết SP | Viewport ≤640px: nút "Thêm vào giỏ hàng" hiển thị đầy đủ (class bug-mobile-hidden áp margin-right:-100px — index.css:10-14) | Nút nguyên vẹn, bấm được ở 375px |
| GUI-IA01-15 | IA-01 General UI | Trang chủ | Grid sản phẩm 1/2/3 cột theo breakpoint (Home.jsx:75), không horizontal scroll ở 375/768/1280px | Responsive đúng cột, không tràn ngang |
| GUI-IA01-16 | IA-01 General UI | Trang chủ | Tên sản phẩm dài bị truncate (Home.jsx:86) vẫn xem được đầy đủ, không phá layout | Tên dài "..." gọn, có cách xem đầy đủ |
| GUI-IA02-01 | IA-02 Forms | Đăng ký, Đăng nhập, Quên MK, Hồ sơ | Mọi field `required` hiển thị dấu `*` cạnh nhãn (hiện không field nào có) | Tất cả field bắt buộc có `*` |
| GUI-IA02-02 | IA-02 Forms | Đăng ký, Đăng nhập, Quên MK | Field Email dùng `type="email"` (hiện cả 3 là `type="text"`); nhập "abc" phải bị chặn | Đúng type, chặn định dạng sai |
| GUI-IA02-03 | IA-02 Forms | Đăng nhập | Field Mật khẩu che ký tự khi gõ (hiện `type="text"` — Login.jsx:39-45; 2 form kia đã đúng) | Mật khẩu dạng chấm tròn trên mọi form |
| GUI-IA02-04 | IA-02 Forms | Đăng nhập, Đăng ký, Quên MK, Hồ sơ | Mọi thông báo lỗi form hiển thị TRONG TRANG, vị trí __phía TRÊN nút submit__ — đúng spec dù ngược convention (hiện: Đăng nhập render lỗi DƯỚI form — Login.jsx:66; Quên MK và Hồ sơ dùng alert() native — ForgotPassword.jsx:27-31, Profile.jsx:44-47; Đăng ký đã đúng — Register.jsx:34) | Lỗi trong trang, nằm trên nút submit, không popup native |
| GUI-IA02-05 | IA-02 Forms | Quên mật khẩu | Luồng 2 bước có Step Indicator rõ ràng (hiện không có — ForgotPassword.jsx:46-98) | Hiển thị "Bước 1/2", "Bước 2/2" |
| GUI-IA02-06 | IA-02 Forms | Hồ sơ | Field SĐT chấp nhận số VN 10 số bắt đầu bằng 0 (regex hiện từ chối số đầu 0 — Profile.jsx:44 — mâu thuẫn placeholder "0912345678" — :144) | "0912345678" hợp lệ; input sai bị chặn kèm message rõ |
| GUI-IA02-07 | IA-02 Forms | Đăng ký, Quên MK | Validate mật khẩu khớp hint: "Abcdef1!" (đủ điều kiện theo hint) phải được chấp nhận (regex hiện yêu cầu khoảng trắng, cấm ký tự đặc biệt — Register.jsx:16-19) | Mật khẩu đúng hint → pass; validate và hint không mâu thuẫn |
| GUI-IA02-08 | IA-02 Forms | Quên mật khẩu | Field OTP giới hạn đúng 4 chữ số như nhãn (hiện không maxLength/pattern — ForgotPassword.jsx:71-77) | Không nhập quá 4 ký tự / ký tự không phải số |
| GUI-IA02-09 | IA-02 Forms | Chi tiết SP | Input Số lượng có ràng buộc min/max (hiện không min — ProductDetail.jsx:57-62); thử 0, -1, trống, chữ | Giá trị <1/rỗng bị chặn; không thêm NaN vào giỏ |
| GUI-IA02-10 | IA-02 Forms | Thanh toán | Tổng tiền thanh toán là giá trị chỉ đọc (hiện là input number sửa được, gửi thẳng lên API — Checkout.jsx:94-103, 44-48) | Không sửa được tổng tiền trên UI |
| GUI-IA02-11 | IA-02 Forms | Thanh toán | Mã giảm giá chuẩn hoá hoa/thường: "sale10" xử lý như "SALE10" (Checkout.jsx:110-116, 30) | Không phân biệt hoa thường, hiển thị chữ hoa |
| GUI-IA02-12 | IA-02 Forms | Hồ sơ | Field Email disabled đúng chuẩn: nhãn "(Không đổi)", nền xám, không nhận input (Profile.jsx:117-125) | Field disabled rõ ràng, không sửa được |
| GUI-IA02-13 | IA-02 Forms | Đăng ký | Form có field "Xác nhận mật khẩu" bắt buộc khớp (hiện không tồn tại — Register.jsx:35-81) | Có field xác nhận; không khớp → lỗi trên nút submit |
| GUI-IA02-14 | IA-02 Forms | Đăng ký, Đăng nhập, Quên MK | Thông báo bắt buộc nhập nhất quán tiếng Việt (hiện dựa HTML5 required native → tooltip theo ngôn ngữ trình duyệt, có thể tiếng Anh) | Message required tiếng Việt, cùng style lỗi khác |
| GUI-IA03-01 | IA-03 Navigation | Tất cả 8 màn hình (Header) | Navbar highlight mục đang chọn (hiện chỉ hover:underline — App.jsx:22-37) | Link trang hiện tại có style active |
| GUI-IA03-02 | IA-03 Navigation | Tất cả 8 màn hình (Header) | Link "Giỏ hàng" có badge số lượng, cập nhật ngay khi thêm SP (hiện link trần — App.jsx:23) | Badge đúng số item, +1 tức thì |
| GUI-IA03-03 | IA-03 Navigation | Header (đã đăng nhập) | Nút đăng xuất nhãn chính xác "Đăng xuất" (hiện ghi "Thoát" — App.jsx:29) | Nhãn đúng từng chữ "Đăng xuất" |
| GUI-IA03-04 | IA-03 Navigation | Chi tiết SP, Giỏ hàng, Thanh toán | Có breadcrumb ở 3 trang con theo spec (hiện không có) | Breadcrumb đúng cấp, click được |
| GUI-IA03-05 | IA-03 Navigation | Toàn app | URL không tồn tại (/abc) hiển thị trang 404 thân thiện (hiện không có route catch-all — App.jsx:50-59 → trang trắng) | 404 có message + link về trang chủ |
| GUI-IA03-06 | IA-03 Navigation | Chi tiết SP | /product/999 (không tồn tại) hiển thị thông báo thân thiện + đường quay về (hiện text kỹ thuật, không link — ProductDetail.jsx:35-36) | Message thân thiện + link về trang chủ |
| GUI-IA03-07 | IA-03 Navigation | Đăng nhập | Link "Quên mật khẩu?" điều hướng SPA không reload trang (hiện dùng `<a href>` — Login.jsx:49-51) | Chuyển trang không full reload |
| GUI-IA03-08 | IA-03 Navigation | Thanh toán | Có link/nút quay lại Giỏ hàng trước khi xác nhận (hiện không có — Checkout.jsx:79-150) | Quay lại giỏ được, không mất dữ liệu |
| GUI-IA03-09 | IA-03 Navigation | Giỏ hàng → Đăng nhập | Bị chặn checkout vì chưa login → đăng nhập xong quay lại giỏ/checkout (hiện luôn về / — Login.jsx:16) | Quay về đúng ngữ cảnh trước đó |
| GUI-IA03-10 | IA-03 Navigation | Thanh toán | Sau thanh toán thành công, Back trình duyệt không quay lại form có thể re-submit (Checkout.jsx:69-77) | Back không cho re-submit đơn |
| GUI-IA03-11 | IA-03 Navigation | Quên mật khẩu | Ở bước 2 bấm Back trình duyệt: không mất tiến trình (step là state, không gắn URL — ForgotPassword.jsx:8) | Back về bước 1 hoặc giữ tiến trình |
| GUI-IA03-12 | IA-03 Navigation | Thanh toán | Vào thẳng /checkout khi giỏ trống/chưa login bị chặn (hiện không guard — form hiện tổng 0 ₫) | Redirect về giỏ hàng / đăng nhập |
| GUI-IA03-13 | IA-03 Navigation | Hồ sơ/ĐH | /profile chưa login: thông báo kèm link tới đăng nhập (hiện text trần — Profile.jsx:109) | Có link "Đăng nhập" hoặc tự redirect |
| GUI-IA03-14 | IA-03 Navigation | Tất cả 8 màn hình | Logo "EShop" luôn về trang chủ từ mọi màn (App.jsx:21) | Click logo → về / |
| GUI-IA03-15 | IA-03 Navigation | Trang chủ, Lịch sử ĐH | Danh sách dài có phân trang/lazy-load hoặc không vỡ layout (hiện render toàn bộ — Home.jsx:75, Profile.jsx:172-213) | Nhiều item vẫn dùng được, không vỡ bảng |
| GUI-IA04-01 | IA-04 Feedback/State | Trang chủ | "Thêm vào giỏ" có phản hồi trực quan ngay (hiện không có gì — Home.jsx:98-103) | Toast/badge ngay sau click |
| GUI-IA04-02 | IA-04 Feedback/State | Chi tiết SP | MỖI click "Thêm vào giỏ hàng" đều thêm SP + feedback từ lần đầu (hiện click đầu bị nuốt — ProductDetail.jsx:22-32) | Click 1 lần → vào giỏ + "Đã thêm" |
| GUI-IA04-03 | IA-04 Feedback/State | Giỏ hàng | "Xóa" item có dialog xác nhận (hiện xoá ngay — Cart.jsx:50-55) | Dialog xác nhận; Hủy → giữ item |
| GUI-IA04-04 | IA-04 Feedback/State | Lịch sử ĐH | "Hủy đơn" có dialog xác nhận (hiện huỷ ngay; nút hiện cả khi "Đang giao" — Profile.jsx:200-208) | Dialog xác nhận trước hành động không hoàn tác |
| GUI-IA04-05 | IA-04 Feedback/State | Giỏ hàng, Lịch sử ĐH | Empty state có icon/hình + message thân thiện (hiện text trần — Cart.jsx:20-27, Profile.jsx:169-170) | Icon/hình + message + CTA |
| GUI-IA04-06 | IA-04 Feedback/State | Trang chủ | Tìm kiếm 0 kết quả có empty state (hiện không có gì — Home.jsx:75-114) | "Không tìm thấy..." + icon |
| GUI-IA04-07 | IA-04 Feedback/State | Trang chủ | Ảnh sản phẩm có alt mô tả (hiện alt="" — Home.jsx:81-85; Chi tiết SP đã đạt) | alt = tên SP, không rỗng |
| GUI-IA04-08 | IA-04 Feedback/State | Trang chủ, Lịch sử ĐH, Chi tiết SP | Thao tác tải dữ liệu có loading indicator (hiện không có/chỉ text — Home.jsx:13-30, Profile.jsx:15-30, ProductDetail.jsx:34); test với Slow 3G | Spinner/skeleton trong lúc chờ |
| GUI-IA04-09 | IA-04 Feedback/State | Chi tiết SP | API lỗi/backend chết → error state, không kẹt "Đang tải..." vô hạn (ProductDetail.jsx:15-20) | Message lỗi + nút thử lại/về trang chủ |
| GUI-IA04-10 | IA-04 Feedback/State | Quên MK, Hồ sơ, Giỏ hàng, Thanh toán | Feedback thành công/lỗi API dùng UI trong trang nhất quán, không alert() native (hiện 8+ chỗ alert — ForgotPassword.jsx:21,35,38; Profile.jsx:61,63,76,79; Cart.jsx:13; Checkout.jsx:64). Lỗi validate đã cover ở GUI-IA02-04 | 1 pattern feedback trong trang thống nhất |
| GUI-IA04-11 | IA-04 Feedback/State | Đăng nhập | Sau 3 lần sai, UI báo rõ tài khoản khoá 30s (hiện message chung — Login.jsx:17-19) | Phân biệt sai mật khẩu vs đang khoá (kèm thời gian) |
| GUI-IA04-12 | IA-04 Feedback/State | Thanh toán | Feedback coupon đủ 2 nhánh: hợp lệ → message + tiết kiệm + thành tiền; sai → lỗi đỏ (Checkout.jsx:125-134); kiểm tra số tiền tính đúng | Cả 2 nhánh đúng, số chính xác |
| GUI-IA04-13 | IA-04 Feedback/State | Trang chủ, Header, Hồ sơ | Text người dùng nhập được render an toàn tại cả 3 điểm: từ khoá tìm kiếm echo (Home.jsx:62-67), tên user ở header "Chào, {name}" (App.jsx:26-28), địa chỉ giao hàng (Profile). Test với `<script>alert(1)</script>` và `<img src=x onerror=alert(1)>` | Text thuần, không thực thi HTML/JS ở cả 3 điểm (fail điểm nào ghi Notes điểm đó) |
| GUI-IA04-14 | IA-04 Feedback/State | Trang chủ | Lỗi backend hiển thị thân thiện (runtime: search `'` → raw HTML "Database Error/SQLITE_ERROR" render nguyên khối — Home.jsx:69-73) | Message thân thiện, không lộ SQL/stack |
| GUI-IA04-15 | IA-04 Feedback/State | Thanh toán, Giỏ hàng | Sau thanh toán thành công giỏ được reset (hiện clearCart không bao giờ gọi — Checkout.jsx:9, 62) | Giỏ trống sau đặt hàng thành công |
| GUI-IA04-16 | IA-04 Feedback/State | Lịch sử ĐH | Lỗi API tải đơn hiển thị khác empty state (hiện lỗi bị nuốt → hiện "chưa có đơn" — Profile.jsx:26-29) | Lỗi → message lỗi; empty chỉ khi thật sự 0 đơn |
| GUI-IA04-17 | IA-04 Feedback/State | Đăng ký | Đăng ký thành công có thông báo xác nhận (hiện navigate thẳng /login không message — Register.jsx:25) | Toast/message "Đăng ký thành công" |
| GUI-GAP-01 | IA-04 Feedback/State | Giỏ hàng (toàn app) | Giỏ hàng được giữ lại sau khi refresh (F5) trang (hiện chỉ trong React state — CartContext.jsx:6, trong khi token CÓ dùng localStorage) | F5 ở bất kỳ trang nào → giỏ còn nguyên |
| GUI-GAP-02 | IA-04 Feedback/State | Trang chủ, Giỏ hàng | Thêm cùng 1 SP nhiều lần → gộp 1 dòng với số lượng cộng dồn (hiện append thành dòng riêng — CartContext.jsx:8-10) | 2 lần thêm cùng SP → 1 dòng SL 2 |
| GUI-GAP-03 | IA-01 General UI | Toàn app | Thẻ `<html>` khai báo đúng ngôn ngữ nội dung (hiện `lang="en"` trong khi UI tiếng Việt — index.html:2) | `lang="vi"` — screen reader đọc đúng giọng |
| GUI-GAP-04 | IA-02 Forms | Đăng nhập, Đăng ký, Quên MK, Hồ sơ | Mọi label gắn với input qua htmlFor/id — click nhãn focus vào ô nhập (hiện 0 label nào có htmlFor trên cả 4 form) | Click nhãn → focus input; screen reader đọc được tên field |

## Tổng kết

| Aspect | Số item | Trong đó Manually added |
|---|---|---|
| IA-01 General UI | 16 + 1 (GAP-03) = 17 | 1 |
| IA-02 Forms | 14 + 1 (GAP-04) = 15 | 1 |
| IA-03 Navigation | 15 | 0 |
| IA-04 Feedback/State | 17 + 2 (GAP-01, 02) = 19 | 2 |
| **Tổng** | **66** | **4** |

## Dedup log (truy vết từ bản draft)

1. GUI-IA01-13 (mới) = GUI-IA01-13 + GUI-IA02-15 (cũ) — cùng quy tắc tab order FR-21, gộp phủ 5 form.
2. GUI-IA02-04 (mới) = GUI-IA02-04 + GUI-IA02-06 (cũ) — cùng quy tắc "lỗi trong trang, trên nút submit" FR-22, gộp phủ 4 form.
3. GUI-IA04-13 (mới) = GUI-IA04-13 + GUI-IA04-14 (cũ) — cùng quy tắc safe rendering, gộp phủ 3 điểm nhập.
4. GUI-IA04-10 viết lại thu hẹp phạm vi (chỉ feedback thành công/lỗi API) để không trùng GUI-IA02-04.
5. Đánh số lại: IA-02 cũ 07→06, 08→07, 09→08, 10→09, 11→10, 12→11, 13→12, 14→13, 16→14; IA-04 cũ 15→14, 16→15, 17→16, 18→17. IA-01, IA-03 giữ nguyên.
