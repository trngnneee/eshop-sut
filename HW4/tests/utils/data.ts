// Shared loader for the external JSON test-data arrays every spec file consumes. Extracted
// out of login/cart/dashboard.spec.ts (which each had an identical copy) so the validation
// rules — file exists, is an array, meets the minimum case count, has no duplicate caseId —
// live in exactly one place.
import * as fs from 'fs';
import * as path from 'path';

export function loadJsonArray<T extends { caseId: string }>(fileName: string, minCount: number): T[] {
  const filePath = path.join(__dirname, '../../test-data', fileName);
  if (!fs.existsSync(filePath)) {
    throw new Error(`Test data file not found: ${filePath}`);
  }
  const parsed = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  if (!Array.isArray(parsed)) {
    throw new Error(`${fileName} must contain a JSON array of test cases`);
  }
  if (parsed.length < minCount) {
    throw new Error(`${fileName} must contain at least ${minCount} cases, found ${parsed.length}`);
  }
  const seen = new Set<string>();
  for (const row of parsed) {
    if (!row || typeof row.caseId !== 'string' || row.caseId.length === 0) {
      throw new Error(`${fileName}: every case must have a non-empty caseId`);
    }
    if (seen.has(row.caseId)) {
      throw new Error(`${fileName}: duplicate caseId "${row.caseId}"`);
    }
    seen.add(row.caseId);
  }
  return parsed as T[];
}
