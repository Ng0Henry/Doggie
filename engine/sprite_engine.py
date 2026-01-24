from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

class SpriteEngine:
    def __init__(self, sheet_path, sprite_size=32, scale=4):
        self.sprite_size = sprite_size
        self.scale = scale
        self.target_size = sprite_size * scale
        
        # Load the original sheet
        self.full_sheet = QImage(sheet_path)
        if self.full_sheet.isNull():
            raise FileNotFoundError(f"Could not load spritesheet at {sheet_path}")
            
        self.animations = {}
        
    def load_animation(self, name, row, frames, col_start=0):
        """
        Extracts frames from the sheet, scales them, and stores both Right and Left versions.
        """
        right_frames = []
        left_frames = []
        
        for i in range(frames):
            x = (col_start + i) * self.sprite_size
            y = row * self.sprite_size
            
            # Extract
            sprite = self.full_sheet.copy(x, y, self.sprite_size, self.sprite_size)
            
            # Scale (Nearest Neighbor / FastTransformation)
            scaled = sprite.scaled(self.target_size, self.target_size, 
                                   Qt.AspectRatioMode.IgnoreAspectRatio, 
                                   Qt.TransformationMode.FastTransformation)
            
            # Create Flipped version
            flipped = scaled.mirrored(True, False)
            
            # Convert to Pixmap for faster rendering
            right_frames.append(QPixmap.fromImage(scaled))
            left_frames.append(QPixmap.fromImage(flipped))
            
        self.animations[name] = {
            "right": right_frames,
            "left": left_frames
        }

    def get_frame(self, anim_name, frame_idx, direction):
        if anim_name not in self.animations:
            return None
        
        frames = self.animations[anim_name]["right" if direction == "right" else "left"]
        return frames[frame_idx % len(frames)]
