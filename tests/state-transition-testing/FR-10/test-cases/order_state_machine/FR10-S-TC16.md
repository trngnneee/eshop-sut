# FR10-S-TC16: Từ chối Admin chuyển canceled sang delivered

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / State Transition Testing

## State transition coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Transition / Class ID | S-INVALID-09 |
| State variable | `status` |
| Actor | admin |
| Flow type | Final-state rejection |
| Covered guard/rule | Invalid final-state transition: canceled -> delivered by admin |
| Covered requirement | `delivered` và `canceled` là final states, không được chuyển sang trạng thái khác. Source: README.md:141-162. |

## Preconditions
- Có đơn hàng hợp lệ đang ở trạng thái `canceled`.
- Tài khoản `admin` đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Current state | canceled |
| Action / Event | Update order status |
| Requested state | delivered |
| Endpoint / UI flow | PUT /api/admin/orders/:id/status |
| Body / Input | {"status": "delivered"} |
| Entity ID | {existing_order_id} |

## Test steps
1. Chuẩn bị một đơn hàng đang ở trạng thái `canceled`.
2. Đăng nhập bằng tài khoản `admin` hợp lệ.
3. Gửi request `PUT /api/admin/orders/:id/status` với body `{"status": "delivered"}`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result
- Hệ thống trả về HTTP 400 với thông báo lỗi phù hợp.
- Trạng thái đơn hàng vẫn giữ nguyên là `canceled`.

## Status / Related bugs
Failed / BUG-FR10-S-02

## Actual result
- Executed by: Đặng Trường Nguyên.
- Execution interface: Local API `PUT /api/admin/orders/16/status` with SQLite fixture order `16`.
- Initial status: `canceled`; expected final status: `canceled`; actual final status: `delivered`.
- HTTP status: `200`; response: `{'message': 'Order status updated'}`.
- Execution result: Failed.
