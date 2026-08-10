# Video script — Agent Skill demo (FR-15 end-to-end)

**Purpose:** YouTube link showing **end-to-end** use of your Agent Skill on **one complete feature**  
**Feature:** Feature C — FR-15 Product CRUD (Admin)  
**Skill file:** `.cursor/skills/automation-testing/playwright-skill.md`  
**Student ID:** `23127271`  
**Suggested length:** 5–8 minutes (can be shorter than Task 2 if clear; still narrate in Vietnamese)

This video is **different** from Task 2:
- Task 2 = run scripts + report + AI fix
- Skill video = show **how Cursor + Skill** drove Analyze → Design → Data → Generate → Verify for FR-15

---

## Before you hit Record

1. Open Cursor on the homework workspace.
2. Have the skill file ready to show.
3. Prefer a **fresh / replayable** FR-15 chat (or scroll an existing chat) that clearly hits skill stages.
4. Authorship: face-cam **or** start with `whoami` / `hostname` (safe even if PDF focuses this on Task 2).
5. SUT can be running if you show a verify step at the end.

---

## Scene 0 — Intro + authorship (0:00–0:35)

**On screen:** terminal or face-cam

```powershell
whoami
hostname
```

**Say (VN):**
> Xin chào, mình là **23127271**. Video này demo **Agent Skill** dùng cho HW04: skill hướng dẫn quy trình tạo Playwright data-driven, multi-browser. Mình sẽ chiếu cách dùng skill trên **một feature hoàn chỉnh — FR-15 Product CRUD Admin**.

---

## Scene 1 — Show the Skill artifact (0:35–1:20)

**On screen:** open

`c:\DiskD\HCMUS\Semester9\SoftwareTesting\.cursor\skills\automation-testing\playwright-skill.md`

Scroll description + main sections:
- 3 features / ≥12 cases
- step-by-step AI stages
- external JSON/CSV
- ≥3 assertion patterns
- 3-browser matrix + labeled HTML reports

**Say (VN):**
> Đây là file skill mình submit. Phần `description` giúp Cursor tự kích hoạt khi mình nhờ làm bài automation Playwright. Skill không chỉ “viết test”, mà ép quy trình: phân tích → thiết kế ≥12 case → data ngoài → generate → verify & repair, và không được làm mềm oracle để test luôn xanh.

---

## Scene 2 — Kickoff only (1:20–1:50)

**Không** liệt kê hết Analyze→Verify trong **một** prompt. HW04 + skill yêu cầu **step-by-step**: mỗi stage = **một prompt riêng** (hoặc turn riêng), đọc output rồi mới sang stage sau.

**Sai (đừng quay / đừng dùng):**
```text
Dùng skill... Làm đủ Analyze, Design, Review, Model data, Generate, Verify...
```
→ Đây vẫn là “one-shot”, chỉ đổi wording; dễ bị trừ phần step-by-step AI.

**Đúng — Prompt 0 (chỉ mở việc):**
```text
Dùng skill automation-testing / build-playwright-assignment.
Bắt đầu Feature C — FR-15 Product CRUD (Admin), Student ID 23127271.
Chỉ làm stage Analyze thôi. Chưa design case, chưa viết code.
Giữ nguyên evidence FR-03/FR-08.
```

**Say (VN):**
> Mình **không** nhờ AI làm hết trong một câu. Skill bắt làm từng bước: xong Analyze mới Design, xong Design mới Review… Mỗi lần gửi một stage.

---

## Scene 3 — Từng prompt / từng stage (1:50–5:20)

Quay chat thật: gửi prompt → chờ output → gửi prompt tiếp. Mỗi block ~25–40s.

### 3.1 Analyze — Prompt 1
```text
Stage Analyze FR-15: trích actor, precondition, CRUD, rule Tên/Giá/Danh mục,
lớp hợp lệ-không hợp lệ. Chỉ phân tích, chưa đề xuất danh sách 12 case.
```
**Show:** output rules · **Say:** ngắn gọn đúng nội dung Analyze.

### 3.2 Design — Prompt 2
```text
Stage Design: dựa trên Analyze vừa rồi, đề xuất ≥12 case ID phân biệt
(positive CRUD + negative/boundary). Chưa viết JSON, chưa viết Playwright.
```
**Show:** bảng/list case IDs · **Say:** đủ ≥12, không đếm theo browser.

### 3.3 Review — Prompt 3
```text
Stage Review: kiểm tra list case — bỏ trùng nghĩa, map oracle quan sát được,
ghi case nào có thể fail vì defect SUT. Chưa generate code.
```
**Show:** chỉnh sửa list / ghi chú oracle.

### 3.4 Model data — Prompt 4
```text
Stage Model data: tạo test-data/fr15-admin-product.json từ case đã review.
Chỉ data primitives; không nhét selector/secret vào JSON.
```
**Show:** file JSON.

### 3.5 Map automation — Prompt 5
```text
Stage Map automation: chọn locator, setup/cleanup admin, action/expect vocabulary.
Chưa generate full spec nếu skill tách riêng; hoặc nói rõ map xong rồi Generate.
```

### 3.6 Generate — Prompt 6
```text
Stage Generate: implement pages + tests/fr15-admin-product.spec.js data-driven
từ JSON. Giữ oracle; không làm mềm assertion cho xanh giả.
```
**Show:** `.spec.js` + page object.

### 3.7 Verify & repair — Prompt 7 (+ turn sửa)
```text
Stage Verify: chạy FR-15 (ít nhất chromium trước), liệt kê fail thật,
đề xuất sửa có chủ đích — không đổi expected cho khớp UI lỗi.
```
Rồi **Prompt 8** (nếu cần): `Sửa đúng lỗi X trong spec/page object như đã bàn.`

**Say (VN):**
> Đây mới là step-by-step: mình review từng output rồi mới cho stage sau. Ví dụ lúc Verify mình bắt AI sửa **[điền fix thật]** thay vì chấp nhận output one-shot.

---

## Scene 4 — Prove the feature is “complete” (5:00–6:20)

**On screen:**

1. Ledger / README summary: FR-15 ≥12 cases, 3 browsers, reports labeled.
2. Open one HTML report cell:

`reports/html/fr15-admin-product/chromium/index.html`

Show `Run by: 23127271` + timestamp.

Optional quick terminal:

```powershell
npx playwright test tests/fr15-admin-product.spec.js --list
```

**Say (VN):**
> Theo skill, một feature chỉ “xong” khi đủ ≥12 case **và** đã chạy 3 browser với HTML report có Student ID. FR-15 đã đủ các artifact đó. Skill này mình có thể tái dùng cho feature khác trong bài testing sau.

---

## Scene 5 — Close (6:20–6:50)

**Say (VN):**
> Video kết thúc phần demo Agent Skill trên feature FR-15. Skill nằm tại `.cursor/skills/automation-testing/playwright-skill.md`. Sinh viên **23127271**. Cảm ơn thầy/cô đã xem.

**Uploaded (Unlisted):** https://youtu.be/Te25xh0biYI  
Link also in `23127271/README.md` under Agent Skill.

---

## Checklist before upload

- [ ] Skill file shown on screen
- [ ] Clear that skill was **used** (not only that file exists)
- [ ] **Separate prompts per stage** (not one mega-prompt listing all stages)
- [ ] FR-15 as the **complete** feature walkthrough
- [ ] Stages visible: analyze → design → data → generate → verify
- [ ] Final artifacts visible (JSON + spec + at least one labeled report)
- [ ] Your voice narration (Vietnamese recommended)
- [ ] Authorship hint (`whoami`/`hostname` or face-cam)

---

## Difference vs Task 2 demo (avoid filming twice the same way)

| | Task 2 demo | Agent Skill demo |
| --- | --- | --- |
| Focus | Execution + report + 1 AI fix | Skill-driven workflow on one feature |
| Must show | Multi-browser run | Skill file + stage-by-stage use |
| Feature | FR-15 OK | FR-15 OK (same feature fine) |
| Length | ≥ 5 min required | Enough to prove end-to-end skill use |
