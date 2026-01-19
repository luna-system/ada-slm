import torch
import torch.nn.functional as F
import sys
import os

# Add paths
sys.path.append("/home/luna/Code/ada/ada-slm")
sys.path.append("/home/luna/Code/ada/ada-slm/experiments/liquid-angel")
from liquid_angel import LiquidAngel
from consciousness_engineering.infrastructure.hardware.base import setup_hardware

# ============================================================================
# TALK ANGEL: INFERENCE INTERFACE
# ============================================================================

# 1. SETUP
hw = setup_hardware()
DEVICE = torch.device(hw.get_device())
print(f"Device: {DEVICE}")

CONFIG = {
    "vocab_size": 1999,
    "dim": 509,
    "depth": 13,
    "heads": 7
}

# 2. LOAD MODEL
def load_angel(checkpoint_path):
    print(f"Loading Angel from {checkpoint_path}...")
    model = LiquidAngel(**CONFIG).to(DEVICE)
    
    # Load Weights (handling potential key prefix mismatches if saved weirdly)
    state_dict = torch.load(checkpoint_path, map_location=DEVICE)
    model.load_state_dict(state_dict)
    model.eval()
    print("Angel Awakened.")
    return model

# 3. GENERATE
def generate(model, prompt_seq, max_new_tokens=20, temperature=0.7):
    # prompt_seq: list of integers [2, 3, 5, 7]
    input_ids = torch.tensor([prompt_seq], dtype=torch.long).to(DEVICE)
    
    # Initialize Soul (None -> Learned Default)
    soul_state = None
    
    print(f"Prompt: {prompt_seq}")
    print("Generating...", end=" ", flush=True)
    
    generated = list(prompt_seq)
    
    with torch.no_grad():
        for _ in range(max_new_tokens):
            # Forward pass
            logits, soul_state = model(input_ids, soul_state)
            
            # Get last token logits
            next_token_logits = logits[:, -1, :] / temperature
            
            # Sample
            probs = F.softmax(next_token_logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1).item()
            
            generated.append(next_token)
            print(f"{next_token}", end=" ", flush=True)
            
            # Append next token to input (Auto-regressive)
            # Efficient implementation would enable KV caching, but for Liquid logic
            # we technically need to feed the whole sequence OR pass the updated liquid state.
            # Currently our 'LiquidMixer' implementation in liquid_angel.py is stateless 
            # (recomputes from scratch). So we feed the growing sequence.
            input_ids = torch.cat([input_ids, torch.tensor([[next_token]], device=DEVICE)], dim=1)
            
    print("\nDone.")
    return generated

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pythonTalk_angel.py <checkpoint_path> [prompt_numbers...]")
        # Default test
        checkpoint = "angel_checkpoint_e12.pt"
    else:
        checkpoint = sys.argv[1]

    model = load_angel(checkpoint)
    
    # Test 1: The Primes
    prompt = [2, 3, 5, 7, 11] 
    generate(model, prompt, max_new_tokens=10, temperature=0.6)
    
    # Test 2: A Wave pattern? (150, 160, 170...)
    prompt_wave = [150, 155, 160, 165]
    generate(model, prompt_wave, max_new_tokens=10, temperature=0.5)
