#!/usr/bin/env python3
"""
Upload anh evidence (screenshots/*.png) len Cloudinary bang signed upload
(HTTP thuan, khong can SDK). Sau khi upload, map secure_url vao cac file
issues/BUG-0X.md (thay link local bang link Cloudinary).

BAO MAT: khong hardcode credential trong code. Script load tu bien moi truong
luc chay; neu thieu, doc tiep tu file .env cung thu muc goc performance_testing.

Bien can co:
  CLOUDINARY_CLOUD_NAME
  CLOUDINARY_API_KEY
  CLOUDINARY_API_SECRET

Cach chay:
  # (a) export truc tiep
  export CLOUDINARY_CLOUD_NAME=... CLOUDINARY_API_KEY=... CLOUDINARY_API_SECRET=...
  python3 scripts/upload_cloudinary.py
  # (b) hoac tao file .env (KEY=VALUE) o thu muc performance_testing roi chay
  python3 scripts/upload_cloudinary.py            # upload + map vao issues
  python3 scripts/upload_cloudinary.py --no-map   # chi upload, khong sua issues
"""
import os
import sys
import re
import json
import time
import hashlib
import glob
import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SHOTS = os.path.join(ROOT, "screenshots")
ISSUES = os.path.join(ROOT, "issues")
MAP_FILE = os.path.join(SHOTS, "cloudinary_map.json")
FOLDER = "eshop-hw05/perf-bugs"


def load_env():
    """os.environ truoc; thieu thi doc them tu .env (khong ghi de bien da co)."""
    dotenv = os.path.join(ROOT, ".env")
    if os.path.exists(dotenv):
        with open(dotenv, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                os.environ.setdefault(k, v)
    cloud = os.environ.get("CLOUDINARY_CLOUD_NAME")
    key = os.environ.get("CLOUDINARY_API_KEY")
    secret = os.environ.get("CLOUDINARY_API_SECRET")
    if not (cloud and key and secret):
        sys.exit("Thieu credential. Set CLOUDINARY_CLOUD_NAME / CLOUDINARY_API_KEY / "
                 "CLOUDINARY_API_SECRET qua env hoac file .env.")
    return cloud, key, secret


def sign(params, secret):
    """SHA1 cua cac param (da sort, k=v noi bang &) + api_secret."""
    to_sign = "&".join(f"{k}={params[k]}" for k in sorted(params))
    return hashlib.sha1((to_sign + secret).encode("utf-8")).hexdigest()


def upload_one(path, cloud, key, secret):
    public_id = f"{FOLDER}/{os.path.splitext(os.path.basename(path))[0]}"
    ts = int(time.time())
    signed = {"invalidate": "true", "overwrite": "true",
              "public_id": public_id, "timestamp": ts}
    data = dict(signed, api_key=key, signature=sign(signed, secret))
    url = f"https://api.cloudinary.com/v1_1/{cloud}/image/upload"
    with open(path, "rb") as fh:
        r = requests.post(url, data=data, files={"file": fh}, timeout=60)
    if r.status_code != 200:
        raise SystemExit(f"Upload that bai {path}: HTTP {r.status_code} {r.text[:200]}")
    return r.json()["secure_url"]


def map_into_issues(url_map):
    """Thay ![BUG-0X](...) trong moi issue bang link Cloudinary tuong ung."""
    changed = 0
    for md in sorted(glob.glob(os.path.join(ISSUES, "BUG-*.md"))):
        bug = os.path.splitext(os.path.basename(md))[0]  # BUG-01
        if bug not in url_map:
            continue
        with open(md, encoding="utf-8") as f:
            content = f.read()
        new = re.sub(rf"!\[{re.escape(bug)}\]\([^)]*\)",
                     f"![{bug}]({url_map[bug]})", content)
        if new != content:
            with open(md, "w", encoding="utf-8") as f:
                f.write(new)
            changed += 1
            print(f"  mapped {bug} -> issue")
    print(f"Da cap nhat {changed} issue file.")


def main():
    do_map = "--no-map" not in sys.argv
    cloud, key, secret = load_env()
    pngs = sorted(glob.glob(os.path.join(SHOTS, "BUG-*.png")))
    if not pngs:
        sys.exit("Khong tim thay screenshots/BUG-*.png")
    url_map = {}
    for p in pngs:
        bug = os.path.splitext(os.path.basename(p))[0]
        url = upload_one(p, cloud, key, secret)
        url_map[bug] = url
        print(f"uploaded {bug} -> {url}")
    with open(MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(url_map, f, indent=2, ensure_ascii=False)
    print(f"Da luu map -> {os.path.relpath(MAP_FILE, ROOT)}")
    if do_map:
        map_into_issues(url_map)


if __name__ == "__main__":
    main()
