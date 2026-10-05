
import os
import cv2
import numpy as np

# Paths
BASE_DIR = r"c:\Users\User\Documents\augment-projects\Croc-O-Bet"
SOURCE_DIR = os.path.join(BASE_DIR, "public", "teeth")
OUTPUT_DIR = os.path.join(BASE_DIR, "public", "teeth_refined")

def refine_existing_teeth():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Loading teeth from {SOURCE_DIR}...")
    
    # Process all tooth*.png files in the source directory
    for filename in os.listdir(SOURCE_DIR):
        if not (filename.startswith("tooth") and filename.endswith(".png")):
            continue
            
        file_path = os.path.join(SOURCE_DIR, filename)
        img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        
        if img is None:
            print(f"Error: Could not load {filename}")
            continue
            
        if img.shape[2] != 4:
            print(f"Warning: {filename} does not have an alpha channel. Skipping.")
            continue
            
        # Extract channels
        b, g, r, a = cv2.split(img)
        
        # 1. Anti-Aliasing (Smoothing the alpha channel)
        # Applying a small Gaussian blur to soften the jagged edges
        # (3,3) kernel with sigma 0 is usually enough for anti-aliasing without losing too much detail
        a_soft = cv2.GaussianBlur(a, (3, 3), 0)
        
        # 2. Sharpening the transition slightly if it gets too blurry
        # We want to remove jaggedness, not necessarily make it look out of focus.
        # However, for anti-aliasing, a soft edge is exactly what we want.
        # Let's try direct blur first, can adjust thresholding if user finds it too 'faded'.
        
        # Merge back
        refined_img = cv2.merge((b, g, r, a_soft))
        
        # Save to output directory
        output_path = os.path.join(OUTPUT_DIR, filename)
        cv2.imwrite(output_path, refined_img)
        print(f"Refined and saved {filename}")

if __name__ == "__main__":
    refine_existing_teeth()
    print("Refinement of existing teeth complete.")
