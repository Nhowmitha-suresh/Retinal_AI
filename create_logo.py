"""
Create logo for Retinal AI application
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    """Create a logo image for the Retinal AI app"""
    # Create logo image
    width, height = 200, 200
    img = Image.new('RGB', (width, height), color='#007BFF')
    draw = ImageDraw.Draw(img)
    
    # Draw eye shape
    # Outer eye
    draw.ellipse([20, 40, 180, 160], fill='white', outline='#0056B3', width=3)
    
    # Iris
    draw.ellipse([60, 80, 140, 120], fill='#007BFF', outline='#0056B3', width=2)
    
    # Pupil
    draw.ellipse([90, 95, 110, 105], fill='#1A2B3C')
    
    # Reflection
    draw.ellipse([95, 98, 105, 103], fill='white')
    
    # Save logo
    os.makedirs('assets', exist_ok=True)
    img.save('assets/logo.png')
    print("Logo created: assets/logo.png")
    
    # Create small icon version
    icon = img.resize((64, 64), Image.Resampling.LANCZOS)
    icon.save('assets/logo_icon.png')
    print("Logo icon created: assets/logo_icon.png")

if __name__ == "__main__":
    create_logo()
