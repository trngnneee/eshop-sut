# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: login.spec.ts >> FR-02 Login UI standards >> TC-LOGIN-009: Nút Đăng nhập phải hiện trạng thái loading/disable khi đang gửi request
- Location: tests\login.spec.ts:133:9

# Error details

```
Error: expect(locator).toBeDisabled() failed

Locator: getByRole('button', { name: /Sign In|Đăng nhập/ })
Expected: disabled
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeDisabled" with timeout 5000ms
  - waiting for getByRole('button', { name: /Sign In|Đăng nhập/ })
    - locator resolved to <button tabindex="1" type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">Sign In</button>
    - unexpected value "enabled"

```

```yaml
- banner:
  - link "EShop":
    - /url: /
  - navigation:
    - link "Giỏ hàng":
      - /url: /cart
    - link "Chào, Test User":
      - /url: /profile
    - button "Thoát"
- main:
  - heading "Danh sách sản phẩm" [level=1]
  - textbox "Tìm kiếm..."
  - button "Tìm"
  - heading "iPhone 15 Pro Max" [level=2]
  - paragraph: 30.000.000 VND
  - link "Xem chi tiết":
    - /url: /product/1
  - button "Thêm vào giỏ"
  - heading "Samsung Galaxy S24 Ultra" [level=2]
  - paragraph: 28.000.000 VND
  - link "Xem chi tiết":
    - /url: /product/2
  - button "Thêm vào giỏ"
  - heading "MacBook Pro M3" [level=2]
  - paragraph: 45.000.000 VND
  - link "Xem chi tiết":
    - /url: /product/3
  - button "Thêm vào giỏ"
  - heading "Tai nghe AirPods Pro 2" [level=2]
  - paragraph: 6.000.000 VND
  - link "Xem chi tiết":
    - /url: /product/4
  - button "Thêm vào giỏ"
  - heading "Bàn phím cơ Keychron Q1" [level=2]
  - paragraph: 4.000.000 VND
  - link "Xem chi tiết":
    - /url: /product/5
  - button "Thêm vào giỏ"
  - heading "Bàn phím cơ Dạ Quang Đặc Biệt" [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/6
  - button "Thêm vào giỏ"
  - heading "Tai nghe \"Pro\" & Co." [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/7
  - button "Thêm vào giỏ"
  - heading "Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout" [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/8
  - button "Thêm vào giỏ"
  - heading "<script>window.__xssFired = true</script>" [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/9
  - button "Thêm vào giỏ"
  - heading "Bulk Item 0" [level=2]
  - paragraph: 10.000 VND
  - link "Xem chi tiết":
    - /url: /product/10
  - button "Thêm vào giỏ"
  - heading "Bulk Item 1" [level=2]
  - paragraph: 10.001 VND
  - link "Xem chi tiết":
    - /url: /product/11
  - button "Thêm vào giỏ"
  - heading "Bulk Item 2" [level=2]
  - paragraph: 10.002 VND
  - link "Xem chi tiết":
    - /url: /product/12
  - button "Thêm vào giỏ"
  - heading "Bulk Item 3" [level=2]
  - paragraph: 10.003 VND
  - link "Xem chi tiết":
    - /url: /product/13
  - button "Thêm vào giỏ"
  - heading "Bulk Item 4" [level=2]
  - paragraph: 10.004 VND
  - link "Xem chi tiết":
    - /url: /product/14
  - button "Thêm vào giỏ"
  - heading "Bulk Item 5" [level=2]
  - paragraph: 10.005 VND
  - link "Xem chi tiết":
    - /url: /product/15
  - button "Thêm vào giỏ"
  - heading "Bulk Item 6" [level=2]
  - paragraph: 10.006 VND
  - link "Xem chi tiết":
    - /url: /product/16
  - button "Thêm vào giỏ"
  - heading "Bulk Item 7" [level=2]
  - paragraph: 10.007 VND
  - link "Xem chi tiết":
    - /url: /product/17
  - button "Thêm vào giỏ"
  - heading "Bulk Item 8" [level=2]
  - paragraph: 10.008 VND
  - link "Xem chi tiết":
    - /url: /product/18
  - button "Thêm vào giỏ"
  - heading "Bulk Item 9" [level=2]
  - paragraph: 10.009 VND
  - link "Xem chi tiết":
    - /url: /product/19
  - button "Thêm vào giỏ"
  - heading "Bulk Item 10" [level=2]
  - paragraph: 10.010 VND
  - link "Xem chi tiết":
    - /url: /product/20
  - button "Thêm vào giỏ"
  - heading "Bulk Item 11" [level=2]
  - paragraph: 10.011 VND
  - link "Xem chi tiết":
    - /url: /product/21
  - button "Thêm vào giỏ"
  - heading "Kim Cương Xanh" [level=2]
  - paragraph: 999.999.999.999 VND
  - link "Xem chi tiết":
    - /url: /product/22
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-092" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/23
  - button "Thêm vào giỏ"
  - heading "Middle Item TC-CART-093" [level=2]
  - paragraph: 77.000 VND
  - link "Xem chi tiết":
    - /url: /product/24
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-102" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/25
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-103" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/26
  - button "Thêm vào giỏ"
  - heading "Price Drift Product" [level=2]
  - paragraph: 1 VND
  - link "Xem chi tiết":
    - /url: /product/28
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-147" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/29
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-148" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/30
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-149" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/31
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-150" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/32
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-151" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/33
  - button "Thêm vào giỏ"
  - heading "Bàn phím cơ Dạ Quang Đặc Biệt" [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/34
  - button "Thêm vào giỏ"
  - heading "Tai nghe \"Pro\" & Co." [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/35
  - button "Thêm vào giỏ"
  - heading "Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout" [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/36
  - button "Thêm vào giỏ"
  - heading "<script>window.__xssFired = true</script>" [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/37
  - button "Thêm vào giỏ"
  - heading "Bulk Item 0" [level=2]
  - paragraph: 10.000 VND
  - link "Xem chi tiết":
    - /url: /product/38
  - button "Thêm vào giỏ"
  - heading "Bulk Item 1" [level=2]
  - paragraph: 10.001 VND
  - link "Xem chi tiết":
    - /url: /product/39
  - button "Thêm vào giỏ"
  - heading "Bulk Item 2" [level=2]
  - paragraph: 10.002 VND
  - link "Xem chi tiết":
    - /url: /product/40
  - button "Thêm vào giỏ"
  - heading "Bulk Item 3" [level=2]
  - paragraph: 10.003 VND
  - link "Xem chi tiết":
    - /url: /product/41
  - button "Thêm vào giỏ"
  - heading "Bulk Item 4" [level=2]
  - paragraph: 10.004 VND
  - link "Xem chi tiết":
    - /url: /product/42
  - button "Thêm vào giỏ"
  - heading "Bulk Item 5" [level=2]
  - paragraph: 10.005 VND
  - link "Xem chi tiết":
    - /url: /product/43
  - button "Thêm vào giỏ"
  - heading "Bulk Item 6" [level=2]
  - paragraph: 10.006 VND
  - link "Xem chi tiết":
    - /url: /product/44
  - button "Thêm vào giỏ"
  - heading "Bulk Item 7" [level=2]
  - paragraph: 10.007 VND
  - link "Xem chi tiết":
    - /url: /product/45
  - button "Thêm vào giỏ"
  - heading "Bulk Item 8" [level=2]
  - paragraph: 10.008 VND
  - link "Xem chi tiết":
    - /url: /product/46
  - button "Thêm vào giỏ"
  - heading "Bulk Item 9" [level=2]
  - paragraph: 10.009 VND
  - link "Xem chi tiết":
    - /url: /product/47
  - button "Thêm vào giỏ"
  - heading "Bulk Item 10" [level=2]
  - paragraph: 10.010 VND
  - link "Xem chi tiết":
    - /url: /product/48
  - button "Thêm vào giỏ"
  - heading "Bulk Item 11" [level=2]
  - paragraph: 10.011 VND
  - link "Xem chi tiết":
    - /url: /product/49
  - button "Thêm vào giỏ"
  - heading "Kim Cương Xanh" [level=2]
  - paragraph: 999.999.999.999 VND
  - link "Xem chi tiết":
    - /url: /product/50
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-092" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/51
  - button "Thêm vào giỏ"
  - heading "Middle Item TC-CART-093" [level=2]
  - paragraph: 77.000 VND
  - link "Xem chi tiết":
    - /url: /product/52
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-102" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/53
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-103" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/54
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-147" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/55
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-148" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/56
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-149" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/57
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-150" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/58
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-151" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/59
  - button "Thêm vào giỏ"
  - heading "Price Drift Product" [level=2]
  - paragraph: 1 VND
  - link "Xem chi tiết":
    - /url: /product/61
  - button "Thêm vào giỏ"
  - heading "Bàn phím cơ Dạ Quang Đặc Biệt" [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/62
  - button "Thêm vào giỏ"
  - heading "Tai nghe \"Pro\" & Co." [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/63
  - button "Thêm vào giỏ"
  - heading "Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout" [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/64
  - button "Thêm vào giỏ"
  - heading "<script>window.__xssFired = true</script>" [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/65
  - button "Thêm vào giỏ"
  - heading "Bulk Item 0" [level=2]
  - paragraph: 10.000 VND
  - link "Xem chi tiết":
    - /url: /product/66
  - button "Thêm vào giỏ"
  - heading "Bulk Item 1" [level=2]
  - paragraph: 10.001 VND
  - link "Xem chi tiết":
    - /url: /product/67
  - button "Thêm vào giỏ"
  - heading "Bulk Item 2" [level=2]
  - paragraph: 10.002 VND
  - link "Xem chi tiết":
    - /url: /product/68
  - button "Thêm vào giỏ"
  - heading "Bulk Item 3" [level=2]
  - paragraph: 10.003 VND
  - link "Xem chi tiết":
    - /url: /product/69
  - button "Thêm vào giỏ"
  - heading "Bulk Item 4" [level=2]
  - paragraph: 10.004 VND
  - link "Xem chi tiết":
    - /url: /product/70
  - button "Thêm vào giỏ"
  - heading "Bulk Item 5" [level=2]
  - paragraph: 10.005 VND
  - link "Xem chi tiết":
    - /url: /product/71
  - button "Thêm vào giỏ"
  - heading "Bulk Item 6" [level=2]
  - paragraph: 10.006 VND
  - link "Xem chi tiết":
    - /url: /product/72
  - button "Thêm vào giỏ"
  - heading "Bulk Item 7" [level=2]
  - paragraph: 10.007 VND
  - link "Xem chi tiết":
    - /url: /product/73
  - button "Thêm vào giỏ"
  - heading "Bulk Item 8" [level=2]
  - paragraph: 10.008 VND
  - link "Xem chi tiết":
    - /url: /product/74
  - button "Thêm vào giỏ"
  - heading "Bulk Item 9" [level=2]
  - paragraph: 10.009 VND
  - link "Xem chi tiết":
    - /url: /product/75
  - button "Thêm vào giỏ"
  - heading "Bulk Item 10" [level=2]
  - paragraph: 10.010 VND
  - link "Xem chi tiết":
    - /url: /product/76
  - button "Thêm vào giỏ"
  - heading "Bulk Item 11" [level=2]
  - paragraph: 10.011 VND
  - link "Xem chi tiết":
    - /url: /product/77
  - button "Thêm vào giỏ"
  - heading "Kim Cương Xanh" [level=2]
  - paragraph: 999.999.999.999 VND
  - link "Xem chi tiết":
    - /url: /product/78
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-092" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/79
  - button "Thêm vào giỏ"
  - heading "Middle Item TC-CART-093" [level=2]
  - paragraph: 77.000 VND
  - link "Xem chi tiết":
    - /url: /product/80
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-102" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/81
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-103" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/82
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-147" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/83
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-148" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/84
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-149" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/85
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-150" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/86
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-151" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/87
  - button "Thêm vào giỏ"
  - heading "Price Drift Product" [level=2]
  - paragraph: 1 VND
  - link "Xem chi tiết":
    - /url: /product/89
  - button "Thêm vào giỏ"
  - heading "Bàn phím cơ Dạ Quang Đặc Biệt" [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/90
  - button "Thêm vào giỏ"
  - heading "Tai nghe \"Pro\" & Co." [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/91
  - button "Thêm vào giỏ"
  - heading "Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout Sản phẩm siêu dài dùng để kiểm tra layout" [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/92
  - button "Thêm vào giỏ"
  - heading "<script>window.__xssFired = true</script>" [level=2]
  - paragraph: 100.000 VND
  - link "Xem chi tiết":
    - /url: /product/93
  - button "Thêm vào giỏ"
  - heading "Bulk Item 0" [level=2]
  - paragraph: 10.000 VND
  - link "Xem chi tiết":
    - /url: /product/94
  - button "Thêm vào giỏ"
  - heading "Bulk Item 1" [level=2]
  - paragraph: 10.001 VND
  - link "Xem chi tiết":
    - /url: /product/95
  - button "Thêm vào giỏ"
  - heading "Bulk Item 2" [level=2]
  - paragraph: 10.002 VND
  - link "Xem chi tiết":
    - /url: /product/96
  - button "Thêm vào giỏ"
  - heading "Bulk Item 3" [level=2]
  - paragraph: 10.003 VND
  - link "Xem chi tiết":
    - /url: /product/97
  - button "Thêm vào giỏ"
  - heading "Bulk Item 4" [level=2]
  - paragraph: 10.004 VND
  - link "Xem chi tiết":
    - /url: /product/98
  - button "Thêm vào giỏ"
  - heading "Bulk Item 5" [level=2]
  - paragraph: 10.005 VND
  - link "Xem chi tiết":
    - /url: /product/99
  - button "Thêm vào giỏ"
  - heading "Bulk Item 6" [level=2]
  - paragraph: 10.006 VND
  - link "Xem chi tiết":
    - /url: /product/100
  - button "Thêm vào giỏ"
  - heading "Bulk Item 7" [level=2]
  - paragraph: 10.007 VND
  - link "Xem chi tiết":
    - /url: /product/101
  - button "Thêm vào giỏ"
  - heading "Bulk Item 8" [level=2]
  - paragraph: 10.008 VND
  - link "Xem chi tiết":
    - /url: /product/102
  - button "Thêm vào giỏ"
  - heading "Bulk Item 9" [level=2]
  - paragraph: 10.009 VND
  - link "Xem chi tiết":
    - /url: /product/103
  - button "Thêm vào giỏ"
  - heading "Bulk Item 10" [level=2]
  - paragraph: 10.010 VND
  - link "Xem chi tiết":
    - /url: /product/104
  - button "Thêm vào giỏ"
  - heading "Bulk Item 11" [level=2]
  - paragraph: 10.011 VND
  - link "Xem chi tiết":
    - /url: /product/105
  - button "Thêm vào giỏ"
  - heading "Kim Cương Xanh" [level=2]
  - paragraph: 999.999.999.999 VND
  - link "Xem chi tiết":
    - /url: /product/106
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-092" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/107
  - button "Thêm vào giỏ"
  - heading "Middle Item TC-CART-093" [level=2]
  - paragraph: 77.000 VND
  - link "Xem chi tiết":
    - /url: /product/108
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-102" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/109
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-103" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/110
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-147" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/111
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-148" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/112
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-149" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/113
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-150" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/114
  - button "Thêm vào giỏ"
  - heading "Qty Check TC-CART-151" [level=2]
  - paragraph: 50.000 VND
  - link "Xem chi tiết":
    - /url: /product/115
  - button "Thêm vào giỏ"
  - heading "Price Drift Product" [level=2]
  - paragraph: 1 VND
  - link "Xem chi tiết":
    - /url: /product/117
  - button "Thêm vào giỏ"
  - heading "Hiển thị 113 sản phẩm" [level=1]
- contentinfo: © 2026 EShop SUT. Dành cho mục đích kiểm thử.
```

# Test source

```ts
  66  | }
  67  | 
  68  | async function submitLogin(page: Page) {
  69  |   await page.getByRole('button', { name: /Sign In|Đăng nhập/ }).click();
  70  | }
  71  | 
  72  | // ---------------------------------------------------------------------------------
  73  | // Shape A - single login attempt, fresh/shared/nonexistent account (31 cases)
  74  | // ---------------------------------------------------------------------------------
  75  | test.describe('FR-02 Login form submission (data-driven)', () => {
  76  |   // Several cases here use the shared seed account (test@eshop.com) with its CORRECT
  77  |   // password and expect success. If a previous run (or a run of another feature's suite
  78  |   // against the same long-lived backend) happened to lock that account within the last
  79  |   // 180s (the real, buggy lock duration — see BUG-FR02-A-02), those cases fail for a
  80  |   // reason that has nothing to do with what they're actually testing. Force it unlocked
  81  |   // once before this describe block runs so the suite's own history can't flake it.
  82  |   test.beforeAll(async () => {
  83  |     await forceLockedUntil('test@eshop.com', null).catch(() => undefined);
  84  |   });
  85  | 
  86  |   for (const c of simpleCases) {
  87  |     test(`${c.caseId}: ${c.description}`, async ({ page, request }, testInfo) => {
  88  |       testInfo.annotations.push({ type: 'Run by', description: STUDENT_ID });
  89  |       if (c.bugRef) testInfo.annotations.push({ type: 'Bug ref', description: c.bugRef });
  90  | 
  91  |       if (c.accountMode === 'fresh') {
  92  |         await deleteUserByEmail(c.registerEmail!).catch(() => undefined);
  93  |         await ensureFreshAccount(request, c.registerEmail!, c.registerPassword!);
  94  |       }
  95  | 
  96  |       let dialogAppeared = false;
  97  |       page.on('dialog', async (dialog) => {
  98  |         dialogAppeared = true;
  99  |         await dialog.dismiss();
  100 |       });
  101 | 
  102 |       await page.goto('/login');
  103 |       await fillLoginForm(page, c.email, c.password);
  104 |       await submitLogin(page);
  105 | 
  106 |       if (c.expectedOutcome === 'success') {
  107 |         // Assertion pattern 1: URL navigation
  108 |         await expect(page).toHaveURL(HOME_URL);
  109 |         // Assertion pattern 2: element visibility
  110 |         await expect(page.getByRole('button', { name: 'Thoát' })).toBeVisible();
  111 |       } else {
  112 |         // Assertion pattern 1 (negated): stays on the login page
  113 |         await expect(page).toHaveURL(/\/login/);
  114 |         if (c.expectedErrorContains) {
  115 |           // Assertion pattern 3: text content
  116 |           await expect(page.getByText(c.expectedErrorContains, { exact: false })).toBeVisible();
  117 |         }
  118 |       }
  119 | 
  120 |       if (c.caseId === 'TC-LOGIN-016') {
  121 |         // Security oracle for the XSS case: no JS dialog must ever fire.
  122 |         expect(dialogAppeared).toBe(false);
  123 |       }
  124 |     });
  125 |   }
  126 | });
  127 | 
  128 | // ---------------------------------------------------------------------------------
  129 | // Shape B - UI/UX/accessibility standards (7 cases)
  130 | // ---------------------------------------------------------------------------------
  131 | test.describe('FR-02 Login UI standards', () => {
  132 |   for (const c of uiCases) {
  133 |     test(`${c.caseId}: ${c.description}`, async ({ page, request }, testInfo) => {
  134 |       testInfo.annotations.push({ type: 'Run by', description: STUDENT_ID });
  135 |       if (c.bugRef) testInfo.annotations.push({ type: 'Bug ref', description: c.bugRef });
  136 | 
  137 |       // Session-lifecycle cases deliberately send a wrong-password attempt or otherwise
  138 |       // touch the account's login_attempts counter - never do that against the shared
  139 |       // seed account (test@eshop.com), or a lockout here breaks every later case in this
  140 |       // describe block that also logs in as that account. Give these a disposable account.
  141 |       const sessionLifecycleCases = ['TC-LOGIN-042', 'TC-LOGIN-043', 'TC-LOGIN-046'];
  142 |       let email = c.email;
  143 |       let password = c.password;
  144 |       if (sessionLifecycleCases.includes(c.caseId)) {
  145 |         email = `${c.caseId.toLowerCase()}@eshop.com`;
  146 |         password = c.caseId === 'TC-LOGIN-046' ? 'WrongPassword1!' : 'Test1234!';
  147 |         await deleteUserByEmail(email).catch(() => undefined);
  148 |         await ensureFreshAccount(request, email, c.caseId === 'TC-LOGIN-046' ? 'ValidPassword1!' : password);
  149 |       }
  150 | 
  151 |       await page.goto('/login');
  152 | 
  153 |       switch (c.check) {
  154 |         case 'form-standards': {
  155 |           await expect(page.getByRole('heading')).toHaveText(/Đăng Nhập|Đăng nhập/i);
  156 |           await expect(page.getByText('Email', { exact: false })).toBeVisible();
  157 |           const pwInput = page.locator('div').filter({ hasText: /^Mật khẩu$/ }).locator('input');
  158 |           await expect(pwInput).toHaveAttribute('type', 'password');
  159 |           await expect(page.getByRole('button', { name: 'Đăng nhập' })).toBeVisible();
  160 |           break;
  161 |         }
  162 |         case 'loading-state': {
  163 |           await fillLoginForm(page, c.email!, c.password!);
  164 |           const button = page.getByRole('button', { name: /Sign In|Đăng nhập/ });
  165 |           await button.click();
> 166 |           await expect(button).toBeDisabled();
      |                                ^ Error: expect(locator).toBeDisabled() failed
  167 |           break;
  168 |         }
  169 |         case 'password-toggle': {
  170 |           const toggle = page.getByRole('button', { name: /hiện mật khẩu|show password|toggle password/i });
  171 |           await expect(toggle).toBeVisible();
  172 |           break;
  173 |         }
  174 |         case 'route-guard': {
  175 |           await fillLoginForm(page, c.email!, c.password!);
  176 |           await submitLogin(page);
  177 |           await expect(page).toHaveURL(HOME_URL);
  178 |           await page.goto('/login');
  179 |           await expect(page).not.toHaveURL(/\/login/);
  180 |           break;
  181 |         }
  182 |         case 'no-credentials-in-url': {
  183 |           await fillLoginForm(page, c.email!, c.password!);
  184 |           await submitLogin(page);
  185 |           await expect(page).not.toHaveURL(new RegExp(c.password!.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
  186 |           break;
  187 |         }
  188 |         case 'tab-order': {
  189 |           const emailInput = page.locator('div').filter({ hasText: /^Username$/ }).locator('input');
  190 |           await page.keyboard.press('Tab');
  191 |           await expect(emailInput).toBeFocused();
  192 |           break;
  193 |         }
  194 |         case 'autofill-attributes': {
  195 |           const emailInput = page.locator('div').filter({ hasText: /^Username$/ }).locator('input');
  196 |           await expect(emailInput).toHaveAttribute('autocomplete', 'username');
  197 |           break;
  198 |         }
  199 |         case 'offline-submit': {
  200 |           await fillLoginForm(page, c.email!, c.password!);
  201 |           await page.context().setOffline(true);
  202 |           await submitLogin(page);
  203 |           await page.waitForTimeout(1000);
  204 |           await expect(page.locator('body')).toBeVisible();
  205 |           await page.context().setOffline(false);
  206 |           break;
  207 |         }
  208 |         case 'session-persist-reload': {
  209 |           await fillLoginForm(page, email!, password!);
  210 |           await submitLogin(page);
  211 |           await expect(page).toHaveURL(HOME_URL);
  212 |           // Assertion pattern: reload the page and confirm the session survived it -
  213 |           // token lives in localStorage (not React state), so a real reload rehydrates it.
  214 |           await page.reload();
  215 |           await expect(page.getByRole('button', { name: 'Thoát' })).toBeVisible();
  216 |           const tokenAfterReload = await page.evaluate(() => localStorage.getItem('token'));
  217 |           expect(tokenAfterReload).toBeTruthy();
  218 |           break;
  219 |         }
  220 |         case 'logout-clears-session': {
  221 |           await fillLoginForm(page, email!, password!);
  222 |           await submitLogin(page);
  223 |           await expect(page).toHaveURL(HOME_URL);
  224 |           await page.getByRole('button', { name: 'Thoát' }).click();
  225 |           // Assertion pattern 1: UI reverts to the logged-out link
  226 |           await expect(page.getByRole('link', { name: 'Đăng nhập' })).toBeVisible();
  227 |           // Assertion pattern 2: the token is actually gone from storage, not just hidden in the UI
  228 |           const tokenAfterLogout = await page.evaluate(() => localStorage.getItem('token'));
  229 |           expect(tokenAfterLogout).toBeNull();
  230 |           break;
  231 |         }
  232 |         case 'invalid-token-auto-logout': {
  233 |           await page.goto('/');
  234 |           await page.evaluate(() => localStorage.setItem('token', 'not-a-real-jwt-string'));
  235 |           await page.reload();
  236 |           // The AuthContext effect fires GET /api/users/me with the bad token, gets a
  237 |           // non-2xx, and calls logout() - the header must show the guest state again.
  238 |           await expect(page.getByRole('link', { name: 'Đăng nhập' })).toBeVisible();
  239 |           const tokenAfter = await page.evaluate(() => localStorage.getItem('token'));
  240 |           expect(tokenAfter).toBeNull();
  241 |           break;
  242 |         }
  243 |         case 'password-autocomplete': {
  244 |           const pwInput = page.locator('div').filter({ hasText: /^Mật khẩu$/ }).locator('input');
  245 |           await expect(pwInput).toHaveAttribute('autocomplete', 'current-password');
  246 |           break;
  247 |         }
  248 |         case 'loading-resets-after-failure': {
  249 |           await fillLoginForm(page, email!, password!);
  250 |           const button = page.getByRole('button', { name: /Sign In|Đăng nhập/ });
  251 |           await button.click();
  252 |           // Assertion pattern: after the failed request settles, the button must be
  253 |           // interactive again (not stuck disabled forever) so the user can retry.
  254 |           await expect(button).toBeEnabled();
  255 |           await expect(page).toHaveURL(/\/login/);
  256 |           break;
  257 |         }
  258 |         case 'forged-token-rejected': {
  259 |           // A structurally valid JWT (3 dot-separated base64url parts) signed with the
  260 |           // wrong secret - jwt.verify() on the backend must reject it just like garbage.
  261 |           const header = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64url');
  262 |           const payload = Buffer.from(JSON.stringify({ id: 1, email: 'forged@eshop.com', exp: Math.floor(Date.now() / 1000) + 3600 })).toString('base64url');
  263 |           const forgedToken = `${header}.${payload}.forged-signature-not-valid`;
  264 |           await page.goto('/');
  265 |           await page.evaluate((t) => localStorage.setItem('token', t), forgedToken);
  266 |           await page.reload();
```