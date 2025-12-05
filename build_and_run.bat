@echo off
cls
echo.
echo ================================================================
echo    BUILDING FRONTEND AND STARTING FULL STACK APPLICATION
echo ================================================================
echo.
echo This will:
echo   1. Build the React frontend
echo   2. Start the Flask server (serves both frontend and backend)
echo.
echo ================================================================
echo.

echo [1/3] Building Frontend...
cd frontend
if not exist node_modules (
    echo Installing frontend dependencies...
    call npm install
)
echo Building React app...
call npm run build
if errorlevel 1 (
    echo ERROR: Frontend build failed!
    pause
    exit /b 1
)

cd ..
echo.
echo [2/3] Frontend built successfully!
echo.
echo [3/3] Starting Full Stack Server...
echo.

cd backend
python app.py

pause

