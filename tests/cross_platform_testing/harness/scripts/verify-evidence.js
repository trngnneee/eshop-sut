// Evidence gate for the Task 3 deliverable.
//
//   node scripts/verify-evidence.js
//
// Fails loudly (exit 1) if the evidence set is not internally consistent, so that
// a partial run can never be reported as a complete one:
//   1. every platform ran the same set of checklist IDs, and that set matches
//      the 66 items of the Task 1 checklist;
//   2. every result with status FAIL/ERROR has at least one screenshot file that
//      actually exists on disk;
//   3. no result is left in ERROR (a harness bug must not masquerade as a finding);
//   4. every referenced screenshot is a non-empty PNG.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..');
const RAW = path.join(ROOT, 'results', 'raw');
const CHECKLIST = path.resolve(
  ROOT,
  '..',
  'gui_and_usability_testing',
  'checklist-final.md',
);

const problems = [];
const notes = [];

// Only the checklist TABLE rows count. IDs mentioned in prose (the dedup log at the
// end of checklist-final.md lists old IDs such as GUI-IA02-15 that were merged away)
// are not checklist items and must not become expectations.
const expectedIds = [
  ...new Set(
    fs
      .readFileSync(CHECKLIST, 'utf8')
      .split('\n')
      .map((line) => (line.match(/^\|\s*(GUI-(?:IA0\d|GAP)-\d{2})\s*\|/) || [])[1])
      .filter(Boolean),
  ),
].sort();
notes.push(`Checklist Task 1: ${expectedIds.length} item IDs found in checklist-final.md`);

const files = fs.readdirSync(RAW).filter((f) => f.endsWith('.json')).sort();
if (files.length < 3) problems.push(`Only ${files.length} platform result file(s) — the assignment requires ≥ 3 platforms.`);

for (const f of files) {
  const run = JSON.parse(fs.readFileSync(path.join(RAW, f), 'utf8'));
  const key = run.platform.key;
  const ids = run.results.map((r) => r.id).sort();

  const missing = expectedIds.filter((id) => !ids.includes(id));
  const extra = ids.filter((id) => !expectedIds.includes(id));
  if (missing.length) problems.push(`${key}: missing ${missing.length} checklist item(s): ${missing.join(', ')}`);
  if (extra.length) problems.push(`${key}: unknown item id(s): ${extra.join(', ')}`);

  for (const r of run.results) {
    if (r.status === 'ERROR') problems.push(`${key}/${r.id}: status ERROR — ${r.evidence}`);
    if (['FAIL', 'ERROR'].includes(r.status) && r.screenshots.length === 0)
      problems.push(`${key}/${r.id}: ${r.status} without a screenshot`);
    for (const s of r.screenshots) {
      const p = path.join(ROOT, 'results', key, 'screenshots', s);
      if (!fs.existsSync(p)) problems.push(`${key}/${r.id}: screenshot missing on disk (${s})`);
      else if (fs.statSync(p).size < 5000) problems.push(`${key}/${r.id}: screenshot suspiciously small (${s})`);
    }
  }

  const proofDir = path.join(ROOT, 'results', key, 'platform-proof');
  const proofs = fs.existsSync(proofDir) ? fs.readdirSync(proofDir).filter((x) => x.endsWith('.png')) : [];
  notes.push(
    `${key}: ${run.results.length} items · ${JSON.stringify(run.summary)} · ` +
      `${run.results.reduce((n, r) => n + r.screenshots.length, 0)} viewport shots · ${proofs.length} window-proof shots`,
  );
  if (!run.platform.emulated && proofs.length === 0)
    problems.push(`${key}: no platform-proof window screenshots (run scripts/capture-platform-proof.js)`);
}

console.log(notes.join('\n'));
if (problems.length) {
  console.error(`\n${problems.length} PROBLEM(S):`);
  for (const p of problems) console.error(`  ✗ ${p}`);
  process.exit(1);
}
console.log('\n✓ Evidence set is complete and consistent.');
