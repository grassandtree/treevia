# Python 3.11 기반 이미지
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사
COPY requirements.txt .

# Python 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 환경 변수 설정
ENV FLASK_APP=main.py
ENV PORT=8080

# 포트 노출
EXPOSE 8080

# 애플리케이션 실행 (gunicorn 사용)
# Gunicorn은 자동으로 0.0.0.0 호스트를 사용합니다.
# Cloud Run이 제공하는 PORT 환경 변수를 사용하도록 바인딩합니다.
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--workers", "1", "main:app"]
