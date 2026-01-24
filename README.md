# Desktop Kitten 🐱
> **A tiny feline companion for your digital desktop.**

Desktop Kitten is a lightweight desktop pet application built with Python and PyQt6. This little kitten lives on your screen, walks on top of your windows, and reacts to your interactions with animations and sounds.

## ✨ Features
- **Cross-Platform**: Works on both Windows and macOS.
- **Window Awareness**: The kitten can detect the top edges of your open windows and use them as platforms to walk or sit on.
- **Physics-Based Movement**: Includes gravity, jumping, and falling logic.
- **Rich Animations**: 10+ distinct animation states including walking, running, sleeping, licking, and "being carried."
- **Interactive**:
  - **Drag & Drop**: Pick up the kitten and move it anywhere.
  - **Petting**: Use your mouse wheel over the kitten to pet it and hear it purr.
  - **Feeding**: Right-click to open a context menu and feed the pet.
- **Standalone Executable**: No Python installation required to run the final version.

## 🎮 How to Use

### Running the Executable
If you don't want to build the project from source, you can buy the pre-built, ready-to-run version on itch.io:

👉 **[Download on itch.io](https://cyberhirsch.itch.io/desktop-kitten-pet)**

Otherwise, simply run the `dist/DesktopKitten.exe` (Windows) or the app bundle (macOS) after building it.

### Bundling as an App (macOS)
To create a native `.app` bundle:
1.  Install PyInstaller: `pip install pyinstaller`
2.  Run:
    ```bash
    pyinstaller --noconfirm --windowed --name "Desktop Kitten" --add-data "assets:assets" main.py
    ```
3.  Find your app in the `dist/` folder.

### Auto-Start on Login (macOS)
1.  Open **System Settings** > **General** > **Login Items**.
2.  Click the **+** button under **Open at Login**.
3.  Select your `Desktop Kitten.app`.

### Controls
| Action | Control |
| :--- | :--- |
| **Pick up / Move** | Left-click and Drag |
| **Pet / Purr** | Scroll Mouse Wheel |
| **Menu (Feed/Quit)** | Right-click |

### Development Setup
If you want to run from source, ensure you have Python installed and install dependencies:

**Windows:**
```bash
pip install PyQt6 pywin32 Pillow
python main.py
```

**macOS:**
```bash
pip install PyQt6 pyobjc-framework-Quartz pyobjc-framework-Cocoa Pillow
python main.py
```

## 🛠️ Technical Details
- **Frontend**: PyQt6 (Frameless, transparent, always-on-top window).
- **Collision Engine**: 
  - **Windows**: `win32gui` integration to find window rectangles.
  - **macOS**: `Quartz` (CoreGraphics) integration via `pyobjc`.
- **Animation System**: Custom sprite engine handling 32x32 frames with nearest-neighbor scaling.
- **Audio**: Python `QMediaPlayer` for MP3 playback.

---
*Created with ❤️ for Cat Lovers.*
