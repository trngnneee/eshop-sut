import { test, expect } from '@playwright/test';
import * as path from 'path';
import { API_BASE_URL, apiLogin, decodeJwtPayload, registerUser } from './utils/api';
import { deleteUserByEmail } from './utils/db';
import { loadJsonArray } from './utils/data';

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

const cases = loadJsonArray<ApiCase>('login-api-cases.json', 1);

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
        case 'duplicate-email-rejected': {
          const email = `dup-${c.caseId.toLowerCase()}@eshop.com`;
          await deleteUserByEmail(email).catch(() => undefined);
          const first = await registerUser(request, { name: 'First', email, password: 'FirstPass1!' });
          expect(first.status()).toBeLessThan(300);
          const second = await registerUser(request, { name: 'Second', email, password: 'SecondPass1!' });
          // Spec-conformant expectation: a duplicate email must be rejected, not silently
          // accepted as a second, unreachable account with the same login identifier.
          expect(second.status()).toBeGreaterThanOrEqual(400);
          break;
        }
        case 'empty-password-rejected': {
          const email = `empty-pw-${c.caseId.toLowerCase()}@eshop.com`;
          await deleteUserByEmail(email).catch(() => undefined);
          const res = await registerUser(request, { name: 'Empty PW', email, password: '' });
          // Spec-conformant expectation: registration must enforce a minimum password
          // policy, not accept an empty string as a valid credential.
          expect(res.status()).toBeGreaterThanOrEqual(400);
          break;
        }
        case 'reset-token-strength': {
          const email = `reset-strength-${c.caseId.toLowerCase()}@eshop.com`;
          await deleteUserByEmail(email).catch(() => undefined);
          await registerUser(request, { name: 'Reset Strength', email, password: 'ValidPassword1!' });
          const res = await request.post(`${API_BASE_URL}/api/forgot-password`, { data: { email } });
          const { resetToken } = await res.json();
          // Spec-conformant expectation: a reset token should be long/random enough to
          // resist brute-forcing (e.g. not a plain 4-digit number, only 9000 possibilities).
          expect(String(resetToken).length).toBeGreaterThanOrEqual(6);
          break;
        }
        default:
          throw new Error(`Unknown API action "${c.action}" for ${c.caseId}`);
      }
    });
  }
});
