
import os
import cv2

BASE_IMG = r"c:/Users/User/Documents/augment-projects/Croc-O-Bet/public/croc_no_tooth01.png"
TEETH_DIR = r"c:/Users/User/Documents/augment-projects/Croc-O-Bet/public/teeth"

def downscale_all():
    # 1. Downscale Base
    if os.path.exists(BASE_IMG):
        img = cv2.imread(BASE_IMG, cv2.IMREAD_UNCHANGED)
        h, w = img.shape[:2]
        if w == 4096:
            new_w = 1024
            new_h = 1024
            print(f"Downscaling Base from {w}x{h} to {new_w}x{new_h}")
            scaled = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
            cv2.imwrite(BASE_IMG, scaled)
        else:
            print(f"Base image width is {w}, skipping downscale.")
            
    # 2. Downscale Teeth
    # I recently upscaled them to match 4096. Now I downscale them back to match 1024.
    for i in range(20):
        fn = f"tooth{i:02d}.png"
        path = os.path.join(TEETH_DIR, fn)
        
        if not os.path.exists(path):
            continue
            
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        h, w = img.shape[:2]
        
        # We expect them to be large now (around 500-800px wide? No, 124*4 = 496).
        # We need to scale them by 0.25
        
        new_w = int(w * 0.25)
        new_h = int(h * 0.25)
        
        # Sanity check: don't downscale if already small?
        # User said "scale all the teeth to 0.25". I assume they are currently 1.0 (4096 relative).
        
        if w > 200: # Arbitrary check to ensure we don't double shrink
            print(f"Downscaling {fn} from {w}x{h} to {new_w}x{new_h}")
            scaled = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
            cv2.imwrite(path, scaled)
        else:
            print(f"Skipping {fn} (already small: {w}x{h})")

if __name__ == "__main__":
    downscale_all()
