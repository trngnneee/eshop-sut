#!/usr/bin/env node
/**
 * Upload bug screenshots lên Cloudinary rồi cập nhật link ảnh trong GitHub Issues.
 *
 * Credentials KHÔNG hardcode — truyền qua biến môi trường lúc chạy:
 *   CLOUDINARY_CLOUD_NAME=<cloud> \
 *   CLOUDINARY_API_KEY=<key> \
 *   CLOUDINARY_API_SECRET=<secret> \
 *   node scripts/upload-screenshots-cloudinary.mjs
 *
 * Các bước:
 *   1. Upload mọi *.png trong bugs/screenshots/ lên Cloudinary (signed upload, folder eshop-hw04-bugs)
 *   2. Ghi mapping <tên file> → <secure_url> ra bugs/cloudinary-map.json
 *   3. Quét các GitHub Issue có label "found-by: test-case" (qua gh CLI),
 *      thay mọi URL ảnh cũ trỏ tới tên file đó bằng URL Cloudinary tương ứng.
 */
import { createHash } from 'node:crypto';
import { readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SCREENSHOT_DIR = path.join(ROOT, 'bugs', 'screenshots');
const MAP_FILE = path.join(ROOT, 'bugs', 'cloudinary-map.json');
const CLOUDINARY_FOLDER = 'eshop-hw04-bugs';
const ISSUE_LABEL = 'found-by: test-case';

const { CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET } = process.env;
if (!CLOUDINARY_CLOUD_NAME || !CLOUDINARY_API_KEY || !CLOUDINARY_API_SECRET) {
  console.error(
    'Thiếu env: cần CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET',
  );
  process.exit(1);
}

/** Signed upload theo Cloudinary Upload API: signature = sha1(params_sorted + api_secret) */
async function uploadImage(filePath) {
  const publicId = path.basename(filePath, '.png');
  const timestamp = Math.floor(Date.now() / 1000);
  const paramsToSign = `folder=${CLOUDINARY_FOLDER}&public_id=${publicId}&timestamp=${timestamp}`;
  const signature = createHash('sha1')
    .update(paramsToSign + CLOUDINARY_API_SECRET)
    .digest('hex');

  const form = new FormData();
  form.append('file', new Blob([readFileSync(filePath)], { type: 'image/png' }), path.basename(filePath));
  form.append('api_key', CLOUDINARY_API_KEY);
  form.append('timestamp', String(timestamp));
  form.append('folder', CLOUDINARY_FOLDER);
  form.append('public_id', publicId);
  form.append('signature', signature);

  const res = await fetch(
    `https://api.cloudinary.com/v1_1/${CLOUDINARY_CLOUD_NAME}/image/upload`,
    { method: 'POST', body: form },
  );
  const json = await res.json();
  if (!res.ok) throw new Error(`Upload ${publicId} thất bại: ${JSON.stringify(json)}`);
  return json.secure_url;
}

function gh(...args) {
  return execFileSync('gh', args, { encoding: 'utf8', cwd: ROOT });
}

// ---- Bước 1 + 2: upload và ghi mapping ----
const files = readdirSync(SCREENSHOT_DIR).filter((f) => f.endsWith('.png')).sort();
if (files.length === 0) {
  console.error(`Không tìm thấy ảnh nào trong ${SCREENSHOT_DIR}`);
  process.exit(1);
}

const map = {};
for (const f of files) {
  map[f] = await uploadImage(path.join(SCREENSHOT_DIR, f));
  console.log(`☁️  ${f} → ${map[f]}`);
}
writeFileSync(MAP_FILE, JSON.stringify(map, null, 2) + '\n');
console.log(`\n💾 Đã ghi mapping: ${path.relative(process.cwd(), MAP_FILE)}`);

// ---- Bước 3: cập nhật GitHub Issues ----
const issues = JSON.parse(
  gh('issue', 'list', '--label', ISSUE_LABEL, '--state', 'open', '--limit', '100', '--json', 'number'),
);
let updated = 0;
for (const { number } of issues) {
  const body = JSON.parse(gh('issue', 'view', String(number), '--json', 'body')).body;
  let newBody = body;
  for (const [file, url] of Object.entries(map)) {
    // thay mọi URL cũ (raw.githubusercontent, ...) kết thúc bằng tên file này
    newBody = newBody.replace(new RegExp(`https?://[^\\s()]+/${file}`, 'g'), url);
  }
  if (newBody !== body) {
    const tmp = path.join(ROOT, 'bugs', `.issue-${number}.tmp.md`);
    writeFileSync(tmp, newBody);
    gh('issue', 'edit', String(number), '--body-file', tmp);
    execFileSync('rm', [tmp]);
    console.log(`🔁 Issue #${number}: đã thay link ảnh sang Cloudinary`);
    updated++;
  }
}
console.log(`\n✅ Hoàn tất: upload ${files.length} ảnh, cập nhật ${updated} issue.`);
