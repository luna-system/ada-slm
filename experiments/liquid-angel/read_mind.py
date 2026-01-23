import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from PIL import Image
import colorsys

# Add paths
sys.path.append("/home/luna/Code/ada/ada-slm")
sys.path.append("/home/luna/Code/ada/ada-slm/experiments/liquid-angel")
from liquid_angel import LiquidAngel, angelic_tokenize, REVERSE_AGL_MAP, AGL_TOKEN_MAP
from consciousness_engineering.infrastructure.hardware.base import setup_hardware

# ============================================================================
# MIND READER ANGEL: INVERSE HOLOGRAPHY
# Decodes a Holographic png back into Concepts
# ============================================================================

# 1. SETUP
CONFIG = {
    'vocab_size': 4093,
    'dim': 769,
    'depth': 17,
    'heads': 13,
    'soul_dim': 16
}

try:
    hw = setup_hardware()
    DEVICE = torch.device(hw.get_device())
except:
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_angel(checkpoint_path):
    print(f"Loading Seraphim (Reference) from {checkpoint_path}...")
    model = LiquidAngel(**CONFIG).to(DEVICE)
    try:
        state_dict = torch.load(checkpoint_path, map_location=DEVICE)
        model.load_state_dict(state_dict)
    except:
        print("Using random reference (Warning: Decoding will fail if not matched)")
    model.eval()
    return model

def complex_from_image(image_path):
    """
    Reconstructs the 32x32 Complex Tensor from the PNG.
    We assume Hue = Phase, Value = Magnitude.
    """
    # Load Image with PIL
    try:
        img = Image.open(image_path).convert('RGB')
        img = img.resize((32, 32), Image.NEAREST)
        arr = np.array(img).astype(float) / 255.0 # [32, 32, 3] RGB
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

    # Convert RGB to HSV manually or via matplotlib colors
    # Faster: vectorized RGB to HSV
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    
    # We need to invert the colorsys conversion. 
    # Or just iterate since 32x32 is tiny.
    h = np.zeros((32, 32))
    v = np.zeros((32, 32))
    
    for i in range(32):
        for j in range(32):
            h_val, s_val, v_val = colorsys.rgb_to_hsv(r[i,j], g[i,j], b[i,j])
            h[i,j] = h_val
            v[i,j] = v_val

    # Reconstruct Phase and Mag
    # Hue 0-1 -> Phase -pi to pi
    phase = (h * 2 * np.pi) - np.pi
    mag = v # Normalized magnitude
    
    # Construct Complex
    real = mag * np.cos(phase)
    imag = mag * np.sin(phase)
    
    tensor = torch.complex(torch.tensor(real), torch.tensor(imag)).to(torch.complex64).to(DEVICE)
    return tensor.unsqueeze(0) # [1, 32, 32]

def decode_thought(model, hologram):
    """
    Uses the model's HolographicLayer inverse logic to decode the thought.
    """
    # 1. READ (Reconstruct the State Vector [Batch, Dim])
    # x_rec = Integral(H * conjugate(basis))
    
    # We need access to the model's HolographicLayer buffers (kx, ky)
    holo_layer = model.hologram
    
    reconstructed, _ = holo_layer(
        # We pass dummy input to get output? 
        # No, the forward pass writes then reads.
        # But we want to JUST read from a provided hologram.
        # The 'read' logic is embedded in forward().
        # Let's manually invoke the READ step logic using the layer's buffers.
        torch.zeros(1, 769).to(DEVICE), # Dummy x
        hologram # The image hologram
    )
    
    # reconstructed is [1, 769] (The latent vector)
    
    # 2. PROJECTION (Latent -> Vocab)
    # This is tricky. The Latent Vector describes the *Concept*.
    # Ideally, we project this to Logits to see which tokens match best.
    
    logits = model.to_logits(reconstructed)
    probs = F.softmax(logits, dim=-1)
    
    # Get Top 10 Concepts
    vals, indices = torch.topk(probs, 10)
    
    print("\nDecoding Neural Pattern...")
    print("-" * 30)
    for i in range(10):
        idx = indices[0][i].item()
        prob = vals[0][i].item()
        token = REVERSE_AGL_MAP.get(idx, str(idx))
        print(f"{token}: {prob:.4f}")
    print("-" * 30)

def fidelity_test(model, prompt_text):
    """
    Generates a hologram from text and attempts to Read it back.
    """
    print(f"\nEncoding Thought: '{prompt_text}'")
    
    # 1. ENCODE
    token_ids = angelic_tokenize(prompt_text)
    input_ids = torch.tensor([token_ids], dtype=torch.long).to(DEVICE)
    
    with torch.no_grad():
        # Run forward pass to get the Hologram State
        # Note: model() returns logits, soul, hologram
        _, _, hologram = model(input_ids)
        
    print(f"Hologram Energy: {torch.sum(torch.abs(hologram)).item():.4f}")
    
    # 2. DECODE (INVERSION)
    decode_thought(model, hologram)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        checkpoint = "angel_checkpoint_e6.pt" # Default
        prompt = "Love ⊗ Self"
    else:
        checkpoint = sys.argv[1]
        prompt = sys.argv[2] if len(sys.argv) > 2 else "Love ⊗ Self"
            
    model = load_angel(checkpoint)
    fidelity_test(model, prompt)
