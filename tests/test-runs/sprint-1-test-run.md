# Test Run - Sprint 1

**Ngày thực hiện**: 25/06/2026  
**Người thực hiện**: Thịnh
**Môi trường thử nghiệm**: Local Backend API & Frontend Web (demo)

| Test Case ID                                        | Module | Tester | Result | Related Bug                  | Note                                                                   |
| :-------------------------------------------------- | :----- | :----- | :----- | :--------------------------- | :--------------------------------------------------------------------- |
| [TC-COUPON-001](../test-cases/coupon/TC-COUPON-001.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-001](../bug-reports/BUG-COUPON-001.md) | Từ chối áp dụng khi đơn hàng đạt chính xác 300k (Strict inequality bug) và tính sai công thức |
| [TC-COUPON-002](../test-cases/coupon/TC-COUPON-002.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác khi đơn hàng 299,999 ₫ |
| [TC-COUPON-003](../test-cases/coupon/TC-COUPON-003.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-002](../bug-reports/BUG-COUPON-002.md) | Số tiền giảm giá tính ra số âm và tổng tiền thanh toán tăng vọt |
| [TC-COUPON-004](../test-cases/coupon/TC-COUPON-004.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-001](../bug-reports/BUG-COUPON-001.md) | Từ chối áp dụng khi đơn hàng đạt chính xác 500k |
| [TC-COUPON-005](../test-cases/coupon/TC-COUPON-005.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác khi đơn hàng 499,999 ₫ |
| [TC-COUPON-006](../test-cases/coupon/TC-COUPON-006.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác đối với mã hết hạn |
| [TC-COUPON-007](../test-cases/coupon/TC-COUPON-007.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác đối với mã không tồn tại |
| [TC-COUPON-008](../test-cases/coupon/TC-COUPON-008.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-003](../bug-reports/BUG-COUPON-003.md) | Áp dụng thành công dù không có JWT Token do thiếu authenticateToken |
| [TC-COUPON-009](../test-cases/coupon/TC-COUPON-009.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác khi số lần dùng đạt giới hạn (2 lần) |
| [TC-COUPON-010](../test-cases/coupon/TC-COUPON-010.md) | Coupon | Thịnh   | Pass   | None                         | Áp dụng thành công khi số lần dùng là 1 < 2 |
| [TC-COUPON-011](../test-cases/coupon/TC-COUPON-011.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác khi mã tồn tại nhưng bị tắt (is_active = 0) |
| [TC-COUPON-012](../test-cases/coupon/TC-COUPON-012.md) | Coupon | Thịnh   | Fail   | None | Từ chối chính xác khi mã quá hạn |
| [TC-COUPON-013](../test-cases/coupon/TC-COUPON-013.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác khi số lần sử dụng trong DB lớn hơn mức tối đa |
| [TC-COUPON-014](../test-cases/coupon/TC-COUPON-014.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác khi mã coupon để trống |
| [TC-COUPON-015](../test-cases/coupon/TC-COUPON-015.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác khi mã coupon chứa ký tự đặc biệt |
| [TC-COUPON-016](../test-cases/coupon/TC-COUPON-016.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-005](../bug-reports/BUG-COUPON-005.md) | Báo sai thông báo lỗi (đơn hàng chưa đủ tối thiểu) khi total_amount là chuỗi |
| [TC-COUPON-017](../test-cases/coupon/TC-COUPON-017.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-005](../bug-reports/BUG-COUPON-005.md) | Báo sai thông báo lỗi khi total_amount là null |
| [TC-COUPON-018](../test-cases/coupon/TC-COUPON-018.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-005](../bug-reports/BUG-COUPON-005.md) | Báo sai thông báo lỗi khi total_amount là số âm |
