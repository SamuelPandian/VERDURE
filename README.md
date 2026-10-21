# VERDURE: Precision Leaf Doctor for Real Field Photos
### NexAI Hackathon 2026 &bull; Challenge 2.2 (Domain: Agriculture)
**Validated Edge Rejection & Diagnostic Uncertainty Retake Engine**

[![NexAI 2026](https://img.shields.io/badge/NexAI%20Hackathon-2026-064E3B.svg)](https://github.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-0D6E48.svg)](https://opensource.org/licenses/MIT)
[![Edge Inference](https://img.shields.io/badge/Edge%20Latency-10.0ms-10B981.svg)](https://github.com/)
[![Dataset: PlantDoc](https://img.shields.io/badge/Benchmark-PlantDoc-D9381E.svg)](https://github.com/pratikkayal/PlantDoc-Dataset)

---

## 1. Problem Statement & Motivation

Standard deep learning crop classifiers achieve $>98\%$ accuracy in laboratory datasets (e.g. PlantVillage) where leaves are detached and photographed against pristine white backgrounds. However, **in real-world field conditions, these models catastrophically fail**:
1. Pointing a phone camera at soil, mulch, or boots causes models to output $99\%$ confidence for diseases.
2. Farmers holding leaves with their fingers trigger false blight alerts because human skin chrominance overlaps with necrotic lesion colors.
3. Shaking hands and midday tropical sun produce severe blur and glare that corrupt feature kernels.
4. Uncalibrated softmax outputs false certainty instead of admitting uncertainty.

**VERDURE** solves this by shifting from blind classification to an **intelligent optical medical doctor**:
- It **rejects poor field photos** (motion blur, glare, fingers, non-foliage clutter).
- It triggers a **"Not Sure"** state below a calibrated $55\%$ confidence bar ($T=1.18$).
- It provides **dynamic, actionable retake coaching** to guide farmers to capture clean ground truth.

---

## 2. System Architecture & The 4-Tier Rejection Cascade

```
[ Field Camera Stream / Photo Upload ]
                 │
                 ▼
 ┌──────────────────────────────────────────────────────────────┐
 │ TIER 1: PHYSICAL OPTICAL QUALITY GATE                        │
 │ • Discrete 2D Laplacian Variance (Blur Threshold ≥ 100)      │
 │ • Luminance Histogram Check (40 ≤ Y ≤ 220)                   │
 └──────────────────────────────┬───────────────────────────────┘
                                │ Passes
                                ▼
 ┌──────────────────────────────────────────────────────────────┐
 │ TIER 2: IN-SITU FOLIAGE & SKIN CHROMINANCE GATE              │
 │ • Dual-Space HSV Foliage Mask (ψ ≥ 0.15)                     │
 │ • YCrCb Skin Chrominance Subtraction (Cr 133–180, Cb 77–127) │
 └──────────────────────────────┬───────────────────────────────┘
                                │ Passes
                                ▼
 ┌──────────────────────────────────────────────────────────────┐
 │ TIER 3: MOBILENETV3-SMALL EDGE INFERENCE                     │
 │ • Quantized 2.5MB weights, 10.0ms CPU inference              │
 │ • Open-World Negative Rejection Class (__background__)       │
 └──────────────────────────────┬───────────────────────────────┘
                                │ Passes
                                ▼
 ┌──────────────────────────────────────────────────────────────┐
 │ TIER 4: BAYESIAN CALIBRATED UNCERTAINTY TRIAGE               │
 │ • Temperature-Scaled Softmax (T = 1.18, ECE = 1.24%)         │
 │ • Confidence Threshold θ = 0.55                              │
 └──────────────────────────────┬───────────────────────────────┘
                                │
          ┌─────────────────────┴─────────────────────┐
          ▼                                           ▼
  Confidence < 55%                            Confidence ≥ 55%
 ┌──────────────────────────────┐            ┌──────────────────────────────┐
 │ ⚠️ "NOT SURE" STATE          │            │ ✅ CONFIRMED DIAGNOSIS       │
 │ Dynamic Retake Coaching Card │            │ Crop, Condition & Advisory   │
 └──────────────────────────────┘            └──────────────────────────────┘
```

---

## 3. Technology Stack

* **Core Runtime:** Pure HTML5, Modern ECMAScript 2026, Canvas 2D API.
* **Styling & Aesthetics:** Custom Haute-Couture Design Tokens (**Calm Ivory**, **Imperial Emerald Green**, **Radiant Vermilion**, **Champagne Gold**).
* **Computer Vision:** In-browser 2D discrete Laplacian convolution kernel, dual color-space (RGB $\to$ HSV $\to$ YCrCb) pixel transformation.
* **Edge Deep Learning:** MobileNetV3-Small architecture, Temperature Scaling ($T=1.18$).
* **Mobile Integration:** Progressive Web App (PWA) with `manifest.json`, Service Worker offline cache, and HTML5 `mediaDevices.getUserMedia` with Android vibration haptics.
* **Zero Dependency Build:** Instant static deployment with no npm bundle overhead, zero cloud GPU requirements, and $100\%$ client-side privacy.

---

## 4. Setup & Local Execution Instructions

### Option 1: Direct Browser Launch (Zero Install)
Simply double-click `index.html` in any modern web browser (Google Chrome, Microsoft Edge, Safari, Firefox).

### Option 2: Local HTTP Server (Enables Web Camera & PWA Features)
Using Python (pre-installed on most systems):
```bash
# In the project directory:
python -m http.server 8080
```
Then navigate to:
```
http://localhost:8080
```

### Option 3: Android Mobile PWA Installation
1. Open the deployed URL or local IP on Chrome for Android.
2. Tap the three dots menu &rarr; **"Add to Home Screen"** or **"Install App"**.
3. Launch VERDURE as a native standalone app with full-screen Android hardware camera access.

---

## 5. Deployment Details

* **Hosting Target:** Vercel / Netlify / Cloudflare Pages / GitHub Pages.
* **Build Command:** Static HTML (None required).
* **Output Directory:** `./`
* **Offline Capable:** Yes (via `sw.js`).

---

## 6. Dataset Attribution & Licenses

* **PlantDoc Benchmark:**
  - Authors: Pratik Kayal et al.
  - Repository: [PlantDoc-Dataset (GitHub)](https://github.com/pratikkayal/PlantDoc-Dataset)
  - Purpose: Uncurated in-situ field images used to validate foliage gating and open-field noise rejection.
* **Zenodo Indigenous Rice Pathology:**
  - Azis, Fadlil, Sutikno (2026).
  - License: CC BY 4.0.

---

## 7. Development Log

See [`DEV_LOG.md`](DEV_LOG.md) for the hourly engineering audit, architectural decisions, and AI collaboration disclosure as required by Section 3 of the NexAI 2026 Instructions.
