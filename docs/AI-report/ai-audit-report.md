# **AI Audit Report**

## **Khai báo sử dụng AI**

Em sử dụng các công cụ AI cho các nhiệm vụ sau:

* Phân tích yêu cầu (FR-05, FR-10, FR-11, FR-19)
* Hỗ trợ kỹ thuật kiểm thử Domain Testing và Boundary Value Analysis
* Sinh và tinh chỉnh test case
* Điều chỉnh phạm vi kiểm thử (chuyển từ API + UI sang UI-only cho mobile)
* Hỗ trợ viết tài liệu và ghi log audit

---

## **Interaction 001**

### **Công cụ AI**

GitHub Copilot

### **Thời gian**

25/06/2026 08:02 AM

### **Prompt**

using skill domain-testing to analyze FR-05

### **Tóm tắt output AI**

* Phân tích Domain Testing cho FR-05 (module sản phẩm)
* Xác định các miền dữ liệu cho chức năng danh sách và tìm kiếm sản phẩm
* Sinh **12 test case**
* Bao gồm:

  * tìm kiếm hợp lệ
  * input rỗng
  * ký tự đặc biệt
  * giới hạn độ dài chuỗi

### **Đánh giá**

* Accepted: 12
* Modified: 0
* Rejected: 0

---

## **Interaction 002**

### **Công cụ AI**

Antigravity (Gemini 3.5 Flash)

### **Thời gian**

27/06/2026 08:03 AM

### **Prompt**

using domain-testing to analyze FR11

### **Tóm tắt output AI**

* Phân tích Domain Testing + Boundary Value Analysis cho FR-11 (Lịch sử đơn hàng)
* Sinh **10 test case**
* Bao gồm:

  * phân trang danh sách đơn hàng
  * trạng thái danh sách rỗng
  * xử lý dữ liệu lớn

### **Đánh giá**

* Accepted: 10
* Modified: 0
* Rejected: 0

---

## **Interaction 003**

### **Công cụ AI**

Antigravity (Claude Sonnet 4.6 Thinking)

### **Thời gian**

28/06/2026 12:26 AM

### **Prompt**

using domain-testing skill to analyze FR-19

### **Tóm tắt output AI**

* Phân tích Domain Testing + BVA cho module Quản lý người dùng (FR-19)
* Sinh **20 test case**
* Bao gồm:

  * phân quyền (admin/user/unauthenticated)
  * kiểm tra xóa user
  * ràng buộc self-delete
  * kiểm tra hiển thị dữ liệu (không lộ mật khẩu)
  * kiểm tra biên user_id (0, 1, max, invalid string)
  * kiểm tra số lượng user (0, 1, 50+)

### **Đánh giá**

* Accepted: 20
* Modified: 0
* Rejected: 0

---

## **Interaction 004**

### **Công cụ AI**

Antigravity (Claude Opus 4.6 Thinking)

### **Thời gian**

28/06/2026 09:40 PM

### **Prompt**

sử dụng domain-testing để phân tích FR-10 Mobile (Order State Machine), tham khảo thêm FR-20

### **Tóm tắt output AI**

* Phân tích trạng thái đơn hàng trên mobile (FR-10 + FR-20)
* Ban đầu sinh 30 test case
* Bao gồm cả test API + UI (không phù hợp phạm vi mobile UI)

### **Đánh giá**

* Yêu cầu chỉnh sửa: loại bỏ test API, chỉ giữ UI

---

## **Interaction 005**

### **Công cụ AI**

Antigravity (Claude Opus 4.6 Thinking)

### **Thời gian**

28/06/2026 10:07 PM

### **Prompt**

Loại bỏ test API, chỉ giữ UI testing cho mobile và cập nhật báo cáo domain-testing

### **Tóm tắt output AI**

* Tinh chỉnh bộ test case FR-10 từ **30 xuống 22 test case**
* Loại bỏ toàn bộ test liên quan API (JWT, gọi API trực tiếp, validate order_id qua API)
* Giữ lại test UI theo hành vi người dùng
* Chuẩn hóa lại test case TC-001 → TC-022
* Cập nhật báo cáo domain-testing theo phạm vi mới: **UI-only**

### **Đánh giá**

* Accepted: 22
* Modified: 0
* Rejected: 0

---

## **Interaction 006**

### **Công cụ AI**

Antigravity (Claude Sonnet 4.6 Thinking)

### **Thời gian**

06/29/2026 03:00 PM

### **Prompt**

using decision-table-pairwise-testing skill to analyze FR-10

### **Tóm tắt output AI**

* Phân tích Decision Table Testing + Pair-wise Testing cho FR-10 (Order State Machine)
* Xác định 3 Conditions: Current State (5 giá trị), Target State (5 giá trị), Role (2 giá trị)
* Xác định 3 Results: R1 (Allow), R2 (Unauthorized), R3 (Invalid Transition)
* Xây dựng Decision Table với **28 rules** bao phủ toàn bộ State Machine
* Phân tích Risk: 10 High, 4 Medium, 14 Low
* Áp dụng Pair-wise Testing: giảm từ 28 xuống **19 test case** (giảm 32%)
* Sinh **19 test case** file riêng biệt tại `tests/test-cases/ORDER/`
* Tạo báo cáo phân tích tại `docs/decision-table-pairwise-analysis.md`

### **Đánh giá**

* Accepted: 19
* Modified: 0
* Rejected: 0

---

## **Interaction 007**

### **Công cụ AI**

Antigravity (Gemini 3.5 Flash)

### **Thời gian**

06/29/2026 04:15 PM

### **Prompt**

Chạy toàn bộ 19 test case và cập nhật status, nếu có bug thì report bug

### **Tóm tắt output AI**

* Thiết lập và khởi chạy Backend Server của EShop.
* Tạo script PowerShell `tests/run-order-tests.ps1` để tự động thực thi 19 test case thông qua REST API.
* Kết quả chạy thực tế: **14 PASS, 5 FAIL**.
* Cập nhật Actual Result và Status của tất cả 19 file test case trong thư mục `tests/test-cases/ORDER/`.
* Phát hiện và lập báo cáo chi tiết cho **3 lỗi nghiêm trọng** mới liên quan đến logic State Machine và Phân quyền của Đơn hàng trong file `docs/bug-report.md`.

### **Đánh giá**


* Accepted: 19 test case updates & 3 bug reports
* Modified: 0
* Rejected: 0

---

## **Interaction 008**

### **Công cụ AI**

Antigravity (Gemini 3.5 Flash)

### **Thời gian**

07/06/2026 03:45 PM

### **Prompt**

using state-transition-testing skill to analysis FR-03

### **Tóm tắt output AI**

* Phân tích State Transition Testing cho FR-03 (Quên mật khẩu & Đặt lại mật khẩu)
* Xác định 4 States, 9 Actions, 36 dòng State Transition Table.
* Xác định 4 Valid Transitions và 5 Invalid Transitions.
* Sinh **4 Test Case** (phiên bản cũ của SKILL, gộp nhiều Coverage vào ít file).
* Tạo báo cáo phân tích kiểm thử tại `docs/state-transition-analysis.md`.

### **Đánh giá**

* Accepted: 4 test cases & 1 report
* Modified: 0
* Rejected: 0

---

## **Interaction 009**

### **Công cụ AI**

Antigravity (Claude Sonnet 4.6 Thinking)

### **Thời gian**

07/06/2026 04:00 PM

### **Prompt**

/state-transition-testing analysis FR-03

### **Tóm tắt output AI**

* Tái phân tích FR-03 theo SKILL.md phiên bản mới với quy tắc: mỗi valid Transition PHẢI có Dedicated Test Case riêng biệt, không được giảm hoặc gộp Test Case.
* Xác định 4 States, 9 Actions, 36 dòng State Transition Table.
* Xác định 4 Valid Transitions và 5 Invalid Transitions (có định nghĩa hành vi).
* Sinh **20 Test Case** theo đúng 7 nhóm Coverage:
  * 4 Dedicated Valid Transition Test Cases (TC-ST-FORGOT-PASSWORD-001 đến 004)
  * 5 Invalid Transition Test Cases (TC-ST-FORGOT-PASSWORD-005 đến 009)
  * 4 1-switch Test Cases (TC-ST-FORGOT-PASSWORD-SW1-001 đến SW1-004)
  * 4 n-switch Test Cases (TC-ST-FORGOT-PASSWORD-SW2-001 đến SW2-004)
  * 2 End-to-End Test Cases (TC-ST-FORGOT-PASSWORD-E2E-001 đến E2E-002)
  * 1 Final State Test Case (TC-ST-FORGOT-PASSWORD-FINAL-001)
* Cập nhật báo cáo phân tích tại `docs/state-transition-analysis.md`.

### **Đánh giá**

* Accepted: 20 test cases & 1 report
* Modified: 0
* Rejected: 0

---

## **Interaction 010**

### **Công cụ AI**

Antigravity (Gemini 3.5 Flash)

### **Thời gian**

07/06/2026 05:10 PM

### **Prompt**

/use-case-testing analyze FR-03

### **Tóm tắt output AI**

* Phân tích Use Case Testing cho FR-03 (Quên mật khẩu & Đặt lại mật khẩu).
* Xác định 2 Actors, 3 Use Cases, 1 Main Flow, 1 Alternative Flow, 5 Exception Flows.
* Sinh bộ **7 Test Cases** (TC-UC-FORGOT-PASSWORD-001 đến 007).
* Viết tập lệnh tự động hóa Playwright để thực thi các test cases trên trình duyệt thực tế.
* Kết quả chạy thực tế: **2 PASS, 5 FAIL**.
* Phát hiện và lập báo cáo thêm cho **2 lỗi nghiêm trọng** mới (BUG-FR03-004: Lỗi regex kiểm duyệt mật khẩu ở giao diện; BUG-FR03-005: Thiếu trường Xác nhận mật khẩu ở Bước 2/2) trong `bug-report.md`.
* Cập nhật Actual Result và Status của tất cả 7 test case trong `tests/test-cases/forgot-password/`.
* Tạo báo cáo phân tích chi tiết tại `docs/use-case-testing-analysis.md`.

### **Đánh giá**

* Accepted: 7 test cases, 1 analysis report, 2 bug reports
* Modified: 0
* Rejected: 0

