
# Project Briefing: Desktop Companion Pet

## 1. Project Overview
**Goal:** Create a standalone, single-file (`.exe`) desktop pet for Windows.
**Core Concept:** A pixel-art cat that lives on the top of windows or the screen bottom (taskbar or screen edge). It behaves like a "living" entity—waking, sleeping, and demanding attention—without interrupting the user's workflow.
**Visual Style:** Retro Pixel Art, scaled up **4x** (Nearest Neighbor) for crisp visibility on modern displays.

## 2. Technical Stack
*   **Language:** Python 3.10+
*   **GUI:** PyQt6 (Qt6)
*   **Build:** PyInstaller (OneFile mode)
*   **Audio:** `QSoundEffect` (WAV)

## 3. Visual & Windowing Specifications

### 3.1. The Window
*   **Scaling:** Base sprite is 32x32. Window size will be locked to **128x128** (4x scale).
*   **Upscaling Algorithm:** `Qt.TransformationMode.FastTransformation` (Nearest Neighbor) to preserve hard pixel edges and avoid blur.
*   **Layering:** `Qt.WindowStaysOnTopHint`.
    *   *Note:* The cat will overlay web browsers (YouTube) but will naturally be hidden behind "Exclusive Fullscreen" games (e.g., Call of Duty) by Windows OS management.
*   **Transparency:** `Qt.FramelessWindowHint` + `Qt.WA_TranslucentBackground`.

### 3.2. Focus Policy (Non-Intrusive)
*   **Attribute:** `Qt.WindowDoesNotAcceptFocus`.
*   **Behavior:** Clicking the cat (to drag/pet) will **not** steal focus from the active window. The user can continue typing in Word/Discord immediately after interacting with the cat, without needing to click back on their document.

## 4. Movement & Physics

### 4.1. Floor & Platform Detection
*   **Gravity:** Constant downward pull ($+Y$).
*   **Dynamic Floors:** The cat can stand on:
    1.  **Screen Floor:** Calculated via `QScreen.availableGeometry().bottom()`.
    2.  **Window Edges:** Top edges of visible, non-minimized windows.
*   **Window Tracking Logic:**
    *   The app will periodically (e.g., every 500ms) query the Windows API (`EnumWindows` + `GetWindowRect`) to build a list of "collidable" rectangles.
    *   If the window the cat is currently standing on moves or is closed, the cat enters the `CARRY_FALL` animation and falls until it hits the next available surface.
    *   **Filter:** Ignore the cat's own window and transparent/invisible windows.

### 4.2. Wall Logic (The "Loiter" Behavior)
*   **Boundary:** Screen Left (0) and Screen Right (Max Width).
*   **Behavior:** When `x <= 0` or `x >= ScreenWidth - 128`:
    1.  **Stop Moving.**
    2.  Force State $\to$ `IDLE` or `LOOK_SIDE`.
    3.  Wait for random timer (e.g., 2-5 seconds).
    4.  Force Direction flip $\to$ Resume `WALK`.

## 5. Game Mechanics

### 5.1. Hunger System
*   **Timer:** A background timer tracks `last_fed_timestamp`.
*   **Threshold:** 2 Hours (7200 seconds).
*   **Effect (Hungry):**
    *   **Mood:** "Annoying."
    *   **Logic Change:** Move Speed increases by 50%. Probability of switching from `IDLE` to `RUN` increases significantly. Cat refuses to `SLEEP`.
*   **Resolution:** Right-click context menu $\to$ "Feed" resets timer and triggers `SLEEP` (Food Coma).

### 5.2. Interaction Map
| User Input | Action | Response |
| :--- | :--- | :--- |
| **Mouse Wheel** | Pet | Play **Purr Sound**. Play `PLAY` or `EMOTE` animation. |
| **L-Click (Hold)** | Carry | Physics Off. Window follows mouse. Anim: `CARRY_HELD`. |
| **L-Click (Release)**| Drop | Physics On. Anim: `CARRY_FALL` until floor hit $\to$ `LANDING`. |
| **Right Click** | Menu | Show Context Menu: "Feed", "Close". |
| **Passive** | Sound | **Silence.** No footstep sounds during walking. |

## 6. Animation Dictionary (Updated for 4x Scale)

*Note: The Logic uses the 32px grid coordinates, but the Viewport scales the result by 4.*

```python
ANIMATIONS = {
    # Loops
    "IDLE":       {"row": 0, "frames": 4,  "speed": 200},
    "LOOK_SIDE":  {"row": 1, "frames": 4,  "speed": 200},
    "LICK":       {"row": 2, "frames": 4,  "speed": 150},
    "CLEAN":      {"row": 3, "frames": 4,  "speed": 150},
    "TROT":       {"row": 4, "frames": 8,  "speed": 100}, 
    "RUN":        {"row": 5, "frames": 8,  "speed": 80},  
    "SLEEP":      {"row": 6, "frames": 4,  "speed": 400},
    "PLAY":       {"row": 7, "frames": 6,  "speed": 120},
    "JUMP":       {"row": 8, "frames": 7,  "speed": 150}, 
    "EMOTE":      {"row": 9, "frames": 8,  "speed": 150},
    
    # Carry / Land Complex (Row 8)

    "CARRY_HELD": {"row": 8, "frames": 1,  "col_start": 2}, 
    "CARRY_FALL": {"row": 8, "frames": 1,  "col_start": 3}, 
    "LANDING":    {"row": 8, "frames": 3,  "col_start": 4, "speed": 100} 
}
```

## 7. Implementation Steps

1.  **Asset Prep:**
    *   Create `spritesheet.png` (32px grid).
    *   Create `purr.wav`.
2.  **Sprite Engine:**
    *   Load Sheet.
    *   **Scale Up:** Immediately transform all frames to 128x128 using `FastTransformation`.
    *   Generate Mirrored (Left) versions.
3.  **Window Setup:**
    *   Initialize `QMainWindow` (128x128).
    *   Apply Flags: `Frameless`, `StaysOnTop`, `Translucent`, `NoFocus`.
4.  **Logic Core:**
    *   Setup `QTimer` (Tick Rate: 30ms).
    *   Implement Physics (Gravity + Floor Clamp).
    *   Implement "Loiter" Wall detection.
5.  **State Machine:**
    *   Implement Hunger Timer.
    *   Connect Input Events (Wheel, Click, Drag).
6.  **Build:**
    *   PyInstaller command: `pyinstaller --noconsole --onefile --add-data "assets;assets" main.py`