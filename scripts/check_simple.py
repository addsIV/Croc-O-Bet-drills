
import cv2
import os

BASE_DIR = r"c:\Users\User\Documents\augment-projects\Croc-O-Bet"

FILES = [
    ("Source", os.path.join(BASE_DIR, "assets", "crocodile.png")),
    ("UserRef", os.path.join(BASE_DIR, "assets", "croc01.png")),
    ("CurrentBase", os.path.join(BASE_DIR, "public", "croc_no_tooth01.png"))
]

def check():
    for name, path in FILES:
        if not os.path.exists(path):
            print(f"{name}: Missing")
            continue
            
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        h, w = img.shape[:2]
        
        # Check BBox
        if img.shape[2] == 4:
            alpha = img[:, :, 3]
            points = cv2.findNonZero(alpha)
            if points is not None:
                bx, by, bw, bh = cv2.boundingRect(points)
                print(f"{name} ({w}x{h}): Content Width={bw}, Height={bh}")
            else:
                print(f"{name} ({w}x{h}): Empty content")
        else:
            print(f"{name} ({w}x{h}): No alpha")

if __name__ == "__main__":
    check()
