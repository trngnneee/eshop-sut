# Gap-finding review for EShop GUI Checklist

Scope: Product Detail Web, Cart Web, Product Management Admin Web, Product Detail Mobile.

## AI-gap-review items added

- GUI-057: Encoding/tiếng Việt có dấu. Lý do bị bỏ sót ban đầu: danh mục IA chung thường giả định text render đúng, nhưng repo đọc qua console cho thấy nguy cơ mojibake nên cần kiểm tra riêng.
- GUI-058: Color contrast thực tế. Lý do bị bỏ sót ban đầu: prompt checklist ban đầu nói màu sắc nhất quán, nhưng contrast ratio phụ thuộc DOM/CSS render thật nên mô hình văn bản dễ không nhắc rõ.
- GUI-059: Screen reader labels cho web/mobile. Lý do bị bỏ sót ban đầu: AI thường tập trung vào giao diện nhìn thấy được nếu prompt không nêu accessibility/ARIA/accessibilityLabel.
- GUI-060: Keyboard-only navigation. Lý do bị bỏ sót ban đầu: các mục navigation ban đầu tập trung vào route, breadcrumb, badge; khả năng thao tác bằng bàn phím cần prompt accessibility riêng.
- GUI-061: Text truncation/localization/data dài. Lý do bị bỏ sót ban đầu: checklist ban đầu dựa trên dữ liệu mẫu bình thường, chưa xét tên/mô tả/URL/lỗi import dài bất thường.

## Coverage count

- IA-01 General UI standards: 20 items
- IA-02 Forms: 16 items
- IA-03 Navigation: 12 items
- IA-04 Feedback/state: 14 items
- Total: 61 items

## Human review checklist

Before execution, review each item and mark one of: Keep, Edit, Reject. Suggested edits to consider:

- If your instructor wants one primary screen only, keep the same rows but filter the `Screen` column to the selected primary screen.
- If your groupmates already chose one of these screens, replace that screen's rows before executing.
- If the mobile app is tested only through Expo Go on a real phone, add the device model/OS version in the execution Notes for failed mobile items.
