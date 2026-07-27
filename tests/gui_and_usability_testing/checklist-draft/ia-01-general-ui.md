# Checklist Draft — IA-01: General UI Standards

- **Input:** inventory 9 file trong `reports/23127438/ui-inventory/` + FR-21 nguyên văn (`eshop-sut/README.md:242-248`)
- **FR-21 gồm 5 quy tắc:** (1) nhất quán ngôn ngữ tiếng Việt; (2) nút tích cực xanh dương / nút nguy hiểm đỏ; (3) tiền tệ `₫` + phân cách hàng nghìn; (4) mỗi trang đúng 1 `<h1>` mô tả nội dung; (5) tab order trên-xuống, trái-sang-phải.

| ID | Screen(s) | Checklist Item | Expected Result | Traced to (FR-21 / heuristic) |
|---|---|---|---|---|
| GUI-IA01-01 | Đăng nhập | Nhãn field và nút trên form đăng nhập hiển thị bằng tiếng Việt (inventory: label "Username", nút "Sign In" — Login.jsx:28,58) | Nhãn "Email"/"Tên đăng nhập", nút "Đăng nhập" — không còn chữ tiếng Anh | FR-21 (ngôn ngữ) |
| GUI-IA01-02 | Tất cả 8 màn hình | Rà toàn bộ text UI tĩnh (nhãn, nút, placeholder, heading, thông báo) — không có chuỗi tiếng Anh ngoài thuật ngữ kỹ thuật chuẩn (Email, OTP) | 100% text UI bằng tiếng Việt | FR-21 (ngôn ngữ) |
| GUI-IA01-03 | Đăng ký | Nút submit "Đăng Ký" dùng màu hành động tích cực (inventory: đang nền đỏ bg-red-500 — Register.jsx:71-76) | Nút màu xanh dương; đỏ chỉ dành cho hành động nguy hiểm/hủy | FR-21 (màu sắc) |
| GUI-IA01-04 | Chi tiết SP, Giỏ hàng, Thanh toán, Quên MK | Các nút tích cực "Thêm vào giỏ hàng" (xanh lá), "Tiến hành thanh toán" (xanh lá), "Xác Nhận Thanh Toán" (xanh lá), "Áp dụng" (cam), "Đặt lại mật khẩu" (xanh lá) dùng đúng màu xanh dương | Tất cả nút hành động tích cực đồng nhất xanh dương | FR-21 (màu sắc) |
| GUI-IA01-05 | Quên mật khẩu | Nút phụ "← Quay lại" (bước 2) phân biệt thị giác với nút chính "Đặt lại mật khẩu" (cả hai cùng bg-green-600, full-width — ForgotPassword.jsx:91-96) | Nút phụ style thứ cấp, không nhầm với nút submit | Heuristic (visual hierarchy) |
| GUI-IA01-06 | Trang chủ | Giá trên card dùng ký hiệu `₫` (đang là "VND" — Home.jsx:87-89; các màn khác dùng ₫) | Mọi giá dạng `30.000.000 ₫`, thống nhất toàn app | FR-21 (tiền tệ) |
| GUI-IA01-07 | Trang chủ, Chi tiết SP, Giỏ hàng, Thanh toán, Lịch sử ĐH | Phân cách hàng nghìn nhất quán (code dùng toLocaleString() không tham số → phụ thuộc locale trình duyệt) | Một kiểu phân cách duy nhất mọi màn hình/trình duyệt | FR-21 (tiền tệ) + heuristic |
| GUI-IA01-08 | Chi tiết SP | Giá luôn render là số có định dạng kể cả khi backend trả price sai kiểu (comment code thừa nhận NaN — ProductDetail.jsx:49-52) | Không bao giờ hiển thị "NaN ₫" | FR-21 (tiền tệ) + heuristic |
| GUI-IA01-09 | Trang chủ | Trang có đúng 1 thẻ h1 (đang có 2: "Danh sách sản phẩm" Home.jsx:44 và dòng đếm Home.jsx:110-114) | Đúng 1 h1; dòng đếm dùng thẻ phi-heading | FR-21 (tiêu đề trang) |
| GUI-IA01-10 | Đăng nhập, Đăng ký, Quên MK, Giỏ hàng, Thanh toán, Hồ sơ/Đơn hàng | Mỗi trang có đúng 1 h1 mô tả nội dung (6 trang này chỉ có h2, không có h1) | Mỗi trang đúng 1 h1 mô tả đúng nội dung | FR-21 (tiêu đề trang) |
| GUI-IA01-11 | Đăng nhập | Heading mô tả đúng chức năng trang (trang Đăng nhập nhưng heading ghi "Đăng Ký" — Login.jsx:24) | Heading là "Đăng Nhập" | FR-21 (tiêu đề trang) |
| GUI-IA01-12 | Tất cả 8 màn hình | Title tab trình duyệt mô tả trang (mọi trang đang là "frontend-web" — index.html:7) | Title dạng "EShop — Đăng nhập", đổi theo trang | Heuristic (page title) |
| GUI-IA01-13 | Đăng nhập | Tab order: Email → Mật khẩu → Quên mật khẩu → submit (nút "Sign In" có tabIndex={1} nên focus TRƯỚC input — Login.jsx:56) | Tab đi trên-xuống, nút submit cuối | FR-21 (tab order) |
| GUI-IA01-14 | Chi tiết SP | Viewport ≤640px: nút "Thêm vào giỏ hàng" hiển thị đầy đủ (class bug-mobile-hidden áp margin-right:-100px — index.css:10-14) | Nút nguyên vẹn, bấm được ở 375px | Heuristic (responsive) |
| GUI-IA01-15 | Trang chủ | Grid sản phẩm 1/2/3 cột theo breakpoint (Home.jsx:75), không horizontal scroll ở 375/768/1280px | Responsive đúng cột, không tràn ngang | Heuristic (responsive) |
| GUI-IA01-16 | Trang chủ | Tên sản phẩm dài bị truncate (Home.jsx:86) vẫn xem được đầy đủ, không phá layout | Tên dài "..." gọn, có cách xem đầy đủ | Heuristic (text overflow) |

**Coverage FR-21:** ngôn ngữ (01-02) · màu sắc (03-05) · tiền tệ (06-08) · h1/tiêu đề (09-12) · tab order (13) · best-practice ngoài FR-21 (05, 12, 14, 15, 16).
