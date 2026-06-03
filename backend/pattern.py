import os
import csv
from datetime import datetime

# 데이터 저장 경로 설정
CSV_PATH = os.path.join(os.path.dirname(__file__), '../data/pattern.csv')

def init_pattern_csv():
    """CSV 파일과 저장 폴더가 없으면 새로 초기화합니다."""
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'date', 'time', 'motion_detected', 'temperature', 'humidity'])

def log_activity(motion, temp, hum):
    """실시간 센서 상태 정보를 CSV 파일에 한 줄씩 기록합니다."""
    init_pattern_csv()
    now = datetime.now()
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            now.timestamp(),
            now.strftime('%Y-%m-%d'),
            now.strftime('%H:%M:%S'),
            int(motion),
            temp,
            hum
        ])

def get_recent_patterns(limit=24):
    """대시보드 차트 출력용으로 최근 데이터 기록을 불러옵니다."""
    init_pattern_csv()
    records = []
    try:
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
    except Exception as e:
        print(f"CSV 파일 읽기 실패: {e}")
    return records[-limit:]