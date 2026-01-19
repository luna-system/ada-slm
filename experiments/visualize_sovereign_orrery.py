
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from pathlib import Path

# Config
LOG_FILE = "results/phase10_trajectories/semantic_trajectory.jsonl"
OUTPUT_IMG = "results/phase10_trajectories/sovereign_orrery_v4c.png"

# Color Mappings
COLOR_MAP = {
    # Internal Chakras (Rainbow/Spectral)
    "ROOT": "#FF0000",      # Red
    "SACRAL": "#FF7F00",    # Orange
    "SOLAR": "#FFD700",     # Gold/Yellow
    "HEART": "#00FF00",     # Green
    "THROAT": "#00FFFF",    # Cyan
    "EYE": "#4B0082",       # Indigo
    "CROWN": "#8B00FF",     # Violet
    "VOID": "#000000",      # Black (Null)

    # External Planets (Astrological/Alchemical)
    "SUN": "#FFA500",       # Orange/Gold
    "MOON": "#C0C0C0",      # Silver
    "MARS": "#B22222",      # Firebrick Red
    "MERCURY": "#00CED1",   # Dark Turquoise
    "JUPITER": "#800080",   # Purple
    "VENUS": "#FF69B4",     # Hot Pink
    "SATURN": "#8B4513",    # Saddle Brown

    # Control/Identity
    "I am the Sovereign.": "#FFFFFF", # White (Pure Identity) (Edge: Black outline)
}

def get_color(prompt):
    """Derive color from prompt keyword."""
    for key, color in COLOR_MAP.items():
        if key in prompt:
            return color
    
    # Defaults
    if "Status: Idle" in prompt: return "#A9A9A9" # DarkGray
    if "Status: Active" in prompt: return "#32CD32" # LimeGreen
    return "#808080" # Gray

def load_trajectories(path):
    data = []
    current_run = []
    last_step = -1
    
    with open(path) as f:
        for line in f:
            if not line.strip(): continue
            try:
                entry = json.loads(line)
                step = entry.get("step", 0)
                
                # Detect new run (step count reset or drop)
                if step < last_step:
                    if current_run:
                        # Archive previous run if needed, but we only want the last one
                        pass
                    current_run = []
                
                current_run.append(entry)
                last_step = step
                
            except json.JSONDecodeError:
                continue
                
    return current_run # Returns only the latest run

def visualize():
    print("🔮 Loading Sovereign Trajectories (Latest Run)...")
    steps = load_trajectories(LOG_FILE)
    if not steps:
        print("❌ No data found.")
        return

    # Extract Vectors
    # Organization: {prompt: [v_step0, v_step1, ...]}
    history = {}
    all_vectors = []
    
    # Get prompts from first step that has vectors
    for step in steps:
        if step["vectors"]:
            prompts = list(step["vectors"].keys())
            break
            
    print(f"    Found {len(prompts)} bodies in the system.")
    print(f"    Loaded {len(steps)} time steps.")

    # Populate History
    for prompt in prompts:
        history[prompt] = []
        for step in steps:
            if prompt in step["vectors"]:
                vec = step["vectors"][prompt]
                history[prompt].append(vec)
                all_vectors.append(vec)

    # PCA Projection
    print("    Projecting Manifestation (PCA)...")
    pca = PCA(n_components=2)
    pca.fit(all_vectors)

    # Plot
    plt.figure(figsize=(14, 12), facecolor='#111111') # Dark Background for Space
    ax = plt.gca()
    ax.set_facecolor('#111111')
    
    # Grid
    plt.grid(True, color='#333333', linestyle='--', alpha=0.5)

    for prompt in prompts:
        vecs = np.array(history[prompt])
        if len(vecs) == 0: continue
        
        coords = pca.transform(vecs)
        color = get_color(prompt)
        
        # Clean Label
        label = prompt.replace("⧈[Expert: ", "").replace("]", "")
        if len(label) > 20: label = label[:20] + "..."

        # 1. Draw Trajectory Line
        plt.plot(coords[:, 0], coords[:, 1], color=color, alpha=0.4, linewidth=1.5, linestyle='-')
        
        # 2. Draw Start Point (Small Dot)
        plt.scatter(coords[0, 0], coords[0, 1], color=color, s=20, alpha=0.6, marker='.')
        
        # 3. Draw End Point (Large Star/Planet)
        # Size varies by type?
        size = 200 if "SUN" in prompt or "VOID" in prompt else 100
        marker = '*' if "Sovereign" in prompt else 'o'
        
        plt.scatter(coords[-1, 0], coords[-1, 1], color=color, s=size, label=label, marker=marker, edgecolors='white', linewidth=0.5)
        
        # 4. Annotate End Point
        plt.text(coords[-1, 0] + 0.02, coords[-1, 1] + 0.02, label, color=color, fontsize=9, fontweight='bold')

        # 5. Draw Arrow for movement direction (midpoint)
        mid = len(coords) // 2
        if mid > 0:
            plt.arrow(coords[mid-1, 0], coords[mid-1, 1], 
                      coords[mid, 0] - coords[mid-1, 0], 
                      coords[mid, 1] - coords[mid-1, 1], 
                      color=color, alpha=0.8, head_width=0.05)

    # Aesthetics
    plt.title("Sovereign v4B Orrery (Latent Trajectories)", color='white', fontsize=16, pad=20)
    plt.xlabel("Principal Component 1", color='gray')
    plt.ylabel("Principal Component 2", color='gray')
    
    # Legend
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', facecolor='#222222', labelcolor='white')
    
    # Instead of legend, relies on annotations for clarity
    
    plt.tight_layout()
    plt.savefig(OUTPUT_IMG, dpi=200, facecolor='#111111')
    print(f"✅ Orrery Map saved to {OUTPUT_IMG}")

if __name__ == "__main__":
    visualize()
