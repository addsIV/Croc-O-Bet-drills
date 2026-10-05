
import cv2
import os

BASE_DIR = r"c:\Users\User\Documents\augment-projects\Croc-O-Bet"

FILES = [
    os.path.join(BASE_DIR, "assets", "crocodile.png"),
    os.path.join(BASE_DIR, "assets", "croc01.png"),
    os.path.join(BASE_DIR, "public", "croc_no_tooth01.png")
]

def check_images():
    for f in FILES:
        if os.path.exists(f):
            img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
            if img is not None:
                print(f"{os.path.basename(f)}: {img.shape}")
            else:
                print(f"{os.path.basename(f)}: Failed to load")
        else:
            print(f"{os.path.basename(f)}: Not Found")

if __name__ == "__main__":
    check_images()
