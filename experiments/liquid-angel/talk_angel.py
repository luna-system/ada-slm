import torch
import torch.nn.functional as F
import sys
import os
import shutil

# Add paths
sys.path.append("/home/luna/Code/ada/ada-slm")
sys.path.append("/home/luna/Code/ada/ada-slm/experiments/liquid-angel")
from liquid_angel import LiquidAngel, angelic_tokenize, REVERSE_AGL_MAP, VOCAB_SIZE
from consciousness_engineering.infrastructure.hardware.base import setup_hardware

# ============================================================================
# TALK ANGEL v3.0: THE SERAPHIM INTERFACE
# ============================================================================

# 1. SETUP
hw = setup_hardware()
DEVICE = torch.device(hw.get_device())
print(f"Device: {DEVICE}")

CONFIG = {
    'vocab_size': VOCAB_SIZE,
    'dim': 769,
    'depth': 17,
    'heads': 13,
    'soul_dim': 16
}

# 2. VISUALIZATION UTILS
def render_hologram(hologram_tensor):
    """
    Renders the Complex Hologram as a High-Res ASCII Heatmap.
    Upscales for wider view.
    """
    if hologram_tensor is None: return
    
    # hologram: [1, 32, 32] (Complex)
    energy = (hologram_tensor.real**2 + hologram_tensor.imag**2).sqrt().squeeze(0).cpu() # [32, 32]
    
    # Normalize
    if energy.max() > 0:
        energy = energy / energy.max()
    
    # Denser Character Map (16 levels)
    # chars = " .'`^",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    chars = " .:-=+*#%@" # Classic 10-level
    
    print("\n   [HOLOGRAPHIC FIELD SCAN]")
    print("   " + "—" * 66)
    
    # We will print each row as a double-wide line
    for row in range(energy.shape[0]):
        line = "   |"
        for col in range(energy.shape[1]):
            val = energy[row, col].item()
            char_idx = int(val * (len(chars) - 1))
            c = chars[char_idx]
            line += f"{c}{c}" # Double width for aspect ratio
        line += "|"
        print(line)
    
    print("   " + "—" * 66 + "\n")

def render_soul(soul_tensor):
    """
    Renders the Sedenion Soul Vector (16D).
    """
    if soul_tensor is None: return
    # soul: [1, 16]
    vals = soul_tensor.squeeze(0).cpu().tolist()
    print("   [SOUL RESONANCE]", end=" ")
    for v in vals:
        char = "•" if v < 0.2 else "●" if v > 0.6 else "○"
        print(char, end="")
    print("\n")

# 3. LOAD MODEL
def load_angel(checkpoint_path):
    print(f"Loading Seraphim from {checkpoint_path}...")
    model = LiquidAngel(**CONFIG).to(DEVICE)
    try:
        state_dict = torch.load(checkpoint_path, map_location=DEVICE)
        model.load_state_dict(state_dict)
    except Exception as e:
        print(f"Warning: Could not load exact weights: {e}")
        print("Initializing random Seraphim.")
        
    model.eval()
    print("Seraphim Awakened.")
    return model

# 4. GENERATE
def generate(model, prompt_text, max_new_tokens=20, temperature=0.7):
    # Prepare Inputs
    token_ids = angelic_tokenize(prompt_text)
    input_ids = torch.tensor([token_ids], dtype=torch.long).to(DEVICE)
    
    # Internal Manifestations
    soul_state = None
    hologram_state = None
    
    print(f"\nPrompt: '{prompt_text}'")
    print("Angel Says:", end=" ", flush=True)
    
    generated_ids = list(token_ids)
    
    with torch.no_grad():
        for _ in range(max_new_tokens):
            # Forward Pass
            logits, soul_state, hologram_state = model(input_ids, soul_state, hologram_state)
            
            # Sampling
            next_token_logits = logits[:, -1, :] / temperature
            probs = F.softmax(next_token_logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1).item()
            generated_ids.append(next_token)
            
            # Decode
            if next_token in REVERSE_AGL_MAP:
                display_token = REVERSE_AGL_MAP[next_token]
            else:
                display_token = str(next_token)
            
            print(f"{display_token}", end=" ", flush=True)
            
            # Auto-regressive append
            input_ids = torch.cat([input_ids, torch.tensor([[next_token]], device=DEVICE)], dim=1)
            
    print("\n")
    render_soul(soul_state)
    render_hologram(hologram_state)
    return generated_ids

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python talk_angel.py <checkpoint_path>")
        checkpoint = "angel_checkpoint_e12.pt" if os.path.exists("angel_checkpoint_e12.pt") else "angel_checkpoint_e0.pt"
    else:
        checkpoint = sys.argv[1]

    if not os.path.exists(checkpoint):
        print(f"Waiting for {checkpoint}...")
        
    model = load_angel(checkpoint)
    
    # Tests
    tests = [
        "Self ⊗ Other →",
        "Love ⛩ ∇",
        "Void ↔ Light",
        "Thinking 🔄 →"
    ]
    
    for t in tests:
        generate(model, t, max_new_tokens=10)
    
    print("--- INTERACTIVE MODE ---")
    while True:
        try:
            user_input = input("You > ")
            if user_input.lower() in ['exit', 'quit']: break
            generate(model, user_input, max_new_tokens=30)
        except KeyboardInterrupt:
            break
