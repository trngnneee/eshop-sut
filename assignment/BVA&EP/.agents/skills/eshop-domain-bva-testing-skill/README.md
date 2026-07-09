# EShop Domain & BVA Testing Skill

Đây là một Agent Skill hoàn chỉnh, có thể tái sử dụng, được thiết kế để hỗ trợ sinh viên thực hiện bài tập **HW02 – Domain Testing on EShop** theo đúng tài liệu đặc tả `Requirements.pdf`.

Skill này trang bị cho AI Agent quy trình phân tích và thiết kế test case chi tiết theo kỹ thuật **Phân vùng tương đương (Equivalence Partitioning)** và **Phân tích giá trị biên (Boundary Value Analysis)**, hỗ trợ dò lỗi (exploratory testing), tự động sinh báo cáo lỗi (Bug Report), ma trận truy vết (Traceability Matrix) và các báo cáo AI Audit, AI Critique bắt buộc.

---

## 1. Cấu Trúc Thư Mục Skill

```text
eshop-domain-bva-testing-skill/
├── SKILL.md                          # Hướng dẫn chính cho Agent (hệ thống quy trình và quy tắc)
├── README.md                         # Tài liệu giới thiệu và hướng dẫn sử dụng skill này (file này)
├── templates/                        # Các biểu mẫu chuẩn phục vụ thiết kế và làm báo cáo
│   ├── feature-input-template.md           # Mẫu điền thông tin mô tả tính năng đầu vào
│   ├── domain-testing-report-template.md   # Mẫu báo cáo kết quả Domain Testing
│   ├── boundary-value-analysis-template.md # Mẫu báo cáo kết quả Boundary Value Analysis
│   ├── bug-report-template.md              # Mẫu báo cáo lỗi chi tiết (Markdown)
│   ├── github-issue-template.md            # Mẫu chuẩn bị nội dung đẩy lên GitHub Issue
│   ├── ai-gap-analysis-template.md         # Mẫu phân tích khoảng cách kiểm thử giữa AI và Người
│   ├── ai-audit-report-template.md         # Mẫu nhật ký tương tác với công cụ AI
│   ├── ai-critique-template.md             # Mẫu viết bài tự phê bình sự hỗ trợ của AI
│   ├── test-summary-template.md            # Mẫu báo cáo tổng hợp kết quả và tự đánh giá
│   └── submission-checklist.md             # Mẫu checklist rà soát hồ sơ nộp bài
├── checklists/                       # Các danh mục kiểm tra chất lượng từng phần
│   ├── domain-testing-checklist.md         # Check chất lượng phân vùng tương đương & test case
│   ├── bva-checklist.md                    # Check chất lượng phân tích biên & giá trị biên
│   ├── bug-report-checklist.md             # Check chất lượng viết báo cáo lỗi
│   ├── submission-checklist.md             # Check danh mục file nộp bài đầy đủ
│   └── demo-video-checklist.md             # Check chất lượng video demo tính năng
└── examples/                         # Ví dụ mẫu đã hoàn thành đầy đủ
    └── FR-07-shopping-cart-example.md      # Ví dụ minh họa tính năng giỏ hàng mẫu chạy end-to-end
```

---

## 2. Các Mức Độ Bloom-AI Đạt Được Trong Bài Tập

Skill này được thiết kế để dẫn dắt sinh viên đạt được hai cấp độ tư duy cao trong thang Bloom-AI:
* **G9.2 Apply (Áp dụng):** Thực thi đúng quy trình kiểm thử biên, phân vùng tương đương cho dữ liệu thực tế của EShop; sử dụng các công cụ GitHub CLI (`gh`) để đẩy lỗi và Git để quản lý lịch sử commit của quá trình kiểm thử.
* **G9.3 Analyse (Phân tích):** Thực hiện AI Gap Analysis để so sánh tư duy kiểm thử của con người với AI; viết AI Critique phân tích điểm yếu logic của mô hình ngôn ngữ lớn; phân tích nguyên nhân gốc rễ của bug và đề xuất phương án sửa lỗi (suggested fix).

---

## 3. Cách Kích Hoạt Và Sử Dụng Skill

1. Đảm bảo thư mục `eshop-domain-bva-testing-skill/` nằm trong thư mục `.agents/skills/` của workspace dự án của bạn.
2. Sao chép file `templates/feature-input-template.md` ra một thư mục tạm hoặc thư mục bài làm của bạn, điền đầy đủ thông tin về tính năng bạn muốn test.
3. Khi chat với Agent, hãy chỉ ra đường dẫn tới file mô tả tính năng của bạn và yêu cầu:
   > *"Hãy sử dụng skill eshop-domain-bva-testing-skill để thực hiện thiết kế test case cho tính năng được mô tả tại [đường dẫn đến file feature-input của bạn]."*
4. Agent sẽ đọc file cấu hình đó và lần lượt dẫn dắt bạn qua 20 bước kiểm thử được mô tả trong `SKILL.md`.
