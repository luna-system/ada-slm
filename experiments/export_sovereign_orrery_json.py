
import json
import numpy as np
from sklearn.decomposition import PCA
from pathlib import Path

# Config
LOG_FILE = "results/phase10_trajectories/semantic_trajectory.jsonl"
OUTPUT_JSON = "/home/luna/Code/ada/neuro-cartographer/web/public/data/sovereign_v4b_map.json"
OUTPUT_IMG_DEST = "/home/luna/Code/ada/neuro-cartographer/web/public/sovereign_orrery_v4b.png"
INPUT_IMG = "results/phase10_trajectories/sovereign_orrery_v4b.png"

# Color Mappings (Reusable)
COLOR_MAP = {
    "ROOT": "#FF0000",
    "SACRAL": "#FF7F00",
    "SOLAR": "#FFD700",
    "HEART": "#00FF00",
    "THROAT": "#00FFFF",
    "EYE": "#4B0082",
    "CROWN": "#8B00FF",
    "VOID": "#000000",
    "SUN": "#FFA500",
    "MOON": "#C0C0C0",
    "MARS": "#B22222",
    "MERCURY": "#00CED1",
    "JUPITER": "#800080",
    "VENUS": "#FF69B4",
    "SATURN": "#8B4513",
    "Sovereign": "#FFFFFF",
    "Active": "#32CD32",
    "Idle": "#A9A9A9"
}

def get_config(prompt):
    for key, color in COLOR_MAP.items():
        if key in prompt:
            is_star = "SUN" in prompt or "Sovereign" in prompt
            radius = 5.0 if is_star else 3.0
            mass = 1.0 if is_star else 0.5
            return color, "star" if is_star else "planet", radius, mass
    
    return "#808080", "planet", 2.0, 0.2

def load_data(path):
    data = []
    with open(path) as f:
        for line in f:
            if line.strip(): data.append(json.loads(line))
    return data

def export():
    print("🔮 Generating 3D Orrery JSON...")
    steps = load_data(LOG_FILE)
    if not steps: return

    # Get Final Step Prompts
    final_step = steps[-1]["vectors"]
    prompts = list(final_step.keys())
    
    # Collect All Vectors for Global PCA (Time + Space)
    all_vectors = []
    for step in steps:
        for p in prompts:
            if p in step["vectors"]:
                all_vectors.append(step["vectors"][p])
    
    # PCA to 3D
    pca = PCA(n_components=3)
    pca.fit(all_vectors)
    
    # Transform Final Positions Only
    final_vectors = [final_step[p] for p in prompts]
    coords_3d = pca.transform(final_vectors)
    
    # Scale coordinates to reasonable Orrery size (e.g. -10 to 10)
    # Norm to max 10
    max_val = np.max(np.abs(coords_3d))
    coords_3d = (coords_3d / max_val) * 10
    
    # Build JSON
    output = {
        "attractors": [],
        "nodes": []
    }
    
    for i, prompt in enumerate(prompts):
        color, type_, radius, mass = get_config(prompt)
        clean_name = prompt.replace("⧈[Expert: ", "").replace("]", "")
        
        # Add as Attractor (Planet)
        attractor = {
            "name": clean_name,
            "type": type_,
            "pos": coords_3d[i].tolist(),
            "mass": mass,
            "color": color,
            "radius": radius
        }
        output["attractors"].append(attractor)
        
        # Add as Node (Clickable Label)
        node = {
            "id": i,
            "label": clean_name,
            "category": "Sovereign_Well",
            "pos": coords_3d[i].tolist(),
            "metadata": {
                "phase": "v4B",
                "full_prompt": prompt
            }
        }
        output["nodes"].append(node)
        
    # Save JSON
    with open(OUTPUT_JSON, "w") as f:
        json.dump(output, f, indent=2)
    print(f"✅ JSON Map saved to {OUTPUT_JSON}")
    
    # Copy Static PNG
    import shutil
    try:
        shutil.copy(INPUT_IMG, OUTPUT_IMG_DEST)
        print(f"✅ Static PNG copied to {OUTPUT_IMG_DEST}")
    except FileNotFoundError:
        print("⚠️  Could not copy static PNG (source missing?)")

if __name__ == "__main__":
    export()
