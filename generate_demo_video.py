import asyncio
import os
import subprocess
import json
import edge_tts

VOICE = "vi-VN-NamMinhNeural"
OUTPUT_DIR = "video_demo"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "audio"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "frames"), exist_ok=True)

SCENES = [
    {
        "id": "scene1",
        "title": "GIỚI THIỆU SKILL KIỂM THỬ HIỆU NĂNG",
        "subtitle": "Performance Testing & Log Analysis Skill",
        "text": "Chào bạn. Video này sẽ trình bày trực quan và toàn diện về Skill 2: Performance Testing and Log Analysis Skill trên hệ thống EShop. Kỹ năng này tự động hóa toàn bộ quy trình kiểm thử hiệu năng từ thiết kế kịch bản, sinh file JMeter Test Plan chuẩn, đến phân tích định lượng log raw và tự động phát hiện suy thoái hiệu năng."
    },
    {
        "id": "scene2",
        "title": "CẤU HÌNH WORKFLOW BẰNG FILE JSON",
        "subtitle": "Declarative Workflow Configuration",
        "text": "Bước đầu tiên, thay vì phải cấu hình thủ công phức tạp trên giao diện JMeter, chúng ta định nghĩa toàn bộ workflow kiểm thử qua file JSON có cấu trúc. File mô tả chi tiết các thông số kịch bản, đặc thù hệ thống, dữ liệu đầu vào và chuỗi các endpoint theo từng nhóm chức năng."
    },
    {
        "id": "scene3",
        "title": "BƯỚC 1: SINH JMETER TEST PLAN TỰ ĐỘNG",
        "subtitle": "Tự động tạo file .jmx từ config JSON",
        "text": "Kế tiếp, agent thực thi script generate_jmx.py. Script tự động phân tích cú pháp JSON, mapping chính xác sang cấu trúc XML của Apache JMeter 5.6.3, tích hợp sẵn Header Manager, trích xuất token tự động, và các assertion kiểm tra phản hồi."
    },
    {
        "id": "scene4",
        "title": "BƯỚC 2: THỰC THI & GIÁM SÁT HỆ THỐNG",
        "subtitle": "JMeter Non-GUI Execution & Resource Monitoring",
        "text": "Sau khi có file JMX, kịch bản kiểm thử được thực thi ở chế độ Non-GUI để tối ưu hóa tài nguyên máy kiểm thử. Quá trình chạy sẽ đồng thời thu thập file log raw JTL, báo cáo HTML Dashboard và log giám sát CPU, RAM của máy chủ backend."
    },
    {
        "id": "scene5",
        "title": "BƯỚC 3: PHÂN TÍCH LOG ĐỊNH LƯỢNG ISO 80000-2",
        "subtitle": "Phân tích p50, p90, p95, p99 từ raw .jtl",
        "text": "Sau khi hoàn tất đợt test, script analyze_jtl.py được kích hoạt để phân tích file log JTL. Script tính toán chính xác các mốc bách phân vị p50, p90, p95, p99 theo chuẩn Nearest-Rank ISO 80000-2, khớp 100% với JMeter Dashboard và xuất ra file summary JSON cùng báo cáo Markdown."
    },
    {
        "id": "scene6",
        "title": "BƯỚC 4: TỰ ĐỘNG BẮT SUY THOÁI HIỆU NĂNG",
        "subtitle": "So sánh Delta % với Baseline",
        "text": "Điểm đột phá của kỹ năng là khả năng tự động so sánh kết quả hiện tại với baseline chuẩn thông qua compare_runs.py. Hệ thống tính toán độ lệch tương đối delta phần trăm cho từng endpoint và tự động đưa ra cảnh báo WARN hoặc FAIL khi hiệu năng bị suy giảm."
    },
    {
        "id": "scene7",
        "title": "TỔNG KẾT & KHẢ NĂNG TÁI SỬ DỤNG",
        "subtitle": "Tự động hóa chuẩn mực - Tiết kiệm 80% thời gian",
        "text": "Skill Performance Testing giúp tự động hóa khép kín, loại bỏ hoàn toàn các thao tác thủ công, đảm bảo số liệu kiểm thử chính xác và có thể tái sử dụng ngay cho bất kỳ workflow nào. Cảm ơn bạn đã theo dõi demo!"
    }
]

async def generate_audios():
    for sc in SCENES:
        audio_path = os.path.join(OUTPUT_DIR, "audio", f"{sc['id']}.mp3")
        communicate = edge_tts.Communicate(sc['text'], VOICE, rate="+5%")
        await communicate.save(audio_path)
        print(f"Generated {audio_path}")

if __name__ == "__main__":
    asyncio.run(generate_audios())
