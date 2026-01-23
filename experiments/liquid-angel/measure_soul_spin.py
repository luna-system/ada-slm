

import numpy as np
import glob
import os
import re
from PIL import Image

# CONFIG
ARTIFACTS_DIR = "forge_v4_artifacts/probes"
START_STEP = 4500
END_STEP = 5500

def sort_key(filename):
    match = re.search(r"step_(\d+)_", filename)
    if match: return int(match.group(1))
    return 0

def phase_correlation(a, b):
    # Windowing (Hanning) to reduce edge effects? Maybe overkill.
    G_a = np.fft.fft2(a)
    G_b = np.fft.fft2(b)
    
    conj_b = np.conjugate(G_b)
    R = G_a * conj_b
    R /= np.absolute(R) # Normalize magnitude -> Phase only
    
    r = np.fft.ifft2(R).real
    
    # Find peak
    y, x = np.unravel_index(np.argmax(r), r.shape)
    
    # Handle wrapping (negative shifts)
    h, w = r.shape
    if y > h // 2: y -= h
    if x > w // 2: x -= w
    
    # Return displacement (dy, dx) -> (v, u)
    # Note: If image A shifted to B, we want B - A.
    # Cross Corr peak gives shift to align B to A?
    # Let's say v = -y, u = -x
    return -x, -y

def measure_spin():
    print(f"🧭 Measuring Soul Spin (FFT Phase Correlation) for Steps {START_STEP}-{END_STEP}...")
    
    files = sorted(glob.glob(os.path.join(ARTIFACTS_DIR, "*_16D.png")), key=sort_key)
    target_files = [f for f in files if START_STEP <= sort_key(f) <= END_STEP]
    
    if len(target_files) < 2:
        print("Not enough frames.")
        return

    prev_img = np.array(Image.open(target_files[0]).convert("L"))
    
    total_u = 0.0
    total_v = 0.0
    count = 0
    
    print(f"Analyzing flow across {len(target_files)} frames...")
    
    for i in range(1, len(target_files)):
        curr_img = np.array(Image.open(target_files[i]).convert("L"))
        
        # Calculate Phase Correlation Shift
        dx, dy = phase_correlation(prev_img, curr_img)
        
        # Accumulated Shift (Velocity)
        total_u += dx
        total_v += dy
        count += 1
        
        prev_img = curr_img
        
        # Debug instantaneous ratio
        if i % 5 == 0:
            inst_ratio = abs(dy/dx) if dx != 0 else 0
            # print(f"Frame {i}: dx={dx}, dy={dy}, Ratio={inst_ratio:.2f}")

    avg_u = total_u / count
    avg_v = total_v / count

    # Determine Angle
    avg_deg = np.degrees(np.arctan2(avg_v, avg_u))
    
    print("\n=== SOUL SPIN ANALYSIS (FFT) ===")
    print(f"Avg Velocity Vector: (u={avg_u:.4f}, v={avg_v:.4f})")
    
    # Analyze Ratio
    ratio = abs(avg_v / avg_u) if abs(avg_u) > 1e-9 else 999.0
    print(f"Flow Ratio (v/u):    {ratio:.4f}")
    
    # Check for Golden Ratio (phi) or Inverse Phi
    phi = 1.61803398875
    inv_phi = 1/phi # 0.618
    
    diff_phi = abs(ratio - phi)
    diff_inv = abs(ratio - inv_phi)
    
    print(f"Difference from PHI (1.618): {diff_phi:.4f}")
    print(f"Difference from 1/PHI (0.618): {diff_inv:.4f}")
    
    if diff_phi < 0.2:
        print("✨ GOLDEN RATIO DETECTED in Spin Dynamics! (Alignment with Phi) ✨")
    elif diff_inv < 0.2:
        print("✨ GOLDEN RATIO DETECTED (Inverse Phi) ✨")
    elif abs(ratio - 1.0) < 0.2:
        print("⭕ UNIT RATIO (1:1 Ring) Detected.")
    else:
        print(f"🌀 Complex Winding Ratio: {ratio:.4f}")

if __name__ == "__main__":
    measure_spin()
