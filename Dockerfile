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
ENV PORT=5000
ENV PYTHONUNBUFFERED=1

# 포트 노출
EXPOSE 5000

# 애플리케이션 실행
CMD ["python", "main.py"]
