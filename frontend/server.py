import os
import sys
from flask import Flask, jsonify, render_template

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.sensor import read_sensors

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def get_live_status():
    """실시간 센서 데이터를 프론트엔드에 JSON으로 제공하는 API"""
    sensor_data = read_sensors()
    
    status_level = "ok"
    status_text = "어르신이 거실에서 평소처럼 활동 중입니다."
    
    if sensor_data['sound'] == 1 and sensor_data['motion'] == 0:
        status_level = "warning"
        status_text = "쿵 소리가 감지되었으나 움직임이 없습니다! 확인이 필요합니다."
        
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