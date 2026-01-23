import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from liquid_angel import LiquidAngel, angelic_tokenize
import math
import sys

# ============================================================================
# TRAIN ANGEL v3.0: THE SERAPHIM PROTOCOL
# ============================================================================

# ----------------------------------------------------------------------------
# 0. HARDWARE SETUP
# ----------------------------------------------------------------------------
sys.path.append("/home/luna/Code/ada/ada-slm")

try:
    from consciousness_engineering.infrastructure.hardware.base import setup_hardware
    hw = setup_hardware()
    DEVICE = torch.device(hw.get_device())
    print(f"Hardware Manager Active. Device: {DEVICE}")
except ImportError as e:
    print(f"HardwareManager not found: {e}. Falling back to CPU.")
    DEVICE = torch.device("cpu")

# ----------------------------------------------------------------------------
# 1. CONFIGURATION (The Seraphim Config)
# ----------------------------------------------------------------------------
CONFIG = {
    "vocab_size": 4093,   # Prime 4093
    "dim": 769,           # Prime 769
    "depth": 17,          # Prime 17
    "heads": 13,          # Prime 13
    "batch_size": 17,     # Prime 17
    "lr": 2e-4,           
    "epochs": 13,         # Prime 13
    "phi": 1.61803398875
}

# ----------------------------------------------------------------------------
# 2. DATASET
# ----------------------------------------------------------------------------
class AngelicDataset(Dataset):
    def __init__(self, filepath, seq_len=64):
        self.seq_len = seq_len
        try:
            with open(filepath, 'r') as f:
                raw_lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: {filepath} not found. Did you run angel_forge.py?")
            raw_lines = []
        
        self.data = []
        for line in raw_lines:
            tokens = angelic_tokenize(line)
            if len(tokens) == 0: continue
            
            if len(tokens) <= seq_len:
                padding = [0] * (seq_len + 1 - len(tokens))
                chunk = tokens + padding
                self.data.append(torch.tensor(chunk, dtype=torch.long))
            else:
                for i in range(0, len(tokens) - seq_len, seq_len // 2):
                    chunk = tokens[i:i+seq_len + 1]
                    if len(chunk) < seq_len + 1:
                        padding = [0] * (seq_len + 1 - len(chunk))
                        chunk = chunk + padding
                    self.data.append(torch.tensor(chunk, dtype=torch.long))

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        seq = self.data[idx]
        return seq[:-1], seq[1:]

# ----------------------------------------------------------------------------
# 3. SPECTRAL LOSS (The Soul & Hologram Constraint)
# ----------------------------------------------------------------------------
def soul_loss(soul_vector):
    norm = torch.norm(soul_vector, dim=-1)
    norm_penalty = torch.mean((norm - 1.0) ** 2)
    return norm_penalty * CONFIG["phi"]

def hologram_loss(hologram):
    # Ensure the hologram doesn't explode in energy
    # It's complex, so we check magnitude
    energy = (hologram.real**2 + hologram.imag**2).mean()
    # We want non-zero energy but bounded
    return torch.abs(energy - 1.0) * 0.01

# ----------------------------------------------------------------------------
# 4. TRAINING LOOP
# ----------------------------------------------------------------------------
def train():
    # Clear previous checkpoints to ensure fresh start
    os.system("rm angel_checkpoint_e*.pt 2>/dev/null")

    # Load Data (SERAPHIM CORPUS v3.0)
    dataset = AngelicDataset("data/corpus_seraphim.txt", seq_len=64)
    if len(dataset) == 0:
        print("Dataset empty. Aborting.")
        return

    loader = DataLoader(dataset, batch_size=CONFIG["batch_size"], shuffle=True)
    print(f"Dataset Size: {len(dataset)} chunks")
    
    # Initialize Model (v3.0 Architecture)
    model = LiquidAngel(
        vocab_size=CONFIG["vocab_size"],
        dim=CONFIG["dim"],
        depth=CONFIG["depth"],
        heads=CONFIG["heads"]
    ).to(DEVICE)
    
    print("✨ Initialized Liquid Angel v3.0 (The Seraphim)")
    
    optimizer = optim.AdamW(model.parameters(), lr=CONFIG["lr"])
    criterion = nn.CrossEntropyLoss()
    
    print("Starting Golden Anneal...")
    
    model.train()
    for epoch in range(CONFIG["epochs"]):
        total_loss = 0
        
        for batch_idx, (x, y) in enumerate(loader):
            x, y = x.to(DEVICE), y.to(DEVICE)
            
            optimizer.zero_grad()
            
            # Forward Pass: Returns (Logits, Soul, Hologram)
            logits, final_soul, hologram = model(x)
            
            # Prediction Loss
            pred_loss = criterion(logits.view(-1, CONFIG["vocab_size"]), y.view(-1))
            
            # Auxiliary Losses
            s_loss = soul_loss(final_soul)
            h_loss = hologram_loss(hologram)
            
            # Total Loss
            loss = pred_loss + 0.1 * s_loss + 0.1 * h_loss
            
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            if batch_idx % 50 == 0:
                print(f"Epoch {epoch} | Batch {batch_idx} | Loss: {loss.item():.4f} (Soul: {s_loss.item():.4f}, Holo: {h_loss.item():.4f})", flush=True)
        
        # Golden Decay Schedule (5th Root of Phi)
        decay_factor = CONFIG["phi"] ** (1/5)
        for param_group in optimizer.param_groups:
            param_group['lr'] /= decay_factor
            
        print(f"=== Epoch {epoch} Complete | Avg Loss: {total_loss / len(loader):.4f} | LR: {optimizer.param_groups[0]['lr']:.6f} ===", flush=True)
        
        torch.save(model.state_dict(), f"angel_checkpoint_e{epoch}.pt")

if __name__ == "__main__":
    train()
