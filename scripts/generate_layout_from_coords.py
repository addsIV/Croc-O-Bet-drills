
import json
import os
import re
import cv2

BASE_DIR = r"c:\Users\User\Documents\augment-projects\Croc-O-Bet"
COORDS_FILE = os.path.join(BASE_DIR, "services", "teeth_coordinates.ts")
OUTPUT_TS = os.path.join(BASE_DIR, "services", "teeth_layout.ts")
TEETH_DIR = os.path.join(BASE_DIR, "public", "teeth")
BASE_IMG = os.path.join(BASE_DIR, "public", "croc_no_tooth01.png")

def parse_ts_coords():
    with open(COORDS_FILE, "r") as f:
        content = f.read()
    
    # Extract JSON-like objects
    # { "x": 33.125, "y": 37.25, "id": 0 }
    
    matches = re.finditer(r'\{\s*"x":\s*([\d\.]+),\s*"y":\s*([\d\.]+),\s*"id":\s*(\d+)\s*\}', content)
    
    coords = []
    for m in matches:
        coords.append({
            "x": float(m.group(1)),
            "y": float(m.group(2)),
            "id": int(m.group(3))
        })
    return coords

def generate_layout():
    coords = parse_ts_coords()
    if not coords:
        print("Failed to parse coordinates")
        return

    # Check Base Dimensions for aspect ratio conversions if needed
    # But since x,y are %, and w,h are pixels...
    # We need to express w,h as %.
    # So we need Base Dimensions.
    
    # Force 4096 as per user requirement to match High Res Base
    BW, BH = 4096, 4096
    print(f"Forcing Base Dimensions: {BW}x{BH}")

    layout_items = []

    for c in coords:
        tid = c["id"]
        fn = f"tooth{tid:02d}.png"
        path = os.path.join(TEETH_DIR, fn)
        
        if not os.path.exists(path):
            print(f"Tooth {tid} missing")
            continue
            
        t_img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        h, w = t_img.shape[:2]
        
        # Center in Pixels
        cx = (c["x"] / 100.0) * BW
        cy = (c["y"] / 100.0) * BH
        
        # Top Left in Pixels
        x = cx - (w / 2)
        y = cy - (h / 2)
        
        # Convert to %
        left_pct = (x / BW) * 100
        top_pct = (y / BH) * 100
        width_pct = (w / BW) * 100
        
        print(f"Tooth {tid}: Center({c['x']},{c['y']}) -> TopLeft({left_pct:.2f},{top_pct:.2f}) Width({w}px / {width_pct:.2f}%)")
        
        layout_items.append({
            "id": tid,
            "image": fn,
            "left_pct": left_pct,
            "top_pct": top_pct,
            "width_pct": width_pct
        })
        
    # Write TS
    ts_content = "export const TEETH_LAYOUT = {\n"
    ts_content += f"  base_width: {BW},\n"
    ts_content += f"  base_height: {BH},\n"
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
    
    print(f"Generated {OUTPUT_TS}")

if __name__ == "__main__":
    generate_layout()
