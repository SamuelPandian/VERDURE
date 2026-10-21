"""
SAKTHI Real-Time Foliage Gated Inference Engine
Supports both Full-Frame Multi-Leaf Dense Detection (100 percent sensor area)
and Single-ROI Center Crop mode.
"""
import argparse
import sys
import time
from collections import deque
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.nn.functional as F
from torchvision import transforms
from torchvision.models import mobilenet_v3_small

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from labels import BACKGROUND_CLASS, parse_label

GREEN = (40, 200, 80)
RED   = (50, 60, 230)
AMBER = (30, 160, 230)
GREY  = (160, 160, 160)
WHITE = (240, 240, 240)
CYAN  = (220, 200, 60)

MODEL_SHORTCUTS = {
    'plantvillage': HERE / 'models' / 'best.pt',
    'best':         HERE / 'models' / 'best.pt',
    'indian':       HERE / 'models' / 'indian_species.pt',
    'rice':         HERE / 'models' / 'rice_diseases.pt',
    'zenodo':       HERE / 'models' / 'zenodo_rice.pt',
}

MODEL_DISPLAY_NAMES = {
    'best.pt':             'PlantVillage (38 classes)',
    'indian_species.pt':   'Indian Medicinal (11 species)',
    'rice_diseases.pt':    'Rice Diseases (3 class)',
    'zenodo_rice.pt':      'Zenodo Rice Pest (10 class)',
}

def resolve_model_path(spec: str) -> Path:
    low = spec.lower()
    if low in MODEL_SHORTCUTS:
        return MODEL_SHORTCUTS[low]
    p = Path(spec)
    if not p.is_absolute():
        candidate = HERE / 'models' / spec
        if candidate.exists():
            return candidate
    return p

def discover_models() -> list[Path]:
    preferred = ['best.pt', 'indian_species.pt', 'rice_diseases.pt', 'zenodo_rice.pt']
    pts = list((HERE / 'models').glob('*.pt')) if (HERE / 'models').exists() else []
    ordered = []
    for name in preferred:
        p = HERE / 'models' / name
        if p in pts:
            ordered.append(p)
    for p in sorted(pts):
        if p not in ordered:
            ordered.append(p)
    return ordered

def load_model(path, device):
    ck = torch.load(path, map_location=device, weights_only=False)
    classes = ck['classes']
    model = mobilenet_v3_small(weights=None)
    model.classifier[3] = torch.nn.Linear(model.classifier[3].in_features, len(classes))
    model.load_state_dict(ck['state_dict'])
    model.eval().to(device)
    size = ck.get('input_size', 224)
    tf = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(ck.get('mean', [0.485, 0.456, 0.406]),
                             ck.get('std',  [0.229, 0.224, 0.225])),
    ])
    return model, classes, size, tf, ck.get('val_acc')

def leaf_fraction(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    green = (h >= 25) & (h <= 95) & (s >= 45) & (v >= 35)
    yellow_brown = (h >= 8) & (h < 25) & (s >= 70) & (v >= 45)
    ycc = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    cr, cb = ycc[..., 1], ycc[..., 2]
    skin = (cr >= 133) & (cr <= 180) & (cb >= 77) & (cb <= 127)
    return float(((green | yellow_brown) & ~skin).mean())

def open_source(src):
    cam = int(src) if str(src).isdigit() else str(src)
    cap = cv2.VideoCapture(cam)
    if isinstance(cam, int):
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return cap

def draw_panel(frame, x, y, w, h, alpha=0.55):
    sub = frame[y:y + h, x:x + w]
    if sub.size:
        frame[y:y + h, x:x + w] = cv2.addWeighted(
            sub, 1 - alpha, np.zeros_like(sub), alpha, 0)

def extract_leaf_candidates(frame, min_area_ratio=0.010, max_leaves=6):
    H, W = frame.shape[:2]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    green = (h >= 25) & (h <= 95) & (s >= 45) & (v >= 35)
    yellow_brown = (h >= 8) & (h < 25) & (s >= 70) & (v >= 45)
    ycc = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    cr, cb = ycc[..., 1], ycc[..., 2]
    skin = (cr >= 133) & (cr <= 180) & (cb >= 77) & (cb <= 127)

    mask = (((green | yellow_brown) & ~skin).astype(np.uint8)) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = H * W * min_area_ratio

    candidates = []
    for cnt in sorted(contours, key=cv2.contourArea, reverse=True):
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        mx = int(w * 0.08)
        my = int(h * 0.08)
        x0 = max(0, x - mx)
        y0 = max(0, y - my)
        x1 = min(W, x + w + mx)
        y1 = min(H, y + h + my)
        crop = frame[y0:y1, x0:x1]
        if crop.size > 0:
            candidates.append({
                'box': (x0, y0, x1 - x0, y1 - y0),
                'contour': cnt,
                'area': area,
                'crop': crop
            })
        if len(candidates) >= max_leaves:
            break
    return candidates

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', default='0')
    ap.add_argument('--model', default='plantvillage',
                    help='model shortcut (plantvillage/indian/rice/zenodo) or path to .pt')
    ap.add_argument('--conf', type=float, default=0.55,
                    help='below this the call is shown as uncertain')
    ap.add_argument('--roi', type=float, default=0.6,
                    help='box size as fraction of frame (in single-ROI mode)')
    ap.add_argument('--multi', action='store_true', default=True,
                    help='Full-frame multi-leaf dense detection mode (evaluates every pixel, finds all leaves at once)')
    ap.add_argument('--no-multi', action='store_false', dest='multi',
                    help='Disable multi-leaf mode and use single center ROI')
    ap.add_argument('--every', type=int, default=2,
                    help='run the CNN every N frames')
    ap.add_argument('--smooth', type=int, default=8,
                    help='frames of temporal averaging')
    ap.add_argument('--gate', type=float, default=0.12,
                    help='min plant-pixel fraction in the box; 0 disables')
    ap.add_argument('--threads', type=int, default=2)
    ap.add_argument('--snapshot-dir', default=str(HERE / 'snapshots'))
    args = ap.parse_args()

    torch.set_num_threads(max(1, args.threads))
    device = torch.device('cpu')

    model_path = resolve_model_path(args.model)
    if not model_path.exists():
        sys.exit(f'No model at {model_path}\n'
                 f'Available shortcuts: {", ".join(MODEL_SHORTCUTS)}\n'
                 'Train one first:  python train.py')

    all_models = discover_models()
    model_idx  = all_models.index(model_path) if model_path in all_models else 0

    def load_current(path):
        m, cls, sz, tf, acc = load_model(path, device)
        prs  = [parse_label(c) for c in cls]
        name = MODEL_DISPLAY_NAMES.get(path.name, path.stem)
        print(f'  model: {name}  |  {len(cls)} classes'
              + (f'  |  val acc {acc:.3f}' if acc else ''))
        return m, cls, sz, tf, prs, name

    model, classes, size, tf, parsed, model_name = load_current(model_path)

    cap = open_source(args.source)
    if not cap.isOpened():
        sys.exit(f'Could not open source "{args.source}".\n'
                 'Webcam: try --source 1. Phone: check the URL and that both\n'
                 'devices are on the same Wi-Fi.')

    hist = deque(maxlen=max(1, args.smooth))
    fps_hist = deque(maxlen=30)
    roi_frac = args.roi
    use_gate = args.gate > 0
    multi_mode = args.multi
    flip     = True
    show_top3 = True
    frame_i   = 0
    probs     = None
    infer_ms  = 0.0
    model_switch_msg = ''
    model_switch_t   = 0.0

    win = 'SAKTHI - Leaf Doctor (q=quit  m=model  u=multi/single)'
    cv2.namedWindow(win, cv2.WINDOW_NORMAL)

    while True:
        t0 = time.time()
        ok, frame = cap.read()
        if not ok:
            print('lost the camera feed')
            break
        if flip:
            frame = cv2.flip(frame, 1)

        H, W = frame.shape[:2]
        frame_i += 1

        if multi_mode:
            candidates = extract_leaf_candidates(frame, min_area_ratio=0.010, max_leaves=6)
            detected_leaves = []

            if candidates and frame_i % max(1, args.every) == 0:
                ti = time.time()
                with torch.inference_mode():
                    for cand in candidates:
                        crop_rgb = cv2.cvtColor(cv2.resize(cand['crop'], (size, size)), cv2.COLOR_BGR2RGB)
                        tensor = tf(crop_rgb).unsqueeze(0).to(device)
                        p_cand = F.softmax(model(tensor), 1)[0].cpu().numpy()
                        top_idx = int(p_cand.argmax())
                        cand_conf = float(p_cand[top_idx])
                        sp, cond, hl = parsed[top_idx]
                        is_b = classes[top_idx] == BACKGROUND_CLASS
                        detected_leaves.append({
                            'box': cand['box'],
                            'conf': cand_conf,
                            'species': sp,
                            'condition': cond,
                            'healthy': hl,
                            'is_bg': is_b,
                        })
                infer_ms = (time.time() - ti) * 1000

            panel_h = 100
            draw_panel(frame, 0, 0, W, panel_h)

            badge = f'[{model_name} · MULTI-LEAF]'
            bw, _ = cv2.getTextSize(badge, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)[0], 0
            cv2.putText(frame, badge, (W - bw[0] - 10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, CYAN, 1)

            if not candidates:
                cv2.putText(frame, 'Full-Frame Scanner Active: Searching Foliage...', (16, 42),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.85, WHITE, 2)
                cv2.putText(frame, 'Every pixel evaluated (HSV/YCrCb) · 0 wasted border pixels', (16, 74),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.52, GREY, 1)
            else:
                n_healthy = sum(1 for d in detected_leaves if d['healthy'] and not d['is_bg'])
                n_diseased = sum(1 for d in detected_leaves if not d['healthy'] and not d['is_bg'])
                cv2.putText(frame, f'Full-Frame Multi-Leaf: {len(candidates)} Detected', (16, 42),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.85, WHITE, 2)
                cv2.putText(frame, f'Healthy: {n_healthy}  |  Diseased: {n_diseased}  |  100% Sensor Coverage', (16, 74),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.52, GREEN if n_diseased == 0 else RED, 1)

            for i, d in enumerate(detected_leaves):
                bx, by, bw_box, bh_box = d['box']
                if d['is_bg'] or d['conf'] < args.conf:
                    col = AMBER
                else:
                    col = GREEN if d['healthy'] else RED

                cv2.rectangle(frame, (bx, by), (bx + bw_box, by + bh_box), col, 2)
                corner_len = min(20, min(bw_box, bh_box) // 4)
                for cx, cy, dx, dy in [(bx, by, 1, 1), (bx + bw_box, by, -1, 1),
                                       (bx, by + bh_box, 1, -1), (bx + bw_box, by + bh_box, -1, -1)]:
                    cv2.line(frame, (cx, cy), (cx + corner_len * dx, cy), col, 4)
                    cv2.line(frame, (cx, cy), (cx, cy + corner_len * dy), col, 4)

                tag = f"#{i+1}: {d['species'][:14]} - {d['condition'][:18]} ({d['conf']*100:.0f}%)"
                (tw, th), _ = cv2.getTextSize(tag, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
                tag_y = max(by - 6, 20)
                cv2.rectangle(frame, (bx, tag_y - th - 4), (bx + tw + 8, tag_y + 2), col, -1)
                cv2.putText(frame, tag, (bx + 4, tag_y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.45, WHITE, 1)

        else:
            side = int(min(H, W) * roi_frac)
            x0, y0 = (W - side) // 2, (H - side) // 2
            roi = frame[y0:y0 + side, x0:x0 + side]

            frac = leaf_fraction(roi) if use_gate else 1.0
            leaf_present = (not use_gate) or (frac >= args.gate)

            if leaf_present and frame_i % max(1, args.every) == 0:
                ti = time.time()
                with torch.inference_mode():
                    rgb = cv2.cvtColor(cv2.resize(roi, (size, size)), cv2.COLOR_BGR2RGB)
                    p   = F.softmax(model(tf(rgb).unsqueeze(0).to(device)), 1)[0]
                    hist.append(p.cpu().numpy())
                infer_ms = (time.time() - ti) * 1000
            elif not leaf_present:
                hist.clear()

            probs = np.mean(hist, axis=0) if hist else None

            box_col = GREY
            if probs is not None:
                top    = int(probs.argmax())
                conf   = float(probs[top])
                species, condition, healthy = parsed[top]
                is_bg  = classes[top] == BACKGROUND_CLASS
                if is_bg or conf < args.conf:
                    box_col = AMBER
                else:
                    box_col = GREEN if healthy else RED
            cv2.rectangle(frame, (x0, y0), (x0 + side, y0 + side), box_col, 2)
            for cx, cy, dx, dy in [(x0, y0, 1, 1), (x0 + side, y0, -1, 1),
                                   (x0, y0 + side, 1, -1), (x0 + side, y0 + side, -1, -1)]:
                cv2.line(frame, (cx, cy), (cx + 26 * dx, cy), box_col, 5)
                cv2.line(frame, (cx, cy), (cx, cy + 26 * dy), box_col, 5)

            panel_h = 112
            draw_panel(frame, 0, 0, W, panel_h)

            badge = f'[{model_name} · SINGLE-ROI]'
            bw, _ = cv2.getTextSize(badge, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)[0], 0
            cv2.putText(frame, badge, (W - bw[0] - 10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, CYAN, 1)

            if probs is None:
                cv2.putText(frame, 'Show a leaf inside the box', (16, 46),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.95, WHITE, 2)
                cv2.putText(frame, f'plant pixels: {frac*100:.0f}%  '
                            f'(need {args.gate*100:.0f}%)', (16, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, GREY, 1)
            else:
                if classes[top] == BACKGROUND_CLASS:
                    cv2.putText(frame, 'No leaf in view', (16, 48),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, AMBER, 2)
                elif conf < args.conf:
                    cv2.putText(frame, f'Unsure - maybe {species}', (16, 48),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.95, AMBER, 2)
                    cv2.putText(frame, f'{conf*100:.0f}% - move closer / better light',
                                (16, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, AMBER, 1)
                else:
                    cv2.putText(frame, species, (16, 48),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.05, WHITE, 2)
                    cv2.putText(frame, f'{condition}  {conf*100:.0f}%',
                                (16, 84), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                GREEN if healthy else RED, 2)
                    bw2 = int((W - 32) * conf)
                    cv2.rectangle(frame, (16, 102), (16 + bw2, 106),
                                  GREEN if healthy else RED, -1)

                if show_top3:
                    order = probs.argsort()[::-1][:3]
                    draw_panel(frame, 0, H - 96, 360, 96)
                    for i, idx in enumerate(order):
                        sp_i, cond_i, hl_i = parsed[idx]
                        name = ('background' if classes[idx] == BACKGROUND_CLASS
                                else f'{sp_i} / {cond_i}')
                        cv2.putText(frame, f'{probs[idx]*100:4.1f}%  {name[:38]}',
                                    (12, H - 66 + i * 24),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.48,
                                    WHITE if i == 0 else GREY, 1)

        if model_switch_msg and (time.time() - model_switch_t) < 2.5:
            draw_panel(frame, 0, H // 2 - 28, W, 56)
            cv2.putText(frame, model_switch_msg,
                        (20, H // 2 + 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, CYAN, 2)

        fps_hist.append(1.0 / max(time.time() - t0, 1e-6))
        mode_label = 'Full-Frame Multi-Leaf' if multi_mode else 'Single-ROI'
        cv2.putText(frame,
                    f'{np.mean(fps_hist):.1f} FPS | {infer_ms:.0f}ms'
                    f' | mode: {mode_label} (u=toggle)'
                    f' | m=cycle model',
                    (10, H - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.44, GREY, 1)

        cv2.imshow(win, frame)
        k = cv2.waitKey(1) & 0xFF
        if k in (ord('q'), 27):
            break
        elif k == ord('u'):
            multi_mode = not multi_mode
            hist.clear()
        elif k == ord('g'):
            use_gate = not use_gate
            hist.clear()
        elif k == ord('f'):
            flip = not flip
        elif k == ord('h'):
            show_top3 = not show_top3
        elif k in (ord('+'), ord('=')):
            roi_frac = min(0.95, roi_frac + 0.05)
        elif k in (ord('-'), ord('_')):
            roi_frac = max(0.2, roi_frac - 0.05)
        elif k == ord('s'):
            d = Path(args.snapshot_dir)
            d.mkdir(parents=True, exist_ok=True)
            fn = d / f'leaf_{time.strftime("%Y%m%d_%H%M%S")}.jpg'
            cv2.imwrite(str(fn), frame)
            print('saved', fn)
        elif k == ord('m') and all_models:
            model_idx = (model_idx + 1) % len(all_models)
            next_path = all_models[model_idx]
            try:
                model, classes, size, tf, parsed, model_name = load_current(next_path)
                hist.clear()
                model_switch_msg = f'Switched -> {model_name}'
                model_switch_t   = time.time()
            except Exception as e:
                model_switch_msg = f'Load failed: {e}'
                model_switch_t   = time.time()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
