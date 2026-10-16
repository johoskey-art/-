@echo off
chcp 65001 > nul
echo ========================================================
echo   주가위치분석시스템 (Stock Position System) 대시보드 실행
echo ========================================================
cd /d "%~dp0"
streamlit run app.py
pause
