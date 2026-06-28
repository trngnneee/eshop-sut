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
