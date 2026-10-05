
import os
import cv2
import json
import numpy as np

# Paths
BASE_DIR = r"c:\Users\User\Documents\augment-projects\Croc-O-Bet"
IMG_FULL = os.path.join(BASE_DIR, "assets", "crocodile.png")
TEETH_DIR = os.path.join(BASE_DIR, "assets", "teeth")
OUTPUT_JSON = os.path.join(BASE_DIR, "src", "teeth_layout.json")

# Coordinates 
TEETH_DATA = [
    { "x": 33.125, "y": 37.25, "id": 0 },
    { "x": 36.875, "y": 37, "id": 1 },
    { "x": 41.125, "y": 34.25, "id": 2 },
    { "x": 46.375, "y": 30.25, "id": 3 },
    { "x": 52.5, "y": 28.875, "id": 4 },
    { "x": 58.75, "y": 28.875, "id": 5 },
    { "x": 64.875, "y": 30.75, "id": 6 },
    { "x": 69.875, "y": 33.125, "id": 7 },
    { "x": 74.125, "y": 37.125, "id": 8 },
    { "x": 78, "y": 37, "id": 9 },
    { "x": 35.25, "y": 63.24999999999999, "id": 10 },
    { "x": 38.625, "y": 66.375, "id": 11 },
    { "x": 42.5, "y": 68.5, "id": 12 },
    { "x": 47.5, "y": 71.125, "id": 13 },
    { "x": 53, "y": 72.75, "id": 14 },
    { "x": 58.5, "y": 72.875, "id": 15 },
    { "x": 63.87500000000001, "y": 70.875, "id": 16 },
    { "x": 68.625, "y": 68.875, "id": 17 },
    { "x": 72.875, "y": 65.875, "id": 18 },
    { "x": 75.75, "y": 63.375, "id": 19 }
]

def generate_layout():
    print("Loading full image...")
    img_full = cv2.imread(IMG_FULL)
    full_h, full_w = img_full.shape[:2]
    
    layout = []
    
    for i in range(20):
        fn = f"tooth{i:02d}.png"
        path = os.path.join(TEETH_DIR, fn)
        
        if not os.path.exists(path):
            print(f"Error: {fn} matching failed - file not found")
            continue
            
        tooth_img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        
        if tooth_img.shape[2] == 4:
            b,g,r,a = cv2.split(tooth_img)
            tooth_bgr = cv2.merge((b,g,r))
        else:
            tooth_bgr = tooth_img
            
        print(f"Matching {fn}...")
        
        # Guided Search ROI
        target = TEETH_DATA[i]
        tx_center = int((target["x"] / 100.0) * full_w)
        ty_center = int((target["y"] / 100.0) * full_h)
        
        # Define search window (e.g. 150x150 pixels around center)
        W_SEARCH = 400
        H_SEARCH = 400
        
        y1 = max(0, ty_center - H_SEARCH//2)
        y2 = min(full_h, ty_center + H_SEARCH//2)
        x1 = max(0, tx_center - W_SEARCH//2)
        x2 = min(full_w, tx_center + W_SEARCH//2)
        
        roi = img_full[y1:y2, x1:x2]
        
        # Check if template fits in ROI
        th, tw = tooth_bgr.shape[:2]
        rh, rw = roi.shape[:2]
        
        if th > rh or tw > rw:
            print(f"  Template ({tw}x{th}) larger than ROI ({rw}x{rh}). Falling back to full search.")
            roi = img_full
            x1, y1 = 0, 0
        
        res = cv2.matchTemplate(roi, tooth_bgr, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        # max_loc is relative to ROI
        rel_x, rel_y = max_loc
        abs_x = rel_x + x1
        abs_y = rel_y + y1
        
        h, w = tooth_img.shape[:2]
        
        print(f"  Found at {abs_x},{abs_y} (Conf: {max_val:.4f})")
        
        layout.append({
            "id": i,
            "x": int(abs_x),
            "y": int(abs_y),
            "width": int(w),
            "height": int(h),
            "image": fn
        })
        
    # Calculate percentage for responsive layout? 
    # Frontend uses responsive image.
    # We should return percentages or assume a base width/height.
    # Let's save both pixel and relative %
    
    full_h, full_w = img_full.shape[:2]
    
    final_data = {
        "base_width": full_w,
        "base_height": full_h,
        "teeth": []
    }
    
    for item in layout:
        item["left_pct"] = (item["x"] / full_w) * 100
        item["top_pct"] = (item["y"] / full_h) * 100
        item["width_pct"] = (item["width"] / full_w) * 100
        final_data["teeth"].append(item)
        
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(final_data, f, indent=2)
        
    print(f"Layout saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    generate_layout()
