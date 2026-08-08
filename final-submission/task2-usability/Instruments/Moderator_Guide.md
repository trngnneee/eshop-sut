# Moderator Guide

## Before the participant arrives

- Use the frozen protocol version from the completed pilot.
- Start the backend and web frontend and verify only that the home page loads.
- Clear the browser's EShop token, storage, and test tabs.
- Prepare Card A with a unique session email.
- Open the consent form, session record, timer, and capture tool.
- Disable unrelated notifications and close personal tabs.
- Confirm disk space and the evidence folder for the assigned participant ID.

## Opening script

Read verbatim:

> Cảm ơn bạn đã tham gia. Hôm nay chúng tôi kiểm thử sản phẩm EShop, không kiểm thử bạn; không có thao tác đúng hay sai về phía bạn. Trong khi làm, xin hãy nói thành tiếng những gì bạn nhìn thấy, đang nghĩ, mong đợi và điều khiến bạn bối rối. Mình sẽ quan sát và hạn chế trợ giúp để hiểu giao diện hoạt động tự nhiên như thế nào. Bạn có thể dừng bất cứ lúc nào. Xin đừng nhập thông tin cá nhân thật hoặc mật khẩu thật; chỉ dùng dữ liệu kiểm thử được cấp.

Review the consent form and obtain choices before recording. State aloud when screen recording starts.

## Warm-up

Ask:

> Bạn thường mua sắm trực tuyến bằng website hay ứng dụng? Bạn thường tạo và quản lý tài khoản mua sắm như thế nào?

Record the genuine response briefly; do not use it to coach the task.

## Start task

1. Give Card A.
2. Read the task scenario exactly from `Usability_Test_Plan.md`.
3. Start the timer when the participant first acts.
4. Observe without naming controls.

## Neutral prompts

Permitted:

- “Bạn đang nghĩ gì lúc này?”
- “Bạn mong đợi điều gì sẽ xảy ra?”
- “Bạn hãy làm theo cách bạn cho là hợp lý.”
- “Bạn đã hoàn thành mục tiêu chưa?”

Not permitted:

- “Hãy nhấn Đăng ký/Đăng nhập/Hồ sơ/Thoát.”
- “Nút ở góc phải.”
- “Số điện thoại phải bỏ số 0.”
- Explaining the password regex or interpreting an error before the participant does.

## Intervention protocol

When the participant explicitly asks for help, repeats a failed action three times, or makes no progress for 120 seconds:

1. Record timestamp, current screen, last action, and request.
2. Give the smallest neutral prompt first.
3. If a technical phone-validation blocker remains, show Card B.
4. Record the exact intervention and resulting action.

## Close the task

When the participant says they are finished:

1. Stop the task timer.
2. Record the outcome without revealing correctness.
3. Run the researcher-only persistence/logout check.
4. Ask the participant to complete SUS independently.
5. Ask all four probes, then relevant non-leading follow-ups.
6. Ask whether they wish to add or withdraw any comment.
7. State aloud when recording ends.

## After the participant leaves

- Save evidence using the participant ID, never the participant name.
- Verify the session file has genuine raw SUS Q1–Q10 and all four probes.
- Note every intervention.
- Do not change `UNVERIFIED` to `COMPLETED` until the record and evidence are complete.
- Reproduce possible software bugs separately and avoid duplicate GitHub Issues.
- Commit this session as its own Git commit.
