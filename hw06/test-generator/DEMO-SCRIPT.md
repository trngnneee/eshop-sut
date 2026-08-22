# Kịch bản quay video demo Agent Skill (R-10)

> Mục tiêu: ~3 phút, chứng minh **bạn hiểu công cụ mình xây**, không phải chỉ chạy được lệnh.
> Điểm mấu chốt của R-10 không nằm ở chỗ generator sinh ra nhiều case, mà ở chỗ bạn giải thích được
> **vì sao output của nó chưa phải test case cuối cùng**.

## Chuẩn bị trước khi bấm ghi

- [ ] Mở sẵn 2 cửa sổ: terminal (PowerShell, phóng chữ lên ~16pt) và VS Code
- [ ] VS Code mở sẵn 4 tab theo thứ tự: `SKILL.md` · `login.endpoint.json` · `generator.py` · `diagram.png`
- [ ] `cd "C:\My Workspace\HCMUS\Test\Week 3\Hw2"` và `Clear-Host`
- [ ] Tắt thông báo Windows (Focus assist), tắt Discord/Zalo
- [ ] Ghi bằng OBS hoặc Xbox Game Bar (`Win + Alt + R`), 1080p, có mic
- [ ] **Không** để lộ mật khẩu, token, email cá nhân trên màn hình

---

## Beat 1 — Mở đầu (0:00 – 0:20)

**Màn hình:** VS Code, tab `SKILL.md`

> "Chào thầy/cô, em là Đặng Đăng Khoa, MSSV 23127207. Đây là demo Agent Skill
> `api_test_generator` em xây cho HW06. Nó nhận mô tả một endpoint và sinh ra bộ test case
> có thể audit được, theo bốn kỹ thuật: phân vùng, chuyển trạng thái, bảo mật và schema."

## Beat 2 — Vì sao là Agent Skill, không phải script rời (0:20 – 0:50)

**Màn hình:** cuộn `SKILL.md`, dừng ở mục *Required five-step process*

> "Điểm khiến nó là một Skill chứ không phải script rời là phần quy trình bắt buộc này.
> Skill ràng buộc AI phải đi đủ năm bước — P1 mô hình input và state, P2 phân vùng và biên,
> P3 ma trận chuyển trạng thái, P4 bảo mật, P5 schema — thay vì hỏi một prompt tổng
> rồi nhận về một đống case không kiểm soát được."

**Dừng ở dòng cuối SKILL.md, đọc to:**

> "Và dòng cuối cùng ghi rõ: *never mark a case human-approved automatically*.
> Đây là ràng buộc em cố ý đặt vào, em sẽ quay lại ở cuối video."

## Beat 3 — Đầu vào (0:50 – 1:20)

**Màn hình:** tab `login.endpoint.json`

> "Đầu vào là một file JSON gọn: parameters với miền giá trị, states với trạng thái đầu và
> kết quả mong đợi, security, và response schema. Mỗi mục đều có trường `requirement` —
> đây là thứ giữ cho traceability không đứt: mọi case sinh ra đều truy ngược được về FR hoặc SEC."

## Beat 4 — Chạy generator (1:20 – 1:50)

**Màn hình:** terminal

```powershell
python hw06\test-generator\generator.py .agents\skills\api_test_generator\examples\login.endpoint.json --out demo\generated.md
```

> "Chạy xong nó trả về một dòng JSON: 12 case, và kết quả audit hook."

**Mở `demo\generated.md`:**

> "Mỗi dòng có ID ổn định dạng `TC-API-LOGIN-###`, nhóm kỹ thuật, tiền điều kiện, dữ liệu,
> kết quả mong đợi và requirement nguồn. Nó cũng xuất kèm một Postman skeleton."

## Beat 5 — Audit hook bắt lỗi (1:50 – 2:20) ★ nhịp quan trọng nhất

**Màn hình:** terminal

```powershell
python hw06\test-generator\generator.py hw06\test-generator\examples\demo-missing-expected.endpoint.json --out demo\broken.md
```

**Kết quả sẽ ra:**

```json
{"cases": 3, "audit": {"count": 3, "duplicate_ids": 0, "missing_expected": ["TC-API-DEMO-001", "TC-API-DEMO-002"]}}
```

> "Em cố ý đưa vào một spec thiếu `expected`. Audit hook chỉ đúng hai case hỏng.
> Nó kiểm ba thứ máy làm được: ID trùng, expected rỗng, và oracle không an toàn.
> Nhưng nó **không** kiểm được expected đó có đúng đặc tả hay không — chỗ đó phải là người."

## Beat 6 — Giới hạn và cổng human review (2:20 – 2:50) ★ chốt điểm

**Màn hình:** `diagram.png` (sơ đồ tự vẽ)

> "Sơ đồ này là thiết kế của em. Input đi qua parser, tạo Parameter và State Model,
> rồi tách ra bốn nhánh sinh test độc lập, hội tụ về Test Case IR."

**Chỉ vào khối Human Review Gate:**

> "Khối quan trọng nhất là cổng này. Generator sinh 12 case cho API login,
> nhưng bảng cuối cùng của em có 42 case. Chênh lệch đó là phần con người làm:
> audit lại nhãn, và bổ sung các case mà máy không thể tự nghĩ ra."

**Ví dụ cụ thể — nói ít nhất một cái:**

> "Ví dụ `TC-API-LOGIN-039` — kiểm response **không** được chứa field `password`.
> Generator chỉ biết kiểm field nào *phải có*, nó không tự lập được danh sách field *bị cấm*.
> Case đó là do em thêm, và nó chính là case bắt được bug D-LOGIN-03, issue #415."

## Beat 7 — Kết (2:50 – 3:00)

> "Tóm lại, generator tạo scaffold có cấu trúc và audit được, còn trách nhiệm oracle
> và kết luận cuối cùng vẫn thuộc về người kiểm thử. Em cảm ơn thầy/cô."

---

## Sau khi quay

1. Upload YouTube, đặt **Unlisted** (không cần Public)
2. Tiêu đề: `HW06 - Agent Skill Demo - 23127207`
3. Dán link vào `hw06/report/main-report.md` mục *Postman, CI và generator*, và vào `hw06/README.md`
4. Báo mình để cập nhật `ai-audit-report.md` và bảng tự chấm

## Câu vấn đáp hay bị hỏi sau demo

| Câu hỏi | Ý trả lời |
| :--- | :--- |
| Sao không để AI tự quyết expected? | Vì oracle phải đến từ đặc tả, không từ hành vi SUT. Sửa expected cho khớp bug là hỏng cả bộ test. |
| Bốn nhánh sao phải độc lập? | Để không nhánh nào che nhánh nào, và để đếm được độ phủ theo từng kỹ thuật. |
| Test Case IR để làm gì? | Tách biểu diễn khỏi cách render, nên cùng một IR xuất được cả Markdown lẫn Postman. |
| Vòng hồi tiếp trong sơ đồ chạy khi nào? | Khi audit phát hiện expected thiếu hoặc sai oracle — sửa model rồi sinh lại, không vá tay vào output. |
