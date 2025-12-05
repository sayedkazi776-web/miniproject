@echo off
cls
echo.
echo ================================================================
echo    CROWD DENSITY MONITORING SYSTEM - STARTING ALL SERVERS
echo ================================================================
echo.
echo This will start both backend and frontend in separate windows.
echo.
echo Backend (API):  http://localhost:5000
echo Frontend (UI):  http://localhost:3000
echo.
echo IMPORTANT: 
echo   - Open your browser to: http://localhost:3000
echo   - Do NOT access http://localhost:5000 directly
echo.
echo ================================================================
echo.
pause

echo.
echo [1/2] Starting Backend Server...
start "Backend Server - Port 5000" cmd /k "cd /d %~dp0backend && python app.py"

echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

echo.
echo [2/2] Starting Frontend Server...
start "Frontend Server - Port 3000" cmd /k "cd /d %~dp0frontend && if not exist node_modules (echo Installing dependencies... && call npm install) && echo Starting frontend... && npm run dev"

echo.
echo ================================================================
echo                    SERVERS STARTING!
echo ================================================================
echo.
echo Backend API:     http://localhost:5000
echo Frontend App:    http://localhost:3000  ^<-- OPEN THIS!
echo.
echo Two new windows have opened:
echo   - Backend Server window
echo   - Frontend Server window
echo.
echo When both show "ready" messages, open:
echo   http://localhost:3000
echo.
echo ================================================================
echo.
echo Press any key to close this window (servers will keep running)...
pause >nul

