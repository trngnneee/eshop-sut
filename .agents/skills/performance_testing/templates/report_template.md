# Báo cáo Kiểm thử Hiệu năng — {{WORKFLOW_NAME}}

## 1. Thông tin Tổng quan
- **Mã sinh viên:** {{STUDENT_ID}}
- **Workflow:** {{WORKFLOW_NAME}}
- **Thời gian thực hiện:** {{EXECUTION_DATE}}
- **Công cụ:** Apache JMeter 5.6.3

## 2. Bảng Tóm tắt Kết quả Thực thi
| Kịch bản | Threads | Thời lượng | Tổng số mẫu | RPS | Tỉ lệ lỗi | p95 chính |
|:---|---:|---:|---:|---:|---:|---:|
| Load | {{LOAD_VU}} | {{LOAD_DUR}} | {{LOAD_SAMPLES}} | {{LOAD_RPS}} | {{LOAD_ERR}} | {{LOAD_P95}} |
| Stress | {{STRESS_VU}} | {{STRESS_DUR}} | {{STRESS_SAMPLES}} | {{STRESS_RPS}} | {{STRESS_ERR}} | {{STRESS_P95}} |
| Spike | {{SPIKE_VU}} | {{SPIKE_DUR}} | {{SPIKE_SAMPLES}} | {{SPIKE_RPS}} | {{SPIKE_ERR}} | {{SPIKE_P95}} |
| Endurance | {{ENDUR_VU}} | {{ENDUR_DUR}} | {{ENDUR_SAMPLES}} | {{ENDUR_RPS}} | {{ENDUR_ERR}} | {{ENDUR_P95}} |

## 3. Phân tích Chi tiết từng Endpoint
{{LABEL_ANALYSIS_TABLE}}

## 4. Ngưỡng Phần cứng và Bộ nhớ
- **Trần bộ nhớ:** {{MAX_MEMORY_MB}} MB
- **Tốc độ rò rỉ:** {{LEAK_RATE_MB_PER_MIN}} MB/phút
- **Điểm gãy hệ thống:** {{BREAKING_POINT}}
