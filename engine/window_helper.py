import sys

if sys.platform == "win32":
    import win32gui
    import win32api
    import win32con
elif sys.platform == "darwin":
    try:
        from Quartz import (
            CGWindowListCopyWindowInfo,
            kCGWindowListOptionOnScreenOnly,
            kCGWindowListExcludeDesktopElements,
            kCGNullWindowID
        )
    except ImportError:
        # Fallback for systems without pyobjc-framework-Quartz installed yet
        CGWindowListCopyWindowInfo = None

def get_collidable_windows(exclude_hwnd=None):
    """
    Returns a list of (left, top, right, bottom) tuples for all visible, non-minimized windows.
    """
    windows = []

    if sys.platform == "win32":
        def enum_handler(hwnd, l_param):
            if hwnd == exclude_hwnd:
                return
            
            # Check if window is visible
            if not win32gui.IsWindowVisible(hwnd):
                return
            
            # Check if window is minimized
            if win32gui.IsIconic(hwnd):
                return
            
            # Get window rect
            rect = win32gui.GetWindowRect(hwnd)
            left, top, right, bottom = rect
            
            # Filter out empty or hidden windows (e.g., system tray, background processes)
            # Also check title to avoid some invisible system windows
            title = win32gui.GetWindowText(hwnd)
            if not title:
                return
                
            # Basic sanity check for size
            if right - left < 50 or bottom - top < 50:
                return

            windows.append(rect)

        win32gui.EnumWindows(enum_handler, None)
    
    elif sys.platform == "darwin":
        if CGWindowListCopyWindowInfo is None:
            return []
            
        # Get all on-screen windows
        window_list = CGWindowListCopyWindowInfo(
            kCGWindowListOptionOnScreenOnly | kCGWindowListExcludeDesktopElements,
            kCGNullWindowID
        )
        
        for window in window_list:
            # Skip if it's our own window (passed as exclude_hwnd which is winId)
            # On macOS winId is a bit different, but let's check kCGWindowOwnerPID or kCGWindowNumber
            # For now, let's filter by layer and name
            
            # Layer 0 is usually normal windows
            if window.get('kCGWindowLayer', 0) != 0:
                continue
                
            # Get bounds
            bounds = window.get('kCGWindowBounds', {})
            x = bounds.get('X', 0)
            y = bounds.get('Y', 0)
            w = bounds.get('Width', 0)
            h = bounds.get('Height', 0)
            
            # Basic sanity check for size
            if w < 50 or h < 50:
                continue
                
            # Convert to (left, top, right, bottom)
            windows.append((x, y, x + w, y + h))
            
    return windows

def get_screen_bottom():
    """
    Returns the Y coordinate of the bottom of the screen (or taskbar).
    """
    if sys.platform == "win32":
        return win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    else:
        # Fallback for macOS if needed, though Qt handles this better in main.py
        return 1080 # Default fallback
