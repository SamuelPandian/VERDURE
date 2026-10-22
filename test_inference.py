import sys
import time
from pathlib import Path
import torch
import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
from labels import parse_label

def test_pipeline():
    pt_path = HERE / 'models' / 'best.pt'
    print(f"Loading {pt_path}...")
    ck = torch.load(pt_path, map_location='cpu', weights_only=False)
    classes = ck['classes']
    from torchvision.models import mobilenet_v3_small
    model = mobilenet_v3_small(weights=None)
    model.classifier[3] = torch.nn.Linear(model.classifier[3].in_features, len(classes))
    model.load_state_dict(ck['state_dict'])
    model.eval()

    # Create synthetic green leaf image with a small brown spot
    img = np.full((300, 300, 3), (35, 120, 45), dtype=np.uint8) # BGR green
    cv2.circle(img, (150, 150), 30, (20, 60, 110), -1) # Brown spot
    
    # Tier 1: Blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    mean_luma = float(gray.mean())
    print(f"Tier 1: Blur Var={blur_var:.1f}, Mean Luma={mean_luma:.1f}")

    # Tier 2: Foliage & Skin
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    green = (h >= 25) & (h <= 95) & (s >= 45) & (v >= 35)
    yellow_brown = (h >= 8) & (h < 25) & (s >= 70) & (v >= 45)
    foliage = green | yellow_brown
    ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    cr, cb = ycc[..., 1], ycc[..., 2]
    skin = (cr >= 133) & (cr <= 180) & (cb >= 77) & (cb <= 127)
    foliage_frac = float(((foliage) & ~skin).mean())
    skin_frac = float(skin.mean())
    print(f"Tier 2: Foliage Frac={foliage_frac:.2f}, Skin Frac={skin_frac:.2f}")

    # Tier 3: Inference
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (224, 224)).astype(np.float32) / 255.0
    mean = np.array(ck.get('mean', [0.485, 0.456, 0.406]), dtype=np.float32)
    std = np.array(ck.get('std', [0.229, 0.224, 0.225]), dtype=np.float32)
    normalized = (resized - mean) / std
    tensor = torch.from_numpy(normalized).permute(2, 0, 1).unsqueeze(0)

    t0 = time.perf_counter()
    with torch.no_grad():
        logits = model(tensor)
        calibrated_logits = logits / 1.18
        probs = torch.softmax(calibrated_logits, dim=1)[0].numpy()
    latency = (time.perf_counter() - t0) * 1000

    top_idx = int(np.argmax(probs))
    top_class = classes[top_idx]
    top_conf = float(probs[top_idx])
    crop, condition, is_healthy = parse_label(top_class)
    print(f"Tier 3: Latency={latency:.2f}ms, Top={top_class} ({top_conf*100:.1f}%)")
    print(f"Parsed: Crop={crop}, Condition={condition}, Healthy={is_healthy}")
    print("SUCCESS!")

if __name__ == '__main__':
    test_pipeline()
