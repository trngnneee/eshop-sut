/**
 * Verify Feature A (FR-03) live reports still match the frozen archive
 * and that EVIDENCE-LOCK markers remain in place.
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..');
const LIVE = path.join(ROOT, 'reports', 'html', 'fr03-forgot-password');
const ARCHIVE = path.join(
  ROOT,
  'evidence',
  'feature-a-fr03-frozen-2026-08-07',
  'reports-html-fr03-forgot-password',
);
const BROWSERS = ['chromium', 'firefox', 'webkit'];

function sha256(filePath) {
  const hash = crypto.createHash('sha256');
  hash.update(fs.readFileSync(filePath));
  return hash.digest('hex');
}

function main() {
  const problems = [];

  if (!fs.existsSync(ARCHIVE)) {
    problems.push(`Missing freeze archive: ${ARCHIVE}`);
  }

  for (const browser of BROWSERS) {
    const liveIndex = path.join(LIVE, browser, 'index.html');
    const archIndex = path.join(ARCHIVE, browser, 'index.html');
    const lock = path.join(LIVE, browser, 'EVIDENCE-LOCK.json');

    if (!fs.existsSync(liveIndex)) {
      problems.push(`Missing live report: ${liveIndex}`);
    }
    if (!fs.existsSync(archIndex)) {
      problems.push(`Missing archived report: ${archIndex}`);
    }
    if (!fs.existsSync(lock)) {
      problems.push(`Missing EVIDENCE-LOCK.json for ${browser}`);
    }
    if (fs.existsSync(liveIndex)) {
      const html = fs.readFileSync(liveIndex, 'utf8');
      if (!html.includes('Run by: 23127271')) {
        problems.push(`${browser} live index.html missing Run by: 23127271`);
      }
    }
    if (fs.existsSync(liveIndex) && fs.existsSync(archIndex)) {
      const liveHash = sha256(liveIndex);
      const archHash = sha256(archIndex);
      // Live may have been stamped identically; hash equality is ideal.
      // If lock exists and label present, warn only when hashes diverge.
      if (liveHash !== archHash) {
        problems.push(
          `${browser}: live index.html hash != frozen archive (possible overwrite). live=${liveHash.slice(0, 12)} archive=${archHash.slice(0, 12)}`,
        );
      }
    }
  }

  if (problems.length) {
    console.error('Feature A evidence verification FAILED:');
    for (const p of problems) console.error(` - ${p}`);
    process.exit(1);
  }

  console.log('Feature A evidence OK:');
  console.log(` - Locks present under ${LIVE}`);
  console.log(` - Archive intact at ${ARCHIVE}`);
  console.log(' - All three index.html contain Run by: 23127271 and match freeze hashes');
}

main();
