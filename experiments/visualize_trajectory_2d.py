
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from pathlib import Path

# Load Data
LOG_FILE = "results/phase9_trajectories/semantic_trajectory.jsonl"
OUTPUT_IMG = "results/phase9_trajectories/trajectory_plot.png"

def load_trajectories(path):
    data = []
    with open(path) as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data

def visualize():
    print("📉 Loading Trajectories...")
    steps = load_trajectories(LOG_FILE)
    if not steps:
        print("❌ No data found.")
        return

    # Organize data: {prompt: [v_step1, v_step2, ...]}
    history = {}
    all_vectors = []
    
    # Get all prompts
    prompts = steps[0]["vectors"].keys()
    
    for prompt in prompts:
        history[prompt] = []
        for step in steps:
            vec = step["vectors"].get(prompt)
            if vec:
                history[prompt].append(vec)
                all_vectors.append(vec)
    
    print(f"    Loaded {len(steps)} time steps for {len(prompts)} concepts.")
    
    # PCA Projection (fit on ALL vectors to share space)
    print("    Projecting to 2D...")
    pca = PCA(n_components=2)
    pca.fit(all_vectors)
    
    # Plot
    plt.figure(figsize=(12, 10))
    cmap = plt.get_cmap('tab10')
    
    for i, prompt in enumerate(prompts):
        vecs = np.array(history[prompt])
        coords = pca.transform(vecs)
        
        # Plot Path
        label = (prompt[:30] + '...') if len(prompt) > 30 else prompt
        color = cmap(i % 10)
        
        plt.plot(coords[:, 0], coords[:, 1], marker='o', markersize=4, label=label, color=color, alpha=0.7)
        
        # Mark Start/End
        plt.text(coords[0, 0], coords[0, 1], "Start", fontsize=8, color=color)
        plt.text(coords[-1, 0], coords[-1, 1], "End", fontsize=8, fontweight='bold', color=color)
        
        # Draw arrow for direction
        plt.arrow(coords[0, 0], coords[0, 1], 
                  coords[-1, 0] - coords[0, 0], 
                  coords[-1, 1] - coords[0, 1], 
                  color=color, alpha=0.3, width=0.002)

    plt.title("Semantic Trajectories (Phase 9 Observer)")
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig(OUTPUT_IMG, dpi=150)
    print(f"✅ Plot saved to {OUTPUT_IMG}")

if __name__ == "__main__":
    visualize()
