@echo off
title WavePulse RF - Backend & React Frontend Launcher
echo Starting FastAPI Backend on http://localhost:8000 ...
start "WavePulse Backend (FastAPI)" cmd /k "python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

echo Starting React Frontend on http://localhost:5173 ...
cd frontend
start "WavePulse Frontend (React + Vite)" cmd /k "npm run dev"

timeout /t 4 >nul
start http://localhost:5173
echo Done! Open http://localhost:5173 in your browser.

