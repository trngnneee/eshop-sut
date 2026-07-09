# GitHub Issue Content Creator

Sử dụng biểu mẫu này để chuẩn bị nội dung trước khi tạo Issue trên GitHub hoặc chạy lệnh `gh issue create`.

## 1. Issue Title
`[BUG][<Module_Name>] <Tóm tắt ngắn gọn lỗi>`
*Ví dụ: `[BUG][Shopping Cart] Số lượng sản phẩm có thể cập nhật thành số âm qua API`*

## 2. Issue Body (Copy & Paste)
```markdown
### Environment
- **Browser/OS:** [Ví dụ: Chrome 125 / Windows 11]
- **URL:** [Ví dụ: http://localhost:3000/cart]
- **Commit Hash:** [Commit hash của mã nguồn kiểm thử]

### Steps to Reproduce
1. [Bước 1]
2. [Bước 2]
3. [Bước 3]

### Expected Result
[Mô tả hành vi đúng của hệ thống]

### Actual Result
[Mô tả hành vi lỗi của hệ thống]

### Evidence
- **Screenshot:** [Đính kèm ảnh screenshot lỗi tại đây khi kéo thả vào giao diện GitHub Web]
- **Related Test Case:** `TC-[ID]-DT-[STT]` hoặc `TC-[ID]-BVA-[STT]`

### Severity / Priority
- **Severity:** [Critical / Major / Minor / Trivial]
- **Priority:** [High / Medium / Low]
```

## 3. GitHub Labels Đề Xuất
* **Type:** `type: bug`
* **Module:** `module: <tên-module>` (ví dụ: `module: cart`)
* **Technique:** `technique: EP` hoặc `technique: BVA`
* **Severity:** `severity: major` hoặc `severity: minor`
* **Priority:** `priority: P1` hoặc `priority: P2`
* **Status:** `status: new`

## 4. GitHub CLI Command (Nếu sử dụng CLI)
```powershell
gh issue create --title "[BUG][<Module>] <Tóm tắt lỗi>" --body-file "path/to/bug-report-markdown-file.md" --label "type: bug,module: <module>,severity: <severity>,priority: <priority>,status: new"
```
