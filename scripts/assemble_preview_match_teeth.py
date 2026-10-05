
import cv2
import os
import re

BASE_DIR = r"c:\Users\User\Documents\augment-projects\Croc-O-Bet"
LAYOUT_FILE = os.path.join(BASE_DIR, "services", "teeth_layout.ts")
OUTPUT_FILE = os.path.join(BASE_DIR, "preview_match_teeth.png")

def load_layout():
    with open(LAYOUT_FILE, "r") as f:
        content = f.read()
    
    ids = re.findall(r"id:\s*(\d+)", content)
    images = re.findall(r"image:\s*'([^']+)'", content)
    lefts = re.findall(r"left_pct:\s*([\d\.]+)", content)
    tops = re.findall(r"top_pct:\s*([\d\.]+)", content)
    
    teeth = []
    for i in range(len(ids)):
        teeth.append({
            "id": int(ids[i]),
            "image": images[i],
            "left_pct": float(lefts[i]),
            "top_pct": float(tops[i]),
            # Ignoring width_pct, using NATIVE size
        })
    return teeth

def overlay_image(bg, fg, x, y):
    bh, bw = bg.shape[:2]
    fh, fw = fg.shape[:2]
    
    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(bw, x + fw)
    y2 = min(bh, y + fh)
    
    fg_x1 = max(0, -x)
    fg_y1 = max(0, -y)
    fg_x2 = fg_x1 + (x2 - x1)
    fg_y2 = fg_y1 + (y2 - y1)
    
    if (x2 <= x1) or (y2 <= y1): return bg
    
    fg_crop = fg[fg_y1:fg_y2, fg_x1:fg_x2]
    bg_crop = bg[y1:y2, x1:x2]
    
    alpha_fg = fg_crop[:, :, 3] / 255.0
    alpha_bg = 1.0 - alpha_fg
    
    for c in range(3):
        bg_crop[:, :, c] = (alpha_fg * fg_crop[:, :, c] + alpha_bg * bg_crop[:, :, c])
        
    return bg

def assemble():
    print("Assembling preview based on Teeth Native Size...")
    
    # Load Teeth 0 to gauge scale
    t0_path = os.path.join(BASE_DIR, "public", "teeth", "tooth00.png")
    t0_img = cv2.imread(t0_path, cv2.IMREAD_UNCHANGED)
    t0_w = t0_img.shape[1]
    
    # We know from layout that Tooth 0 width_pct is ~12.1%
    # So BaseWidth should be: t0_w / 0.121
    # 124 / 0.121 ~= 1024.
    TARGET_BASE_W = int(t0_w / 0.121)
    TARGET_BASE_H = TARGET_BASE_W # Square aspect assumed
    
    print(f"Tooth 0 width: {t0_w}. IMPLIED Base Width: {TARGET_BASE_W}")
    
    # Load Base
    base_path = os.path.join(BASE_DIR, "public", "croc_no_tooth01.png")
    base_img = cv2.imread(base_path, cv2.IMREAD_UNCHANGED)
    h, w = base_img.shape[:2]
    
    # Resize Base to match the Implied Scale of the teeth
    print(f"Original Base: {w}x{h}. Resizing to {TARGET_BASE_W}x{TARGET_BASE_H}")
    base_resized = cv2.resize(base_img, (TARGET_BASE_W, TARGET_BASE_H), interpolation=cv2.INTER_AREA)

    teeth_data = load_layout()
    
    for t in teeth_data:
        t_path = os.path.join(BASE_DIR, "public", "teeth", t['image'])
        if not os.path.exists(t_path): continue
            
        t_img = cv2.imread(t_path, cv2.IMREAD_UNCHANGED)
        
        # Position using percentages on the Resized Base
        x = int((t['left_pct'] / 100.0) * TARGET_BASE_W)
        y = int((t['top_pct'] / 100.0) * TARGET_BASE_H)
        
        # Overlay NATIVE tooth (no resizing of tooth!)
        overlay_image(base_resized, t_img, x, y)
        
    cv2.imwrite(OUTPUT_FILE, base_resized)
    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    assemble()
