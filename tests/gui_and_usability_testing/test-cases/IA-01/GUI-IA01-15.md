# GUI-IA01-15: Grid sản phẩm responsive đúng số cột, không tràn ngang

## Requirement ID
Heuristic (responsive)

## Module / Test type / Technique
Giao diện chung (General UI) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA01-15 |
| Interface Aspect | Giao diện chung (General UI) |
| Actor | Người dùng cuối (khách) |
| Goal | Grid sản phẩm responsive đúng số cột, không tràn ngang. |
| Screen(s) | Trang chủ |
| Checklist item | Grid sản phẩm 1/2/3 cột theo breakpoint (Home.jsx:75), không horizontal scroll ở 375/768/1280px. |
| Traced to | Heuristic (responsive) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — DevTools device toolbar |
| Endpoint / UI flow | / |
| Input / Payload | Viewport 375 / 768 / 1280px |
| Fixture | ≥3 sản phẩm seed |

## Test steps
1. Mở `/`, lần lượt đặt viewport 375, 768, 1280px.
2. Đếm số cột grid và kiểm tra thanh cuộn ngang.
3. Fail nếu sai số cột hoặc có horizontal scroll.

## Expected result
- 375px → 1 cột, 768px → 2 cột, 1280px → 3 cột.
- Không xuất hiện thanh cuộn ngang ở cả 3 kích thước.

## Status / Related bugs
Passed (kiểm thử tay 25/07/2026) · ⚠️ **Task 3 đo lại 28/07/2026: Fail** — xem mục "Retest — Task 3" cuối file

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — kiểm thử thủ công trên trình duyệt Chrome
- Observed: Grid sản phẩm co giãn theo breakpoint (1/2/3 cột), không xuất hiện cuộn ngang ở 375/768/1280px.
- Execution result: **Passed**
- Screenshot: _(không có — test Passed)_

## Retest — Task 3 (28/07/2026)

- Kết quả đo lại: **Fail** trên cả 3 platform — không phải hiện tượng phụ thuộc platform.
- Vì sao lần chạy tay ở trên kết luận Passed: chấm bằng mắt tại đúng 768px, nơi breakpoint `md:` của Tailwind (`min-width:768px`) đã kích hoạt → grid ra **3 cột** trong khi item đòi 2. Ranh giới breakpoint rất khó phân biệt bằng mắt.
- Bằng chứng: `../../../cross_platform_testing/results/P*/screenshots/GUI-IA01-15.png` · phân tích: `../../../cross_platform_testing/report.md` §5.
