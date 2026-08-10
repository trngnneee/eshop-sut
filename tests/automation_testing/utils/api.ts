import { APIRequestContext, expect } from '@playwright/test';

export const API_BASE = 'http://localhost:3000/api';

function authHeader(token: string) {
  return { Authorization: `Bearer ${token}` };
}

/** Đăng ký user mới qua API (dùng seed dữ liệu cho các kịch bản lockout / coupon usage). */
export async function registerUser(
  request: APIRequestContext,
  email: string,
  password: string,
  name = 'Automation User',
): Promise<void> {
  const res = await request.post(`${API_BASE}/register`, { data: { name, email, password } });
  expect(res.ok(), `đăng ký user seed ${email} thất bại`).toBeTruthy();
}

/** Đăng nhập qua API, trả về JWT token. */
export async function loginToken(
  request: APIRequestContext,
  email: string,
  password: string,
): Promise<string> {
  const res = await request.post(`${API_BASE}/login`, { data: { email, password } });
  expect(res.ok(), `đăng nhập API với ${email} thất bại`).toBeTruthy();
  return (await res.json()).token;
}

/** Lấy map code → id của tất cả coupon. */
export async function getCouponIds(
  request: APIRequestContext,
  token: string,
): Promise<Record<string, number>> {
  const res = await request.get(`${API_BASE}/coupons`, { headers: authHeader(token) });
  expect(res.ok()).toBeTruthy();
  const rows: Array<{ code: string; id: number }> = await res.json();
  return Object.fromEntries(rows.map((r) => [r.code, r.id]));
}

/** Ghi nhận 1 lượt sử dụng coupon cho user của token (seed cho kịch bản C5 — vượt giới hạn lượt dùng). */
export async function recordCouponUsage(
  request: APIRequestContext,
  token: string,
  couponId: number,
): Promise<void> {
  const res = await request.post(`${API_BASE}/coupon-usage`, {
    data: { coupon_id: couponId },
    headers: authHeader(token),
  });
  expect(res.ok(), 'seed lượt dùng coupon thất bại').toBeTruthy();
}

export async function getCategories(
  request: APIRequestContext,
): Promise<Array<{ id: number; name: string }>> {
  const res = await request.get(`${API_BASE}/categories`);
  expect(res.ok()).toBeTruthy();
  return res.json();
}

export async function deleteCategory(
  request: APIRequestContext,
  token: string,
  id: number,
): Promise<void> {
  await request.delete(`${API_BASE}/categories/${id}`, { headers: authHeader(token) });
}
