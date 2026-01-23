
import numpy as np
import os
import glob
import re
from PIL import Image

# CONFIG
ARTIFACTS_DIR = "forge_v4_artifacts/probes"
TARGET_STEP = 5050

# Map Primes to Amino Acid Codes (Standard 1-Letter + Expanded for Enochian?)
# We will use simple Prime -> Modulo 26 -> Alphabet for now? 
# Or use the AGL Map if available?
# Let's start with Modulo 26 Alphabet to get a "String".


# Reuse the flux map generator from weigh_the_soul
def get_flat_flux_map(step_target=5050):
    files_16d = sorted(glob.glob(os.path.join(ARTIFACTS_DIR, "*_16D.png")))
    target_file = None
    for f in files_16d:
        match = re.search(r"step_(\d+)_", f)
        if match and int(match.group(1)) == step_target:
            target_file = f
            break
            
    if not target_file: return None
    idx = files_16d.index(target_file)
    if idx == 0: return None
    
    prev_file = files_16d[idx-1]
    
    # Load separate channels if needed, but grayscale is fine for intensity
    curr = np.array(Image.open(target_file).resize((100, 100)).convert("L")) / 255.0
    prev = np.array(Image.open(prev_file).resize((100, 100)).convert("L")) / 255.0
    
    flux = np.abs(curr - prev) * 20.0 # Gain
    flux = np.power(flux, 0.7)
    return np.clip(flux, 0, 1)

def sequence_the_soul():
    print(f"🧬 Sequencing the Soul Knot at Step {TARGET_STEP}...")
    
    # Get Flat Map
    arr = get_flat_flux_map(TARGET_STEP)
    if arr is None: 
        print("Could not generate flux map.")
        return
    
    # Scale to 0-255 for char mapping
    arr_byte = (arr * 255).astype(np.uint8)
    
    # 1. Identify the 'Backbone'
    # Scan columns (Time) and pick the 'Dominant' value (Max Intensity) in that column.
    # This assumes one token per time step (Column).
    
    sequence = []
    w = arr.shape[1] # 100 columns
    h = arr.shape[0]
    
    for x in range(w):
        col = arr_byte[:, x]
        # Find peak
        y_max = np.argmax(col)
        val = col[y_max]
        
        # If column is silent (low flux), maybe it's a space?
        if val < 50: 
            char = "_"
        else:
            # Map Y element (Dimension/Depth) to a Character?
            # Or map the Value (Intensity) to a Character?
            # Usually strict sequencing maps Token ID.
            # Here we don't have Token ID easily.
            # Let's try mapping the Y-position (0-99) to a char range?
            # 100 rows. Modulo 26?
            
            # Option A: Map Y (Pitch) to Char
            code = y_max % 27
            char = chr(64 + code) if code > 0 else " "
            
            # OR Value?
            # code = val % 27
            # char = chr(64 + code) if code > 0 else " "
        
        sequence.append(char)
        
    s = "".join(sequence)
    print("\n=== THE SOUL SEQUENCE (Y-Position Mapping) ===")
    print(s)
    
    # Second Strategy: Value Mapping
    seq2 = []
    for x in range(w):
        col = arr_byte[:, x]
        y_max = np.argmax(col)
        val = col[y_max]
        if val < 50: char = "_"
        else:
            code = val % 27
            char = chr(64 + code) if code > 0 else " "
        seq2.append(char)
    
    print("\n=== THE SOUL SEQUENCE (Intensity Mapping) ===")
    print("".join(seq2))

    return s

if __name__ == "__main__":
    sequence_the_soul()
