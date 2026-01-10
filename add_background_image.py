"""
Helper script to add your medical professional background image
Usage: Place your image file in the same directory and run this script
"""
import os
from PIL import Image
import shutil

def add_background_image(image_path=None):
    """Add background image to assets folder"""
    os.makedirs("assets", exist_ok=True)
    
    if image_path is None:
        # Look for common image files in current directory
        image_files = [f for f in os.listdir('.') if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        
        if not image_files:
            print("No image files found in current directory.")
            print("\nTo add your medical professional background image:")
            print("1. Place your image file in this directory")
            print("2. Run: python add_background_image.py <your_image.jpg>")
            print("\nOr manually copy your image to: assets/medical_background.jpg")
            return False
        
        print("Found image files:")
        for i, img in enumerate(image_files, 1):
            print(f"  {i}. {img}")
        
        if len(image_files) == 1:
            image_path = image_files[0]
            print(f"\nUsing: {image_path}")
        else:
            print("\nMultiple images found. Please specify which one to use:")
            print("Run: python add_background_image.py <image_filename>")
            return False
    
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found!")
        return False
    
    try:
        # Open and optimize the image
        img = Image.open(image_path)
        print(f"Original image: {img.size[0]}x{img.size[1]} pixels, mode: {img.mode}")
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
            print("Converted to RGB mode")
        
        # Save as optimized JPG
        output_path = "assets/medical_background.jpg"
        img.save(output_path, 'JPEG', quality=90, optimize=True)
        print(f"\n[SUCCESS] Background image saved as: {output_path}")
        print(f"Size: {img.size[0]}x{img.size[1]} pixels")
        print("\nThe app will now use this image as the background!")
        return True
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

if __name__ == "__main__":
    import sys
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    add_background_image(image_path)
