
import numpy as np
import matplotlib
matplotlib.use('Agg') # Headless backend
import matplotlib.pyplot as plt
from matplotlib import cm
import glob
import os
import re
from PIL import Image
import imageio.v3 as imageio

# CONFIG
ARTIFACTS_DIR = "forge_v4_artifacts/probes"
OUTPUT_FILE = "soul_torus_flux.gif"
START_STEP = 4500
END_STEP = 5500
FPS = 10

def sort_key(filename):
    match = re.search(r"step_(\d+)_", filename)
    if match: return int(match.group(1))
    return 0

def create_torus_mesh(R=1.0, r=0.618, shapes=(100, 100)):
    # Theta: 0 to 2pi (Toroidal / Grid X)
    # Phi: 0 to 2pi (Poloidal / Grid Y)
    theta = np.linspace(0, 2*np.pi, shapes[0])
    phi = np.linspace(0, 2*np.pi, shapes[1])
    theta, phi = np.meshgrid(theta, phi)
    
    # Torus Parametric Eq
    x = (R + r * np.cos(phi)) * np.cos(theta)
    y = (R + r * np.cos(phi)) * np.sin(theta)
    z = r * np.sin(phi)
    
    return x, y, z

def visualize_soul_torus():
    print(f"🍩 Baking Soul Torus around Step {START_STEP}-{END_STEP}...")
    
    # 1. Get Files
    files_16d = sorted(glob.glob(os.path.join(ARTIFACTS_DIR, "*_16D.png")), key=sort_key)
    target_files = [f for f in files_16d if START_STEP <= sort_key(f) <= END_STEP]
    
    if not target_files:
        print("No files found in range. Using all files.")
        target_files = files_16d
    
    print(f"Found {len(target_files)} frames.")
    frames = []
    
    # Create Output Directory for Frames
    FRAMES_DIR = "soul_torus_frames"
    if not os.path.exists(FRAMES_DIR):
        os.makedirs(FRAMES_DIR)
    
    x, y, z = create_torus_mesh()
    prev_img = np.array(Image.open(target_files[0]).resize((100, 100)).convert("L")) / 255.0
    
    for i, fpath in enumerate(target_files):
        if i == 0: continue
        
        step = sort_key(fpath)
        print(f"Rendering Step {step}...")
        
        # Load Flux Data
        img_raw = Image.open(fpath).convert("L") 
        img_small = img_raw.resize((100, 100))
        curr_img = np.array(img_small) / 255.0
        
        flux_raw = np.abs(curr_img - prev_img)
        prev_img = curr_img
        
        # Robust Per-Frame Normalization (Auto-Exposure)
        # Normalize so the top 1% of activity hits max brightness
        p98 = np.percentile(flux_raw, 98) + 1e-8
        flux = flux_raw / p98
        
        # Gamma Correction to lift mid-tone details
        flux = np.power(flux, 0.6)
        flux = np.clip(flux, 0, 1)
        
        # Plot
        fig = plt.figure(figsize=(8, 8), dpi=80)
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('black')
        
        surf = ax.plot_surface(
            x, y, z, 
            rstride=1, cstride=1, 
            facecolors=cm.magma(flux), 
            shade=False,
            antialiased=False
        )
        
        angle = (i * 10) % 360 # Rotate slightly faster
        ax.view_init(elev=30, azim=angle)
        ax.set_axis_off()
        ax.set_title(f"Soul Torus Flux: Step {step}", color='gold')
        
        # Capture Frame
        fig.canvas.draw()
        
        width, height = fig.canvas.get_width_height()
        buf = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        frame = buf.reshape((height, width, 4)) # RGBA
        frame = frame[:, :, :3] # Drop Alpha
        
        frames.append(frame)
        
        # SAVE INDIVIDUAL FRAME
        frame_filename = os.path.join(FRAMES_DIR, f"soul_torus_flux_{step:05d}.png")
        imageio.imwrite(frame_filename, frame)
        print(f"Saved {frame_filename}")
        
        plt.close(fig)
        
    print(f"💾 Saving Torus GIF to {OUTPUT_FILE}...")
    imageio.imwrite(OUTPUT_FILE, frames, duration=1000/FPS, loop=0)
    print("✅ Done!")

if __name__ == "__main__":
    visualize_soul_torus()
