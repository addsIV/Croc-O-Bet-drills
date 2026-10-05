
import cv2
import os
import re

BASE_DIR = r"c:\Users\User\Documents\augment-projects\Croc-O-Bet"
LAYOUT_FILE = os.path.join(BASE_DIR, "services", "teeth_layout.ts")
OUTPUT_FILE = os.path.join(BASE_DIR, "preview_raw_assembly.png")

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
        })
    return teeth

def overlay_image_raw(bg, fg, x, y):
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

def assemble_raw():
    print("Assembling RAW preview (No resizing)...")
    
    base_path = os.path.join(BASE_DIR, "public", "croc_no_tooth01.png")
    base_img = cv2.imread(base_path, cv2.IMREAD_UNCHANGED)
    
    if base_img is None:
        print("Failed to load base")
        return
        
    H, W = base_img.shape[:2]
    print(f"Base size: {W}x{H}")
    
    teeth_data = load_layout()
    
    for t in teeth_data:
        t_path = os.path.join(BASE_DIR, "public", "teeth", t['image'])
        if not os.path.exists(t_path): continue
            
        t_img = cv2.imread(t_path, cv2.IMREAD_UNCHANGED)
        fw, fh = t_img.shape[:2]
        
        # Calculate Percentage-based Position relative to 4096
        # This trusts 'left_pct' from the layout
        x = int((t['left_pct'] / 100.0) * W)
        y = int((t['top_pct'] / 100.0) * H)
        
        print(f"Placing Tooth {t['id']} RAW ({fw}x{fh}) at {x},{y}")
        overlay_image_raw(base_img, t_img, x, y)
        
    cv2.imwrite(OUTPUT_FILE, base_img)
    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    assemble_raw()
