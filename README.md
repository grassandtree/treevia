# treevia
tree trivia

> 나무 사진을 보고 나무의 이름을 맞춰보세요. (TBD)

---

### 🌳 앱 소개 (TBD)

**Treevia**는 나무 도감에 있는 다양한 사진들을 보며 나무의 이름을 맞히는 재미있는 퀴즈 게임입니다. 나무 전문가가 되어 보세요!

### ✨ 주요 기능 (TBD)

* **랜덤 나무 퀴즈**: 방대한 나무 도감에서 사진을 무작위로 제시합니다.
* **쉽고 빠른 학습**: 사진과 함께 나무의 이름을 맞히며 자연스럽게 지식을 습득할 수 있습니다.
* **직관적인 인터페이스**: 누구나 쉽게 이용할 수 있도록 단순하고 깔끔한 화면을 제공합니다.
* **정답 해설**: 정답을 맞힌 후에는 해당 나무에 대한 간단한 설명을 볼 수 있습니다.

### 🎮 사용 방법 (TBD)

1.  앱을 실행하면 무작위로 선택된 나무 사진이 나타납니다.
2.  사진을 보고 아래 제시된 보기 중에서 정답을 선택하세요.
3.  정답을 맞히면 점수를 얻고, 틀려도 정답과 함께 설명을 확인할 수 있습니다.
4.  다음 문제로 넘어가 계속해서 퀴즈를 즐기세요!

### 💻 개발 환경 (TBD)

*   **Backend**
    *   **언어**: Python
    *   **프레임워크**: Flask
    *   **데이터베이스**: SQLAlchemy, SQLite (초기)
*   **Frontend (Mobile)**
    *   **언어**: Kotlin / Swift
    *   **프레임워크**: Android Studio / Xcode

### 🚀 실행 방법

#### 1. Google Cloud OAuth 설정

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성
3. **OAuth 2.0 클라이언트 ID** 생성
   - 애플리케이션 유형: **웹 애플리케이션**
   - 승인된 리다이렉션 URI:
     - `http://localhost/auth/google/callback`
     - `http://localhost:80/auth/google/callback`
4. **클라이언트 ID** 복사하여 `.env` 파일에 저장

#### 2. 환경 설정

```bash
# .env 파일 생성 (.env.example 참조)
GOOGLE_CLIENT_ID=your-google-client-id-here
SECRET_KEY=your-secret-key-change-this
PORT=80
```

#### 3. 가상 환경 생성 및 활성화

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

#### 4. 필요한 라이브러리 설치

```bash
pip install -r requirements.txt
```

#### 5. Flask 서버 실행

**Windows:**
```powershell
.\devserver.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
python -m flask --app main run --debug
```

또는 직접 실행:
```bash
python main.py
```

#### 6. 브라우저 접속

```
http://localhost/
```

### 🐳 Docker 실행 방법

#### Docker로 실행 (권장)

**전제 조건**: Docker와 Docker Compose 설치 필수

1. **`.env` 파일 확인**
   ```bash
   # .env 파일이 있는지 확인
   # 필요한 환경 변수 설정 확인
   ```

2. **Docker Compose로 실행**
   ```powershell
   docker-compose up --build
   ```

3. **브라우저 접속**
   ```
   http://localhost/
   ```

4. **중지하기**
   ```powershell
   docker-compose down
   ```

#### Docker 명령어 (Compose 없이)

```powershell
# 이미지 빌드
docker build -t treevia:latest .

# 컨테이너 실행
docker run -p 80:5000 --env-file .env treevia:latest

# 컨테이너 중지
docker stop <container-id>
```

#### Docker 유용한 명령어

```powershell
# 실행 중인 컨테이너 확인
docker ps

# 컨테이너 로그 확인
docker logs <container-id>

# 컨테이너 내부 접속
docker exec -it <container-id> bash

# 이미지 제거
docker rmi treevia:latest
```

### 🤝 기여하기 (TBD)

버그를 발견했거나 새로운 기능을 제안하고 싶으시면 언제든지 연락해 주세요. 여러분의 의견은 앱을 더 좋게 만드는 데 큰 도움이 됩니다.

---

**© 2025 Treevia Inc.**
