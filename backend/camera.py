import os
import base64
import requests
from dotenv import load_dotenv

# .env 파일에 적은 비밀 키들을 프로그램에 로드해옵니다.
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def encode_image(image_path):
    """이미지 파일을 Base64 텍스트 스트링으로 변환합니다."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_with_openai(image_path="captured.jpg", mode="fall_check"):
    """
    OpenAI API를 사용해 가상/실제 캡처 이미지를 종합 판단합니다.
    mode: 'fall_check' (낙상 상태 판단) 또는 'gesture_sos' (손바닥 제스처 판단)
    """
    if not OPENAI_API_KEY:
        return {"status": "error", "message": "OpenAI API 키가 세팅되지 않았습니다."}

    if not os.path.exists(image_path):
        return {"status": "error", "message": "분석할 이미지 파일이 로컬에 없습니다."}

    base64_image = encode_image(image_path)
    
    if mode == "fall_check":
        prompt = (
            "당신은 독거노인 응급 모니터링 시스템의 AI입니다. "
            "제공된 이미지 속 노인이 바닥에 쓰러져 있거나 고통스러워하고 있는지 분석하세요. "
            "반드시 다음 JSON 형식으로만 답변하세요: "
            '{"is_emergency": true/false, "analysis": "상세 분석 내용 요약"}'
        )
    else:  # gesture_sos
        prompt = (
            "제공된 이미지 속 인물이 카메라를 향해 '손바닥을 명확히 펼쳐 보이고 있는 SOS 신호'를 보내고 있나요? "
            "반드시 다음 JSON 형식으로만 답변하세요: "
            '{"sos_detected": true/false, "confidence": 0.0~1.0}'
        )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ],
        "response_format": {"type": "json_object"},
        "max_tokens": 300
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return {"status": "error", "message": str(e)}