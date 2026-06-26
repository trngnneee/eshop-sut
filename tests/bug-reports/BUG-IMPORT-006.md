Title: [BUG][Import][Frontend] Không hỗ trợ dấu phẩy bọc trong dấu nháy kép (RFC 4180)

## Found by Test Case
TC-IMPORT-010

## Requirement liên quan
FR-16: Import Sản phẩm từ CSV (Hỗ trợ các trường có chứa dấu phẩy nếu được bọc trong dấu nháy kép)

## Severity / Priority
Major / P1

## Environment
Frontend Admin Web Dashboard

## Steps to reproduce
1. Tải lên file CSV chứa sản phẩm có tên: `"Sản phẩm, đặc biệt"` (được bọc trong nháy kép).
2. Nhấn nút "Import".

## Expected result
- Hệ thống nhận diện đúng đây là một cột dữ liệu duy nhất và hiển thị/import đúng tên.

## Actual result
- Hệ thống chia cột tại dấu phẩy bên trong dấu nháy kép, dẫn đến việc vỡ cấu trúc cột của dòng đó.

## Evidence
![Ảnh chụp minh chứng](../bugs-screenshots/BUG-IMPORT-006.png)
---
*Nhãn (Labels) cần gắn:* `type: bug`, `module: admin`, `severity: major`, `priority: P1`, `status: new`, `found-by: test-case`
