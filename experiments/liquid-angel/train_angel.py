import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from liquid_angel import LiquidAngel
import math

# ============================================================================
# TRAIN ANGEL: GOLDEN ANNEALING PROTOCOL
# ============================================================================

# ----------------------------------------------------------------------------
# 0. HARDWARE SETUP (Via HardwareManager)
# ----------------------------------------------------------------------------
import sys
import os

# Add ada-slm to path to find consciousness_engineering
sys.path.append("/home/luna/Code/ada/ada-slm")

try:
    from consciousness_engineering.infrastructure.hardware.base import setup_hardware
    # Setup hardware (ROCm aware)
    hw = setup_hardware()
    DEVICE = torch.device(hw.get_device())
    print(f"Hardware Manager Active. Device: {DEVICE}")
except ImportError as e:
    print(f"HardwareManager not found: {e}. Falling back to CPU.")
    DEVICE = torch.device("cpu")

# ----------------------------------------------------------------------------
# 1. CONFIGURATION (The Angelic Config)
# ----------------------------------------------------------------------------
CONFIG = {
    "vocab_size": 1999,   # Prime
    "dim": 509,           # Prime
    "depth": 13,          # Prime
    "heads": 7,           # Prime (must divide dim? No, prime dims usually imply unique projection)
                          # NOTE: head_dim = 509 // 7 = 72.7 (Not clean).
                          # Correction: We project qkv to (heads * head_dim).
                          # Let's let the linear layer handle the sizing.
    "batch_size": 19,     # Prime
    "lr": 3e-4,           # Standard-ish
    "epochs": 13,         # Prime
    "phi": 1.61803398875
}

# ----------------------------------------------------------------------------
# 2. DATASET
# ----------------------------------------------------------------------------
class AngelicDataset(Dataset):
    def __init__(self, filepath, seq_len=128):
        self.seq_len = seq_len
        with open(filepath, 'r') as f:
            raw_lines = f.readlines()
        
        # Tokenize (Simple splitting for now due to synthetic nature)
        self.data = []
        for line in raw_lines:
            tokens = [int(t) for t in line.strip().split() if t.isdigit()]
            if len(tokens) > 1:
                # Chunking
                for i in range(0, len(tokens) - seq_len, seq_len):
                    chunk = tokens[i:i+seq_len]
                    if len(chunk) == seq_len:
                        self.data.append(torch.tensor(chunk, dtype=torch.long))
                        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        # x = input, y = target (next token)
        seq = self.data[idx]
        return seq[:-1], seq[1:]

# ----------------------------------------------------------------------------
# 3. SPECTRAL LOSS (The Soul Constraint)
# ----------------------------------------------------------------------------
def soul_loss(soul_vector):
    """
    Enforces that the eigenvalues of the soul covariance 
    approximate the Golden Ratio structure.
    """
    # Simply punishing variance collapse for now (ensure it's not zero)
    # And ensuring norm is stable (unit sphere)
    norm = torch.norm(soul_vector, dim=-1)
    norm_penalty = torch.mean((norm - 1.0) ** 2)
    return norm_penalty * CONFIG["phi"]

# ----------------------------------------------------------------------------
# 4. TRAINING LOOP
# ----------------------------------------------------------------------------
def train():
    # Load Data
    dataset = AngelicDataset("data/corpus_angelic.txt", seq_len=64)
    loader = DataLoader(dataset, batch_size=CONFIG["batch_size"], shuffle=True)
    print(f"Dataset Size: {len(dataset)} chunks")
    
    # Initialize Model
    model = LiquidAngel(
        vocab_size=CONFIG["vocab_size"],
        dim=CONFIG["dim"],
        depth=CONFIG["depth"],
        heads=CONFIG["heads"]
    ).to(DEVICE)
    
    optimizer = optim.AdamW(model.parameters(), lr=CONFIG["lr"])
    criterion = nn.CrossEntropyLoss()
    
    print("Starting Golden Anneal...")
    
    model.train()
    for epoch in range(CONFIG["epochs"]):
        total_loss = 0
        
        for batch_idx, (x, y) in enumerate(loader):
            x, y = x.to(DEVICE), y.to(DEVICE)
            
            optimizer.zero_grad()
            
            # Forward Pass (with Soul State)
            # We initialize Soul to None (Learnable default)
            logits, final_soul = model(x)
            
            # Prediction Loss
            # Flatten for CE: [B*N, V]
            pred_loss = criterion(logits.view(-1, CONFIG["vocab_size"]), y.view(-1))
            
            # Soul Loss (Spectral regularization)
            s_loss = soul_loss(final_soul)
            
            # Total Loss
            loss = pred_loss + 0.1 * s_loss
            
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            if batch_idx % 50 == 0:
                print(f"Epoch {epoch} | Batch {batch_idx} | Loss: {loss.item():.4f} (Soul: {s_loss.item():.4f})", flush=True)
        
        # Golden Decay Schedule
        # Reduce LR by Phi factor every epoch
        for param_group in optimizer.param_groups:
            param_group['lr'] /= 1.1 # Gentle decay (Phi is too aggressive per epoch)
            
        print(f"=== Epoch {epoch} Complete | Avg Loss: {total_loss / len(loader):.4f} ===", flush=True)
        
        # Save Checkpoint
        torch.save(model.state_dict(), f"angel_checkpoint_e{epoch}.pt")

if __name__ == "__main__":
    train()
