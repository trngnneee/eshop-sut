# TC-LOGIN-BVA-012: Kiểm tra Password biên độ dài max + 1 (65 ký tự)

## Requirement ID
FR-02, FR-22

## Module / Test type / Technique
Login / Boundary Value Analysis (BVA)

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu | PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP! |

## Test steps
1. Nhập email.
2. Nhập mật khẩu dài 65 ký tự.
3. Nhấn 'Đăng nhập'.

## Expected result
- Hệ thống báo lỗi độ dài mật khẩu vượt quá giới hạn tối đa cho phép.

## Status / Related bugs
Pass / None
