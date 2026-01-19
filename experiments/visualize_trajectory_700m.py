
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from pathlib import Path
import sys

# Load Data
LOG_FILE = "results/phase9_trajectories_700m/semantic_trajectory.jsonl"
OUTPUT_IMG = "results/phase9_trajectories_700m/trajectory_plot_700m.png"

def load_trajectories(path):
    data = []
    if not Path(path).exists():
        print(f"❌ File not found: {path}")
        return []
        
    with open(path) as f:
        for line in f:
            if line.strip():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return data

def visualize():
    print(f"📉 Loading 700M Trajectories from {LOG_FILE}...")
    steps = load_trajectories(LOG_FILE)
    if not steps:
        print("❌ No data found.")
        return

    # Organize: {prompt: [v1, v2, ...]}
    history = {}
    all_vectors = []
    
    # Get prompts from first valid step
    prompts = list(steps[0]["vectors"].keys())
    
    for prompt in prompts:
        history[prompt] = []
        for step in steps:
            vec = step["vectors"].get(prompt)
            if vec:
                history[prompt].append(vec)
                all_vectors.append(vec)
    
    print(f"    Loaded {len(steps)} frames for {len(prompts)} concepts.")
    
    # PCA to 2D
    print("    Projecting to 2D...")
    pca = PCA(n_components=2)
    pca.fit(all_vectors)
    
    # Plot
    plt.figure(figsize=(14, 12)) # Larger canvas for high res
    cmap = plt.get_cmap('tab20') # More colors for more tracers
    
    for i, prompt in enumerate(prompts):
        vecs = np.array(history[prompt])
        coords = pca.transform(vecs)
        
        # Plot Path
        label = (prompt[:30] + '...') if len(prompt) > 30 else prompt
        color = cmap(i % 20)
        
        # Draw line
        plt.plot(coords[:, 0], coords[:, 1], '-', linewidth=1.5, color=color, alpha=0.6, label=label)
        
        # Draw dots (frames) - smaller for 50 epochs
        plt.scatter(coords[:, 0], coords[:, 1], s=10, color=color, alpha=0.8)
        
        # Mark Start/End
        plt.text(coords[0, 0], coords[0, 1], "Start", fontsize=8, color=color)
        plt.text(coords[-1, 0], coords[-1, 1], "End", fontsize=9, fontweight='bold', color=color)
        
        # Draw arrows every 10 steps to show flow direction
        for j in range(0, len(coords)-1, 5):
             plt.arrow(coords[j, 0], coords[j, 1], 
                  coords[j+1, 0] - coords[j, 0], 
                  coords[j+1, 1] - coords[j, 1], 
                  color=color, alpha=0.5, width=0.001)

    plt.title("Semantic Orbital Mechanics (LFM2-700M - 50 Epochs)")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    
    plt.savefig(OUTPUT_IMG, dpi=200) # High DPI
    print(f"✅ Plot saved to {OUTPUT_IMG}")

if __name__ == "__main__":
    visualize()
