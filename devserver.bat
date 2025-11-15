@echo off
REM Windows용 Flask 개발 서버 실행 스크립트

REM .env 파일에서 PORT 값을 읽어 환경 변수로 설정
for /f "tokens=1,2 delims==" %%a in ('findstr /R /C:"^PORT=" .env') do (
    if /i "%%a"=="PORT" set "PORT=%%b"
)

REM PORT 값이 .env 파일에 없거나 설정되지 않았을 경우 기본값(5000)으로 설정
if not defined PORT set "PORT=5000"

REM 가상환경 활성화
call .venv\Scripts\activate.bat

REM Flask 서버 실행
echo Starting Flask server on port %PORT%...
python -u -m flask --app main run -p %PORT% --debug
