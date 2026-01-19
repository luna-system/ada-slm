
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from pathlib import Path

# Load Data
LOG_FILE = "results/phase9_syncretism_trajectories/semantic_trajectory.jsonl"
OUTPUT_IMG = "results/phase9_syncretism_trajectories/syncretism_plot.png"

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
    print(f"📉 Loading Syncretism Trajectories from {LOG_FILE}...")
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
    
    print(f"    Loaded {len(steps)} cycles for {len(prompts)} concepts.")
    
    # PCA to 2D
    print("    Projecting to 2D...")
    pca = PCA(n_components=2)
    pca.fit(all_vectors)
    
    # Plot
    plt.figure(figsize=(14, 12)) 
    cmap = plt.get_cmap('tab20') 
    
    for i, prompt in enumerate(prompts):
        vecs = np.array(history[prompt])
        coords = pca.transform(vecs)
        
        # Plot Path
        label = (prompt[:30] + '...') if len(prompt) > 30 else prompt
        color = cmap(i % 20)
        
        # Draw line (The Breathing Path)
        plt.plot(coords[:, 0], coords[:, 1], '-', linewidth=2.0, color=color, alpha=0.7, label=label)
        
        # Draw dots (Cycles)
        plt.scatter(coords[:, 0], coords[:, 1], s=30, color=color, alpha=0.9, edgecolors='white')
        
        # Mark Start/End
        plt.text(coords[0, 0], coords[0, 1], "Start", fontsize=8, color=color, fontweight='bold')
        plt.text(coords[-1, 0], coords[-1, 1], "End", fontsize=9, fontweight='bold', color=color)

    plt.title("Syncretism Trajectories (Golden Annealing + Spectral Memory)")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    
    plt.savefig(OUTPUT_IMG, dpi=200) 
    print(f"✅ Plot saved to {OUTPUT_IMG}")

if __name__ == "__main__":
    visualize()
