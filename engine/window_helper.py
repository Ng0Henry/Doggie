import win32gui
import win32api
import win32con

def get_collidable_windows(exclude_hwnd=None):
    """
    Returns a list of (left, top, right, bottom) tuples for all visible, non-minimized windows.
    """
    windows = []

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
    return windows

def get_screen_bottom():
    """
    Returns the Y coordinate of the bottom of the screen (or taskbar).
    """
    # This is handled well by Qt's QScreen, but we can have it here as a fallback
    return win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
