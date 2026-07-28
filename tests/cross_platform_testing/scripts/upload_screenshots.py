#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload proof screenshot của Task 3 (cross-platform) lên Cloudinary, lấy secure URL,
rồi nhúng vào issues/XP-*.md (và cross-platform-report.md / divergences.md nếu có
token ảnh) để ảnh render được trên GitHub Issues.

Khác với script Task 2: ảnh nằm rải ở results/<platform>/{screenshots,platform-proof}/
và TRÙNG TÊN giữa các platform (GUI-IA02-14.png có ở cả P2 lẫn P3). Vì vậy:
  - key của url map là ĐƯỜNG DẪN TƯƠNG ĐỐI ("results/P2-firefox-macos/screenshots/x.png")
  - public_id trên Cloudinary là "<platform>__<subdir>__<name>" để không ghi đè nhau.

Chỉ dùng thư viện chuẩn của Python (urllib) — KHÔNG cần pip install gì thêm.

------------------------------------------------------------------------------
CÁCH DÙNG
------------------------------------------------------------------------------
  export CLOUDINARY_URL="cloudinary://<API_KEY>:<API_SECRET>@dnqinxiwo"
  python3 upload_screenshots.py --dry-run   # xem sẽ upload/sửa gì, không cần key
  python3 upload_screenshots.py             # upload + nhúng URL vào issues/XP-*.md
  python3 upload_screenshots.py --force     # upload lại kể cả ảnh đã có URL
  python3 upload_screenshots.py --only-referenced   # chỉ upload ảnh được issue tham chiếu

Idempotent: URL lưu ở scripts/cloudinary-url-map.json, chạy lại an toàn.
------------------------------------------------------------------------------
"""
import os, sys, json, time, hashlib, mimetypes, urllib.request, re, ssl

HERE = os.path.dirname(os.path.abspath(__file__))          # .../cross_platform_testing/scripts
ROOT = os.path.dirname(HERE)                               # .../cross_platform_testing
RESULTS_DIR = os.path.join(ROOT, "results")
ISSUES_DIR = os.path.join(ROOT, "issues")
EXTRA_TARGETS = ["cross-platform-report.md", "divergences.md",
                 "results-matrix.md", "platform-matrix.md"]
URL_MAP = os.path.join(HERE, "cloudinary-url-map.json")
CLOUD_FOLDER = "eshop-hw03/cross-platform"

DRY = "--dry-run" in sys.argv
FORCE = "--force" in sys.argv
INSECURE = "--insecure" in sys.argv
ONLY_REF = "--only-referenced" in sys.argv

# token ảnh trong markdown: `results/<platform>/<subdir>/<file>.png`
REF_RE = re.compile(r"`(results/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+\.png)`")


def make_ssl_context():
    """macOS Python hay thiếu CA bundle: ưu tiên certifi -> mặc định -> --insecure."""
    if INSECURE:
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


SSL_CTX = make_ssl_context()


def get_creds():
    url = os.environ.get("CLOUDINARY_URL")
    if url:
        m = re.match(r"cloudinary://([^:]+):([^@]+)@(.+)", url.strip())
        if not m:
            sys.exit("CLOUDINARY_URL sai định dạng. Đúng: cloudinary://KEY:SECRET@CLOUD_NAME")
        return m.group(3), m.group(1), m.group(2)
    cn = os.environ.get("CLOUDINARY_CLOUD_NAME")
    ak = os.environ.get("CLOUDINARY_API_KEY")
    ase = os.environ.get("CLOUDINARY_API_SECRET")
    if cn and ak and ase:
        return cn, ak, ase
    sys.exit("Thiếu credential. Set CLOUDINARY_URL hoặc CLOUDINARY_CLOUD_NAME/API_KEY/"
             "API_SECRET. (Có thể chạy --dry-run mà không cần key.)")


def sign(params, api_secret):
    items = sorted((k, v) for k, v in params.items() if v not in (None, ""))
    to_sign = "&".join("%s=%s" % (k, v) for k, v in items)
    return hashlib.sha1((to_sign + api_secret).encode("utf-8")).hexdigest()


def upload(path, public_id, cloud_name, api_key, api_secret):
    ts = str(int(time.time()))
    params = {"public_id": public_id, "folder": CLOUD_FOLDER,
              "overwrite": "true", "timestamp": ts}
    fields = dict(params, api_key=api_key, signature=sign(params, api_secret))

    boundary = "----hw03xpboundary" + ts
    body = b""
    for k, v in fields.items():
        body += ("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n"
                 % (boundary, k, v)).encode("utf-8")
    ctype = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        filedata = f.read()
    body += ("--%s\r\nContent-Disposition: form-data; name=\"file\"; filename=\"%s\"\r\n"
             "Content-Type: %s\r\n\r\n" % (boundary, os.path.basename(path), ctype)).encode("utf-8")
    body += filedata + ("\r\n--%s--\r\n" % boundary).encode("utf-8")

    url = "https://api.cloudinary.com/v1_1/%s/image/upload" % cloud_name
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "multipart/form-data; boundary=%s" % boundary})
    with urllib.request.urlopen(req, timeout=90, context=SSL_CTX) as resp:
        return json.loads(resp.read().decode("utf-8"))["secure_url"]


def md_targets():
    targets = []
    if os.path.isdir(ISSUES_DIR):
        targets += sorted(os.path.join(ISSUES_DIR, f)
                          for f in os.listdir(ISSUES_DIR) if f.endswith(".md"))
    for name in EXTRA_TARGETS:
        p = os.path.join(ROOT, name)
        if os.path.exists(p):
            targets.append(p)
    return targets


def referenced_paths():
    """Tập đường dẫn ảnh đang được markdown tham chiếu (kể cả đã nhúng dạng ![](...))."""
    refs = set()
    for t in md_targets():
        refs.update(REF_RE.findall(open(t, encoding="utf-8").read()))
    return refs


def discover():
    """Trả về list (relpath, abspath, public_id) cho mọi .png dưới results/."""
    out = []
    for dirpath, _dirnames, filenames in os.walk(RESULTS_DIR):
        for fn in sorted(filenames):
            if not fn.lower().endswith(".png"):
                continue
            ab = os.path.join(dirpath, fn)
            rel = os.path.relpath(ab, ROOT).replace(os.sep, "/")
            # results/P2-firefox-macos/screenshots/GUI-IA02-14.png
            #   -> P2-firefox-macos__screenshots__GUI-IA02-14
            parts = rel.split("/")[1:]
            pid = "__".join(parts)[:-4]
            out.append((rel, ab, pid))
    return out


def embed_into_markdown(url_map):
    """Thay token `results/.../x.png` bằng ảnh nhúng ![tên](url)."""
    def sub(m):
        rel = m.group(1)
        u = url_map.get(rel)
        if not u:
            return m.group(0)                       # chưa có URL → giữ nguyên
        label = os.path.basename(rel)[:-4]
        platform = rel.split("/")[1]
        return "![%s @ %s](%s)" % (label, platform, u)

    changed = []
    for t in md_targets():
        txt = open(t, encoding="utf-8").read()
        new = REF_RE.sub(sub, txt)
        if new != txt:
            if not DRY:
                open(t, "w", encoding="utf-8").write(new)
            changed.append(os.path.relpath(t, ROOT))
    return changed


def main():
    if not os.path.isdir(RESULTS_DIR):
        sys.exit("Không thấy thư mục results: %s" % RESULTS_DIR)

    shots = discover()
    refs = referenced_paths()
    if ONLY_REF:
        shots = [s for s in shots if s[0] in refs]
    print("Tìm thấy %d ảnh dưới results/ (%d ảnh đang được markdown tham chiếu)%s"
          % (len(discover()), len(refs), " — lọc --only-referenced" if ONLY_REF else ""))

    missing = sorted(r for r in refs if not os.path.exists(os.path.join(ROOT, r)))
    if missing:
        print("[!] %d đường dẫn trong markdown KHÔNG tồn tại trên đĩa:" % len(missing))
        for r in missing:
            print("    -", r)

    url_map = json.load(open(URL_MAP)) if os.path.exists(URL_MAP) else {}

    if DRY:
        todo = [s for s in shots if FORCE or s[0] not in url_map]
        print("[DRY-RUN] Sẽ upload %d ảnh, bỏ qua %d ảnh đã có URL."
              % (len(todo), len(shots) - len(todo)))
        for rel, _ab, pid in todo[:8]:
            print("  upload -> %s  (public_id=%s)" % (rel, pid))
        if len(todo) > 8:
            print("  ... (+%d nữa)" % (len(todo) - 8))
        print("[DRY-RUN] Sẽ cập nhật: %s" % (", ".join(embed_into_markdown(url_map)) or "(chưa file nào)"))
        return

    cloud_name, api_key, api_secret = get_creds()
    print("Cloudinary cloud: %s | folder: %s" % (cloud_name, CLOUD_FOLDER))

    ok, skip, fail = 0, 0, 0
    for rel, ab, pid in shots:
        if rel in url_map and not FORCE:
            skip += 1
            continue
        try:
            url_map[rel] = upload(ab, pid, cloud_name, api_key, api_secret)
            ok += 1
            print("  ✓ %s -> %s" % (rel, url_map[rel]))
            json.dump(url_map, open(URL_MAP, "w"), indent=2, ensure_ascii=False)
        except Exception as e:
            fail += 1
            print("  ✗ %s : %s" % (rel, e))

    json.dump(url_map, open(URL_MAP, "w"), indent=2, ensure_ascii=False)
    print("Upload xong: %d mới, %d bỏ qua (đã có), %d lỗi." % (ok, skip, fail))

    changed = embed_into_markdown(url_map)
    print("Đã nhúng URL vào %d file: %s" % (len(changed), ", ".join(changed)))
    print("URL map lưu tại: %s" % URL_MAP)


if __name__ == "__main__":
    main()
