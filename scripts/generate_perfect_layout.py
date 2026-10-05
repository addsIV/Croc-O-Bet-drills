
import os
import cv2
import numpy as np

# Paths
BASE_DIR = r"c:\Users\User\Documents\augment-projects\Croc-O-Bet"
REF_IMG_PATH = os.path.join(BASE_DIR, "assets", "croc01.png") # The one WITH teeth (4096px)
TEETH_DIR = os.path.join(BASE_DIR, "public", "teeth")
OUTPUT_TS = os.path.join(BASE_DIR, "src", "services", "teeth_layout.ts")

# Coordinates (For guided search / fallback reference)
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

def generate_perfect_layout():
    print(f"Loading reference: {REF_IMG_PATH}")
    img_ref = cv2.imread(REF_IMG_PATH)
    if img_ref is None:
        print("Error: Could not load reference image!")
        return
        
    full_h, full_w = img_ref.shape[:2]
    print(f"Reference Size: {full_w}x{full_h}")
    
    layout_items = []
    
    for tooth in TEETH_DATA:
        tid = tooth["id"]
        fn = f"tooth{tid:02d}.png"
        path = os.path.join(TEETH_DIR, fn)
        
        if not os.path.exists(path):
            print(f"Error: {fn} not found!")
            continue
            
        # Load tooth img (keep alpha for now to check dimensions)
        tooth_img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        h, w = tooth_img.shape[:2]
        
        # Prepare for matching: Drop alpha, BGR only
        if tooth_img.shape[2] == 4:
            tooth_bgr = tooth_img[:, :, :3]
            # Optional: Use alpha as mask?
            # mask = tooth_img[:, :, 3] 
            # matchTemplate supports mask in TM_CCORR_NORMED and TM_SQDIFF
            # but usually BGR match is sufficient if unique enough.
        else:
            tooth_bgr = tooth_img
            
        # Guided Search ROI
        # We know roughly where it should be from TEETH_DATA
        cx_target = int((tooth["x"] / 100.0) * full_w)
        cy_target = int((tooth["y"] / 100.0) * full_h)
        
        # Large Search Window to accommodate shifts
        # But ensure we don't pick up a similar looking neighbor
        W_SEARCH = w + 200
        H_SEARCH = h + 200
        
        x1 = max(0, cx_target - W_SEARCH//2)
        y1 = max(0, cy_target - H_SEARCH//2)
        x2 = min(full_w, cx_target + W_SEARCH//2)
        y2 = min(full_h, cy_target + H_SEARCH//2)
        
        # Ensure ROI is larger than template
        if (x2 - x1) < w or (y2 - y1) < h:
            print(f"  Warning: ROI too small for Tooth {tid}. Searching full image.")
            roi = img_ref
            off_x, off_y = 0, 0
        else:
            roi = img_ref[y1:y2, x1:x2]
            off_x, off_y = x1, y1
            
        # Match
        res = cv2.matchTemplate(roi, tooth_bgr, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        # Check confidence
        if max_val < 0.8:
            print(f"  Warning: Low confidence ({max_val:.2f}) for Tooth {tid}")
        
        final_x = off_x + max_loc[0]
        final_y = off_y + max_loc[1]
        
        print(f"Tooth {tid}: Found at {final_x},{final_y} (Conf: {max_val:.4f})")
        
        # Percentages
        left_pct = (final_x / full_w) * 100
        top_pct = (final_y / full_h) * 100
        width_pct = (w / full_w) * 100
        
        layout_items.append({
            "id": tid,
            "image": fn,
            "left_pct": left_pct,
            "top_pct": top_pct,
            "width_pct": width_pct
        })

    # Write TS
    ts_content = "export const TEETH_LAYOUT = {\n"
    ts_content += f"  base_width: {full_w},\n"
    ts_content += f"  base_height: {full_h},\n"
    ts_content += "  teeth: [\n"
    
    for item in layout_items:
        ts_content += "    {\n"
        ts_content += f"      id: {item['id']},\n"
        ts_content += f"      image: '{item['image']}',\n"
        ts_content += f"      left_pct: {item['left_pct']},\n"
        ts_content += f"      top_pct: {item['top_pct']},\n"
        ts_content += f"      width_pct: {item['width_pct']}\n"
        ts_content += "    },\n"
        
    ts_content += "  ]\n"
    ts_content += "};\n"
    
    with open(OUTPUT_TS, 'w') as f:
        f.write(ts_content)
    
    print(f"Saved layout to {OUTPUT_TS}")

if __name__ == "__main__":
    generate_perfect_layout()
