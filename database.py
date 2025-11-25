import duckdb
import os
from datetime import datetime

# DuckDB 데이터베이스 파일 경로
DB_PATH = os.path.join(os.path.dirname(__file__), 'treevia.duckdb')

def get_connection():
    """DuckDB 연결 반환"""
    return duckdb.connect(DB_PATH)

def init_db():
    """데이터베이스 초기화 및 테이블 생성"""
    conn = get_connection()
    
    # 시퀀스 먼저 생성
    try:
        conn.execute("DROP SEQUENCE IF EXISTS seq_login_history")
        conn.execute("CREATE SEQUENCE seq_login_history START 1")
        print("✓ Sequence created")
    except Exception as e:
        print(f"Sequence creation note: {e}")
    
    # users 테이블 생성
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR PRIMARY KEY,
            email VARCHAR UNIQUE NOT NULL,
            name VARCHAR NOT NULL,
            picture VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    """)
    
    # login_history 테이블 생성 (외래 키 제약 없이)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS login_history (
            id INTEGER PRIMARY KEY DEFAULT nextval('seq_login_history'),
            user_id VARCHAR NOT NULL,
            email VARCHAR NOT NULL,
            name VARCHAR NOT NULL,
            picture VARCHAR,
            login_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.close()

def insert_or_update_user(user_id, email, name, picture):
    """사용자 정보 insert or update"""
    conn = get_connection()
    
    try:
        from datetime import datetime
        now = datetime.now()
        
        # 사용자가 이미 존재하는지 확인
        existing = conn.execute(
            "SELECT id FROM users WHERE id = ?", 
            (user_id,)
        ).fetchone()
        
        if existing:
            # UPDATE
            conn.execute("""
                UPDATE users 
                SET last_login = ?
                WHERE id = ?
            """, (now, user_id))
        else:
            # INSERT
            conn.execute("""
                INSERT INTO users (id, email, name, picture, created_at, last_login)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, email, name, picture, now, now))
        
        conn.commit()
        print(f"✓ 사용자 정보 저장 성공: {email}")
        return True
    except Exception as e:
        print(f"✗ User insert/update error: {e}")
        return False
    finally:
        conn.close()

def insert_login_history(user_id, email, name, picture):
    """로그인 이력 기록"""
    conn = get_connection()
    
    try:
        from datetime import datetime
        now = datetime.now()
        
        conn.execute("""
            INSERT INTO login_history (user_id, email, name, picture, login_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, email, name, picture, now))
        
        conn.commit()
        print(f"✓ 로그인 이력 저장 성공: {email}")
        return True
    except Exception as e:
        print(f"✗ Login history insert error: {e}")
        return False
    finally:
        conn.close()

def get_user(user_id):
    """사용자 정보 조회"""
    conn = get_connection()
    
    try:
        result = conn.execute(
            "SELECT id, email, name, picture, created_at, last_login FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
        
        return result
    except Exception as e:
        print(f"User query error: {e}")
        return None
    finally:
        conn.close()

def get_login_history(user_id, limit=10):
    """사용자의 로그인 이력 조회"""
    conn = get_connection()
    
    try:
        results = conn.execute("""
            SELECT id, user_id, email, name, login_at
            FROM login_history
            WHERE user_id = ?
            ORDER BY login_at DESC
            LIMIT ?
        """, (user_id, limit)).fetchall()
        
        return results
    except Exception as e:
        print(f"Login history query error: {e}")
        return []
    finally:
        conn.close()

def get_all_users():
    """모든 사용자 조회"""
    conn = get_connection()
    
    try:
        results = conn.execute("""
            SELECT id, email, name, created_at, last_login
            FROM users
            ORDER BY last_login DESC
        """).fetchall()
        
        return results
    except Exception as e:
        print(f"Users query error: {e}")
        return []
    finally:
        conn.close()

def debug_db_state():
    """데이터베이스 상태 확인 (디버깅용)"""
    conn = get_connection()
    
    try:
        print("\n=== 데이터베이스 상태 ===")
        
        # users 테이블 확인
        users = conn.execute("SELECT * FROM users").fetchall()
        print(f"Users 테이블 행 수: {len(users)}")
        for user in users:
            print(f"  - {user}")
        
        # login_history 테이블 확인
        history = conn.execute("SELECT * FROM login_history").fetchall()
        print(f"Login_history 테이블 행 수: {len(history)}")
        for h in history:
            print(f"  - {h}")
            
    except Exception as e:
        print(f"Debug error: {e}")
    finally:
        conn.close()
