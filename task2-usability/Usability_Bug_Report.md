# Usability Evaluation — Software Bug Report

**Current status:** `PARTICIPANT_EVIDENCE_RECORDED — HUMAN_REVIEW_AND_INDEPENDENT_REPRODUCTION_PENDING`
**GitHub policy for this deliverable:** Chỉ chuẩn bị local drafts; không tạo/đăng GitHub Issue.
**Privacy:** Không chép password hoặc raw name/email/phone/address.

## Bug summary

| Bug ID | Requirement/baseline | Participants | Frequency | Independent reproduction | Severity provisional | Draft | Published URL |
|---|---|---|---:|---|---:|---|---|
| BUG-PF-02 | FR-04: phone bắt đầu bằng 0 và gồm 10–11 chữ số | P01, P02, P04 | 3/7 | REQUIRED — fresh retest pending; prior preflight exists | S1 | `github-issues/DRAFT-BUG-USABILITY-01.md` | NOT_CREATED |
| BUG-AUTH-PLAINTEXT-01 | Password control phải che credential mặc định | P01, P02, P04, P05, P07 | 5/7 | REQUIRED — pending | S2 | `github-issues/DRAFT-BUG-AUTH-PLAINTEXT-01.md` | NOT_CREATED |

P06 không được tính cho BUG-AUTH-PLAINTEXT-01 vì replacement recording không tới login; frequency vẫn là 5/7.

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
- Status: PENDING fresh reproduction after participant analysis.
- Prior technical preflight exists at `evidence/technical-preflight/`, nhưng không được tính như participant evidence hoặc thay publication review.

### Evidence/redaction

- Screenshot/clip candidates: các timestamps ở trên.
- Redact toàn bộ name, email, phone, address và password trước khi attach.
- Không có redacted participant clip được xuất trong deliverable hiện tại.

### Potential duplicate

- Duplicate search: NOT_PERFORMED/UNVERIFIED trong external GitHub state.
- Publication action: DRAFT ONLY; reviewer phải search existing issues trước khi đăng.

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
- Status: PENDING với test-only credential và supported-browser matrix.

### Evidence/redaction

- Screenshot/clip candidates: timestamps ở trên.
- Trước khi attach, phải che toàn bộ password và adjacent PII; clip chỉ cần chứng minh field không mask, không được để readable value.
- Không có redacted participant clip được xuất trong deliverable hiện tại.

### Potential duplicate

- Local preflight tài liệu có nhắc một Task 1 candidate `BUG-GUI-01`, nhưng external issue existence/URL chưa được xác minh.
- Duplicate disposition: UNVERIFIED; search/reuse existing issue nếu có, không mở duplicate.

## Non-bug dispositions

| Observation | Disposition | Reason |
|---|---|---|
| `Username`/`Đăng Ký` copy ở login | `USABILITY_ISSUE` với observed impact ở P07; chưa khẳng định software spec defect | Một participant login sai rồi tự recovery; các participant khác không có cùng observable error. |
| P04 browser password-manager detour | Isolated usability observation | Chỉ 2 giây và tự recovery; chưa có reproducible SUT defect. |
| Logout route vẫn ở protected profile nhưng hiển thị login-required | Behavioral SC5 PASS ở P01/P04; không đủ bằng chứng token/storage | Không nâng thành bug khi chưa có auth-state reproduction. |
| P05 system password prompt | UNVERIFIED | Không đủ bằng chứng prompt tự bật hay participant chủ động mở. |
| P06 repeated weak-password recovery | `USABILITY_ISSUE`, không phải software bug | Password được masked nên không thể xác minh input có đáp ứng policy; task kết thúc mà registration chưa thành công. |

## Publication checklist

- [x] Participant evidence và frequency tách theo distinct participant.
- [x] Không chép raw password/PII vào report/draft.
- [ ] Human-review timestamps.
- [ ] Fresh independent reproduction bằng test-only data.
- [ ] Redacted screenshot/clip tạo và reviewer kiểm tra.
- [ ] Existing GitHub issues searched.
- [ ] Requirement/owner/severity confirmed.
- [ ] Reviewer phê duyệt draft.
- [ ] Issue được đăng và URL cập nhật vào bug report, findings, summary và evidence index.

Không GitHub issue nào đã được tạo trong lần phân tích này.
