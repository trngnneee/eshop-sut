# Kế hoạch usability test U-01

## Phạm vi

- Website: <https://lumierecinema-testing-demo-ui.vercel.app/>
- Flow: **U-01**
- FR: **FR-14, FR-15, FR-18, FR-19, FR-20, FR-35, FR-37**
- Mẫu: 3 người tham gia thật, mã hóa P01–P03.
- Phương pháp: moderated think-aloud.
- Timebox: 10 phút/người.
- Ngày dự kiến: CHƯA THU THẬP.
- Moderator: CHƯA THU THẬP.

## Mục tiêu nghiên cứu

1. Xác định người dùng có nhận ra cách bắt đầu tìm và đặt vé hay không.
2. Xác định người dùng có chọn được phim, rạp và suất chiếu mà không cần hướng dẫn hay không.
3. Xác định người dùng có hiểu số lượng vé, trạng thái ghế và chọn đúng 2 ghế hay không.
4. Xác định người dùng có nhận ra hành động tiếp theo để đi đến thông tin vé hay không.a
5. Ghi nhận mức dễ dùng, sự tự tin và độ rõ ràng của phản hồi hệ thống.

## Task scenario

> Bạn muốn xem một phim đang chiếu tại Lumiere Cinema vào cuối tuần này. Hãy tìm một phim phù hợp, chọn rạp, chọn suất chiếu, chọn ghế cho 2 người và hoàn tất đến khi bạn thấy thông tin vé.

## Chỉ số

- Outcome: `SUCCESS_UNASSISTED`, `SUCCESS_ASSISTED`, `FAIL`, `ABANDONED`.
- Task time: số giây từ khi participant bắt đầu đến end state.
- Error: hành động gây trạng thái sai, lỗi hoặc phải phục hồi.
- Wrong turn: đi vào màn hình/chức năng không phục vụ task rồi quay lại.
- Hesitation: dừng ít nhất 5 giây, kèm vị trí và biểu hiện.
- Intervention: moderator cung cấp gợi ý có nội dung giúp tiến tới bước kế tiếp.
- Post-session rating: ba câu 1–5.

## Ba câu đánh giá sau phiên

1. “Bạn thấy task này dễ hoàn thành ở mức nào?” — 1: rất khó, 5: rất dễ.
2. “Bạn tự tin mình đã chọn đúng phim, suất và 2 ghế ở mức nào?” — 1: không tự tin, 5: rất tự tin.
3. “Thông tin và phản hồi của hệ thống rõ ràng ở mức nào?” — 1: rất không rõ, 5: rất rõ.

Sau mỗi câu hỏi: “Điều gì khiến bạn cho điểm như vậy?” và ghi quote nguyên văn.

## Quy tắc can thiệp

- Không chỉ đường hoặc xác nhận đúng/sai trong khi participant còn tự thử.
- Khi participant kẹt hoàn toàn, hỏi trung lập trước: “Bạn mong đợi điều gì xảy ra ở đây?”
- Nếu vẫn không tiến triển, cho một gợi ý tối thiểu; ghi nguyên văn gợi ý và đánh outcome là `SUCCESS_ASSISTED` nếu hoàn thành.

## Severity

| Mức | Quy tắc áp dụng |
| --- | --- |
| S1 | Vấn đề khiến participant không hoàn thành task. |
| S2 | Hoàn thành nhưng cần trợ giúp hoặc mắc nhầm lẫn nghiêm trọng. |
| S3 | Hoàn thành nhưng chậm hoặc do dự đáng kể. |
| S4 | Vướng nhỏ, ít ảnh hưởng đến tiến độ. |

Severity dựa trên tác động quan sát được; frequency chỉ là bằng chứng bổ sung, không tự động quyết định severity.

## Checklist trước phiên

- [ ] Có đồng thuận tham gia và ghi hình/chụp ảnh nếu áp dụng.
- [ ] Chỉ dùng mã P01–P03; không ghi dữ liệu cá nhân không cần thiết.
- [ ] Kiểm tra website và đồng hồ.
- [ ] Chuẩn hóa start state.
- [ ] Tắt autofill, extension hoặc tab có thể gợi ý thao tác.
- [ ] Không cho participant tập flow trước.
- [ ] Chuẩn bị phương án deviation nếu cuối tuần không có suất.

