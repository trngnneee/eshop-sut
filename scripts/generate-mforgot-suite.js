/**
 * Generate TC-MFORGOT-SUP-001..007 and port BVA TC-MFORGOT-021..044 from web forgot suite.
 */
const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, '../tests/test-cases/forgot');
const dstDir = path.join(__dirname, '../tests/test-cases/forgot-mobile');
const nav =
  'Mở Mobile App, vào màn hình Đăng nhập, bấm "Quên mật khẩu?" để vào màn hình Quên Mật Khẩu';
const navStep1 = `${nav} (Bước 1)`;
const mobilePre =
  '- Mobile App (React Native + Expo) đang chạy và kết nối Backend API tại IP LAN máy chủ';

function transformBva(content) {
  let c = content
    .replace(/TC-FORGOT-/g, 'TC-MFORGOT-')
    .replace(/^FR-03$/m, 'FR-22')
    .replace(/Forgot Password \//g, 'Forgot Password (Mobile) /');

  c = c.replace(/(## Preconditions\n)([\s\S]*?)(## Test data)/, (m, h, pre, rest) => {
    const lines = pre.trim().split('\n').filter((l) => l.trim());
    if (!lines.some((l) => l.includes('Mobile App'))) lines.unshift(mobilePre);
    return `${h}${lines.join('\n')}\n\n${rest}`;
  });

  c = c.replace(/Truy cập trang Quên mật khẩu \(Bước 1\)\./g, `${navStep1}.`);
  c = c.replace(/Truy cập trang Quên mật khẩu\./g, `${nav}.`);
  c = c.replace(/trang Quên mật khẩu/g, 'màn hình Quên Mật Khẩu trên Mobile App');
  c = c.replace(/trang Đăng nhập/g, 'màn hình Đăng nhập trên Mobile App');
  c = c.replace(/## Status \/ Related bugs[\s\S]*$/m, '## Status / Related bugs\nNot Run / None');

  if (c.includes('Xác nhận mật khẩu') && !c.includes('**Lưu ý:**')) {
    c = c.replace(
      '## Test steps',
      '## Test steps\n> **Lưu ý:** Theo FR-22, Bước 2 phải có trường Xác nhận mật khẩu mới (nếu có trên UI).'
    );
  }
  return c;
}

const supFiles = {
  'TC-MFORGOT-SUP-001.md': `# TC-MFORGOT-SUP-001: API sinh OTP đúng 6 chữ số + label UI Mobile

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Supplementary

## Preconditions
${mobilePre}
- Tài khoản \`test@eshop.com\` tồn tại
- Backend API đang chạy tại \`http://localhost:3000\`

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |

## Test steps
1. Gửi \`POST /api/forgot-password\` với body \`{"email":"test@eshop.com"}\`.
2. Đọc trường \`resetToken\` trong response JSON; kiểm tra regex \`^\\\\d{6}$\`.
3. ${navStep1}.
4. Nhập Email \`test@eshop.com\`, bấm "Lấy mã OTP", chuyển sang Bước 2.
5. Kiểm tra label OTP trên màn hình Mobile (phải mô tả **6 số**, không phải 4).

## Expected result
- API: \`resetToken\` gồm **đúng 6 chữ số**.
- Mobile UI: label hiển thị "Mã OTP (6 số)" hoặc tương đương; không ghi "4 số".

## Sub-domains covered
GAP-02 — OTP length contract (API + Mobile label)

## Type
Valid

## Status / Related bugs
Not Run / #6
`,
  'TC-MFORGOT-SUP-002.md': `# TC-MFORGOT-SUP-002: Demo hiển thị OTP trên màn hình Mobile (FR-03)

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Supplementary

## Preconditions
${mobilePre}
- Tài khoản \`test@eshop.com\` tồn tại

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |

## Test steps
1. ${navStep1}.
2. Nhập Email \`test@eshop.com\`, bấm "Lấy mã OTP".
3. Quan sát hộp thông báo / message sau Bước 1 trên Mobile.
4. So sánh với giá trị \`resetToken\` từ API (nếu cần).

## Expected result
- Môi trường demo: màn hình hiển thị **trực tiếp** mã OTP 6 chữ số (ví dụ "Mã OTP của bạn là: 123456").
- Không chỉ hiển thị message chung không chứa mã.

## Sub-domains covered
GAP-03 — Demo OTP on screen

## Type
Valid

## Status / Related bugs
Not Run / #6
`,
  'TC-MFORGOT-SUP-003.md': `# TC-MFORGOT-SUP-003: Backend từ chối mật khẩu yếu khi reset (Mobile flow)

## Requirement ID
FR-22 (FR-01 password rules)

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Supplementary

## Preconditions
- Đã lấy OTP hợp lệ cho \`test@eshop.com\` qua API (dùng chung backend với Mobile)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| newPassword | weakpass |

## Test steps
1. Gọi \`POST /api/reset-password\` với email, OTP hợp lệ và \`newPassword: "weakpass"\`.
2. Quan sát HTTP status và body.
3. (Tùy chọn) Lặp qua Mobile Bước 2 với cùng OTP và mật khẩu yếu.

## Expected result
- API trả lỗi 4xx và **không** cập nhật mật khẩu (theo FR-01).
- Mobile không cho hoàn tất reset với mật khẩu yếu.

## Sub-domains covered
GAP-04 — server-side password validation

## Type
Invalid

## Status / Related bugs
Not Run / #10
`,
  'TC-MFORGOT-SUP-004.md': `# TC-MFORGOT-SUP-004: OTP không thể tái sử dụng sau reset thành công

## Requirement ID
FR-22, SEC-07

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Supplementary

## Preconditions
- Đã reset mật khẩu thành công một lần với OTP \`X\` (qua Mobile hoặc API)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP (lần 2) | X (cùng mã đã dùng) |

## Test steps
1. Hoàn tất reset mật khẩu thành công với OTP \`X\`.
2. Gọi lại \`POST /api/reset-password\` với cùng email, OTP \`X\`, và mật khẩu mới khác.

## Expected result
- Lần 2 bị từ chối (OTP đã vô hiệu / \`reset_token\` cleared).

## Sub-domains covered
GAP-05 — OTP one-time use

## Type
Invalid

## Status / Related bugs
Not Run / None
`,
  'TC-MFORGOT-SUP-005.md': `# TC-MFORGOT-SUP-005: Bước 2 phải có trường Xác nhận mật khẩu mới

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Supplementary

## Preconditions
${mobilePre}
- Đã hoàn thành Bước 1 với Email \`test@eshop.com\`

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| (Không áp dụng) | — |

## Test steps
1. ${nav}; hoàn thành Bước 1 với \`test@eshop.com\`.
2. Trên Bước 2, đếm các trường nhập mật khẩu (\`secureTextEntry\`) hoặc tìm label "Xác nhận mật khẩu".

## Expected result
- Có **hai** trường mật khẩu: "Mật khẩu mới" và "Xác nhận mật khẩu mới".
- Hiện tại SUT chỉ có một trường → Fail.

## Sub-domains covered
GAP-06 — confirm-password field present

## Type
Valid

## Status / Related bugs
Not Run / #4
`,
  'TC-MFORGOT-SUP-006.md': `# TC-MFORGOT-SUP-006: Lỗi validation hiển thị trên nút submit (FR-22) — không dùng Alert

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Supplementary

## Preconditions
${mobilePre}
- Đang ở Bước 2 sau khi lấy OTP hợp lệ

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ] |
| Mật khẩu mới | weakpass |

## Test steps
1. Hoàn thành Bước 1, vào Bước 2.
2. Nhập OTP hợp lệ và mật khẩu yếu \`weakpass\`.
3. Bấm "Đặt lại mật khẩu".
4. Quan sát: lỗi phải là **inline text phía trên nút**, không phải \`Alert.alert\` popup.

## Expected result
- Thông báo lỗi xuất hiện inline (ví dụ \`errorBoxText\`) **trên** nút submit theo FR-22.
- Không dùng dialog Alert làm phản hồi validation chính.

## Sub-domains covered
GAP-07 — FR-22 error placement on Mobile

## Type
Invalid

## Status / Related bugs
Not Run / None
`,
  'TC-MFORGOT-SUP-007.md': `# TC-MFORGOT-SUP-007: Mật khẩu với ký tự đặc biệt ngoài whitelist FR-01

## Requirement ID
FR-22 (FR-01)

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Supplementary

## Preconditions
${mobilePre}
- Đang ở Bước 2 với OTP hợp lệ

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ] |
| Mật khẩu mới | Test1234+ |

## Test steps
1. Hoàn thành Bước 1 với \`test@eshop.com\`.
2. Nhập OTP hợp lệ và mật khẩu \`Test1234+\` (ký tự \`+\` **không** thuộc \`@$!%*?&\`).
3. Bấm "Đặt lại mật khẩu".

## Expected result
- Theo FR-01: hệ thống **từ chối** vì ký tự đặc biệt không thuộc tập cho phép.
- Client Mobile không được chấp nhận chỉ vì regex \`[^A-Za-z\\\\d]\` rộng hơn đặc tả.

## Sub-domains covered
GAP-08 — FR-01 special-char whitelist

## Type
Invalid

## Status / Related bugs
Not Run / #7
`,
};

fs.mkdirSync(dstDir, { recursive: true });

for (const [name, content] of Object.entries(supFiles)) {
  fs.writeFileSync(path.join(dstDir, name), content);
}

for (let i = 21; i <= 44; i++) {
  const num = String(i).padStart(3, '0');
  const src = path.join(srcDir, `TC-FORGOT-${num}.md`);
  const dst = path.join(dstDir, `TC-MFORGOT-${num}.md`);
  fs.writeFileSync(dst, transformBva(fs.readFileSync(src, 'utf8')));
}

console.log('Created SUP 001-007 and BVA 021-044 in', dstDir);
