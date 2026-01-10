"""
Setup script to prepare background image for Retinal AI app
Place your medical professional background image in the assets folder as:
- assets/medical_background.jpg (preferred)
- assets/medical_background.png
- assets/bg_eye.jpg
- assets/bg_eye.png

The app will automatically detect and use it.
"""
import os
from PIL import Image

def check_background_images():
    """Check if background images exist"""
    bg_paths = [
        "assets/medical_background.jpg",
        "assets/medical_background.png",
        "assets/bg_eye.jpg",
        "assets/bg_eye.png",
        "assets/image.png"
    ]
    
    print("Checking for background images...")
    found = False
    for bg_path in bg_paths:
        if os.path.exists(bg_path):
            try:
                img = Image.open(bg_path)
                print(f"[OK] Found: {bg_path} ({img.size[0]}x{img.size[1]})")
                found = True
                # Optimize image for app use
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                if bg_path.endswith('.png'):
                    # Convert PNG to JPG for better performance
                    new_path = bg_path.replace('.png', '.jpg')
                    if not os.path.exists(new_path):
                        img.save(new_path, 'JPEG', quality=85)
                        print(f"  -> Created optimized version: {new_path}")
                break
            except Exception as e:
                print(f"[ERROR] Error reading {bg_path}: {e}")
    
    if not found:
        print("\n[WARN] No background image found!")
        print("Please place your medical professional image in assets/ folder as:")
        print("  - assets/medical_background.jpg (recommended)")
        print("  - assets/medical_background.png")
        print("  - assets/bg_eye.jpg")
        print("  - assets/bg_eye.png")
    else:
        print("\n[OK] Background image is ready!")

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    check_background_images()
