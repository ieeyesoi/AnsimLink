import time
import random

try:
    import RPi.GPIO as GPIO
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

def read_sensors():
    """PC 테스트용 가상 데이터를 반환하는 함수 (밤에 장비 연결 시 실제 GPIO 작동)"""
    mock_motion = random.choice([0, 1])
    mock_sound = random.choice([0, 1])
    mock_temp = round(random.uniform(22.0, 25.0), 1)
    mock_humidity = round(random.uniform(55.0, 65.0), 1)
    
    return {
        "motion": mock_motion,
        "sound": mock_sound,
        "temperature": mock_temp,
        "humidity": mock_humidity,
        "timestamp": time.time()
    }