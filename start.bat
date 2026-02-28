@echo off
start /b python server.py
timeout /t 2 /nobreak >nul
echo Server started
