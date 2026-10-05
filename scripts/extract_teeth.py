
import os
import cv2
import numpy as np
from math import sqrt

# Paths
BASE_DIR = r"c:\Users\User\Documents\augment-projects\Croc-O-Bet"
IMG_WITH_TEETH = os.path.join(BASE_DIR, "assets", "crocodile.png")
IMG_NO_TEETH = os.path.join(BASE_DIR, "croc_no_tooth01.png")
OUTPUT_DIR = os.path.join(BASE_DIR, "assets", "teeth")

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

def extract_teeth_smart_v2():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Loading images...")
    img_full = cv2.imread(IMG_WITH_TEETH, cv2.IMREAD_UNCHANGED)
    img_bare = cv2.imread(IMG_NO_TEETH, cv2.IMREAD_UNCHANGED)

    if img_full.shape != img_bare.shape:
        img_bare = cv2.resize(img_bare, (img_full.shape[1], img_full.shape[0]))

    height, width = img_full.shape[:2]

    # Difference Analysis
    diff = cv2.absdiff(img_full, img_bare)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    # User liked the "Smart" batch, which used Threshold=25
    _, mask = cv2.threshold(diff_gray, 25, 255, cv2.THRESH_BINARY)
    
    # "Smart" used a simple Close/Open kernel
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Connected Components
    num_labels, labels_im, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
    
    # Assign seeds to blobs
    blob_seeds = {i: [] for i in range(1, num_labels)}
    pixel_coords = {}
    
    # Map tooth IDs to blob labels
    for tooth in TEETH_DATA:
        tid = tooth["id"]
        tx = int((tooth["x"] / 100.0) * width)
        ty = int((tooth["y"] / 100.0) * height)
        pixel_coords[tid] = (tx, ty)
        
        # Check label at centroid
        label = labels_im[ty, tx]
        
        # Fallback search if centroid is in hole
        if label == 0:
            for dx in range(-5, 6):
                for dy in range(-5, 6):
                    ny, nx = ty+dy, tx+dx
                    if 0 <= ny < height and 0 <= nx < width:
                        if labels_im[ny, nx] != 0:
                            label = labels_im[ny, nx]
                            break
                if label != 0: break
        
        if label != 0:
            blob_seeds[label].append(tid)

    # Output Process
    for label_idx, seeds in blob_seeds.items():
        if not seeds: continue
        
        x, y, w, h, area = stats[label_idx]
        blob_mask_roi = (labels_im[y:y+h, x:x+w] == label_idx).astype(np.uint8) * 255
        
        if len(seeds) == 1:
            # 1. CLEAN EXTRACTION (What user liked)
            # We crop the blob mask exactly
            tid = seeds[0]
            save_tooth(img_full, blob_mask_roi, x, y, w, h, tid)
            
        else:
            # 2. SPLIT ONLY FOR MULTI-SEED BLOBS (10/11, 18/19)
            print(f"Splitting blob {label_idx} for seeds {seeds}")
            
            # Use Voronoi but try to be smoother?
            # Or perhaps just a simple linear separator?
            # Creating mask for splitting
            
            grid_y, grid_x = np.indices((h, w))
            abs_x = grid_x + x
            abs_y = grid_y + y
            
            distances = {}
            for tid in seeds:
                tx, ty = pixel_coords[tid]
                # Distance to seed
                distances[tid] = (abs_x - tx)**2 + (abs_y - ty)**2
            
            tids = list(seeds)
            dist_stack = np.stack([distances[tid] for tid in tids])
            nearest_idx = np.argmin(dist_stack, axis=0)
            
            for i, tid in enumerate(tids):
                # Create sub-mask
                tooth_mask = blob_mask_roi.copy()
                tooth_mask[nearest_idx != i] = 0
                
                # Check bounding box of new mask
                pts = cv2.findNonZero(tooth_mask)
                if pts is not None:
                    nx, ny, nw, nh = cv2.boundingRect(pts)
                    sub_mask = tooth_mask[ny:ny+nh, nx:nx+nw]
                    save_tooth(img_full, sub_mask, x+nx, y+ny, nw, nh, tid)

def save_tooth(full_img, mask, x, y, w, h, tid):
    # Same save function as "Smart" logic (preserving transparency)
    
    # We crop the Full Image at the same rect as the Mask context
    # Be careful with boundaries
    H, W = full_img.shape[:2]
    
    # Crop Image
    tooth_crop = full_img[y:y+h, x:x+w].copy()
    
    # Apply Mask to Alpha
    # The mask is already at the correct size (w,h)
    
    if tooth_crop.shape[2] == 4:
        b, g, r, a = cv2.split(tooth_crop)
        # Combine original alpha with mask (AND)
        final_alpha = cv2.bitwise_and(a, mask)
        tooth_crop = cv2.merge((b, g, r, final_alpha))
    else:
        # Create alpha
        b, g, r = cv2.split(tooth_crop)
        tooth_crop = cv2.merge((b, g, r, mask))
    
    fn = f"tooth{tid:02d}.png"
    cv2.imwrite(os.path.join(OUTPUT_DIR, fn), tooth_crop)

if __name__ == "__main__":
    try:
        extract_teeth_smart_v2()
        print("Restored Smart Extraction complete.")
    except Exception as e:
        print(f"Error: {e}")
