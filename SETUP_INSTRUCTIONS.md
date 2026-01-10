# Setup Instructions for Retinal AI App

## Setting Up Your Background Image

To use your medical professional image as the background:

1. **Save your image file** in the `assets/` folder with one of these names:
   - `assets/medical_background.jpg` (RECOMMENDED - best quality)
   - `assets/medical_background.png`
   - `assets/bg_eye.jpg`
   - `assets/bg_eye.png`

2. **Image Requirements:**
   - Format: JPG or PNG
   - Recommended size: 1920x1080 or larger
   - The app will automatically resize it to fit your screen

3. **Run the setup script** to verify:
   ```bash
   python setup_background.py
   ```

## Logo

The app logo has been automatically created and saved as:
- `assets/logo.png` - Full logo (used in splash screen and login)
- `assets/logo_icon.png` - Small icon (used in topbar)

## Running the App

Simply run:
```bash
python blindness.py
```

The app will automatically:
- Use your medical professional image as background (if placed correctly)
- Display the logo on splash screen, login page, and topbar
- Fall back to a clean gradient background if no image is found
