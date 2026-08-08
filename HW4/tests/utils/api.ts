// Thin wrappers around the SUT's REST API used for deterministic test-data setup
// (registering throwaway accounts, reading admin-only state) so UI specs don't have
// to click through unrelated flows just to reach a precondition.
import type { APIRequestContext } from '@playwright/test';

// Override with API_BASE_URL if your local machine needs a non-default backend port
// (see HW4/docs/prompt-log.md "environment notes" — this repo's default is :3000).
export const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:3000';

export const ADMIN_CREDENTIALS = { email: 'admin@eshop.com', password: 'Admin123!' };
export const SEED_USER_CREDENTIALS = { email: 'test@eshop.com', password: 'Test1234!' };

export async function registerUser(
  request: APIRequestContext,
  user: { name: string; email: string; password: string },
) {
  return request.post(`${API_BASE_URL}/api/register`, { data: user });
}

export async function apiLogin(request: APIRequestContext, email: string, password: string) {
  return request.post(`${API_BASE_URL}/api/login`, { data: { email, password } });
}

export async function loginAdminToken(request: APIRequestContext): Promise<string> {
  const res = await apiLogin(request, ADMIN_CREDENTIALS.email, ADMIN_CREDENTIALS.password);
  const body = await res.json();
  if (!body.token) throw new Error(`Admin login failed while setting up test data: ${JSON.stringify(body)}`);
  return body.token as string;
}

export async function getAdminUserByEmail(request: APIRequestContext, token: string, email: string) {
  const res = await request.get(`${API_BASE_URL}/api/admin/users`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const users = await res.json();
  return (users as Array<{ email: string }>).find((u) => u.email === email);
}

/** Registers a throwaway single-use account for a test case; ignores "already exists" races. */
export async function ensureFreshAccount(
  request: APIRequestContext,
  email: string,
  password: string,
  name = 'HW04 Test User',
) {
  await registerUser(request, { name, email, password });
}

/** Decodes a JWT's payload without verifying the signature (test inspection only). */
export function decodeJwtPayload(token: string): Record<string, unknown> {
  const parts = token.split('.');
  if (parts.length !== 3) throw new Error(`Not a JWT: ${token}`);
  const payloadJson = Buffer.from(parts[1], 'base64url').toString('utf-8');
  return JSON.parse(payloadJson);
}
