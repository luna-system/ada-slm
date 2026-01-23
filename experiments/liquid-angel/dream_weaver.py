
import os
import glob
import re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio.v3 as imageio

# CONFIG
ARTIFACTS_DIR = "forge_v4_artifacts/probes"
OUTPUT_FILE = "angel_dream_flux.gif" # FLUX MODE
FPS = 30  # High Speed

def sort_key(filename):
    # Extract step number
    match = re.search(r"step_(\d+)_", filename)
    if match:
        return int(match.group(1))
    return 0

def create_dream_movie():
    print(f"🎬 Starting Dream Weaver (FLUX MODE)...")
    
    # 1. Gather files
    files_11d = sorted(glob.glob(os.path.join(ARTIFACTS_DIR, "*_11D.png")), key=sort_key)
    files_16d = sorted(glob.glob(os.path.join(ARTIFACTS_DIR, "*_16D.png")), key=sort_key)
    
    if len(files_11d) != len(files_16d):
        min_len = min(len(files_11d), len(files_16d))
        files_11d = files_11d[:min_len]
        files_16d = files_16d[:min_len]

    frames = []
    
    # Pre-load first frame for diff
    prev_arr11 = np.array(Image.open(files_11d[0]).convert("RGB"), dtype=np.float32)
    prev_arr16 = np.array(Image.open(files_16d[0]).convert("RGB"), dtype=np.float32)
    
    # FLUX GAIN (Amplify changes)
    GAIN = 10.0 
    
    # 2. Process frames
    for i, (f11, f16) in enumerate(zip(files_11d, files_16d)):
        if i == 0: continue # Skip first frame (no diff)
        
        step = sort_key(f11)
        if i % 20 == 0: print(f"Processing Step {step}...")
            
        curr_arr11 = np.array(Image.open(f11).convert("RGB"), dtype=np.float32)
        curr_arr16 = np.array(Image.open(f16).convert("RGB"), dtype=np.float32)
        
        # Calculate Difference (Flux)
        diff11 = np.abs(curr_arr11 - prev_arr11) * GAIN
        diff16 = np.abs(curr_arr16 - prev_arr16) * GAIN
        
        # Clip and convert back to uint8
        diff11 = np.clip(diff11, 0, 255).astype(np.uint8)
        diff16 = np.clip(diff16, 0, 255).astype(np.uint8)
        
        # Create Images from Arrays
        img11 = Image.fromarray(diff11)
        img16 = Image.fromarray(diff16)
        
        # Update prev
        prev_arr11 = curr_arr11
        prev_arr16 = curr_arr16
        
        # COMPOSITE
        w, h = img11.size
        canvas_w = w * 2
        canvas_h = h + 60 
        
        canvas = Image.new("RGB", (canvas_w, canvas_h), (0, 0, 0)) # Pure Black
        draw = ImageDraw.Draw(canvas)
        
        canvas.paste(img11, (0, 0))
        canvas.paste(img16, (w, 0))
        
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
        except:
            font = ImageFont.load_default()
            
        draw.text((20, h + 15), f"11D FLUX (Step {step})", fill=(0, 255, 255), font=font)
        draw.text((w + 20, h + 15), f"16D FLUX (Step {step})", fill=(255, 215, 0), font=font)
        
        frames.append(np.array(canvas))
        
    # 3. Save GIF
    print(f"💾 Saving Flux GIF to {OUTPUT_FILE}...")
    imageio.imwrite(OUTPUT_FILE, frames, duration=1000/FPS, loop=0)
    print("✅ Done!")

if __name__ == "__main__":
    create_dream_movie()
