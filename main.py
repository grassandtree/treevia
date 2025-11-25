import os
from flask import Flask, send_file, redirect, url_for, session, request, jsonify
from flask_session import Session
from google.auth.transport.requests import Request
from google.oauth2.id_token import verify_oauth2_token
import json
from database import init_db, insert_or_update_user, insert_login_history, get_login_history, debug_db_state

app = Flask(__name__)

# Session 설정
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
Session(app)

# 구글 OAuth 클라이언트 ID (Google Cloud Console에서 발급)
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID')

# 앱 시작 시 데이터베이스 초기화
init_db()

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
        
        # 사용자 정보
        user_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo['name']
        picture = idinfo['picture']
        
        print(f"\n[로그인] 사용자: {email} ({user_id})")
        
        # 데이터베이스에 사용자 정보 저장 (insert or update)
        result1 = insert_or_update_user(user_id, email, name, picture)
        print(f"[DB] 사용자 정보 저장: {result1}")
        
        # 로그인 이력 기록
        result2 = insert_login_history(user_id, email, name, picture)
        print(f"[DB] 로그인 이력 기록: {result2}")
        
        # 세션에 사용자 정보 저장
        session['user'] = {
            'id': user_id,
            'email': email,
            'name': name,
            'picture': picture
        }
        
        return {'status': 'success', 'user': session['user']}
    except Exception as e:
        print(f"[오류] 로그인 처리 중 오류: {e}")
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

@app.route("/user/login-history")
def get_user_login_history():
    """현재 사용자의 로그인 이력 반환"""
    user = session.get('user')
    if not user:
        return {'status': 'not_logged_in'}, 401
    
    history = get_login_history(user['id'], limit=10)
    return {
        'user_id': user['id'],
        'history': [
            {
                'id': h[0],
                'user_id': h[1],
                'email': h[2],
                'name': h[3],
                'login_at': str(h[4])
            }
            for h in history
        ]
    }

@app.route("/debug/db-state")
def debug_endpoint():
    """데이터베이스 상태 확인 (개발용)"""
    debug_db_state()
    return {'status': 'checked', 'message': '터미널을 확인하세요'}

def main():
    # 로컬 개발용: devserver.bat 또는 python -m flask run 사용을 권장
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)

if __name__ == "__main__":
    main()
