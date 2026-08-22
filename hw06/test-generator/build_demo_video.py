#!/usr/bin/env python3
"""Build audio and video demo for HW06 Agent Skill strictly following DEMO-SCRIPT.md."""

import asyncio
import json
import math
import os
import subprocess
from pathlib import Path
import edge_tts
from PIL import Image, ImageDraw, ImageFont

VOICE = "vi-VN-NamMinhNeural"
BUILD_DIR = Path("hw06/test-generator/_build")
AUDIO_DIR = BUILD_DIR / "audio"
FRAMES_DIR = BUILD_DIR / "frames"
OUTPUT_VIDEO = Path("hw06/test-generator/demo-video.mp4")

BEATS = [
    {
        "id": "beat1",
        "title": "Beat 1 — Mở đầu",
        "text": "Chào thầy cô, em là Đặng Đăng Khoa, MSSV 23127207. Đây là demo Agent Skill api_test_generator em xây cho HW06. Nó nhận mô tả một endpoint và sinh ra bộ test case có thể audit được, theo bốn kỹ thuật: phân vùng, chuyển trạng thái, bảo mật và schema.",
        "display_text": "Chào thầy/cô, em là Đặng Đăng Khoa, MSSV 23127207. Đây là demo Agent Skill `api_test_generator` em xây cho HW06. Nó nhận mô tả một endpoint và sinh ra bộ test case có thể audit được, theo bốn kỹ thuật: phân vùng, chuyển trạng thái, bảo mật và schema."
    },
    {
        "id": "beat2a",
        "title": "Beat 2a — Quy trình 5 bước bắt buộc",
        "text": "Điểm khiến nó là một Skill chứ không phải script rời là phần quy trình bắt buộc này. Skill ràng buộc AI phải đi đủ năm bước — P1 mô hình input và state, P2 phân vùng và biên, P3 ma trận chuyển trạng thái, P4 bảo mật, P5 schema — thay vì hỏi một prompt tổng rồi nhận về một đống case không kiểm soát được.",
        "display_text": "Điểm khiến nó là một Skill chứ không phải script rời là phần quy trình bắt buộc này. Skill ràng buộc AI phải đi đủ năm bước — P1 mô hình input và state, P2 phân vùng và biên, P3 ma trận chuyển trạng thái, P4 bảo mật, P5 schema — thay vì hỏi một prompt tổng rồi nhận về một đống case không kiểm soát được."
    },
    {
        "id": "beat2b",
        "title": "Beat 2b — Ràng buộc Human-Review",
        "text": "Và dòng cuối cùng ghi rõ: never mark a case human-approved automatically. Đây là ràng buộc em cố ý đặt vào, em sẽ quay lại ở cuối video.",
        "display_text": "Và dòng cuối cùng ghi rõ: *never mark a case human-approved automatically*. Đây là ràng buộc em cố ý đặt vào, em sẽ quay lại ở cuối video."
    },
    {
        "id": "beat3",
        "title": "Beat 3 — Đầu vào JSON & Traceability",
        "text": "Đầu vào là một file JSON gọn: parameters với miền giá trị, states với trạng thái đầu và kết quả mong đợi, security, và response schema. Mỗi mục đều có trường requirement — đây là thứ giữ cho traceability không đứt: mọi case sinh ra đều truy ngược được về FR hoặc SEC.",
        "display_text": "Đầu vào là một file JSON gọn: parameters với miền giá trị, states với trạng thái đầu và kết quả mong đợi, security, và response schema. Mỗi mục đều có trường `requirement` — đây là thứ giữ cho traceability không đứt: mọi case sinh ra đều truy ngược được về FR hoặc SEC."
    },
    {
        "id": "beat4a",
        "title": "Beat 4a — Chạy Generator",
        "text": "Chạy xong nó trả về một dòng JSON: 12 case, và kết quả audit hook.",
        "display_text": "Chạy xong nó trả về một dòng JSON: 12 case, và kết quả audit hook."
    },
    {
        "id": "beat4b",
        "title": "Beat 4b — Kết quả sinh và Postman Skeleton",
        "text": "Mỗi dòng có ID ổn định dạng TC-API-LOGIN-###, nhóm kỹ thuật, tiền điều kiện, dữ liệu, kết quả mong đợi và requirement nguồn. Nó cũng xuất kèm một Postman skeleton.",
        "display_text": "Mỗi dòng có ID ổn định dạng `TC-API-LOGIN-###`, nhóm kỹ thuật, tiền điều kiện, dữ liệu, kết quả mong đợi và requirement nguồn. Nó cũng xuất kèm một Postman skeleton."
    },
    {
        "id": "beat5",
        "title": "Beat 5 — Audit Hook bắt lỗi",
        "text": "Em cố ý đưa vào một spec thiếu expected. Audit hook chỉ đúng hai case hỏng. Nó kiểm ba thứ máy làm được: ID trùng, expected rỗng, và oracle không an toàn. Nhưng nó không kiểm được expected đó có đúng đặc tả hay không — chỗ đó phải là người.",
        "display_text": "Em cố ý đưa vào một spec thiếu `expected`. Audit hook chỉ đúng hai case hỏng. Nó kiểm ba thứ máy làm được: ID trùng, expected rỗng, và oracle không an toàn. Nhưng nó không kiểm được expected đó có đúng đặc tả hay không — chỗ đó phải là người."
    },
    {
        "id": "beat6a",
        "title": "Beat 6a — Kiến trúc và 4 nhánh sinh test",
        "text": "Sơ đồ này là thiết kế của em. Input đi qua parser, tạo Parameter và State Model, rồi tách ra bốn nhánh sinh test độc lập, hội tụ về Test Case IR.",
        "display_text": "Sơ đồ này là thiết kế của em. Input đi qua parser, tạo Parameter và State Model, rồi tách ra bốn nhánh sinh test độc lập, hội tụ về Test Case IR."
    },
    {
        "id": "beat6b",
        "title": "Beat 6b — Cổng Human Review Gate",
        "text": "Khối quan trọng nhất là cổng này. Generator sinh 12 case cho API login, nhưng bảng cuối cùng của em có 42 case. Chênh lệch đó là phần con người làm: audit lại nhãn, và bổ sung các case mà máy không thể tự nghĩ ra.",
        "display_text": "Khối quan trọng nhất là cổng này. Generator sinh 12 case cho API login, nhưng bảng cuối cùng của em có 42 case. Chênh lệch đó là phần con người làm: audit lại nhãn, và bổ sung các case mà máy không thể tự nghĩ ra."
    },
    {
        "id": "beat6c",
        "title": "Beat 6c — Ví dụ thực tế: Bug D-LOGIN-03",
        "text": "Ví dụ TC-API-LOGIN-039 — kiểm response không được chứa field password. Generator chỉ biết kiểm field nào phải có, nó không tự lập được danh sách field bị cấm. Case đó là do em thêm, và nó chính là case bắt được bug D-LOGIN-03, issue số 415.",
        "display_text": "Ví dụ `TC-API-LOGIN-039` — kiểm response **không** được chứa field `password`. Generator chỉ biết kiểm field nào *phải có*, nó không tự lập được danh sách field *bị cấm*. Case đó là do em thêm, và nó chính là case bắt được bug D-LOGIN-03, issue #415."
    },
    {
        "id": "beat7",
        "title": "Beat 7 — Kết luận & Trách nhiệm Tester",
        "text": "Tóm lại, generator tạo scaffold có cấu trúc và audit được, còn trách nhiệm oracle và kết luận cuối cùng vẫn thuộc về người kiểm thử. Em cảm ơn thầy cô.",
        "display_text": "Tóm lại, generator tạo scaffold có cấu trúc và audit được, còn trách nhiệm oracle và kết luận cuối cùng vẫn thuộc về người kiểm thử. Em cảm ơn thầy/cô."
    }
]


async def generate_audio():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    for b in BEATS:
        out_file = AUDIO_DIR / f"{b['id']}.mp3"
        print(f"Generating TTS for {b['id']}...")
        comm = edge_tts.Communicate(b['text'], VOICE, rate="+2%")
        await comm.save(str(out_file))
        print(f"  -> Saved {out_file}")


def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())


if __name__ == "__main__":
    asyncio.run(generate_audio())
    print("\nAudio Durations:")
    total = 0.0
    for b in BEATS:
        p = AUDIO_DIR / f"{b['id']}.mp3"
        dur = get_audio_duration(p)
        b["duration"] = dur
        total += dur
        print(f"  {b['id']}: {dur:.2f}s")
    print(f"Total narration duration: {total:.2f}s (~{total/60:.2f} minutes)")
