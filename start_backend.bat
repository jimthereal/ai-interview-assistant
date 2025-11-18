@echo off
echo Starting AI Interview Assistant Backend...
echo.
echo IMPORTANT: This window must stay open!
echo.
C:\Users\Jimmy\anaconda3\envs\ai-interview-assistant\python.exe -m uvicorn api.main:app --reload
pause
