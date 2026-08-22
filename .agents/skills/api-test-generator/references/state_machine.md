# Order State Machine (FR-10) — dùng cho Stage 2

Tham khảo nhanh máy trạng thái đơn hàng theo đề bài. **Đây là tham khảo mặc định** — nếu `api_specification.md` thực tế của repo `eshop-sut` mô tả chi tiết hơn (thêm state, thêm điều kiện huỷ), ưu tiên theo spec thật, dùng file này chỉ để đối chiếu không bỏ sót cạnh nào.

## Các trạng thái hợp lệ

```
pending → confirmed → shipping → delivered
```

## Quy tắc huỷ (cancellation) — mặc định giả thiết cần xác nhận lại theo spec thật

- Huỷ được khi đơn ở `pending` hoặc `confirmed`.
- **Không** huỷ được khi đơn đã `shipping` hoặc `delivered`.
- Trạng thái `cancelled` là trạng thái kết thúc (terminal), không thể chuyển tiếp sang trạng thái nào khác.
- `delivered` cũng là trạng thái kết thúc.

## Ma trận các cạnh cần test ở Stage 2

### Cạnh hợp lệ (expected_allowed = true)
| From | Action | To |
|---|---|---|
| pending | confirm | confirmed |
| confirmed | ship | shipping |
| shipping | deliver | delivered |
| pending | cancel | cancelled |
| confirmed | cancel | cancelled |

### Cạnh KHÔNG hợp lệ (expected_allowed = false) — nhóm hay bị AI generic bỏ sót
| From | Action | To (mong muốn) | Vì sao invalid |
|---|---|---|---|
| pending | deliver | delivered | Nhảy cóc bỏ qua confirmed + shipping |
| pending | ship | shipping | Nhảy cóc bỏ qua confirmed |
| confirmed | deliver | delivered | Nhảy cóc bỏ qua shipping |
| shipping | cancel | cancelled | Đã giao vận, không được huỷ |
| delivered | cancel | cancelled | Đơn đã kết thúc, không được huỷ |
| delivered | (bất kỳ action) | * | Trạng thái terminal, mọi action khác đều phải bị từ chối |
| cancelled | (bất kỳ action) | * | Trạng thái terminal, mọi action khác đều phải bị từ chối |
| cancelled | confirm | confirmed | Không "hồi sinh" đơn đã huỷ |

## Gợi ý thêm khi áp dụng cho API khác (không phải order)

Nếu Stage 2 đang chạy cho API không thuộc FR-10 (vd login/lockout FR-02), coi đây là mẫu tương tự:
- Login/lockout: `active → (n lần login sai) → locked → (timeout/admin reset) → active`. Test cạnh hợp lệ (login đúng khi active) và cạnh không hợp lệ (login đúng nhưng account đang locked vẫn phải bị từ chối).
- Coupon: `active → expired`, `active → used` (nếu single-use), test dùng coupon đã `expired`/`used` phải bị từ chối ở API checkout.