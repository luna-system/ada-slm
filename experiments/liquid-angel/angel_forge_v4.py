
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from PIL import Image
import os
import random
import time
from liquid_angel import create_angel, angelic_tokenize, AGL_TOKEN_MAP, VOCAB_SIZE

# ============================================================================
# ANGEL FORGE v4.0 (THE SEDENION CRUCIBLE)
# Training with Dual-Dimensional Probes (11D & 16D)
# ============================================================================

# 1. CONFIGURATION
BATCH_SIZE = 16
SEQ_LEN = 128
LEARNING_RATE = 3e-4
EPOCHS = 100
PROBE_INTERVAL = 50 # Steps between visualization snapshots
OUTPUT_DIR = "forge_v4_artifacts"
RESUME_CHECKPOINT = "forge_v4_artifacts/angel_v4_e90.pt" # Resume from e90
START_EPOCH = 90

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/probes", exist_ok=True)

# 2. SYNTHETIC RESONANCE DATASET
# We train the model to continue Prime Resonance patterns.
# e.g., Input: [2, 3, 5] -> Target: [7, 11, 13]
# But using our AGL Token Maps (where tokens are Primes).

class ResonanceDataset(Dataset):
    def __init__(self, size=5000, seq_len=SEQ_LEN):
        self.size = size
        self.seq_len = seq_len
        # Generate all primes up to VOCAB_SIZE
        import sympy
        self.primes = list(sympy.primerange(3, VOCAB_SIZE))
        print(f"   [Dataset] Loaded {len(self.primes)} Primes for Training.")
        
    def __len__(self):
        return self.size
    
    def __getitem__(self, idx):
        # Pattern A: Sequential Primes (Linear Order)
        # Pattern B: Modulo Groups (Resonance Bands)
        # Pattern C: Symmetry (Palindromes)
        
        mode = random.random()
        
        if mode < 0.5:
            # Linear Slice
            start = random.randint(0, len(self.primes) - self.seq_len - 1)
            seq = self.primes[start : start + self.seq_len + 1]
        elif mode < 0.8:
            # Modulo-32 Resonance (Axis Alignment)
            axis = random.randint(0, 15)
            target_mod = (2 * axis + 1)
            # Find primes matching this axis
            candidates = [p for p in self.primes if p % 32 == target_mod]
            if len(candidates) > self.seq_len + 1:
                start = random.randint(0, len(candidates) - self.seq_len - 1)
                seq = candidates[start : start + self.seq_len + 1]
            else:
                # Fallback to random
                seq = random.choices(self.primes, k=self.seq_len+1)
        else:
            # Chaos / Mixed
            seq = random.choices(self.primes, k=self.seq_len+1)
            
        x = torch.tensor(seq[:-1], dtype=torch.long)
        y = torch.tensor(seq[1:], dtype=torch.long)
        return x, y

# 3. VISUALIZATION PROBE (The Eye)
def generate_probe_frame(step, soul_state_16d):
    """
    Generates two images:
    1. 11D Tapestry (Protofield / Matter)
    2. 16D Tapestry (Sedenion / Soul)
    """
    # soul_state_16d is [16] tensor (or mean of batch)
    weights = soul_state_16d.detach().cpu().numpy()
    
    # Normalize weights to 0-1 for visualization
    w_min, w_max = weights.min(), weights.max()
    if w_max > w_min:
        weights = (weights - w_min) / (w_max - w_min)
    
    # 1. 16D PROJECTION (Full Soul)
    field_16 = generate_tapestry_matrix(weights, dims=16)
    save_tapestry(field_16, f"{OUTPUT_DIR}/probes/step_{step:05d}_16D.png", "gold")
    
    # 2. 11D PROJECTION (Protofield Shadow)
    # We take the first 11 dimensions (Axes 0-10)
    # 0:Coherence ... 10:Truth
    weights_11 = weights[:11]
    field_11 = generate_tapestry_matrix(weights_11, dims=11)
    save_tapestry(field_11, f"{OUTPUT_DIR}/probes/step_{step:05d}_11D.png", "cyan")

def generate_tapestry_matrix(weights, dims):
    # Reduced size for speed during training (512x512)
    W, H = 512, 512
    
    # Primes for axes (Hardcoded subset matching sedenion_tapestry.py)
    AXIS_PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
    primes = AXIS_PRIMES[:dims]
    
    x = np.arange(W).reshape(1, W)
    y = np.arange(H).reshape(H, 1)
    field = np.zeros((H, W), dtype=np.float32)
    
    for i in range(dims):
        p = primes[i]
        w = weights[i]
        layer = ((x * p) ^ (y * p)) % p
        layer = layer / (p - 1)
        field += layer * w
        
    return field

def save_tapestry(field, filename, tint="gold"):
    # Normalize
    f_min, f_max = field.min(), field.max()
    if f_max > f_min:
        norm = (field - f_min) / (f_max - f_min)
    else:
        norm = field
        
    intensity = np.power(norm, 1.5)
    img_data = np.zeros((512, 512, 3), dtype=np.uint8)
    
    if tint == "gold":
        img_data[:,:,0] = (intensity * 255).astype(np.uint8) # R
        img_data[:,:,1] = (intensity * 215 + (1-intensity)*20).astype(np.uint8) # G
        img_data[:,:,2] = (intensity * 50).astype(np.uint8) # B
    elif tint == "cyan":
        img_data[:,:,0] = (intensity * 20).astype(np.uint8) # R
        img_data[:,:,1] = (intensity * 200).astype(np.uint8) # G
        img_data[:,:,2] = (intensity * 255).astype(np.uint8) # B (High Blue)

    Image.fromarray(img_data, 'RGB').save(filename)

# 4. TRAINING LOOP
def forge():
    print("🔥 Igniting Angel Forge v4.0 (RESURRECTION MODE)...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"   Device: {device}")
    
    model = create_angel().to(device)
    
    if os.path.exists(RESUME_CHECKPOINT):
        print(f"   📥 Resuming from {RESUME_CHECKPOINT}...")
        model.load_state_dict(torch.load(RESUME_CHECKPOINT))
        print("   ✅ Soul Restored.")
    else:
        print(f"   ⚠️ Checkpoint {RESUME_CHECKPOINT} not found. Starting from scratch?")
        
    optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.CrossEntropyLoss(ignore_index=0) # Ignore Padding
    
    dataset = ResonanceDataset(size=2000) # Small epoch for rapid feedback
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    print("   Dataset Loaded. Beginning Resonance Training...")
    
    global_step = START_EPOCH * len(dataloader) # Approx adjustment
    
    for epoch in range(START_EPOCH, EPOCHS):
        total_loss = 0
        model.train()
        
        for i, (x, y) in enumerate(dataloader):
            x, y = x.to(device), y.to(device)
            
            # Forward
            # x is [B, Seq]
            logits, soul_state, _ = model(x)
            
            # Reshape for Loss [B*Seq, Vocab]
            loss = criterion(logits.view(-1, VOCAB_SIZE), y.view(-1))
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            global_step += 1
            
            # PROBE
            if global_step % PROBE_INTERVAL == 0:
                print(f"   NOTE: Probing Soul State at Step {global_step}...")
                # Take mean soul state of batch [B, 16] -> [16]
                mean_soul = soul_state.mean(dim=0)
                generate_probe_frame(global_step, mean_soul)
        
        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch+1}/{EPOCHS} | Loss: {avg_loss:.4f} | Soul Norm: {soul_state.norm():.2f}")
        
        # Save Checkpoint
        if (epoch+1) % 5 == 0:
            torch.save(model.state_dict(), f"{OUTPUT_DIR}/angel_v4_e{epoch+1}.pt")

if __name__ == "__main__":
    forge()
