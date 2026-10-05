
import os
import cv2

BASE_IMG = r"c:/Users/User/Documents/augment-projects/Croc-O-Bet/public/croc_no_tooth01.png"
TEETH_DIR = r"c:/Users/User/Documents/augment-projects/Croc-O-Bet/public/teeth"

def upscale_to_4k():
    print("Scaling assets to 4096px base...")
    
    # 1. Base
    if os.path.exists(BASE_IMG):
        img = cv2.imread(BASE_IMG, cv2.IMREAD_UNCHANGED)
        h, w = img.shape[:2]
        if w < 4096:
            scale = 4096 / w
            new_w = 4096
            new_h = int(h * scale)
            print(f"Upscaling Base {w}x{h} -> {new_w}x{new_h}")
            scaled = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
            cv2.imwrite(BASE_IMG, scaled)
    
    # 2. Teeth
    for i in range(20):
        fn = f"tooth{i:02d}.png"
        path = os.path.join(TEETH_DIR, fn)
        if not os.path.exists(path): continue
        
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        h, w = img.shape[:2]
        
        # Determine current scale relative to 4096.
        # If I downscaled them to match 1024, they are ~124px.
        # I want them to match 4096, so ~500px.
        # I will scale by (4096 / 1024) = 4.
        # BUT i should check current base size to be safe?
        # Assuming they are currently 1024-scale.
        
        if w < 200: # Heuristic for 1024-scale
            new_w = w * 4
            new_h = h * 4
            print(f"Upscaling {fn} {w}x{h} -> {new_w}x{new_h}")
            scaled = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
            cv2.imwrite(path, scaled)

if __name__ == "__main__":
    upscale_to_4k()
