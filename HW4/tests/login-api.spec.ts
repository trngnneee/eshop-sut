import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';
import { API_BASE_URL, apiLogin, decodeJwtPayload } from './utils/api';

// Reuses the backend's own already-installed jsonwebtoken package to forge adversarial
// tokens for the wrong-secret / tampered-payload cases — never used to bypass anything,
// only to prove the protected endpoints correctly reject them.
// eslint-disable-next-line @typescript-eslint/no-var-requires
const jwt = require(path.join(__dirname, '../../backend/node_modules/jsonwebtoken'));

const STUDENT_ID = '23127207';

interface ApiCase {
  caseId: string;
  category: string;
  description: string;
  bugRef?: string;
  action: string;
  body?: Record<string, unknown>;
  email?: string;
  password?: string;
  expectedStatusNot?: number;
}

function loadCases(): ApiCase[] {
  const filePath = path.join(__dirname, '../test-data/login-api-cases.json');
  if (!fs.existsSync(filePath)) {
    throw new Error(`Test data file not found: ${filePath}`);
  }
  const parsed = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  if (!Array.isArray(parsed) || parsed.length === 0) {
    throw new Error('login-api-cases.json must contain a non-empty JSON array');
  }
  return parsed as ApiCase[];
}

const cases = loadCases();

test.describe('FR-02 Login API contract', () => {
  for (const c of cases) {
    test(`${c.caseId}: ${c.description}`, async ({ request }, testInfo) => {
      testInfo.annotations.push({ type: 'Run by', description: STUDENT_ID });
      if (c.bugRef) testInfo.annotations.push({ type: 'Bug ref', description: c.bugRef });

      switch (c.action) {
        case 'missing-field':
        case 'extra-fields': {
          const res = await request.post(`${API_BASE_URL}/api/login`, { data: c.body });
          // Assertion pattern: HTTP status must not be a server crash (500).
          expect(res.status()).not.toBe(c.expectedStatusNot);
          break;
        }
        case 'malformed-json': {
          const res = await request.post(`${API_BASE_URL}/api/login`, {
            headers: { 'Content-Type': 'application/json' },
            data: '{ this is not valid json',
          });
          expect(res.status()).not.toBe(c.expectedStatusNot);
          break;
        }
        case 'bad-content-type': {
          const res = await request.post(`${API_BASE_URL}/api/login`, {
            headers: { 'Content-Type': 'text/plain' },
            data: JSON.stringify(c.body),
          });
          expect(res.status()).not.toBe(c.expectedStatusNot);
          break;
        }
        case 'success-body-shape': {
          const res = await apiLogin(request, c.email!, c.password!);
          const body = await res.json();
          expect(body).toHaveProperty('token');
          expect(body.user?.password).toBeUndefined();
          break;
        }
        case 'error-body-shape': {
          const res = await apiLogin(request, c.email!, c.password!);
          const body = await res.json();
          const text = JSON.stringify(body).toLowerCase();
          expect(text).not.toMatch(/sqlite|stack|at object\.|node_modules/);
          break;
        }
        case 'token-has-exp-claim': {
          const res = await apiLogin(request, c.email!, c.password!);
          const body = await res.json();
          const payload = decodeJwtPayload(body.token);
          expect(payload).toHaveProperty('exp');
          break;
        }
        case 'tampered-payload-rejected': {
          const res = await apiLogin(request, c.email!, c.password!);
          const { token } = await res.json();
          const [headerB64, , sigB64] = token.split('.');
          const tamperedPayload = Buffer.from(JSON.stringify({ id: 1, role: 'admin' })).toString('base64url');
          const tamperedToken = `${headerB64}.${tamperedPayload}.${sigB64}`;
          const protectedRes = await request.get(`${API_BASE_URL}/api/users/me`, {
            headers: { Authorization: `Bearer ${tamperedToken}` },
          });
          expect(protectedRes.status()).toBe(403);
          break;
        }
        case 'wrong-secret-rejected': {
          const forged = jwt.sign({ id: 1, role: 'admin' }, 'a-completely-wrong-secret');
          const protectedRes = await request.get(`${API_BASE_URL}/api/users/me`, {
            headers: { Authorization: `Bearer ${forged}` },
          });
          expect(protectedRes.status()).toBe(403);
          break;
        }
        case 'tokens-differ-across-logins': {
          const res1 = await apiLogin(request, c.email!, c.password!);
          const body1 = await res1.json();
          const res2 = await apiLogin(request, c.email!, c.password!);
          const body2 = await res2.json();
          expect(body1.token).not.toBe(body2.token);
          break;
        }
        default:
          throw new Error(`Unknown API action "${c.action}" for ${c.caseId}`);
      }
    });
  }
});
