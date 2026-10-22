@echo off
REM =====================================================================
REM VERDURE Native Android APK Build Script (Capacitor)
REM Packages the VERDURE PWA into a native Android Studio project and APK
REM =====================================================================

echo [VERDURE] Starting Native Android APK Packaging...

where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js and npm are required. Please install Node.js from https://nodejs.org/
    exit /b 1
)

echo [1/4] Installing Capacitor dependencies...
call npm install --save-dev @capacitor/core @capacitor/cli @capacitor/android @capacitor/camera @capacitor/haptics

echo [2/4] Initializing Capacitor configuration...
if not exist "capacitor.config.json" (
    call npx cap init "VERDURE" "org.verdure.leafdoctor" --web-dir .
)

echo [3/4] Adding Android native platform...
if not exist "android" (
    call npx cap add android
)

echo [4/4] Copying web assets and syncing native project...
call npx cap sync android

echo.
echo =====================================================================
echo  VERDURE Android Project Synced Successfully!
echo =====================================================================
echo To build the final APK:
echo   1. Run: npx cap open android
echo   2. In Android Studio: Build -> Build Bundle(s) / APK(s) -> Build APK(s)
echo   3. Output APK will be at: android\app\build\outputs\apk\debug\app-debug.apk
echo =====================================================================
pause
