---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Cart] Giỏ hàng lưu in-memory: mất khi restart, trộn giỏ giữa VU trùng user, rò rỉ RAM'
labels: ['type: bug', 'status: new', 'found-by: test-case', 'severity: major', 'reliability']
assignees: ''
---

## Found by Test Case

PERF-SOAK-01 (quan sát RAM node process trong soak 12 phút) + review source `POST /api/cart`.

## Requirement liên quan

FR-07 (Shopping cart)

## Severity / Priority

Major / P1

## Environment

- **OS**: macOS 15.5 (Darwin 24.5.0), Apple M4
- **Browser**: N/A — Backend REST API (JMeter 5.6.3 / curl)
- **URL**: http://localhost:3000/api/cart
- **Build/Commit**: eshop-sut (HW05 SUT) · `backend/server.js` dòng 14, 284–295

## Steps to reproduce

1. Login lấy token, thêm sản phẩm vào giỏ: `POST /api/cart` (Bearer) với body bất kỳ.
2. (a) Restart backend → gọi `GET /api/cart` → giỏ **rỗng** (mất dữ liệu).
3. (b) Hai VU dùng chung một `user_id` cùng thêm giỏ → `GET /api/cart` thấy **giỏ bị trộn**.
4. (c) Chạy tải kéo dài với nhiều user → theo dõi RSS của node (`monitor.sh`): `userCarts` không bao giờ được giải phóng.

## Expected result

Giỏ hàng được lưu bền vững (DB), phân tách theo user/phiên, và có validate payload; bộ nhớ được giải phóng khi phiên kết thúc.

## Actual result

- `server.js:14`: `const userCarts = {}` — lưu toàn bộ giỏ trong RAM tiến trình.
- `server.js:293`: `userCarts[userId].push(req.body)` — push nguyên `req.body`, không validate.
- Hệ quả: (a) restart mất toàn bộ giỏ; (b) VU trùng `user_id` trộn giỏ lẫn nhau; (c) rò rỉ bộ nhớ khi số user tăng (không bao giờ giải phóng). Trong soak 12 phút mức 30 VU chưa thấy leak rõ (GC thu hồi kịp) nhưng rủi ro hiện hữu ở tải cao/kéo dài.

## Evidence

`results/soak/resource_soak.csv` (xu hướng RSS node), `docs/results_summary.md` (mục Soak).
![BUG-05](https://res.cloudinary.com/dnqinxiwo/image/upload/v1786794400/eshop-hw05/perf-bugs/BUG-05.png)
