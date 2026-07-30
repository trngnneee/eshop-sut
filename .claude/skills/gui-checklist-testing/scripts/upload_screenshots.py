#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload screenshot lên Cloudinary rồi nhúng URL vào issues/*.md và bug-report.md,
để ảnh render được trên GitHub Issues (GitHub không hiển thị ảnh từ đường dẫn local).

Chỉ dùng thư viện chuẩn (urllib) — không cần pip install. Signed upload (SHA-1).
Idempotent: URL đã upload lưu ở <base>/scripts/cloudinary-url-map.json, chạy lại an toàn.

CÁCH DÙNG
  1) Lấy Cloud name / API Key / API Secret trong Cloudinary Dashboard.
  2) export CLOUDINARY_URL="cloudinary://<API_KEY>:<API_SECRET>@<CLOUD_NAME>"
     (hoặc CLOUDINARY_CLOUD_NAME / CLOUDINARY_API_KEY / CLOUDINARY_API_SECRET)
  3) python3 upload_screenshots.py --base tests/gui_and_usability_testing --dry-run
     python3 upload_screenshots.py --base tests/gui_and_usability_testing

Script tìm token dạng `GUI-IA02-04.png` (trong backtick) và thay bằng ![ID](url).
Đặt tên ảnh TRÙNG checklist ID thì mọi thứ tự khớp.

Tuỳ chọn: --prefix để đổi tiền tố ID (mặc định GUI-), --folder để đổi thư mục Cloudinary.
"""
import argparse
import hashlib
import json
import mimetypes
import os
import re
import ssl
import sys
import time
import urllib.request


def make_ssl_context(insecure: bool):
    """macOS Python hay thiếu CA bundle: certifi -> mặc định -> (nếu cho phép) bỏ verify."""
    if insecure:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        print("[!] --insecure: BỎ QUA xác minh SSL (chỉ nên dùng tạm).")
        return ctx
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


def get_creds():
    url = os.environ.get("CLOUDINARY_URL")
    if url:
        m = re.match(r"cloudinary://([^:]+):([^@]+)@(.+)", url.strip())
        if not m:
            sys.exit("CLOUDINARY_URL sai định dạng. Đúng: cloudinary://KEY:SECRET@CLOUD_NAME")
        return m.group(3), m.group(1), m.group(2)
    cn = os.environ.get("CLOUDINARY_CLOUD_NAME")
    ak = os.environ.get("CLOUDINARY_API_KEY")
    asec = os.environ.get("CLOUDINARY_API_SECRET")
    if cn and ak and asec:
        return cn, ak, asec
    sys.exit("Thiếu credential. Set CLOUDINARY_URL hoặc 3 biến rời. "
             "(--dry-run chạy được mà không cần key.)")


def sign(params: dict, api_secret: str) -> str:
    items = sorted((k, v) for k, v in params.items() if v not in (None, ""))
    to_sign = "&".join(f"{k}={v}" for k, v in items)
    return hashlib.sha1((to_sign + api_secret).encode("utf-8")).hexdigest()


def upload(path, public_id, folder, cloud_name, api_key, api_secret, ssl_ctx):
    ts = str(int(time.time()))
    params = {"public_id": public_id, "folder": folder, "overwrite": "true", "timestamp": ts}
    fields = dict(params, api_key=api_key, signature=sign(params, api_secret))

    boundary = "----hw-boundary" + ts
    body = b""
    for k, v in fields.items():
        body += (f"--{boundary}\r\nContent-Disposition: form-data; "
                 f"name=\"{k}\"\r\n\r\n{v}\r\n").encode("utf-8")
    ctype = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        filedata = f.read()
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
             f"filename=\"{os.path.basename(path)}\"\r\nContent-Type: {ctype}\r\n\r\n").encode("utf-8")
    body += filedata + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        f"https://api.cloudinary.com/v1_1/{cloud_name}/image/upload", data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=60, context=ssl_ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))["secure_url"]


def embed(url_map, issues_dir, bug_report, prefix, dry):
    """Thay token `<PREFIX>...png` trong issues/*.md và bug-report.md bằng ảnh nhúng."""
    pat = re.compile(r"`(" + re.escape(prefix) + r"[A-Za-z0-9-]+\.(?:png|jpg|jpeg|gif))`")

    def repl(text):
        return pat.sub(lambda m: (f"![{os.path.splitext(m.group(1))[0]}]({url_map[m.group(1)]})"
                                  if m.group(1) in url_map else m.group(0)), text)

    targets = []
    if os.path.isdir(issues_dir):
        targets += [os.path.join(issues_dir, f) for f in sorted(os.listdir(issues_dir))
                    if f.endswith(".md")]
    if os.path.exists(bug_report):
        targets.append(bug_report)

    changed = 0
    for t in targets:
        txt = open(t, encoding="utf-8").read()
        new = repl(txt)
        if new != txt:
            if not dry:
                open(t, "w", encoding="utf-8").write(new)
            changed += 1
    return changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="thư mục output của GUI checklist")
    ap.add_argument("--folder", default="gui-checklist", help="thư mục trên Cloudinary")
    ap.add_argument("--prefix", default="GUI-", help="tiền tố ID/tên file ảnh")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="upload lại kể cả ảnh đã có URL")
    ap.add_argument("--insecure", action="store_true")
    a = ap.parse_args()

    base = os.path.abspath(a.base)
    shots_dir = os.path.join(base, "test-cases", "screenshots")
    issues_dir = os.path.join(base, "issues")
    bug_report = os.path.join(base, "bug-report.md")
    url_map_path = os.path.join(base, "scripts", "cloudinary-url-map.json")

    if not os.path.isdir(shots_dir):
        sys.exit(f"Không thấy thư mục screenshots: {shots_dir}")
    shots = sorted(f for f in os.listdir(shots_dir)
                   if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif")))
    print(f"Tìm thấy {len(shots)} screenshot trong {shots_dir}")

    url_map = json.load(open(url_map_path, encoding="utf-8")) if os.path.exists(url_map_path) else {}

    if a.dry_run:
        todo = [s for s in shots if a.force or s not in url_map]
        print(f"[DRY-RUN] Sẽ upload {len(todo)} ảnh, bỏ qua {len(shots) - len(todo)} ảnh đã có URL.")
        for s in todo[:5]:
            print("  upload ->", s)
        if len(todo) > 5:
            print(f"  ... (+{len(todo) - 5} nữa)")
        n = embed(url_map, issues_dir, bug_report, a.prefix, dry=True)
        print(f"[DRY-RUN] Sẽ cập nhật {n} file markdown (dựa trên URL đang có trong cache).")
        return 0

    cloud_name, api_key, api_secret = get_creds()
    ssl_ctx = make_ssl_context(a.insecure)
    print(f"Cloudinary cloud: {cloud_name} | folder: {a.folder}")
    os.makedirs(os.path.dirname(url_map_path), exist_ok=True)

    ok = skip = bad = 0
    for s in shots:
        if s in url_map and not a.force:
            skip += 1
            continue
        try:
            secure = upload(os.path.join(shots_dir, s), os.path.splitext(s)[0], a.folder,
                            cloud_name, api_key, api_secret, ssl_ctx)
            url_map[s] = secure
            ok += 1
            print(f"  ✓ {s} -> {secure}")
            json.dump(url_map, open(url_map_path, "w", encoding="utf-8"),
                      indent=2, ensure_ascii=False)  # lưu ngay từng ảnh
        except Exception as e:
            bad += 1
            print(f"  ✗ {s} : {e}")

    json.dump(url_map, open(url_map_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Upload xong: {ok} mới, {skip} bỏ qua, {bad} lỗi.")
    print(f"Đã nhúng URL vào {embed(url_map, issues_dir, bug_report, a.prefix, dry=False)} file markdown.")
    print(f"URL map: {url_map_path}")
    print("\nBước tiếp — đăng issue:")
    print(f"  for f in {a.base}/issues/BUG-*.md; do")
    print("    gh issue create --repo <owner/repo> --title \"$(sed -n '2p' \"$f\")\" \\")
    print("      --body-file \"$f\" --label bug,ui ; done")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
