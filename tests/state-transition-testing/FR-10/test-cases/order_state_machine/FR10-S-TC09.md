# FR10-S-TC09: Từ chối Admin chuyển tắt confirmed sang delivered

## Requirement ID
FR-10

## Module / Test type / Technique
Order State Machine / Functional / State Transition Testing

## State transition coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Transition / Class ID | S-INVALID-02 |
| State variable | `status` |
| Actor | admin |
| Flow type | Invalid transition |
| Covered guard/rule | Invalid transition: confirmed -> delivered skips shipping |
| Covered requirement | Mọi chuyển đổi không hợp lệ phải trả về lỗi với thông báo phù hợp. Source: README.md:141-162. |

## Preconditions
- Có đơn hàng hợp lệ đang ở trạng thái `confirmed`.
- Tài khoản `admin` đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | admin |
| Current state | confirmed |
| Action / Event | Update order status |
| Requested state | delivered |
| Endpoint / UI flow | PUT /api/admin/orders/:id/status |
| Body / Input | {"status": "delivered"} |
| Entity ID | {existing_order_id} |

## Test steps
1. Chuẩn bị một đơn hàng đang ở trạng thái `confirmed`.
2. Đăng nhập bằng tài khoản `admin` hợp lệ.
3. Gửi request `PUT /api/admin/orders/:id/status` với body `{"status": "delivered"}`.
4. Tải lại thông tin đơn hàng sau khi request hoàn tất.

## Expected result
- Hệ thống trả về HTTP 400 với thông báo lỗi phù hợp.
- Trạng thái đơn hàng vẫn giữ nguyên là `confirmed`.

## Status / Related bugs
Passed / None

## Actual result
- Executed by: Đặng Trường Nguyên.
- Execution interface: Local API `PUT /api/admin/orders/9/status` with SQLite fixture order `9`.
- Initial status: `confirmed`; expected final status: `confirmed`; actual final status: `confirmed`.
- HTTP status: `400`; response: `{'error': 'Invalid state transition from confirmed to delivered'}`.
- Execution result: Passed.
