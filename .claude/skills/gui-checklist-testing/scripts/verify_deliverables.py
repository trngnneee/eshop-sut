#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cổng kiểm tra deliverable của GUI checklist trước khi commit.

Chỉ dùng thư viện chuẩn. Chạy:

    python3 verify_deliverables.py --dir tests/gui_and_usability_testing
    python3 verify_deliverables.py --dir <dir> --gh owner/repo      # + kiểm issue trên GitHub (cần gh CLI)
    python3 verify_deliverables.py --dir <dir> --min-items 40 --critique-range 200 300

Exit code 0 = sạch, 1 = có FAIL. WARN không làm fail.

Kiểm:
  1. Bảng markdown lệch số cột (header vs separator) — lỗi này làm GitHub/pandoc bỏ nhận bảng.
  2. checklist-final.md: tổng item, mọi item có status Passed/Failed, tổng > --min-items.
  3. Screenshot: song ánh với item Failed; item Passed không có ảnh; không có ảnh mồ côi.
  4. Test case: 1:1 với item trong checklist.
  5. Traceability: mọi item Failed được ít nhất một bug trong bug-report.md phủ.
  6. Mọi item GUI-GAP có dòng ở Phần B gap-analysis kèm lý do AI bỏ sót.
  7. AI Critique trong report.md nằm trong khoảng từ cho phép.
  8. (--gh) mọi issue URL trong issue-map.tsv tồn tại và thân issue có ảnh nhúng.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys

PIPE = re.compile(r"(?<!\\)\|")
SEP_ROW = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
ITEM_ID = re.compile(r"GUI-(?:IA\d{2}|GAP)-\d{2}")

fails: list[str] = []
warns: list[str] = []
notes: list[str] = []


def fail(msg: str) -> None:
    fails.append(msg)


def warn(msg: str) -> None:
    warns.append(msg)


def note(msg: str) -> None:
    notes.append(msg)


def cells(line: str) -> int:
    """Số ô của một dòng bảng markdown."""
    parts = PIPE.split(line.strip())
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return len(parts)


# ---------------------------------------------------------------- 1. bảng md
def check_tables(root: str) -> None:
    bad = 0
    for path in sorted(glob.glob(os.path.join(root, "**", "*.md"), recursive=True)):
        lines = open(path, encoding="utf-8").read().split("\n")
        in_fence = False
        for i, line in enumerate(lines):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence or not SEP_ROW.match(line):
                continue
            if i == 0 or not lines[i - 1].strip().startswith("|"):
                continue
            head, sep = cells(lines[i - 1]), cells(line)
            if head != sep:
                bad += 1
                rel = os.path.relpath(path, root)
                fail(f"[bảng lệch cột] {rel}:{i + 1} — header {head} ô, separator {sep} ô "
                     f"→ GitHub/pandoc sẽ KHÔNG render thành bảng")
    if not bad:
        note("Bảng markdown: mọi bảng có separator khớp số cột")


# ------------------------------------------------------- 2. checklist-final
def parse_checklist(path: str):
    """-> (failed set, passed set, thứ tự xuất hiện)"""
    failed, passed, order = set(), set(), []
    for line in open(path, encoding="utf-8"):
        if not line.startswith("| GUI-"):
            continue
        cols = [c.strip() for c in PIPE.split(line.strip())[1:-1]]
        if not cols:
            continue
        iid = cols[0]
        order.append(iid)
        blob = " ".join(cols[1:])
        has_f, has_p = "Failed" in blob, "Passed" in blob
        if has_f and has_p:
            fail(f"[status nhập nhằng] {iid} — dòng chứa cả Passed và Failed")
        elif has_f:
            failed.add(iid)
        elif has_p:
            passed.add(iid)
        else:
            fail(f"[thiếu status] {iid} — chưa đánh Passed/Failed")
    dupes = {i for i in order if order.count(i) > 1}
    if dupes:
        fail(f"[ID trùng trong checklist] {sorted(dupes)}")
    return failed, passed, order


# ------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="thư mục output của GUI checklist")
    ap.add_argument("--gh", help="owner/repo — kiểm issue trên GitHub (cần gh CLI)")
    ap.add_argument("--min-items", type=int, default=40)
    ap.add_argument("--critique-range", nargs=2, type=int, default=[200, 300])
    ap.add_argument("--json", action="store_true", help="in kết quả dạng JSON")
    a = ap.parse_args()

    root = os.path.abspath(a.dir)
    if not os.path.isdir(root):
        print(f"Không thấy thư mục: {root}", file=sys.stderr)
        return 2

    p = lambda *x: os.path.join(root, *x)  # noqa: E731

    check_tables(root)

    # 2 -------------------------------------------------------------------
    cl = p("checklist-final.md")
    failed, passed, order = set(), set(), []
    if not os.path.exists(cl):
        fail("[thiếu file] checklist-final.md")
    else:
        failed, passed, order = parse_checklist(cl)
        total = len(order)
        if total <= a.min_items:
            fail(f"[số item] {total} item — đề yêu cầu > {a.min_items}")
        else:
            note(f"Checklist: {total} item (> {a.min_items}) — {len(passed)} Passed / {len(failed)} Failed")
        aspects = {m.group(1) for i in order if (m := re.match(r"GUI-(IA\d{2}|GAP)-", i))}
        missing_ia = {f"IA{n:02d}" for n in range(1, 5)} - aspects
        if missing_ia:
            fail(f"[thiếu aspect] không có item nào cho {sorted(missing_ia)}")
        if "GAP" not in aspects:
            fail("[thiếu item tự thêm] không có ID GUI-GAP-xx — đề yêu cầu item do người bổ sung")

    all_items = failed | passed

    # 3 -------------------------------------------------------------------
    shots_dir = p("test-cases", "screenshots")
    if not os.path.isdir(shots_dir):
        fail("[thiếu thư mục] test-cases/screenshots/")
    elif all_items:
        shots = {os.path.splitext(f)[0] for f in os.listdir(shots_dir)
                 if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))}
        if miss := sorted(failed - shots):
            fail(f"[Failed thiếu screenshot] {miss}")
        if extra := sorted(passed & shots):
            fail(f"[Passed lại có screenshot] {extra} — đề yêu cầu ảnh CHỈ cho item Failed")
        if orphan := sorted(shots - all_items):
            warn(f"[ảnh mồ côi] {orphan} — không khớp ID nào trong checklist")
        if not miss and not extra:
            note(f"Screenshot: {len(failed)}/{len(failed)} item Failed có ảnh, 0 item Passed có ảnh")

    # 4 -------------------------------------------------------------------
    tc_files = glob.glob(p("test-cases", "IA-*", "*.md"))
    if not tc_files:
        warn("[không thấy test case] test-cases/IA-*/*.md — bỏ qua kiểm 1:1")
    elif all_items:
        tcs = {os.path.splitext(os.path.basename(f))[0] for f in tc_files}
        if miss := sorted(all_items - tcs):
            fail(f"[item không có file test case] {miss}")
        if extra := sorted(tcs - all_items):
            fail(f"[test case không có item tương ứng] {extra}")
        if not miss and not extra:
            note(f"Test case: {len(tcs)} file khớp 1:1 với checklist")

    # 5 -------------------------------------------------------------------
    br = p("bug-report.md")
    if not os.path.exists(br):
        fail("[thiếu file] bug-report.md")
    elif failed:
        text = open(br, encoding="utf-8").read()
        covered = set(ITEM_ID.findall(text))
        bugs = set(re.findall(r"\bBUG-\d{2}\b", text))
        if miss := sorted(failed - covered):
            fail(f"[item Failed chưa có bug] {miss}")
        else:
            note(f"Traceability: {len(failed)} item Failed đều được phủ bởi {len(bugs)} bug")
        if ghost := sorted(covered - all_items):
            warn(f"[bug trỏ tới ID không có trong checklist] {ghost}")

    # 6 -------------------------------------------------------------------
    gap_ids = {i for i in order if i.startswith("GUI-GAP-")}
    ga = p("checklist-draft", "gap-analysis.md")
    if gap_ids:
        if not os.path.exists(ga):
            fail("[thiếu file] checklist-draft/gap-analysis.md — không có chỗ giải thích AI bỏ sót")
        else:
            reasons = ("prompt", "mô hình", "model", "đặc thù", "SUT")
            body = open(ga, encoding="utf-8").read()
            rows = {}
            for line in body.split("\n"):
                if line.startswith("| GUI-GAP-"):
                    cols = [c.strip() for c in PIPE.split(line.strip())[1:-1]]
                    rows[cols[0]] = cols
            for gid in sorted(gap_ids):
                if gid not in rows:
                    fail(f"[{gid}] không có dòng trong gap-analysis.md Phần B")
                    continue
                blob = " ".join(rows[gid][1:])
                if not any(r.lower() in blob.lower() for r in reasons):
                    fail(f"[{gid}] chưa nêu lý do AI bỏ sót (prompt / giới hạn mô hình / đặc thù SUT)")
                elif len(blob) < 120:
                    warn(f"[{gid}] giải thích rất ngắn ({len(blob)} ký tự) — đề chấm nặng phần này")
            if not any(f.startswith("[GUI-GAP") for f in fails):
                note(f"Gap analysis: {len(gap_ids)} item tự thêm đều có lý do AI bỏ sót")

    # 7 -------------------------------------------------------------------
    rp = p("report.md")
    lo, hi = a.critique_range
    if not os.path.exists(rp):
        fail("[thiếu file] report.md")
    else:
        text = open(rp, encoding="utf-8").read()
        m = re.search(r"^#{1,6}[^\n]*AI Critique[^\n]*$", text, re.M)
        if not m:
            fail("[thiếu mục] report.md không có heading 'AI Critique'")
        else:
            after = text[m.end():]
            nxt = re.search(r"^#{1,6} ", after, re.M)
            body = after[:nxt.start()] if nxt else after
            n = len(re.findall(r"[\w'À-ỹ-]+", body))
            if lo <= n <= hi:
                note(f"AI Critique: {n} từ (trong khoảng {lo}–{hi})")
            else:
                fail(f"[AI Critique] {n} từ — đề yêu cầu {lo}–{hi}")

    # 8 -------------------------------------------------------------------
    imap = p("issue-map.tsv")
    if a.gh:
        if not os.path.exists(imap):
            fail("[thiếu file] issue-map.tsv — không kiểm được issue")
        else:
            nums = re.findall(r"/issues/(\d+)", open(imap, encoding="utf-8").read())
            if not nums:
                fail("[issue-map.tsv] không có issue URL nào")
            else:
                try:
                    out = subprocess.run(
                        ["gh", "issue", "list", "--repo", a.gh, "--limit", "500",
                         "--state", "all", "--json", "number,body"],
                        capture_output=True, text=True, timeout=120, check=True).stdout
                    live = {str(i["number"]): (i.get("body") or "") for i in json.loads(out)}
                except Exception as e:  # gh chưa login / offline
                    warn(f"[--gh] không gọi được gh CLI ({e}) — bỏ qua kiểm issue")
                    live = None
                if live is not None:
                    if miss := sorted(set(nums) - set(live), key=int):
                        fail(f"[issue không tồn tại trên {a.gh}] #{', #'.join(miss)}")
                    noimg = sorted((n for n in nums if n in live and "![" not in live[n]), key=int)
                    if noimg:
                        fail(f"[issue thiếu ảnh nhúng] #{', #'.join(noimg)} — đề yêu cầu mỗi issue có screenshot")
                    if not miss and not noimg:
                        note(f"GitHub: {len(set(nums))} issue tồn tại, tất cả có ảnh nhúng")
    elif os.path.exists(imap):
        note("issue-map.tsv có mặt (chạy lại với --gh owner/repo để kiểm issue thật)")

    # ---------------------------------------------------------------- output
    if a.json:
        print(json.dumps({"fails": fails, "warns": warns, "notes": notes}, ensure_ascii=False, indent=2))
    else:
        for m in notes:
            print(f"  ok   {m}")
        for m in warns:
            print(f"  WARN {m}")
        for m in fails:
            print(f"  FAIL {m}")
        print()
        print(f"{len(fails)} FAIL · {len(warns)} WARN · {len(notes)} ok")
        print("SẠCH — commit được." if not fails else "CÓ LỖI — sửa rồi chạy lại trước khi commit.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
