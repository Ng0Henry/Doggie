import os
import wave
import struct
import math
from PIL import Image

def clean_spritesheet(input_path, output_path):
    print(f"Cleaning spritesheet: {input_path}")
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    
    # Simple background removal (light grey)
    # The background is approximately (164, 180, 192) or similar
    data = img.getdata()
    new_data = []
    for item in data:
        # If it's grey-ish (R,G,B are close to each other and above 150)
        # or if it's the specific grid color
        r, g, b, a = item
        if abs(r - g) < 20 and abs(r - b) < 20 and r > 150:
            new_data.append((255, 255, 255, 0))
        elif r == 115 and g == 129 and b == 135: # Grid color detection
             new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    
    # Detect columns (256px -> 8 cols, 320px -> 10 cols)
    cols = 8 if width == 256 else 10
    final_sheet = Image.new("RGBA", (cols * 32, 320), (0, 0, 0, 0))
    
    cell_w = width // cols
    cell_h = height // 10
    
    for row in range(10):
        for col in range(cols):
            left = col * cell_w
            top = row * cell_h
            right = left + cell_w
            bottom = top + cell_h
            
            sprite = img.crop((left, top, right, bottom))
            # Resize to 32x32
            sprite = sprite.resize((32, 32), Image.Resampling.LANCZOS)
            final_sheet.paste(sprite, (col * 32, row * 32))
            
    final_sheet.save(output_path)
    print(f"Saved cleaned spritesheet to {output_path} (detected {cols} columns)")

def generate_purr(output_path):
    print(f"Generating purr sound: {output_path}")
    sample_rate = 44100
    duration = 1.0  # seconds
    n_samples = int(sample_rate * duration)
    
    with wave.open(output_path, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2) # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            # Base frequency (low rumble)
            freq = 25.0 + 5.0 * math.sin(2 * math.pi * 5 * t) # slight modulation
            value = 0.5 * math.sin(2 * math.pi * freq * t)
            # Add some harmonics for "raspiness"
            value += 0.2 * math.sin(2 * math.pi * freq * 2 * t)
            # Amplitude modulation (the "thrumming" breath)
            value *= 0.5 + 0.5 * math.sin(2 * math.pi * 3 * t)
            
            sample = int(value * 32767.0)
            wav_file.writeframes(struct.pack('<h', sample))
    print(f"Saved purr to {output_path}")

if __name__ == "__main__":
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        
    spritesheet_raw = os.path.join(assets_dir, "spritesheet.png")
    spritesheet_clean = os.path.join(assets_dir, "spritesheet_clean.png")
    purr_wav = os.path.join(assets_dir, "purr.wav")
    
    if os.path.exists(spritesheet_raw):
        clean_spritesheet(spritesheet_raw, spritesheet_clean)
        # Use the clean one as the main one
        os.replace(spritesheet_clean, spritesheet_raw)
        
    # generate_purr(purr_wav)
