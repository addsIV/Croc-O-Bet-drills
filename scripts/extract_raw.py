
import os
import cv2
import numpy as np

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

TARGET_IDS = [10, 11, 18, 19]

def extract_raw_blobs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Loading images...")
    img_full = cv2.imread(IMG_WITH_TEETH, cv2.IMREAD_UNCHANGED)
    img_bare = cv2.imread(IMG_NO_TEETH, cv2.IMREAD_UNCHANGED)

    if img_full.shape != img_bare.shape:
        img_bare = cv2.resize(img_bare, (img_full.shape[1], img_full.shape[0]))

    height, width = img_full.shape[:2]

    # Difference & Mask
    diff = cv2.absdiff(img_full, img_bare)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(diff_gray, 25, 255, cv2.THRESH_BINARY)
    
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Connected Components
    num_labels, labels_im, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
    
    # Identify which blob belongs to which Target ID
    blob_map = {} # tid -> label_idx
    
    for tooth in TEETH_DATA:
        tid = tooth["id"]
        if tid not in TARGET_IDS: continue
        
        tx = int((tooth["x"] / 100.0) * width)
        ty = int((tooth["y"] / 100.0) * height)
        
        label = labels_im[ty, tx]
        # Search neighborhood if zero
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
            blob_map[tid] = label
        else:
            print(f"Warning: No blob found for Target {tid}")

    # Extract Full Blobs
    for tid, label_idx in blob_map.items():
        print(f"Extracting Raw Blob {label_idx} for Tooth {tid}")
        
        x, y, w, h, area = stats[label_idx]
        
        # We want the ENTIRE blob mask, no splitting
        blob_mask_roi = (labels_im[y:y+h, x:x+w] == label_idx).astype(np.uint8) * 255
        
        save_tooth(img_full, blob_mask_roi, x, y, w, h, tid)

def save_tooth(full_img, mask, x, y, w, h, tid):
    PAD = 2
    H, W = full_img.shape[:2]
    
    x1 = max(0, x - PAD)
    y1 = max(0, y - PAD)
    x2 = min(W, x + w + PAD)
    y2 = min(H, y + h + PAD)
    
    mask_h, mask_w = mask.shape
    padded_mask = np.zeros((y2-y1, x2-x1), dtype=np.uint8)
    
    off_x = x - x1
    off_y = y - y1
    
    h_paste = min(mask_h, y2-y1-off_y)
    w_paste = min(mask_w, x2-x1-off_x)
    
    if h_paste > 0 and w_paste > 0:
        padded_mask[off_y:off_y+h_paste, off_x:off_x+w_paste] = mask[:h_paste, :w_paste]
        
    tooth_crop = full_img[y1:y2, x1:x2].copy()
    
    if tooth_crop.shape[2] == 4:
        b, g, r, a = cv2.split(tooth_crop)
        final_alpha = cv2.bitwise_and(a, padded_mask)
        tooth_crop = cv2.merge((b, g, r, final_alpha))
    else:
        b, g, r = cv2.split(tooth_crop)
        tooth_crop = cv2.merge((b, g, r, padded_mask))
    
    fn = f"tooth{tid:02d}.png"
    cv2.imwrite(os.path.join(OUTPUT_DIR, fn), tooth_crop)
    print(f"    Saved {fn}")

if __name__ == "__main__":
    try:
        extract_raw_blobs()
    except Exception as e:
        print(f"Error: {e}")
