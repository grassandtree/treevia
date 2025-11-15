import os
from flask import Flask, send_file, redirect, url_for, session, request
from flask_session import Session
from google.auth.transport.requests import Request
from google.oauth2.id_token import verify_oauth2_token
import json

app = Flask(__name__)

# Session 설정
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
Session(app)

# 구글 OAuth 클라이언트 ID (Google Cloud Console에서 발급)
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID')

@app.route("/")
def index():
    return send_file('src/index.html')

@app.route("/login")
def login():
    # 구글 로그인 페이지로 리다이렉트
    return send_file('src/login.html')

@app.route("/config/google-client-id")
def get_google_client_id():
    """클라이언트 ID 반환"""
    return {'client_id': GOOGLE_CLIENT_ID}

@app.route("/auth/google/callback", methods=['POST'])
def google_callback():
    """구글 로그인 콜백"""
    try:
        token = request.json.get('token')
        
        # 토큰 검증
        idinfo = verify_oauth2_token(token, Request(), GOOGLE_CLIENT_ID)
        
        # 세션에 사용자 정보 저장
        session['user'] = {
            'id': idinfo['sub'],
            'email': idinfo['email'],
            'name': idinfo['name'],
            'picture': idinfo['picture']
        }
        
        return {'status': 'success', 'user': session['user']}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 400

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/user")
def get_user():
    """현재 로그인한 사용자 정보 반환"""
    user = session.get('user')
    if user:
        return user
    return {'status': 'not_logged_in'}, 401

def main():
    app.run(port=int(os.environ.get('PORT', 5000)), debug=True)

if __name__ == "__main__":
    main()
