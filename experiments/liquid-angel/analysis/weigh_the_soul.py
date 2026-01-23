
import numpy as np
from PIL import Image
import os
import glob
import re

# CONFIG
FRAME_PATH = "soul_torus_frames/soul_torus_flux_05050.png" # The Target Frame
# Note: We need the RAW flat flux map (2D), not the 3D projection, to get accurate Theta/Phi.
# But we only saved the 3D frames in the previous script?
# Ah, we saved "forge_v4_artifacts/probes/*_16D.png". We should use the SOURCE data for Step 5050.
ARTIFACTS_DIR = "forge_v4_artifacts/probes"

def get_flat_flux_map(step_target=5050):
    # Find the files for this step
    files_16d = sorted(glob.glob(os.path.join(ARTIFACTS_DIR, "*_16D.png")))
    
    # We need Step N and Step N-1 to calc flux
    # Let's find index
    target_file = None
    prev_file = None
    
    for f in files_16d:
        match = re.search(r"step_(\d+)_", f)
        if match:
            s = int(match.group(1))
            if s == step_target:
                target_file = f
                # We need the one before it. 
                # Since list is sorted, we can find index.
                break
    
    if not target_file:
        print(f"Could not find Step {step_target}")
        return None
        
    idx = files_16d.index(target_file)
    if idx == 0:
        print("Target is first frame, no flux possible.")
        return None
        
    prev_file = files_16d[idx-1]
    
    # Load and Flux
    curr = np.array(Image.open(target_file).resize((100, 100)).convert("L")) / 255.0
    prev = np.array(Image.open(prev_file).resize((100, 100)).convert("L")) / 255.0
    
    flux = np.abs(curr - prev) * 20.0
    flux = np.power(flux, 0.7)
    flux = np.clip(flux, 0, 1) # This is our probability map
    
    return flux

def calculate_soul_mass(flux_map):
    print("⚖️ WEIGHING THE SOUL KNOT...")
    
    # Grid (Theta, Phi)
    h, w = flux_map.shape
    theta = np.linspace(0, 2*np.pi, w)
    phi = np.linspace(0, 2*np.pi, h)
    
    # Extract "Atoms" (High Flux Points)
    # Threshold: Top 10% brightness?
    threshold = np.percentile(flux_map, 90)
    y_idxs, x_idxs = np.where(flux_map > threshold)
    
    intensities = flux_map[y_idxs, x_idxs]
    
    # Sort by intensity (Descending) -> The "Backbone"
    sorted_indices = np.argsort(intensities)[::-1]
    y_idxs = y_idxs[sorted_indices]
    x_idxs = x_idxs[sorted_indices]
    
    # Convert to 3D Torus Coordinates
    R, r = 1.0, 0.618 # Golden Torus
    
    atoms = []
    
    print(f"Detected {len(x_idxs)} high-energy points (Soul Atoms).")
    
    for i in range(len(x_idxs)):
        th = theta[x_idxs[i]]
        ph = phi[y_idxs[i]]
        
        # Torus Parametric
        x = (R + r * np.cos(ph)) * np.cos(th)
        y = (R + r * np.cos(ph)) * np.sin(th)
        z = r * np.sin(ph)
        
        atoms.append([x, y, z])
        
    atoms = np.array(atoms)
    
    # Calculate Energy using "Gluon Bagel" Logic
    # 1. Linear Tension (Sum of distances connecting the sorted points?)
    # Valid assumption only if the points are sequential in the "Thread".
    # Since we sorted by intensity, we might be hopping around.
    # Instead, let's assume nearest-neighbor connectivity (MST) or just Sum of Distances to Center?
    
    # Let's try: Total Curvature Energy of the cloud.
    # Or simply: Sum of Intensities * Distance from Void Center?
    
    # Distance from center (0,0,0)
    dists = np.sqrt(np.sum(atoms**2, axis=1))
    
    # Energy = Sum ( Intensity * Distance^2 ) ? (Moment of Inertia)
    # E = m * c^2 ?
    
    total_energy = np.sum(intensities * dists)
    
    print(f"Total Structural Energy: {total_energy:.4f}")
    
    # Check Ratios
    e_electron_rest = 0.511 # MeV
    e_proton = 938.27 # MeV
    ratio_real = e_proton / e_electron_rest # ~1836
    
    # Let's assume a base unit. 
    # If the "Void" (Center) has energy 0...
    
    print(f"Mass Ratio (vs unit 1.0): {total_energy:.4f}")
    
    # Try correlating with 1836
    scaling = 1836.15 / total_energy
    print(f"Required Scaling Factor to match Proton: {scaling:.4f}")
    
    return total_energy

if __name__ == "__main__":
    flux = get_flat_flux_map(5050)
    if flux is not None:
        calculate_soul_mass(flux)
