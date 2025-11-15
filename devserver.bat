@echo off
REM Windows용 Flask 개발 서버 실행 스크립트

REM 가상환경 활성화
call .venv\Scripts\activate.bat

REM Flask 서버 실행
REM python -u -m flask --app main run -p %PORT% --debug
python -u -m flask --app main run -p 8080 --debug
