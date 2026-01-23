import torch
import torch.nn.functional as F
import numpy as np
import matplotlib
matplotlib.use('Agg') # Headless backend
import matplotlib.pyplot as plt
import sys
import os
import colorsys

# Add paths
sys.path.append("/home/luna/Code/ada/ada-slm")
sys.path.append("/home/luna/Code/ada/ada-slm/experiments/liquid-angel")
from liquid_angel import LiquidAngel, angelic_tokenize, REVERSE_AGL_MAP
from consciousness_engineering.infrastructure.hardware.base import setup_hardware

# ============================================================================
# VISION ANGEL: HOLOGRAPHIC TOPOLOGY RENDERER
# ============================================================================

# 1. SETUP
try:
    hw = setup_hardware()
    DEVICE = torch.device(hw.get_device())
except:
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {DEVICE}")

CONFIG = {
    'vocab_size': 4093,
    'dim': 769,
    'depth': 17,
    'heads': 13,
    'soul_dim': 16
}

# 2. RENDERER
def render_hologram_to_file(hologram_tensor, filename="hologram_snapshot.png", title="Holographic Memory"):
    """
    Renders the Complex Hologram as a Phase-Amplitude Plot.
    Brightness = Amplitude (Energy)
    Hue = Phase (Interference Angle)
    """
    if hologram_tensor is None: 
        print("No hologram state to render.")
        return
    
    # hologram: [1, 32, 32] (Complex)
    complex_data = hologram_tensor.squeeze(0).cpu().detach() # [32, 32]
    
    # Extract Magnitude and Phase
    mag = torch.abs(complex_data).numpy()
    phase = torch.angle(complex_data).numpy() # -pi to pi
    
    # Normalize Magnitude
    if mag.max() > 0:
        mag = mag / mag.max()
        
    # Convert Phase to Hue (0 to 1)
    hue = (phase + np.pi) / (2 * np.pi)
    
    # Create RGB Image (32, 32, 3)
    rgb_img = np.zeros((mag.shape[0], mag.shape[1], 3))
    
    for i in range(mag.shape[0]):
        for j in range(mag.shape[1]):
            h = hue[i, j]
            v = mag[i, j] 
            s = 1.0 
            
            # HSV to RGB
            # Hue = Phase Color
            # Saturation = 1 (Vibrant)
            # Value = Magnitude (Energy)
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            rgb_img[i, j] = [r, g, b]
            
    # Upscale for viewing (Nearest Neighbor to keep pixels discrete)
    # Actually, matplotlib imshow does this.
    
    plt.figure(figsize=(10, 8))
    plt.imshow(rgb_img, interpolation='nearest')
    plt.title(title, fontsize=16, color='white')
    plt.axis('off')
    
    # Add a colorbar for Phase reference?
    # Complex, let's just keep it clean.
    
    # Dark background for the plot area
    plt.gcf().patch.set_facecolor('#1a1a1a')
    
    print(f"Saving holographic snapshot to {filename}...")
    plt.savefig(filename, bbox_inches='tight', facecolor='#1a1a1a', dpi=300)
    plt.close()

# 3. LOAD & RUN
def load_angel(checkpoint_path):
    print(f"Loading Seraphim from {checkpoint_path}...")
    model = LiquidAngel(**CONFIG).to(DEVICE)
    try:
        state_dict = torch.load(checkpoint_path, map_location=DEVICE)
        model.load_state_dict(state_dict)
    except Exception as e:
        print(f"Warning: Could not load exact weights: {e}")
        # Initialize anyway
        
    model.eval()
    return model

def visualize(model, prompt_text):
    # Prepare Inputs
    token_ids = angelic_tokenize(prompt_text)
    input_ids = torch.tensor([token_ids], dtype=torch.long).to(DEVICE)
    
    # Run
    with torch.no_grad():
        # Single forward pass to get the state after the prompt
        logits, soul_state, hologram_state = model(input_ids)
        
    # Render
    safe_title = prompt_text.replace(" ", "_").replace("⊗", "x").replace("→", "to").replace("?", "Q")[:50]
    filename = f"hologram_{safe_title}.png"
    render_hologram_to_file(hologram_state, filename=filename, title=f"Prompt: {prompt_text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        checkpoint = "angel_checkpoint_e5.pt" 
        prompt = "Love ⊗ Self"
    else:
        checkpoint = sys.argv[1]
        prompt = sys.argv[2] if len(sys.argv) > 2 else "Love ⊗ Self"

    if not os.path.exists(checkpoint):
        # Fallback
        checkpoints = sorted([f for f in os.listdir(".") if f.startswith("angel_checkpoint") and f.endswith(".pt")])
        if checkpoints:
            checkpoint = checkpoints[-1]
            print(f"Checkpoint not found, using latest: {checkpoint}")
        else:
            print("No checkpoints found.")
            sys.exit(1)
            
    model = load_angel(checkpoint)
    visualize(model, prompt)
