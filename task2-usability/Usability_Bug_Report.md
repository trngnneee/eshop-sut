# Usability Evaluation — Software Bug Report

**Current status:** `HUMAN_REVIEWED — 3_INDEPENDENTLY_REPRODUCED — 2_EVIDENCE_COMMENTS_PUBLISHED`
**GitHub policy for this deliverable:** Duplicate search bắt buộc; dùng existing issue khi cùng defect, không tạo issue trùng.
**Privacy:** Không chép password hoặc raw name/email/phone/address.

## Bug summary

| Bug ID | Requirement/baseline | Participants | Frequency | Independent reproduction | Severity provisional | Draft | Published URL |
|---|---|---|---:|---|---:|---|---|
| BUG-PF-02 | FR-04: phone bắt đầu bằng 0 và gồm 10–11 chữ số | P01, P02, P04 | 3/7 | REPRODUCED 2026-07-31 với synthetic data | S1 | `github-issues/DRAFT-BUG-USABILITY-01.md` | https://github.com/trngnneee/eshop-sut/issues/55 |
| BUG-AUTH-PLAINTEXT-01 | Password control phải che credential mặc định | P01, P02, P04, P05, P07 | 5/7 | REPRODUCED 2026-07-31 với synthetic data | S2 | `github-issues/DRAFT-BUG-AUTH-PLAINTEXT-01.md` | https://github.com/trngnneee/eshop-sut/issues/37 |
| BUG-REG-PASSWORD-POLICY-01 | FR-01: password phải có ký tự đặc biệt trong `@ $ ! % * ? &` và các lớp bắt buộc khác | NONE — technical only | N/A | REPRODUCED 2026-08-02 bằng direct API và synthetic data | S2 | `github-issues/DRAFT-BUG-REG-PASSWORD-POLICY-01.md` | https://github.com/trngnneee/eshop-sut/issues/118 |

P06 không được tính cho BUG-AUTH-PLAINTEXT-01 vì replacement recording không tới login; frequency vẫn là 5/7.
BUG-REG-PASSWORD-POLICY-01 không có participant attribution. Input của P04/P06 bị masked nên không chứng minh họ đã nhập password thiếu ký tự đặc biệt; finding usability recovery của họ vẫn được giữ riêng.

## BUG-PF-02 — Profile rejects requirement-conforming phone format

### Requirement

FR-04 yêu cầu số điện thoại test bắt đầu bằng `0` và có 10–11 chữ số.

### Preconditions

- Một account test hợp lệ đã được tạo và login.
- User ở profile page.
- Name/address dùng dữ liệu test, không dùng PII thật.

### Reproduction steps từ participant evidence

1. Mở profile.
2. Nhập một phone test gồm 10 chữ số, bắt đầu bằng `0`; không ghi raw value trong report.
3. Submit profile update.
4. Nếu cần xác nhận boundary, thử 11 chữ số bắt đầu bằng `0`.
5. Quan sát validation feedback; trong independent retest, kiểm tra thêm một non-leading-zero value để xác định rule thực tế.

### Expected result

- Phone 10 hoặc 11 chữ số bắt đầu bằng `0` được chấp nhận khi các required fields hợp lệ.
- Non-leading-zero value bị từ chối.
- Success state/persistence phản ánh đúng dữ liệu đã lưu.

### Actual result

- P01: nhiều leading-zero attempts nhận cùng phone-invalid error; không save.
- P02: first update có 10-digit leading-zero phone nhưng bị từ chối; ba submits thất bại trước confirmed task end.
- P04: 10/11-digit leading-zero attempts bị từ chối; một non-leading-zero value nhận success alert.

### Participant evidence

- P01/D01 @ 00:00:53–00:01:49.
- P02/D02 @ 00:00:57–00:01:34.
- P04/D04 @ 00:01:43–00:02:09.
- Distinct participant frequency: 3/7.
- Genuine quote: NOT_RECORDED.

### Impact and severity

- Severity provisional: `S1`.
- P01/P02 không hoàn thành SC3; P04 chỉ nhận success với format trái FR-04 và vẫn thiếu required name/address update.
- Repeated actions: P01 4 repeats, P02 2, P04 3 profile-update repeats.

### Independent reproduction

- Required: YES.
- Status: REPRODUCED 2026-07-31 trên Chromium với account `example.com` và isolated temporary SQLite database; leading-zero phone bị reject, non-leading-zero control được accept và persisted.
- Evidence: `evidence/github-issue-reproduction/BUG-PF-02-safe-reproduction.png`; current SHA-256 `6694badca3c9906415fce4bd5dda1256ddabece431a969da6e90bf3752e1361c`.

### Evidence/redaction

- Participant timestamps vẫn là evidence riêng và không được xuất frame thô.
- Fresh screenshot chỉ dùng synthetic name/email/phone/address và không có participant PII.
- Machine-readable result: `evidence/github-issue-reproduction/result.json`.

### Potential duplicate

- Duplicate search: COMPLETE. Canonical existing issue #55; related duplicates #102, #110, #163 và #204.
- Publication action: REUSED EXISTING ISSUE — https://github.com/trngnneee/eshop-sut/issues/55. Fresh safe-reproduction evidence was published in comment https://github.com/trngnneee/eshop-sut/issues/55#issuecomment-5149476574 from evidence commit `d9bc4c0`.

## BUG-AUTH-PLAINTEXT-01 — Login password is visible as plaintext

### Requirement/baseline

Credential input phải được masked mặc định; nếu có reveal control, reveal phải explicit và reversible. Đây là security/privacy baseline và cần product owner xác nhận requirement ID nếu repository có spec riêng.

### Preconditions

- User ở login screen.
- Không dùng real password trong independent reproduction.

### Reproduction steps từ participant evidence

1. Mở login page.
2. Focus password field.
3. Nhập test characters.
4. Quan sát character rendering trước bất kỳ reveal action nào.

### Expected result

Password characters được masked mặc định; screen recording không đọc được giá trị.

### Actual result

Characters xuất hiện như text thường trong login ở năm distinct participant recordings. Không participant nào thực hiện explicit reveal action quan sát được.

### Participant evidence

- P01/D01 @ 00:00:19–00:00:33.
- P02/D02 @ 00:00:17–00:00:35.
- P04/D04 @ 00:01:01–00:01:39.
- P05/D05 @ 00:00:39–00:00:46.
- P07/D07 @ 00:00:29–00:00:48.
- Frequency: 5/7 distinct participants.
- Genuine quote/concern: NOT_RECORDED; không suy ra cảm xúc hoặc trust impact.

### Impact and severity

- Severity provisional: `S2`.
- Credential exposure trực tiếp cho người nhìn màn hình và trong recordings; không quan sát task blocking.
- Mọi original frame/clip chứa password phải coi là sensitive evidence.

### Independent reproduction

- Required: YES.
- Status: REPRODUCED 2026-07-31 trên Chromium; password field có DOM `type="text"` và hiển thị synthetic value không cần reveal action.

### Evidence/redaction

- Fresh screenshot: `evidence/github-issue-reproduction/BUG-AUTH-PLAINTEXT-01-safe-reproduction.png`.
- Screenshot chỉ hiển thị chuỗi `NotARealCredential!42`, là synthetic non-account value; không có participant credential/PII.
- SHA-256: `06866ab67ad5ac6ae1d51c3529a67292eb157e79e17ae3f598920dec88ce7d6d`.

### Potential duplicate

- Duplicate search: COMPLETE. Canonical existing issue #37; related duplicates #184 và #196.
- Publication action: REUSED EXISTING ISSUE — https://github.com/trngnneee/eshop-sut/issues/37. Fresh safe-reproduction evidence was published in comment https://github.com/trngnneee/eshop-sut/issues/37#issuecomment-5149476796 from evidence commit `d9bc4c0`.

## BUG-REG-PASSWORD-POLICY-01 — Registration API accepts a password without the required special character

### Requirement

FR-01 yêu cầu password dài tối thiểu 8 ký tự, có chữ hoa, chữ thường, chữ số và ít nhất một ký tự trong tập `@`, `$`, `!`, `%`, `*`, `?`, `&`.

### Preconditions

- Backend chạy với isolated temporary SQLite database.
- Chỉ dùng synthetic `example.com` account; không dùng participant data.
- Đây là direct API test để kiểm tra server-side enforcement, không phải quan sát usability session.

### Reproduction steps

1. Gửi `POST /api/register` với unique synthetic email và password `NoSpecial1`.
2. Xác nhận password có 10 ký tự, có uppercase/lowercase/digit nhưng không có ký tự nào trong allowed-special set.
3. Ghi HTTP status/response.
4. Gửi `POST /api/login` với cùng synthetic credentials.
5. Hủy isolated database sau khi chụp evidence.

### Expected result

- Registration trả 4xx và không tạo account.
- Login bằng rejected credentials thất bại.

### Actual result

- Registration trả HTTP `200` với `User registered successfully`.
- Account vừa tạo login được, HTTP `200`.
- Frontend regex control matrix vẫn đúng: 13/13 EP/BVA checks pass, bao gồm minimum 8, length 7, đủ bảy allowed special characters và unsupported `#`.

### Evidence and attribution

- Independent reproduction: `FAIL_DEFECT_REPRODUCED`, 1/1 isolated API run ngày 2026-08-02.
- Machine-readable result: `evidence/github-issue-reproduction/result.json`.
- Safe screenshot: `evidence/github-issue-reproduction/BUG-REG-PASSWORD-POLICY-01-safe-reproduction.png`; SHA-256 `5c1e6d718f39f20dff7c5263c505a3789d96f6ddf196fae6167e8ce4f85d0537`.
- Test case: `../tests/test-cases/register/TC-REGISTER-001.md`.
- Participant IDs/frequency: `NONE` / `N/A`; không cộng vào P01–P07 metrics.
- P04/P06 chỉ support `UF-REG-PASSWORD-RECOVERY-01`; masked input không đủ để gán defect này cho họ.

### Impact and severity

- Task 2 severity: `S2` provisional vì client validation có thể bị bypass và weak account được tạo/đăng nhập; cần owner/security review.
- Canonical issue #118 mô tả defect rộng hơn (thiếu từng password class) và ghi Critical/P0; Task 2 không tự thay đổi severity/priority của issue đó.
- Root cause evidence: `frontend-web/src/pages/Register.jsx` có client regex đúng, trong khi handler `backend/server.js` insert trực tiếp mà không validate FR-01.

### Duplicate and publication disposition

- Duplicate search: COMPLETE ngày 2026-08-02. GitHub Search API tìm thấy canonical existing issue #118 với cùng missing-special-character API bypass.
- Publication action: REUSED EXISTING ISSUE — https://github.com/trngnneee/eshop-sut/issues/118; không tạo duplicate.
- Fresh Task 2 screenshot/comment: `NOT_PUBLISHED`; cần human privacy review và explicit external action trước khi đăng.

### Recommended fix and retest

Validate toàn bộ FR-01 ở backend trước khi insert, dùng một shared policy definition với frontend, trả 4xx cụ thể và bảo đảm rejected credentials không login được. Retest các partition thiếu uppercase/lowercase/digit/allowed-special, boundary length 7/8/9, từng ký tự `@ $ ! % * ? &`, và unsupported-only `#`.

## Non-bug dispositions

| Observation | Disposition | Reason |
|---|---|---|
| `Username`/`Đăng Ký` copy ở login | `USABILITY_ISSUE` với observed impact ở P07; chưa khẳng định software spec defect | Một participant login sai rồi tự recovery; các participant khác không có cùng observable error. |
| P04 browser password-manager detour | Isolated usability observation | Chỉ 2 giây và tự recovery; chưa có reproducible SUT defect. |
| Logout route vẫn ở protected profile nhưng hiển thị login-required | Behavioral SC5 PASS ở P01/P04; không đủ bằng chứng token/storage | Không nâng thành bug khi chưa có auth-state reproduction. |
| P05 system password prompt | `NOT_OBSERVABLE_AFTER_HUMAN_REVIEW` | Recording không đủ bằng chứng để xác định prompt tự bật hay participant chủ động mở. |
| P06 repeated weak-password recovery | `USABILITY_ISSUE`, không phải software bug | Password được masked nên không thể xác minh input có đáp ứng policy; task kết thúc mà registration chưa thành công. |

## Publication checklist

- [x] Participant evidence và frequency tách theo distinct participant.
- [x] Không chép raw password/PII vào report/draft.
- [x] Human-review timestamps/coding — student confirmed 2026-08-02.
- [x] Fresh independent reproduction bằng test-only data.
- [x] Privacy-safe synthetic screenshots tạo và integrity hash được ghi.
- [x] Existing GitHub issues searched; canonical duplicates #55, #37 và #118 được linked.
- [x] Requirement và Task 2 severity reviewed; product-owner/security adjudication của canonical issues vẫn là external responsibility.
- [x] Student phê duyệt local bug records/drafts ngày 2026-08-02.
- [x] Real existing issue URLs được cập nhật; published evidence-comment URLs chỉ có cho #55 và #37; không tạo duplicate.
- [x] Human-review #118 mapping/evidence hoàn tất; disposition hiện tại là local-only và không claim đã publish fresh comment.

Không tạo issue mới vì cả ba defect đều đã có issue thật. Fresh evidence của #55/#37 được host trên branch `task2-github-issue-evidence` tại commit `d9bc4c0` và đăng vào comments `5149476574`/`5149476796` ngày 2026-08-01. Evidence mới của #118 vẫn chỉ ở local package và không được trình bày như đã publish.
