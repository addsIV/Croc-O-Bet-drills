
import cv2
import os
import re
import numpy as np

BASE_DIR = r"c:\Users\User\Documents\augment-projects\Croc-O-Bet"
LAYOUT_FILE = os.path.join(BASE_DIR, "services", "teeth_layout.ts")
OUTPUT_FILE = os.path.join(BASE_DIR, "preview_assembly.png")

def load_layout():
    with open(LAYOUT_FILE, "r") as f:
        content = f.read()
    
    # Simple regex parsing
    # teeth: [ { id: 0, ... width_pct: 12.1... }, ... ]
    teeth = []
    
    # ID
    ids = re.findall(r"id:\s*(\d+)", content)
    # Image
    images = re.findall(r"image:\s*'([^']+)'", content)
    # Left
    lefts = re.findall(r"left_pct:\s*([\d\.]+)", content)
    # Top
    tops = re.findall(r"top_pct:\s*([\d\.]+)", content)
    # Width
    widths = re.findall(r"width_pct:\s*([\d\.]+)", content)
    
    for i in range(len(ids)):
        teeth.append({
            "id": int(ids[i]),
            "image": images[i],
            "left_pct": float(lefts[i]),
            "top_pct": float(tops[i]),
            "width_pct": float(widths[i])
        })
    return teeth

def overlay_image(bg, fg, x, y, w, h):
    # Resize fg to w, h
    fg_resized = cv2.resize(fg, (w, h), interpolation=cv2.INTER_AREA)
    
    # Overlay with alpha
    # x,y are top-left
    
    bh, bw = bg.shape[:2]
    fh, fw = fg_resized.shape[:2]
    
    # Clipping
    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(bw, x + fw)
    y2 = min(bh, y + fh)
    
    fg_x1 = max(0, -x)
    fg_y1 = max(0, -y)
    fg_x2 = fg_x1 + (x2 - x1)
    fg_y2 = fg_y1 + (y2 - y1)
    
    if (x2 <= x1) or (y2 <= y1): return bg
    
    fg_crop = fg_resized[fg_y1:fg_y2, fg_x1:fg_x2]
    bg_crop = bg[y1:y2, x1:x2]
    
    alpha_fg = fg_crop[:, :, 3] / 255.0
    alpha_bg = 1.0 - alpha_fg
    
    for c in range(3):
        bg_crop[:, :, c] = (alpha_fg * fg_crop[:, :, c] + alpha_bg * bg_crop[:, :, c])
        
    return bg

def assemble():
    print("Assembling preview...")
    
    # Load Base
    base_path = os.path.join(BASE_DIR, "public", "croc_no_tooth01.png")
    base_img = cv2.imread(base_path, cv2.IMREAD_UNCHANGED)
    
    if base_img is None:
        print("Failed to load base image")
        return

    H, W = base_img.shape[:2]
    print(f"Base size: {W}x{H}")

    teeth_data = load_layout()
    
    for t in teeth_data:
        t_path = os.path.join(BASE_DIR, "public", "teeth", t['image'])
        if not os.path.exists(t_path):
            print(f"Missing tooth {t['image']}")
            continue
            
        t_img = cv2.imread(t_path, cv2.IMREAD_UNCHANGED)
        
        # Calculate pixel position for 4096 (W)
        x = int((t['left_pct'] / 100.0) * W)
        y = int((t['top_pct'] / 100.0) * H)
        target_w = int((t['width_pct'] / 100.0) * W)
        
        # Determine aspect ratio
        th, tw = t_img.shape[:2]
        aspect = th / tw
        target_h = int(target_w * aspect)
        
        print(f"Placing Tooth {t['id']} at {x},{y} Size {target_w}x{target_h}")
        overlay_image(base_img, t_img, x, y, target_w, target_h)
        
    cv2.imwrite(OUTPUT_FILE, base_img)
    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    assemble()
