import os
from flask import Flask, render_template

# Flask 앱 설정 (templates 폴더 위치 지정)
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    # templates 폴더 안의 index.html을 찾아서 브라우저에 띄워줍니다
    return render_template('index.html')

if __name__ == '__main__':
    # 5000번 포트로 디버그 모드 켜서 웹 서버 실행
    app.run(host='0.0.0.0', port=5000, debug=True)