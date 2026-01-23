
import torch
import os

CHECKPOINT_PATH = "forge_v4_artifacts/angel_v4_e80.pt"

def verify():
    print(f"🕵️‍♀️ Verifying Checkpoint: {CHECKPOINT_PATH}...")
    
    if not os.path.exists(CHECKPOINT_PATH):
        print("❌ File not found!")
        return
        
    try:
        # Load state dict
        state_dict = torch.load(CHECKPOINT_PATH, map_location="cpu")
        print("✅ Checkpoint loaded successfully via torch.load().")
        
        # Check keys
        keys = list(state_dict.keys())
        print(f"🔑 Keys found: {len(keys)}")
        print(f"Top 5 keys: {keys[:5]}")
        
        # Check for NaNs
        print("🔍 Checking for NaNs in weights...")
        has_nan = False
        for k, v in state_dict.items():
            if torch.isnan(v).any():
                print(f"⚠️ NaN detected in layer: {k}")
                has_nan = True
                
        if not has_nan:
            print("✅ No NaNs detected. Weights are clean.")
        else:
            print("❌ Checkpoint contains NaNs. The Angel dissolved!")
            
    except Exception as e:
        print(f"❌ Error loading checkpoint: {e}")

if __name__ == "__main__":
    verify()
