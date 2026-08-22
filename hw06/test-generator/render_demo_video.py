#!/usr/bin/env python3
"""Complete Video Renderer for HW06 Agent Skill Demo strictly following DEMO-SCRIPT.md."""

import json
import math
import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BUILD_DIR = Path("hw06/test-generator/_build")
AUDIO_DIR = BUILD_DIR / "audio"
FRAMES_DIR = BUILD_DIR / "frames"
CLIPS_DIR = BUILD_DIR / "clips"
OUTPUT_VIDEO = Path("hw06/test-generator/demo-video.mp4")

WIDTH = 1920
HEIGHT = 1080

# System Fonts
FONT_CODE = "C:/Windows/Fonts/consola.ttf"
FONT_CODE_BOLD = "C:/Windows/Fonts/consolab.ttf"
FONT_UI = "C:/Windows/Fonts/segoeui.ttf"
FONT_UI_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_UI_SEMIBOLD = "C:/Windows/Fonts/seguisb.ttf"


def get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_rounded_rect(draw: ImageDraw.ImageDraw, xy, radius=10, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)


def draw_subtitles(img: Image.Image, text: str, beat_title: str = ""):
    draw = ImageDraw.Draw(img, "RGBA")
    font_sub = get_font(FONT_UI_BOLD, 26)
    font_badge = get_font(FONT_UI_SEMIBOLD, 18)
    font_header = get_font(FONT_UI_BOLD, 20)

    # Top right presenter badge
    header_w, header_h = 580, 52
    hx0, hy0 = WIDTH - header_w - 30, 20
    draw.rounded_rectangle([hx0, hy0, hx0 + header_w, hy0 + header_h], radius=8, fill=(20, 24, 35, 230), outline=(56, 139, 253, 200), width=2)
    draw.text((hx0 + 16, hy0 + 14), "Đặng Đăng Khoa (23127207)  |  HW06 Agent Skill Demo", font=font_header, fill=(240, 246, 252))

    # Beat badge top left
    if beat_title:
        bw = 360
        draw.rounded_rectangle([30, 20, 30 + bw, 68], radius=8, fill=(22, 27, 34, 230), outline=(48, 54, 61, 200), width=1)
        draw.text((45, 33), f"🎬 {beat_title}", font=font_badge, fill=(88, 166, 255))

    # Bottom subtitle container
    sub_y = HEIGHT - 115
    sub_h = 85
    sub_w = WIDTH - 200
    sub_x = 100
    draw.rounded_rectangle([sub_x, sub_y, sub_x + sub_w, sub_y + sub_h], radius=14, fill=(13, 17, 23, 240), outline=(48, 54, 61, 220), width=2)

    # Word wrapping
    words = text.split()
    lines = []
    curr = []
    for w in words:
        test_line = " ".join(curr + [w])
        bbox = draw.textbbox((0, 0), test_line, font=font_sub)
        if bbox[2] - bbox[0] > sub_w - 60:
            lines.append(" ".join(curr))
            curr = [w]
        else:
            curr.append(w)
    if curr:
        lines.append(" ".join(curr))

    # Center lines inside box
    total_text_h = len(lines) * 32
    start_y = sub_y + (sub_h - total_text_h) // 2
    for i, line in enumerate(lines):
        l_bbox = draw.textbbox((0, 0), line, font=font_sub)
        l_w = l_bbox[2] - l_bbox[0]
        lx = sub_x + (sub_w - l_w) // 2
        draw.text((lx, start_y + i * 32), line, font=font_sub, fill=(255, 255, 255))


def render_base_vscode(active_tab="SKILL.md") -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGBA", (WIDTH, HEIGHT), (24, 24, 24, 255))
    draw = ImageDraw.Draw(img)

    # Titlebar
    draw.rectangle([0, 0, WIDTH, 35], fill=(30, 30, 30))
    font_sm = get_font(FONT_UI, 14)
    draw.text((20, 9), "hw06 - Visual Studio Code", font=font_sm, fill=(204, 204, 204))

    # Window buttons
    draw.ellipse([WIDTH - 70, 12, WIDTH - 60, 22], fill=(235, 100, 100))
    draw.ellipse([WIDTH - 50, 12, WIDTH - 40, 22], fill=(235, 190, 100))
    draw.ellipse([WIDTH - 30, 12, WIDTH - 20, 22], fill=(100, 200, 100))

    # Activity Bar
    draw.rectangle([0, 35, 50, HEIGHT - 25], fill=(51, 51, 51))
    draw.rectangle([48, 45, 50, 85], fill=(0, 122, 204))  # Explorer active indicator

    # Explorer Sidebar
    draw.rectangle([50, 35, 320, HEIGHT - 25], fill=(37, 37, 38))
    font_bold = get_font(FONT_UI_BOLD, 13)
    draw.text((65, 45), "EXPLORER", font=font_bold, fill=(187, 187, 187))

    font_tree = get_font(FONT_UI, 14)
    font_tree_b = get_font(FONT_UI_BOLD, 14)

    tree = [
        (65, 75, "▼ HW06-TEST-GENERATOR", (220, 220, 220), True),
        (80, 105, "▼ .agents/skills/api_test_generator", (200, 200, 200), True),
        (95, 135, "📄 SKILL.md", (88, 166, 255) if active_tab == "SKILL.md" else (180, 180, 180), active_tab == "SKILL.md"),
        (95, 165, "▼ examples", (200, 200, 200), False),
        (110, 195, "{} login.endpoint.json", (229, 146, 50) if active_tab == "login.endpoint.json" else (180, 180, 180), active_tab == "login.endpoint.json"),
        (80, 225, "▼ hw06/test-generator", (200, 200, 200), True),
        (95, 255, "🐍 generator.py", (78, 201, 176) if active_tab == "generator.py" else (180, 180, 180), active_tab == "generator.py"),
        (95, 285, "🖼 diagram.png", (206, 145, 120) if active_tab == "diagram.png" else (180, 180, 180), active_tab == "diagram.png"),
        (95, 315, "📝 DEMO-SCRIPT.md", (180, 180, 180), False),
        (95, 345, "📊 generated.md", (88, 166, 255) if active_tab == "generated.md" else (180, 180, 180), active_tab == "generated.md"),
    ]

    for tx, ty, ttext, tcolor, is_b in tree:
        draw.text((tx, ty), ttext, font=font_tree_b if is_b else font_tree, fill=tcolor)

    # Editor Area
    draw.rectangle([320, 35, WIDTH, HEIGHT - 25], fill=(30, 30, 30))

    # Tabs
    tabs = [
        ("SKILL.md", "📄"),
        ("login.endpoint.json", "{}"),
        ("generator.py", "🐍"),
        ("diagram.png", "🖼")
    ]
    tab_x = 320
    for name, icon in tabs:
        is_active = (name == active_tab)
        tab_w = 200
        tab_fill = (30, 30, 30) if is_active else (45, 45, 45)
        draw.rectangle([tab_x, 35, tab_x + tab_w, 75], fill=tab_fill)
        if is_active:
            draw.rectangle([tab_x, 35, tab_x + tab_w, 37], fill=(0, 122, 204))  # Active tab bar
        draw.text((tab_x + 15, 46), f"{icon}  {name}", font=font_tree, fill=(255, 255, 255) if is_active else (150, 150, 150))
        tab_x += tab_w + 2

    # Status Bar
    draw.rectangle([0, HEIGHT - 25, WIDTH, HEIGHT], fill=(0, 122, 204))
    draw.text((20, HEIGHT - 20), "⚡ Agent Skill: api_test_generator  |  Ln 1, Col 1  |  UTF-8  |  Markdown / JSON", font=font_sm, fill=(255, 255, 255))

    return img, draw


def render_beat1_frame() -> Image.Image:
    img, draw = render_base_vscode(active_tab="SKILL.md")
    font_code = get_font(FONT_CODE, 20)
    font_code_b = get_font(FONT_CODE_BOLD, 22)
    font_lineno = get_font(FONT_CODE, 18)

    lines = [
        (" 1", "---", (106, 153, 85)),
        (" 2", "name: api_test_generator", (156, 220, 254)),
        (" 3", "description: Generate auditable API test cases from a compact endpoint specification", (206, 145, 120)),
        ("  ", "             using partition, state, security, and schema techniques.", (206, 145, 120)),
        (" 4", "---", (106, 153, 85)),
        (" 5", "", (200, 200, 200)),
        (" 6", "# API test generator skill", (86, 156, 214)),
        (" 7", "", (200, 200, 200)),
        (" 8", "Use this skill when an API endpoint needs a repeatable AI-assisted test inventory.", (220, 220, 220)),
        (" 9", "The output is a candidate suite, not an oracle; compare every expected result", (220, 220, 220)),
        ("10", "with the API specification, business requirements, and SUT before execution.", (220, 220, 220)),
        ("11", "", (200, 200, 200)),
        ("12", "## Required five-step process", (78, 201, 176)),
        ("13", "", (200, 200, 200)),
        ("14", "1. **P1 — input/state model:** list every parameter and every state/precondition.", (215, 186, 125)),
        ("15", "2. **P2 — partition/BVA:** create valid, invalid, type and boundary partitions.", (215, 186, 125)),
        ("16", "3. **P3 — state transition:** enumerate allowed, forbidden, and terminal transitions.", (215, 186, 125)),
        ("17", "4. **P4 — security:** cover auth/JWT, IDOR, role escalation, injection and leakage.", (215, 186, 125)),
        ("18", "5. **P5 — schema:** check status, content type, required fields, field types.", (215, 186, 125)),
    ]

    y = 95
    for lineno, content, color in lines:
        draw.text((345, y), lineno, font=font_lineno, fill=(100, 100, 100))
        draw.text((400, y), content, font=font_code_b if content.startswith("#") else font_code, fill=color)
        y += 34

    # Highlighting card for Agent Skill Concept
    cx0, cy0 = 1320, 120
    cw, ch = 550, 320
    draw.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=12, fill=(22, 27, 34, 240), outline=(56, 139, 253, 220), width=2)
    font_card_title = get_font(FONT_UI_BOLD, 22)
    font_card_body = get_font(FONT_UI, 18)

    draw.text((cx0 + 20, cy0 + 20), "✨ AGENT SKILL: api_test_generator", font=font_card_title, fill=(88, 166, 255))
    draw.line([cx0 + 20, cy0 + 55, cx0 + cw - 20, cy0 + 55], fill=(48, 54, 61), width=1)

    bullets = [
        ("✦ Mục tiêu:", "Tạo bộ test cases có thể AUDIT được cho API"),
        ("✦ 4 Kỹ thuật:", "Phân vùng (EP/BVA), State, Security, Schema"),
        ("✦ Cấu trúc:", "Quy trình 5 bước nghiêm ngặt + Audit Hook"),
        ("✦ Ràng buộc:", "Tuyệt đối không tự động duyệt Human-Approved")
    ]
    by = cy0 + 75
    for b_title, b_desc in bullets:
        draw.text((cx0 + 20, by), b_title, font=get_font(FONT_UI_BOLD, 18), fill=(240, 136, 62))
        draw.text((cx0 + 20, by + 26), b_desc, font=font_card_body, fill=(201, 209, 217))
        by += 58

    draw_subtitles(img, "Chào thầy/cô, em là Đặng Đăng Khoa, MSSV 23127207. Đây là demo Agent Skill `api_test_generator` em xây cho HW06.", "Beat 1 — Mở đầu")
    return img


def render_beat2a_frame() -> Image.Image:
    img, draw = render_base_vscode(active_tab="SKILL.md")
    font_code = get_font(FONT_CODE, 20)
    font_code_b = get_font(FONT_CODE_BOLD, 22)
    font_lineno = get_font(FONT_CODE, 18)

    lines = [
        (" 8", "Use this skill when an API endpoint needs a repeatable AI-assisted test inventory.", (140, 140, 140)),
        (" 9", "The output is a candidate suite, not an oracle; compare every expected result", (140, 140, 140)),
        ("10", "## Required five-step process", (78, 201, 176)),
        ("11", "", (200, 200, 200)),
        ("12", "1. **P1 — input/state model:** list every parameter and every state/precondition.", (240, 246, 252)),
        ("13", "2. **P2 — partition/BVA:** create valid, invalid, type and boundary partitions.", (240, 246, 252)),
        ("14", "3. **P3 — state transition:** enumerate allowed, forbidden, and terminal transitions.", (240, 246, 252)),
        ("15", "4. **P4 — security:** cover auth/JWT, IDOR, role escalation, injection and leakage.", (240, 246, 252)),
        ("16", "5. **P5 — schema:** check status, content type, required fields, field types.", (240, 246, 252)),
        ("17", "", (200, 200, 200)),
        ("18", "Then run the audit hook: stable IDs, duplicate detection, missing expected result,", (156, 220, 254)),
        ("19", "unsupported oracle assumptions, and a human-review checkpoint.", (156, 220, 254)),
    ]

    # Glow box around 5-step process
    draw.rounded_rectangle([385, 175, 1340, 430], radius=10, fill=(30, 45, 65, 180), outline=(56, 139, 253, 240), width=3)

    y = 95
    for lineno, content, color in lines:
        draw.text((345, y), lineno, font=font_lineno, fill=(100, 100, 100))
        draw.text((400, y), content, font=font_code_b if content.startswith("##") else font_code, fill=color)
        y += 38

    # Side callout card
    cx0, cy0 = 1370, 130
    cw, ch = 510, 360
    draw.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=12, fill=(22, 27, 34, 245), outline=(56, 139, 253, 220), width=2)
    draw.text((cx0 + 20, cy0 + 20), "🎯 VÌ SAO LÀ AGENT SKILL?", font=get_font(FONT_UI_BOLD, 22), fill=(88, 166, 255))
    draw.line([cx0 + 20, cy0 + 55, cx0 + cw - 20, cy0 + 55], fill=(48, 54, 61), width=1)

    pts = [
        ("❌ Prompt tự do:", "Sinh ra một đống case ngẫu nhiên, không thể kiểm soát."),
        ("✔ Ràng buộc 5 bước:", "Bắt buộc đi đủ P1 (Model) ➔ P2 (BVA) ➔ P3 (State) ➔ P4 (Security) ➔ P5 (Schema)."),
        ("✔ Đảm bảo độ phủ:", "Không bỏ sót góc kiểm thử, kiểm soát được chất lượng IR.")
    ]
    by = cy0 + 75
    for t1, t2 in pts:
        draw.text((cx0 + 20, by), t1, font=get_font(FONT_UI_BOLD, 18), fill=(235, 100, 100) if "❌" in t1 else (63, 185, 80))
        draw.text((cx0 + 20, by + 26), t2, font=get_font(FONT_UI, 16), fill=(201, 209, 217))
        by += 68

    draw_subtitles(img, "Skill ràng buộc AI phải đi đủ 5 bước — P1 tới P5 — thay vì hỏi một prompt tổng rồi nhận về case không kiểm soát được.", "Beat 2a — Quy trình 5 bước bắt buộc")
    return img


def render_beat2b_frame() -> Image.Image:
    img, draw = render_base_vscode(active_tab="SKILL.md")
    font_code = get_font(FONT_CODE, 20)
    font_code_b = get_font(FONT_CODE_BOLD, 22)
    font_lineno = get_font(FONT_CODE, 18)

    lines = [
        ("20", "## Reusable commands", (78, 201, 176)),
        ("21", "", (200, 200, 200)),
        ("22", "```powershell", (106, 153, 85)),
        ("23", "python hw06/test-generator/generator.py login.endpoint.json --out generated.md", (206, 145, 120)),
        ("24", "```", (106, 153, 85)),
        ("25", "", (200, 200, 200)),
        ("26", "## Output contract", (78, 201, 176)),
        ("27", "", (200, 200, 200)),
        ("28", "Every case has `TC-API-<domain>-###`, group, technique, precondition, data,", (220, 220, 220)),
        ("29", "expected result, requirement and source. Render Markdown and a Postman skeleton.", (220, 220, 220)),
        ("30", "Never mark a case human-approved automatically; retain reviewer fields.", (255, 215, 0)),
    ]

    # Amber box highlighting line 30
    draw.rounded_rectangle([385, 420, 1340, 505], radius=10, fill=(60, 45, 10, 200), outline=(240, 136, 62, 255), width=3)

    y = 95
    for lineno, content, color in lines:
        draw.text((345, y), lineno, font=font_lineno, fill=(100, 100, 100))
        draw.text((400, y), content, font=font_code_b if content.startswith("##") or "Never mark" in content else font_code, fill=color)
        y += 38

    # Side callout card
    cx0, cy0 = 1370, 140
    cw, ch = 510, 340
    draw.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=12, fill=(35, 20, 20, 245), outline=(248, 81, 73, 230), width=2)
    draw.text((cx0 + 20, cy0 + 20), "⚠️ RÀNG BUỘC CỐ Ý ĐẶT RA", font=get_font(FONT_UI_BOLD, 22), fill=(248, 81, 73))
    draw.line([cx0 + 20, cy0 + 55, cx0 + cw - 20, cy0 + 55], fill=(80, 40, 40), width=1)

    draw.text((cx0 + 20, cy0 + 75), "\"Never mark a case human-approved automatically\"", font=get_font(FONT_CODE_BOLD, 17), fill=(255, 215, 0))
    desc = [
        "• Máy CHỈ sinh ra bộ ứng viên (Candidate Suite)",
        "• Trách nhiệm kiểm tra Oracle thuộc về Tester",
        "• AI không được tự ý đóng dấu phê duyệt",
        "➔ Sẽ giải thích chi tiết tại Cổng Human Review Gate!"
    ]
    by = cy0 + 130
    for d in desc:
        draw.text((cx0 + 20, by), d, font=get_font(FONT_UI, 16), fill=(240, 246, 252))
        by += 42

    draw_subtitles(img, "Dòng cuối cùng: *never mark a case human-approved automatically*. Đây là ràng buộc em cố ý đặt vào!", "Beat 2b — Ràng buộc Human-Review")
    return img


def render_beat3_frame() -> Image.Image:
    img, draw = render_base_vscode(active_tab="login.endpoint.json")
    font_code = get_font(FONT_CODE, 20)
    font_lineno = get_font(FONT_CODE, 18)

    lines = [
        (" 1", "{", (220, 220, 220)),
        (" 2", '  "id_prefix": "TC-API-LOGIN",', (156, 220, 254)),
        (" 3", '  "method": "POST", "path": "/api/login",', (156, 220, 254)),
        (" 4", '  "parameters": [', (156, 220, 254)),
        (" 5", '    {"name": "email", "examples": ["test@eshop.com", "", null], "expected": "200 for valid; 4xx for invalid", "requirement": "FR-02"},', (206, 145, 120)),
        (" 6", '    {"name": "password", "examples": ["Test1234!", "wrong", null], "expected": "200 for valid; 401 for invalid", "requirement": "FR-02"}', (206, 145, 120)),
        (" 7", '  ],', (156, 220, 254)),
        (" 8", '  "states": [', (156, 220, 254)),
        (" 9", '    {"title": "active user with valid credentials", "from": "active", "expected": "200 + token/user", "requirement": "FR-02"},', (206, 145, 120)),
        ("10", '    {"title": "locked user rejects login", "from": "locked", "expected": "403 without token", "requirement": "FR-02"}', (206, 145, 120)),
        ("11", '  ],', (156, 220, 254)),
        ("12", '  "security": [', (156, 220, 254)),
        ("13", '    {"title": "SQL injection is rejected", "technique": "SQLi", "expected": "401/no token", "requirement": "SEC-05"},', (206, 145, 120)),
        ("14", '    {"title": "password is absent from response", "technique": "data leakage", "expected": "no password field", "requirement": "SEC-01"}', (206, 145, 120)),
        ("15", '  ],', (156, 220, 254)),
        ("16", '  "response_schema": [', (156, 220, 254)),
        ("17", '    {"name": "token", "type": "string", "expected": "non-empty string", "requirement": "FR-02"},', (206, 145, 120)),
        ("18", '    {"name": "user", "type": "object", "expected": "object without password", "requirement": "SEC-01"}', (206, 145, 120)),
        ("19", '  ]', (156, 220, 254)),
        ("20", '}', (220, 220, 220)),
    ]

    y = 85
    for lineno, content, color in lines:
        draw.text((345, y), lineno, font=font_lineno, fill=(100, 100, 100))
        draw.text((400, y), content, font=font_code, fill=color)
        y += 34

    # Traceability callout card
    cx0, cy0 = 1350, 100
    cw, ch = 530, 390
    draw.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=12, fill=(22, 27, 34, 245), outline=(63, 185, 80, 230), width=2)
    draw.text((cx0 + 20, cy0 + 20), "🔗 TRACEABILITY 100% (FR / SEC)", font=get_font(FONT_UI_BOLD, 22), fill=(63, 185, 80))
    draw.line([cx0 + 20, cy0 + 55, cx0 + cw - 20, cy0 + 55], fill=(48, 54, 61), width=1)

    titems = [
        ("Trường requirement:", "Gắn trực tiếp vào từng spec entry (FR-02, SEC-01, SEC-05)."),
        ("Không đứt gãy:", "Mọi test case sinh ra đều truy ngược được về yêu cầu nghiệp vụ gốc."),
        ("4 Nhóm Spec:", "Parameters (BVA), States, Security, Response Schema.")
    ]
    by = cy0 + 75
    for h, desc in titems:
        draw.text((cx0 + 20, by), h, font=get_font(FONT_UI_BOLD, 18), fill=(240, 136, 62))
        draw.text((cx0 + 20, by + 26), desc, font=get_font(FONT_UI, 16), fill=(201, 209, 217))
        by += 68

    draw_subtitles(img, "Đầu vào là JSON gọn: parameters, states, security, response_schema. Mỗi mục đều có trường requirement giữ traceability.", "Beat 3 — Đầu vào JSON & Traceability")
    return img


def render_beat4a_frame() -> Image.Image:
    # Terminal Window Full View
    img = Image.new("RGBA", (WIDTH, HEIGHT), (15, 18, 24, 255))
    draw = ImageDraw.Draw(img)

    # Terminal Header
    draw.rectangle([0, 0, WIDTH, 45], fill=(30, 35, 45))
    draw.text((30, 12), "Administrator: Windows PowerShell (16pt)", font=get_font(FONT_UI, 16), fill=(200, 200, 200))
    draw.ellipse([WIDTH - 70, 16, WIDTH - 60, 26], fill=(235, 100, 100))
    draw.ellipse([WIDTH - 50, 16, WIDTH - 40, 26], fill=(235, 190, 100))
    draw.ellipse([WIDTH - 30, 16, WIDTH - 20, 26], fill=(100, 200, 100))

    font_term = get_font(FONT_CODE, 22)
    font_term_b = get_font(FONT_CODE_BOLD, 22)

    y = 80
    draw.text((40, y), "Windows PowerShell", font=font_term, fill=(200, 200, 200)); y += 35
    draw.text((40, y), "Copyright (C) Microsoft Corporation. All rights reserved.", font=font_term, fill=(150, 150, 150)); y += 50

    draw.text((40, y), "PS C:\\My Workspace\\HCMUS\\Test\\Week 3\\Hw2> ", font=font_term_b, fill=(230, 230, 230))
    cmd = "python hw06\\test-generator\\generator.py .agents\\skills\\api_test_generator\\examples\\login.endpoint.json --out demo\\generated.md"
    draw.text((580, y), cmd, font=font_term, fill=(240, 136, 62)); y += 60

    # Output Card Box
    draw.rounded_rectangle([40, y, WIDTH - 40, y + 160], radius=10, fill=(22, 27, 34), outline=(63, 185, 80), width=2)
    draw.text((60, y + 25), "OUTPUT JSON:", font=get_font(FONT_UI_BOLD, 18), fill=(63, 185, 80))
    out_json = '{"cases": 12, "audit": {"count": 12, "duplicate_ids": 0, "missing_expected": []}}'
    draw.text((60, y + 65), out_json, font=get_font(FONT_CODE_BOLD, 22), fill=(126, 231, 135))
    draw.text((60, y + 110), "✔ 12 test cases generated cleanly   ✔ 0 duplicate IDs   ✔ 0 missing expected", font=get_font(FONT_UI, 18), fill=(200, 200, 200))

    draw_subtitles(img, "Chạy generator xong, nó trả về một dòng JSON: 12 case và kết quả của audit hook.", "Beat 4a — Chạy Generator")
    return img


def render_beat4b_frame() -> Image.Image:
    img, draw = render_base_vscode(active_tab="generated.md")
    font_code = get_font(FONT_CODE, 16)
    font_code_b = get_font(FONT_CODE_BOLD, 17)

    # Markdown Table Preview
    draw.text((345, 85), "# Generated test cases — 12 cases", font=get_font(FONT_UI_BOLD, 22), fill=(88, 166, 255))
    draw.text((345, 115), "> Audit hook: `{'count': 12, 'duplicate_ids': 0, 'missing_expected': []}`", font=get_font(FONT_CODE, 16), fill=(126, 231, 135))

    table_data = [
        ("id", "group", "technique", "title", "expected", "requirement"),
        ("TC-API-LOGIN-001", "Partition", "EP/BVA", "email partition: test@eshop.com", "200 for valid; controlled 4xx", "FR-02"),
        ("TC-API-LOGIN-002", "Partition", "EP/BVA", "email partition: ''", "200 for valid; controlled 4xx", "FR-02"),
        ("TC-API-LOGIN-003", "Partition", "EP/BVA", "email partition: None", "200 for valid; controlled 4xx", "FR-02"),
        ("TC-API-LOGIN-004", "Partition", "EP/BVA", "password partition: Test1234!", "200 for valid; 401 for invalid", "FR-02"),
        ("TC-API-LOGIN-005", "Partition", "EP/BVA", "password partition: wrong", "200 for valid; 401 for invalid", "FR-02"),
        ("TC-API-LOGIN-007", "State", "transition", "active user with valid credentials", "200 + token/user", "FR-02"),
        ("TC-API-LOGIN-008", "State", "transition", "locked user rejects login", "403 without token", "FR-02"),
        ("TC-API-LOGIN-009", "Security", "SQLi", "SQL injection is rejected", "401/no token", "SEC-05"),
        ("TC-API-LOGIN-010", "Security", "data leakage", "password absent from response", "no password field", "SEC-01"),
        ("TC-API-LOGIN-011", "Schema", "schema", "response field token", "token is non-empty string", "FR-02"),
        ("TC-API-LOGIN-012", "Schema", "schema", "response field user", "user object without password", "SEC-01"),
    ]

    ty = 155
    # Table header
    draw.rectangle([345, ty, 1380, ty + 30], fill=(45, 55, 72))
    headers = table_data[0]
    draw.text((355, ty + 6), headers[0], font=font_code_b, fill=(255, 255, 255))
    draw.text((540, ty + 6), headers[1], font=font_code_b, fill=(255, 255, 255))
    draw.text((640, ty + 6), headers[2], font=font_code_b, fill=(255, 255, 255))
    draw.text((760, ty + 6), headers[3], font=font_code_b, fill=(255, 255, 255))
    draw.text((1080, ty + 6), headers[4], font=font_code_b, fill=(255, 255, 255))
    draw.text((1300, ty + 6), headers[5], font=font_code_b, fill=(255, 255, 255))
    ty += 32

    for row in table_data[1:]:
        draw.rectangle([345, ty, 1380, ty + 26], fill=(35, 39, 46) if (ty % 2 == 0) else (28, 31, 38))
        draw.text((355, ty + 4), row[0], font=font_code, fill=(126, 231, 135))
        draw.text((540, ty + 4), row[1], font=font_code, fill=(200, 200, 200))
        draw.text((640, ty + 4), row[2], font=font_code, fill=(240, 136, 62))
        draw.text((760, ty + 4), row[3][:32], font=font_code, fill=(220, 220, 220))
        draw.text((1080, ty + 4), row[4][:24], font=font_code, fill=(156, 220, 254))
        draw.text((1300, ty + 4), row[5], font=font_code, fill=(215, 186, 125))
        ty += 28

    # Side card for Postman Skeleton
    cx0, cy0 = 1410, 100
    cw, ch = 480, 420
    draw.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=12, fill=(22, 27, 34, 245), outline=(240, 136, 62, 230), width=2)
    draw.text((cx0 + 20, cy0 + 20), "🚀 XUẤT KÈM POSTMAN SKELETON", font=get_font(FONT_UI_BOLD, 20), fill=(240, 136, 62))
    draw.line([cx0 + 20, cy0 + 55, cx0 + cw - 20, cy0 + 55], fill=(48, 54, 61), width=1)

    draw.text((cx0 + 20, cy0 + 75), "File: demo/generated.postman.json", font=get_font(FONT_CODE, 15), fill=(88, 166, 255))
    p_lines = [
        '{\n  "info": {"name": "Generated API skeleton"},\n  "item": [\n    {"name": "TC-API-LOGIN-001 - email..."},\n    {"name": "TC-API-LOGIN-002 - email..."},\n    {"name": "TC-API-LOGIN-009 - SQLi..."}\n  ]\n}'
    ]
    draw.text((cx0 + 20, cy0 + 110), p_lines[0], font=get_font(FONT_CODE, 15), fill=(200, 200, 200))
    draw.text((cx0 + 20, cy0 + 280), "• Sẵn sàng import vào Postman / Newman\n• Khung chuẩn hóa giúp dev/tester thực thi ngay", font=get_font(FONT_UI, 16), fill=(63, 185, 80))

    draw_subtitles(img, "Mỗi dòng có ID ổn định TC-API-LOGIN-###, nhóm kỹ thuật, dữ liệu, kết quả và requirement nguồn; kèm Postman skeleton.", "Beat 4b — Kết quả sinh và Postman Skeleton")
    return img


def render_beat5_frame() -> Image.Image:
    img = Image.new("RGBA", (WIDTH, HEIGHT), (15, 18, 24, 255))
    draw = ImageDraw.Draw(img)

    # Terminal Header
    draw.rectangle([0, 0, WIDTH, 45], fill=(30, 35, 45))
    draw.text((30, 12), "Administrator: Windows PowerShell (Audit Hook Failure Verification)", font=get_font(FONT_UI, 16), fill=(200, 200, 200))
    draw.ellipse([WIDTH - 70, 16, WIDTH - 60, 26], fill=(235, 100, 100))
    draw.ellipse([WIDTH - 50, 16, WIDTH - 40, 26], fill=(235, 190, 100))
    draw.ellipse([WIDTH - 30, 16, WIDTH - 20, 26], fill=(100, 200, 100))

    font_term = get_font(FONT_CODE, 21)
    font_term_b = get_font(FONT_CODE_BOLD, 21)

    y = 75
    draw.text((40, y), "PS C:\\My Workspace\\HCMUS\\Test\\Week 3\\Hw2> ", font=font_term_b, fill=(230, 230, 230))
    cmd = "python hw06\\test-generator\\generator.py hw06\\test-generator\\examples\\demo-missing-expected.endpoint.json --out demo\\broken.md"
    draw.text((580, y), cmd, font=font_term, fill=(240, 136, 62)); y += 50

    # Output Error Alert Box
    draw.rounded_rectangle([40, y, WIDTH - 40, y + 130], radius=10, fill=(35, 18, 20), outline=(248, 81, 73), width=2)
    draw.text((60, y + 20), "AUDIT HOOK DETECTED DEFECTS:", font=get_font(FONT_UI_BOLD, 18), fill=(248, 81, 73))
    out_json = '{"cases": 3, "audit": {"count": 3, "duplicate_ids": 0, "missing_expected": ["TC-API-DEMO-001", "TC-API-DEMO-002"]}}'
    draw.text((60, y + 55), out_json, font=get_font(FONT_CODE_BOLD, 21), fill=(255, 160, 160))
    draw.text((60, y + 95), "⚠️ Audit Hook bắt đúng 2 test case thiếu trường expected!", font=get_font(FONT_UI, 17), fill=(255, 200, 200))
    y += 150

    # Comparison Graphic: Machine capability vs Human Oracle
    cw = (WIDTH - 120) // 2
    # Left Card: Machine
    draw.rounded_rectangle([40, y, 40 + cw, y + 250], radius=12, fill=(22, 27, 34), outline=(56, 139, 253), width=2)
    draw.text((60, y + 20), "🤖 MÁY LÀM ĐƯỢC (Tự động hóa)", font=get_font(FONT_UI_BOLD, 20), fill=(88, 166, 255))
    draw.line([60, y + 55, 40 + cw - 20, y + 55], fill=(48, 54, 61), width=1)
    m_pts = [
        ("✔ Phát hiện ID trùng lặp", "Đảm bảo tính duy nhất của ID"),
        ("✔ Phát hiện Expected rỗng", "Bắt lỗi thiếu oracle bề mặt"),
        ("✔ Kiểm tra cấu trúc Skeleton", "Đảm bảo tính hợp lệ của schema Postman")
    ]
    my = y + 70
    for p1, p2 in m_pts:
        draw.text((60, my), p1, font=get_font(FONT_UI_BOLD, 17), fill=(63, 185, 80))
        draw.text((60, my + 24), p2, font=get_font(FONT_UI, 15), fill=(200, 200, 200))
        my += 55

    # Right Card: Human
    draw.rounded_rectangle([60 + cw, y, 60 + 2 * cw, y + 250], radius=12, fill=(35, 24, 15), outline=(240, 136, 62), width=2)
    draw.text((80 + cw, y + 20), "👤 MÁY KHÔNG THỂ LÀM (Cần Human Oracle)", font=get_font(FONT_UI_BOLD, 20), fill=(240, 136, 62))
    draw.line([80 + cw, y + 55, 60 + 2 * cw - 20, y + 55], fill=(80, 50, 30), width=1)
    h_pts = [
        ("❌ Không biết Expected có ĐÚNG ĐẶC TẢ hay không", "Máy không hiểu ngữ nghĩa nghiệp vụ thực tế của SUT."),
        ("❌ Nguy cơ chấp nhận bug nếu sửa expected cho khớp SUT", "Nếu API trả sai mà máy coi đó là đúng thì bộ test vô nghĩa."),
        ("👉 BẮT BUỘC CON NGƯỜI DUYỆT ORACLE", "Chỉ con người mới thẩm định được tính đúng đắn của logic!")
    ]
    hy = y + 70
    for p1, p2 in h_pts:
        draw.text((80 + cw, hy), p1, font=get_font(FONT_UI_BOLD, 16), fill=(248, 81, 73) if "❌" in p1 else (255, 215, 0))
        draw.text((80 + cw, hy + 24), p2, font=get_font(FONT_UI, 14), fill=(240, 246, 252))
        hy += 55

    draw_subtitles(img, "Audit hook chỉ đúng 2 case hỏng. Máy kiểm được ID trùng, expected rỗng, nhưng KHÔNG kiểm được expected có đúng đặc tả hay không!", "Beat 5 — Audit Hook bắt lỗi")
    return img


def render_beat6a_frame() -> Image.Image:
    # High-res Diagram View with Camera focus on Top/Middle (Architecture)
    img = Image.new("RGBA", (WIDTH, HEIGHT), (240, 242, 245, 255))
    draw = ImageDraw.Draw(img)

    diag = Image.open("hw06/test-generator/diagram.png").convert("RGBA")
    # Diagram size: (853, 1331) -> let's scale to fit neatly on left side
    diag_h = 920
    diag_w = int(diag.width * (diag_h / diag.height))
    diag_resized = diag.resize((diag_w, diag_h), Image.Resampling.LANCZOS)

    img.paste(diag_resized, (80, 50), diag_resized)

    # Highlight box on Top & 4 branches
    draw.rounded_rectangle([70, 45, 80 + diag_w + 10, 520], radius=10, fill=None, outline=(0, 102, 204), width=4)

    # Right side explanation cards
    rx = 80 + diag_w + 50
    rw = WIDTH - rx - 50
    draw.rounded_rectangle([rx, 80, rx + rw, 520], radius=14, fill=(255, 255, 255), outline=(0, 102, 204), width=2)

    draw.text((rx + 30, 105), "🏛 KIẾN TRÚC GENERATOR & 4 NHÁNH ĐỘC LẬP", font=get_font(FONT_UI_BOLD, 24), fill=(0, 102, 204))
    draw.line([rx + 30, 145, rx + rw - 30, 145], fill=(220, 220, 220), width=1)

    steps = [
        ("1. Input Parser & Normalization:", "Đọc OpenAPI/Swagger + Yêu cầu FR/SEC thành JSON chuẩn hóa."),
        ("2. Parameter & State Model:", "Mô hình hóa tham số, kiểu dữ liệu, preconditions và trạng thái."),
        ("3. 4 Hướng sinh test ĐỘC LẬP:", "• EP/BVA Generator (Phân vùng & Biên)\n• State Transition Generator (Chuyển trạng thái)\n• Security Generator (Auth, SQLi, Abuse)\n• Schema Validation Generator (Cấu trúc & Kiểu)"),
        ("4. Test Case IR (Intermediate Representation):", "Hội tụ về cấu trúc dữ liệu trung gian trước khi render.")
    ]
    sy = 165
    for s_title, s_desc in steps:
        draw.text((rx + 30, sy), s_title, font=get_font(FONT_UI_BOLD, 18), fill=(30, 30, 30))
        lines = s_desc.split("\n")
        for i, l in enumerate(lines):
            draw.text((rx + 30, sy + 25 + i * 22), l, font=get_font(FONT_UI, 16), fill=(70, 70, 70))
        sy += 30 + len(lines) * 22 + 15

    draw_subtitles(img, "Sơ đồ này là thiết kế của em: Input qua parser, tạo Parameter & State Model, tách ra 4 nhánh sinh test độc lập hội tụ về Test Case IR.", "Beat 6a — Kiến trúc và 4 nhánh sinh test")
    return img


def render_beat6b_frame() -> Image.Image:
    # Focus on Human Review Gate
    img = Image.new("RGBA", (WIDTH, HEIGHT), (240, 242, 245, 255))
    draw = ImageDraw.Draw(img)

    diag = Image.open("hw06/test-generator/diagram.png").convert("RGBA")
    diag_h = 920
    diag_w = int(diag.width * (diag_h / diag.height))
    diag_resized = diag.resize((diag_w, diag_h), Image.Resampling.LANCZOS)
    img.paste(diag_resized, (80, 50), diag_resized)

    # Highlight Human Review Gate & Loops
    draw.rounded_rectangle([70, 500, 80 + diag_w + 10, 760], radius=10, fill=None, outline=(220, 50, 50), width=5)

    rx = 80 + diag_w + 50
    rw = WIDTH - rx - 50
    draw.rounded_rectangle([rx, 80, rx + rw, 520], radius=14, fill=(255, 255, 255), outline=(220, 50, 50), width=2)

    draw.text((rx + 30, 105), "🛡️ CỔNG QUAN TRỌNG NHẤT: HUMAN REVIEW GATE", font=get_font(FONT_UI_BOLD, 24), fill=(220, 50, 50))
    draw.line([rx + 30, 145, rx + rw - 30, 145], fill=(220, 220, 220), width=1)

    # Comparison metrics box
    draw.rounded_rectangle([rx + 30, 165, rx + rw - 30, 260], radius=10, fill=(245, 247, 250), outline=(200, 200, 200), width=1)
    draw.text((rx + 50, 180), "AI Generator Sinh:", font=get_font(FONT_UI, 18), fill=(80, 80, 80))
    draw.text((rx + 220, 175), "12 Test Cases", font=get_font(FONT_UI_BOLD, 24), fill=(0, 102, 204))

    draw.text((rx + 50, 220), "Bảng Chốt Cuối Cùng:", font=get_font(FONT_UI, 18), fill=(80, 80, 80))
    draw.text((rx + 250, 215), "42 Test Cases (+30 cases)", font=get_font(FONT_UI_BOLD, 24), fill=(40, 167, 69))

    insights = [
        ("• Chênh lệch 30 cases là gì?", "Phần con người làm: audit lại nhãn, thêm boundary, token invalid, concurrency, forbidden fields..."),
        ("• Vòng hồi tiếp (Feedback Loop):", "Khi audit thấy expected sai -> Sửa lại model để sinh lại nhất quán, KHÔNG vá tay vào markdown output!"),
        ("• Nguyên tắc vàng:", "Máy sinh khung scaffold, người chịu trách nhiệm chất lượng oracle.")
    ]
    iy = 280
    for it, idesc in insights:
        draw.text((rx + 30, iy), it, font=get_font(FONT_UI_BOLD, 17), fill=(30, 30, 30))
        draw.text((rx + 30, iy + 24), idesc, font=get_font(FONT_UI, 15), fill=(70, 70, 70))
        iy += 68

    draw_subtitles(img, "Khối quan trọng nhất là Human Review Gate. Generator sinh 12 case, nhưng bảng cuối có 42 case. Chênh lệch là phần con người audit và bổ sung!", "Beat 6b — Cổng Human Review Gate")
    return img


def render_beat6c_frame() -> Image.Image:
    img = Image.new("RGBA", (WIDTH, HEIGHT), (240, 242, 245, 255))
    draw = ImageDraw.Draw(img)

    diag = Image.open("hw06/test-generator/diagram.png").convert("RGBA")
    diag_h = 920
    diag_w = int(diag.width * (diag_h / diag.height))
    diag_resized = diag.resize((diag_w, diag_h), Image.Resampling.LANCZOS)
    img.paste(diag_resized, (80, 50), diag_resized)

    # Highlight Test Generator & Output
    draw.rounded_rectangle([70, 680, 80 + diag_w + 10, 950], radius=10, fill=None, outline=(40, 167, 69), width=5)

    rx = 80 + diag_w + 50
    rw = WIDTH - rx - 50
    draw.rounded_rectangle([rx, 80, rx + rw, 520], radius=14, fill=(255, 255, 255), outline=(240, 136, 62), width=2)

    draw.text((rx + 30, 105), "🎯 VÍ DỤ THỰC TẾ: TC-API-LOGIN-039 (BUG D-LOGIN-03)", font=get_font(FONT_UI_BOLD, 22), fill=(217, 83, 79))
    draw.line([rx + 30, 145, rx + rw - 30, 145], fill=(220, 220, 220), width=1)

    # Case info card
    draw.rounded_rectangle([rx + 30, 165, rx + rw - 30, 310], radius=10, fill=(253, 242, 242), outline=(217, 83, 79), width=1)
    draw.text((rx + 50, 180), "Test Case ID: TC-API-LOGIN-039", font=get_font(FONT_CODE_BOLD, 18), fill=(217, 83, 79))
    draw.text((rx + 50, 210), "Mục tiêu: Kiểm tra response KHÔNG ĐƯỢC chứa trường 'password'", font=get_font(FONT_UI_BOLD, 16), fill=(30, 30, 30))
    draw.text((rx + 50, 240), "Assertion: pm.expect(pm.response.json()).to.not.have.property('password')", font=get_font(FONT_CODE, 14), fill=(100, 100, 100))
    draw.text((rx + 50, 270), "Bug phát hiện: D-LOGIN-03 (GitHub Issue #415) — Lộ plain hash password!", font=get_font(FONT_UI_BOLD, 16), fill=(217, 83, 79))

    ex_text = [
        ("Tại sao Generator không tự nghĩ ra?", "Generator chỉ biết kiểm field nào PHẢI CÓ theo schema đặc tả."),
        ("Vai trò của Con Người:", "Người kiểm thử tự lập danh sách field BỊ CẤM (Sensitive Data Exposure)."),
        ("Giá trị thực tế:", "Case do người thêm chính là case bắt được bug bảo mật quan trọng!")
    ]
    ey = 330
    for eh, edesc in ex_text:
        draw.text((rx + 30, ey), eh, font=get_font(FONT_UI_BOLD, 16), fill=(0, 102, 204) if "Người" in eh else (30, 30, 30))
        draw.text((rx + 30, ey + 22), edesc, font=get_font(FONT_UI, 15), fill=(70, 70, 70))
        ey += 55

    draw_subtitles(img, "Ví dụ TC-API-LOGIN-039 kiểm response không chứa password. Generator chỉ biết field phải có; case này do em thêm và bắt được bug D-LOGIN-03, issue #415.", "Beat 6c — Ví dụ thực tế: Bug D-LOGIN-03")
    return img


def render_beat7_frame() -> Image.Image:
    # Outro / Conclusion Slide
    img = Image.new("RGBA", (WIDTH, HEIGHT), (13, 17, 23, 255))
    draw = ImageDraw.Draw(img)

    # Header
    draw.text((WIDTH // 2 - 400, 80), "TỔNG KẾT DEMO AGENT SKILL (R-10)", font=get_font(FONT_UI_BOLD, 36), fill=(88, 166, 255))
    draw.line([WIDTH // 2 - 400, 135, WIDTH // 2 + 400, 135], fill=(48, 54, 61), width=2)

    # 3 Summary Cards
    cards = [
        ("1. GENERATOR", "Tạo Scaffold có cấu trúc", "• Tự động hóa sinh test từ Spec\n• Phủ 4 kỹ thuật cơ bản\n• Xuất chuẩn Markdown & Postman", (56, 139, 253)),
        ("2. AUDIT HOOK", "Kiểm tra Tính nhất quán", "• Bắt lỗi ID trùng lặp\n• Bắt lỗi Expected rỗng\n• Đảm bảo Traceability 100%", (63, 185, 80)),
        ("3. HUMAN TESTER", "Oracle & Quyết định cuối", "• Thẩm định nghiệp vụ thực tế\n• Bổ sung Negative & Forbidden fields\n• Chịu trách nhiệm chất lượng cuối cùng", (240, 136, 62)),
    ]

    cx = 100
    card_w = (WIDTH - 200 - 60) // 3
    card_h = 360
    cy = 180

    for title, subtitle, desc, col in cards:
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=14, fill=(22, 27, 34), outline=col, width=2)
        draw.text((cx + 25, cy + 25), title, font=get_font(FONT_UI_BOLD, 22), fill=col)
        draw.text((cx + 25, cy + 58), subtitle, font=get_font(FONT_UI_BOLD, 18), fill=(240, 246, 252))
        draw.line([cx + 25, cy + 90, cx + card_w - 25, cy + 90], fill=(48, 54, 61), width=1)

        lines = desc.split("\n")
        ly = cy + 110
        for l in lines:
            draw.text((cx + 25, ly), l, font=get_font(FONT_UI, 16), fill=(201, 209, 217))
            ly += 35

        cx += card_w + 30

    # Student signature footer
    draw.rounded_rectangle([WIDTH // 2 - 420, 580, WIDTH // 2 + 420, 680], radius=12, fill=(20, 24, 35), outline=(56, 139, 253), width=1)
    draw.text((WIDTH // 2 - 380, 600), "Sinh viên: ĐẶNG ĐĂNG KHOA  |  MSSV: 23127207  |  Môn: Kiểm thử phần mềm", font=get_font(FONT_UI_BOLD, 20), fill=(255, 255, 255))
    draw.text((WIDTH // 2 - 200, 638), "Cảm ơn Thầy / Cô đã theo dõi phần demo!", font=get_font(FONT_UI, 18), fill=(126, 231, 135))

    draw_subtitles(img, "Tóm lại, generator tạo scaffold có cấu trúc và audit được, còn trách nhiệm oracle và kết luận cuối cùng vẫn thuộc về người kiểm thử. Em cảm ơn thầy/cô.", "Beat 7 — Kết")
    return img


def build_all_frames():
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    frames = {
        "beat1": render_beat1_frame(),
        "beat2a": render_beat2a_frame(),
        "beat2b": render_beat2b_frame(),
        "beat3": render_beat3_frame(),
        "beat4a": render_beat4a_frame(),
        "beat4b": render_beat4b_frame(),
        "beat5": render_beat5_frame(),
        "beat6a": render_beat6a_frame(),
        "beat6b": render_beat6b_frame(),
        "beat6c": render_beat6c_frame(),
        "beat7": render_beat7_frame(),
    }
    for k, frame in frames.items():
        p = FRAMES_DIR / f"{k}.png"
        frame.save(p)
        print(f"Rendered frame: {p}")


def build_video():
    CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    beat_ids = ["beat1", "beat2a", "beat2b", "beat3", "beat4a", "beat4b", "beat5", "beat6a", "beat6b", "beat6c", "beat7"]
    concat_list = BUILD_DIR / "concat.txt"
    concat_lines = []

    for b_id in beat_ids:
        img_p = FRAMES_DIR / f"{b_id}.png"
        aud_p = AUDIO_DIR / f"{b_id}.mp3"
        clip_p = CLIPS_DIR / f"{b_id}.mp4"

        # Create video clip with audio
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(img_p),
            "-i", str(aud_p),
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            str(clip_p)
        ]
        print(f"Encoding clip {b_id}...")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        concat_lines.append(f"file '{clip_p.resolve().as_posix()}'")

    concat_list.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")

    # Concatenate all clips into final video
    print("Concatenating clips into final video...")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(OUTPUT_VIDEO)
    ]
    subprocess.run(cmd_concat, check=True)
    print(f"SUCCESS: Final demo video generated at {OUTPUT_VIDEO}")


if __name__ == "__main__":
    build_all_frames()
    build_video()
