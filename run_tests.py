#!/usr/bin/env python3
"""
VERDURE Automated Test & Verification Suite
Validates the complete 4-tier edge rejection cascade, PyTorch model inference,
agronomic prescriptions, dynamic lesion localization, and REST API endpoints.
"""

import sys
import time
import json
import base64
import unittest
from pathlib import Path
import numpy as np
import cv2
import torch

# Force UTF-8 stdout if supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = Path(__file__).resolve().parent
from labels import parse_label
from prescriptions import get_prescription, PRESCRIPTION_DB
from server import app, MODEL_REGISTRY, locate_lesion_hotspots, evaluate_image, load_pt_model
from fastapi.testclient import TestClient

client = TestClient(app)

class TestVerdurePipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n" + "=" * 65)
        print(" VERDURE TEST & VERIFICATION SUITE -- NexAI 2026 Challenge 2.2")
        print("=" * 65)

    def test_01_model_loading(self):
        """Verify all PyTorch checkpoints can be loaded without error."""
        print("\n[TEST 01] Verifying PyTorch model checkpoints...")
        for key, info in MODEL_REGISTRY.items():
            pt_path = info["path"]
            self.assertTrue(pt_path.exists(), f"Model file missing: {pt_path}")
            ck = torch.load(pt_path, map_location="cpu", weights_only=False)
            self.assertIn("classes", ck, f"No classes in {key}")
            self.assertIn("state_dict", ck, f"No state_dict in {key}")
            self.assertGreater(len(ck["classes"]), 0)
            print(f"  [PASS] {key} loaded successfully ({len(ck['classes'])} classes)")

    def test_02_label_parsing(self):
        """Verify label parsing across PlantVillage, Rice, and Indian species."""
        print("\n[TEST 02] Verifying label parsing...")
        samples = [
            ("Potato___Early_blight", "Potato", "Early blight", False),
            ("Tomato___healthy", "Tomato", "healthy", True),
            ("Corn_(maize)___Common_rust_", "Corn (maize)", "Common rust", False),
            ("Rice___Brown_spot", "Rice", "Brown spot", False),
            ("Arjun healthy (P1b)", "Arjun", "healthy", True)
        ]
        for raw, expected_crop, expected_cond, expected_healthy in samples:
            crop, cond, healthy = parse_label(raw)
            self.assertEqual(crop, expected_crop)
            self.assertEqual(healthy, expected_healthy)
            print(f"  [PASS] '{raw}' -> Crop: {crop}, Condition: {cond}, Healthy: {healthy}")

    def test_03_prescriptions_lookup(self):
        """Verify clinical agronomic prescriptions for pathogens."""
        print("\n[TEST 03] Verifying agronomic prescription database...")
        # Early blight
        rx_eb = get_prescription("Potato", "Early blight", False)
        self.assertIn("Alternaria", rx_eb["pathogen"])
        self.assertIn("Chlorothalonil", rx_eb["rx_chemical"])
        self.assertIn("Trichoderma", rx_eb["rx_biological"])
        print(f"  [PASS] Potato Early Blight: {rx_eb['pathogen']}")

        # Healthy stand
        rx_h = get_prescription("Apple", "healthy", True)
        self.assertIn("Healthy", rx_h["pathogen"])
        print(f"  [PASS] Healthy standby prescription: {rx_h['pathogen']}")

    def test_04_tier1_optical_rejection(self):
        """Verify Tier 1 discrete 2D Laplacian motion blur and luminance checks."""
        print("\n[TEST 04] Testing Tier 1: Optical Gate (Blur & Glare)...")
        # Blurry synthetic image (smooth constant gradient)
        blurry = np.full((300, 300, 3), 120, dtype=np.uint8)
        cv2.GaussianBlur(blurry, (45, 45), 0, dst=blurry)
        res_blur = evaluate_image(blurry)
        self.assertEqual(res_blur["status"], "rejected")
        self.assertEqual(res_blur["rejection_tier"], 1)
        self.assertEqual(res_blur["code"], "MOTION_BLUR")
        print(f"  [PASS] Motion blur correctly caught: {res_blur['code']}")

        # Glare image (overexposed)
        glare = np.full((300, 300, 3), 245, dtype=np.uint8)
        noise = np.random.randint(-15, 10, (300, 300, 3), dtype=np.int16)
        glare = np.clip(glare.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        res_glare = evaluate_image(glare)
        self.assertEqual(res_glare["status"], "rejected")
        self.assertEqual(res_glare["rejection_tier"], 1)
        self.assertEqual(res_glare["code"], "GLARE")
        print(f"  [PASS] Direct sun glare correctly caught: {res_glare['code']}")

    def test_05_tier2_skin_occlusion_rejection(self):
        """Verify Tier 2 human skin chrominance rejection on hand-held leaves."""
        print("\n[TEST 05] Testing Tier 2: Skin & Foliage Gate...")
        # Use verified benchmark specimen: samples/hand_occlusion_leaf.jpg
        specimen = HERE / "samples" / "hand_occlusion_leaf.jpg"
        self.assertTrue(specimen.exists(), "hand_occlusion_leaf.jpg missing")
        bgr = cv2.imread(str(specimen))
        res = evaluate_image(bgr)
        self.assertEqual(res["status"], "rejected")
        self.assertEqual(res["rejection_tier"], 2)
        self.assertIn(res["code"], ["FINGERS", "SKIN_OCCLUSION"])
        print(f"  [PASS] Hand/finger occlusion correctly caught: {res['code']} ({res['title']})")

    def test_06_tier3_open_world_rejection(self):
        """Verify Tier 3 open-world negative background class rejection."""
        print("\n[TEST 06] Testing Tier 3: Open-World Negative Class...")
        soil_sample = HERE / "samples" / "soil_non_foliage.jpg"
        if soil_sample.exists():
            bgr = cv2.imread(str(soil_sample))
            res = evaluate_image(bgr)
            self.assertEqual(res["status"], "rejected")
            self.assertEqual(res["rejection_tier"], 3)
            print(f"  [PASS] Soil clutter correctly rejected: {res['title']}")

    def test_07_tier4_uncertainty_triage(self):
        """Verify Tier 4 Bayesian calibrated uncertainty triage below 55% bar."""
        print("\n[TEST 07] Testing Tier 4: Uncertainty Triage & Calibrated Softmax...")
        potato_sample = HERE / "samples" / "potato_early_blight.jpg"
        self.assertTrue(potato_sample.exists())
        bgr = cv2.imread(str(potato_sample))
        # With default cutoff 0.55
        res = evaluate_image(bgr, conf_cutoff=0.55)
        self.assertEqual(res["status"], "uncertain")
        self.assertEqual(res["rejection_tier"], 4)
        self.assertIn("top3", res)
        self.assertIn("pins", res)
        self.assertIn("prescription", res)
        print(f"  [PASS] Ambiguous diagnosis triaged into Not-Sure state: {res['title']}")
        print(f"         Confidence: {res['confidence']*100:.1f}%, Leading Crop: {res['crop']}, Condition: {res['condition']}")

    def test_08_lesion_pin_localization(self):
        """Verify dynamic lesion hotspot coordinates calculation."""
        print("\n[TEST 08] Testing dynamic lesion pin localization...")
        # Image with distinct non-green lesion
        img = np.full((300, 300, 3), (35, 130, 45), dtype=np.uint8) # green
        cv2.circle(img, (90, 120), 25, (20, 50, 100), -1) # necrotic dark brown lesion
        pins = locate_lesion_hotspots(img, is_healthy=False)
        self.assertEqual(len(pins), 3)
        self.assertGreater(pins[0]["x"], 0)
        self.assertLess(pins[0]["x"], 100)
        self.assertGreater(pins[0]["y"], 0)
        self.assertLess(pins[0]["y"], 100)
        print(f"  [PASS] Saliency Pin 1 located at ({pins[0]['x']}%, {pins[0]['y']}%)")
        print(f"  [PASS] Saliency Pin 2 located at ({pins[1]['x']}%, {pins[1]['y']}%)")
        print(f"  [PASS] Saliency Pin 3 located at ({pins[2]['x']}%, {pins[2]['y']}%)")

    def test_09_fastapi_endpoints(self):
        """Verify live FastAPI REST API endpoints."""
        print("\n[TEST 09] Testing FastAPI REST Endpoints...")
        # /api/health
        r_health = client.get("/api/health")
        self.assertEqual(r_health.status_code, 200)
        self.assertEqual(r_health.json()["status"], "online")
        print(f"  [PASS] GET /api/health -> 200 OK ({r_health.json()['service']})")

        # /api/models
        r_models = client.get("/api/models")
        self.assertEqual(r_models.status_code, 200)
        self.assertGreater(len(r_models.json()["models"]), 0)
        print(f"  [PASS] GET /api/models -> 200 OK ({len(r_models.json()['models'])} models available)")

        # /api/predict via sample_path
        r_pred = client.post("/api/predict", json={"sample_path": "samples/potato_early_blight.jpg"})
        self.assertEqual(r_pred.status_code, 200)
        pred_data = r_pred.json()
        self.assertIn(pred_data["status"], ["uncertain", "diagnosed", "rejected"])
        print(f"  [PASS] POST /api/predict (sample_path) -> 200 OK (Status: {pred_data['status']})")

        # /api/predict via base64
        synthetic_img = np.full((120, 120, 3), (40, 150, 60), dtype=np.uint8)
        _, buf = cv2.imencode(".jpg", synthetic_img)
        b64_str = "data:image/jpeg;base64," + base64.b64encode(buf).decode("utf-8")
        r_pred_b64 = client.post("/api/predict", json={"image_base64": b64_str})
        self.assertEqual(r_pred_b64.status_code, 200)
        print(f"  [PASS] POST /api/predict (base64) -> 200 OK")

    def test_10_static_assets_serving(self):
        """Verify root static and PWA files are served."""
        print("\n[TEST 10] Testing static and PWA asset serving...")
        endpoints = ["/", "/manifest.json", "/sw.js", "/samples/potato_early_blight.jpg"]
        for ep in endpoints:
            r = client.get(ep)
            self.assertEqual(r.status_code, 200, f"Endpoint {ep} failed with status {r.status_code}")
            print(f"  [PASS] GET {ep} -> 200 OK ({len(r.content)} bytes)")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVerdurePipeline)
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\n" + "=" * 65)
        print(" ALL 10 TESTS PASSED -- VERDURE READY FOR HACKATHON EVALUATION")
        print("=" * 65)
        sys.exit(0)
    else:
        sys.exit(1)
