# TC-LOGIN-BVA-011: Kiểm tra Password biên độ dài max (64 ký tự)

## Requirement ID
FR-02

## Module / Test type / Technique
Login / Boundary Value Analysis (BVA)

## Preconditions
- Đã đăng ký tài khoản có mật khẩu đúng dài đúng 64 ký tự.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Mật khẩu | PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP! |

## Test steps
1. Nhập email.
2. Nhập mật khẩu đúng dài 64 ký tự.
3. Nhấn 'Đăng nhập'.

## Expected result
- Hệ thống chấp nhận và đăng nhập thành công.

## Status / Related bugs
Not Run / None
