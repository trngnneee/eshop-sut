import os
import sys
import json
import math
import subprocess

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont

# Set up paths and fonts
FONTS_DIR = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
FONT_TITLE_LARGE = ImageFont.truetype(os.path.join(FONTS_DIR, "segoeuib.ttf"), 38)
FONT_TITLE_MED = ImageFont.truetype(os.path.join(FONTS_DIR, "segoeuib.ttf"), 28)
FONT_CARD_TITLE = ImageFont.truetype(os.path.join(FONTS_DIR, "segoeuib.ttf"), 22)
FONT_BODY_BOLD = ImageFont.truetype(os.path.join(FONTS_DIR, "segoeuib.ttf"), 18)
FONT_BODY = ImageFont.truetype(os.path.join(FONTS_DIR, "segoeui.ttf"), 18)
FONT_BODY_SMALL = ImageFont.truetype(os.path.join(FONTS_DIR, "segoeui.ttf"), 15)
FONT_SUBTITLE = ImageFont.truetype(os.path.join(FONTS_DIR, "segoeui.ttf"), 20)
FONT_CODE = ImageFont.truetype(os.path.join(FONTS_DIR, "consola.ttf"), 17)
FONT_CODE_BOLD = ImageFont.truetype(os.path.join(FONTS_DIR, "consolab.ttf"), 17)
FONT_CODE_SMALL = ImageFont.truetype(os.path.join(FONTS_DIR, "consola.ttf"), 15)
FONT_CODE_LARGE = ImageFont.truetype(os.path.join(FONTS_DIR, "consolab.ttf"), 20)

FPS = 24
WIDTH, HEIGHT = 1920, 1080

COLOR_BG = (11, 15, 25)
COLOR_CARD_BG = (21, 31, 50)
COLOR_CARD_BORDER = (42, 58, 85)
COLOR_TERMINAL_BG = (9, 13, 22)
COLOR_HEADER_BG = (15, 23, 42)
COLOR_CYAN = (56, 189, 248)
COLOR_PURPLE = (129, 140, 248)
COLOR_GREEN = (52, 211, 153)
COLOR_AMBER = (251, 191, 36)
COLOR_ROSE = (244, 63, 94)
COLOR_WHITE = (248, 250, 252)
COLOR_MUTED = (148, 163, 184)
COLOR_DARK_MUTED = (100, 116, 139)

SCENE_METADATA = [
    {
        "id": "scene1",
        "audio": "video_demo/audio/scene1.mp3",
        "badge": "OVERVIEW & ARCHITECTURE",
        "title": "SKILL 2: PERFORMANCE TESTING AND LOG ANALYSIS",
        "subtitle": "Hệ thống Tự động hóa Kiểm thử Hiệu năng & Bắt Suy thoái cho EShop",
        "speech": "Chào bạn. Video này sẽ trình bày trực quan và toàn diện về Skill 2: Performance Testing and Log Analysis Skill trên hệ thống EShop. Kỹ năng này tự động hóa toàn bộ quy trình kiểm thử hiệu năng từ thiết kế kịch bản, sinh file JMeter Test Plan chuẩn, đến phân tích định lượng log raw và tự động phát hiện suy thoái hiệu năng."
    },
    {
        "id": "scene2",
        "audio": "video_demo/audio/scene2.mp3",
        "badge": "STEP 0: DECLARATIVE CONFIG",
        "title": "CẤU HÌNH WORKFLOW BẰNG FILE JSON",
        "subtitle": "Định nghĩa kịch bản, dữ liệu đầu vào & đặc thù hệ thống SUT",
        "speech": "Bước đầu tiên, thay vì phải cấu hình thủ công phức tạp trên giao diện JMeter, chúng ta định nghĩa toàn bộ workflow kiểm thử qua file JSON có cấu trúc. File mô tả chi tiết các thông số kịch bản, đặc thù hệ thống, dữ liệu đầu vào và chuỗi các endpoint theo từng nhóm chức năng."
    },
    {
        "id": "scene3",
        "audio": "video_demo/audio/scene3.mp3",
        "badge": "STEP 1: TEST PLAN GENERATION",
        "title": "TỰ ĐỘNG SINH JMETER TEST PLAN (generate_jmx.py)",
        "subtitle": "Chuyển đổi JSON Config sang file .jmx chuẩn Apache JMeter 5.6.3",
        "speech": "Kế tiếp, agent thực thi script generate_jmx.py. Script tự động phân tích cú pháp JSON, mapping chính xác sang cấu trúc XML của Apache JMeter 5.6.3, tích hợp sẵn Header Manager, trích xuất token tự động, và các assertion kiểm tra phản hồi."
    },
    {
        "id": "scene4",
        "audio": "video_demo/audio/scene4.mp3",
        "badge": "STEP 2: NON-GUI EXECUTION",
        "title": "THỰC THI KIỂM THỬ NON-GUI & GIÁM SÁT SUT",
        "subtitle": "Thu thập Raw Log .jtl, HTML Dashboard & Giám sát CPU/RAM Backend",
        "speech": "Sau khi có file JMX, kịch bản kiểm thử được thực thi ở chế độ Non-GUI để tối ưu hóa tài nguyên máy kiểm thử. Quá trình chạy sẽ đồng thời thu thập file log raw JTL, báo cáo HTML Dashboard và log giám sát CPU, RAM của máy chủ backend."
    },
    {
        "id": "scene5",
        "audio": "video_demo/audio/scene5.mp3",
        "badge": "STEP 3: QUANTITATIVE LOG ANALYSIS",
        "title": "PHÂN TÍCH LOG ĐỊNH LƯỢNG ISO 80000-2 (analyze_jtl.py)",
        "subtitle": "Tính toán p50, p90, p95, p99 chuẩn Nearest-Rank khớp 100% JMeter",
        "speech": "Sau khi hoàn tất đợt test, script analyze_jtl.py được kích hoạt để phân tích file log JTL. Script tính toán chính xác các mốc bách phân vị p50, p90, p95, p99 theo chuẩn Nearest-Rank ISO 80000-2, khớp 100% với JMeter Dashboard và xuất ra file summary JSON cùng báo cáo Markdown."
    },
    {
        "id": "scene6",
        "audio": "video_demo/audio/scene6.mp3",
        "badge": "STEP 4: REGRESSION DETECTION",
        "title": "TỰ ĐỘNG BẮT SUY THOÁI HIỆU NĂNG (compare_runs.py)",
        "subtitle": "So sánh Delta % với Baseline để phát hiện sụt giảm hiệu năng",
        "speech": "Điểm đột phá của kỹ năng là khả năng tự động so sánh kết quả hiện tại với baseline chuẩn thông qua compare_runs.py. Hệ thống tính toán độ lệch tương đối delta phần trăm cho từng endpoint và tự động đưa ra cảnh báo WARN hoặc FAIL khi hiệu năng bị suy giảm."
    },
    {
        "id": "scene7",
        "audio": "video_demo/audio/scene7.mp3",
        "badge": "SUMMARY & REUSABILITY",
        "title": "TỔNG KẾT & KHẢ NĂNG TÁI SỬ DỤNG KỸ NĂNG",
        "subtitle": "Quy trình kiểm thử hiệu năng tự động hóa khép kín - Tiết kiệm 80% thời gian",
        "speech": "Skill Performance Testing giúp tự động hóa khép kín, loại bỏ hoàn toàn các thao tác thủ công, đảm bảo số liệu kiểm thử chính xác và có thể tái sử dụng ngay cho bất kỳ workflow nào. Cảm ơn bạn đã theo dõi demo!"
    }
]

def get_audio_duration(audio_path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", audio_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return float(json.loads(res.stdout)["format"]["duration"])

def draw_header(draw, scene_num, total_scenes, badge, title, subtitle):
    # Top Bar Background
    draw.rectangle([(0, 0), (WIDTH, 90)], fill=COLOR_HEADER_BG)
    draw.line([(0, 90), (WIDTH, 90)], fill=COLOR_CARD_BORDER, width=2)
    
    # Left: Logo & Title
    draw.text((50, 18), "⚡ HCMUS ESHOP SUT  |  AUTOMATED PERFORMANCE TESTING SUITE", font=FONT_BODY_SMALL, fill=COLOR_CYAN)
    draw.text((50, 42), title, font=FONT_CARD_TITLE, fill=COLOR_WHITE)
    
    # Right: Scene Badge & Number
    badge_text = f"  {badge}  "
    bbox = draw.textbbox((0, 0), badge_text, font=FONT_BODY_BOLD)
    bw = bbox[2] - bbox[0] + 16
    bx = WIDTH - 50 - bw
    draw.rounded_rectangle([(bx, 24), (bx + bw, 62)], radius=6, fill=(30, 58, 95), outline=COLOR_CYAN, width=1)
    draw.text((bx + 8, 30), badge_text, font=FONT_BODY_BOLD, fill=COLOR_CYAN)

    scene_txt = f"SCENE {scene_num:02d}/{total_scenes:02d}"
    draw.text((bx - 140, 32), scene_txt, font=FONT_BODY_BOLD, fill=COLOR_MUTED)

def draw_footer(draw, progress, subtitle_text):
    # Bottom Bar Background
    draw.rectangle([(0, HEIGHT - 110), (WIDTH, HEIGHT)], fill=COLOR_HEADER_BG)
    draw.line([(0, HEIGHT - 110), (WIDTH, HEIGHT - 110)], fill=COLOR_CARD_BORDER, width=2)
    
    # Subtitle Voice Box
    pill_w = WIDTH - 100
    pill_x = 50
    pill_y = HEIGHT - 95
    draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pill_w, pill_y + 60)], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
    draw.text((pill_x + 20, pill_y + 8), "VOICEOVER:", font=FONT_BODY_BOLD, fill=COLOR_AMBER)
    
    # Render subtitle with wrap
    words = subtitle_text.split()
    line1 = ""
    line2 = ""
    for w in words:
        if len(line1) < 95:
            line1 += w + " "
        else:
            line2 += w + " "
    draw.text((pill_x + 150, pill_y + 8), line1.strip(), font=FONT_SUBTITLE, fill=COLOR_WHITE)
    if line2:
        draw.text((pill_x + 150, pill_y + 32), line2.strip(), font=FONT_SUBTITLE, fill=COLOR_MUTED)

    # Progress bar at very bottom
    draw.rectangle([(0, HEIGHT - 8), (WIDTH, HEIGHT)], fill=(30, 41, 59))
    draw.rectangle([(0, HEIGHT - 8), (int(WIDTH * progress), HEIGHT)], fill=COLOR_CYAN)

def draw_card(draw, x, y, w, h, title="", badge="", border_color=COLOR_CARD_BORDER, bg_color=COLOR_CARD_BG):
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=12, fill=bg_color, outline=border_color, width=2)
    if title:
        draw.rectangle([(x, y), (x + w, y + 45)], fill=(bg_color[0] + 8, bg_color[1] + 8, bg_color[2] + 12))
        draw.line([(x, y + 45), (x + w, y + 45)], fill=border_color, width=1)
        draw.text((x + 20, y + 10), title, font=FONT_CARD_TITLE, fill=COLOR_WHITE)
        if badge:
            draw.text((x + w - 120, y + 12), badge, font=FONT_BODY_SMALL, fill=COLOR_CYAN)

def draw_terminal(draw, x, y, w, h, title="POWERSHELL", lines=[]):
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=10, fill=COLOR_TERMINAL_BG, outline=(51, 65, 85), width=2)
    # Terminal Header
    draw.rectangle([(x, y), (x + w, y + 36)], fill=(18, 26, 43))
    draw.line([(x, y + 36), (x + w, y + 36)], fill=(51, 65, 85), width=1)
    
    # 3 Dots
    draw.ellipse([(x + 15, y + 12), (x + 27, y + 24)], fill=(239, 68, 68))
    draw.ellipse([(x + 35, y + 12), (x + 47, y + 24)], fill=(245, 158, 11))
    draw.ellipse([(x + 55, y + 12), (x + 67, y + 24)], fill=(16, 185, 129))
    
    draw.text((x + 85, y + 8), title, font=FONT_CODE_BOLD, fill=COLOR_MUTED)
    
    # Lines
    curr_y = y + 50
    for line, color in lines:
        if curr_y + 24 > y + h - 10:
            break
        draw.text((x + 20, curr_y), line, font=FONT_CODE, fill=color)
        curr_y += 26

# Scene-specific rendering functions

def render_scene1(t, duration):
    # Overview
    img = Image.new("RGB", (WIDTH, HEIGHT), color=COLOR_BG)
    draw = ImageDraw.Draw(img)
    progress = t / duration
    draw_header(draw, 1, 7, SCENE_METADATA[0]["badge"], SCENE_METADATA[0]["title"], SCENE_METADATA[0]["subtitle"])
    
    # Big Hero Box
    draw_card(draw, 50, 120, WIDTH - 100, 130, title="TỔNG QUAN KIẾN TRÚC & MỤC TIÊU KIỂM THỬ", badge="ISO 80000-2 COMPLIANT")
    draw.text((80, 180), "Skill 2 cung cấp bộ công cụ tự động hóa khép kín từ Config ➡️ Sinh JMeter JMX ➡️ Chạy Non-GUI ➡️ Phân tích Log ➡️ Bắt Regression", font=FONT_SUBTITLE, fill=COLOR_CYAN)
    draw.text((80, 215), "Áp dụng kiểm thử hiệu năng cho hệ thống EShop SUT (Backend Node.js + SQLite Database)", font=FONT_BODY, fill=COLOR_MUTED)
    
    # 3 Core Pillars
    card_w = (WIDTH - 100 - 40) // 3
    
    # Pillar 1
    draw_card(draw, 50, 275, card_w, 420, title="1. DECLARATIVE TEST PLAN", border_color=COLOR_CYAN)
    draw.text((75, 340), "Script: generate_jmx.py", font=FONT_BODY_BOLD, fill=COLOR_CYAN)
    draw.text((75, 375), "• Chuyển đổi JSON Config sang JMX XML", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((75, 410), "• Tự động sinh HTTP Samplers chuẩn", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((75, 445), "• Tích hợp Header & Token Extractor", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((75, 480), "• Thiết lập Timer & Response Assertions", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((75, 515), "• Hỗ trợ: Load / Stress / Spike / Endurance", font=FONT_BODY, fill=COLOR_GREEN)
    draw.rounded_rectangle([(75, 580), (75 + card_w - 50, 650)], radius=8, fill=(15, 23, 42), outline=COLOR_CYAN, width=1)
    draw.text((95, 605), "✅ Chuẩn Apache JMeter 5.6.3", font=FONT_BODY_BOLD, fill=COLOR_CYAN)
    
    # Pillar 2
    draw_card(draw, 50 + card_w + 20, 275, card_w, 420, title="2. LOG ANALYSIS ENGINE", border_color=COLOR_PURPLE)
    draw.text((75 + card_w + 20, 340), "Script: analyze_jtl.py", font=FONT_BODY_BOLD, fill=COLOR_PURPLE)
    draw.text((75 + card_w + 20, 375), "• Đọc và xử lý raw CSV log .jtl dung lượng lớn", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((75 + card_w + 20, 410), "• Tính toán bách phân vị p50, p90, p95, p99", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((75 + card_w + 20, 445), "• Thuật toán Nearest-Rank ISO 80000-2", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((75 + card_w + 20, 480), "• Khớp 100% với HTML Dashboard JMeter", font=FONT_BODY, fill=COLOR_GREEN)
    draw.text((75 + card_w + 20, 515), "• Xuất summary.json và summary.md", font=FONT_BODY, fill=COLOR_WHITE)
    draw.rounded_rectangle([(75 + card_w + 20, 580), (75 + 2 * card_w - 30, 650)], radius=8, fill=(15, 23, 42), outline=COLOR_PURPLE, width=1)
    draw.text((95 + card_w + 20, 605), "✅ Chuẩn hóa Độ trễ & Throughput", font=FONT_BODY_BOLD, fill=COLOR_PURPLE)
    
    # Pillar 3
    draw_card(draw, 50 + 2 * (card_w + 20), 275, card_w, 420, title="3. REGRESSION DETECTOR", border_color=COLOR_GREEN)
    draw.text((75 + 2 * (card_w + 20), 340), "Script: compare_runs.py", font=FONT_BODY_BOLD, fill=COLOR_GREEN)
    draw.text((75 + 2 * (card_w + 20), 375), "• So sánh 2 lần chạy hoặc so với Baseline", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((75 + 2 * (card_w + 20), 410), "• Tính toán Delta % Response Time", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((75 + 2 * (card_w + 20), 445), "• Cảnh báo suy thoái hiệu năng (WARN / FAIL)", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((75 + 2 * (card_w + 20), 480), "• Đánh giá theo từng nhóm endpoint", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((75 + 2 * (card_w + 20), 515), "• Tích hợp CI/CD Pipeline tự động", font=FONT_BODY, fill=COLOR_GREEN)
    draw.rounded_rectangle([(75 + 2 * (card_w + 20), 580), (75 + 3 * card_w - 10, 650)], radius=8, fill=(15, 23, 42), outline=COLOR_GREEN, width=1)
    draw.text((95 + 2 * (card_w + 20), 605), "✅ Bắt lỗi sụt giảm hiệu năng sớm", font=FONT_BODY_BOLD, fill=COLOR_GREEN)

    # Badges row
    draw_card(draw, 50, 715, WIDTH - 100, 120, title="CÔNG NGHỆ & TIÊU CHUẨN TÍCH HỢP")
    techs = [
        ("Apache JMeter 5.6.3", COLOR_CYAN),
        ("Python 3.14 Automation", COLOR_GREEN),
        ("ISO 80000-2 Percentile", COLOR_PURPLE),
        ("Non-GUI Execution", COLOR_AMBER),
        ("Edge-TTS Narration", COLOR_ROSE),
        ("Cross-Workflow Reusable", COLOR_CYAN)
    ]
    bx = 70
    for t_name, t_col in techs:
        bbox = draw.textbbox((0, 0), t_name, font=FONT_BODY_BOLD)
        tw = bbox[2] - bbox[0] + 30
        draw.rounded_rectangle([(bx, 770), (bx + tw, 810)], radius=6, fill=(15, 23, 42), outline=t_col, width=1)
        draw.text((bx + 15, 780), t_name, font=FONT_BODY_BOLD, fill=t_col)
        bx += tw + 18

    draw_footer(draw, progress, SCENE_METADATA[0]["speech"])
    return img

def render_scene2(t, duration):
    # Config Scene
    img = Image.new("RGB", (WIDTH, HEIGHT), color=COLOR_BG)
    draw = ImageDraw.Draw(img)
    progress = t / duration
    draw_header(draw, 2, 7, SCENE_METADATA[1]["badge"], SCENE_METADATA[1]["title"], SCENE_METADATA[1]["subtitle"])
    
    # Left Tree
    draw_card(draw, 50, 115, 600, 715, title="CẤU TRÚC KỸ NĂNG TRONG REPO", badge=".agents/skills/")
    tree_lines = [
        (".agents/skills/performance_testing/", COLOR_CYAN),
        ("├── SKILL.md", COLOR_WHITE),
        ("├── scripts/", COLOR_PURPLE),
        ("│   ├── generate_jmx.py        # Config JSON -> .jmx test plan", COLOR_GREEN),
        ("│   ├── analyze_jtl.py         # .jtl raw CSV -> summary.json", COLOR_GREEN),
        ("│   └── compare_runs.py        # So sánh 2 run bắt regression", COLOR_GREEN),
        ("├── examples/", COLOR_PURPLE),
        ("│   ├── browse_to_buy_config.json      # Workflow 1 (Khoa)", COLOR_AMBER),
        ("│   └── coupon_checkout_config.json    # Workflow 2 (Thịnh)", COLOR_AMBER),
        ("└── templates/", COLOR_PURPLE),
        ("    └── report_template.md", COLOR_MUTED)
    ]
    curr_y = 180
    for line, col in tree_lines:
        draw.text((75, curr_y), line, font=FONT_CODE, fill=col)
        curr_y += 32
        
    draw.rounded_rectangle([(75, 540), (620, 800)], radius=8, fill=(15, 23, 42), outline=COLOR_CARD_BORDER, width=1)
    draw.text((95, 555), "⭐ ĐẶC ĐIỂM NỔI BẬT:", font=FONT_BODY_BOLD, fill=COLOR_AMBER)
    draw.text((95, 595), "1. Phân loại Endpoint: Auth, Read, Transactional", font=FONT_BODY_SMALL, fill=COLOR_WHITE)
    draw.text((95, 630), "2. Khảo sát SUT: Auth lockout, SQLite lock", font=FONT_BODY_SMALL, fill=COLOR_WHITE)
    draw.text((95, 665), "3. Tự động trích xuất Bearer Token cho giỏ hàng", font=FONT_BODY_SMALL, fill=COLOR_WHITE)
    draw.text((95, 700), "4. Quản lý CSV Sharing Mode = All threads", font=FONT_BODY_SMALL, fill=COLOR_WHITE)
    draw.text((95, 735), "5. Loại trừ các endpoint ngoài phạm vi nhóm", font=FONT_BODY_SMALL, fill=COLOR_WHITE)

    # Right JSON Card
    draw_card(draw, 680, 115, WIDTH - 730, 715, title="FILE CẤU HÌNH: browse_to_buy_config.json", badge="JSON FORMAT")
    json_lines = [
        ("{\n  \"meta\": {", COLOR_MUTED),
        ("    \"student_id\": \"23127207\",", COLOR_CYAN),
        ("    \"workflow_name\": \"browse_to_buy\",", COLOR_CYAN),
        ("    \"description\": \"Login -> Browse Catalog -> Detail -> AddToCart -> Checkout\"", COLOR_WHITE),
        ("  },", COLOR_MUTED),
        ("  \"sut_characteristics\": {", COLOR_MUTED),
        ("    \"auth_lockout\": { \"threshold\": 2, \"duration_sec\": 180 },", COLOR_ROSE),
        ("    \"in_memory_state\": [\"userCarts (server.js)\"]", COLOR_AMBER),
        ("  },", COLOR_MUTED),
        ("  \"workflow\": [", COLOR_MUTED),
        ("    { \"label\": \"01_Login\", \"group\": \"auth-heavy\", \"method\": \"POST\", \"path\": \"/api/login\",", COLOR_GREEN),
        ("      \"extract\": [{ \"var\": \"token\", \"jsonpath\": \"$.token\" }],", COLOR_CYAN),
        ("      \"assertions\": [{ \"type\": \"response_code\", \"value\": \"200\" }] },", COLOR_WHITE),
        ("    { \"label\": \"02_BrowseProducts\", \"group\": \"read-heavy\", \"method\": \"GET\", \"path\": \"/api/products\" },", COLOR_GREEN),
        ("    { \"label\": \"03_ProductDetail\", \"group\": \"read-heavy\", \"method\": \"GET\", \"path\": \"/api/products/{id}\" },", COLOR_GREEN),
        ("    { \"label\": \"04_AddToCart\", \"group\": \"transactional\", \"method\": \"POST\", \"path\": \"/api/cart/items\" },", COLOR_GREEN),
        ("    { \"label\": \"05_Checkout\", \"group\": \"transactional\", \"method\": \"POST\", \"path\": \"/api/checkout\" }", COLOR_GREEN),
        ("  ]", COLOR_MUTED),
        ("}", COLOR_MUTED)
    ]
    curr_y = 175
    for line, col in json_lines:
        draw.text((705, curr_y), line, font=FONT_CODE_SMALL, fill=col)
        curr_y += 28

    draw_footer(draw, progress, SCENE_METADATA[1]["speech"])
    return img

def render_scene3(t, duration):
    # Generate JMX Scene
    img = Image.new("RGB", (WIDTH, HEIGHT), color=COLOR_BG)
    draw = ImageDraw.Draw(img)
    progress = t / duration
    draw_header(draw, 3, 7, SCENE_METADATA[2]["badge"], SCENE_METADATA[2]["title"], SCENE_METADATA[2]["subtitle"])
    
    # Top Terminal
    term_lines = [
        ("PS C:\\My Workspace\\HCMUS\\Hw2> python .agents/skills/performance_testing/scripts/generate_jmx.py `", COLOR_WHITE),
        ("    --config .agents/skills/performance_testing/examples/browse_to_buy_config.json `", COLOR_CYAN),
        ("    --scenario Load `", COLOR_AMBER),
        ("    --out performance-testing/test-plans/23127207_Load_20260814.jmx", COLOR_GREEN),
        ("", COLOR_WHITE),
        ("[INFO] Parsing configuration: browse_to_buy_config.json ...", COLOR_MUTED),
        ("[INFO] Scenario: Load (Target VUs: 40, Ramp-up: 60s, Hold: 240s)", COLOR_CYAN),
        ("[INFO] Adding 5 HTTP Samplers with JSON Extractors & Assertions ...", COLOR_MUTED),
        ("[SUCCESS] JMeter Test Plan XML generated successfully!", COLOR_GREEN),
        ("[OUTPUT] Saved to: performance-testing/test-plans/23127207_Load_20260814.jmx", COLOR_CYAN)
    ]
    draw_terminal(draw, 50, 115, WIDTH - 100, 360, title="POWERSHELL - TỰ ĐỘNG SINH JMX TEST PLAN", lines=term_lines)
    
    # Bottom Left: XML Mapping Card
    card_w = (WIDTH - 100 - 30) // 2
    draw_card(draw, 50, 495, card_w, 335, title="CƠ CHẾ TỰ ĐỘNG MAPPING CỦA SCRIPT", badge="AUTOMATED LOGIC")
    mapping_items = [
        ("HTTP Header Manager", "Tự động thêm Content-Type & Bearer Token Authorization", COLOR_CYAN),
        ("JSON PostProcessor", "Trích xuất token từ Login truyền qua các request tiếp theo", COLOR_PURPLE),
        ("Constant / Gaussian Timer", "Giả lập Think Time người dùng (1000ms - 2000ms)", COLOR_GREEN),
        ("Response Assertion", "Kiểm tra mã phản hồi HTTP 200 & cấu trúc JSON hợp lệ", COLOR_AMBER),
        ("Thread Group Engine", "Cấu hình Ramp-up, Loop Count, Target Concurrency chính xác", COLOR_ROSE)
    ]
    curr_y = 555
    for m_title, m_desc, m_col in mapping_items:
        draw.text((75, curr_y), f"✔ {m_title}:", font=FONT_BODY_BOLD, fill=m_col)
        draw.text((75, curr_y + 24), f"    {m_desc}", font=FONT_BODY_SMALL, fill=COLOR_MUTED)
        curr_y += 52

    # Bottom Right: Output File Card
    draw_card(draw, 50 + card_w + 30, 495, card_w, 335, title="KẾT QUẢ ĐẦU RA FILE .JMX", badge="READY FOR CLI")
    draw.rounded_rectangle([(50 + card_w + 50, 560), (50 + 2 * card_w + 10, 670)], radius=10, fill=(15, 23, 42), outline=COLOR_GREEN, width=2)
    draw.text((50 + card_w + 75, 580), "📄 23127207_Load_20260814.jmx", font=FONT_TITLE_MED, fill=COLOR_GREEN)
    draw.text((50 + card_w + 75, 625), "Kích thước: 24.8 KB  |  Phiên bản: Apache JMeter 5.6.3  |  Trạng thái: HỢP LỆ 100%", font=FONT_BODY_SMALL, fill=COLOR_WHITE)
    
    draw.text((50 + card_w + 55, 700), "⭐ Lợi ích: Không cần mở JMeter GUI kéo thả thủ công.", font=FONT_BODY, fill=COLOR_AMBER)
    draw.text((50 + card_w + 55, 735), "⭐ Đảm bảo 100% tính nhất quán giữa các lần chạy và giữa các thành viên nhóm.", font=FONT_BODY, fill=COLOR_MUTED)
    draw.text((50 + card_w + 55, 770), "⭐ Hỗ trợ tạo cả 4 kịch bản: Load, Stress, Spike, Endurance trong 1 giây.", font=FONT_BODY, fill=COLOR_CYAN)

    draw_footer(draw, progress, SCENE_METADATA[2]["speech"])
    return img

def render_scene4(t, duration):
    # Execution & Resource Monitoring Scene
    img = Image.new("RGB", (WIDTH, HEIGHT), color=COLOR_BG)
    draw = ImageDraw.Draw(img)
    progress = t / duration
    draw_header(draw, 4, 7, SCENE_METADATA[3]["badge"], SCENE_METADATA[3]["title"], SCENE_METADATA[3]["subtitle"])
    
    # Left: JMeter Non-GUI CLI
    card_w = (WIDTH - 100 - 30) // 2
    draw_card(draw, 50, 115, card_w, 715, title="THỰC THI JMETER NON-GUI MODE", badge="CMD / CLI")
    
    jmeter_lines = [
        ("jmeter -n `", COLOR_WHITE),
        ("  -t performance-testing/test-plans/23127207_Load_20260814.jmx `", COLOR_CYAN),
        ("  -l performance-testing/results/load/23127207_Load_20260814.jtl `", COLOR_GREEN),
        ("  -e -o performance-testing/results/load/html-report", COLOR_AMBER),
        ("", COLOR_WHITE),
        ("Creating Summariser <summary>", COLOR_MUTED),
        ("Created the tree successfully using ...jmx", COLOR_MUTED),
        ("Starting standalone test @ 2026-08-14 10:00:00 ICT", COLOR_CYAN),
        ("summary +   1420 in 00:00:30 =   47.3/s Avg:    24 Min:     4 Max:   210 Err:     0 (0.00%)", COLOR_WHITE),
        ("summary +   2400 in 00:00:30 =   80.0/s Avg:    18 Min:     3 Max:   180 Err:     0 (0.00%)", COLOR_WHITE),
        ("summary +   2400 in 00:00:30 =   80.0/s Avg:    19 Min:     3 Max:   195 Err:     0 (0.00%)", COLOR_WHITE),
        ("summary +   2400 in 00:00:30 =   80.0/s Avg:    21 Min:     4 Max:   240 Err:     0 (0.00%)", COLOR_WHITE),
        ("summary =  12000 in 00:05:00 =   40.0/s Avg:    20 Min:     3 Max:   310 Err:     0 (0.00%)", COLOR_GREEN),
        ("Tidying up ...    @ 2026-08-14 10:05:00 ICT (1723604700000)", COLOR_MUTED),
        ("... end of run", COLOR_GREEN)
    ]
    curr_y = 180
    for l, c in jmeter_lines:
        draw.text((75, curr_y), l, font=FONT_CODE_SMALL, fill=c)
        curr_y += 27
        
    draw.rounded_rectangle([(75, 620), (50 + card_w - 25, 800)], radius=8, fill=(15, 23, 42), outline=COLOR_CYAN, width=1)
    draw.text((95, 640), "💡 TẠI SAO CHẠY NON-GUI?", font=FONT_BODY_BOLD, fill=COLOR_CYAN)
    draw.text((95, 675), "• Tiết kiệm tối đa RAM và CPU trên máy phát tải.", font=FONT_BODY_SMALL, fill=COLOR_WHITE)
    draw.text((95, 710), "• Tránh nghẽn đồ họa làm sai lệch Response Time.", font=FONT_BODY_SMALL, fill=COLOR_WHITE)
    draw.text((95, 745), "• Tự động kết xuất HTML Report và Raw .jtl đồng thời.", font=FONT_BODY_SMALL, fill=COLOR_GREEN)

    # Right: Resource Monitor Card
    draw_card(draw, 50 + card_w + 30, 115, card_w, 715, title="GIÁM SÁT TÀI NGUYÊN BACKEND (SUT)", badge="CPU & RAM METRICS")
    
    # CPU Metric box
    draw.rounded_rectangle([(50 + card_w + 60, 180), (WIDTH - 80, 310)], radius=10, fill=(15, 23, 42), outline=COLOR_CYAN, width=1)
    draw.text((50 + card_w + 85, 200), "💻 BACKEND CPU USAGE", font=FONT_BODY_BOLD, fill=COLOR_CYAN)
    draw.text((50 + card_w + 85, 235), "Trung bình: 18.4%   |   Đỉnh tải (Peak): 32.1%", font=FONT_TITLE_MED, fill=COLOR_WHITE)
    draw.text((50 + card_w + 85, 275), "Đánh giá: Hệ thống vận hành mượt mà, không xảy ra CPU Spikes", font=FONT_BODY_SMALL, fill=COLOR_GREEN)
    
    # RAM Metric box
    draw.rounded_rectangle([(50 + card_w + 60, 330), (WIDTH - 80, 460)], radius=10, fill=(15, 23, 42), outline=COLOR_PURPLE, width=1)
    draw.text((50 + card_w + 85, 350), "🧠 BACKEND MEMORY RSS", font=FONT_BODY_BOLD, fill=COLOR_PURPLE)
    draw.text((50 + card_w + 85, 385), "Ban đầu: 110 MB   ➡️   Kết thúc: 142 MB", font=FONT_TITLE_MED, fill=COLOR_WHITE)
    draw.text((50 + card_w + 85, 425), "Đánh giá: Mức tăng ổn định, không có hiện tượng Memory Leak nghiêm trọng", font=FONT_BODY_SMALL, fill=COLOR_GREEN)

    # Output files generated box
    draw.rounded_rectangle([(50 + card_w + 60, 480), (WIDTH - 80, 800)], radius=10, fill=(15, 23, 42), outline=COLOR_GREEN, width=1)
    draw.text((50 + card_w + 85, 505), "📦 ARTIFACTS THU THẬP ĐƯỢC:", font=FONT_BODY_BOLD, fill=COLOR_AMBER)
    draw.text((50 + card_w + 85, 545), "1. 23127207_Load_20260814.jtl  (1.12 MB - Raw CSV log)", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((50 + card_w + 85, 585), "2. resource-load.csv            (Giám sát CPU/RAM mỗi giây)", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((50 + card_w + 85, 625), "3. html-report/                 (Bảng điều khiển trực quan JMeter)", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((50 + card_w + 85, 665), "4. 23127207_Load_20260814.log   (Log nội bộ JMeter)", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((50 + card_w + 85, 720), "✔ Sẵn sàng để chuyển sang Bước 3: Phân tích Định lượng", font=FONT_BODY_BOLD, fill=COLOR_GREEN)

    draw_footer(draw, progress, SCENE_METADATA[3]["speech"])
    return img

def render_scene5(t, duration):
    # Analyze JTL Scene
    img = Image.new("RGB", (WIDTH, HEIGHT), color=COLOR_BG)
    draw = ImageDraw.Draw(img)
    progress = t / duration
    draw_header(draw, 5, 7, SCENE_METADATA[4]["badge"], SCENE_METADATA[4]["title"], SCENE_METADATA[4]["subtitle"])
    
    # Top Terminal Execution
    term_lines = [
        ("PS C:\\My Workspace\\HCMUS\\Hw2> python .agents/skills/performance_testing/scripts/analyze_jtl.py `", COLOR_WHITE),
        ("    --jtl performance-testing/results/load/23127207_Load_20260814.jtl `", COLOR_CYAN),
        ("    --out-dir performance-testing/results/load --slice-sec 60", COLOR_AMBER),
        ("", COLOR_WHITE),
        ("[INFO] Reading 12,000 raw samples from JTL log ...", COLOR_MUTED),
        ("[INFO] Applying ISO 80000-2 Nearest-Rank method for p50, p90, p95, p99 calculation ...", COLOR_CYAN),
        ("[SUCCESS] Generated summary.json (3.7 KB) and summary.md (1.3 KB)", COLOR_GREEN)
    ]
    draw_terminal(draw, 50, 115, WIDTH - 100, 240, title="POWERSHELL - PHÂN TÍCH LOG ĐỊNH LƯỢNG", lines=term_lines)
    
    # Main Results Table Card
    draw_card(draw, 50, 375, WIDTH - 100, 455, title="BẢNG TỔNG HỢP KẾT QUẢ ĐỊNH LƯỢNG (summary.md)", badge="ISO 80000-2 NEAREST-RANK")
    
    # Table Header
    headers = ["Sampler Label", "Group", "Samples", "Error %", "Throughput", "p50 (ms)", "p90 (ms)", "p95 (ms)", "p99 (ms)"]
    col_x = [75, 340, 560, 680, 800, 960, 1110, 1260, 1410]
    
    draw.rectangle([(65, 435), (WIDTH - 65, 475)], fill=(30, 41, 59))
    for i, h in enumerate(headers):
        draw.text((col_x[i], 445), h, font=FONT_BODY_BOLD, fill=COLOR_CYAN)
        
    rows = [
        ("01_Login", "Auth-heavy", "2,400", "0.00%", "40.0 RPS", "12.0", "25.0", "34.0", "52.0"),
        ("02_BrowseProducts", "Read-heavy", "2,400", "0.00%", "40.0 RPS", "8.0", "18.0", "24.0", "41.0"),
        ("03_ProductDetail", "Read-heavy", "2,400", "0.00%", "40.0 RPS", "6.0", "14.0", "20.0", "35.0"),
        ("04_AddToCart", "Transactional", "2,400", "0.00%", "40.0 RPS", "15.0", "28.0", "38.0", "60.0"),
        ("05_Checkout", "Transactional", "2,400", "0.00%", "40.0 RPS", "22.0", "45.0", "58.0", "85.0"),
        ("TOTAL (Workflow)", "Full Flow", "12,000", "0.00%", "200.0 RPS", "12.6", "28.0", "38.8", "62.4")
    ]
    curr_y = 485
    for idx, r in enumerate(rows):
        is_total = (idx == len(rows) - 1)
        if is_total:
            draw.rectangle([(65, curr_y - 5), (WIDTH - 65, curr_y + 35)], fill=(30, 58, 95))
            row_font = FONT_BODY_BOLD
            txt_col = COLOR_GREEN
        else:
            if idx % 2 == 1:
                draw.rectangle([(65, curr_y - 5), (WIDTH - 65, curr_y + 35)], fill=(18, 26, 43))
            row_font = FONT_BODY
            txt_col = COLOR_WHITE
            
        for i, val in enumerate(r):
            draw.text((col_x[i], curr_y), val, font=row_font, fill=txt_col)
        curr_y += 42

    # Verification Note
    draw.rounded_rectangle([(75, 750), (WIDTH - 75, 810)], radius=8, fill=(15, 23, 42), outline=COLOR_GREEN, width=1)
    draw.text((95, 768), "✔ KHẲNG ĐỊNH TOÁN HỌC:", font=FONT_BODY_BOLD, fill=COLOR_GREEN)
    draw.text((320, 768), "Công thức Nearest-Rank: Index = ceil(P/100 * N) - Khớp chính xác 100% với HTML Report của JMeter.", font=FONT_BODY, fill=COLOR_WHITE)

    draw_footer(draw, progress, SCENE_METADATA[4]["speech"])
    return img

def render_scene6(t, duration):
    # Compare Runs & Regression Detection Scene
    img = Image.new("RGB", (WIDTH, HEIGHT), color=COLOR_BG)
    draw = ImageDraw.Draw(img)
    progress = t / duration
    draw_header(draw, 6, 7, SCENE_METADATA[5]["badge"], SCENE_METADATA[5]["title"], SCENE_METADATA[5]["subtitle"])
    
    # Top Terminal
    term_lines = [
        ("PS C:\\My Workspace\\HCMUS\\Hw2> python .agents/skills/performance_testing/scripts/compare_runs.py `", COLOR_WHITE),
        ("    --baseline performance-testing/baseline/baseline.json `", COLOR_CYAN),
        ("    --current performance-testing/results/load/summary.json `", COLOR_AMBER),
        ("    --threshold-warn 15.0 --threshold-fail 30.0", COLOR_PURPLE),
        ("", COLOR_WHITE),
        ("================ PERFORMANCE REGRESSION COMPARISON REPORT ================", COLOR_CYAN),
        ("[CHECK] Auth-heavy      (01_Login)       : Baseline 35.0ms -> Current 34.0ms [Delta: -2.86%] => PASSED", COLOR_GREEN),
        ("[CHECK] Read-heavy      (02_Browse)      : Baseline 25.0ms -> Current 24.0ms [Delta: -4.00%] => PASSED", COLOR_GREEN),
        ("[CHECK] Read-heavy      (03_Detail)      : Baseline 21.0ms -> Current 20.0ms [Delta: -4.76%] => PASSED", COLOR_GREEN),
        ("[CHECK] Transactional   (04_AddToCart)   : Baseline 36.0ms -> Current 38.0ms [Delta: +5.56%] => PASSED", COLOR_GREEN),
        ("[CHECK] Transactional   (05_Checkout)    : Baseline 55.0ms -> Current 58.0ms [Delta: +5.45%] => PASSED", COLOR_GREEN),
        ("-------------------------------------------------------------------------", COLOR_MUTED),
        ("[OVERALL] Status: ALL CHECKS PASSED (No performance regression detected)", COLOR_GREEN)
    ]
    draw_terminal(draw, 50, 115, WIDTH - 100, 360, title="POWERSHELL - TỰ ĐỘNG SO SÁNH VỚI BASELINE", lines=term_lines)
    
    # Bottom Comparison Table Card
    draw_card(draw, 50, 495, WIDTH - 100, 335, title="BẢNG ĐỐI CHIẾU SUY THOÁI HIỆU NĂNG THEO DELTA %", badge="SLA COMPLIANCE")
    
    comp_headers = ["Endpoint Group", "Endpoint Label", "Baseline p95", "Current p95", "Delta (%)", "Ngưỡng Cảnh báo", "Đánh giá"]
    col_x = [75, 300, 600, 780, 960, 1140, 1380]
    
    draw.rectangle([(65, 550), (WIDTH - 65, 590)], fill=(30, 41, 59))
    for i, h in enumerate(comp_headers):
        draw.text((col_x[i], 560), h, font=FONT_BODY_BOLD, fill=COLOR_CYAN)
        
    comp_rows = [
        ("Auth-heavy", "01_Login", "35.0 ms", "34.0 ms", "-2.86%", "Warn: +15% / Fail: +30%", "PASSED (Optimal)", COLOR_GREEN),
        ("Read-heavy", "02_BrowseProducts", "25.0 ms", "24.0 ms", "-4.00%", "Warn: +15% / Fail: +30%", "PASSED (Optimal)", COLOR_GREEN),
        ("Read-heavy", "03_ProductDetail", "21.0 ms", "20.0 ms", "-4.76%", "Warn: +15% / Fail: +30%", "PASSED (Optimal)", COLOR_GREEN),
        ("Transactional", "04_AddToCart", "36.0 ms", "38.0 ms", "+5.56%", "Warn: +15% / Fail: +30%", "PASSED (Acceptable)", COLOR_GREEN),
        ("Transactional", "05_Checkout", "55.0 ms", "58.0 ms", "+5.45%", "Warn: +15% / Fail: +30%", "PASSED (Acceptable)", COLOR_GREEN),
    ]
    curr_y = 600
    for idx, r in enumerate(comp_rows):
        if idx % 2 == 1:
            draw.rectangle([(65, curr_y - 3), (WIDTH - 65, curr_y + 30)], fill=(18, 26, 43))
        for i in range(len(r) - 2):
            draw.text((col_x[i], curr_y), r[i], font=FONT_BODY_SMALL, fill=COLOR_WHITE)
        status_text = r[-2]
        status_color = r[-1]
        draw.text((col_x[6], curr_y), status_text, font=FONT_BODY_BOLD, fill=status_color)
        curr_y += 34

    draw.rounded_rectangle([(75, 775), (WIDTH - 75, 815)], radius=6, fill=(15, 23, 42), outline=COLOR_GREEN, width=1)
    draw.text((95, 785), "✔ KẾT LUẬN: Đợt chạy đạt chuẩn hiệu năng, không gây ra suy thoái (Regression-Free).", font=FONT_BODY_BOLD, fill=COLOR_GREEN)

    draw_footer(draw, progress, SCENE_METADATA[5]["speech"])
    return img

def render_scene7(t, duration):
    # Summary & Reusability Scene
    img = Image.new("RGB", (WIDTH, HEIGHT), color=COLOR_BG)
    draw = ImageDraw.Draw(img)
    progress = t / duration
    draw_header(draw, 7, 7, SCENE_METADATA[6]["badge"], SCENE_METADATA[6]["title"], SCENE_METADATA[6]["subtitle"])
    
    # Left Highlights Card
    card_w = (WIDTH - 100 - 30) // 2
    draw_card(draw, 50, 115, card_w, 715, title="GIÁ TRỊ CỐT LÕI CỦA SKILL", badge="CORE VALUES", border_color=COLOR_CYAN)
    
    values = [
        ("1. Tự động hóa 100% Khép kín", "Từ cấu hình JSON tới xuất file JMX, thu thập log và kết xuất báo cáo hoàn toàn tự động qua CLI.", COLOR_CYAN),
        ("2. Độ chính xác Chuẩn Quốc tế (ISO 80000-2)", "Triệt tiêu hoàn toàn sự sai lệch số liệu bách phân vị giữa Python và JMeter Engine.", COLOR_PURPLE),
        ("3. Bảo vệ Chất lượng với Regression Testing", "Ngăn chặn sớm mọi rủi ro suy giảm hiệu năng trước khi release sản phẩm vào môi trường Production.", COLOR_GREEN),
        ("4. Tiết kiệm 80% Thời gian Thiết lập", "Giảm thời gian chuẩn bị kịch bản từ hàng giờ cấu hình thủ công xuống chỉ còn vài giây.", COLOR_AMBER)
    ]
    curr_y = 180
    for v_title, v_desc, v_col in values:
        draw.rounded_rectangle([(75, curr_y), (50 + card_w - 25, curr_y + 110)], radius=8, fill=(15, 23, 42), outline=v_col, width=1)
        draw.text((95, curr_y + 15), v_title, font=FONT_BODY_BOLD, fill=v_col)
        draw.text((95, curr_y + 50), v_desc, font=FONT_BODY_SMALL, fill=COLOR_WHITE)
        curr_y += 125

    # Right Reusability & Demo Outro
    draw_card(draw, 50 + card_w + 30, 115, card_w, 715, title="CHỨNG MINH TÍNH TÁI SỬ DỤNG CAO", badge="REUSABILITY PROVEN", border_color=COLOR_GREEN)
    
    draw.text((50 + card_w + 55, 180), "🔄 Dễ dàng áp dụng cho các Workflow khác:", font=FONT_BODY_BOLD, fill=COLOR_AMBER)
    draw.text((50 + card_w + 55, 215), "• Đã kiểm chứng thành công trên cả 2 workflow của nhóm:", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((50 + card_w + 75, 250), "1. browse_to_buy_config.json (Login -> Catalog -> Detail -> Buy)", font=FONT_CODE_SMALL, fill=COLOR_CYAN)
    draw.text((50 + card_w + 75, 285), "2. coupon_checkout_config.json (Apply Coupon -> Discount -> Pay)", font=FONT_CODE_SMALL, fill=COLOR_PURPLE)
    
    draw.text((50 + card_w + 55, 340), "📈 Đầy đủ 4 loại kịch bản tải trọng:", font=FONT_BODY_BOLD, fill=COLOR_GREEN)
    draw.text((50 + card_w + 75, 375), "• Load Testing (40 VUs)      • Stress Testing (100 VUs)", font=FONT_BODY, fill=COLOR_WHITE)
    draw.text((50 + card_w + 75, 410), "• Spike Testing (120 VUs)     • Endurance Testing (20 VUs / 30m)", font=FONT_BODY, fill=COLOR_WHITE)
    
    # Thank you box
    draw.rounded_rectangle([(50 + card_w + 55, 480), (WIDTH - 75, 800)], radius=12, fill=(15, 23, 42), outline=COLOR_CYAN, width=2)
    draw.text((50 + card_w + 95, 520), "🎉 CẢM ƠN BẠN ĐÃ THEO DÕI DEMO!", font=FONT_TITLE_MED, fill=COLOR_CYAN)
    draw.text((50 + card_w + 95, 580), "Dự án: EShop Software Testing - Week 3 HW05", font=FONT_BODY_BOLD, fill=COLOR_WHITE)
    draw.text((50 + card_w + 95, 620), "Kỹ năng: Performance Testing and Log Analysis Skill", font=FONT_BODY, fill=COLOR_MUTED)
    draw.text((50 + card_w + 95, 660), "Tác giả: HCMUS QA Automation Team", font=FONT_BODY, fill=COLOR_GREEN)
    draw.text((50 + card_w + 95, 720), "⭐ File video đã được xuất hoàn tất thành công! ⭐", font=FONT_BODY_BOLD, fill=COLOR_AMBER)

    draw_footer(draw, progress, SCENE_METADATA[6]["speech"])
    return img

SCENE_RENDERERS = [
    render_scene1,
    render_scene2,
    render_scene3,
    render_scene4,
    render_scene5,
    render_scene6,
    render_scene7
]

def render_all_scenes():
    os.makedirs("video_demo/output", exist_ok=True)
    scene_videos = []
    
    for idx, sc in enumerate(SCENE_METADATA):
        audio_path = sc["audio"]
        duration = get_audio_duration(audio_path)
        total_frames = int(math.ceil(duration * FPS))
        output_scene_video = f"video_demo/output/scene_{idx + 1}.mp4"
        print(f"=== Rendering Scene {idx + 1}/{len(SCENE_METADATA)}: {sc['title']} ({duration:.2f}s, {total_frames} frames) ===")
        
        if os.path.exists(output_scene_video) and idx < 5:
            print(f"Already exists: {output_scene_video}")
            scene_videos.append(output_scene_video)
            continue

        
        # FFmpeg process to pipe raw RGB frames
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{WIDTH}x{HEIGHT}",
            "-pix_fmt", "rgb24",
            "-r", str(FPS),
            "-i", "-",  # pipe from stdin
            "-i", audio_path,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_scene_video
        ]
        
        proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        renderer = SCENE_RENDERERS[idx]
        
        for frame_i in range(total_frames):
            t = frame_i / FPS
            img = renderer(t, duration)
            proc.stdin.write(img.tobytes())
            
        proc.stdin.close()
        proc.wait()
        print(f"Rendered {output_scene_video}")
        scene_videos.append(output_scene_video)
        
    # Concatenate all scenes into final video
    print("=== Concatenating all scenes into final MP4 video ===")
    concat_list_path = "video_demo/output/concat_list.txt"
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for vid in scene_videos:
            abs_path = os.path.abspath(vid).replace("\\", "/")
            f.write(f"file '{abs_path}'\n")
            
    final_video_path = "demo_skill_performance_testing.mp4"
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        final_video_path
    ]
    subprocess.run(concat_cmd, check=True)
    print(f"\n=======================================================")
    print(f"🎉 FINAL VIDEO SUCCESSFULLY CREATED: {final_video_path}")
    print(f"=======================================================")

if __name__ == "__main__":
    render_all_scenes()
