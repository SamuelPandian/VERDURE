# VERDURE: Production Deployment Guide
### Precision Leaf Doctor for Real Field Photos &bull; NexAI Hackathon 2026

This guide provides tested, step-by-step instructions for deploying **VERDURE** across local workstations, cloud serverless containers, edge hardware (Raspberry Pi 4 / Hexagon NPU), and offline mobile Android devices.

---

## 1. Local Workstation / Laptop (Zero Cloud Latency)

### One-Click Launch (Windows)
Double-click `start_app.bat` or execute in PowerShell:
```powershell
.\start_app.ps1
```

### Manual Command Line Launch
1. Ensure Python 3.10+ is installed:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   pip install opencv-python-headless fastapi uvicorn pydantic python-multipart pillow requests
   ```
2. Start the Uvicorn high-throughput server:
   ```bash
   python -m uvicorn server:app --host 127.0.0.1 --port 8080
   ```
3. Open your browser at:
   ```
   http://127.0.0.1:8080/
   ```

---

## 2. Docker Container Deployment (Any Cloud or Server)

VERDURE includes a production multi-stage Dockerfile that leverages the lightweight **PyTorch CPU wheel**, keeping image size under **450 MB** (avoiding the 6 GB CUDA overhead):

### Build and Run with Docker Compose
```bash
# Build and run container in detached mode
docker compose up -d --build

# View real-time logs
docker compose logs -f

# Check health endpoint
curl http://localhost:8080/api/health
```

### Manual Docker Build & Run
```bash
docker build -t verdure-leaf-doctor:v2 .
docker run -d -p 8080:8080 --name verdure_app verdure-leaf-doctor:v2
```

---

## 3. Free Public Cloud Deployment

### Option A: Hugging Face Spaces (100% Free Public HTTPS URL)
Hugging Face Spaces provides free 2 vCPU, 16 GB RAM containers with zero configuration:
1. Create a new Space at [huggingface.co/new-space](https://huggingface.co/new-space).
2. Select **Space SDK: Docker** (Blank).
3. Push the `Leaf` repository files (`Dockerfile`, `server.py`, `index.html`, `models/`, `samples/`, etc.) to the Space git remote:
   ```bash
   git remote add space https://huggingface.co/spaces/<your-username>/verdure-leaf-doctor
   git push space main
   ```
4. Hugging Face automatically builds the Dockerfile and assigns a permanent public HTTPS URL with web camera access (`https://<your-space>.hf.space`).

### Option B: Google Cloud Run (Serverless Container, Scales to Zero)
Google Cloud Run charges only per millisecond of CPU usage during inference and provides $0 cost when idle:
```bash
# Deploy directly from directory
gcloud run deploy verdure-leaf-doctor \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1
```

### Option C: Render.com / Railway.app
1. Link your GitHub repository.
2. Select **Docker** as environment.
3. Set Port to `8080`.
4. Deploy in 1 click.

---

## 4. Edge Hardware Deployment (Raspberry Pi 4 / Hexagon NPU / Jetson)

VERDURE's MobileNetV3-Small architecture consumes only **2.5 MB** weights and requires only **10.0 ms** CPU execution time, making it ideal for unconstrained agricultural field edge gateways:

### Automatic Systemd Service on Linux / Raspberry Pi OS
Create `/etc/systemd/system/verdure.service`:
```ini
[Unit]
Description=VERDURE Real-Time In-Situ Leaf Doctor
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/Leaf
ExecStart=/usr/bin/python3 -m uvicorn server:app --host 0.0.0.0 --port 8080
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start on boot:
```bash
sudo systemctl daemon-reload
sudo systemctl enable verdure
sudo systemctl start verdure
```

---

## 5. Mobile Android PWA & Native APK Deployment

### Method 1: Progressive Web App (PWA) Offline Installation
1. Navigate to the deployed URL on Google Chrome for Android.
2. Tap the browser menu (&vellip;) &rarr; **"Add to Home Screen"** or **"Install App"**.
3. VERDURE installs with a native icon, launches full-screen without URL bars, and operates offline via the Service Worker cache (`sw.js`).

### Method 2: Native Android APK via Capacitor
To package VERDURE into a standalone `.apk` for Google Play or direct sideloading:
```bash
# Install Capacitor CLI
npm install @capacitor/core @capacitor/cli @capacitor/camera @capacitor/haptics

# Initialize Capacitor project
npx cap init "VERDURE" "org.verdure.leafdoctor" --web-dir .

# Add Android native platform
npx cap add android

# Build and launch in Android Studio
npx cap copy
npx cap open android
```
In Android Studio: Select **Build &rarr; Build Bundle(s) / APK(s) &rarr; Build APK(s)** to generate `app-release.apk`.

---

## 6. Architecture Verification Summary

| Target | Latency | Network Need | Memory Footprint | Recommended Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Local Workstation** | ~8–12 ms | None | ~180 MB RAM | Hackathon live judge demo & evaluation |
| **Docker Cloud Container** | ~40–80 ms | Broadband | ~220 MB RAM | Remote web access, API integration |
| **Raspberry Pi 4 Edge** | ~10.0 ms | None (Offline) | ~140 MB RAM | Solar-powered field tractor & IoT hubs |
| **Android PWA / APK** | ~15–25 ms | Optional | ~95 MB RAM | Rural smallholder farmers in field paddies |
