import { IA01 } from './ia01.js';
import { IA02 } from './ia02.js';
import { IA03 } from './ia03.js';
import { IA04 } from './ia04.js';

export const CHECKS = [...IA01, ...IA02, ...IA03, ...IA04];

const ids = CHECKS.map((c) => c.id);
const dupes = ids.filter((id, i) => ids.indexOf(id) !== i);
if (dupes.length) throw new Error(`Duplicate check ids: ${dupes.join(', ')}`);
