# Stage 0 — Drive inventory và participant mapping

**Ngày kiểm tra ban đầu:** 2026-07-29
**Replacement D06 nhận:** 2026-07-29
**Timezone:** Asia/Bangkok (UTC+7)
**SUT:** EShop Web Frontend
**Chế độ truy cập:** Chỉ đọc; không sửa, xóa, đổi tên hoặc chia sẻ file Drive
**Trạng thái:** `COMPLETE_WITH_DISCLOSED_LIMITATIONS — HUMAN_REVIEWED — CONFIRMED_MISSING_DATA`

## Kết luận gate sau replacement

- Mapping được người dùng xác nhận: `D01→P01`, `D02→P02`, `D03→P03`, `D04→P04`, `D05→P05`, `D06→P06`, `D07→P07`.
- Tên nguồn là số điện thoại/contact PII. Báo cáo chỉ dùng D01–D07 và P01–P07, không ghi số điện thoại hoặc tên thật.
- File D06 cũ từng là duplicate byte-for-byte của D01. Người dùng đã cung cấp replacement D06 mới qua một Drive link riêng; bản cũ được loại khỏi official analysis nhưng không bị sửa/xóa trên Drive.
- Replacement D06 có SHA-256 `544EDA05B62A17088F8967433C20AF72056A080179ECB38ACE90F18CA8E31E1A`, khác D01 `EA10D38B2EF8DA138F00989337C9476BEEA06BF9EC646D47957FC052A4B2248D`. Official inventory hiện có 7 recording contents độc lập.
- Người dùng xác nhận D02, D03, D05 và replacement D06 là toàn bộ session, không phải file upload bị cắt: P02 kết thúc trên phone alert, P03 kết thúc sau 4 giây ở register, P05 kết thúc ở login, P06 kết thúc trên weak-password error.
- Cả 7 official files có audio stream nhưng không file nào có speech dùng được. Replacement D06 có low-level signal, song VAD phát hiện 0 speech segments; canned ASR hallucinations bị loại bỏ.
- Không tìm thấy pilot riêng và người dùng xác nhận pilot không được thu thập: **PILOT EVIDENCE MISSING**.

## Official inventory sau replacement

| File | Participant ID | Duration | Screen | Audio | Complete/cut | Accessible | Notes |
|---|---|---:|---|---|---|---|---|
| [D01](https://drive.google.com/file/d/1_S4NoOyGboNTjEocl4Ilv-i8eGP6MMIh/view) | P01 | 00:01:52 | YES | Stream YES; speech NO | COMPLETE-LOOKING | YES | MP4/H.264, 1920×1032, AAC stereo, 9.34 MiB. Product list → register → login → profile attempts → logout. |
| [D02](https://drive.google.com/file/d/1zwZUcapIakre5MtRjn8EvrwHTlC1Vyje/view) | P02 | 00:01:34 | YES | Stream YES; speech NO | COMPLETE — CONFIRMED | YES | MP4/H.264, 2558×1350, AAC stereo, 15.32 MiB. Session kết thúc trên phone-validation alert; chưa có persistence/logout. |
| [D03](https://drive.google.com/file/d/1U2oLdr3iu9W8u6FFc-Uur83DzWDGkldh/view) | P03 | 00:00:04 | YES | Stream YES; speech NO | COMPLETE — CONFIRMED | YES | MP4/H.264, 1376×736, AAC stereo, 3.06 MiB. Toàn bộ session chỉ thấy register; non-monotonic DTS warning nhưng decode được. |
| [D04](https://drive.google.com/file/d/1rLeBwRJjE5S2aDyROS6vZvFL5nNSW76M/view) | P04 | 00:02:16 | YES | Stream YES; usable speech NO | COMPLETE-LOOKING | YES | MP4/H.264, 2556×1470, AAC stereo, 256.40 MiB. Flow tới logout; chỉ khoảng 0,2 giây non-silent signal. |
| [D05](https://drive.google.com/file/d/18IQu0ttl7dCO1s6LL0yJnjvfGVnpc6aj/view) | P05 | 00:00:51 | YES | Stream YES; speech NO | COMPLETE — CONFIRMED | YES | MP4/HEVC portrait, 1242×2688, AAC stereo, 26.57 MiB. Register thành công rồi session kết thúc ở login; không có login submit/result. |
| [D06 replacement](https://drive.google.com/file/d/19Mo8J_MOYr-5qSfFh0gRzbAoItlTW-08/view) | P06 | 00:00:53 | YES | Stream YES; speech NO | COMPLETE — CONFIRMED | YES | MP4/HEVC portrait, 1126×2436, AAC stereo, 41.11 MiB. Session kết thúc sau bốn weak-password registration errors; chưa tới login. Full-decode PASS với DTS warnings. |
| [D07](https://drive.google.com/file/d/15vhKH-DHLNunVm1PgYolzLq2SlsZhC3B/view) | P07 | 00:01:06 | YES | Stream YES; speech NO | COMPLETE-LOOKING | YES | MP4/H.264, 1920×1008, AAC stereo, 75.82 MiB. Register → failed login/recovery → profile view → logout; DTS warning nhưng decode được. |

## Xác nhận Stage 0

| Kiểm tra | Kết quả | Bằng chứng |
|---|---|---|
| Truy cập official sources | PASS | 7/7 official source files tải và full-decode được. |
| Mapping D01–D07→P01–P07 | PASS | Người dùng xác nhận thứ tự; replacement source được gán P06. |
| 7 recording contents độc lập | PASS AFTER REPLACEMENT | Replacement D06 có hash khác D01; old duplicate bị loại khỏi analysis. |
| Video pilot riêng | FAIL | **PILOT EVIDENCE MISSING**. |
| File bị cắt/upload thiếu | NO — USER CONFIRMED | Cả 7 file là toàn bộ session; D02/D03/D05/D06 là early-ended failed sessions. |
| Khả năng phát/decode | PASS WITH WARNINGS | D03, D07 và replacement D06 có non-monotonic DTS; không có decode failure. |
| Audio speech usable | FAIL | 0/7 có speech đủ dùng; không có quote/moderator/SUS/probe audio. |

## Privacy gate

`PASSWORD_VISIBLE_IN_RECORDING — REDACTION_REQUIRED` được xác nhận ở D01/P01, D02/P02, D04/P04, D05/P05 và D07/P07. Replacement D06/P06 chỉ hiển thị registration password ở dạng masked; name và email vẫn cần redaction. Mọi screenshot/clip còn phải che name, email, phone, address và browser PII.

## Trạng thái sau xác nhận

1. Không cần cung cấp thêm phần video cho D02, D03, D05 hoặc D06; task-end đã được chốt tại recording end.
2. SUS Q1–Q10 không xuất hiện trong Drive recordings; dataset riêng được người dùng cung cấp ngày 2026-07-31 và xác nhận dùng participant ID P01–P07 ngày 2026-08-02. Post-session probes, consent supplement và pilot vẫn `NOT_RECORDED`/`PILOT EVIDENCE MISSING`.
3. Moderator/intervention/Card B vẫn `NOT_OBSERVABLE` vì không có usable speech hoặc notes nguồn.
4. Redact toàn bộ PII và plaintext password trước khi trích evidence ra khỏi khu vực kiểm soát truy cập.

## Authenticated Drive recheck — 2026-08-02

- Drive metadata traced all official D01–D07 links to the same `Khoa` folder (`13N2LhCqzcD524D3ScSR4rEt4ofWFoAan`).
- A direct folder listing returned eight items, all `video/mp4`: the seven official sources plus one excluded/superseded recording. No document, spreadsheet, form or subfolder was present.
- The parent `HW3` folder (`1uqlcG1PRR-uNuHnVNhHsFeEBOl6NSM-_`) contained participant folders and two screen/flow-allocation files only. No pilot record, consent record, probe notes or SUS collection artefact was present.
- Broader authenticated Drive searches for `HW03 pilot`, `HW03 consent`, `HW03 SUS`, `HW03 usability`, `pilot`, `consent`, `SUS` and `usability` returned no relevant EShop fieldwork record.
- This negative inventory does not prove that consent never occurred; it proves only that no auditable artefact was available in the supplied/accessible sources. The missing fields therefore remain missing and were not reconstructed.
