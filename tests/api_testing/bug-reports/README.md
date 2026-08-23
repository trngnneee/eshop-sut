# Bug Reports — HW06 (MSSV 23127438)

SUT: **eshop-sut** `http://localhost:3000` @ commit `0601698`. Scope 3 API (FR-05/06, FR-10, FR-15).

Mỗi file theo đúng template `.github/ISSUE_TEMPLATE/bug_report.md`. Đã đẩy lên GitHub Issues bằng `gh` (xem link trong mỗi issue). Không đánh số bug — mỗi issue định danh bằng tiêu đề + TC-ID.


| Bug | Module | FR/SEC | Severity | Found by (TC-ID) | Issue |
|-----|--------|--------|----------|------------------|------|
| `price` trả về string với product id CHẴN (sai kiểu) | API-1 | FR-06 | Major / P1 | TC-P1-004, TC-P1-005, TC-P1-020, TC-P1-021, TC-P1-062, TC-P1-063, TC-P1-070 | [#452](https://github.com/trngnneee/eshop-sut/issues/452) |
| GET id không tồn tại trả `200 {}` thay vì `404` | API-1 | FR-06 | Major / P1 | TC-P1-006, TC-P1-007, TC-P1-065 | [#450](https://github.com/trngnneee/eshop-sut/issues/450) |
| Không validate kiểu path param `:id` (sai kiểu vẫn trả `200 {}`) | API-1 | FR-06 | Minor / P2 | TC-P1-008, TC-P1-009, TC-P1-010, TC-P1-011, TC-P1-013, TC-P1-019 | [#443](https://github.com/trngnneee/eshop-sut/issues/443) |
| Lỗi SQL trả HTML + lộ nguyên văn thông điệp lỗi DB (500 text/html) | API-1 | SEC-05 | Major / P1 | TC-P1-050, TC-P1-051, TC-P1-052, TC-P1-053 | [#456](https://github.com/trngnneee/eshop-sut/issues/456) |
| User HỦY được đơn đang `shipping` (đáng lẽ chỉ Admin) | API-2 | FR-10 | Critical / P0 | TC-O2-018, TC-O2-023, TC-O2-024, TC-O2-041 | [#440](https://github.com/trngnneee/eshop-sut/issues/440) |
| Đọc đơn hàng của bất kỳ ai KHÔNG cần token (IDOR read) | API-2 | SEC-02 / FR-10 | Critical / P0 | TC-O2-058, TC-O2-034 | [#451](https://github.com/trngnneee/eshop-sut/issues/451) |
| CRUD sản phẩm KHÔNG có auth — ẩn danh tạo/sửa/XOÁ được | API-3 | FR-12 / SEC-02 / SEC-03 | Critical / P0 | TC-P3-049, TC-P3-050, TC-P3-052, TC-P3-053, TC-P3-054, TC-P3-055, TC-P3-070 | [#453](https://github.com/trngnneee/eshop-sut/issues/453) |
| POST/PUT không validate input theo FR-15 (name rỗng / price ≤0 / category không tồn tại) | API-3 | FR-15 | Critical / P0 | TC-P3-004, 005, 008, 009, 011, 012, 013, 014, 015, 016, 021, 022, 023, 024, 025, 030, 036, 037, 038, 068, 076 | [#448](https://github.com/trngnneee/eshop-sut/issues/448) |
| Body rỗng `{}` tạo record toàn `null` | API-3 | FR-15 | Major / P1 | TC-P3-031, TC-P3-046 | [#441](https://github.com/trngnneee/eshop-sut/issues/441) |
| `name` vượt 255 ký tự vẫn được tạo | API-3 | FR-15 | Major / P1 | TC-P3-006, TC-P3-007 | [#447](https://github.com/trngnneee/eshop-sut/issues/447) |
| PUT thiếu field làm NULL hóa các field không gửi (mất dữ liệu) | API-3 | FR-15 | Critical / P0 | TC-P3-034, TC-P3-042 | [#454](https://github.com/trngnneee/eshop-sut/issues/454) |
| PUT/DELETE trên id không tồn tại trả `200` no-op thay vì `404` | API-3 | FR-15 | Major / P1 | TC-P3-035, TC-P3-069, TC-P3-074 | [#449](https://github.com/trngnneee/eshop-sut/issues/449) |
| Secret JWT hardcode → forge token, mạo danh + nâng quyền | API-2/API-3 | SEC-02 / SEC-03 | Critical / P0 | TC-O2-032, TC-O2-033, TC-O2-034 | [#445](https://github.com/trngnneee/eshop-sut/issues/445) |
| id không canonical (`1.0`, `" 1"`, `"+1"`, `"01"`) được chấp nhận (numeric affinity) | API-1 | FR-06 | Minor / P2 | TC-P1-012, TC-P1-015, TC-P1-016, TC-P1-017, TC-P1-018, TC-P1-084 | [#444](https://github.com/trngnneee/eshop-sut/issues/444) |
| Lỗi 404/400 trả HTML thay vì JSON `{error}` | API-1/2/3 | FR-06 (contract) | Minor / P2 | TC-P1-025, 075, 076, 077 | [#442](https://github.com/trngnneee/eshop-sut/issues/442) |
| Tìm kiếm không phân biệt hoa/thường KHÔNG nhất quán với Unicode (chữ HOA có dấu → 0 kết quả) | API-1 | FR-05 | Major / P1 | TC-P1-038 | [#458](https://github.com/trngnneee/eshop-sut/issues/458) |
| SQL Injection / wildcard bypass ở `?search=` (%, _, tautology trả toàn bộ sản phẩm) | API-1 | FR-05 / SEC-05 | Critical / P0 | TC-P1-040, 041, 042, 045, 046, 047, 085 | [#457](https://github.com/trngnneee/eshop-sut/issues/457) |
| Param `search` lặp → nối chuỗi sai → 0 kết quả (thất bại im lặng) | API-1 | FR-05 | Minor / P2 | TC-P1-044 | [#455](https://github.com/trngnneee/eshop-sut/issues/455) |
| SQLi UNION rút bảng `users` — lộ email + password PLAINTEXT + role admin qua 1 GET không auth | API-1 | SEC-05 + SEC-01 | Critical / P0 | TC-P1-048, TC-P1-049 | [#459](https://github.com/trngnneee/eshop-sut/issues/459) |
| Thiếu header `X-Content-Type-Options: nosniff` (hardening) | API-1 | SEC-04 | Minor / P2 | TC-P1-056 | [#446](https://github.com/trngnneee/eshop-sut/issues/446) |

**Tổng: 20 bug.** Observation KHÔNG tính bug: OBS-01 (`?search=` rỗng trả toàn bộ — hợp lý); validation gap `:id` API-2 (query parameterized nên chỉ 404); trùng tên TC-P3-075 (spec không cấm). Cờ SEC-04 (stored-XSS vector) kiểm chéo ở tầng UI.

