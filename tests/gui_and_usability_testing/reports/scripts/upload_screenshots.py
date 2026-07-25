#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload screenshot lên Cloudinary, lấy secure URL, rồi nhúng vào các file issue
(reports/issues/*.md) và reports/bug-report.md để ảnh render được trên GitHub Issues.

Chỉ dùng thư viện chuẩn của Python (urllib) — KHÔNG cần pip install gì thêm.
Ký request bằng thuật toán signed upload của Cloudinary (SHA-1).

------------------------------------------------------------------------------
CÁCH DÙNG
------------------------------------------------------------------------------
1. Lấy 3 giá trị trong Cloudinary Dashboard (Account Details):
     Cloud name, API Key, API Secret
2. Cấp credential theo 1 trong 2 cách:
   a) Biến môi trường CLOUDINARY_URL:
        export CLOUDINARY_URL="cloudinary://<API_KEY>:<API_SECRET>@<CLOUD_NAME>"
   b) Hoặc 3 biến rời:
        export CLOUDINARY_CLOUD_NAME="..."
        export CLOUDINARY_API_KEY="..."
        export CLOUDINARY_API_SECRET="..."
3. Chạy:
     python3 upload_screenshots.py            # upload + nhúng URL vào issue/bug-report
     python3 upload_screenshots.py --dry-run  # chỉ in việc sẽ làm, không upload/sửa file
     python3 upload_screenshots.py --force     # upload lại kể cả ảnh đã có URL trong cache

Idempotent: URL đã upload được lưu ở reports/scripts/cloudinary-url-map.json.
Chạy lại sẽ bỏ qua ảnh đã upload (trừ khi --force), nên chạy nhiều lần an toàn.
------------------------------------------------------------------------------
"""
import os, sys, json, time, hashlib, mimetypes, urllib.request, urllib.parse, re, ssl

# ---- Đường dẫn (tự suy từ vị trí script) ----
HERE = os.path.dirname(os.path.abspath(__file__))          # .../reports/scripts
REPORTS = os.path.dirname(HERE)                            # .../reports
SHOTS_DIR = os.path.join(REPORTS, "test-cases", "screenshots")
ISSUES_DIR = os.path.join(REPORTS, "issues")
BUG_REPORT = os.path.join(REPORTS, "bug-report.md")
URL_MAP = os.path.join(HERE, "cloudinary-url-map.json")
CLOUD_FOLDER = "eshop-hw03/gui-checklist"                  # thư mục trên Cloudinary

DRY = "--dry-run" in sys.argv
FORCE = "--force" in sys.argv
INSECURE = "--insecure" in sys.argv


def make_ssl_context():
    """Tạo SSL context có CA bundle hợp lệ (macOS Python hay thiếu).
    Thứ tự ưu tiên: certifi -> mặc định hệ thống -> (nếu --insecure) bỏ verify."""
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
    sys.exit("Thiếu credential. Set CLOUDINARY_URL hoặc CLOUDINARY_CLOUD_NAME/API_KEY/API_SECRET. "
             "Xem hướng dẫn ở đầu file. (Có thể chạy --dry-run mà không cần key.)")


def sign(params, api_secret):
    # Cloudinary: sort param theo alpha, nối key=value bằng &, thêm secret, sha1
    items = sorted((k, v) for k, v in params.items() if v not in (None, ""))
    to_sign = "&".join("%s=%s" % (k, v) for k, v in items)
    return hashlib.sha1((to_sign + api_secret).encode("utf-8")).hexdigest()


def upload(path, public_id, cloud_name, api_key, api_secret):
    ts = str(int(time.time()))
    params = {"public_id": public_id, "folder": CLOUD_FOLDER,
              "overwrite": "true", "timestamp": ts}
    signature = sign(params, api_secret)
    fields = dict(params, api_key=api_key, signature=signature)

    # multipart/form-data thủ công
    boundary = "----hw03boundary" + ts
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
    with urllib.request.urlopen(req, timeout=60, context=SSL_CTX) as resp:
        return json.loads(resp.read().decode("utf-8"))["secure_url"]


def embed_into_markdown(url_map):
    """Thay token `GUI-xxx.png` trong issues/*.md và bug-report.md bằng ảnh nhúng."""
    def repl(text):
        def sub(m):
            fname = m.group(1)                     # GUI-xxx.png
            cid = fname[:-4]
            u = url_map.get(fname)
            if not u:
                return m.group(0)                  # chưa có URL → giữ nguyên
            return "![%s](%s)" % (cid, u)
        # match `GUI-xxx.png` (trong backtick)
        return re.sub(r"`(GUI-[A-Za-z0-9-]+\.png)`", sub, text)

    targets = []
    if os.path.isdir(ISSUES_DIR):
        targets += [os.path.join(ISSUES_DIR, f) for f in os.listdir(ISSUES_DIR) if f.endswith(".md")]
    if os.path.exists(BUG_REPORT):
        targets.append(BUG_REPORT)

    changed = 0
    for t in targets:
        txt = open(t, encoding="utf-8").read()
        new = repl(txt)
        # dọn ghi chú "_(trong reports/test-cases/screenshots/)_" thừa
        new = new.replace(" _(trong reports/test-cases/screenshots/)_", "")
        if new != txt:
            if not DRY:
                open(t, "w", encoding="utf-8").write(new)
            changed += 1
    return changed


def main():
    if not os.path.isdir(SHOTS_DIR):
        sys.exit("Không thấy thư mục screenshots: %s" % SHOTS_DIR)
    shots = sorted(f for f in os.listdir(SHOTS_DIR) if f.endswith(".png"))
    print("Tìm thấy %d screenshot trong %s" % (len(shots), SHOTS_DIR))

    url_map = {}
    if os.path.exists(URL_MAP):
        url_map = json.load(open(URL_MAP))

    if DRY:
        todo = [s for s in shots if FORCE or s not in url_map]
        print("[DRY-RUN] Sẽ upload %d ảnh, bỏ qua %d ảnh đã có URL." % (len(todo), len(shots) - len(todo)))
        for s in todo[:5]:
            print("  upload ->", s)
        if len(todo) > 5:
            print("  ... (+%d nữa)" % (len(todo) - 5))
        n = embed_into_markdown(url_map)  # nhúng bằng URL đã cache (nếu có)
        print("[DRY-RUN] Sẽ cập nhật %d file markdown (dựa trên URL đang có trong cache)." % n)
        return

    cloud_name, api_key, api_secret = get_creds()
    print("Cloudinary cloud: %s | folder: %s" % (cloud_name, CLOUD_FOLDER))

    ok, skip, fail = 0, 0, 0
    for s in shots:
        if s in url_map and not FORCE:
            skip += 1
            continue
        cid = s[:-4]
        try:
            secure = upload(os.path.join(SHOTS_DIR, s), cid, cloud_name, api_key, api_secret)
            url_map[s] = secure
            ok += 1
            print("  ✓ %s -> %s" % (s, secure))
            json.dump(url_map, open(URL_MAP, "w"), indent=2, ensure_ascii=False)  # lưu ngay từng ảnh
        except Exception as e:
            fail += 1
            print("  ✗ %s : %s" % (s, e))

    json.dump(url_map, open(URL_MAP, "w"), indent=2, ensure_ascii=False)
    print("Upload xong: %d mới, %d bỏ qua (đã có), %d lỗi." % (ok, skip, fail))

    changed = embed_into_markdown(url_map)
    print("Đã nhúng URL vào %d file markdown (issues/ + bug-report.md)." % changed)
    print("URL map lưu tại: %s" % URL_MAP)
    print("\nBước tiếp: đăng issue lên GitHub, ví dụ:")
    print("  gh auth login")
    print("  for f in reports/issues/BUG-*.md; do")
    print("    gh issue create --repo trngnneee/eshop-sut \\")
    print("      --title \"$(sed -n '2p' \"$f\")\" --body-file \"$f\" --label bug,ui ; done")


if __name__ == "__main__":
    main()
