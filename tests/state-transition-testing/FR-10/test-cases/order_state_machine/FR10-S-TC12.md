# FR10-S-TC12: Từ chối User tự hủy đơn hàng đang shipping

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / State Transition Testing

## State transition coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Transition / Class ID | S-INVALID-05 |
| State variable | `status` |
| Actor | user |
| Flow type | Guard rejection |
| Covered guard/rule | Invalid transition: user cannot cancel shipping order |
| Covered requirement | Khi đơn hàng ở `shipping`, User không được phép tự hủy. Source: README.md:141-162. |

## Preconditions
- Có đơn hàng hợp lệ đang ở trạng thái `shipping`.
- Tài khoản `user` đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | user |
| Current state | shipping |
| Action / Event | Cancel order |
| Requested state | canceled |
| Endpoint / UI flow | PUT /api/orders/:id/cancel |
| Body / Input | [Không có body] |
| Entity ID | {existing_order_id} |

## Test steps
1. Chuẩn bị một đơn hàng đang ở trạng thái `shipping`.
2. Đăng nhập bằng tài khoản `user` hợp lệ.
3. Gửi request `PUT /api/orders/:id/cancel`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result
- Hệ thống trả về HTTP 400 với thông báo lỗi phù hợp.
- Trạng thái đơn hàng vẫn giữ nguyên là `shipping`.

## Status / Related bugs
Failed / BUG-FR10-S-01

## Actual result
- Executed by: Đặng Trường Nguyên.
- Execution interface: Local API `PUT /api/orders/12/cancel` with SQLite fixture order `12`.
- Initial status: `shipping`; expected final status: `shipping`; actual final status: `canceled`.
- HTTP status: `200`; response: `{'message': 'Order canceled successfully'}`.
- Execution result: Failed.
