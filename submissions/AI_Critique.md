# Phê bình AI (AI Critique) – HW05 Kiểm thử hiệu năng

**Sinh viên thực hiện:** Phan Quốc Thịnh  
**MSSV:** 23127486  
**Môn học:** CS423 / CSC13003 – Kiểm thử phần mềm (Định hướng AI · 2026)  
**Bài tập:** HW05 – Kiểm thử hiệu năng (Performance Testing)  
**Số lượng từ:** 255 từ (Yêu cầu: 200–300 từ)

---

## 1. Đoạn văn phê bình năng lực AI (AI Critique: 200–300 từ)

> **Hướng dẫn:** Viết một đoạn văn từ 200–300 từ đánh giá, phản biện khách quan về AI. Cần giải quyết đầy đủ 3 câu hỏi trọng tâm:
> - AI đã đưa ra những nhận định sai sót, thiên lệch hoặc chưa đầy đủ ở đâu?
> - Tại sao AI lại mắc phải các sai sót hoặc không phát hiện được vấn đề đó?
> - Bạn đã rút ra nguyên tắc nào về việc hợp tác với AI trong quá trình thực hiện bài tập này?

Trong quá trình thực hiện kiểm thử hiệu năng HW05, AI (Claude Sonnet 4.6) bộc lộ sự sai sót và ảo giác (hallucination) rõ nét khi phân tích chuyên sâu về kiến trúc SUT và số liệu log JTL. Cụ thể, AI tự suy diễn rằng cơ sở dữ liệu SQLite đang chạy ở chế độ `WAL mode` và sử dụng thư viện đồng bộ `better-sqlite3`, trong khi codebase thực tế dùng driver bất đồng bộ `sqlite3` ở chế độ rollback journal mặc định. Ngoài ra, AI còn "tưởng tượng" endpoint `POST /api/checkout` thực hiện một chuỗi giao dịch phức tạp (cập nhật tồn kho, xóa giỏ hàng) và gán nhầm giá trị p99 của toàn bộ bài test cho riêng giai đoạn Phase 3. Nguyên nhân của các sai sót này xuất phát từ việc mô hình LLM có xu hướng ngoại suy theo khuôn mẫu phổ biến của các ứng dụng thương mại điện tử thực tế và thói quen phỏng đoán cấu hình tối ưu thay vì kiểm tra mã nguồn thực tế; đồng thời AI nhầm lẫn giữa định dạng log thô từng dòng kèm mốc thời gian của JTL với bảng tổng hợp dữ liệu tĩnh. Qua bài tập này, nguyên tắc cốt lõi tôi rút ra khi cộng tác cùng AI là: AI là công cụ sinh khung mã lệnh và gợi mở ý tưởng rất mạnh mẽ, nhưng con người bắt buộc phải giữ vai trò làm chủ và kiểm soát (Human-in-the-Loop). Mọi giả định kỹ thuật, đề xuất tối ưu hóa hay phân tích số liệu của AI đều phải được đối chiếu nghiêm ngặt với mã nguồn thực tế và dữ liệu đo đạc khách quan trước khi đưa ra quyết định kỹ thuật.

---

## 2. Các câu hỏi định hướng phân tích (Guiding Questions)

1. **AI đã mắc sai sót hoặc bộc lộ sự thiên lệch ở đâu?**
   - Tự gán các thuộc tính kiến trúc không có thật (SQLite WAL mode, driver `better-sqlite3`).
   - Suy diễn sai cơ chế hoạt động nội bộ của endpoint checkout (nghĩ rằng có trừ kho và xóa cart trong DB, trong khi thực tế cart chỉ lưu in-memory).
   - Hiểu sai bản chất file log JTL khi cho rằng không thể tách riêng dữ liệu theo từng giai đoạn (phase).

2. **Tại sao AI lại không nắm bắt chính xác vấn đề?**
   - Do AI bị chi phối bởi các mẫu dữ liệu phổ biến trong tập huấn luyện (các ứng dụng e-commerce tiêu chuẩn thường dùng WAL và trừ kho trong DB).
   - Prompt ban đầu cung cấp số liệu dạng tổng hợp (aggregate) khiến AI tự suy diễn chi tiết mà không yêu cầu thêm log thô.
   - Hạn chế về tri thức đặc thù (domain-specific) đối với cấu trúc log dòng thời gian của Apache JMeter.

3. **Nguyên tắc rút ra khi làm việc cùng AI là gì?**
   - Phải phân rã bài toán thành từng bước nhỏ, cung cấp ngữ cảnh cụ thể và đặt ra ranh giới kiểm duyệt rõ ràng.
   - Không chấp nhận nguyên văn các đề xuất tối ưu hóa hệ thống nếu chưa kiểm tra tính tương thích trên mã nguồn thực tế.
   - AI đóng vai trò là "trợ lý tăng cường tốc độ", còn trách nhiệm thẩm định và quyết định cuối cùng luôn thuộc về kỹ sư kiểm thử.
