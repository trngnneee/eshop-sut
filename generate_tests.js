const fs = require('fs');
const path = require('path');

const testCasesDir = path.join(__dirname, 'tests', 'test-cases', 'ORDER-HISTORY');
if (!fs.existsSync(testCasesDir)) {
    fs.mkdirSync(testCasesDir, { recursive: true });
}

const template = (id, objective, preconditions, data, steps, expected) => `# Test Case Template

## Test Case ID
${id}

## Feature
Xem lịch sử đơn hàng (User)

## Requirement Reference
FR-11

## Testing Technique
Domain Testing / Boundary Value Analysis

## Test Objective
${objective}

## Preconditions
${preconditions}

## Test Data
${data}

## Test Steps
${steps}

## Expected Result
${expected}

## Actual Result
(Chưa thực thi)

## Status
NOT EXECUTED

## Bug Reference
`;

const testCases = [
  {
    id: 'TC-ORDERHISTORY-001',
    objective: 'Kiểm tra người dùng chưa đăng nhập không thể xem lịch sử đơn hàng',
    preconditions: 'Người dùng chưa đăng nhập vào hệ thống',
    data: '| Parameter | Value |\n|-|-|\n| Trạng thái đăng nhập | False |',
    steps: '1. Mở trang web EShop.\n2. Cố gắng truy cập trực tiếp vào URL trang Lịch sử đơn hàng (VD: /order-history).',
    expected: 'Hệ thống chặn truy cập và chuyển hướng người dùng về trang Đăng nhập kèm theo thông báo lỗi yêu cầu đăng nhập.'
  },
  {
    id: 'TC-ORDERHISTORY-002',
    objective: 'Kiểm tra hiển thị khi người dùng không có đơn hàng nào (BVA: 0 đơn hàng)',
    preconditions: 'Người dùng đã đăng nhập, tài khoản chưa từng đặt hàng',
    data: '| Parameter | Value |\n|-|-|\n| Số lượng đơn hàng | 0 |',
    steps: '1. Đăng nhập vào hệ thống với tài khoản hợp lệ.\n2. Điều hướng đến trang Lịch sử đơn hàng.',
    expected: 'Giao diện hiển thị thông báo "Chưa có đơn hàng nào" (Empty state) kèm theo icon minh họa và nút "Tiếp tục mua sắm".'
  },
  {
    id: 'TC-ORDERHISTORY-003',
    objective: 'Kiểm tra hiển thị khi người dùng có ít nhất 1 đơn hàng (BVA: 1 đơn hàng)',
    preconditions: 'Người dùng đã đăng nhập, tài khoản có đúng 1 đơn hàng',
    data: '| Parameter | Value |\n|-|-|\n| Số lượng đơn hàng | 1 |',
    steps: '1. Đăng nhập vào hệ thống.\n2. Điều hướng đến trang Lịch sử đơn hàng.',
    expected: 'Hiển thị danh sách gồm 1 đơn hàng với đầy đủ thông tin: Mã đơn, Ngày đặt, Tổng tiền, Trạng thái.'
  },
  {
    id: 'TC-ORDERHISTORY-004',
    objective: 'Kiểm tra người dùng không thể xem đơn hàng của người khác',
    preconditions: 'Người dùng A đã đăng nhập, người dùng B có 1 đơn hàng',
    data: '| Parameter | Value |\n|-|-|\n| ID người dùng | User A |\n| Đơn hàng của | User B |',
    steps: '1. Đăng nhập bằng tài khoản User A.\n2. Truy cập trang Lịch sử đơn hàng.\n3. Nếu có API hoặc URL chi tiết đơn hàng của User B, thử truy cập trực tiếp bằng ID đơn hàng của B.',
    expected: 'Ở bước 2, chỉ hiển thị đơn hàng của User A. Ở bước 3, hệ thống trả về lỗi 403 Forbidden hoặc không tìm thấy (404).'
  },
  {
    id: 'TC-ORDERHISTORY-005',
    objective: 'Kiểm tra hiển thị đầy đủ và đúng định dạng các trường thông tin',
    preconditions: 'Người dùng đã đăng nhập và có ít nhất 1 đơn hàng',
    data: '| Parameter | Value |\n|-|-|\n| Dữ liệu đơn hàng | Có giá trị |',
    steps: '1. Đăng nhập vào hệ thống.\n2. Chuyển đến trang Lịch sử đơn hàng.\n3. Kiểm tra các cột dữ liệu hiển thị trên danh sách.',
    expected: 'Mã đơn hiển thị rõ ràng. Ngày đặt đúng định dạng (VD: dd/mm/yyyy). Tổng tiền có định dạng phân cách hàng nghìn và kèm ký hiệu ₫. Trạng thái hiện tại rõ ràng.'
  },
  {
    id: 'TC-ORDERHISTORY-006',
    objective: 'Kiểm tra hiển thị trạng thái "pending" (chờ xác nhận)',
    preconditions: 'Người dùng đã đăng nhập và có 1 đơn hàng vừa đặt thành công (trạng thái pending)',
    data: '| Parameter | Value |\n|-|-|\n| Trạng thái | pending |',
    steps: '1. Truy cập Lịch sử đơn hàng.\n2. Tìm đơn hàng có trạng thái "pending".\n3. Kiểm tra text và màu sắc của trạng thái.',
    expected: 'Trạng thái hiển thị là "Chờ xác nhận" (hoặc tương đương bằng tiếng Việt), có màu sắc nổi bật (VD: màu cam/vàng).'
  },
  {
    id: 'TC-ORDERHISTORY-007',
    objective: 'Kiểm tra hiển thị trạng thái "confirmed" (đã xác nhận)',
    preconditions: 'Người dùng có 1 đơn hàng đã được Admin xác nhận (trạng thái confirmed)',
    data: '| Parameter | Value |\n|-|-|\n| Trạng thái | confirmed |',
    steps: '1. Truy cập Lịch sử đơn hàng.\n2. Tìm đơn hàng có trạng thái "confirmed".\n3. Kiểm tra text và màu sắc của trạng thái.',
    expected: 'Trạng thái hiển thị là "Đã xác nhận", có màu sắc phân biệt (VD: màu xanh dương).'
  },
  {
    id: 'TC-ORDERHISTORY-008',
    objective: 'Kiểm tra hiển thị trạng thái "shipping" (đang giao)',
    preconditions: 'Người dùng có 1 đơn hàng đang trong quá trình vận chuyển (trạng thái shipping)',
    data: '| Parameter | Value |\n|-|-|\n| Trạng thái | shipping |',
    steps: '1. Truy cập Lịch sử đơn hàng.\n2. Tìm đơn hàng có trạng thái "shipping".\n3. Kiểm tra text và màu sắc của trạng thái.',
    expected: 'Trạng thái hiển thị là "Đang giao", có màu sắc phân biệt (VD: màu xanh lơ/xanh lam).'
  },
  {
    id: 'TC-ORDERHISTORY-009',
    objective: 'Kiểm tra hiển thị trạng thái "delivered" (đã giao)',
    preconditions: 'Người dùng có 1 đơn hàng đã hoàn tất (trạng thái delivered)',
    data: '| Parameter | Value |\n|-|-|\n| Trạng thái | delivered |',
    steps: '1. Truy cập Lịch sử đơn hàng.\n2. Tìm đơn hàng có trạng thái "delivered".\n3. Kiểm tra text và màu sắc của trạng thái.',
    expected: 'Trạng thái hiển thị là "Đã giao" hoặc "Hoàn thành", có màu sắc tích cực (VD: màu xanh lá).'
  },
  {
    id: 'TC-ORDERHISTORY-010',
    objective: 'Kiểm tra hiển thị trạng thái "canceled" (đã hủy)',
    preconditions: 'Người dùng có 1 đơn hàng đã bị hủy (trạng thái canceled)',
    data: '| Parameter | Value |\n|-|-|\n| Trạng thái | canceled |',
    steps: '1. Truy cập Lịch sử đơn hàng.\n2. Tìm đơn hàng có trạng thái "canceled".\n3. Kiểm tra text và màu sắc của trạng thái.',
    expected: 'Trạng thái hiển thị là "Đã hủy", có màu sắc cảnh báo (VD: màu đỏ/xám).'
  }
];

for (const tc of testCases) {
  const fileContent = template(tc.id, tc.objective, tc.preconditions, tc.data, tc.steps, tc.expected);
  fs.writeFileSync(path.join(testCasesDir, `${tc.id}.md`), fileContent, 'utf8');
}
console.log('Created 10 test cases.');
