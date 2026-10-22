#!/usr/bin/env bash
# =====================================================================
# VERDURE Native Android APK Build Script (Capacitor)
# Packages the VERDURE PWA into a native Android Studio project and APK
# =====================================================================

set -e

echo "[VERDURE] Starting Native Android APK Packaging..."

if ! command -v npm &> /dev/null; then
    echo "[ERROR] Node.js and npm are required. Please install Node.js."
    exit 1
fi

echo "[1/4] Installing Capacitor dependencies..."
npm install --save-dev @capacitor/core @capacitor/cli @capacitor/android @capacitor/camera @capacitor/haptics

echo "[2/4] Initializing Capacitor configuration..."
if [ ! -f "capacitor.config.json" ]; then
    npx cap init "VERDURE" "org.verdure.leafdoctor" --web-dir .
fi

echo "[3/4] Adding Android native platform..."
if [ ! -d "android" ]; then
    npx cap add android
fi

echo "[4/4] Copying web assets and syncing native project..."
npx cap sync android

echo ""
echo "====================================================================="
echo " VERDURE Android Project Synced Successfully!"
echo "====================================================================="
echo "To build the final APK:"
echo "  1. Run: npx cap open android"
echo "  2. In Android Studio: Build -> Build Bundle(s) / APK(s) -> Build APK(s)"
echo "  3. Output APK will be at: android/app/build/outputs/apk/debug/app-debug.apk"
echo "====================================================================="
