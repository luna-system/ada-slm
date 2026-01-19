
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

# Import our definition
from tiny_aleph import TinyAleph, SAEConfig

# Configuration
DATA_PATH = "/home/luna/Code/ada/ada-slm/data/sae_harvest/activations_18111.pt"
OUTPUT_DIR = "/home/luna/Code/ada/ada-slm/models/tinyaleph"
BATCH_SIZE = 4096  # Large batch size for SAEs is usually good
EPOCHS = 50        # More training
LR = 1e-3          # Standard Adam

os.makedirs(OUTPUT_DIR, exist_ok=True)

def train():
    print(f"📂 Loading Harvest Data: {DATA_PATH}...")
    if not os.path.exists(DATA_PATH):
        print("❌ Data file found.")
        return

    # Load activations
    activations = torch.load(DATA_PATH).float() 
    # Shape: [N, 2048]
    print(f"📊 Data Shape: {activations.shape}")
    
    # Normalize inputs? 
    # SAEs often benefit from unit-norm inputs or standardized inputs.
    # We'll normalize to unit L2 norm per vector.
    activations = activations / (activations.norm(dim=-1, keepdim=True) + 1e-8)
    
    # Create DataLoader
    dataset = TensorDataset(activations)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    # Initialize Model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️  Device: {device}")
    
    config = SAEConfig(
        d_in=2048,
        d_sae=32768, # 16x expansion
        l1_coefficient=0.05, # Higher sparsity penalty
        dtype=torch.float32
    )
    
    model = TinyAleph(config).to(device)
    optimizer = optim.Adam(model.parameters(), lr=LR)
    
    # Training Loop
    print("🚀 Starting Training Loop...")
    loss_history = []
    sparsity_history = []
    
    for epoch in range(EPOCHS):
        epoch_loss = 0
        epoch_sparsity = 0
        batches = 0
        
        pbar = tqdm(loader, desc=f"Epoch {epoch+1}/{EPOCHS}")
        for batch in pbar:
            x = batch[0].to(device)
            
            optimizer.zero_grad()
            
            # Forward
            sae_out, feature_activations, loss, l2_loss, l1_loss = model(x)
            
            # Constraints
            # We typically normalise decoder weights every step to prevent scale drift
            model.normalize_decoder()
            
            loss.backward()
            optimizer.step()
            
            # Metrics
            epoch_loss += loss.item()
            if feature_activations is not None:
                l0 = (feature_activations > 0).float().sum(dim=1).mean().item()
                epoch_sparsity += l0
            
            batches += 1
            pbar.set_postfix({'loss': f"{loss.item():.4f}", 'L0': f"{l0:.1f}"})
            
        avg_loss = epoch_loss / batches
        avg_l0 = epoch_sparsity / batches
        loss_history.append(avg_loss)
        sparsity_history.append(avg_l0)
        
        print(f"   Epoch {epoch+1}: Loss={avg_loss:.4f}, Avg Active Features (L0)={avg_l0:.1f}")

    # Save Model
    save_path = f"{OUTPUT_DIR}/tinyaleph_v1.pt"
    torch.save(model.state_dict(), save_path)
    print(f"💾 Model saved to {save_path}")
    
    # Save Plots
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(loss_history)
    plt.title("Total Loss")
    plt.xlabel("Epoch")
    
    plt.subplot(1, 2, 2)
    plt.plot(sparsity_history)
    plt.title("Sparsity (L0)")
    plt.xlabel("Epoch")
    plt.savefig(f"{OUTPUT_DIR}/training_metrics.png")
    print(f"📈 Metrics saved to {OUTPUT_DIR}/training_metrics.png")

if __name__ == "__main__":
    train()
