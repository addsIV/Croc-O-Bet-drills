
import cv2
import os
import numpy as np

BASE_DIR = r"c:\Users\User\Documents\augment-projects\Croc-O-Bet"

FILES = [
    os.path.join(BASE_DIR, "assets", "crocodile.png"),
    os.path.join(BASE_DIR, "assets", "croc01.png"),
    os.path.join(BASE_DIR, "public", "croc_no_tooth01.png")
]

def get_bbox(path):
    if not os.path.exists(path):
        return f"{os.path.basename(path)}: Not Found"
        
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return f"{os.path.basename(path)}: Failed load"
        
    if img.shape[2] != 4:
        return f"{os.path.basename(path)}: No Alpha (Shape {img.shape})"
        
    alpha = img[:, :, 3]
    points = cv2.findNonZero(alpha)
    if points is None:
        return f"{os.path.basename(path)}: Empty"
        
    x, y, w, h = cv2.boundingRect(points)
    # Area of interest
    return f"{os.path.basename(path) } ({img.shape[1]}x{img.shape[0]}): Content Box x={x},y={y}, w={w},h={h}"

def check_content_scale():
    for f in FILES:
        print(get_bbox(f))

if __name__ == "__main__":
    check_content_scale()
