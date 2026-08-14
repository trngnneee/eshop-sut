# 05 — Endurance & Memory Threshold Analysis (Task 1)

> **Học phần:** Kiểm thử Phần mềm (HW05)  
> **Sinh viên:** Khoa (MSSV: **23127207**) · **SUT:** EShop  
> **Kịch bản phân tích:** **Endurance / Soak Test** (30 VU, 12 phút / 720 giây)  

---

## 1. Dữ liệu Thực nghiệm từ Giám sát Bộ nhớ

Từ file log tài nguyên thực tế `results/endurance/resource-endurance.csv` và `summary.json`:

| Chỉ số bộ nhớ | Giá trị đo được |
|:---|---:|
| **RAM Private tại $t=0$ (Khởi động):** | **60.30 MB** |
| **RAM Private tại $t=12\text{ min}$ (Kết thúc):** | **137.39 MB** |
| **Trần RAM Private cao nhất (Memory Ceiling):** | **172.49 MB** |
| **Tăng trưởng tuyệt đối ($\Delta\text{RAM}$):** | **+77.09 MB** |
| **Thời lượng kiểm thử ($\Delta t$):** | **11.95 phút** (~717 giây) |
| **Độ dốc rò rỉ bộ nhớ (Memory Leak Slope):** | **`6.45 MB / phút`** (~`387.0 MB / giờ`) |

---

## 2. Mô hình Tính toán Thời gian Sập Hệ thống (Time to Out-of-Memory — TT-OOM)

Giả định hệ thống chịu tải liên tục ở mức **30 VU** (tương đương ~18.6 req/s), công thức ngoại suy thời gian chạm ngưỡng giới hạn bộ nhớ:

$$\text{Time to OOM} = \frac{\text{Memory Limit} - \text{Initial RAM}}{\text{Leak Rate}}$$

### 2.1 Bảng Dự báo Thời gian Chết Hệ thống (OOM Projection Table)

| Môi trường triển khai | Hạn mức Bộ nhớ (RAM Limit) | Thời gian hoạt động còn lại trước khi OOM | Dự báo Trạng thái |
|:---|:---:|:---:|:---|
| **Micro Container (Docker)** | **512 MB** | $\frac{512 - 60.3}{6.45} \approx \mathbf{70\text{ phút}}$ (~**1.17 giờ**) | 💥 **CRITICAL**: Server crash ngay trong phiên làm việc buổi sáng |
| **Small Cloud Instance (AWS/GCP)** | **1,024 MB (1 GB)** | $\frac{1024 - 60.3}{6.45} \approx \mathbf{149\text{ phút}}$ (~**2.49 giờ**) | 💥 **HIGH**: Server sập 3–4 lần mỗi ngày |
| **Standard Node.js V8 Heap** | **2,048 MB (2 GB)** | $\frac{2048 - 60.3}{6.45} \approx \mathbf{308\text{ phút}}$ (~**5.14 giờ**) | ⚠️ **MEDIUM**: Server không thể sống qua 1 ngày mà không restart |
| **Dedicated Server (High RAM)** | **4,096 MB (4 GB)** | $\frac{4096 - 60.3}{6.45} \approx \mathbf{625\text{ phút}}$ (~**10.42 giờ**) | ⚠️ Server suy thoái p95 nghiêm trọng sau vài giờ |

---

## 3. Phân tích Nguyên nhân Gốc rễ trong Mã nguồn (Root Cause Analysis)

Khi kiểm tra mã nguồn `backend/server.js`:

```javascript
// backend/server.js:14
const userCarts = {};

// backend/server.js:293 - Add to cart
app.post("/api/cart", authenticateToken, (req, res) => {
  const userId = req.user.id;
  if (!userCarts[userId]) {
    userCarts[userId] = [];
  }
  userCarts[userId].push(req.body); // <-- LƯU TRỮ VĨNH VIỄN TRÊN HEAP
  res.json({ message: "Added to cart" });
});

// backend/server.js:306 - Checkout
app.post("/api/checkout", authenticateToken, (req, res) => {
  const userId = req.user.id;
  // ... Thực hiện ghi đơn hàng vào SQLite ...
  // THIẾU: Không hề có dòng `delete userCarts[userId]` hay `userCarts[userId] = []` !
  res.json({ message: "Checkout successful", orderId: this.lastID });
});
```

### Cơ chế Gây nghẽn:
1. Đối tượng toàn cục `userCarts` đóng vai trò là một **GC Root** không bao giờ bị thu hồi.
2. Mỗi lần khách hàng thêm hàng và thanh toán, đối tượng payload giỏ hàng tiếp tục được giữ chặt trong bộ nhớ heap.
3. Khi heap phình to, thuật toán **Mark-Sweep / Compact** của V8 Garbage Collector phải duyệt qua hàng trăm nghìn đối tượng mồ côi, làm tăng tần suất và thời lượng của **Stop-The-World GC Pauses**.
4. Điều này giải thích trực tiếp tại sao trong kịch bản Endurance, p95 ở lát cắt `0-120s` chỉ là **47 ms**, nhưng đến lát cắt `600-720s` đã tăng vọt lên **2,112 ms** dù số VU và tải mạng hoàn toàn không thay đổi!

---

## 4. Giải pháp Khắc phục (Proposed Solution & Code Fix)

### 4.1 Sửa đổi Mã nguồn Backend

```diff
--- a/backend/server.js
+++ b/backend/server.js
@@ -308,6 +308,8 @@ app.post("/api/checkout", authenticateToken, (req, res) => {
         function (err) {
           if (err) return res.status(500).json({ error: err.message });
+          // Giải phóng giỏ hàng khỏi bộ nhớ sau khi thanh toán thành công
+          delete userCarts[userId];
           res.json({ message: "Order placed successfully", orderId: this.lastID });
         }
       );
```

### 4.2 Thiết lập Bộ nhớ đệm có Thời hạn sống (TTL / LRU Cache)
Đối với các giỏ hàng bị bỏ dở (abandoned carts), thay thế biến `Object` thuần túy bằng `lru-cache` với cấu hình TTL tối đa 24 giờ và dung lượng tối đa 10,000 giỏ hàng:

```javascript
const { LRUCache } = require('lru-cache');
const userCarts = new LRUCache({
  max: 10000,
  ttl: 1000 * 60 * 60 * 24 // 24 giờ
});
```
