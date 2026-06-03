import os
import sys
from flask import Flask, jsonify, render_template

# 상위 폴더(..)에 있는 backend 모듈을 올바르게 참조하기 위한 경로 설정 [cite: 142]
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.sensor import read_sensors

app = Flask(__name__, template_folder='templates') # templates 폴더 연동 [cite: 142]

@app.route('/')
def index():
    # templates 폴더 안의 index.html을 웹 화면에 띄워줍니다 [cite: 142]
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def get_live_status():
    """실시간 센서 데이터를 프론트엔드에 JSON으로 제공하는 API"""
    sensor_data = read_sensors()
    
    status_level = "ok"
    status_text = "어르신이 거실에서 평소처럼 활동 중입니다." [cite: 35]
    
    # 쿵 소리가 났는데 움직임이 전혀 없는 위험 상황 판단 예시 [cite: 126]
    if sensor_data['sound'] == 1 and sensor_data['motion'] == 0:
        status_level = "warning"
        status_text = "쿵 소리가 감지되었으나 움직임이 없습니다! 확인이 필요합니다." [cite: 126]
        
    return jsonify({
        "status": status_level,
        "message": status_text,
        "temperature": sensor_data['temperature'],
        "humidity": sensor_data['humidity'],
        "motion_detected": bool(sensor_data['motion']),
        "sound_detected": bool(sensor_data['sound'])
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)