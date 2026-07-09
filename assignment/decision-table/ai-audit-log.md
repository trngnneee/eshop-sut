# AI Audit Log

| Tool | Date Time | Prompt Summary | Output Summary | Human Review / Correction |
|---|---|---|---|---|
| Claude Sonnet 4.6 (Thinking) | 2026-06-29 15:51 | Sử dụng decision-table-pairwise-skill để thiết kế test cho FR02 — Đăng nhập và Lock Account của EShop SUT | Phân tích requirement từ server.js + database.js; xây dựng 5 conditions (C01–C05), 6 actions (A01–A06); full decision table 38 rules (72 lý thuyết); lọc 11 rules impossible/redundant; pairwise 18 cases; 18 test cases; 1 bug report (BUG-FR02-001: login_attempts +2 bug); traceability matrix đầy đủ | Cần review: (1) Xác nhận bug ASM01 — `+2` thay vì `+1` là thực sự là bug hay intentional; (2) Xác nhận `C03=Đã hết hạn + C04=0` có thực sự impossible không (nếu DB được can thiệp tay); (3) Kiểm tra lại rule R005/R023/R024 với DB manipulation scenario |
