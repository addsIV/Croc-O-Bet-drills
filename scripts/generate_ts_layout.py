
import os
import cv2
import json

# Paths
BASE_DIR = r"c:\Users\User\Documents\augment-projects\Croc-O-Bet"
TEETH_DIR = os.path.join(BASE_DIR, "public", "teeth")
OUTPUT_TS = os.path.join(BASE_DIR, "src", "services", "teeth_layout.ts")

# Copied from earlier files
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

def generate_ts():
    # Base dimensions (assuming 1024x1024 from previous checks, 
    # but strictly we should check crocodile.png. 
    # Let's assume 1024x1024 or check the file if possible.
    # We can perform read of crocodile.png too?
    # Or just use relative % from TEETH_DATA directly!
    # TEETH_DATA x,y uses %.
    # We need width_pct and height_pct and left_pct, top_pct.
    
    # We need Aspect Ratio of full image to correct w/h relative to x/y?
    # Assuming Square image (1024x1024).
    FULL_W = 1024
    FULL_H = 1024
    
    # Check actual size if possible
    croc_path = os.path.join(BASE_DIR, "assets", "crocodile.png")
    if os.path.exists(croc_path):
        img = cv2.imread(croc_path)
        FULL_H, FULL_W = img.shape[:2]
    
    layout_items = []
    
    print(f"Base size: {FULL_W}x{FULL_H}")
    
    for tooth in TEETH_DATA:
        tid = tooth["id"]
        cx_pct = tooth["x"]
        cy_pct = tooth["y"]
        
        # Determine image size
        fn = f"tooth{tid:02d}.png"
        path = os.path.join(TEETH_DIR, fn)
        
        if not os.path.exists(path):
            print(f"Missing {fn}")
            continue
            
        t_img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        h, w = t_img.shape[:2]
        
        # Center in pixels
        cx = (cx_pct / 100.0) * FULL_W
        cy = (cy_pct / 100.0) * FULL_H
        
        # Top-Left
        x = cx - (w / 2)
        y = cy - (h / 2)
        
        # Convert back to %
        left_pct = (x / FULL_W) * 100
        top_pct = (y / FULL_H) * 100
        width_pct = (w / FULL_W) * 100
        
        layout_items.append({
            "id": tid,
            "image": fn,
            "left_pct": left_pct,
            "top_pct": top_pct,
            "width_pct": width_pct
        })
        
    # Write TS file
    ts_content = "export const TEETH_LAYOUT = {\n"
    ts_content += f"  base_width: {FULL_W},\n"
    ts_content += f"  base_height: {FULL_H},\n"
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
    
    os.makedirs(os.path.dirname(OUTPUT_TS), exist_ok=True)
    with open(OUTPUT_TS, 'w') as f:
        f.write(ts_content)
        
    print(f"Generated {OUTPUT_TS}")

if __name__ == "__main__":
    generate_ts()
