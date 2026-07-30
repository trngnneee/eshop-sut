---
name: usability-testing-skill
description: Lập kế hoạch, thu thập và kiểm tra tính đầy đủ của Task 2 HW03 EShop với đúng 7 participant thật, SUS raw responses, moderated sessions, severity findings và anti-fabrication gates.
---

# Usability Testing Skill — HW03

## 1. Nguyên tắc không thương lượng

- SUT là EShop; chọn đúng một end-to-end flow. Không tái sử dụng dữ liệu Lumiere hoặc đề khác.
- Có **đúng 7 participant thật**, mã P01–P07 và contact có thể xác minh (che bốn số giữa).
- AI không tự tạo tên, contact, quote, task time, hành vi, rating, recording hoặc SUS response.
- Dữ liệu chưa do người làm bài nhập từ phiên thật phải để `<REQUIRED_REAL_DATA>` và `UNVERIFIED`.
- Pilot là phiên riêng, không tính vào bảy phiên chính thức.
- Chỉ báo `COMPLETE` khi bảy session thật đã hoàn tất và validator đạt.

## 2. Phase 1 — Plan & Prepare

1. Ghi 3–5 research objectives.
2. Viết task scenario theo mục tiêu, không chỉ dẫn click.
3. Chọn SUS 10 câu hoặc UEQ-S 8 cặp. Custom scale phải có giải trình.
4. Chuẩn bị bốn probe: Clarity, Error Recovery, Speed, Trust.
5. Lập roster P01–P07, trạng thái ban đầu `UNVERIFIED`.
6. Chuẩn bị consent cho tham gia, screen recording và audio.
7. Chạy pilot, ghi vấn đề và thay đổi trước các phiên chính thức.

## 3. Phase 2 — Conduct 7 Sessions

- Đọc moderator script: “Chúng tôi kiểm thử sản phẩm, không kiểm thử bạn”; yêu cầu think aloud.
- Không dẫn dắt; ghi nguyên văn mọi intervention.
- Mỗi session lưu date/time, device/browser, consent; outcome; task time, wrong turns, hesitations >=5s, errors, interventions; timestamped notes/quotes; raw SUS Q1–Q10; bốn probes; recording/evidence path hoặc lý do từ chối.
- Không chuyển template thành Completed nếu còn placeholder.

## 4. Phase 3 — Analyse & Report

- SUS: odd contribution = response - 1; even = 5 - response; tổng ×2.5. Lưu raw responses và phép tính.
- Tính mean, median, min, max cho đủ bảy người; không suy diễn significance từ mẫu nhỏ.
- Tách usability issue khỏi software bug. Mỗi finding có participant IDs, frequency, evidence, impact, severity, recommendation, retest criterion.
- S1: không hoàn thành; S2: cần trợ giúp/nhầm nghiêm trọng; S3: chậm/do dự đáng kể; S4: vướng nhỏ.
- Expert/pilot finding phải gắn `PROVISIONAL`; không trình bày như participant-validated.
- Mọi genuine software bug được chuẩn bị GitHub Issue, không chỉ S1/S2.

## 5. Deliverables

`Usability_Test_Plan.md`, `Participant_Roster.md`, `Pilot_Session.md`, `Instruments/SUS_Form.md`, `Instruments/Post_Session_Probes.md`, `Sessions/Session_P01.md`…`P07.md`, `Usability_Findings.md`, `Usability_Bug_Report.md`, `Usability_Test_Summary.md`, evidence index, AI Audit, AI Critique, commit log và demo-video link.

## 6. Completion validator

Chạy `scripts/validate-usability.ps1`. Chỉ báo `COMPLETE` khi P01–P07 có dữ liệu thật/contact masked/Completed; bảy session không còn placeholder và có raw scale/probes; có pilot/refinement; có score tổng hợp/findings/evidence; không có dữ liệu mô phỏng hoặc SUT khác; có bug/GitHub traceability.

Nếu thiếu dữ liệu người thật, kết thúc ở `READY_FOR_FIELDWORK`, liệt kê dữ liệu cần người làm bài cung cấp; không tự lấp chỗ trống.
