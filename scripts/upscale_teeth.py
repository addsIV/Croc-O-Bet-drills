
import os
import cv2

TEETH_DIR = r"c:/Users/User/Documents/augment-projects/Croc-O-Bet/public/teeth"

def upscale_teeth():
    print("Upscaling teeth 4x...")
    for i in range(20):
        fn = f"tooth{i:02d}.png"
        path = os.path.join(TEETH_DIR, fn)
        
        if not os.path.exists(path):
            print(f"{fn} not found")
            continue
            
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        # Upscale 4x
        # Using INTER_NEAREST to keep pixel-art look if it is pixel art, 
        # or INTER_CUBIC if it's vector-like. 
        # The crocodile looks 'painted'. Let's use Lanczos (INTER_LANCZOS4) for quality.
        h, w = img.shape[:2]
        new_w = w * 4
        new_h = h * 4
        
        scaled = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        
        cv2.imwrite(path, scaled)
        print(f"Upscaled {fn} to {new_w}x{new_h}")

if __name__ == "__main__":
    upscale_teeth()
